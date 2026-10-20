<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/hero-light.svg">
  <img alt="Tailcove — log management for developers who ship fast" src="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/hero-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="https://tailcove.dev"><img alt="Website" src="https://img.shields.io/badge/tailcove.dev-0A0A0A?style=for-the-badge&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1NiA1NiI+PHJlY3Qgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiByeD0iMTIiIGZpbGw9IiNBNkUzRDIiLz48ZyBmaWxsPSIjMEEwQTBBIj48cmVjdCB4PSIxMiIgeT0iMTQiIHdpZHRoPSIzMiIgaGVpZ2h0PSI4IiByeD0iMiIvPjxyZWN0IHg9IjI0IiB5PSIyMiIgd2lkdGg9IjgiIGhlaWdodD0iMjQiIHJ4PSIyIi8+PHJlY3QgeD0iMTIiIHk9IjM0IiB3aWR0aD0iOCIgaGVpZ2h0PSIxMiIgcng9IjIiLz48cmVjdCB4PSIzNiIgeT0iMzQiIHdpZHRoPSI4IiBoZWlnaHQ9IjEyIiByeD0iMiIvPjwvZz48L3N2Zz4=&logoColor=white"></a>
  <a href="https://tailcove.dev/docs"><img alt="Docs" src="https://img.shields.io/badge/Docs-2DD4BF?style=for-the-badge&logoColor=0A0A0A"></a>
  <a href="https://tailcove.dev/pricing"><img alt="Pricing" src="https://img.shields.io/badge/Pricing-0A0A0A?style=for-the-badge"></a>
  <a href="https://app.tailcove.dev/register"><img alt="Get started free" src="https://img.shields.io/badge/Get%20started%20free-0A0A0A?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="https://packagist.org/packages/tailcove/laravel"><img alt="Packagist" src="https://img.shields.io/packagist/v/tailcove/laravel?label=tailcove%2Flaravel&color=2DD4BF&labelColor=0A0A0A"></a>
  <a href="https://www.npmjs.com/package/@tailcove/node"><img alt="npm" src="https://img.shields.io/npm/v/@tailcove/node?label=%40tailcove%2Fnode&color=2DD4BF&labelColor=0A0A0A"></a>
  <a href="https://pypi.org/project/tailcove/"><img alt="PyPI" src="https://img.shields.io/pypi/v/tailcove?label=tailcove%20(PyPI)&color=2DD4BF&labelColor=0A0A0A"></a>
  <a href="https://www.npmjs.com/package/@tailcove/browser"><img alt="npm" src="https://img.shields.io/npm/v/@tailcove/browser?label=%40tailcove%2Fbrowser&color=2DD4BF&labelColor=0A0A0A"></a>
</p>

<br>

<h3 align="center">One <code>composer require</code> away from searchable, alertable, grouped logs.</h3>

<p align="center">
  Tailcove is the logging stack for teams that would rather ship than babysit observability.<br>
  Send structured logs from Laravel, Node, Python or the browser; get sub-second search, a live tail,<br>
  exception grouping, alerts and uptime monitoring — metered on gigabytes, not seats.
</p>

<br>

<img alt="How Tailcove works: your apps send logs over HTTP or syslog, Tailcove never slows your app down, and you get search, issues, alerts and uptime" src="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/flow.svg" width="100%">

<br>

## Ship your first log in under a minute

<details open>
<summary><b>Laravel</b> &nbsp;·&nbsp; <code>composer require tailcove/laravel</code></summary>
<br>

```php
// config/logging.php
'channels' => [
    'tailcove' => ['driver' => 'tailcove'],
],
```

```dotenv
TAILCOVE_TOKEN=your-source-token
LOG_STACK=single,tailcove
```

That's it. Every `Log::info()`, exception and `report()` call now lands in Tailcove, enriched with the request ID, authenticated user, environment and host. Flip on the optional listeners to capture slow queries, failed jobs and scheduler failures too.

</details>

<details>
<summary><b>Node.js</b> &nbsp;·&nbsp; <code>npm install @tailcove/node</code></summary>
<br>

```ts
import { Tailcove } from '@tailcove/node';

const log = new Tailcove({ token: process.env.TAILCOVE_TOKEN });

log.info('order placed', { orderId: 1042, total: 49.0 });
```

Already on pino or winston? Use `@tailcove/node/pino` or `@tailcove/node/winston` as a transport and keep your existing loggers.

</details>

<details>
<summary><b>Python</b> &nbsp;·&nbsp; <code>pip install tailcove</code></summary>
<br>

```python
import logging
from tailcove import TailcoveHandler

logging.getLogger().addHandler(TailcoveHandler(token="your-source-token"))
logging.getLogger(__name__).error("card declined", extra={"order_id": 1042})
```

Zero dependencies, standard `logging.Handler`, so Django and Flask need nothing more than a `LOGGING` entry.

</details>

<details>
<summary><b>Browser</b> &nbsp;·&nbsp; <code>npm install @tailcove/browser</code></summary>
<br>

```ts
import { Tailcove } from '@tailcove/browser';

const log = new Tailcove({
  key: 'your-browser-key',
  captureWindowErrors: true,
  captureUnhandledRejections: true,
});
```

Adapters for React, Vue, Svelte and Next.js, plus a drop-in `<script>` build for sites with no build step. Frontend errors are grouped into the same issues as your backend exceptions.

</details>

<details>
<summary><b>Vector · Fluent Bit · rsyslog · syslog-ng</b> &nbsp;·&nbsp; no client needed</summary>
<br>

Point an HTTP sink at `https://ingest.tailcove.dev/api/v1/logs` with a bearer token, or a syslog output at port `6514`. Tailcove understands the field names each shipper emits out of the box, so there's no remap stage to write. See the [sending logs](https://tailcove.dev/docs) guides.

</details>

<br>

## What you get

<table>
  <tr>
    <td width="33%" valign="top">
      <h4>🔎 &nbsp;Search &amp; live tail</h4>
      Sub-second structured search over every field you send. Watch requests stream in live, pause, filter, save the query.
    </td>
    <td width="33%" valign="top">
      <h4>🧩 &nbsp;Issues</h4>
      Exceptions are fingerprinted across all four clients and grouped into one issue with first-seen, last-seen and occurrence counts. One bug, one row.
    </td>
    <td width="33%" valign="top">
      <h4>🔔 &nbsp;Alerts</h4>
      Turn any search into an alert with a threshold. Delivered to email, Slack and webhooks, with durable retries and resolve notifications.
    </td>
  </tr>
  <tr>
    <td valign="top">
      <h4>🟢 &nbsp;Uptime &amp; status pages</h4>
      HTTP monitors with keyword checks and a two-strikes state machine. Publish a public status page in a click.
    </td>
    <td valign="top">
      <h4>📦 &nbsp;Log drains</h4>
      Scheduled exports to any S3-compatible bucket for long-term retention and compliance, per source.
    </td>
    <td valign="top">
      <h4>🏷️ &nbsp;Built for agencies</h4>
      Group sources by client, white-label the UI, hand out read-only API tokens. Run logging for everyone you build for.
    </td>
  </tr>
</table>

<br>

## Repositories

| | Repository | What's inside |
|:--|:--|:--|
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-original.svg" width="20"> | [**laravel**](https://github.com/tailcove/laravel) | Monolog handler, service provider, context processor and optional slow-query / failed-job / scheduler listeners |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" width="20"> | [**node**](https://github.com/tailcove/node) | TypeScript client with ESM + CJS builds, pino transport and winston transport |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="20"> | [**python**](https://github.com/tailcove/python) | Stdlib-only `logging.Handler` with a background flusher |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" width="20"> | [**browser**](https://github.com/tailcove/browser) | Browser client with auto-capture, framework adapters and a UMD build |

Every client follows the same contract: batch, never throw, flush on shutdown or page unload, and render exceptions in one shared shape so grouping works regardless of where the error came from.

<br>

## Contributing & security

Issues and pull requests are welcome on each client repository. If you believe you've found a security vulnerability, please email **security@tailcove.dev** instead of opening a public issue.

<br>

<p align="center">
  <sub>Powered by <a href="https://akcybex.com">AKCybex</a> &nbsp;·&nbsp; <a href="https://tailcove.dev">tailcove.dev</a></sub>
</p>
