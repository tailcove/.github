#!/usr/bin/env python3
"""Generate the per-package hero banners (dark + light) for the Tailcove READMEs.

Each hero carries the package's live stats (version, release date, size, ...) read from the
registries, so re-run this after every release (needs network). The round icon buttons are visual
only; the READMEs repeat them as text links.

Usage: python3 tools/banners/make_heroes.py <out-dir>
       HERO_ONLY=agent python3 tools/banners/make_heroes.py <out-dir>   (the agent hero; reads only its GitHub release)
"""
import os
import sys
from html import escape

import herolib as hl

OUT = sys.argv[1]
ONLY = os.environ.get("HERO_ONLY") or None
CELLS = hl.package_cells(only=ONLY)
H = hl.HERO_H

SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg="#0B0D14", grid="#FFFFFF", grid_o="0.035", g1="#FF5F2E", g1_o="0.30", g2="#6D6AFF", g2_o="0.26",
        ring_a="#FFB199", ring_b="#8B8CFF", word_a="#FFFFFF", word_b="#FFD2C2",
        head="#F4F5F8", sub="#9399A8", pill_fill="#FF5F2E", pill_o="0.12", pill_stroke="#FF5F2E", pill_so="0.45",
        pill_text="#FFB199", cmd_fill="#FFFFFF", cmd_o="0.05", cmd_stroke="#FFFFFF", cmd_so="0.14",
        cmd_text="#E4E6EE", cmd_prompt="#FFB199",
        card="#10121B", card_bar="#FFFFFF", card_bar_o="0.03", card_line="#FFFFFF", card_line_o="0.07",
        card_title="#6C7283", foot="#6C7283",
        plain="#C9CCD6", kw="#B4B5FF", st="#FFB199", num="#FBBF24", cm="#6C7283", fn="#E4E6EE", prop="#C9CCD6",
    ),
    "light": dict(
        bg="#FAFAF7", grid="#000000", grid_o="0.045", g1="#FF5F2E", g1_o="0.22", g2="#6D6AFF", g2_o="0.14",
        ring_a="#C7340F", ring_b="#6D6AFF", word_a="#0A0A0A", word_b="#7A1F08",
        head="#0A0A0A", sub="#5C5C58", pill_fill="#C7340F", pill_o="0.08", pill_stroke="#C7340F", pill_so="0.40",
        pill_text="#C7340F", cmd_fill="#0A0A0A", cmd_o="0.04", cmd_stroke="#0A0A0A", cmd_so="0.16",
        cmd_text="#1F1F1D", cmd_prompt="#C7340F",
        card="#FFFFFF", card_bar="#000000", card_bar_o="0.03", card_line="#000000", card_line_o="0.08",
        card_title="#8A8A85", foot="#6B6B66",
        plain="#2A2A28", kw="#5450E6", st="#C7340F", num="#B45309", cm="#8A8A85", fn="#111111", prop="#3F3F3C",
    ),
}

# Each code line is a list of (text, token-class). Classes: p plain, kw, st, num, cm, fn, prop.
PACKAGES = {
    "node": dict(
        pkg="@tailcove/node", title="log.ts", label="Node.js",
        h1="Node.js logs,", h2="in two lines", sub="Batched · non-blocking · never throws into your app.",
        cmd="npm install @tailcove/node",
        code=[
            [("import", "kw"), (" { Tailcove } ", "p"), ("from", "kw"), (" '@tailcove/node'", "st"), (";", "p")],
            [],
            [("const", "kw"), (" log = ", "p"), ("new", "kw"), (" ", "p"), ("Tailcove", "fn"), ("({", "p")],
            [("  token: process.env.", "p"), ("TAILCOVE_TOKEN", "prop"), (",", "p")],
            [("});", "p")],
            [],
            [("log.", "p"), ("info", "fn"), ("(", "p"), ("'user signed up'", "st"), (", { userId: ", "p"), ("42", "num"), (" });", "p")],
            [("log.", "p"), ("error", "fn"), ("(", "p"), ("'payment failed'", "st"), (", { orderId: ", "p"), ("99", "num"), (" });", "p")],
        ],
        foot="Pino · Winston · ESM + CJS · TypeScript types included",
    ),
    "browser": dict(
        pkg="@tailcove/browser", title="main.ts", label="Browser",
        h1="Frontend errors,", h2="next to your backend", sub="Reliable on page close · opt-in auto-capture · tiny.",
        cmd="npm install @tailcove/browser",
        code=[
            [("import", "kw"), (" { init } ", "p"), ("from", "kw"), (" '@tailcove/browser'", "st"), (";", "p")],
            [],
            [("const", "kw"), (" log = ", "p"), ("init", "fn"), ("({", "p")],
            [("  key: ", "p"), ("'your-browser-key'", "st"), (",", "p")],
            [("  captureWindowErrors: ", "p"), ("true", "kw"), (",", "p")],
            [("  captureUnhandledRejections: ", "p"), ("true", "kw"), (",", "p")],
            [("});", "p")],
            [],
            [("log.", "p"), ("error", "fn"), ("(", "p"), ("'checkout failed'", "st"), (", { orderId: ", "p"), ("99", "num"), (" });", "p")],
        ],
        foot="React · Vue · Svelte · Next.js · plain <script> tag",
    ),
    "python": dict(
        pkg="tailcove", title="app.py", label="Python",
        h1="Python logs,", h2="with plain logging", sub="Standard library only · background thread · never raises.",
        cmd="pip install tailcove",
        code=[
            [("import", "kw"), (" logging", "p")],
            [("from", "kw"), (" tailcove ", "p"), ("import", "kw"), (" TailcoveHandler", "fn")],
            [],
            [("log = logging.", "p"), ("getLogger", "fn"), ("(", "p"), ('"myapp"', "st"), (")", "p")],
            [("log.", "p"), ("addHandler", "fn"), ("(", "p"), ("TailcoveHandler", "fn"), ("(token=TOKEN))", "p")],
            [],
            [("log.", "p"), ("info", "fn"), ("(", "p"), ('"user signed up"', "st"), (",", "p")],
            [("         extra={", "p"), ('"user_id"', "st"), (": ", "p"), ("42", "num"), ("})", "p")],
            [("log.", "p"), ("error", "fn"), ("(", "p"), ('"payment failed"', "st"), (", exc_info=", "p"), ("True", "kw"), (")", "p")],
        ],
        foot="Django · Flask · structured exceptions · zero dependencies",
    ),
    "laravel": dict(
        pkg="tailcove/laravel", title=".env  +  app code", label="Laravel",
        h1="Laravel logs,", h2="one composer require", sub="Sent after the response · never slows a request down.",
        cmd="composer require tailcove/laravel",
        code=[
            [("# .env", "cm")],
            [("TAILCOVE_TOKEN", "prop"), ("=", "p"), ("your-source-token", "st")],
            [("LOG_STACK", "prop"), ("=", "p"), ("single,tailcove", "st")],
            [],
            [("// anywhere in your app", "cm")],
            [("Log", "fn"), ("::", "p"), ("info", "fn"), ("(", "p"), ("'user signed up'", "st"), (");", "p")],
            [("Log", "fn"), ("::", "p"), ("error", "fn"), ("(", "p"), ("'payment failed'", "st"), (", [", "p"), ("'order_id'", "st"), (" => ", "p"), ("99", "num"), ("]);", "p")],
            [("report", "fn"), ("($exception);", "p")],
        ],
        foot="Slow queries · failed jobs · scheduler failures · queue mode",
    ),
}

PACKAGES["agent"] = dict(
    pkg="tailcove-agent", title="tailcove-agent.json", label="the agent",
    h1="One agent,", h2="logs and host metrics", sub="One static binary · follows your files · no dependencies.",
    cmd="curl -fsSL .../install.sh | sh",
    code=[
        [("{", "p")],
        [('  "token"', "prop"), (": ", "p"), ('"your-source-token"', "st"), (",", "p")],
        [('  "logs"', "prop"), (": [", "p")],
        [("    { ", "p"), ('"path"', "prop"), (": ", "p"), ('"/var/log/nginx/*.log"', "st"), (" }", "p")],
        [("  ],", "p")],
        [('  "metrics"', "prop"), (": { ", "p"), ('"enabled"', "prop"), (": ", "p"), ("true", "kw"), (" }", "p")],
        [("}", "p")],
    ],
    foot="systemd · Docker · rotation-safe · restarts without repeats",
)

PACKAGES["terraform"] = dict(
    pkg="terraform-provider-tailcove", title="main.tf", label="Terraform",
    h1="Tailcove,", h2="as code", sub="Sources, monitors and alerts · plan before you change anything.",
    cmd="terraform init",
    code=[
        [("provider", "kw"), (" ", "p"), ('"tailcove"', "st"), (" {}", "p")],
        [("resource", "kw"), (" ", "p"), ('"tailcove_source"', "st"), (" ", "p"), ('"web"', "st"), (" {", "p")],
        [("  name", "prop"), (" = ", "p"), ('"web"', "st")],
        [("}", "p")],
        [],
        [("resource", "kw"), (" ", "p"), ('"tailcove_monitor"', "st"), (" ", "p"), ('"site"', "st"), (" {", "p")],
        [("  url", "prop"), (" = ", "p"), ('"https://example.com"', "st")],
        [("}", "p")],
    ],
    foot="Write-only secrets · safe retries · import",
)

CHAR_W = 7.9  # monospace advance at 13px


def code_lines(lines, t, x, y0, step=25):
    out = []
    for i, line in enumerate(lines):
        if not line:
            continue
        y = y0 + i * step
        spans = "".join(
            f'<tspan fill="{t["plain" if cls == "p" else cls]}">{escape(txt)}</tspan>' for txt, cls in line
        )
        out.append(f'<text x="{x}" y="{y}" xml:space="preserve">{spans}</text>')
    return "\n      ".join(out)


def build(name, p, mode):
    t = THEMES[mode]
    cmd_w = int(len(p["cmd"]) * 9.1 + 60)
    pill_label = p["pkg"]
    pill_w = int(len(pill_label) * 7.3 + 30)
    n = len(p["code"])
    card_h = 38 + 24 + n * 25 + 30
    card_y = 210 - card_h // 2 + 0
    card_y = max(48, card_y)
    cy = card_y + card_h + 28  # centre line of the buttons / footnote row under the card
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{H}" viewBox="0 0 1200 {H}" role="img" aria-label="Tailcove for {p["label"]}: {p["h1"]} {p["h2"]}">
  <defs>
    <radialGradient id="g1" cx="0.16" cy="0.3" r="0.6"><stop offset="0" stop-color="{t["g1"]}" stop-opacity="{t["g1_o"]}"/><stop offset="1" stop-color="{t["g1"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="0.88" cy="0.92" r="0.55"><stop offset="0" stop-color="{t["g2"]}" stop-opacity="{t["g2_o"]}"/><stop offset="1" stop-color="{t["g2"]}" stop-opacity="0"/></radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["ring_a"]}"/><stop offset="0.5" stop-color="{t["ring_a"]}" stop-opacity="0.15"/><stop offset="1" stop-color="{t["ring_b"]}"/></linearGradient>
    <linearGradient id="word" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["word_a"]}"/><stop offset="1" stop-color="{t["word_b"]}"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}"/></pattern>
    <clipPath id="hclip"><rect width="1200" height="{H}" rx="20"/></clipPath>
    <clipPath id="card"><rect x="640" y="{card_y}" width="500" height="{card_h}" rx="14"/></clipPath>
  </defs>

  <g clip-path="url(#hclip)">
  <rect width="1200" height="{H}" fill="{t["bg"]}"/>
  <rect width="1200" height="{H}" fill="url(#grid)"/>
  <rect width="1200" height="{H}" fill="url(#g1)"/>
  <rect width="1200" height="{H}" fill="url(#g2)"/>

  <!-- mark + wordmark + package pill -->
  <g transform="translate(72 64)">
    <linearGradient id="tcTile1" x1="0" y1="0" x2="44.0" y2="44.0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FF8A5C"/><stop offset="0.55" stop-color="#FF5F2E"/><stop offset="1" stop-color="#D63A12"/></linearGradient><rect width="44.0" height="44.0" rx="11" fill="url(#tcTile1)"/><g transform="scale(1.375) translate(6 6) scale(0.8333)" fill="#FFFFFF"><rect x="3.5" y="5" width="11" height="4" rx="2"/><rect x="16.5" y="5" width="4" height="4" rx="1.2"/><path d="M7 7v8c0 2.2 1.8 4 4 4h4.5a2 2 0 0 0 0-4h-3.9a.6.6 0 0 1-.6-.6V7Z"/></g>
    <text x="58" y="33" font-family="{SANS}" font-size="30" font-weight="700" letter-spacing="-1" fill="url(#word)">tailcove</text>
  </g>
  <g font-family="{MONO}" font-size="12.5" font-weight="500">
    <rect x="252" y="73" width="{pill_w}" height="26" rx="13" fill="{t["pill_fill"]}" fill-opacity="{t["pill_o"]}" stroke="{t["pill_stroke"]}" stroke-opacity="{t["pill_so"]}"/>
    <text x="{252 + pill_w // 2}" y="90.5" text-anchor="middle" fill="{t["pill_text"]}">{escape(pill_label)}</text>
  </g>

  <!-- headline -->
  <g font-family="{SANS}">
    <text x="72" y="198" font-size="48" font-weight="700" letter-spacing="-1.4" fill="{t["head"]}">{escape(p["h1"])}</text>
    <text x="72" y="254" font-size="48" font-weight="700" letter-spacing="-1.4" fill="url(#word)">{escape(p["h2"])}</text>
    <text x="72" y="294" font-size="16" fill="{t["sub"]}">{escape(p["sub"])}</text>
  </g>

  <!-- install command -->
  <g font-family="{MONO}" font-size="15" font-weight="500">
    <rect x="72" y="326" width="{cmd_w}" height="40" rx="10" fill="{t["cmd_fill"]}" fill-opacity="{t["cmd_o"]}" stroke="{t["cmd_stroke"]}" stroke-opacity="{t["cmd_so"]}"/>
    <text x="92" y="351" fill="{t["cmd_prompt"]}">$</text>
    <text x="110" y="351" fill="{t["cmd_text"]}">{escape(p["cmd"])}</text>
  </g>

  <!-- code card -->
  <rect x="639" y="{card_y - 1}" width="502" height="{card_h + 2}" rx="15" fill="url(#ring)"/>
  <rect x="640" y="{card_y}" width="500" height="{card_h}" rx="14" fill="{t["card"]}"/>
  <g clip-path="url(#card)">
    <rect x="640" y="{card_y}" width="500" height="38" fill="{t["card_bar"]}" fill-opacity="{t["card_bar_o"]}"/>
    <line x1="640" y1="{card_y + 38.5}" x2="1140" y2="{card_y + 38.5}" stroke="{t["card_line"]}" stroke-opacity="{t["card_line_o"]}"/>
    <circle cx="662" cy="{card_y + 19}" r="5" fill="#FF5F57"/><circle cx="680" cy="{card_y + 19}" r="5" fill="#FEBC2E"/><circle cx="698" cy="{card_y + 19}" r="5" fill="#28C840"/>
    <text x="890" y="{card_y + 24}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["card_title"]}">{escape(p["title"])}</text>
    <g font-family="{MONO}" font-size="13">
      {code_lines(p["code"], t, 664, card_y + 38 + 34)}
    </g>
  </g>

  <!-- round icon buttons (left) and footnote (right) under the card -->
  <g>
    {hl.round_buttons([("book", False), ("arrow", True), ("box", False), ("bug", False)], mode, 640, cy)}
    {hl.footnote(p["foot"], cy, mode)}
  </g>

  <!-- live stats -->
  <g>
    {hl.stats_panel(CELLS[name], mode)}
  </g>
  </g>
  <rect x="0.5" y="0.5" width="1199" height="{H - 1}" rx="19.5" fill="none" stroke="{t["grid"]}" stroke-opacity="0.12"/>
</svg>
'''


for name, p in PACKAGES.items():
    if ONLY and name != ONLY:
        continue

    for mode in ("dark", "light"):
        with open(f"{OUT}/{name}-{mode}.svg", "w") as f:
            f.write(build(name, p, mode))
print("ok")
