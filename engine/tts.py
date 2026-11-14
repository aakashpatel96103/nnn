"""OPTIONAL fallback voice-over when the user gives only a script and explicitly agrees to an AI voice.
The user's own recorded voice is ALWAYS preferred - ask for it first.

usage:
  python engine/tts.py <project_dir> [--voice hi-IN-MadhurNeural] [--rate +8%]

Reads inputs/script.txt, writes inputs/vo.mp3 using edge-tts (free, needs internet).
Hindi/Hinglish voices: hi-IN-MadhurNeural (male), hi-IN-SwaraNeural (female).
English (India): en-IN-PrabhatNeural, en-IN-NeerjaNeural.
"""
import argparse, asyncio
from pathlib import Path


async def run(text, voice, rate, out):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--voice", default="hi-IN-MadhurNeural")
    ap.add_argument("--rate", default="+8%")
    a = ap.parse_args()
    proj = Path(a.project).resolve()
    text = " ".join(l.strip() for l in (proj / "inputs" / "script.txt").read_text(encoding="utf-8").splitlines() if l.strip())
    out = proj / "inputs" / "vo.mp3"
    if out.exists():
        raise SystemExit("inputs/vo.mp3 already exists - not overwriting")
    asyncio.run(run(text, a.voice, a.rate, out))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
