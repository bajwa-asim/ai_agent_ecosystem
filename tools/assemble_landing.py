# Assembles one landing HTML from Page-1..Page-5 sections (marker-based).
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def slice_between(html: str, start: str, end: str, *, include_end: bool = False) -> str:
    a = html.find(start)
    if a == -1:
        raise SystemExit(f"start not found: {start!r}")
    b = html.find(end, a + len(start))
    if b == -1:
        raise SystemExit(f"end not found after start: {end!r}")
    if include_end:
        b += len(end)
    return html[a:b]


def extract_script_page2(p2: str) -> str:
    start = p2.find("<script>\n    // Micro-interaction for cards")
    if start == -1:
        start = p2.find("<script>")
    end = p2.find("</script>", start)
    if start == -1 or end == -1:
        raise SystemExit("Could not find Page-2 script block")
    # Include FAQ in same block if present later — Page-2 has single </script> at end
    end = p2.rfind("</script>", start)
    return p2[start : end + len("</script>")]


def main() -> None:
    p1 = (ROOT / "Page-1" / "code.html").read_text(encoding="utf-8")
    p2 = (ROOT / "Page-2" / "code.html").read_text(encoding="utf-8")
    p3 = (ROOT / "Page-3" / "code.html").read_text(encoding="utf-8")
    p4 = (ROOT / "Page-4" / "code.html").read_text(encoding="utf-8")
    p5 = (ROOT / "Page-5" / "code.html").read_text(encoding="utf-8")

    nav = slice_between(p4, "<!-- TopNavBar -->", "</header>", include_end=True)

    hero = slice_between(
        p5, "<!-- Hero Section -->", "<!-- Our AI Agents & Tools Section -->", include_end=False
    )

    agents_cta = slice_between(
        p2,
        "<!-- Our AI Agents & Tools Section -->",
        "<!-- The Enterprise Shift: Legacy Replace Section -->",
        include_end=False,
    )

    modules = slice_between(
        p1,
        "<!-- Software Modules Section -->",
        "</main>",
        include_end=False,
    )
    modal = slice_between(
        p1,
        "<!-- Modules Modal Overlay -->",
        "<script>",
        include_end=False,
    )

    enterprise = slice_between(
        p3,
        "<!-- Redesigned Software Comparison Section -->",
        "<!-- Pricing Plans Section -->",
        include_end=False,
    )

    pricing = slice_between(
        p2,
        "<!-- Executive Pricing Plans -->",
        "<!-- CTA 3: Before FAQ Section -->",
        include_end=False,
    )
    faq = slice_between(
        p2,
        "<!-- FAQ Section -->",
        "<!-- Software Modules Section -->",
        include_end=False,
    )
    unlock = slice_between(
        p2,
        "<!-- CTA 3: Before FAQ Section -->",
        "<!-- FAQ Section -->",
        include_end=False,
    )

    footer = slice_between(
        p2,
        '<footer class="bg-surface-container-lowest border-t border-outline-variant/15">',
        "</footer>",
        include_end=True,
    )

    head = slice_between(p1, "<!DOCTYPE html>", "</head>", include_end=True)

    if ".comparison-gradient" not in head:
        head = head.replace(
            "</style>",
            """        .comparison-gradient {
            background: linear-gradient(to bottom, rgba(242, 202, 80, 0.05) 0%, transparent 100%);
        }
    </style>""",
            1,
        )

    scripts = extract_script_page2(p2)

    body_inner = "\n".join(
        [
            nav,
            '<main class="max-w-container-max mx-auto">',
            hero,
            agents_cta,
            modules,
            enterprise,
            pricing,
            faq,
            unlock,
            "</main>",
            footer,
            modal,
            scripts,
        ]
    )

    out = (
        head
        + '\n<body class="bg-background text-on-background font-body-md selection:bg-primary selection:text-on-primary">\n'
        + body_inner
        + "\n</body></html>\n"
    )

    out_dir = ROOT / "assembled-landing"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "code.html"
    out_path.write_text(out, encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
