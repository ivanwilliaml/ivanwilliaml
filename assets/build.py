"""Generate the glass SVG assets used by README.md.

Run:  python assets/build.py
Self-contained SVG (gradients, blur, SMIL animation) so it renders inside
GitHub's <img> sandbox with no external resources.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

# ---- design tokens -----------------------------------------------------------
W = 1200
BG_0, BG_1 = "#070B14", "#0B1226"
BLUE, BLUE_SOFT, PURPLE = "#2563EB", "#60A5FA", "#7C3AED"
TEXT, MUTED = "#F1F5F9", "#94A3B8"
FONT = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def defs(uid):
    return f"""
  <defs>
    <linearGradient id="bg-{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG_0}"/><stop offset="1" stop-color="{BG_1}"/>
    </linearGradient>
    <linearGradient id="glass-{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.03"/>
    </linearGradient>
    <linearGradient id="stroke-{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.30"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>
    <linearGradient id="accent-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{BLUE_SOFT}"/><stop offset="1" stop-color="{PURPLE}"/>
    </linearGradient>
    <filter id="blur-{uid}" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="70"/>
    </filter>
  </defs>"""


def blob(cx, cy, r, color, uid, dur, dx, dy, opacity):
    return f"""
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{opacity}" filter="url(#blur-{uid})">
    <animateTransform attributeName="transform" type="translate" values="0 0; {dx} {dy}; 0 0"
      dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
  </circle>"""


def glass(x, y, w, h, uid, rx=20):
    return f"""
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#glass-{uid})"
    stroke="url(#stroke-{uid})" stroke-width="1"/>"""


def text(x, y, s, size, weight=500, fill=TEXT, anchor="start", ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{escape(s)}</text>')


def est_w(s, size):
    return sum(0.62 if c.isupper() or c.isdigit() else 0.36 if c in " .,·'/" else 0.55 for c in s) * size


def pill(x, y, label, uid, size=13, h=30):
    w = est_w(label, size) + 28
    return w, f"""
  <rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="#FFFFFF" fill-opacity="0.06"
    stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  {text(x + w/2, y + h/2 + size*0.36, label, size, 500, TEXT, "middle")}"""


def svg(h, uid, body, blobs):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
  {defs(uid)}
  <clipPath id="clip-{uid}"><rect width="{W}" height="{h}" rx="24"/></clipPath>
  <g clip-path="url(#clip-{uid})">
    <rect width="{W}" height="{h}" fill="url(#bg-{uid})"/>{blobs}
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="24" fill="none" stroke="#FFFFFF" stroke-opacity="0.06"/>
  {body}
</svg>
"""


# ---- header ------------------------------------------------------------------
def header():
    uid, h = "hd", 300
    blobs = (blob(220, 60, 260, BLUE, uid, 16, 50, 30, 0.45)
             + blob(1060, 300, 240, PURPLE, uid, 19, -50, -40, 0.35))
    cx, cy, cw, ch = 80, 50, W - 160, 200
    pills, px = "", cx + 40
    for lbl in ["3× National Data Science Titles", "COO · BNCC Kemanggisan", "Jakarta, Indonesia"]:
        w, s = pill(px, cy + 138, lbl, uid)
        pills += s
        px += w + 10
    body = glass(cx, cy, cw, ch, uid, rx=24) + f"""
  <rect x="{cx+40}" y="{cy+40}" width="44" height="4" rx="2" fill="url(#accent-{uid})"/>
  {text(cx+40, cy+90, "Ivan William Lianata", 42, 700, TEXT, ls=-0.5)}
  {text(cx+40, cy+120, "Data Science Student @ BINUS University  ·  GPA 3.94 / 4.00", 18, 500, BLUE_SOFT)}
  {pills}
"""
    return svg(h, uid, body, blobs)


# ---- stats -------------------------------------------------------------------
def stats():
    uid, h = "st", 130
    blobs = blob(150, 130, 200, BLUE, uid, 15, 40, 0, 0.35) + blob(1050, 0, 200, PURPLE, uid, 18, -40, 0, 0.3)
    items = [("3×", "National Titles"), ("3.94", "GPA / 4.00"), ("250+", "Members Led"), ("27", "Projects on GitHub")]
    n, gap, m = len(items), 16, 30
    cw = (W - 2 * m - gap * (n - 1)) / n
    body = ""
    for i, (num, lbl) in enumerate(items):
        x = m + i * (cw + gap)
        body += glass(x, 20, cw, 90, uid, rx=18)
        body += text(x + cw / 2, 62, num, 28, 700, TEXT, "middle")
        body += text(x + cw / 2, 88, lbl, 13, 500, MUTED, "middle")
    return svg(h, uid, body, blobs)


# ---- skills ------------------------------------------------------------------
def skills():
    uid = "sk"
    tags = ["Python", "R", "SQL", "Scikit-learn", "LightGBM", "XGBoost", "CatBoost", "ConvNeXt",
            "Optuna", "SHAP", "Statistics", "Streamlit", "AWS", "Jupyter", "Git"]
    m, pad, gap, row_h = 30, 32, 10, 40
    x, y, rows, placed = m + pad, 20 + 32, 1, []
    for t in tags:
        w = est_w(t, 13) + 28
        if x + w > W - m - pad:
            x, y, rows = m + pad, y + row_h, rows + 1
        placed.append((x, y, t))
        x += w + gap
    h = 20 + 32 + rows * row_h + 20
    blobs = blob(100, h, 180, BLUE, uid, 14, 30, 0, 0.3) + blob(1100, 0, 180, PURPLE, uid, 16, -30, 0, 0.28)
    body = glass(m, 20, W - 2 * m, h - 40, uid, rx=20)
    for x, y, t in placed:
        body += pill(x, y, t, uid)[1]
    return svg(h, uid, body, blobs)


if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        old.unlink()
    (OUT / "header.svg").write_text(header(), encoding="utf-8")
    (OUT / "stats.svg").write_text(stats(), encoding="utf-8")
    (OUT / "skills.svg").write_text(skills(), encoding="utf-8")
    print("built", len(list(OUT.glob("*.svg"))), "svgs")
