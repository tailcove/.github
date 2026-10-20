<a href="https://tailcove.dev"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/hero-light.svg">
  <img alt="Tailcove: log management for developers who ship fast. Current versions of the Laravel, Node.js, Python and browser libraries." src="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/hero-dark.svg" width="100%">
</picture></a>

<p align="center">
  <a href="https://tailcove.dev">Website</a> &nbsp;·&nbsp;
  <a href="https://tailcove.dev/docs">Documentation</a> &nbsp;·&nbsp;
  <a href="https://tailcove.dev/pricing">Pricing</a> &nbsp;·&nbsp;
  <a href="https://app.tailcove.dev/register">Get started free</a>
</p>

<h3 align="center">One <code>composer require</code> away from searchable, alertable, grouped logs.</h3>

<p align="center">
  Tailcove is the logging stack for teams that would rather ship than babysit observability.<br>
  Send structured logs from Laravel, Node, Python or the browser; get sub-second search, a live tail,<br>
  exception grouping, alerts and uptime monitoring — metered on gigabytes, not seats.
</p>

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

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/features-profile-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/features-profile-light.svg">
  <img alt="What you get: search and live tail, issues, alerts, uptime and status pages, log drains, and tools for agencies" src="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/features-profile-dark.svg" width="100%">
</picture>

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

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/footer-light.svg">
  <img alt="Tailcove. Built by AKCybex." src="https://raw.githubusercontent.com/tailcove/.github/main/profile/assets/footer-dark.svg" width="100%">
</picture>

<p align="center">
  <a href="https://tailcove.dev">Website</a> &nbsp;·&nbsp;
  <a href="https://tailcove.dev/docs">Documentation</a> &nbsp;·&nbsp;
  <a href="https://tailcove.dev/pricing">Pricing</a> &nbsp;·&nbsp;
  <a href="https://app.tailcove.dev/register">Get started free</a> &nbsp;·&nbsp;
  <a href="https://akcybex.com">AKCybex</a>
</p>
