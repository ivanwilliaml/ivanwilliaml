"""Generate the glassmorphism SVG assets used by README.md.

Run:  python assets/build.py
Everything is self-contained SVG (gradients, blur filters, SMIL animation),
so it renders inside GitHub's <img> sandbox with no external resources.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

# ---- design tokens -----------------------------------------------------------
W = 1200
NAVY_0, NAVY_1 = "#060D1F", "#0B1F3A"
BLUE, YELLOW, PURPLE = "#2563EB", "#FACC15", "#7C3AED"
TEXT, MUTED = "#F8FAFC", "#B6C2D6"
FONT = "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"


def defs(uid: str) -> str:
    return f"""
  <defs>
    <linearGradient id="bg-{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{NAVY_0}"/><stop offset="1" stop-color="{NAVY_1}"/>
    </linearGradient>
    <linearGradient id="glass-{uid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.07"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>
    <linearGradient id="stroke-{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.45"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.30"/>
    </linearGradient>
    <linearGradient id="accent-{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{YELLOW}"/><stop offset="1" stop-color="{PURPLE}"/>
    </linearGradient>
    <filter id="blur-{uid}" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="55"/>
    </filter>
    <filter id="shadow-{uid}" x="-10%" y="-10%" width="120%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000" flood-opacity="0.35"/>
    </filter>
  </defs>"""


def blob(cx, cy, r, color, uid, dur, dx, dy, opacity=0.55):
    return f"""
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{opacity}" filter="url(#blur-{uid})">
    <animateTransform attributeName="transform" type="translate"
      values="0 0; {dx} {dy}; 0 0" dur="{dur}s" repeatCount="indefinite" calcMode="spline"
      keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"/>
  </circle>"""


def glass(x, y, w, h, uid, rx=22, shadow=True):
    f = f' filter="url(#shadow-{uid})"' if shadow else ""
    return f"""
  <g{f}>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#glass-{uid})"
      stroke="url(#stroke-{uid})" stroke-width="1.2"/>
    <rect x="{x+1.5}" y="{y+1.5}" width="{w-3}" height="{h*0.45}" rx="{rx-1}"
      fill="#FFFFFF" opacity="0.045"/>
  </g>"""


def text(x, y, s, size, weight=500, fill=TEXT, anchor="start", opacity=1, ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" opacity="{opacity}" letter-spacing="{ls}">{escape(s)}</text>')


def est_w(s, size):  # rough width estimate for pill sizing
    return sum(0.62 if c.isupper() or c.isdigit() else 0.36 if c in " .,·'" else 0.55 for c in s) * size


def pill(x, y, label, uid, size=14, h=32, fill_opacity=0.10, color=TEXT, stroke_color="#FFFFFF"):
    w = est_w(label, size) + 30
    return w, f"""
  <g>
    <rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="#FFFFFF" fill-opacity="{fill_opacity}"
      stroke="{stroke_color}" stroke-opacity="0.28" stroke-width="1"/>
    {text(x + w/2, y + h/2 + size*0.36, label, size, 600, color, "middle")}
  </g>"""


def svg(h, uid, body, blobs):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
  {defs(uid)}
  <rect width="{W}" height="{h}" rx="28" fill="url(#bg-{uid})"/>
  <clipPath id="clip-{uid}"><rect width="{W}" height="{h}" rx="28"/></clipPath>
  <g clip-path="url(#clip-{uid})">{blobs}
    <!-- fine grid for depth -->
    <path d="{' '.join(f'M{x} 0V{h}' for x in range(0, W, 40))} {' '.join(f'M0 {y}H{W}' for y in range(0, h, 40))}"
      stroke="#FFFFFF" stroke-opacity="0.025" stroke-width="1"/>
  </g>
  {body}
</svg>
"""


# ---- 1. header ---------------------------------------------------------------
def header():
    uid, h = "hd", 380
    blobs = (blob(180, 90, 210, BLUE, uid, 14, 60, 40)
             + blob(1010, 80, 190, PURPLE, uid, 17, -50, 50)
             + blob(620, 380, 220, YELLOW, uid, 20, 30, -60, 0.35)
             + blob(1150, 340, 150, BLUE, uid, 12, -40, -30, 0.45))
    cx, cy, cw, ch = 90, 60, W - 180, 260
    pills, px = "", cx + 40
    for lbl in ["🏆 2× National Data Science Champion", "🧑‍💼 COO @ BNCC Kemanggisan", "🔬 ML Researcher", "📍 Jakarta, Indonesia"]:
        w, s = pill(px, cy + 190, lbl, uid)
        pills += s
        px += w + 12
    body = glass(cx, cy, cw, ch, uid, rx=28) + f"""
  <rect x="{cx+40}" y="{cy+44}" width="56" height="5" rx="2.5" fill="url(#accent-{uid})"/>
  {text(cx+40, cy+98, "Ivan William Lianata", 46, 700, TEXT, ls=-0.5)}
  {text(cx+40, cy+134, "Data Science Student @ BINUS University  ·  GPA 3.94 / 4.00", 21, 600, YELLOW)}
  {text(cx+40, cy+166, "I learn fastest by building and competing — and I'm as comfortable leading people as I am training models.", 16, 400, MUTED)}
  {pills}
  <!-- animated status dot -->
  <circle cx="{cx+cw-52}" cy="{cy+44}" r="6" fill="{YELLOW}">
    <animate attributeName="opacity" values="1;0.25;1" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  {text(cx+cw-66, cy+49, "open to collaborate", 13, 600, MUTED, "end")}
"""
    return svg(h, uid, body, blobs)


# ---- 2. impact stats ---------------------------------------------------------
def stats():
    uid, h = "st", 150
    blobs = blob(150, 75, 160, PURPLE, uid, 15, 40, 0, 0.4) + blob(1050, 75, 160, BLUE, uid, 13, -40, 0, 0.5) + blob(600, 160, 140, YELLOW, uid, 18, 0, -30, 0.25)
    items = [("2×", "National Champion"), ("3.94", "GPA / 4.00"), ("250+", "Members Led"),
             ("5,800", "Seminar Registrants"), ("96.9%", "CV Test Accuracy"), ("1,000+", "Applicants → Mentor")]
    n, gap, m = len(items), 16, 30
    cw = (W - 2 * m - gap * (n - 1)) / n
    body = ""
    for i, (num, lbl) in enumerate(items):
        x = m + i * (cw + gap)
        color = YELLOW if i % 3 == 0 else TEXT if i % 3 == 1 else "#C4B5FD"
        body += glass(x, 22, cw, 106, uid, rx=20, shadow=False)
        body += text(x + cw / 2, 74, num, 32, 700, color, "middle")
        body += text(x + cw / 2, 102, lbl, 13, 500, MUTED, "middle")
    return svg(h, uid, body, blobs)


# ---- 3. section headers ------------------------------------------------------
def section(slug, icon, title, subtitle):
    uid, h = "sc-" + slug, 84
    blobs = blob(80, 42, 120, BLUE, uid, 12, 30, 0, 0.45) + blob(1120, 42, 110, PURPLE, uid, 14, -30, 0, 0.4)
    body = glass(20, 12, W - 40, 60, uid, rx=18, shadow=False) + f"""
  <rect x="44" y="30" width="5" height="24" rx="2.5" fill="url(#accent-{uid})"/>
  {text(66, 50, f"{icon}  {title}", 22, 700, TEXT)}
  {text(W-48, 49, subtitle, 13, 500, MUTED, "end")}
"""
    return svg(h, uid, body, blobs)


SECTIONS = [
    ("about", "👋", "About", "who I am"),
    ("record", "🏆", "Competition Record", "8 national placements · 2 titles"),
    ("work", "🔬", "Featured Work", "selected projects"),
    ("skills", "🛠️", "Skills", "what I build with"),
    ("leadership", "🧑‍💼", "Leadership & Community", "click a role to expand"),
    ("certs", "📜", "Certifications", "2025"),
    ("activity", "📈", "GitHub Activity", "auto-updated"),
    ("contact", "📬", "Contact", "let's build something"),
]


# ---- 4. project cards --------------------------------------------------------
def projects():
    uid, h = "pj", 272
    blobs = blob(300, 330, 200, BLUE, uid, 16, 40, -30, 0.45) + blob(900, 0, 200, PURPLE, uid, 14, -40, 30, 0.4) + blob(600, 165, 120, YELLOW, uid, 19, 0, 20, 0.22)
    cards = [
        ("⚽ Football Match Outcome Prediction", "🥇 1st Place · National — Gammafest 2026, IPB University", YELLOW,
         ["Decay-weighted features · Poisson LightGBM / XGBoost / CatBoost",
          "Simplex blending · pseudo-labeling · Bayes-optimal discretization",
          "Won by iterating on SHAP-driven error analysis"]),
        ("🕵️ Deepfake Liveness Detection", "Top 15 of 300+ teams — FindIT 2026 Data Analytics", "#C4B5FD",
         ["ConvNeXt + GeM Pooling · per-class augmentation from EDA",
          "Liveness via micro-texture, not facial shape",
          "96.9% test accuracy with TTA + Out-of-Fold inference"]),
    ]
    m, gap = 30, 20
    cw = (W - 2 * m - gap) / 2
    body = ""
    for i, (title, badge, color, lines) in enumerate(cards):
        x = m + i * (cw + gap)
        body += glass(x, 24, cw, h - 48, uid, rx=24)
        body += text(x + 32, 74, title, 22, 700, TEXT)
        bw, bs = pill(x + 32, 92, badge, uid, 13, 28, 0.12, color, color)
        body += bs
        for j, ln in enumerate(lines):
            y = 160 + j * 34
            body += f'<circle cx="{x+40}" cy="{y-5}" r="3.5" fill="{color}"/>'
            body += text(x + 56, y, ln, 15, 400, MUTED)
    return svg(h, uid, body, blobs)


# ---- 5. skills ---------------------------------------------------------------
def skills():
    groups = [
        ("Machine Learning & AI", YELLOW, ["Python", "Scikit-learn", "LightGBM", "XGBoost", "CatBoost", "Random Forest", "CNN / ConvNeXt", "Optuna", "SHAP", "Feature Engineering", "IBM Granite"]),
        ("Data & Analytics", "#93C5FD", ["R", "SQL", "Statistics", "Data Visualization", "SAP Analytics Cloud", "Excel", "Prompt Engineering"]),
        ("Deployment & Tools", "#C4B5FD", ["Streamlit", "AWS EC2", "AWS SageMaker", "Jupyter", "Kaggle", "Git & GitHub"]),
        ("Professional", TEXT, ["Project & Event Management", "Financial Planning & Budgeting", "Research & Scientific Writing", "Public Speaking", "Mentoring", "Stakeholder Coordination", "Leadership"]),
    ]
    uid = "sk"
    m, pad, row_h, gap = 30, 32, 40, 10
    # layout pass
    y_cursor, layout = 24, []
    for name, color, tags in groups:
        y0 = y_cursor
        x, y = m + pad, y0 + 58
        rows = 1
        placed = []
        for t in tags:
            w = est_w(t, 14) + 30
            if x + w > W - m - pad:
                x, y, rows = m + pad, y + row_h, rows + 1
            placed.append((x, y, t))
            x += w + gap
        card_h = 58 + rows * row_h + 6
        layout.append((y0, card_h, name, color, placed))
        y_cursor += card_h + 16
    h = y_cursor + 8
    blobs = blob(100, 80, 180, BLUE, uid, 15, 30, 40, 0.4) + blob(1100, h - 80, 180, PURPLE, uid, 17, -30, -40, 0.4) + blob(700, h / 2, 140, YELLOW, uid, 21, 20, 0, 0.18)
    body = ""
    for y0, card_h, name, color, placed in layout:
        body += glass(m, y0, W - 2 * m, card_h, uid, rx=22, shadow=False)
        body += f'<rect x="{m+pad}" y="{y0+24}" width="4" height="18" rx="2" fill="{color}"/>'
        body += text(m + pad + 14, y0 + 39, name, 16, 700, TEXT)
        for x, y, t in placed:
            body += pill(x, y - 2, t, uid, 14, 32, 0.09, TEXT if color == TEXT else color)[1]
    return svg(h, uid, body, blobs)


# ---- 6. footer ---------------------------------------------------------------
def footer():
    uid, h = "ft", 130
    blobs = blob(200, 130, 170, YELLOW, uid, 16, 40, 0, 0.22) + blob(1000, 0, 170, PURPLE, uid, 14, -40, 0, 0.4) + blob(600, 65, 160, BLUE, uid, 12, 0, 30, 0.35)
    body = glass(30, 24, W - 60, 82, uid, rx=22, shadow=False) + f"""
  {text(W/2, 62, "“I care about work that genuinely reaches people.”", 19, 600, TEXT, "middle")}
  {text(W/2, 88, "ivanwilliam156@gmail.com  ·  linkedin.com/in/ivanwilliaml  ·  github.com/ivanwilliaml", 13, 500, MUTED, "middle")}
"""
    return svg(h, uid, body, blobs)


if __name__ == "__main__":
    (OUT / "header.svg").write_text(header(), encoding="utf-8")
    (OUT / "stats.svg").write_text(stats(), encoding="utf-8")
    (OUT / "projects.svg").write_text(projects(), encoding="utf-8")
    (OUT / "skills.svg").write_text(skills(), encoding="utf-8")
    (OUT / "footer.svg").write_text(footer(), encoding="utf-8")
    for slug, icon, title, sub in SECTIONS:
        (OUT / f"section-{slug}.svg").write_text(section(slug, icon, title, sub), encoding="utf-8")
    print("built", len(list(OUT.glob("*.svg"))), "svgs")
