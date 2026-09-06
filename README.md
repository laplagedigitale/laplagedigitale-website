# La Plage Digitale — website

The site for La Plage Digitale, a tiers-lieu in Strasbourg. It is a
[Sovrium](https://sovrium.com) app: the whole site — design system, languages,
components, pages and analytics — is declared in YAML, served by a long-running
Sovrium process and deployed to [Scalingo](https://scalingo.com).

## Layout

`app.yaml` is a table of contents. It holds the app's scalars and a `$ref` map;
everything else lives in `config/`, one file per singleton and one per entity.

```text
app.yaml                       # name, version, description + the $ref map
config/
  design.yaml                  # theme tokens and type scale
  languages.yaml               # locales and the $t: translation dictionary
  analytics.yaml
  components/                  # reusable component templates, one per file
    site-header.yaml
    site-footer.yaml
    space-card.yaml
    amenity-item.yaml
  pages/                       # one file per page
    home.yaml
    about.yaml
    contact.yaml
    legal.yaml
    privacy.yaml
```

A partial is the entity unwrapped — `config/pages/about.yaml` starts at
`name: about`, with no `pages:` key and no leading `-`. Adding a page means
writing the file *and* adding its `- $ref:` line to `app.yaml`; nothing scans
the directory, so an unreferenced file is never read. The `$ref` order in
`app.yaml` is the order the pages and components are in.

`$ref`s resolve into one object before validation, so errors still name the
partial they came from:

```text
Unknown property 'noindexx'
  at pages[3].meta  (legal.yaml)
```

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

Scalingo builds with buildpacks, and four files drive it:

| File               | Role                                                             |
| ------------------ | ---------------------------------------------------------------- |
| `.buildpacks`      | Selects the Sovrium buildpack.                                   |
| `.sovrium-version` | Pins the release to download. Bump this file to upgrade.         |
| `Procfile`         | Boots the binary the buildpack installed into `bin/`.            |
| `scalingo.json`    | Declares the environment every instance of this app needs.       |

The buildpack verifies the release checksum before installing it, and a version
that does not exist fails the build rather than deploying something unexpected.

### The environment

`scalingo.json` declares four variables, each for a reason:

- **`SOVRIUM_ENCRYPTION_KEY`** (`generator: secret`) — Sovrium generates its own
  key when none is given, but Scalingo rebuilds the container filesystem on
  every deploy and restart, so a self-generated key would be new each time. The
  session-signing secret derives from it, so there is no `AUTH_SECRET` to set.
- **`BASE_URL`** (`generator: url`) — the public origin, filled in with the
  app's own address. A non-loopback value is also what switches on secure
  cookies and CSRF enforcement.
- **`NODE_ENV=production`** — turns on immutable caching for content-hashed
  assets. Without it every asset is returned `no-store` and the browser
  refetches the whole bundle on each page view.
- **`TRUSTED_PROXY_HOPS=1`** — accounts for Scalingo's router, so rate limits
  count per visitor instead of lumping every request onto the router's address.
  Raise it only if you put your own CDN in front of Scalingo.

`PORT` is injected by Scalingo and read by Sovrium; no wiring needed.

No database add-on is declared: the site is pages only, so nothing needs to
survive a restart and review apps stay cheap. Add a `postgresql` entry to
`addons` if the site ever grows tables, auth, or forms that store submissions.

> [!IMPORTANT]
> **The manifest applies at app *creation*, not on every deploy.** Scalingo
> reads `scalingo.json` when it creates an app — a review app, or a one-click
> deploy — and not on a `git push` to an app that already exists. An app created
> before this file landed still needs its environment set once:
>
> ```bash
> scalingo --app laplagedigitale env-set \
>   SOVRIUM_ENCRYPTION_KEY="$(openssl rand -hex 32)" \
>   BASE_URL=https://laplagedigitale.osc-fr1.scalingo.io \
>   NODE_ENV=production \
>   TRUSTED_PROXY_HOPS=1
> ```
>
> `scalingo env-set` echoes values to your terminal. Generate secrets inline as
> shown rather than pasting them.

### Review apps

Enable review apps on the parent app and each pull request gets its own
instance, configured from `scalingo.json`. A manifest variable **replaces** what
the parent app holds, which is the behaviour you want here: a review app
generates its own encryption key instead of inheriting production's, and its
`BASE_URL` points at itself rather than at the live site.

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
