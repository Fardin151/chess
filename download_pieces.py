"""Download chess piece PNGs from Wikimedia Commons."""
import urllib.request
import os

BASE = "https://upload.wikimedia.org/wikipedia/commons/thumb"
PIECES = {
    "wK": f"{BASE}/4/42/Chess_klt45.svg/80px-Chess_klt45.svg.png",
    "wQ": f"{BASE}/1/15/Chess_qlt45.svg/80px-Chess_qlt45.svg.png",
    "wR": f"{BASE}/7/72/Chess_rlt45.svg/80px-Chess_rlt45.svg.png",
    "wB": f"{BASE}/b/b1/Chess_blt45.svg/80px-Chess_blt45.svg.png",
    "wN": f"{BASE}/e/ef/Chess_nlt45.svg/80px-Chess_nlt45.svg.png",
    "wP": f"{BASE}/4/45/Chess_plt45.svg/80px-Chess_plt45.svg.png",
    "bK": f"{BASE}/f/f0/Chess_kdt45.svg/80px-Chess_kdt45.svg.png",
    "bQ": f"{BASE}/4/47/Chess_qdt45.svg/80px-Chess_qdt45.svg.png",
    "bR": f"{BASE}/f/ff/Chess_rdt45.svg/80px-Chess_rdt45.svg.png",
    "bB": f"{BASE}/9/98/Chess_bdt45.svg/80px-Chess_bdt45.svg.png",
    "bN": f"{BASE}/e/e1/Chess_ndt45.svg/80px-Chess_ndt45.svg.png",
    "bP": f"{BASE}/c/c7/Chess_pdt45.svg/80px-Chess_pdt45.svg.png",
}

out_dir = os.path.join(os.path.dirname(__file__), "assets", "pieces")
os.makedirs(out_dir, exist_ok=True)

for name, url in PIECES.items():
    dest = os.path.join(out_dir, f"{name}.png")
    if os.path.exists(dest):
        print(f"  {name}.png already exists, skipping")
        continue
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        print(f"  Downloaded {name}.png")
    except Exception as e:
        print(f"  FAILED {name}: {e}")

print("Done.")
