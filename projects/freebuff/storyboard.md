# Storyboard: Claude ka free alternative (naam comment mein)

Voice: creator's own recording (`inputs/vo.mp3`, 24.4 s). Reel length 25.6 s, 1080x1920, 60 fps (2x supersampled render).
Rule for this reel: the software name is never readable. It is the comment-to-DM reward.

| # | Time | Spoken line | Screen |
|---|------|-------------|--------|
| S0 | 0.00 | Log reel aur video editing ke liye Claude ke peeche pagal ho rahe hain | Real Claude app card (dark theme, official logo, "Pro plan" pill), three request bubbles, sticker "SAB PAGAL!" |
| S1 | 3.38 | aur main abhi bhi free mein reels bana raha hoon | Price card: Rs 0, FREE chip, three reel thumbnails, sticker "FREE MEIN" |
| S2 | 5.78 | Aur sabse interesting baat, ye wali reel bhi maine isi software se banayi hai | Real screen recording: blurred app window + phone preview crop, sticker "REAL RECORDING", lock pill "NAAM (blur) COMMENT MEIN" |
| S3 | 10.06 | Main use karta hoon Claude ka ek free alternative, jisme tum wahi kaam kar sakte ho jo Claude mein karte the | Compare table: Claude Paid vs alternative FREE, four green checks, sticker "SAME KAAM" |
| S4 | 15.24 | Reel creation, video editing aur AI workflows, sab ek jagah | Three feature rows with checks, rows join, pill "SAB EK JAGAH", sticker "ALL-IN-ONE" |
| S5 | 19.66 | Software chahiye to comment karo ALTERNATIVE, aur main iska link tumhe DM kar dunga | Halftone wipe, comment box types ALTERNATIVE, Post, DM bubble with blurred link, "DM SENT", follow card |

## Name hiding
- Footage is cropped to the phone preview panel only (`assets/prev60/`, 656x1166, lanczos upscale from source), where the name never appears.
- The app shell behind it is blurred (`assets/shell60/`, 1640x692, gaussian sigma 10 at 2x = same visual blur as sigma 5 at 1x: chrome and text-line structure stay visible, letters do not) and is not readable.
- The build script stops if the product name appears anywhere in the reel HTML.
