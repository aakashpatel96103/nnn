# 06 — Build the composition (src/reel.html)

`new_project.py` copied `template/reel.html`. It already renders (placeholder content). Turn it into this reel:

## 1. Timing from words.json
Print the words with times (`python -c "import json;[print(w['line'],w['s'],w['w']) for w in json.load(open('projects/<slug>/src/words.json',encoding='utf-8'))]"`).
- `SC` = scene start times = start of the line(s) that open each scene (first scene = 0).
- `HL_T` = time the highlighted word is spoken in each scene.
- `KICK` = 2–4 biggest visual hits (stamp, DONE, final click). Put the hit ON the spoken keyword (± 0.1 s).
- `WIPE` = `{a: SC[last]-.34, m: SC[last], b: SC[last]+.34}` (CTA scene) or `null`.
- `END_T` = after the last word of the CTA, ≥ 1.2 s before `DUR`.
- `CURSOR` = `[t, x, y, click]` in world coordinates (the same px as the element positions in CSS), `null` to hide.
- `CRUMBS`, `KEYW`, `HANDLE`.

## 2. Content
- One `.head` per scene (`id h0..hN`, highlighter `hl0..hN`, `data-qa-text`). Two `<span class="l">` lines.
- Scene bodies: replace the placeholders with real UI. Use screenshots in `assets/` as reference: open them,
  measure layout, copy exact labels/colors/icons (simple inline SVG or CSS shapes; logos can be `<img>` of the
  cropped screenshot area — crop with PIL into `assets/`). Image paths are relative to `src/` → `../assets/x.png`.
- Screen recordings: frames are in `assets/<name>_frames/` (2 fps). Either rebuild the UI states as HTML (best) or
  show a short clip: put the mp4 in `assets/` and drive `<video>` currentTime from `render(t)` (set `video.currentTime`
  and wait is NOT possible inside render — instead pre-extract frames at 30 fps with ffmpeg into a folder and swap an
  `<img>` src per frame: `img.src = '../assets/clip/' + String(Math.floor((t-a)*30)+1).padStart(4,'0') + '.png'`).
- Every scene fx is a pure function of `t` in `SCENE_FX`. Use the helpers: `pop`, `card`, `head`, `typeText`,
  `check`, `P`, `eo`, `eio`, `back`, `lerp`. No `setTimeout`, no CSS transitions/animations, no `Date`, no randomness
  without a fixed seed — the renderer jumps to arbitrary t.
- Add/remove scenes by adding/removing entries in `SC`, `CRUMBS`, `HL_T`, `.head` elements and `SCENE_FX` together.
- Mark headline/sticker blocks `data-qa-text` so QA checks overlaps; decoration `data-qa-ignore`.

## 3. Check fast, often
```
python engine/render.py projects/<slug> snap projects/<slug>/review/s <mid of each scene> <each beat> <wipe a,m,b> <END_T+.6>
python engine/contact.py projects/<slug>/review/s projects/<slug>/review/sheet.jpg --cols 4
python engine/qa.py projects/<slug>
python engine/render.py projects/<slug> measure 6.5 card1 s1   # exact boxes when aligning
```
Delete old snaps before a new round (`review/s` is yours) so the sheet only shows the current state.

## 4. Footage reels
If the user wants their face/camera footage, keep this style as overlays: put the footage as a full-bleed frame
sequence behind `#world` (or in a rounded card), and follow `skills/edit-video` + `skills/text-over-footage` /
`skills/adaptive-glass` for cut and caption rules. Still render through `render.py` so QA works.
