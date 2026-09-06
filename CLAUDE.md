## Sovrium Documentation

This project uses [Sovrium](https://sovrium.com), a configuration-driven application platform. The entire app is defined in `app.yaml` and uses the Sovrium CLI directly — no TypeScript files.

### LLMs Documentation References

For complete Sovrium documentation, fetch these files:

- **Full reference**: `https://sovrium.com/llms-full.txt` — Complete docs (~45000 lines, EN + FR) covering schema, components, fields, actions, auth, themes, pages, the changelog, and more.
- **JSON Schema**: `https://sovrium.com/schema/app.json` — Machine-readable schema for validation and autocompletion. `sovrium schema` prints the schema the installed binary actually enforces.

When working on `app.yaml` or any Sovrium configuration, **always fetch `https://sovrium.com/llms-full.txt`** to get the latest documentation before making changes, and **always run `sovrium validate app.yaml`** afterwards — since v0.22.0 an unrecognised property fails the config instead of being ignored, so the validator names anything that no longer exists.

### Key Concepts

- **Config-driven**: The entire app (design system, languages, pages, analytics) is defined in a single YAML file (`app.yaml`).
- **Version**: pinned in `.sovrium-version` (currently 0.24.0) — the Scalingo buildpack downloads exactly that release.
- **49 field types**, **90 component types**, built-in auth, RBAC permissions, i18n.
- App is started with `sovrium start app.yaml` (CLI only, no TypeScript needed).

### Project Setup

- **No runtime and no package manager.** Sovrium is a self-contained binary; the project has no dependencies, no `package.json` and no lockfile. Do not add one.
- Install: `curl -fsSL https://sovrium.com/install | sh` (or `brew install sovrium/tap/sovrium`)
- Config: `app.yaml` — single file, all config
- Static assets: `./public` directory, served automatically
- The app is a **long-running server**, not a static build. There is no `sovrium build` step in this project.

### CLI Commands

```bash
sovrium start app.yaml          # Start dev server
sovrium start app.yaml --watch  # Start with hot reload
sovrium validate app.yaml       # Validate config
sovrium schema                  # Print JSON Schema
sovrium design-system           # Export the design system (md or DTCG JSON)
sovrium update                  # Update the binary
```

### Config conventions for this app

- **Components are typed from a closed vocabulary.** Raw HTML tag names (`div`, `p`, `section`, `h2`, …) are not component types. Use `container` with `element: div|section|main|aside|nav|header|footer|article`, and `text` with `element: h1..h6|p|span|label|blockquote|code`.
- `text` renders a `<span>` unless you set `element:` — write `element: p` for real paragraphs.
- Page content lives under `pages[].components` (not `sections`).
- Design tokens live under `design.theme`. The top-level `theme` key is a deprecated alias and the two cannot both be present.
- `design.typeScale` is the working replacement for `theme.fonts.*.size`, `.lineHeight` and `.weights`, which validate but reach nothing.

### Deployment — Scalingo

The app is deployed to Scalingo via the Sovrium buildpack. Four files drive it; keep them in sync:

- `.buildpacks` — selects `https://github.com/sovrium/scalingo-buildpack`
- `.sovrium-version` — pins the release the buildpack downloads (checksum-verified). **Bumping this file is how the app is upgraded.**
- `Procfile` — `web: bin/sovrium start app.yaml` (the `bin/` prefix matters — the buildpack installs into the app tree, not the system `PATH`)
- `scalingo.json` — the app manifest: declares the environment, and the container formation for review apps

Scalingo deploys from `master` while the default branch is `main`, so pushes are explicit: `git push scalingo HEAD:refs/heads/master`.

**The manifest applies at app creation, not on every deploy.** Scalingo reads `scalingo.json` when it *creates* an app — a review app, or a one-click deploy — never on a `git push` to an app that already exists. Editing `scalingo.json` therefore does nothing to a running app: change that app's environment with `scalingo --app <name> env-set` as well, or the two drift apart. A manifest variable replaces whatever the parent app holds, so a review app generates its own encryption key and points `BASE_URL` at itself.

### Environment Variables

Declared in `scalingo.json` — see README.md for why each one:

- `SOVRIUM_ENCRYPTION_KEY` (`generator: secret`) — must be set explicitly on a managed host, whose filesystem is rebuilt on every deploy. `AUTH_SECRET` derives from it and is never set alongside.
- `BASE_URL` (`generator: url`) — public origin; a non-loopback value switches on secure cookies and CSRF enforcement
- `NODE_ENV=production` — enables immutable caching for content-hashed assets
- `TRUSTED_PROXY_HOPS=1` — accounts for Scalingo's router so rate limits count per visitor
- `PORT` — injected by Scalingo (default: 3000 locally)
- `DATABASE_URL` — unused; the site is pages only, so the embedded SQLite default is fine. No add-on is declared, which also keeps review apps cheap.
