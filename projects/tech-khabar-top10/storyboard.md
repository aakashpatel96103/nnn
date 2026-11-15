# Storyboard — Top 10 Tech Khabar (14 Nov 2026)

16:9 long-form, 1920×1080 / 30 fps / 166.1 s. Brand **Tech Khabar**. Hinglish Latin on-screen text.
Voice-over: user ka upload (`inputs/vo.mp3`, 166.4 s) — screen pe **jo audio bolta hai wahi** likha hai.

Har scene ka layout same family: left = number + headline + 2 supporting lines, right = white card with the big number,
neeche = karaoke caption pill (audio ke words ke saath chalte hue). Upar brand bar + progress line.

| # | Time | Scene | Headline | Card number | Caption beat |
|---|------|-------|----------|-------------|--------------|
| 1 | 0.00–8.08 | Intro | Aaj ki 10 badi khabrein | TOP 10 / 14 Nov | "Jahan miltihain tech…" |
| 2 | 8.58–13.16 | Bulletin | (bulletin wipe) | — | — |
| 3 | 13.62–25.36 | Apple | Apple ka pehla touchscreen MacBook Pro | $400 (price jump — same chip model se) | "MacBook Pro se…" |
| 4 | 25.56–38.96 | GTA6 | GTA6 preload shuru, 212 GB | 212 GB (launch 19 Nov) | "game preload kar sakte" |
| 5 | 39.36–45.06 | AMD | AMD ke Q3 results out | 3 NOV (Q3) | "ke official results jaari" |
| 6 | 45.34–60.20 | China / SoftBank | China ne $5.4B deal roka | $5.4B (BLOCKED stamp) | "ko iss se confirm" |
| 7 | 60.58–70.58 | Blue Origin | New Glenn ki udaan Jan 2027 tak ruki | JAN 2027 | "Reuters ke mutabik…" |
| 8 | 70.90–86.66 | AI fraud | AI se nakal, **$139M** ka fraud | $139M (3 logon par charges) | "se CEOs aur vakilon" |
| 9 | 87.00–98.58 | Nitori | Nitori ka data breach, 37M records | 37M | "jisme saadhe 37 million" |
| 10 | 98.82–111.46 | Paris AI safety | Paris mein AI safety meeting | ~50 participants | "jisme lagbhag 50 participants" |
| 11 | 111.46–121.12 | Gemini | Gemini 4 Carbon sab ke liye | $2/$10 per 1M tokens (intro) | "hai." |
| 12 | 121.48–133.08 | Anthropic | Anthropic ke naye models, 30% tez | +30% (Fable 5.2 / Mythos 5.2) | "pichle 5.1 se 30%" |
| 13 | 133.12–141.56 | Recap | Inme se kaunsi best lagi? | 10/10 | "10 badi tech khabrein." |
| 14 | 141.96–165.54 | Outro | Subscribe karo, *bell bhi dabao* | TK monogram · Subscribe · **Comment karo "GTA"** | "Aur agar GTA ka wait…" → "pahunche." |

Halftone wipe ≈141.6–142.4.

## Comment CTA (v3 change)
Audio me GTA keyword wala CTA hai, is liye screen pe bhi:
- Scene 14 me **slide-in sticker** `Comment karo "GTA"` (left column, GTA word par land karta hai — cue: `curated/ui-pop.wav`).
- End card ke Subscribe button ke neeche **chip** `Comment karo "GTA"`.
- Word-timed pill (`GTA.`) bhi GTA bolte waqt dikhta hai.
- Outro me avatar nahi — TK monogram circle (user ki choice).

## Facts / notes
- Fraud figure screen pe **$139M** — audio isi kehta hai. DOJ ki release me "more than $129M" hai;
  farq user ko bata diya gaya, audio na dubaara record hoga is liye audio wala figure rakha.
- Charges = allegations; koi convicted nahi. On-screen wording alleged.
- Baaki numbers audio + sources se cross-checked (Apple $2,899 / +$400, GTA6 212 GB + 19 Nov,
  China–SoftBank $5.4B, New Glenn Jan 2027, Nitori 37M, Paris ~50, Gemini $2/$10 intro + $4/$20 from 1 Dec, Anthropic +30%).

## Build
1. `python3 src/make_cues.py` → `src/cues.json` (28 cues)
2. `python3 src/render169.py . video review/silent.mp4 --crf=17 --preset=veryfast` (4,983 frames)
3. `python3 ../../engine/mix.py .` (repo root se: `engine/mix.py projects/tech-khabar-top10`)
4. `python3 src/qa169.py . --video export/tech-khabar-top10.mp4`

Source HTML: `src/reel.html` (single file, no deps). Snaps/measure: `src/render169.py`.
