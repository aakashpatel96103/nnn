"""Word-level timestamps for a voice-over, aligned to the approved script spelling.

usage:
  python engine/transcribe.py <project_dir> [--audio inputs/vo.mp3] [--script inputs/script.txt] [--lang auto|en|hi] [--model small]

--lang auto (default): Hinglish written in Latin letters transcribes best as "en" (whisper "hi" outputs
Devanagari or hallucinates). auto tries en, then hi if the match is < 80%, and keeps the best.

Writes:
  src/words_raw.json  - whisper's own words  [{w,s,e}]
  src/words.json      - final caption words  [{w,s,e,line}]  (script spelling, whisper timing)

Lines: each non-empty line of script.txt is one "line" (scene/chapter) - captions never span two lines.
If there is no script, whisper words are used as-is (line = sentence index).
Alignment: difflib over normalized tokens; script words with no whisper match get interpolated times.
After running, ALWAYS spot-check 3-4 words against the audio (render snaps at their .s times).
"""
import argparse, difflib, json, re, sys
from pathlib import Path


def norm(w: str) -> str:
    w = w.lower()
    w = re.sub(r"[^\w]", "", w)
    # common Hinglish whisper variants
    for a, b in (("ph", "f"), ("oo", "u"), ("ee", "i"), ("aa", "a"), ("w", "v"), ("z", "j")):
        w = w.replace(a, b)
    return w


def load_whisper_words(audio: Path, lang: str, model_name: str, prompt: str):
    import whisper  # openai-whisper
    model = whisper.load_model(model_name)
    res = model.transcribe(str(audio), language=lang, word_timestamps=True,
                           initial_prompt=prompt[:800] if prompt else None, fp16=False)
    out = []
    for seg in res["segments"]:
        for w in seg.get("words", []):
            t = w["word"].strip()
            if t:
                out.append({"w": t, "s": round(float(w["start"]), 3), "e": round(float(w["end"]), 3)})
    return out


def align(script_lines, raw):
    sw = []  # (word, line)
    for li, line in enumerate(script_lines):
        for w in line.split():
            sw.append((w, li))
    a = [norm(w) for w, _ in sw]
    b = [norm(x["w"]) for x in raw]
    times = [None] * len(sw)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (raw[j1 + k]["s"], raw[j1 + k]["e"])
        elif tag == "replace":
            # spread the whisper span over the script words (handles merges like set+up -> setup)
            s, e = raw[j1]["s"], raw[j2 - 1]["e"]
            n = i2 - i1
            for k in range(n):
                times[i1 + k] = (round(s + (e - s) * k / n, 3), round(s + (e - s) * (k + 1) / n, 3))
    # interpolate gaps (script words whisper missed)
    for i in range(len(times)):
        if times[i] is None:
            prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
            nxt_i = next((j for j in range(i + 1, len(times)) if times[j]), None)
            nxt = times[nxt_i][0] if nxt_i is not None else prev + 0.3
            gap_n = (nxt_i if nxt_i is not None else len(times)) - i + 1
            times[i] = (round(prev, 3), round(prev + (nxt - prev) / gap_n, 3))
    words = []
    for (w, li), (s, e) in zip(sw, times):
        if words and s < words[-1]["s"]:
            s = words[-1]["s"]
        words.append({"w": w, "s": round(s, 3), "e": round(max(e, s + 0.06), 3), "line": li})
    matched = sum(1 for tag, i1, i2, *_ in sm.get_opcodes() if tag == "equal" for _ in range(i2 - i1))
    return words, matched / max(1, len(sw))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--audio", default="inputs/vo.mp3")
    ap.add_argument("--script", default="inputs/script.txt")
    ap.add_argument("--lang", default="auto")
    ap.add_argument("--model", default="small")
    ap.add_argument("--raw", help="reuse an existing words_raw.json instead of running whisper")
    a = ap.parse_args()
    proj = Path(a.project).resolve()
    audio = proj / a.audio
    if not audio.exists() and a.audio == "inputs/vo.mp3":
        audio = next((x for x in sorted((proj / "inputs").glob("vo.*")) if x.suffix.lower() in
                      (".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac", ".opus", ".mp4")), audio)
    script_p = proj / a.script
    script_lines = [l.strip() for l in script_p.read_text(encoding="utf-8").splitlines() if l.strip()] if script_p.exists() else []
    (proj / "src").mkdir(exist_ok=True)
    if a.raw:
        raw = json.loads(Path(a.raw).read_text(encoding="utf-8"))
    else:
        if not audio.exists():
            sys.exit(f"no audio at {audio}")
        langs = ["en", "hi"] if a.lang == "auto" else [a.lang]
        best = None
        for lg in langs:
            r = load_whisper_words(audio, lg, a.model, " ".join(script_lines))
            score = align(script_lines, r)[1] if script_lines else len(r)
            print(f"whisper lang={lg}: {len(r)} words" + (f", match {score:.0%}" if script_lines else ""))
            if best is None or score > best[0]:
                best = (score, r)
            if script_lines and score >= 0.8:
                break
        raw = best[1]
    (proj / "src" / "words_raw.json").write_text(json.dumps(raw, ensure_ascii=False, indent=0), encoding="utf-8")
    if script_lines:
        words, ratio = align(script_lines, raw)
        print(f"aligned {len(words)} script words to {len(raw)} whisper words, exact match {ratio:.0%}")
        if ratio < 0.6:
            print("WARNING: low match - check that script.txt is what was actually spoken; fix words.json by hand")
    else:
        words, li = [], 0
        for x in raw:
            words.append({**x, "line": li})
            if re.search(r"[.!?।]$", x["w"]):
                li += 1
        print(f"no script.txt - used {len(words)} whisper words as captions (verify spelling!)")
    (proj / "src" / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
    end = raw[-1]["e"] if raw else 0
    print(f"speech ends at {end:.2f}s -> suggested duration {end + 0.6:.1f}s (set project.json 'duration')")
    for li in sorted({w['line'] for w in words}):
        ws = [w for w in words if w["line"] == li]
        print(f"  line {li}: {ws[0]['s']:.2f}-{ws[-1]['e']:.2f}s  {' '.join(w['w'] for w in ws)}")


if __name__ == "__main__":
    main()
