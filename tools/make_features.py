#!/usr/bin/env python3
"""Generate feature-card banners and the shared footer banner (dark + light)."""
import re
import sys
import textwrap
from html import escape, unescape

OUT = sys.argv[1]
SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

T = {
    "dark": dict(card="#0F1413", border="#FFFFFF", border_o="0.09", title="#EDEDEC", body="#9A9A96",
                 accent="#5EEAD4", tile="#2DD4BF", tile_o="0.12", tile_s="#2DD4BF", tile_so="0.30",
                 g1="#2DD4BF", g1_o="0.10", foot_bg="#0F1413", word_a="#FFFFFF", word_b="#C7FFF3", muted="#7C8785"),
    "light": dict(card="#FFFFFF", border="#000000", border_o="0.10", title="#0A0A0A", body="#5C5C58",
                  accent="#0F766E", tile="#0F766E", tile_o="0.08", tile_s="#0F766E", tile_so="0.28",
                  g1="#2DD4BF", g1_o="0.14", foot_bg="#FFFFFF", word_a="#0A0A0A", word_b="#134E4A", muted="#6B6B66"),
}

# 24x24 stroke icons
ICONS = {
    "bolt": '<path d="M13 2 4 14h7l-1 8 10-13h-7z"/>',
    "shield": '<path d="M12 2l8 3v6c0 5.5-3.5 9.5-8 11-4.5-1.5-8-5.5-8-11V5z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "plug": '<path d="M9 2v5M15 2v5"/><path d="M6 7h12v5a6 6 0 0 1-12 0z"/><path d="M12 18v4"/>',
    "tag": '<path d="M3 12V4h8l10 10-7 7z"/><circle cx="7.5" cy="8.5" r="1.2"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "link": '<circle cx="9" cy="12" r="5"/><circle cx="15" cy="12" r="5"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-8M17 7l2 2"/>',
    "layers": '<path d="m12 2 10 6-10 6L2 8z"/><path d="m2 12 10 6 10-6"/>',
    "thread": '<path d="M3 12c3-6 6-6 9 0s6 6 9 0"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="m3 7 9 4 9-4M12 11v10"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-4 5-4 13 0 18M12 3c4 5 4 13 0 18"/>',
    "terminal": '<path d="m4 17 6-5-6-5M12 19h8"/>',
    "sliders": '<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="9" cy="6" r="2"/><circle cx="15" cy="12" r="2"/><circle cx="8" cy="18" r="2"/>',
    "bell": '<path d="M6 9a6 6 0 0 1 12 0c0 6 3 7 3 8H3c0-1 3-2 3-8z"/><path d="M10 21h4"/>',
    "pulse": '<path d="M3 12h5l2-6 4 12 2-6h5"/>',
}


def strip(html):
    return unescape(re.sub(r"<[^>]+>", "", html))


def icon_svg(spec, t, x, y):
    tile = (f'<rect x="{x}" y="{y}" width="44" height="44" rx="11" fill="{t["tile"]}" fill-opacity="{t["tile_o"]}" '
            f'stroke="{t["tile_s"]}" stroke-opacity="{t["tile_so"]}"/>')
    if isinstance(spec, tuple):
        label = escape(spec[1])
        return tile + (f'<text x="{x + 22}" y="{y + 28}" text-anchor="middle" font-family="{MONO}" font-size="15" '
                       f'font-weight="700" fill="{t["accent"]}">{label}</text>')
    return tile + (f'<g transform="translate({x + 10} {y + 10}) scale(1)" fill="none" stroke="{t["accent"]}" '
                   f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
                   f'transform-origin="0 0">{ICONS[spec]}</g>')


def features(name, cards, mode):
    t = T[mode]
    W, CW, CH, GX, GY = 1200, 376, 176, 36, 24
    H = 2 * CH + GY
    parts = []
    for i, (icon, title, body) in enumerate(cards):
        col, row = i % 3, i // 3
        x, y = col * (CW + GX), row * (CH + GY)
        lines = textwrap.wrap(strip(body), width=43)[:3]
        desc = "".join(
            f'<text x="{x + 28}" y="{y + 106 + k * 22}" font-size="14.5" fill="{t["body"]}">{escape(l)}</text>'
            for k, l in enumerate(lines)
        )
        parts.append(
            f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{CW - 1}" height="{CH - 1}" rx="16" fill="{t["card"]}" '
            f'stroke="{t["border"]}" stroke-opacity="{t["border_o"]}"/>'
            f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{CW - 1}" height="{CH - 1}" rx="16" fill="url(#glow)"/>'
            + icon_svg(icon, t, x + 28, y + 26)
            + f'<text x="{x + 88}" y="{y + 56}" font-size="19" font-weight="650" letter-spacing="-0.3" fill="{t["title"]}">{escape(strip(title))}</text>'
            + desc
        )
    alt = "; ".join(f"{strip(c[1])}: {strip(c[2])}" for c in cards)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(alt, quote=True)}">
  <defs>
    <radialGradient id="glow" cx="0" cy="0" r="1"><stop offset="0" stop-color="{t["g1"]}" stop-opacity="{t["g1_o"]}"/><stop offset="1" stop-color="{t["g1"]}" stop-opacity="0"/></radialGradient>
  </defs>
  <g font-family="{SANS}">
  {chr(10).join("  " + p for p in parts)}
  </g>
</svg>
'''


def footer(mode):
    t = T[mode]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="112" viewBox="0 0 1200 112" role="img" aria-label="Tailcove. Built by AKCybex. MIT licensed.">
  <defs>
    <linearGradient id="word" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["word_a"]}"/><stop offset="1" stop-color="{t["word_b"]}"/></linearGradient>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2DD4BF" stop-opacity="0"/><stop offset="0.5" stop-color="#2DD4BF" stop-opacity="0.85"/><stop offset="1" stop-color="#6366F1" stop-opacity="0"/></linearGradient>
    <radialGradient id="glow" cx="0.1" cy="0.5" r="0.7"><stop offset="0" stop-color="{t["g1"]}" stop-opacity="{t["g1_o"]}"/><stop offset="1" stop-color="{t["g1"]}" stop-opacity="0"/></radialGradient>
  </defs>
  <rect x="0.5" y="12.5" width="1199" height="99" rx="18" fill="{t["foot_bg"]}" stroke="{t["border"]}" stroke-opacity="{t["border_o"]}"/>
  <rect x="0.5" y="12.5" width="1199" height="99" rx="18" fill="url(#glow)"/>
  <rect x="60" y="11" width="1080" height="2" rx="1" fill="url(#line)"/>
  <g transform="translate(36 38)">
    <rect width="48" height="48" rx="11" fill="#A6E3D2"/>
    <g fill="#0A0A0A"><rect x="10" y="12" width="28" height="7" rx="1.8"/><rect x="20.5" y="19" width="7" height="21" rx="1.8"/><rect x="10" y="30" width="7" height="10" rx="1.8"/><rect x="31" y="30" width="7" height="10" rx="1.8"/></g>
  </g>
  <g font-family="{SANS}">
    <text x="102" y="60" font-size="26" font-weight="700" letter-spacing="-0.9" fill="url(#word)">tailcove</text>
    <text x="102" y="82" font-size="13.5" fill="{t["muted"]}">Log management for developers who ship fast.</text>
    <text x="1164" y="60" text-anchor="end" font-size="20" font-weight="600" letter-spacing="-0.3" fill="{t["title"]}">Built by AKCybex</text>
    <text x="1164" y="82" text-anchor="end" font-size="13.5" fill="{t["muted"]}">MIT licensed · tailcove.dev</text>
  </g>
</svg>
'''


PACKAGES = {
    "node": [("bolt", "Fast", "Lines are batched, 50 at a time or every 2 seconds. Your code never waits on the network."),
             ("shield", "Safe", "A failed delivery is caught and dropped. Logging will never be the reason your app crashes."),
             ("chip", "Lightweight", "Delivery uses the built-in fetch. Only two tiny helpers for the transports."),
             ("plug", "Pino and Winston", "Drop in as a transport and keep the logger you already use."),
             ("tag", "Context for free", "Hostname, process ID and environment are added to every line automatically."),
             (("text", "TS"), "Typed", "Written in TypeScript, with ESM and CommonJS builds.")],
    "browser": [("search", "Catches real errors", "Opt in to uncaught errors, unhandled rejections and console.error, next to your backend logs."),
                ("mail", "Reliable on page close", "Flushes with sendBeacon when a tab is hidden or closed, so the last log isn't lost."),
                ("shield", "Safe", "A failed delivery is caught and dropped. Logging will never break your page."),
                ("layers", "Any framework", "React, Vue, Svelte and Next.js helpers, or a plain script tag."),
                ("link", "One shared issue", "A browser error groups with the matching server error, because both use the same shape."),
                ("key", "Public by design", "A browser key is meant to ship in your front-end. Allowed origins control access.")],
    "python": [("terminal", "Plain logging", "TailcoveHandler is a normal logging.Handler. Keep the loggers you have."),
               ("thread", "Never blocks", "Records are batched and sent from a background thread, so nothing waits on the network."),
               ("box", "No dependencies", "Delivery uses urllib from the standard library."),
               ("shield", "Safe", "A failed delivery is caught and never raised into your code."),
               (("text", "{ }"), "Structured exceptions", "Class, message, location and trace arrive as data, so identical errors group together."),
               ("globe", "Django and Flask", "Copy-paste setup for both, below.")],
    "laravel": [("bolt", "No added latency", "Logs are sent from a shutdown function, after the response has already gone out."),
                ("shield", "Safe", "A failed delivery is caught and written to error_log(). It never fails a request."),
                ("tag", "Context for free", "Environment, hostname, signed-in user and a request ID on every line."),
                (("text", "{ }"), "Exceptions as data", "report($e) arrives with class, message, location and trace."),
                ("sliders", "Optional extras", "Slow queries, failed jobs and scheduler failures, one setting each."),
                ("layers", "Queue mode", "Prefer the worker? Switch to a queued job with retries.")],
}
PROFILE = [("search", "Search and live tail", "Sub-second structured search over every field you send. Watch requests stream in live, pause, filter, save the query."),
           ("link", "Issues", "Exceptions are fingerprinted across all four clients and grouped into one issue. One bug, one row."),
           ("bell", "Alerts", "Turn any search into an alert with a threshold. Email, Slack and webhooks, with durable retries."),
           ("pulse", "Uptime and status pages", "HTTP monitors with keyword checks and a two-strikes state machine. Publish a status page in a click."),
           ("box", "Log drains", "Scheduled exports to any S3-compatible bucket for long-term retention, per source."),
           ("layers", "Built for agencies", "Group sources by client, white-label the UI, hand out read-only API tokens.")]

for mode in ("dark", "light"):
    for name, cards in PACKAGES.items():
        open(f"{OUT}/features-{name}-{mode}.svg", "w").write(features(name, cards, mode))
    open(f"{OUT}/features-profile-{mode}.svg", "w").write(features("profile", PROFILE, mode))
    open(f"{OUT}/footer-{mode}.svg", "w").write(footer(mode))
print("ok")
