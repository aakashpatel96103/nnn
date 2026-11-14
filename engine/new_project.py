"""Scaffold a new reel project.

usage:
  python engine/new_project.py <slug> [--title "Reel title"]

Creates projects/<slug>/
  inputs/    user files: vo.mp3, script.txt, screenshots, screen recordings, logos
  assets/    processed media used by reel.html (cropped screenshots, extracted frames)
  src/       reel.html (from template), words.json, cues.json
  review/    snaps + contact sheets + QA reports (agent's working area)
  export/    final MP4s only
  project.json
"""
import argparse, json, shutil
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--title", default="")
    a = ap.parse_args()
    proj = KIT / "projects" / a.slug
    if proj.exists():
        raise SystemExit(f"{proj} already exists - pick a new slug (never overwrite a project)")
    for d in ("inputs", "assets", "src", "review", "export"):
        (proj / d).mkdir(parents=True)
    shutil.copy(KIT / "template" / "reel.html", proj / "src" / "reel.html")
    shutil.copy(KIT / "template" / "cues.json", proj / "src" / "cues.json")
    shutil.copy(KIT / "brand" / "avatar.png", proj / "assets" / "avatar.png")
    (proj / "src" / "words.json").write_text("[]", encoding="utf-8")
    cfg = {"slug": a.slug, "title": a.title, "duration": 15.0, "fps": 30, "width": 1080, "height": 1920,
           "handle": "@mukku.tech", "language": "hi", "status": "intake",
           "notes": "duration = last spoken word end + ~0.6s; update after transcribe"}
    (proj / "project.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    print(f"created {proj}")
    print("next: put user files into inputs/ (vo.mp3, script.txt, screenshots, recordings)")


if __name__ == "__main__":
    main()
