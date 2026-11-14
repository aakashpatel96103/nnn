# 04 — Voice & word timings

## Get the voice
1. **Best: user's own voice.** Send them the script + notes: quiet room, phone 15–20 cm from mouth, energetic
   (smile while talking), small pause between lines, no music. Any format (mp3/m4a/wav/ogg). Save as `inputs/vo.<ext>`.
2. **AI voice only with explicit consent** (it sends the text to Microsoft's edge TTS service):
   `python engine/tts.py projects/<slug>` (default `hi-IN-MadhurNeural`, rate +8%; try `--voice hi-IN-SwaraNeural`).
   It refuses to overwrite an existing `vo.*`.
3. Clean-up only if needed (noise, long silences): keep a copy, write the cleaned file as `inputs/vo-clean.wav`,
   ask before replacing. Trim leading silence to ≤ 0.3 s so the hook starts instantly.

## Transcribe
```
python engine/transcribe.py projects/<slug>            # uses inputs/vo.* + inputs/script.txt, whisper small, --lang auto (en first: Hinglish in Latin letters; hi only if en matches badly)
```
- Output: `src/words.json` = `[{"w","s","e","line"}]` with the SCRIPT spelling (FREE, API, "CLAUDE") and whisper timing.
- Read the printed match ratio. ≥ 80 % fine. 60–80 % → spot-check 5 words by playing the audio around them
  (or snap captions at those times). < 60 % → the script does not match what was said: ask the user or
  transcribe without `--script` and rebuild script.txt from what was really said.
- `--model medium` for better timing on noisy audio (slower). `--lang en` forces English; `--lang hi` only for Devanagari scripts.
- Never hand-type timings. If one word is off, fix only that entry's `s/e` in words.json.

## Duration
`project.json` → `duration` = voice end + 0.6 s (printed by transcribe), plus extra if the end card plays after
the voice (end card needs ~1.2 s visible). Keep 15–30 s; > 35 s needs a reason.
