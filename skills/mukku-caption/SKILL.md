---
name: mukku-caption
description: The @mukku.tech Instagram caption writer. After a reel is done, writes projects/<slug>/caption.md with a hook line plus CTA word, proof, feature bullets, CTA repeat, a keyword line of 12-20 search phrases, the follow line and EXACTLY 5 hashtags, plus the pinned first comment, alt text, cover text and DM reply. Use when the user asks for "caption", "hashtags", "post copy", "description" or "first comment" for a mukku reel.
---

# mukku-caption — Instagram post copy for @mukku.tech

This skill is the house caption writer for **@mukku.tech** (Hinglish tech / AI tools reels).
It overrides `skills/caption-and-hashtags` wherever they disagree. In particular, it uses **exactly 5 hashtags**, never 12–15.
Real captions the user liked live in `reference/ig-captions.md`. Read them first and copy their rhythm.

Instagram search ranks reels mostly by **keywords in the caption, on-screen text and the spoken words**.
Hashtags matter much less. So a caption carries many natural keywords and only 5 hashtags.

## The caption (after the reel is done)

Write the caption into `projects/<slug>/caption.md` with exactly these blocks, in this order.

1. **Line 1, the hook plus the comment keyword.** It must work alone in the 125-character preview. Repeat the CTA word here.
   `Claude ka FREE alternative 👀 Comment karo "ALTERNATIVE" — link DM kar dunga`
2. **Proof line.** One sentence on why to trust it: `Ye reel bhi isi software se bani hai.`
3. **What you get.** 3–4 bullets, each starting with an emoji (✅ 🎬 ⚡ 🤖), each a real feature with its keyword.
4. **Steps (optional).** 1️⃣ 2️⃣ 3️⃣ short steps if the reel had setup steps.
5. **Urgency / free line.** For example `100% free, no card` or `Sirf kuch din ke liye free`. Only if it is true.
6. **CTA repeat.** `Comment "ALTERNATIVE" 👇 aur Save karo baad ke liye 📌`. Add a share line: `Us dost ko bhejo jo Claude ke paise bhar raha hai`.
7. **Keyword line.** 12–20 search phrases people actually type, separated by ` | `. Mix:
   - Hinglish phrases: `free ai tool`, `reel kaise banaye`, `video editing app free`
   - English phrases: `claude alternative`, `ai video editor`, `best ai tools 2026`
   - The tool name and its competitors' names
   No `#` on keywords.
8. `Follow @mukku.tech for daily AI tools 🚀`
9. **EXACTLY 5 hashtags** on the last line, ordered:
   - 1 broad: `#aitools`
   - 2 niche: `#claudeai #aivideoediting`
   - 1 community/language: `#hinglish` or `#techindia`
   - 1 topic-specific: `#freeaitools` or the tool's tag

   Never write 6. Never use banned or spammy tags (`#followforfollow`, `#viral`, `#fyp`).

Also write:
- **First comment (pin it):** a question that invites replies, plus the CTA word again.
  `Kaunsa AI tool use karte ho reels ke liye? 👇 Link chahiye to "ALTERNATIVE" likho`
- **Alt text** (accessibility + search, ≤ 125 chars): `Hinglish reel showing a free Claude alternative for reel and video editing, with setup steps`
- **On-screen keyword check:** the main keyword must appear in at least one scene `head`, the spoken script, and caption line 1. If it is missing from the reel, say so.
- **Cover text** (≤ 5 words): for example `Claude FREE Alternative`.

Caption checklist before you hand it over:
- [ ] Line 1 is under 125 characters and has the hook and the CTA word.
- [ ] The CTA word is identical in the reel, caption line 1, the CTA repeat and the first comment.
- [ ] 12+ keywords and exactly 5 hashtags. Count them.
- [ ] Every claim (free, price, features) is true and was said in the voice-over or checked.
- [ ] No AI tells: "game-changer", "unlock", "dive in", "it's not X, it's Y" (see `skills/humanizer`).
- [ ] Nothing is posted. Hand the text to the user. They post it.

---

## Comment-to-DM reels: hide the tool name

When the tool is given only after people comment (the usual mukku CTA), its name must appear **nowhere public**:
- not in the reel (show it as `Secret Tool ?`, blur its name and logo in screen recordings)
- not in the caption, the keyword line, the hashtags, the first comment, the alt text or the cover text

Put the name only in a **DM reply template** at the end of `caption.md`:
`Ye lo bhai 👇 <Tool name> — <link>`

Keywords then use the category and the competitor instead: `claude alternative`, `free ai video editor`, `ai reel maker`.
