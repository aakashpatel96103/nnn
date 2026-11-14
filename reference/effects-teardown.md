# Reel Teardown — effects, motion, graphics, animation

Analysed 5 links: 4 reels + 1 post. Method: downloaded each video, measured duration / resolution / fps, ran scene-change detection (`scene > 0.30`) to count hard cuts, then sampled 12–16 frames per reel and read them.

| # | Link | Length | Res | FPS | Hard cuts |
|---|------|--------|-----|-----|-----------|
| 1 | instagram.com/reel/DfewPhMNUix | 68.9s | 720×1280 | 30 | 5 (8.7, 17.1, 22.7, 51.3, 56.9s) |
| 2 | instagram.com/reel/DfjgHxjgf6P | 37.6s | 720×1280 | 30 | 3 (13.5, 14.2, 14.4s) |
| 3 | instagram.com/reel/DfjlJfwgnMK | 35.3s | 720×1280 | 30 | **0** |
| 4 | instagram.com/reel/DfE97D2tif_ | 48.0s | 720×1280 | 30 | **0** |
| 5 | instagram.com/p/DfmfC9fnw50 | 5.0s | 1080×1350 | 30 | 0 (static post) |

**The single biggest finding:** 35–48 second reels with **zero hard cuts**. These are not edited videos — they are one continuous animated canvas where cards slide, swap and pop. That is why they look "expensive" while being cheap to produce: no footage, no camera, no editing timeline. Everything is typography + cards + UI screenshots + a few vectors.

---

## 1. DfewPhMNUix — "FOUND ON GITHUB" (69s, 9 swaps)

**Look:** white background with a faint grid paper texture; a huge soft mesh gradient (orange → pink → yellow) blurred across the lower half; black pill badge top-centre; dark charcoal cards floating on the light field.

**Type system:** bold geometric sans headline, centred, with one word set in *italic serif* in a warm gold ("payment", "version on Github", "VoiceStudio", "OpenSEO", "Wispr", "Cal.diy", "Loom"). Micro-labels in uppercase mono.

**Effect inventory**
- **Money-leak dashboard:** one dark card listing 10 subscriptions with prices, right-aligned, total row `$263/mo`. Built purely with text rows.
- **Sticker layer:** white labels with heavy borders and slight rotation drop onto the dashboard ("you stop paying", "9 swaps", "$263/mo"), plus an outlined green chip `free on GitHub` and a red `$0` badge.
- **The swap pattern (repeated 5×):** greyed-out paid product card on top (logo + price pill, e.g. `$139/mo`) → **green dashed arrow pointing down** → open-source replacement card (dark, name, GitHub stars, green `$0` chip). Each swap is one beat: ElevenLabs→VoiceStudio, Semrush→OpenSEO, Wispr Flow, Calendly→Cal.diy, Loom.
- **Progress counter:** `SWAP 2/9`, `SWAP 3/9`, `SWAP 5/9`… tiny mono label — creates "how many left" anticipation.
- **Star grid:** 6 logo tiles with star counts (`5.5K`, `104K`, `26.8K`, `78.4K`, `11K`, `17.1K`), green checkmark badges appearing one by one on each tile.
- **Big number:** `356K` in orange, with `GITHUB STARS` in mono above.
- **Search interaction:** a search field with a typed query `notionl` and a blinking caret, then a result row with logo + price, then the word "search GitHub".
- **Thumbnail wall finale:** 10+ small video thumbnails flying in as a grid.

**Motion character:** slides + scale, 200–400 ms, ease-out with slight overshoot; stickers rotate ±4–8° as they land; nothing spins or bounces hard. Pacing ≈ one idea every 2–3 s.

**Colour:** off-white `#F7F7F5`, charcoal `#141414`, warm brown-gold accent, money green `#2FB344`, danger red `$0` chip.

---

## 2. DfjgHxjgf6P — "Fable 5.2 × Higgsfield" (37.6s)

**Look:** almost white, very airy, left-aligned copy. A **real iPhone mockup** (Claude app UI rendered inside, status bar included) is the hero object in most beats.

**Type:** bold sans headline; secondary words in grey *italic serif*; key terms get a **blue highlighter swipe** behind them (`Fable 5.2`, `FREE`, `Comment FABLE`).

**Effect inventory**
- **Real app screens that change:** Claude app → model picker list (`Fable 5.2 New`, `Opus 5.5`, `Sonnet 5.5`, `Haiku 5.5`, `Reply to Claude` composer), then the Connectors settings screen, then back to chat. The phone frame stays, only the screen morphs — this is the "screen recording" illusion without any recording.
- **Mascot:** a tiny 3D white/blue robot sits bottom-left in nearly every frame, bobbing ~2 px, with a glowing eye. It is the brand anchor and it never leaves.
- **Step chips:** small dark pills on card corners — `2 Cinematic`, `5 Hypermotion` — like tier labels.
- **Proof clips:** short video clips play *inside* rounded card frames (cinematic car chase, sunglass macro shot) with a microscopic credit `clip: @Higgsfield.ai`.
- **Countdown card:** `AI VIDEO $$$ / 3 DAYS` in dark card with three dots filling.
- **Release card:** `JUST RELEASED / Fable 5.2 / by Anthropic` with a blue glow bloom behind it and floating particles.
- **Offer UI:** `DAY 1 / DAY 2 / DAY 3` blue button row, then a big `FREE` + `UNLIMITED` two-tone block, then "Every top video model" with two logo rows.
- **Callout system:** speech-bubble labels with a thin connector line to the exact UI element (`Customize > Connectors`, `1 MIN` badge with clock icon), numbered step badges (`1`, `2`) popping on the phone, and a giant ghost numeral (`3`, `1`) behind the device.
- **Success toast:** green circle with a checkmark scaling in over the screen, plus `Connected` pill.
- **End card:** comment box with typed `FABLE` highlighted in blue.

**Motion character:** the phone never moves much — content inside changes; overlays pop with a 10% overshoot; small drift/parallax on cards; particles float upward slowly.

---

## 3. DfjlJfwgnMK — "Claude Fable 5.2 hook" (35.3s, 0 cuts)

**Look:** white, ultra-minimal, magazine layout. Micro breadcrumb top-left in mono: `// 01 — CLAUDE FABLE 5.2 HOOK`, `// 03 — STRIP / V1 & SETTINGS.JSON`. Those labels make it feel like chapters of a document.

**Type:** large bold sans, left aligned, with *italic serif* accent at line end ("Claude Code completely free", "with a massive 1 million token", "v-one from"). Body copy small and grey.

**Effect inventory**
- **Real developer UI on display:** dark pricing/console card (Fable 5.2, `1M`, `128K`, `$8 → $0.20`, green progress bar), an API-key page with a masked key `sk-apx84446b…2a45` and `$0.00` spent, a VS Code window with `settings.json` (coloured env vars), a dark terminal, and a docs page.
- **Character presenter:** a hand-drawn cartoon man in a black hoodie stands bottom-centre in every scene, changing pose each beat (waving, open palms, presenting, leaning). Same trick as the robot — a permanent human anchor.
- **Sticker callouts with dashed borders:** yellow label `A KEY GENERATED IN PLAIN SIGHT, MASKED FOR:`, green label `PASTE THESE 3 SETTINGS`, dark label `COMMENT "CODE"` with a green arrow, and a black `Follow @mukku.tech`-style CTA strip.
- **Key card transformation:** the 1M-context card slides in, prices count/replace (`$8 → $0.20`), a green CTA row `START FREE TRIAL / LIMITLESS CODING` pulses, then a chip `FOR A LIMITLESS CONTEXT ✓` appears.
- **Big gesture overlays:** a huge black `3 •••` block with a `pin connector` label, a green check circle over the phone.
- **Halftone wipe:** a dot-matrix pattern expands across the full frame as a chapter transition — the only "effect" transition in the reel, and it lands hard because everything else is quiet.

**Motion character:** fast, snappy, 150–250 ms; elements snap into place rather than glide; frequent small cursor arrows that move to a button and click; one bold pattern wipe per chapter.

---

## 4. DfE97D2tif_ — "800M tokens router" (48s, 0 cuts, dark)

**Look:** true black (#0A0A0A) with warm orange ambient glow behind cards, orange/gold accent type, thin 1px borders with a soft orange outer glow. Reads as "premium dev tool".

**Effect inventory**
- **Real brand logos as nodes:** ChatGPT, Claude, Gemini, Llama, Mistral in rounded tiles, each with a tiny label underneath.
- **Animated diagram:** a central dark card `Smart Free-Tier Router`; above it a dotted "incoming request" line with a dot travelling downward; below it **curved connector lines that draw themselves** out to the five model tiles (stroke-dashoffset animation), with a glowing vertical bar under each model.
- **State change storytelling:** `● FREE TIER ACTIVE` pill in green; then a failure state — the GPT tile turns red, gets an `✕`, its connector goes dashed red, and a label reads `✕ 429 RATE LIMIT`. A dashed red arrow reroutes to another model. This is "explain the product by showing it break and recover".
- **Big number cards:** `$100 – $200 / month` (paid) vs `800M tokens` vs `600M Words / Month` — huge numbers with an orange suffix, thin borders, glow.
- **Repo card:** GitHub folder icon, `open-free-ai-router`, `800M free tokens / Month`, gold `★ Starred` button that pops in.
- **Profile CTA:** avatar `How Hub`, big orange gradient button `Follow @HowHub`, an arrow cursor sliding in and clicking, emoji burst.
- **Squiggle separator** (~) between two number cards — one vector doodle.

**Motion character:** slow, confident 400–600 ms easing; glows pulse; dots travel along paths; lines draw in; the failure state shakes once. No slides at all — everything fades/scales in place.

---

## The reusable playbook (what makes these look expensive)

1. **One canvas, no cuts.** Build the whole reel as layers on a fixed 1080×1920 canvas. 35–70 s, 0–5 cuts. Motion is *element* animation, not video editing.
2. **A recurring anchor character.** Robot, hoodie guy, avatar — bottom corner, small, bobbing, pose changes per beat. Instantly makes it feel authored.
3. **Real UI as the content.** Phone mockups, terminals, dashboards, settings files, repo cards, search boxes. Not stock photos, not icons floating in space.
4. **Sticker + callout layer.** Rotated labels, dashed-border notes, speech bubbles with connector lines, numbered step badges, cursor arrows that click.
5. **A repeating "pattern" beat.** The swap card (paid → green arrow → free) or the router diagram. Repetition with a counter (`SWAP 4/9`, `DAY 2`) buys 30 seconds of attention cheaply.
6. **Type hierarchy:** bold sans headline + *italic serif* accent word + highlighter marker behind 1–2 key words + uppercase mono micro-labels. Exactly two accent colours: warm orange/gold and money green.
7. **Micro-motion on everything:** numbers tick, checkmarks pop, toasts slide, toggles flip, keys type, bars fill. Nothing is ever fully static for more than ~1.5 s.
8. **Pacing:** a new visual idea every 2–3 s; text never longer than ~5 words on screen at once (rolling captions in the bottom third).
9. **One signature transition** used sparingly (halftone wipe, glow bloom) — because everything else is quiet, it reads as a design choice.
10. **Loopable ending:** last frame returns to the same layout as the first (badge + headline + card), so replays feel seamless.

---

## What this means for our build

Already in my renderer (HTML + Playwright → ffmpeg): element animation on one canvas, rolling word-sync captions, avatar poses, real brand SVG logos, browser/terminal/chat/comment mockups, camera push, grain.

Missing vs these reels, in priority order:
1. **Sticker/callout layer** (dashed notes, connector lines, numbered badges, cursor arrows) — biggest visual upgrade per unit of work.
2. **A repeating pattern beat with a counter** (swap card or router diagram) — carries the middle of the reel.
3. **Deeper real UI screens** (phone frame with an app screen that morphs, settings.json editor, API key page).
4. **Halftone / bloom wipe** as the one signature transition.
5. **Dark-mode variant** with orange glow for tech-product reels.
