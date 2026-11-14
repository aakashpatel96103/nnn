# 09 — Lessons & pitfalls (learned making the reference reel)

- `window.render(t)` must be pure. Anything time-based outside it (CSS animation, setTimeout, video playback) renders
  wrong or flickers in the frame-by-frame render.
- Whisper splits/merges words ("set up", "doon ga"); transcribe.py aligns to the script spelling — always pass the
  script. Check words that carry a keyword highlight or a sound cue.
- Captions break on punctuation, ≥ 4 words, a pause > 0.22 s, or a new script line. Write script punctuation on purpose.
- cues.json `total` is seconds, not frames (mix.py fixes it).
- Clicks/pops feel late if placed at animation start; use the visible peak (2–4 frames later).
- A full-width headline box makes QA think text hits the edges — qa.py measures glyphs, so keep text in text nodes
  (not only in pseudo-elements) for it to be checked.
- Headline top < 200 px triggers safe-area WARN (IG top bar). Template uses 262 px.
- The wipe must hide the swap: switch scene content exactly at `WIPE.m` and hide the old scene's elements after it.
- Viewing images: one contact sheet per message; many images in one message can hit the image limit.
- Don't run `python -I` (playwright in user site-packages). Use the interpreter doctor printed.
- Never overwrite an export; mix.py versions automatically. Never delete the user's inputs.
- The avatar path in reel.html is `../assets/avatar.png` (new_project copies brand/avatar.png there).
- On non-Windows systems Segoe UI / Cascadia Mono are missing → fallbacks render slightly wider: re-run qa.py,
  shrink headline font-size if text overflows.
- Caption keyword regex must match whole words (`/^(FREE|API|AI)…$/i`), else "main" lights up because it contains "ai".
- Hinglish voice: whisper `--lang en` + script prompt gives ~100% match; `hi` gives Devanagari/garbage. transcribe.py `--lang auto` handles it.
