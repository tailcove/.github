"""Shared pieces for the hero banners: live registry data, the round icon buttons, the footnote
line and the stats panel. Imported by make_heroes.py and make_profile_hero.py (not run directly).

Live values (latest version, release date, gzipped size of the published npm core file) are read
from the registries every time a hero is generated, so regenerate the heroes after each release.
"""
import gzip
import io
import json
import os
import re
import tarfile
import time
import urllib.request
from datetime import datetime
from html import escape

SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
HERO_H = 556  # hero height: 420 for the banner proper + the stats panel

# 24x24 stroke icons
ICONS = {
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H19v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5V5.5M8 7h7"/>',
    "arrow": '<path d="M7 17 17 7M8 7h9v9"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="m3 7 9 4 9-4M12 11v10"/>',
    "bug": '<rect x="8" y="8" width="8" height="11" rx="4"/><path d="M12 8V5M9 5.5 10.5 8M15 5.5 13.5 8M4.5 12H8M16 12h3.5M4.5 17H8M16 17h3.5"/>',
    "tag": '<path d="M3 12V4h8l10 10-7 7z"/><circle cx="7.5" cy="8.5" r="1.2"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "weight": '<path d="M6 8h12l2 12H4z"/><circle cx="12" cy="5" r="2"/>',
    "braces": '<path d="M9 4C6 4 7 9 4 12c3 3 2 8 5 8M15 4c3 0 2 5 5 8-3 3-2 8-5 8"/>',
    "scale": '<path d="M12 3v18M5 7h14"/><path d="M5 7 2 14a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
    "layers": '<path d="m12 2 10 6-10 6L2 8z"/><path d="m2 12 10 6 10-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-4 5-4 13 0 18M12 3c4 5 4 13 0 18"/>',
    "pulse": '<path d="M3 12h5l2-6 4 12 2-6h5"/>',
}

THEME = {
    "dark": dict(fill="#FFFFFF", fill_o="0.06", stroke="#FFFFFF", stroke_o="0.18", text="#F4F5F8",
                 pa="#FF5F2E", pb="#FFB199", ptext="#2A0D04", panel="#FFFFFF", panel_o="0.045",
                 pstroke="#FFFFFF", pstroke_o="0.12", label="#9399A8", value="#F4F5F8", unit="#9399A8",
                 cap="#6C7283", accent="#FFB199", div_o="0.09", foot="#6C7283"),
    "light": dict(fill="#000000", fill_o="0.04", stroke="#000000", stroke_o="0.16", text="#0A0A0A",
                  pa="#C7340F", pb="#F0461A", ptext="#FFFFFF", panel="#FFFFFF", panel_o="0.62",
                  pstroke="#000000", pstroke_o="0.10", label="#6F6F6A", value="#0A0A0A", unit="#6F6F6A",
                  cap="#8A8A85", accent="#C7340F", div_o="0.09", foot="#6B6B66"),
}


# ---------------------------------------------------------------- live registry data
def _fetch(url, fresh=False):
    """fresh=True bypasses CDN caches: PyPI's JSON is cached up to 15 minutes, so right after a release the
    plain URL can still return the previous version and the banner would show a stale number."""
    if fresh:
        url += ("&" if "?" in url else "?") + f"_={int(time.time())}"
    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
    # GitHub's API allows 60 anonymous requests an hour per address, and Actions runners share addresses
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def _date(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return d.strftime("%b %-d, %Y")


def _npm(pkg):
    data = json.loads(_fetch(f"https://registry.npmjs.org/{pkg.replace('/', '%2f')}", fresh=True))
    version = data["dist-tags"]["latest"]
    tar = _fetch(data["versions"][version]["dist"]["tarball"])
    with tarfile.open(fileobj=io.BytesIO(tar), mode="r:gz") as t:
        core = t.extractfile("package/dist/index.js").read()
    return version, _date(data["time"][version]), len(gzip.compress(core, 9))


def _pypi():
    data = json.loads(_fetch("https://pypi.org/pypi/tailcove/json", fresh=True))
    version = data["info"]["version"]
    return version, _date(data["releases"][version][0]["upload_time_iso_8601"])


def _packagist():
    data = json.loads(_fetch("https://repo.packagist.org/p2/tailcove/laravel.json", fresh=True))["packages"]["tailcove/laravel"]
    top = next(v for v in data if not v["version"].startswith("dev"))
    return top["version"].lstrip("v"), _date(top["time"])


def _kb(n):
    return f"{n / 1000:.1f} kB"


def _github_release(repo):
    """Latest GitHub release of a public repo: (version without the leading v, date)."""
    data = json.loads(_fetch(f"https://api.github.com/repos/{repo}/releases/latest", fresh=True))
    return data["tag_name"].lstrip("v"), _date(data["published_at"])


def _agent_cells():
    """The agent is a Go binary released on GitHub, not a registry package: its version is the latest release."""
    av, ad = _github_release("tailcove/agent")
    return [("tag", "VERSION", av, f"released {ad}"), ("chip", "PLATFORM", "Linux, macOS", "amd64 and arm64"),
            ("box", "DEPENDENCIES", "None", "one static binary"), ("pulse", "SENDS", "Logs + metrics", "files, journald, Docker, Kubernetes"),
            ("scale", "LICENSE", "MIT", "open source")]


def _terraform_cells():
    """The provider is a Go plugin released from GitHub: its version is the latest release (a published one, so a
    release candidate does not show)."""
    tv, td = _github_release("tailcove/terraform-provider-tailcove")
    return [("tag", "VERSION", f"v{tv}", f"released {td}"), ("chip", "TERRAFORM", "1.0+", "and OpenTofu"),
            ("layers", "RESOURCES", "3", "source, monitor, alert"), ("braces", "DATA SOURCES", "3", "source, policy, schedule"),
            ("scale", "LICENSE", "MIT", "open source")]


def package_cells(only=None):
    """name -> list of (icon, label, value, caption), read live. only="agent" reads just the agent release."""
    if only == "agent":
        return {"agent": _agent_cells()}
    if only == "terraform":
        return {"terraform": _terraform_cells()}

    nv, nd, ns = _npm("@tailcove/node")
    bv, bd, bs = _npm("@tailcove/browser")
    pv, pd = _pypi()
    lv, ld = _packagist()
    return {
        "node": [("tag", "VERSION", nv, f"released {nd}"), ("chip", "NODE.JS", "18+", "and newer"),
                 ("weight", "SIZE", _kb(ns), "gzipped, core client"), ("braces", "TYPES", "Included", "TypeScript"),
                 ("scale", "LICENSE", "MIT", "open source")],
        "browser": [("tag", "VERSION", bv, f"released {bd}"), ("weight", "SIZE", _kb(bs), "gzipped, core client"),
                    ("layers", "BUILDS", "ESM · CJS · UMD", "plus a script tag"), ("globe", "FRAMEWORKS", "4 adapters", "React, Vue, Svelte, Next.js"),
                    ("scale", "LICENSE", "MIT", "open source")],
        "python": [("tag", "VERSION", pv, f"released {pd}"), ("chip", "PYTHON", "3.9+", "and newer"),
                   ("box", "DEPENDENCIES", "None", "standard library only"), ("braces", "TYPED", "Yes", "ships type hints"),
                   ("scale", "LICENSE", "MIT", "open source")],
        "laravel": [("tag", "VERSION", lv, f"released {ld}"), ("chip", "PHP", "8.1+", "and newer"),
                    ("layers", "LARAVEL", "10 to 13", "supported majors"), ("arrow", "SENT", "After response", "never slows a request"),
                    ("scale", "LICENSE", "MIT", "open source")],
        "agent": _agent_cells(),
        "terraform": _terraform_cells(),
        "_versions": {"laravel": lv, "node": nv, "python": pv, "browser": bv},
    }


def profile_cells(versions):
    return [("box", "LARAVEL", f"v{versions['laravel']}", "Packagist"), ("box", "NODE.JS", f"v{versions['node']}", "npm"),
            ("box", "PYTHON", f"v{versions['python']}", "PyPI"), ("box", "BROWSER", f"v{versions['browser']}", "npm")]


# ---------------------------------------------------------------- drawing
def icon(name, x, y, color, size=14):
    return (f'<g transform="translate({x} {y}) scale({size / 24})" fill="none" stroke="{color}" stroke-width="2.1" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def round_buttons(items, mode, x, cy, d=34, gap=10):
    """Round icon-only buttons, left-aligned at x and centred on cy. items: (icon, primary).
    Purely visual: an image can't hold separate links, so the READMEs repeat them as text links."""
    c = THEME[mode]
    out = []
    for i, (ic, primary) in enumerate(items):
        cx = x + d / 2 + i * (d + gap)
        if primary:
            out.append(f'<defs><linearGradient id="rb{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["pa"]}"/>'
                       f'<stop offset="1" stop-color="{c["pb"]}"/></linearGradient></defs>'
                       f'<circle cx="{cx}" cy="{cy}" r="{d / 2}" fill="url(#rb{i})"/>')
            col = c["ptext"]
        else:
            out.append(f'<circle cx="{cx}" cy="{cy}" r="{d / 2 - 0.5}" fill="{c["fill"]}" fill-opacity="{c["fill_o"]}" '
                       f'stroke="{c["stroke"]}" stroke-opacity="{c["stroke_o"]}"/>')
            col = c["text"]
        out.append(icon(ic, cx - 8, cy - 8, col, 16))
    return "\n    ".join(out)


def footnote(text, cy, mode):
    """Right-aligned at x=1140 on the buttons' line; wraps to two lines when too long to sit beside them."""
    col = THEME[mode]["foot"]
    base = f'text-anchor="end" font-family="{SANS}" font-size="12.5" fill="{col}"'
    if len(text) * 5.9 <= 270:
        return f'<text x="1140" y="{cy + 4.5}" {base}>{escape(text)}</text>'
    parts = text.split(" · ")
    best = min(range(1, len(parts)), key=lambda i: abs(len(" · ".join(parts[:i])) - len(" · ".join(parts[i:]))))
    l1, l2 = " · ".join(parts[:best]), " · ".join(parts[best:])
    return (f'<text x="1140" y="{cy - 3}" {base}>{escape(l1)}</text>'
            f'<text x="1140" y="{cy + 13}" {base}>{escape(l2)}</text>')


def _split_unit(value):
    m = re.match(r"^([\d.]+)\s*(\S*)$", value)
    return (m.group(1), m.group(2)) if m else (value, "")


def stats_panel(cells, mode, y=432, h=92, x=72, w=1056):
    """Glass panel: icon + label, big value with a small unit, caption. Cells are sized to their content."""
    c = THEME[mode]
    need = [max(len(label) * 7.8 + 22, len(value) * 14.4, len(cap) * 6.3) + 62 for _, label, value, cap in cells]
    widths = [n * w / sum(need) for n in need]
    starts = [x + sum(widths[:i]) for i in range(len(cells))]
    parts = [f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="18" fill="{c["panel"]}" '
             f'fill-opacity="{c["panel_o"]}" stroke="{c["pstroke"]}" stroke-opacity="{c["pstroke_o"]}"/>']
    for i, (ic, label, value, cap) in enumerate(cells):
        cx = starts[i]
        if i:
            parts.append(f'<rect x="{cx:.1f}" y="{y + 20}" width="1" height="{h - 40}" fill="{c["pstroke"]}" fill-opacity="{c["div_o"]}"/>')
        num, unit = _split_unit(value)
        col = c["accent"] if label == "VERSION" else c["value"]
        unit_svg = f'<tspan font-size="14" font-weight="600" fill="{c["unit"]}" dx="3">{escape(unit)}</tspan>' if unit else ""
        parts.append(icon(ic, cx + 28, y + 17, c["accent"], 13))
        parts.append(f'<text x="{cx + 48:.1f}" y="{y + 28}" font-family="{SANS}" font-size="10.5" font-weight="650" letter-spacing="1.2" fill="{c["label"]}">{escape(label)}</text>')
        parts.append(f'<text x="{cx + 28:.1f}" y="{y + 60}" font-family="{SANS}" font-size="27" font-weight="700" letter-spacing="-0.8" fill="{col}">{escape(num)}{unit_svg}</text>')
        parts.append(f'<text x="{cx + 28:.1f}" y="{y + 79}" font-family="{SANS}" font-size="11.5" fill="{c["cap"]}">{escape(cap)}</text>')
    return "\n    ".join(parts)
