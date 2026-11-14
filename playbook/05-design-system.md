# 05 — Design system (the @mukku.tech look)

Look at `reference/example-reel/contact-sheet.jpg` first. Palette and type: `brand/mukku-brand.md`.

## Canvas
- 1080×1920, 30 fps. Paper `#F6F3EE` + 54 px grid, two warm blurred glows drifting slowly in the lower half, soft vignette.
- **One continuous canvas, no hard cuts.** Cards slide/scale in, carry up and out; the next scene arrives while the
  last leaves. The only "cut" is ONE halftone wipe (clay dots from bottom-left) into the CTA scene.
- `#world` holds everything that zooms; chrome, captions, end card, cursor sit outside it.

## Safe areas (Instagram UI)
- Design area: x 72–1008, y 262–1250 for headline + UI. Captions at top 1236. End card y ≈ 1384–1534.
- Nothing important below y 1700 (IG caption/buttons) or above y 200 (except the chrome bar). qa.py enforces
  x 60–1020, y 200–1700.

## Layers per scene (top to bottom)
1. **Chrome** (always): `// 0N — WORD` mono breadcrumb left, `0N / 0M` counter right, clay progress bar.
2. **Headline** (y ≈ 262): 2 lines, bold sans, ONE italic serif clay accent, ONE highlighter swipe on the key
   word at the moment it is spoken. ≤ 22 characters per line at 92–100 px.
3. **Proof UI** (y ≈ 520–1150): real UI rebuilt in HTML from screenshots — model pickers, key cards, settings,
   terminals, tiles, checklists, comment box. Crisp, simplified, real labels. Max 780 px wide card.
4. **Sticker** (1 per scene): short (≤ 14 chars) — "100% FREE", "TUM BHI!", "Bas itna hi!" — pops with overshoot
   and a ±3–6° tilt, on a beat.
5. **Cursor**: an arrow that moves (eased) to what matters and clicks (scale press 0.82) — every click = a sound.
6. **Captions**: word-synced pill (chunks of ≤ 4 words), spoken words ink, upcoming grey, keywords clay.
7. **End card**: avatar + @mukku.tech + Follow → "Following" click, last ~1.4 s, after the CTA payoff.

## Motion grammar
- Ease out with slight overshoot (`back`) for arrivals 280–360 ms; ease-in-out for moves; exits 220–320 ms, carry up.
- Camera: base scale 1.04, slow push +0.03 per scene, beat kicks (`sin(πx)(1−x)·0.05` over 0.4 s) on the 2–4 biggest hits.
- Something meaningful changes every 1–2 s (check, stamp, type, click, count). No still frame > 1.2 s.
- Stagger lists 120 ms per row; check marks 300–400 ms apart, each with a tick sound.
- Typing: ~10–14 chars/s with a blinking caret, then a DONE pill.
- Never: spinning, bouncing loops, rainbow gradients, emoji spam, stock icons, drop shadows on text, more than
  2 fonts + mono.

## Scene recipes that work (see reference reel.html)
- **Model/tool picker**: list rows with icons + green FREE chips stamping in one after another.
- **Key / token card**: dark card, masked key `sk-ant-••••`, copy button clicked, "COPIED" pill.
- **Tiles grid**: 2×2 / 3×2 logo tiles with green check badges appearing in sequence.
- **Setup guide checklist**: 4 numbered steps, checks ticking down.
- **Comment → DM** (always the last scene): IG comment sheet, cursor clicks field, CTA WORD types in, Post click,
  then a DM bubble/notification "Link bhej diya ✅".
- **Before → after / paid → free swap**: grey paid card, green dashed arrow, free card with $0 chip.
- **Big number**: one huge clay number counting up with a mono label.
