#!/usr/bin/env python3
"""Rewrite the top and footer of each package README. Everything from '## Install' down is kept."""
import re
import sys

ROOT = sys.argv[1]
RAW = "https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/packages"

PKGS = {
    "node": dict(
        pkg="@tailcove/node", label="Node.js", tagline="Send logs from Node.js to Tailcove in two lines of code.",
        docs="https://tailcove.dev/docs/sending-logs/node",
        badges=[
            ("npm version", "https://img.shields.io/npm/v/@tailcove/node?label=%40tailcove%2Fnode&color=2DD4BF&labelColor=0A0A0A", "https://www.npmjs.com/package/@tailcove/node"),
            ("Node.js 18+", "https://img.shields.io/node/v/@tailcove/node?color=2DD4BF&labelColor=0A0A0A", None),
            ("Types included", "https://img.shields.io/badge/types-included-2DD4BF?labelColor=0A0A0A", None),
            ("MIT license", "https://img.shields.io/badge/license-MIT-2DD4BF?labelColor=0A0A0A", "LICENSE"),
        ],
        cards=[
            ("⚡", "Fast", "Lines are batched, 50 at a time or every 2 seconds. Your code never waits on the network."),
            ("🛡️", "Safe", "A failed delivery is caught and dropped. Logging will never be the reason your app crashes."),
            ("🪶", "Lightweight", "Delivery uses the built-in <code>fetch</code>. Only two tiny helpers for the transports."),
            ("🔌", "Pino &amp; Winston", "Drop in as a transport and keep the logger you already use."),
            ("🏷️", "Context for free", "Hostname, process ID and environment are added to every line automatically."),
            ("🟦", "Typed", "Written in TypeScript, with ESM and CommonJS builds."),
        ],
    ),
    "browser": dict(
        pkg="@tailcove/browser", label="Browser", tagline="Send logs and frontend errors from the browser to Tailcove.",
        docs="https://tailcove.dev/docs/sending-logs/browser",
        badges=[
            ("npm version", "https://img.shields.io/npm/v/@tailcove/browser?label=%40tailcove%2Fbrowser&color=2DD4BF&labelColor=0A0A0A", "https://www.npmjs.com/package/@tailcove/browser"),
            ("Types included", "https://img.shields.io/badge/types-included-2DD4BF?labelColor=0A0A0A", None),
            ("MIT license", "https://img.shields.io/badge/license-MIT-2DD4BF?labelColor=0A0A0A", "LICENSE"),
        ],
        cards=[
            ("🔎", "Catches real errors", "Opt in to uncaught errors, unhandled rejections and <code>console.error</code>, next to your backend logs."),
            ("📮", "Reliable on page close", "Flushes with <code>sendBeacon</code> when a tab is hidden or closed, so the last log isn't lost."),
            ("🛡️", "Safe", "A failed delivery is caught and dropped. Logging will never break your page."),
            ("🧱", "Any framework", "React, Vue, Svelte and Next.js helpers, or a plain <code>&lt;script&gt;</code> tag."),
            ("🧩", "One shared issue", "A browser error groups with the matching server error, because both use the same shape."),
            ("🔑", "Public by design", "A browser key is meant to ship in your front-end. Allowed origins control access."),
        ],
    ),
    "python": dict(
        pkg="tailcove", label="Python", tagline="Send Python logs to Tailcove with the standard logging module.",
        docs="https://tailcove.dev/docs/sending-logs/python",
        badges=[
            ("PyPI version", "https://img.shields.io/pypi/v/tailcove?color=2DD4BF&labelColor=0A0A0A", "https://pypi.org/project/tailcove/"),
            ("Python versions", "https://img.shields.io/pypi/pyversions/tailcove?color=2DD4BF&labelColor=0A0A0A", "https://pypi.org/project/tailcove/"),
            ("MIT license", "https://img.shields.io/badge/license-MIT-2DD4BF?labelColor=0A0A0A", "LICENSE"),
        ],
        cards=[
            ("🐍", "Plain <code>logging</code>", "<code>TailcoveHandler</code> is a normal <code>logging.Handler</code>. Keep the loggers you have."),
            ("🧵", "Never blocks", "Records are batched and sent from a background thread, so nothing waits on the network."),
            ("📦", "No dependencies", "Delivery uses <code>urllib</code> from the standard library."),
            ("🛡️", "Safe", "A failed delivery is caught and never raised into your code."),
            ("🧩", "Structured exceptions", "Class, message, location and trace arrive as data, so identical errors group together."),
            ("🌐", "Django &amp; Flask", "Copy-paste setup for both, below."),
        ],
    ),
    "laravel": dict(
        pkg="tailcove/laravel", label="Laravel", tagline="Send your Laravel logs to Tailcove with one <code>composer require</code>.",
        docs="https://tailcove.dev/docs/sending-logs/laravel-package",
        badges=[
            ("Packagist version", "https://img.shields.io/packagist/v/tailcove/laravel?color=2DD4BF&labelColor=0A0A0A", "https://packagist.org/packages/tailcove/laravel"),
            ("PHP 8.2+", "https://img.shields.io/packagist/dependency-v/tailcove/laravel/php?color=2DD4BF&labelColor=0A0A0A", None),
            ("Laravel 11, 12, 13", "https://img.shields.io/badge/laravel-11%20%7C%2012%20%7C%2013-2DD4BF?labelColor=0A0A0A", None),
            ("MIT license", "https://img.shields.io/badge/license-MIT-2DD4BF?labelColor=0A0A0A", "LICENSE"),
        ],
        cards=[
            ("🚀", "No added latency", "Logs are sent from a shutdown function, after the response has already gone out."),
            ("🛡️", "Safe", "A failed delivery is caught and written to <code>error_log()</code>. It never fails a request."),
            ("🏷️", "Context for free", "Environment, hostname, signed-in user and a request ID on every line."),
            ("🧩", "Exceptions as data", "<code>report($e)</code> arrives with class, message, location and trace."),
            ("🔧", "Optional extras", "Slow queries, failed jobs and scheduler failures, one setting each."),
            ("📬", "Queue mode", "Prefer the worker? Switch to a queued job with retries."),
        ],
    ),
}


def button(alt, text, href, fill, text_color=None):
    color = f"&logoColor={text_color}" if text_color else ""
    return (
        f'  <a href="{href}"><img alt="{alt}" '
        f'src="https://img.shields.io/badge/{text}-{fill}?style=for-the-badge{color}"></a>'
    )


def cards_table(cards):
    rows = []
    for start in (0, 3):
        cells = []
        for icon, title, body in cards[start:start + 3]:
            cells.append(
                f'    <td width="33%" valign="top">\n'
                f"      <h4>{icon} &nbsp;{title}</h4>\n"
                f"      {body}\n"
                f"    </td>"
            )
        rows.append("  <tr>\n" + "\n".join(cells) + "\n  </tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def top(name, p):
    dark, light = f"{RAW}/{name}-dark.svg", f"{RAW}/{name}-light.svg"
    badge_imgs = []
    for alt, src, href in p["badges"]:
        img = f'<img alt="{alt}" src="{src}">'
        badge_imgs.append(f'  <a href="{href}">{img}</a>' if href else f"  {img}")
    return f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{dark}">
  <source media="(prefers-color-scheme: light)" srcset="{light}">
  <img alt="{p["pkg"]}: Tailcove for {p["label"]}" src="{dark}" width="100%">
</picture>

<p align="center">
  <a href="{p["docs"]}"><img alt="Documentation" src="https://img.shields.io/badge/Documentation-2DD4BF?style=for-the-badge&logoColor=0A0A0A"></a>
  <a href="https://app.tailcove.dev/register"><img alt="Get started free" src="https://img.shields.io/badge/Get%20started%20free-0A0A0A?style=for-the-badge"></a>
  <a href="https://github.com/tailcove/{name}/issues/new/choose"><img alt="Report a bug" src="https://img.shields.io/badge/Report%20a%20bug-0A0A0A?style=for-the-badge"></a>
</p>

<p align="center">
{chr(10).join(badge_imgs)}
</p>

<br>

<h3 align="center">{p["tagline"]}</h3>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{RAW}/features-{name}-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="{RAW}/features-{name}-light.svg">
  <img alt="{p["pkg"]} features" src="{RAW}/features-{name}-dark.svg" width="100%">
</picture>

<br>

'''


LIBS = {
    "laravel": ("Laravel", "https://github.com/tailcove/laravel"),
    "node": ("Node.js", "https://github.com/tailcove/node"),
    "python": ("Python", "https://github.com/tailcove/python"),
    "browser": ("Browser", "https://github.com/tailcove/browser"),
}


def footer(name, p):
    others = " &nbsp;·&nbsp; ".join(f'<a href="{u}">{l}</a>' for k, (l, u) in LIBS.items() if k != name)
    return f'''<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{RAW}/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="{RAW}/footer-light.svg">
  <img alt="Tailcove. Built by AKCybex." src="{RAW}/footer-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="{p["docs"]}">Documentation</a> &nbsp;·&nbsp;
  <a href="https://app.tailcove.dev/register">Get started free</a> &nbsp;·&nbsp;
  <a href="https://github.com/tailcove/{name}/issues/new/choose">Report a bug</a> &nbsp;·&nbsp;
  <a href="LICENSE">MIT License</a>
</p>

<p align="center">
  <sub>More Tailcove libraries: {others}</sub>
</p>
'''


for name, p in PKGS.items():
    path = f"{ROOT}/{name}/README.md"
    s = open(path).read()
    idx = s.index("\n## Install")
    body = s[idx + 1:]
    li = body.index("## Other Tailcove libraries")
    body = body[:li].rstrip() + "\n\n" + footer(name, p)
    open(path, "w").write(top(name, p) + body)
    print("wrote", path, f"({len(top(name, p) + body)} chars)")
