"""Check (and with --install, install) everything the reel pipeline needs.

usage:
  python engine/doctor.py            # report only
  python engine/doctor.py --install  # install missing python packages + chromium; print how to get ffmpeg/node

Needs: Python 3.10+, ffmpeg + ffprobe on PATH, Node 18+, pip packages:
  playwright (+ chromium), openai-whisper, numpy, pillow; optional: edge-tts (AI voice fallback)
"""
import importlib, platform, shutil, subprocess, sys

PKGS = [("playwright", "playwright"), ("whisper", "openai-whisper"), ("numpy", "numpy"), ("PIL", "pillow")]
OPTIONAL = [("edge_tts", "edge-tts")]


def has(mod):
    try:
        importlib.import_module(mod); return True
    except Exception:
        return False


def pip(pkg):
    print(f"  installing {pkg} ...")
    return subprocess.run([sys.executable, "-m", "pip", "install", "--user", "-q", pkg]).returncode == 0


def tool_version(cmd):
    exe = shutil.which(cmd)
    if not exe:
        return None
    try:
        out = subprocess.run([exe, "-version" if cmd.startswith("ff") else "--version"], capture_output=True, text=True).stdout
        return out.splitlines()[0][:70]
    except Exception:
        return exe


def chromium_ok():
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


def main():
    install = "--install" in sys.argv
    ok = True
    print(f"python   {sys.version.split()[0]} ({sys.executable})")
    if sys.version_info < (3, 10):
        print("  FAIL need Python 3.10+"); ok = False
    for mod, pkg in PKGS:
        if has(mod):
            print(f"OK   {pkg}")
        elif install and pip(pkg) and has(mod):
            print(f"OK   {pkg} (installed)")
        else:
            print(f"MISS {pkg}  ->  {sys.executable} -m pip install --user {pkg}"); ok = False
    for mod, pkg in OPTIONAL:
        if has(mod):
            print(f"OK   {pkg} (optional)")
        elif install and pip(pkg):
            print(f"OK   {pkg} (optional, installed)")
        else:
            print(f"--   {pkg} optional (only for AI voice fallback)")
    if has("playwright"):
        if chromium_ok():
            print("OK   chromium for playwright")
        elif install:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
            print("OK   chromium (installed)" if chromium_ok() else "FAIL chromium install"); ok = ok and chromium_ok()
        else:
            print(f"MISS chromium  ->  {sys.executable} -m playwright install chromium"); ok = False
    osname = platform.system()
    for t in ("ffmpeg", "ffprobe", "node"):
        v = tool_version(t)
        if v:
            print(f"OK   {t}: {v}")
            continue
        ok = False
        hint = {"Windows": "winget install --id Gyan.FFmpeg -e" if t != "node" else "winget install --id OpenJS.NodeJS.LTS -e",
                "Darwin": "brew install ffmpeg" if t != "node" else "brew install node",
                "Linux": "sudo apt-get install -y ffmpeg" if t != "node" else "sudo apt-get install -y nodejs"}.get(osname, "")
        if install and hint:
            print(f"MISS {t} - running: {hint}")
            subprocess.run(hint, shell=True)
            print("     (open a NEW terminal afterwards so PATH refreshes, then run doctor again)")
        else:
            print(f"MISS {t}  ->  {hint}")
    if shutil.which("node"):
        v = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip().lstrip("v")
        if int(v.split(".")[0]) < 18:
            print(f"FAIL node {v} < 18"); ok = False
    print("\nREADY" if ok else "\nNOT READY - fix the MISS/FAIL lines (or rerun with --install)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
