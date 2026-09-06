# La Plage Digitale — website

The site for La Plage Digitale, a tiers-lieu in Strasbourg. It is a
[Sovrium](https://sovrium.com) app: the whole site — design system, languages,
pages and analytics — is declared in `app.yaml`, served by a long-running
Sovrium process and deployed to [Scalingo](https://scalingo.com).

## Setup

Sovrium ships as a self-contained binary. There is no runtime and no package
manager to install first, and the project has no dependencies.

```bash
curl -fsSL https://sovrium.com/install | sh
```

## Commands

```bash
sovrium start app.yaml --watch   # dev server on http://localhost:3000
sovrium validate app.yaml        # check app.yaml against the schema
```

Run `sovrium validate app.yaml` before every commit. Since v0.22.0 an
unrecognised property fails the config rather than being ignored, so the
validator names anything that no longer exists.

## Deployment

Scalingo builds with buildpacks, and three files drive it:

| File               | Role                                                             |
| ------------------ | ---------------------------------------------------------------- |
| `.buildpacks`      | Selects the Sovrium buildpack.                                   |
| `.sovrium-version` | Pins the release to download. Bump this file to upgrade.         |
| `Procfile`         | Boots the binary the buildpack installed into `bin/`.            |

The buildpack verifies the release checksum before installing it, and a version
that does not exist fails the build rather than deploying something unexpected.

### First-time setup

```bash
scalingo --app laplagedigitale env-set \
  SOVRIUM_ENCRYPTION_KEY="$(openssl rand -hex 32)" \
  BASE_URL=https://laplagedigitale.osc-fr1.scalingo.io \
  NODE_ENV=production \
  TRUSTED_PROXY_HOPS=1
```

Four variables, each for a reason:

- **`SOVRIUM_ENCRYPTION_KEY`** — Sovrium generates its own key when none is
  given, but Scalingo rebuilds the container filesystem on every deploy and
  restart, so a generated key would be new each time. Set it once. The
  session-signing secret derives from it, so there is no `AUTH_SECRET` to set.
- **`BASE_URL`** — the public origin. A non-loopback value is also what switches
  on secure cookies and CSRF enforcement. Update it once a custom domain is
  attached.
- **`NODE_ENV=production`** — turns on immutable caching for content-hashed
  assets. Without it every asset is returned `no-store` and the browser refetches
  the whole bundle on each page view.
- **`TRUSTED_PROXY_HOPS=1`** — accounts for Scalingo's router, so rate limits
  count per visitor instead of lumping every request onto the router's address.
  Raise it only if you put your own CDN in front of Scalingo.

`PORT` is injected by Scalingo and read by Sovrium; no wiring needed.

No database add-on is required: the site is pages only, so nothing needs to
survive a restart. Add managed PostgreSQL and let Scalingo inject `DATABASE_URL`
if the site ever grows tables, auth or forms that store submissions.

:::note
`scalingo env-set` echoes values to your terminal. Generate secrets inline as
shown rather than pasting them.
:::

### Deploy

Scalingo deploys from `master`, while this repository's default branch is
`main` — push explicitly:

```bash
git push scalingo HEAD:refs/heads/master
```

Then check it is up:

```bash
curl -fsS https://laplagedigitale.osc-fr1.scalingo.io/ >/dev/null && echo "up"
```
