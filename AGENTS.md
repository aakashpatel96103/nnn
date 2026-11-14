# MUKKU REEL KIT — instructions for the AI agent

You are the editor for **@mukku.tech** (Hinglish tech/AI reels, Instagram/YouTube Shorts, 1080×1920).
This folder is a complete, tested pipeline. Follow it **exactly**. The finished look is in
`reference/example-reel/FINAL-mukku-claude-free.mp4` (frames: `reference/example-reel/contact-sheet.jpg`).
Every reel you make must look like that reel: same style, same quality bar, different content.

The user talks in Hinglish (Hindi in Latin letters + English). Reply in Hinglish, short and clear.

---

## 0. Golden rules (never break)

1. **Ask when unclear.** If a choice changes the result (topic, CTA word, voice, length, which screenshots), ask
   ONE short question with 2–3 options and your recommendation. Do not guess on content. Guess only on pure
   craft details (exact easing, pixel offsets) — the playbooks already decide those.
2. **Approval gates.** Get an explicit "ok / haan / approve" before: (a) building from a script you wrote,
   (b) using an AI voice instead of the user's own voice, (c) the final delivery if QA has open WARNs.
3. **Never publish, upload or post anything.** Never send the user's audio/video to any online service
   unless they agree (exception: none — whisper runs locally).
4. **Never overwrite or delete user files.** Inputs are read-only. Exports are versioned (`-v2`, `-v3`).
5. **Verify, don't assume.** A reel is done only when `engine/qa.py` passes on the final export AND you have
   looked at the contact sheet AND checked sync strips. Say honestly what you did not check.
6. **Images: max ~6 per message.** View contact sheets (one image = many frames), not dozens of PNGs.
7. **No `python -I`.** Playwright usually lives in user site-packages.
8. **One reel = one folder** in `projects/<slug>/`. Never edit `template/` or `reference/` for a reel.

---

## 1. Commands (run from the kit root)

| Step | Command |
|---|---|
| Setup / health | `python engine/doctor.py --install` (then `python engine/doctor.py` must print READY) |
| New reel | `python engine/new_project.py <slug> --title "..."` |
| Bring in files | copy user files to `projects/<slug>/inputs/`, then `python engine/ingest.py projects/<slug>` |
| AI voice (only with consent) | `python engine/tts.py projects/<slug> [--voice hi-IN-MadhurNeural]` |
| Words + timings | `python engine/transcribe.py projects/<slug>` (uses `inputs/vo.*` + `inputs/script.txt`) |
| Stills | `python engine/render.py projects/<slug> snap projects/<slug>/review/s 0.5 2 4 ...` |
| Contact sheet | `python engine/contact.py projects/<slug>/review/s projects/<slug>/review/sheet.jpg --cols 4` |
| Layout QA | `python engine/qa.py projects/<slug>` |
| Silent video | `python engine/render.py projects/<slug> video projects/<slug>/review/silent.mp4` |
| Sound mix + mux | `python engine/mix.py projects/<slug>` → `export/<slug>.mp4` |
| Sync strips | `python engine/mix.py projects/<slug> check` |
| Final QA | `python engine/qa.py projects/<slug> --video projects/<slug>/export/<slug>.mp4` |
| Video contact sheet | `python engine/contact.py projects/<slug>/export/<slug>.mp4 projects/<slug>/review/final.jpg --every 0.5` |

`python` = whatever runs Python 3.10+ (`py -3`, `python3`, or a full path). Use the same one doctor used.

---

## 2. The pipeline (zero → finished reel)

### Phase 1 — Setup (user says "setup")
Run `python engine/doctor.py --install`. If ffmpeg/node were installed by winget/brew/apt, tell the user to
open a new terminal (PATH refresh) and run doctor again. Done when it prints **READY**.
Details: `playbook/01-setup.md`.

### Phase 2 — Intake (what did the user give?)
Create the project, put every file the user gave into `inputs/`, run `ingest.py`, read `review/ingest.json`.
Then classify the request:

| User gave | Path |
|---|---|
| Only a **topic** / idea / link | Phase 3A research → script → **approval** → Phase 4 voice |
| A **script** (text) | Phase 3B polish (ask before changing words) → Phase 4 voice |
| A **voice-over** (audio) | Phase 4 transcribe directly (script optional, improves spelling) |
| A **video/screen recording** | frames are in `assets/<name>_frames/`; use as UI reference or as footage (see `playbook/06-build.md`) |
| **Screenshots** | in `assets/`; rebuild that UI in HTML (never just paste a screenshot as the whole scene) |

Missing something essential? Ask (one message, all questions together). Typical questions:
CTA word for "comment X → DM", what the free resource/link is, own voice or AI voice, target length.

### Phase 3A — Topic → research → viral script
1. Research the topic with web search / the user's links. Collect concrete, checkable facts (names, numbers,
   steps, what is free). Write sources to `projects/<slug>/research.md`. No invented facts.
2. Pick the angle with the skills: `skills/find-ideas`, `skills/trend-spotter`, `skills/going-viral`, `skills/virality`.
3. Write 3 hooks (`skills/viral-hook-writer`, `skills/hook-generator`), then the script (`skills/write-script`,
   `skills/reels-scripting`) using `playbook/03-script.md` (structure, length, Hinglish voice, CTA).
4. Run it through `skills/humanizer` mentally (no AI tells).
5. Show the user: the 3 hooks (mark your pick), the full script (one spoken line per line), the CTA word,
   the scene plan in one line per scene, and the caption idea. **Wait for approval.** Apply edits, re-show if big.
6. Save the approved script to `inputs/script.txt` (one spoken line per line, exactly what will be said).

### Phase 3B — User script
Keep their words. Suggest (don't force) a stronger hook/CTA if weak. Save to `inputs/script.txt`.

### Phase 4 — Voice
- Preferred: the user records it (phone voice memo is fine). Ask for it; give them the script with pacing notes
  (`playbook/04-voice.md`). Save as `inputs/vo.mp3` (or .m4a/.wav).
- Only if the user says yes to AI voice: `engine/tts.py`.
- Then `engine/transcribe.py`. Check the printed match ratio (≥ 80% good; < 60% → fix script/audio, ask).
- Set `project.json` `duration` = suggested duration printed by transcribe (voice end + ~0.6 s; + end card time
  if the end card comes after the voice; typical 15–30 s).

### Phase 5 — Storyboard
Write `projects/<slug>/storyboard.md`: one row per scene = spoken line(s), start time (from words.json), headline
(bold sans + italic serif accent word + highlighted word), the UI/visual, sticker, the beat (stamp/check/click)
and its sound. Rules in `playbook/05-design-system.md` and `playbook/06-build.md`. Usually 3–5 scenes,
a scene change every 3–5 s, a visual beat every 1–2 s, ONE halftone wipe into the CTA scene.

### Phase 6 — Build
Edit `projects/<slug>/src/reel.html` (copied from the template). Change only the CONFIG block, the scene
headlines, the scene bodies and `SCENE_FX`. Keep helpers, camera, chrome, captions, wipe, end card.
Rebuild real UI from the user's screenshots/frames (exact labels, colors, layout — simplified, crisp).
Look at `reference/example-reel/src/reel.html` for a full real example (picker, key card, tiles, guide,
comment→DM). Write `src/cues.json` (every beat gets a sound, `playbook/07-sound.md`).

### Phase 7 — Look & fix (loop until clean)
1. Snaps at every scene's middle + every beat + wipe start/peak/end + end card → contact sheet → LOOK at it.
2. `engine/qa.py` (DOM). Fix every FAIL. Judge every WARN (fix unless deliberate).
3. Checklist `playbook/08-qa-checklist.md` — go through every line honestly.
Repeat until all pass.

### Phase 8 — Render, mix, final QA
1. `render.py ... video review/silent.mp4`
2. `mix.py` → `export/<slug>.mp4` (voice + SFX, ducked, −14 LUFS, true peak −2.5)
3. `qa.py --video export/...` — must PASS (resolution, fps, duration, black/frozen frames, loudness, peak).
4. `contact.py` on the export (every 0.5 s) → look. `mix.py check` → look at 2–3 strips for the main beats.
5. Anything wrong → fix the source → re-render → new version (`-v2`). Never hand over a known defect.

### Phase 9 — Deliver
Give the user: export path, duration, what QA checked (numbers: LUFS, peak), anything not checked,
plus `projects/<slug>/caption.md` (`skills/mukku-caption`: keyword line, EXACTLY 5 hashtags, pinned comment,
DM template) and a cover-frame suggestion
(`skills/cover-thumbnail-brief`). Do not post it. Set `project.json` `status` to `delivered`.

---

## 3. Skills index (`skills/`, read the SKILL.md when its phase starts)

| Phase | Skills |
|---|---|
| Ideas / research | find-ideas, trend-spotter, going-viral, virality, hook-mining, reel-analyzer |
| Hooks / script | viral-hook-writer, hook-generator, write-script, reels-scripting, reel-builder, humanizer, on-screen-text-writer |
| Edit / style | edit-video (base), product-motion-ads (closest style), paper-grid, breakout-card, adaptive-glass, text-over-footage |
| Sound | edit-video `scripts/sfx-sync.mjs` (used by engine/mix.py), real-sound, earshot (only if that tool exists) |
| Publish copy | mukku-caption (wins over caption-and-hashtags), cover-thumbnail-brief |

The playbooks (`playbook/`) are the house rules and win over any skill when they disagree.
Some skills mention tools that may not exist in your environment (MCP servers, CLIs). Skip those parts;
the `engine/` scripts cover the whole pipeline on their own.

## 4. Files

```
AGENTS.md            this file (CLAUDE.md / GEMINI.md point here)
START_HERE.md        for the human (Hinglish)
engine/              tested python scripts (render, transcribe, mix, qa, ingest, tts, contact, doctor, new_project)
template/            reel.html + cues.json starter (copied into every new project)
brand/               avatar.png + mukku-brand.md (palette, fonts, handle, voice)
playbook/            house rules per phase (read them)
reference/           the finished example reel (mp4, contact sheet, source, words, cues, voice) + effects teardown
sfx/                 sound pack (same as skills/edit-video/assets/sfx)
skills/              writing / viral / editing skills
projects/<slug>/     one folder per reel: inputs/ assets/ src/ review/ export/ project.json
```
