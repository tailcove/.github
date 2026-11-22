#!/usr/bin/env python3
"""Generate a package's feature cards (dark + light): six cards in a 3x2 grid, an icon, a title and up to
three lines of text each. The cards hold no live data, so they change only when this file does.

Usage: python3 tools/banners/make_features.py <out-dir>
"""
import sys
import textwrap
from html import escape

OUT = sys.argv[1]
SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(card="#10121B", card_stroke="#FFFFFF", card_so="0.09", glow_o="0.10", tile="#FF5F2E", tile_o="0.12",
                 tile_stroke="#FF5F2E", tile_so="0.30", icon="#FFB199", title="#F4F5F8", text="#9399A8"),
    "light": dict(card="#FFFFFF", card_stroke="#000000", card_so="0.10", glow_o="0.14", tile="#C7340F", tile_o="0.08",
                  tile_stroke="#C7340F", tile_so="0.28", icon="#C7340F", title="#0A0A0A", text="#5C5C58"),
}

# 24x24 stroke icons
ICONS = {
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="m3 7 9 4 9-4M12 11v10"/>',
    "bug": '<rect x="8" y="8" width="8" height="11" rx="4"/><path d="M12 8V5M9 5.5 10.5 8M15 5.5 13.5 8M4.5 12H8M16 12h3.5M4.5 17H8M16 17h3.5"/>',
    "disk": '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "wave": '<path d="M3 12c3-6 6-6 9 0s6 6 9 0"/>',
    "shield": '<path d="M12 2l8 3v6c0 5.5-3.5 9.5-8 11-4.5-1.5-8-5.5-8-11V5z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
}

PACKAGES = {
    "react-native": [
        ("box", "Works in Expo", "Plain JavaScript, no native module: Expo managed and bare, and React Native 0.70 and later."),
        ("bug", "JavaScript crashes", "Uncaught errors and unhandled rejections arrive with the stack and the last 20 steps before them."),
        ("disk", "Kept offline", "With AsyncStorage, lines written offline or just before a crash are sent on the next launch."),
        ("wave", "Batched and retried", "50 lines or 5 seconds, and when the app goes to the background. Retries honour Retry-After."),
        ("shield", "A key safe to ship", "The app key works only for your app ids and has its own rate limit, so a copy cannot use your quota."),
        ("user", "Private by default", "Only the user id you set is sent, never a name or an email. The client never throws into your app."),
    ],
}


def card(i, ic, title, body, t):
    x, y = (i % 3) * 412, (i // 3) * 200
    lines = textwrap.wrap(body, 42)
    assert len(lines) <= 3, (title, lines)
    text = "".join(f'<text x="{x + 28}" y="{y + 106 + n * 22}" font-size="14.5" fill="{t["text"]}">{escape(line)}</text>'
                   for n, line in enumerate(lines))
    return (f'<rect x="{x + 0.5}" y="{y + 0.5}" width="375" height="175" rx="16" fill="{t["card"]}" stroke="{t["card_stroke"]}" stroke-opacity="{t["card_so"]}"/>'
            f'<rect x="{x + 0.5}" y="{y + 0.5}" width="375" height="175" rx="16" fill="url(#glow)"/>'
            f'<rect x="{x + 28}" y="{y + 26}" width="44" height="44" rx="11" fill="{t["tile"]}" fill-opacity="{t["tile_o"]}" stroke="{t["tile_stroke"]}" stroke-opacity="{t["tile_so"]}"/>'
            f'<g transform="translate({x + 38} {y + 36}) scale(1)" fill="none" stroke="{t["icon"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" transform-origin="0 0">{ICONS[ic]}</g>'
            f'<text x="{x + 88}" y="{y + 56}" font-size="19" font-weight="650" letter-spacing="-0.3" fill="{t["title"]}">{escape(title)}</text>'
            + text)


def build(cards, mode):
    t = THEMES[mode]
    label = escape("; ".join(f"{title}: {body}" for _, title, body in cards))
    body = "\n  ".join(card(i, *c, t) for i, c in enumerate(cards))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="376" viewBox="0 0 1200 376" role="img" aria-label="{label}">
  <defs>
    <radialGradient id="glow" cx="0" cy="0" r="1"><stop offset="0" stop-color="#FF5F2E" stop-opacity="{t["glow_o"]}"/><stop offset="1" stop-color="#FF5F2E" stop-opacity="0"/></radialGradient>
  </defs>
  <g font-family="{SANS}">
  {body}
  </g>
</svg>
'''


for name, cards in PACKAGES.items():
    for mode in ("dark", "light"):
        with open(f"{OUT}/features-{name}-{mode}.svg", "w") as f:
            f.write(build(cards, mode))
print("ok")
