## Sovrium Documentation

This project uses [Sovrium](https://sovrium.com), a configuration-driven application platform. The entire app is defined in `app.yaml` and uses the Sovrium CLI directly — no TypeScript files.

### LLMs Documentation References

For complete Sovrium documentation, fetch these files:

- **Full reference**: `https://sovrium.com/llms-full.txt` — Complete docs (~45000 lines, EN + FR) covering schema, components, fields, actions, auth, themes, pages, the changelog, and more.
- **JSON Schema**: `https://sovrium.com/schema/app.json` — Machine-readable schema for validation and autocompletion. `sovrium schema` prints the schema the installed binary actually enforces.

When working on `app.yaml` or any Sovrium configuration, **always fetch `https://sovrium.com/llms-full.txt`** to get the latest documentation before making changes, and **always run `sovrium validate app.yaml`** afterwards — since v0.22.0 an unrecognised property fails the config instead of being ignored, so the validator names anything that no longer exists.

### Key Concepts

- **Config-driven**: The entire app (design system, languages, components, pages, analytics) is declared in YAML — `app.yaml` plus the partials it `$ref`s from `config/`.
- **Version**: pinned in `.sovrium-version` (currently 0.30.0) — the Scalingo buildpack downloads exactly that release.
- **49 field types**, **90 component types**, built-in auth, RBAC permissions, i18n.
- App is started with `sovrium start app.yaml` (CLI only, no TypeScript needed).

### Project Setup

- **No runtime and no package manager.** Sovrium is a self-contained binary; the project has no dependencies, no `package.json` and no lockfile. Do not add one.
- Install: `curl -fsSL https://sovrium.com/install | sh` (or `brew install sovrium/tap/sovrium`)
- Config: `app.yaml` is a table of contents; the content lives in `config/` (see below)
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

### Config layout

The config follows the `config/` convention Sovrium scaffolds: **one file per singleton, one file per collection entity, scalars inline.** `app.yaml` holds `name`, `version`, `description` and the `$ref` map, so what the app contains is legible without opening anything else.

```text
app.yaml                       # scalars + the $ref map
config/
  design.yaml                  # singleton
  auth.yaml                    # singleton
  languages.yaml               # singleton — locales and the $t: dictionary
  analytics.yaml               # singleton
  components/<name>.yaml       # one reusable component template per file
  pages/<name>.yaml            # one page per file
```

Working rules:

- **A partial is the entity, unwrapped.** `config/pages/home.yaml` starts at `name: home`, with no `pages:` key and no leading `-`. Same for a component template.
- **Adding a page means two edits**: the new `config/pages/<name>.yaml`, and its `- $ref:` line in `app.yaml`. A file nothing `$ref`s is dead weight — it is never read.
- **Order matters.** Pages and components are arrays, so the `$ref` order in `app.yaml` is their order in the app.
- `$ref` paths resolve relative to the file containing them, and all `$ref`s resolve into one object *before* validation — so cross-section checks still see the whole app, and errors are attributed to the partial they came from (`at pages[3].meta (legal.yaml)`).

### Config conventions for this app

- **Components are typed from a closed vocabulary.** Raw HTML tag names (`div`, `p`, `section`, `h2`, …) are not component types. Use `container` with `element: div|section|main|aside|nav|header|footer|article`, and `text` with `element: h1..h6|p|span|label|blockquote|code`.
- `text` renders a `<span>` unless you set `element:` — write `element: p` for real paragraphs.
- Page content lives under `pages[].components` (not `sections`).
- Design tokens are direct keys of `design` — `colors`, `radius`, `elevation`, `motion`, `breakpoints`, `typeScale`. Both `design.theme` and the top-level `theme` were removed in v0.30 and are refused.
- Colour token names are kebab-case (`text-muted`, not `textMuted`).
- Faces live in `design.typeScale.families`; sizes, leading and weight live in `design.typeScale.steps`. A face's `size`, `lineHeight` and `weights` validate but reach nothing.
- `design.spacing` takes lengths only (`px`/`rem`), each step becoming a utility suffix (`py-section`). A reusable class list belongs on `props.className`, not in a token.
- **Auth is on because the `auth` block exists** — there is no `enabled` flag; presence is the switch. It mounts `/api/auth/*`, RBAC and the admin endpoints. Every page stays public except the two signed-in spaces: `/espace-membre/*`, « Espace Membre », the coworker space (roles `coworker`, `admin`), and `/editor/*`, the editors' space (`editor`, `admin`). Both sign in at `/connexion`, which sends everyone to `/app` — no `landingPath`: in 0.30 a custom role's `defaultLanding` lands on `/403`.
- **The two spaces are app shells.** Each page places its space's sidebar template (`espace-membre-nav`, `editor-nav`) beside its own `<main>` — a component template cannot take children. Sidebar hrefs are literal paths: the current-entry mark does not match a `$t:` href.
- **Portal data is isolated by the tables, not the page.** Each portal table carries a `rowLevelPermissions.read` rule matching a stored email to `$currentUser.email`. Keep one on any table the portal reads; a relation-chain rule (`member.email`) fails on list reads in 0.30.
- **`allowSignUp: false` is deliberate.** The default is `true`, which on a public marketing site would let anyone create an account. Users are created by admins; `defaultRole: viewer` keeps them least-privilege.
- Auth needs a **persistent** database. Scalingo rebuilds the container filesystem on every deploy, so the SQLite default would discard users each time — this is why the PostgreSQL add-on is not optional here.

### Deployment — Scalingo

The app is deployed to Scalingo via the Sovrium buildpack. Four files drive it; keep them in sync:

- `.buildpacks` — selects `https://github.com/sovrium/scalingo-buildpack`
- `.sovrium-version` — pins the release the buildpack downloads (checksum-verified). **Bumping this file is how the app is upgraded.**
- `Procfile` — `web: bin/sovrium start app.yaml` (the `bin/` prefix matters — the buildpack installs into the app tree, not the system `PATH`)
- `scalingo.json` — the app manifest: declares the environment and the container formation

**The container must be `M`.** `formation.web.size` is `M` because an `S` container crashes on deploy — Sovrium compiles the stylesheet at boot and that does not fit. Do not trim it back to `S` to save money.

Scalingo deploys from `master` while the default branch is `main`, so pushes are explicit: `git push scalingo HEAD:refs/heads/master`.

**The manifest applies at app creation, not on every deploy.** Scalingo reads `scalingo.json` when it *creates* an app — a review app, or a one-click deploy — never on a `git push` to an app that already exists. Editing `scalingo.json` therefore does nothing to a running app: change that app's environment with `scalingo --app <name> env-set` as well, or the two drift apart. A manifest variable replaces whatever the parent app holds, so a review app generates its own encryption key and points `BASE_URL` at itself.

### Environment Variables

Declared in `scalingo.json` — see README.md for why each one:

- `SOVRIUM_ENCRYPTION_KEY` (`generator: secret`) — must be set explicitly on a managed host, whose filesystem is rebuilt on every deploy. `AUTH_SECRET` derives from it and is never set alongside.
- `BASE_URL` (`generator: url`) — public origin; a non-loopback value switches on secure cookies and CSRF enforcement
- `NODE_ENV=production` — enables immutable caching for content-hashed assets
- `TRUSTED_PROXY_HOPS=1` — accounts for Scalingo's router so rate limits count per visitor
- `PORT` — injected by Scalingo (default: 3000 locally)
- `DATABASE_URL` — **injected by the PostgreSQL add-on**, never declared in `scalingo.json`. Its presence is what switches Sovrium off its embedded SQLite default.
- `PENNYLANE_API_TOKEN` — Pennylane company token (read and write) for the portal's sync and mandate requests. Required: the app refuses to boot without it.
- `SMTP_*` — needed for coworker invitations and password resets.
- `MCP_ENABLED=true` — mounts the MCP server at `/mcp` (see below).
- `AUTH_ADMIN_EMAIL` / `AUTH_ADMIN_PASSWORD` (`generator: secret`) — seed the first administrator. **Both are inert until the config declares an `auth` block** — the admin plugin turns on with `auth` and not before. Seeding runs only against a fresh database and only with both set; later boots no-op rather than duplicating or modifying a user.

### MCP server

`MCP_ENABLED=true` mounts `/mcp`, so Claude can read the app's data. Every table declares `aiAccess` with `operations: [read, list]` — **read-only by design**: the Pennylane tables are mirrors the sync overwrites, and writes stay in the admin and the portal. An admin key also sees the read-only `{app}_auth_*` / `{app}_system_*` tools and the four `{app}_config_*` tools.

- **Credential**: an API key minted in `/_admin` by the user whose role Claude should inherit, sent on **`x-api-key`** (a key on `Authorization: Bearer` answers 401). Row-level rules apply to the key's owner, so a coworker's key sees only their own rows.
- **Connect Claude Code**: `claude mcp add --transport http laplage https://la-plage-digitale.osc-fr1.scalingo.io/mcp --header "x-api-key: <key>"`
- **Check it** by hand: the HTTP route speaks only protocol revision `2026-07-28` (a legacy `initialize` is refused), which needs two headers and a `_meta` envelope. Claude Code handles this itself.

  ```bash
  curl -s -X POST "$BASE_URL/mcp" -H "x-api-key: $KEY" \
    -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/list' \
    -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientCapabilities":{},"io.modelcontextprotocol/clientInfo":{"name":"curl","version":"0"}}}}'
  ```

  A `200` with an empty list is eligibility (no `aiAccess`), a `401` is the credential. An admin key also lists `{app}_system_automation_runs_*` and `_run_steps_*` — the way to read why a run failed.

### Automations

`app.yaml` ends with an `env:` block, the `connections:` installed from the Sovrium library (`library/connection/*.yaml`, written by `sovrium library add connection/<name>`) and the `automations:` list. One file per automation under `config/automations/`.

- **`notion-hebdo`** — every Monday 08:30 (Europe/Paris) posts a French digest of the Notion task database in Slack `#notion-hebdo` and writes one row per week in « Indicateurs d'usage Notion ». The code step reads Notion through the `notion` connection (token injected, cursor pagination in the request body, adaptive `page_size` under the 64 KiB response cap). It adapts to the V1 schema (`Status`) and the V2 schema (`Statut`), so it can be tested against either database.
- **Run it on demand** (admin only, no need to wait for Monday):

  ```bash
  curl -s -c /tmp/sv.jar -H 'Content-Type: application/json' \
    -d '{"email":"<admin>","password":"<pwd>"}' http://localhost:3000/api/auth/sign-in/email
  curl -s -b /tmp/sv.jar -H 'Content-Type: application/json' \
    -d '{"dryRun":true,"channel":"C_TEST_CHANNEL"}' http://localhost:3000/api/automations/notion-hebdo/trigger
  ```

  `dryRun: true` skips the metrics row; `channel` overrides the destination. In production add `-H "Origin: $BASE_URL"` to both calls (CSRF), and read the run with `GET /api/automations/runs/<id>`.
- **Environment**: `NOTION_TOKEN`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`, `NOTION_TASKS_DATA_SOURCE_ID` are required at boot; `NOTION_METRICS_DATA_SOURCE_ID` is optional. Set them with `scalingo env-set` **before** pushing — a missing required variable refuses to start. Keep `formation.web.amount: 1`: the cron scheduler is in-process, a second container would post twice.
- **Slack app** (`A0C71BTPUCS`): bot scopes `chat:write` and `channels:read`; the bot must be invited to the channel (or have `chat:write.public`). Slack answers errors as HTTP 200 with `ok: false`, which the `assertPosted` step turns into a failed run.
- The code step is type-checked by `sovrium validate app.yaml`: annotate anything TypeScript cannot infer (an `opts = {}` parameter, `let x` without initial value).
