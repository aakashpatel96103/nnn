"""Write src/cues.json: each sound on its visible peak (seconds -> frames at 60 fps)."""
import json, pathlib

proj = pathlib.Path(__file__).parent.parent.parent
C = [
    (0.00, "curated/hook-impact.wav", -6, "hook card"),
    (0.40, "curated/ui-pop.wav", -8, "bubble 1"),
    (1.20, "curated/ui-pop.wav", -8, "bubble 2"),
    (2.00, "curated/ui-pop.wav", -8, "bubble 3"),
    (2.46, "thock.wav", -5, "sticker SAB PAGAL"),
    (3.36, "curated/zoom-swish.wav", -6, "card 2 in"),
    (3.74, "curated/ui-pop.wav", -5, "Rs 0 pop"),
    (4.32, "clean-ding.wav", -5, "FREE chip"),
    (4.80, "tick.wav", -7, "thumb 1"),
    (4.96, "tick.wav", -7, "thumb 2"),
    (5.12, "tick.wav", -7, "thumb 3"),
    (5.76, "curated/zoom-swish.wav", -5, "recording window in"),
    (6.10, "curated/ui-pop.wav", -5, "phone pop"),
    (7.18, "curated/camera-shutter-light.wav", -7, "REAL RECORDING sticker"),
    (8.04, "shimmer.wav", -7, "proof flash"),
    (8.74, "latch.wav", -6, "name locked pill"),
    (10.04, "curated/zoom-swish.wav", -6, "compare card in"),
    (11.52, "clean-ding.wav", -4, "FREE reveal"),
    (12.78, "tick.wav", -6, "check 1"),
    (12.96, "tick.wav", -6, "check 2"),
    (13.48, "tick.wav", -6, "check 3"),
    (13.66, "latch.wav", -6, "check 4"),
    (14.22, "curated/ui-pop.wav", -6, "sticker SAME KAAM"),
    (15.30, "curated/zoom-swish.wav", -7, "row 1"),
    (15.78, "tick.wav", -6, "row 1 check"),
    (16.44, "curated/zoom-swish.wav", -7, "row 2"),
    (16.68, "tick.wav", -6, "row 2 check"),
    (17.22, "curated/zoom-swish.wav", -7, "row 3"),
    (17.52, "tick.wav", -6, "row 3 check"),
    (18.30, "thock.wav", -5, "rows join"),
    (18.82, "curated/ui-pop.wav", -6, "sticker ALL-IN-ONE"),
    (19.42, "curated/zoom-swish.wav", -4, "wipe"),
    (20.22, "curated/ui-pop.wav", -6, "sticker FREE LINK"),
    (21.40, "curated/ui-click.wav", -4, "click field"),
]
C += [(21.56 + i * 0.131, "typing-tick.wav", -10, "type") for i in range(6)]
C += [
    (22.60, "curated/ui-click.wav", -3, "Post"),
    (23.30, "curated/ui-pop.wav", -4, "DM in"),
    (23.90, "clean-ding.wav", -4, "DM SENT"),
    (24.80, "sparkle.wav", -8, "follow"),
]
cues = [{"frame": round(t * 60), "sound": s, "gain": g, "label": l} for t, s, g, l in sorted(C)]
(proj / "src/cues.json").write_text(json.dumps({"fps": 60, "total": 25.6, "cues": cues}, indent=1), encoding="utf-8")
print(len(cues))
