"""Automatic QA for a reel. Run it on EVERY export; fix every FAIL, judge every WARN.

usage:
  python engine/qa.py <project_dir> [--video export/final.mp4] [--every 0.25]

Checks
  A. Composition (DOM, via playwright, sampled every --every seconds):
     - page errors / console errors
     - visible text clipped by its own box (scrollWidth > clientWidth) -> overflowing text
     - visible elements partly outside the 1080x1920 frame
     - visible text (headline / stickers / UI) outside the safe area x 60-1020, y 200-1700
       (Instagram UI covers the top ~200px and bottom ~220px; captions sit around y 1236)
     - caption pill wider than 900px or more than 2 lines
     - two visible text blocks overlapping each other (headline vs sticker etc.)
  B. Final file (ffprobe / ffmpeg):
     - decodes end to end, 1080x1920, project fps, yuv420p, H.264 + AAC
     - video and audio durations match project duration (+-0.15s)
     - black frames, frozen stretches > 1.2s (blackdetect / freezedetect)
     - integrated loudness about -14 LUFS (-16..-12), true peak <= -1 dBTP
Writes review/qa_report.json and prints PASS/WARN/FAIL lines. Exit code 1 if any FAIL.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

SAFE = (60, 200, 1020, 1700)

DOM_JS = r"""
(SAFE)=>{
 const out=[]; const vis=e=>{const s=getComputedStyle(e); if(s.display==='none'||s.visibility==='hidden') return false;
   let o=1; for(let n=e;n&&n.nodeType===1;n=n.parentElement){o*=parseFloat(getComputedStyle(n).opacity);} return o>0.35;};
 const hasText=e=>[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length>0);
 const els=[...document.querySelectorAll('body *')].filter(e=>!['SCRIPT','STYLE','svg','path','CANVAS'].includes(e.tagName));
 const textBoxes=[];
 for(const e of els){
   if(e.closest('[data-qa-ignore]')) continue;
   if(!vis(e)) continue;
   let r=e.getBoundingClientRect(); if(r.width<2||r.height<2) continue;
   if(hasText(e)){ // measure the glyphs, not the (possibly full-width) box
     let L=1e9,T=1e9,R=-1e9,B=-1e9; for(const n of e.childNodes){ if(n.nodeType!==3||!n.textContent.trim()) continue;
       const rg=document.createRange(); rg.selectNodeContents(n); const q=rg.getBoundingClientRect();
       L=Math.min(L,q.left);T=Math.min(T,q.top);R=Math.max(R,q.right);B=Math.max(B,q.bottom);}
     if(R>L) r={left:L,top:T,right:R,bottom:B,width:R-L,height:B-T}; }
   const id=e.id||(e.className&&typeof e.className==='string'?'.'+e.className.split(' ')[0]:e.tagName);
   const txt=hasText(e)?e.textContent.trim().slice(0,40):'';
   if(txt && (e.scrollWidth>e.clientWidth+2) && getComputedStyle(e).overflow!=='visible')
     out.push(['FAIL','text clipped by its box',id,txt]);
   if(r.right<0||r.left>1080||r.bottom<0||r.top>1920) continue; // fully off-screen = fine (parked)
   if(txt && (r.left< -2||r.right>1082||r.top< -2||r.bottom>1922)) out.push(['FAIL','text cut by frame edge',id,txt,[r.left|0,r.top|0,r.right|0,r.bottom|0]]);
   if(txt && !e.closest('[data-qa-chrome]') && (r.left<SAFE[0]||r.right>SAFE[2]||r.top<SAFE[1]||r.bottom>SAFE[3]))
     out.push(['WARN','text outside safe area',id,txt,[r.left|0,r.top|0,r.right|0,r.bottom|0]]);
   if(txt && e.closest('[data-qa-text]')===e) textBoxes.push([id,txt,r]);
 }
 const cap=document.getElementById('capin');
 if(cap && vis(cap)){const r=cap.getBoundingClientRect(); const lh=parseFloat(getComputedStyle(cap).lineHeight)||70;
   if(r.width>900) out.push(['FAIL','caption wider than 900px','capin',cap.textContent.slice(0,40)]);
   if(r.height>lh*2+40) out.push(['FAIL','caption more than 2 lines','capin',cap.textContent.slice(0,40)]);}
 for(let i=0;i<textBoxes.length;i++) for(let j=i+1;j<textBoxes.length;j++){
   const a=textBoxes[i][2], b=textBoxes[j][2];
   const ix=Math.min(a.right,b.right)-Math.max(a.left,b.left), iy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
   if(ix>8&&iy>8) out.push(['WARN','text blocks overlap',textBoxes[i][0]+' x '+textBoxes[j][0],textBoxes[i][1]+' | '+textBoxes[j][1]]);
 }
 return out;
}
"""


def dom_checks(proj: Path, every: float, dur: float):
    sys.path.insert(0, str(Path(__file__).parent))
    from render import build
    from playwright.sync_api import sync_playwright
    page = build(proj)
    issues = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto(page.as_uri()); pg.wait_for_timeout(600)
        t = 0.0
        seen = set()
        while t <= dur + 1e-6:
            pg.evaluate(f"render({t:.3f})")
            for it in pg.evaluate(DOM_JS, list(SAFE)):
                key = (it[0], it[1], it[2])
                if key in seen:
                    continue
                seen.add(key)
                issues.append([it[0], f"t={t:.2f}s {it[1]}: {it[2]} '{it[3]}'" + (f" box={it[4]}" if len(it) > 4 else "")])
            t += every
        b.close()
    for e in errs:
        issues.append(["FAIL", f"page error: {e}"])
    return issues


def probe(video: Path):
    j = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(video)]))
    return j


def file_checks(video: Path, dur: float, fps_want: float = 30.0):
    issues = []
    if not video.exists():
        return [["FAIL", f"no export at {video}"]]
    j = probe(video)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        return [["FAIL", "no video stream"]]
    if (v["width"], v["height"]) != (1080, 1920):
        issues.append(["FAIL", f"resolution {v['width']}x{v['height']} (need 1080x1920)"])
    if v["codec_name"] != "h264" or v.get("pix_fmt") != "yuv420p":
        issues.append(["FAIL", f"video {v['codec_name']} {v.get('pix_fmt')} (need h264 yuv420p)"])
    num, den = map(int, v["r_frame_rate"].split("/"))
    if abs(num / den - fps_want) > 0.5:
        issues.append(["WARN", f"fps {num/den:.2f}"])
    vd = float(v.get("duration", j["format"]["duration"]))
    if abs(vd - dur) > 0.15:
        issues.append(["FAIL", f"video duration {vd:.2f}s vs project {dur:.2f}s"])
    if not a:
        issues.append(["FAIL", "no audio stream"])
    else:
        ad = float(a.get("duration", vd))
        if a["codec_name"] != "aac":
            issues.append(["WARN", f"audio codec {a['codec_name']}"])
        if abs(ad - vd) > 0.15:
            issues.append(["FAIL", f"audio {ad:.2f}s vs video {vd:.2f}s"])
    # full decode
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(video), "-f", "null", "-"], capture_output=True, text=True)
    if r.stderr.strip():
        issues.append(["FAIL", "decode errors: " + r.stderr.strip()[:300]])
    # black / freeze
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "blackdetect=d=0.1:pix_th=0.08,freezedetect=n=0.001:d=1.2",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    for m in re.finditer(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr):
        issues.append(["FAIL", f"black frames {m.group(1)}-{m.group(2)}s"])
    for m in re.finditer(r"freeze_start: ([\d.]+)", r.stderr):
        issues.append(["WARN", f"frozen picture from {m.group(1)}s for >1.2s (is something always moving?)"])
    if a:
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True)
        tail = r.stderr[r.stderr.rfind("Summary:"):]
        I = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
        P = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
        if I:
            lv = float(I.group(1))
            if not -16.5 <= lv <= -11.5:
                issues.append(["WARN", f"loudness {lv} LUFS (target -14)"])
            else:
                issues.append(["INFO", f"loudness {lv} LUFS"])
        if P:
            pk = float(P.group(1))
            issues.append(["FAIL" if pk > -0.9 else "INFO", f"true peak {pk} dBTP (max -1)"])
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--video")
    ap.add_argument("--every", type=float, default=0.25)
    ap.add_argument("--no-dom", action="store_true")
    a = ap.parse_args()
    proj = Path(a.project).resolve()
    cfg = json.loads((proj / "project.json").read_text(encoding="utf-8"))
    dur = float(cfg["duration"])
    issues = []
    if not a.no_dom:
        issues += dom_checks(proj, a.every, dur)
    if a.video:
        issues += file_checks(Path(a.video).resolve(), dur, float(cfg.get("fps", 30)))
    (proj / "review").mkdir(exist_ok=True)
    (proj / "review" / "qa_report.json").write_text(json.dumps(issues, indent=1, ensure_ascii=False), encoding="utf-8")
    fails = [i for i in issues if i[0] == "FAIL"]
    warns = [i for i in issues if i[0] == "WARN"]
    for lvl, msg in issues:
        print(f"{lvl:4} {msg}")
    print(f"\nQA: {len(fails)} FAIL, {len(warns)} WARN" + ("  -> PASS" if not fails else "  -> FIX THE FAILS"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
