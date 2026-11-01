#!/usr/bin/env python3
"""Bring the org-profile hero banners up to the current design and refresh their live stats.

The two profile heroes (hero-dark.svg / hero-light.svg) were supplied as files, so this edits them in
place and is safe to re-run: it rounds the corners and grows the canvas only once, and replaces its own
buttons/footnote/stats block (between the tc:band markers) every time. Needs network (registry versions).

Usage: python3 tools/banners/make_profile_hero.py profile/assets
"""
import re
import sys

import herolib as hl

ROOT = sys.argv[1]
H = hl.HERO_H
FOOT = "Sub-second search · One bug, one issue · Pay for GB, not seats"
BORDER = {"dark": "#FFFFFF", "light": "#000000"}
CARD_END = 56 + 308  # the terminal card's y + height

cells = hl.profile_cells(hl.package_cells()["_versions"])

for mode in ("dark", "light"):
    path = f"{ROOT}/hero-{mode}.svg"
    s = open(path).read()

    if "heroClip" not in s:  # rounded corners + hairline border
        s = s.replace("</defs>", '  <clipPath id="heroClip"><rect width="1200" height="420" rx="20"/></clipPath>\n  </defs>', 1)
        s = re.sub(r"(</defs>\n)", r'\1  <g clip-path="url(#heroClip)">\n', s, count=1)
        s = s.rstrip()
        assert s.endswith("</svg>")
        s = (s[: -len("</svg>")] + '  </g>\n  <rect x="0.5" y="0.5" width="1199" height="419" rx="19.5" fill="none" '
             f'stroke="{BORDER[mode]}" stroke-opacity="0.12"/>\n</svg>\n')

    if 'viewBox="0 0 1200 420"' in s:  # grow once to make room for the stats panel
        s = s.replace('height="420" viewBox="0 0 1200 420"', f'height="{H}" viewBox="0 0 1200 {H}"')
        s = s.replace('<rect width="1200" height="420"', f'<rect width="1200" height="{H}"')
        s = s.replace('<clipPath id="heroClip"><rect width="1200" height="420" rx="20"/>', f'<clipPath id="heroClip"><rect width="1200" height="{H}" rx="20"/>')
        s = s.replace('height="419" rx="19.5"', f'height="{H - 1}" rx="19.5"')

    # drop the old footnote and any previous generated block, then write a fresh one
    s = re.sub(r'\s*<text x="1140" y="[\d.]+" text-anchor="end"[^>]*>.*?</text>', "", s)
    s = re.sub(r"\n  <!-- tc:band -->.*?<!-- /tc:band -->\n", "\n", s, flags=re.S)
    cy = CARD_END + 28
    band = (f'  <!-- tc:band -->\n  <g>\n    {hl.round_buttons([("book", False), ("arrow", True), ("tag", False), ("globe", False)], mode, 640, cy)}\n'
            f'    {hl.footnote(FOOT, cy, mode)}\n  </g>\n  <g>\n    {hl.stats_panel(cells, mode)}\n  </g>\n  <!-- /tc:band -->\n')
    marker = '  </g>\n  <rect x="0.5" y="0.5"'
    assert marker in s, "closing marker not found"
    s = s.replace(marker, band + marker, 1)
    open(path, "w").write(s)
    print("updated", path)
