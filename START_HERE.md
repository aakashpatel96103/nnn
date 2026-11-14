# Mukku Reel Kit — shuru kaise kare

Ye folder kisi bhi coding AI agent (Claude Code, Codex, Cursor, Gemini CLI, Windsurf...) ko do —
wo bilkul @mukku.tech wali style me reel banayega (example: `reference/example-reel/FINAL-mukku-claude-free.mp4`).

## Step 1 — folder kholo
Zip extract karo. Us folder ko apne AI agent me open karo (project/working folder bana do).

## Step 2 — bolo: `setup`
Agent khud sab install karega: Python packages, Chromium (render ke liye), whisper (voice se words),
ffmpeg, Node. Agar wo bole "naya terminal kholo" to kholo aur fir se `setup` bolo.
Last me **READY** dikhna chahiye.

> Python 3.10+ pehle se chahiye. Nahi hai to: Windows → `winget install Python.Python.3.12`, Mac → `brew install python`.

## Step 3 — reel maango (inme se kuch bhi do)

| Tum do | Example message |
|---|---|
| Sirf **topic** | `reel banao: Cursor ka free plan kaise use kare` |
| **Script** | `ye script hai, reel banao:` + script paste |
| **Voice** | `inputs me vo.mp3 daala hai, reel banao` |
| **Screenshots / screen recording** | files do aur bolo kaunsa part dikhana hai |

Topic doge to agent research karega, viral hook + script likhega, aur **tumse approval lega** — tabhi banayega.
Voice tumhari hi best hai (phone voice memo chalega). AI voice sirf tum haan bologe tab.

## Step 4 — check & deliver
Agent khud reel check karega (text kata to nahi, safe area, sync, loudness, black frames...) aur galti
khud fix karega. Final file milegi: `projects/<naam>/export/<naam>.mp4` + caption + hashtags.
Agent kabhi khud post/upload nahi karega.

## Tips
- Jo pasand nahi aaya seedha bolo: "scene 2 ka headline bada karo", "CTA word GUIDE karo", "click sound kam karo".
- Purani files kabhi overwrite nahi hoti — naya version `-v2` banta hai.
