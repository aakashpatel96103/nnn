# 08 — QA checklist (go through ALL of it before delivery)

Automatic (must pass):
- [ ] `python engine/qa.py projects/<slug>` → 0 FAIL (DOM: clipped text, cut by frame, overlap, caption size, page errors)
- [ ] `python engine/qa.py projects/<slug> --video export/<slug>.mp4` → 0 FAIL (1080×1920, h264 yuv420p, 30 fps,
      durations match, AAC audio, decodes clean, no black frames, loudness −16.5…−11.5 LUFS, true peak ≤ −0.9 dBTP)
- [ ] Every WARN judged: fixed, or deliberately kept and told to the user.

By eye (contact sheet of the EXPORT every 0.5 s + a few full-size snaps):
- [ ] Frame 0 already shows the hook headline + a visual (no blank/fade-in start).
- [ ] Every headline readable, ≤ 2 lines, accent word + highlighter present, nothing touching edges.
- [ ] Spelling: tool names, CTA word, Hinglish words consistent with the script.
- [ ] No two things fighting for the same spot (sticker over headline, caption over UI text, cursor hiding a label).
- [ ] UI looks real (labels, colors) and every number/claim matches research.md.
- [ ] Something meaningful moves every 1–2 s; no dead stretch (> 1.2 s still).
- [ ] Scene changes carry (slide/scale), no flash or empty frame between scenes; ONE wipe max and it fully covers at the peak.
- [ ] Captions: in sync with the voice (±1 frame feel), chunk ≤ 4 words, keyword highlight right, never covering the UI focus.
- [ ] Cursor moves to targets smoothly and presses exactly when the click sound plays.
- [ ] CTA scene: WORD visibly typed, Post clicked, DM payoff shown; end card avatar + handle + Following.
- [ ] Last frame is not cut mid-animation; end card visible ≥ 1.2 s.

By ear (sync strips `mix.py check` + measured numbers):
- [ ] Voice clear and on top; SFX audible but under the voice.
- [ ] Each cue's spike sits on its marker (± 1 frame). Clicks on presses, pops on stamps.
- [ ] No clipping, no harsh stacked hits, no silence gap at start.

Delivery:
- [ ] Export path, duration, LUFS/peak numbers, versions, open WARNs, and what you could NOT check (you cannot
      hear — say you verified sync by waveform strips/measurements, not by listening).
- [ ] Caption + hashtags + pinned comment + cover frame time.
