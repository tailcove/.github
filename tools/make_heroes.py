#!/usr/bin/env python3
"""Generate the per-package hero banners (dark + light) for the Tailcove READMEs."""
import sys
from html import escape

OUT = sys.argv[1]

SANS = "ui-sans-serif, -apple-system, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg="#0A0A0A", grid="#FFFFFF", grid_o="0.035", g1="#2DD4BF", g1_o="0.30", g2="#6366F1", g2_o="0.26",
        ring_a="#5EEAD4", ring_b="#818CF8", word_a="#FFFFFF", word_b="#C7FFF3",
        head="#EDEDEC", sub="#9A9A96", pill_fill="#2DD4BF", pill_o="0.12", pill_stroke="#2DD4BF", pill_so="0.45",
        pill_text="#5EEAD4", cmd_fill="#FFFFFF", cmd_o="0.05", cmd_stroke="#FFFFFF", cmd_so="0.14",
        cmd_text="#E6E6E2", cmd_prompt="#5EEAD4",
        card="#0F1413", card_bar="#FFFFFF", card_bar_o="0.03", card_line="#FFFFFF", card_line_o="0.07",
        card_title="#7C8785", foot="#7C8785",
        plain="#D4D4D0", kw="#A5B4FC", st="#5EEAD4", num="#FBBF24", cm="#6B7472", fn="#E5E7EB", prop="#C9D1CE",
    ),
    "light": dict(
        bg="#FAFAF7", grid="#000000", grid_o="0.045", g1="#2DD4BF", g1_o="0.22", g2="#6366F1", g2_o="0.14",
        ring_a="#0F766E", ring_b="#6366F1", word_a="#0A0A0A", word_b="#134E4A",
        head="#0A0A0A", sub="#5C5C58", pill_fill="#0F766E", pill_o="0.08", pill_stroke="#0F766E", pill_so="0.40",
        pill_text="#0F766E", cmd_fill="#0A0A0A", cmd_o="0.04", cmd_stroke="#0A0A0A", cmd_so="0.16",
        cmd_text="#1F1F1D", cmd_prompt="#0F766E",
        card="#FFFFFF", card_bar="#000000", card_bar_o="0.03", card_line="#000000", card_line_o="0.08",
        card_title="#8A8A85", foot="#6B6B66",
        plain="#2A2A28", kw="#4F46E5", st="#0F766E", num="#B45309", cm="#8A8A85", fn="#111111", prop="#3F3F3C",
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-label="Tailcove for {p["label"]}: {p["h1"]} {p["h2"]}">
  <defs>
    <radialGradient id="g1" cx="0.16" cy="0.3" r="0.6"><stop offset="0" stop-color="{t["g1"]}" stop-opacity="{t["g1_o"]}"/><stop offset="1" stop-color="{t["g1"]}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="0.88" cy="0.92" r="0.55"><stop offset="0" stop-color="{t["g2"]}" stop-opacity="{t["g2_o"]}"/><stop offset="1" stop-color="{t["g2"]}" stop-opacity="0"/></radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["ring_a"]}"/><stop offset="0.5" stop-color="{t["ring_a"]}" stop-opacity="0.15"/><stop offset="1" stop-color="{t["ring_b"]}"/></linearGradient>
    <linearGradient id="word" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["word_a"]}"/><stop offset="1" stop-color="{t["word_b"]}"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t["grid"]}" stroke-opacity="{t["grid_o"]}"/></pattern>
    <clipPath id="card"><rect x="640" y="{card_y}" width="500" height="{card_h}" rx="14"/></clipPath>
  </defs>

  <rect width="1200" height="420" fill="{t["bg"]}"/>
  <rect width="1200" height="420" fill="url(#grid)"/>
  <rect width="1200" height="420" fill="url(#g1)"/>
  <rect width="1200" height="420" fill="url(#g2)"/>

  <!-- mark + wordmark + package pill -->
  <g transform="translate(72 64)">
    <rect width="44" height="44" rx="10" fill="#A6E3D2"/>
    <g fill="#0A0A0A">
      <rect x="9" y="11" width="26" height="6" rx="1.6"/><rect x="19" y="17" width="6" height="19" rx="1.6"/>
      <rect x="9" y="27" width="6" height="9" rx="1.6"/><rect x="29" y="27" width="6" height="9" rx="1.6"/>
    </g>
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

  <text x="1140" y="{max(card_y + card_h + 28, 396)}" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="{t["foot"]}">{escape(p["foot"])}</text>
</svg>
'''


for name, p in PACKAGES.items():
    for mode in ("dark", "light"):
        with open(f"{OUT}/{name}-{mode}.svg", "w") as f:
            f.write(build(name, p, mode))
print("ok")
