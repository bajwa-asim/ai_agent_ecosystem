"""Generate cognitive-bootstrap.css + patch HTML for Bootstrap 4.6 without Tailwind."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_CSS = ROOT / "assembled-landing" / "css" / "cognitive-bootstrap.css"
IN_HTML = ROOT / "assembled-landing" / "code.tailwind-backup.html"
OUT_HTML = ROOT / "assembled-landing" / "code.html"

# Design tokens (from original tailwind config)
C = {
    "background": "#131313",
    "surface": "#131313",
    "surface_low": "#1c1b1b",
    "surface_high": "#2a2a2a",
    "surface_lowest": "#0e0e0e",
    "surface_bright": "#393939",
    "primary": "#f2ca50",
    "on_primary": "#3c2f00",
    "on_primary_fixed": "#241a00",
    "on_background": "#e5e2e1",
    "on_surface": "#e5e2e1",
    "on_surface_variant": "#d0c5af",
    "outline": "#99907c",
    "outline_variant": "#4d4635",
    "error": "#ffb4ab",
    "tertiary": "#e7c9a6",
    "primary_fixed_dim": "#e9c349",
}

MD = "768px"
LG = "1024px"
SM = "640px"


def rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def esc(name: str) -> str:
    return name.replace("/", r"\/").replace(":", r"\:").replace("[", r"\[").replace("]", r"\]")


lines = []
L = lines.append

L("/* Cognitive Nexus — utility layer matching former Tailwind build + Bootstrap 4.6 coexistence */")
L(":root {")
for k, v in C.items():
    L(f"  --cn-{k}: {v};")
L("  --cn-container: 1280px;")
L("  --cn-gutter: 24px;")
L("  --cn-margin-desktop: 40px;")
L("  --cn-margin-mobile: 16px;")
L("  --cn-base: 8px;")
L("}")

L("html.dark, html.dark body { background: var(--cn-background); }")
L("body.bg-background {")
L("  font-family: 'Hanken Grotesk', system-ui, -apple-system, sans-serif;")
L("  background-color: var(--cn-background) !important;")
L("  color: var(--cn-on_background) !important;")
L("  -webkit-font-smoothing: antialiased;")
L("}")

L("::selection { background: var(--cn-primary); color: var(--cn-on_primary); }")

# Material + components from original <style>
L(
    """.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 300, 'GRAD' 0, 'opsz' 24;
  font-style: normal;
  line-height: 1;
  display: inline-block;
  vertical-align: middle;
}
.brushed-gold-icon {
  background: linear-gradient(135deg, #f2ca50 0%, #8B7355 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.card-inner-glow {
  box-shadow: inset 0 1px 0 0 rgba(242, 202, 80, 0.1);
}
.hero-glow {
  background: radial-gradient(circle at 50% 50%, rgba(242, 202, 80, 0.08) 0%, transparent 70%);
}
.comparison-gradient {
  background: linear-gradient(to bottom, rgba(242, 202, 80, 0.05) 0%, transparent 100%);
}
.hero-carbon-bg {
  background-image: url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
}
"""
)

# Typography
L(
    """/* font-* = font-family (original Tailwind theme); text-* = sizes */
.font-body-md, .font-body-lg, .font-label-md, .font-label-sm,
.font-headline-sm, .font-headline-md, .font-display-lg {
  font-family: "Hanken Grotesk", system-ui, -apple-system, sans-serif;
}
.text-display-lg-mobile { font-size: 32px; line-height: 40px; letter-spacing: -0.02em; font-weight: 700; }
@media (min-width: %s) {
  .md\\:text-display-lg { font-size: 48px; line-height: 56px; letter-spacing: -0.02em; font-weight: 700; }
}
@media (min-width: %s) {
  .sm\\:text-display-lg { font-size: 48px; line-height: 56px; letter-spacing: -0.02em; font-weight: 700; }
}
.text-body-md { font-size: 16px; line-height: 24px; }
.text-body-lg { font-size: 18px; line-height: 28px; }
.text-label-md { font-size: 14px; line-height: 20px; letter-spacing: 0.01em; font-weight: 500; }
.text-label-sm { font-size: 12px; line-height: 16px; letter-spacing: 0.05em; font-weight: 600; }
.text-headline-sm { font-size: 20px; line-height: 28px; font-weight: 600; }
.text-headline-md { font-size: 24px; line-height: 32px; font-weight: 600; }
.text-display-lg { font-size: 48px; line-height: 56px; letter-spacing: -0.02em; font-weight: 700; }
"""
    % (MD, SM)
)

# Colors text/bg
pairs = [
    ("text-primary", f"color: {C['primary']}"),
    ("text-on-primary", f"color: {C['on_primary']}"),
    ("text-on-primary-fixed", f"color: {C['on_primary_fixed']}"),
    ("text-on-background", f"color: {C['on_background']}"),
    ("text-on-surface", f"color: {C['on_surface']}"),
    ("text-on-surface-variant", f"color: {C['on_surface_variant']}"),
    ("text-error", f"color: {C['error']}"),
    ("bg-background", f"background-color: {C['background']}"),
    ("bg-surface", f"background-color: {C['surface']}"),
    ("bg-surface-container-low", f"background-color: {C['surface_low']}"),
    ("bg-surface-container-high", f"background-color: {C['surface_high']}"),
    ("bg-surface-container-lowest", f"background-color: {C['surface_lowest']}"),
    ("bg-primary", f"background-color: {C['primary']}"),
]
for cls, rule in pairs:
    L(f".{esc(cls)} {{ {rule}; }}")

L(f".text-on-surface-variant\\/60 {{ color: {rgba(C['on_surface_variant'], 0.6)}; }}")
L(f".text-on-surface-variant\\/80 {{ color: {rgba(C['on_surface_variant'], 0.8)}; }}")
L(f".text-primary\\/70 {{ color: {rgba(C['primary'], 0.7)}; }}")

L(f".bg-background\\/80 {{ background-color: {rgba(C['background'], 0.8)}; }}")
L(f".bg-primary\\/5 {{ background-color: {rgba(C['primary'], 0.05)}; }}")

# Borders
L(".border { border-width: 1px; border-style: solid; }")
L(".border-2 { border-width: 2px; border-style: solid; }")
L(".border-b { border-bottom-width: 1px; border-bottom-style: solid; }")
L(".border-b-2 { border-bottom-width: 2px; border-bottom-style: solid; }")
L(".border-t { border-top-width: 1px; border-top-style: solid; }")
L(".border-y { border-top-width: 1px; border-bottom-width: 1px; border-style: solid solid; }")

for alpha, suffix in [(0.1, "10"), (0.15, "15"), (0.2, "20"), (0.3, "30")]:
    L(
        f".border-outline-variant\\/{suffix} {{ border-color: {rgba(C['outline_variant'], alpha)}; }}"
    )
L(f".border-outline\\/30 {{ border-color: {rgba(C['outline'], 0.3)}; }}")
L(f".border-primary {{ border-color: {C['primary']}; }}")
for alpha, sfx in [(0.2, "20"), (0.3, "30"), (0.4, "40")]:
    L(f".border-primary\\/{sfx} {{ border-color: {rgba(C['primary'], alpha)}; }}")

# Layout
L(
    """.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }
.sticky { position: sticky; }
.inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
.top-0 { top: 0; }
.top-4 { top: 1rem; }
.right-4 { right: 1rem; }
.-top-4 { top: -1rem; }
.left-1\\/2 { left: 50%; }
.-translate-x-1\\/2 { transform: translateX(-50%); }
.z-10 { z-index: 10; }
.z-50 { z-index: 50; }
.z-100 { z-index: 100; }
.pointer-events-none { pointer-events: none; }
.overflow-hidden { overflow: hidden; }
.max-h-0 { max-height: 0; }
"""
)

L(
    """.flex { display: flex; }
.inline-flex { display: inline-flex; }
.flex-col { flex-direction: column; }
.flex-grow { flex-grow: 1; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-baseline { align-items: baseline; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.gap-1 { gap: 0.25rem; }
.gap-2 { gap: 0.5rem; }
.gap-4 { gap: 1rem; }
.gap-base { gap: var(--cn-base); }
.gap-gutter { gap: var(--cn-gutter); }
"""
)

L(
    """.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.grid-cols-12 { grid-template-columns: repeat(12, minmax(0, 1fr)); }
@media (min-width: %s) {
  .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .md\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (min-width: %s) {
  .lg\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}
.col-span-3 { grid-column: span 3 / span 3; }
.col-span-4 { grid-column: span 4 / span 4; }
.col-span-5 { grid-column: span 5 / span 5; }
"""
    % (MD, LG)
)

L(
    """.hidden { display: none !important; }
@media (min-width: %s) {
  .md\\:flex { display: flex !important; }
  .md\\:flex-row { flex-direction: row !important; }
  .md\\:items-start { align-items: flex-start !important; }
  .md\\:mb-0 { margin-bottom: 0 !important; }
}
@media (min-width: %s) {
  .sm\\:flex-row { flex-direction: row !important; }
  .sm\\:gap-gutter { gap: var(--cn-gutter); }
}
"""
    % (MD, SM)
)

# Spacing
margins = [
    ("m", "margin"),
    ("mx", ("margin-left", "margin-right")),
    ("my", ("margin-top", "margin-bottom")),
    ("mt", "margin-top"),
    ("mb", "margin-bottom"),
    ("pt", "padding-top"),
    ("pb", "padding-bottom"),
    ("px", ("padding-left", "padding-right")),
    ("py", ("padding-top", "padding-bottom")),
    ("p", "padding"),
]
vals = {
    "0": "0",
    "1": "0.25rem",
    "2": "0.5rem",
    "3": "0.75rem",
    "4": "1rem",
    "5": "1.25rem",
    "6": "1.5rem",
    "8": "2rem",
    "10": "2.5rem",
    "12": "3rem",
    "16": "4rem",
    "20": "5rem",
    "24": "6rem",
    "base": "var(--cn-base)",
    "gutter": "var(--cn-gutter)",
    "margin-desktop": "var(--cn-margin-desktop)",
    "margin-mobile": "var(--cn-margin-mobile)",
}


def add_space(prefix: str, name: str, prop):
    v = vals[name]
    if isinstance(prop, tuple):
        L(f".{prefix}-{name} {{ {prop[0]}: {v}; {prop[1]}: {v}; }}")
    else:
        L(f".{prefix}-{name} {{ {prop}: {v}; }}")


# py-base / px etc. token spacing
L(".py-base { padding-top: var(--cn-base); padding-bottom: var(--cn-base); }\n")

for n in ["0", "1", "2", "4", "6", "8", "10", "16", "20", "24"]:
    add_space("m", n, "margin")
    add_space("mt", n, "margin-top")
    add_space("mb", n, "margin-bottom")
    add_space("mx", n, ("margin-left", "margin-right"))
    add_space("my", n, ("margin-top", "margin-bottom"))
    add_space("p", n, "padding")
    add_space("px", n, ("padding-left", "padding-right"))
    add_space("py", n, ("padding-top", "padding-bottom"))
    add_space("pt", n, "padding-top")
    add_space("pb", n, "padding-bottom")

add_space("px", "margin-desktop", ("padding-left", "padding-right"))
add_space("px", "gutter", ("padding-left", "padding-right"))
add_space("p", "gutter", "padding")
add_space("p", "margin-mobile", "padding")
add_space("py", "gutter", ("padding-top", "padding-bottom"))
add_space("pb", "gutter", "padding-bottom")
add_space("mb", "base", "margin-bottom")
add_space("mb", "gutter", "margin-bottom")

L(".mx-auto { margin-left: auto; margin-right: auto; }")
L(".max-w-2xl { max-width: 42rem; }")
L(".max-w-3xl { max-width: 48rem; }")
L(".max-w-4xl { max-width: 56rem; }")
L(".max-w-container-max { max-width: var(--cn-container); }")

L(".w-full { width: 100%; }")
L(".w-10 { width: 2.5rem; }")
L(".h-10 { height: 2.5rem; }")
L(".h-auto { height: auto; }")

L(
    """.rounded { border-radius: 0.25rem; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-xl { border-radius: 0.75rem; }
.rounded-full { border-radius: 9999px; }
"""
)

L(
    """.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.font-bold { font-weight: 700; }
.font-medium { font-weight: 500; }
.font-normal { font-weight: 400; }
.uppercase { text-transform: uppercase; }
.italic { font-style: italic; }
.tracking-tight { letter-spacing: -0.025em; }
.tracking-wider { letter-spacing: 0.05em; }
.tracking-widest { letter-spacing: 0.1em; }
.leading-relaxed { line-height: 1.625; }
.leading-tight { line-height: 1.25; }
.cursor-pointer { cursor: pointer; }
.object-cover { object-fit: cover; }
.opacity-10 { opacity: 0.1; }
"""
)

L(
    """.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
.text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
.text-6xl { font-size: 3.75rem; line-height: 1; }
"""
)

L(
    """.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.25), 0 4px 6px -4px rgba(0, 0, 0, 0.2);
}
.shadow-xl {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.25);
}
.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
}
"""
)
L(
    f".shadow-primary\\/10 {{ box-shadow: 0 25px 50px -12px {rgba(C['primary'], 0.1)}; }}"
)
L(
    f".shadow-primary\\/20 {{ box-shadow: 0 25px 50px -12px {rgba(C['primary'], 0.2)}, 0 10px 15px -3px {rgba(C['primary'], 0.15)}; }}"
)
L(
    f".shadow-primary\\/30 {{ box-shadow: 0 25px 50px -12px {rgba(C['primary'], 0.3)}, 0 10px 15px -3px {rgba(C['primary'], 0.2)}; }}"
)

L(
    """.transition-all { transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
.transition-colors { transition-property: color, background-color, border-color; transition-duration: 150ms; }
.transition-transform { transition-property: transform; transition-duration: 300ms; }
.duration-200 { transition-duration: 200ms; }
.duration-300 { transition-duration: 300ms; }
.ease-in-out { transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }
"""
)

L(
    """.divide-y.divide-outline-variant\\/10 > * + * {
  border-top: 1px solid """ + rgba(C["outline_variant"], 0.1) + """;
}
"""
)

L(
    """.space-y-4 > * + * { margin-top: 1rem; }
.space-y-gutter > * + * { margin-top: var(--cn-gutter); }
"""
)

L(
    """.pb-1 { padding-bottom: 0.25rem; }
.pb-gutter { padding-bottom: var(--cn-gutter); }
"""
)

L(
    """.drop-shadow-sm { filter: drop-shadow(0 1px 1px rgba(0,0,0,0.25)); }
.backdrop-blur-sm { backdrop-filter: blur(4px); }
"""
)

L(
    """.focus\\:outline-none:focus { outline: 2px solid transparent; outline-offset: 2px; }
"""
)

# Hover states
L(
    f".hover\\:text-primary-fixed-dim:hover {{ color: {C['primary_fixed_dim']}; }}"
)
L(f".hover\\:text-primary:hover {{ color: {C['primary']}; }}")
L(f".hover\\:text-on-primary:hover {{ color: {C['on_primary']}; }}")
L(f".hover\\:text-tertiary:hover {{ color: {C['tertiary']}; }}")
L(f".hover\\:bg-primary:hover {{ background-color: {C['primary']}; }}")
L(f".hover\\:bg-primary\\/5:hover {{ background-color: {rgba(C['primary'], 0.05)}; }}")
L(f".hover\\:border-primary:hover {{ border-color: {C['primary']}; }}")
L(
    f".hover\\:bg-surface-bright\\/5:hover {{ background-color: {rgba(C['surface_bright'], 0.05)}; }}"
)

L(
    """.hover\\:brightness-110:hover { filter: brightness(1.1); }
.active\\:opacity-80:active { opacity: 0.8; }
.active\\:scale-95:active { transform: scale(0.95); }
"""
)

L(".scale-105 { transform: scale(1.05); }")

L(
    """ul.space-y-4 { list-style: none; padding-left: 0; margin-bottom: 0; }
"""
)

# Modal flex center
L(
    """#modules-modal.flex { display: flex !important; align-items: center; justify-content: center; }
#modules-modal.hidden { display: none !important; }
"""
)

# Bootstrap overrides (minimal)
L(
    """a { color: inherit; }
button { font: inherit; cursor: pointer; }
"""
)

OUT_CSS.parent.mkdir(parents=True, exist_ok=True)
OUT_CSS.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Wrote", OUT_CSS)

# Patch HTML
html = IN_HTML.read_text(encoding="utf-8")
html = html.replace(
    """bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]""",
    "hero-carbon-bg",
)
html = html.replace("z-[100]", "z-100")

new_head = """<!DOCTYPE html><html class="dark" lang="en"><head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" crossorigin="anonymous">
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700;800&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/cognitive-bootstrap.css">
</head>
"""

# Replace from DOCTYPE through </head>
import re

html = re.sub(r"<!DOCTYPE html>.*?</head>\s*", new_head, html, count=1, flags=re.DOTALL)

# Insert jQuery + Bootstrap JS before closing body script
inject = """
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
"""

html = html.replace("<script>\n    // Micro-interaction", inject + "<script>\n    // Micro-interaction", 1)

OUT_HTML.write_text(html, encoding="utf-8")
print("Wrote", OUT_HTML)
