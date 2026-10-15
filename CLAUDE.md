## Sovrium Documentation

This project uses [Sovrium](https://sovrium.com), a configuration-driven application platform. The entire app is defined in `app.yaml` and uses the Sovrium CLI directly — no TypeScript files.

### LLMs Documentation References

For complete Sovrium documentation, fetch these files:

- **Full reference**: `https://sovrium.com/llms-full.txt` — Complete docs (~45000 lines, EN + FR) covering schema, components, fields, actions, auth, themes, pages, the changelog, and more.
- **JSON Schema**: `https://sovrium.com/schema/app.json` — Machine-readable schema for validation and autocompletion. `sovrium schema` prints the schema the installed binary actually enforces.

When working on `app.yaml` or any Sovrium configuration, **always fetch `https://sovrium.com/llms-full.txt`** to get the latest documentation before making changes, and **always run `sovrium validate app.yaml`** afterwards — since v0.22.0 an unrecognised property fails the config instead of being ignored, so the validator names anything that no longer exists.

### Key Concepts

- **Config-driven**: The entire app (design system, languages, components, pages, analytics) is declared in YAML — `app.yaml` plus the partials it `$ref`s from `config/`.
- **Version**: pinned in `.sovrium-version` (currently 0.37.0) — the Scalingo buildpack downloads exactly that release.
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
- **Auth is on because the `auth` block exists** — there is no `enabled` flag; presence is the switch. It mounts `/api/auth/*`, RBAC and the admin endpoints. Every page stays public except the two signed-in spaces: `/espace-membre/*`, « Espace Membre », the coworker space (roles `coworker`, `admin`), and `/administration/*`, « Administration de l'association » — Calendrier de gestion, Membres, Finances, Contenu (role `admin`; `editor` only on `/administration/contenu/*` and `/administration/compte`). Both sign in at `/connexion`, which sends everyone to `/app`; `/app` shows each role exactly one card and forwards to it — coworker → `/espace-membre`, admin → `/administration`, editor → `/administration/contenu`. No `landingPath`: in 0.30 a custom role's `defaultLanding` lands on `/403`.
- **The two spaces are app shells.** Each page places its space's sidebar template (`espace-membre-nav`, `admin-nav`) beside its own `<main>` — a component template cannot take children. Sidebar hrefs are literal paths: the current-entry mark does not match a `$t:` href. A sidebar group cannot be gated, so `admin-nav` declares two sidebars, one per role (`admin`, `editor`). Its « Mon Espace Membre » link is a `list` on the admin's own `members` row filtered on `pennylane_customer_id isNotEmpty` with `hideWhenEmpty` — not a `visibility.record` gate, which would make every admin page bind a `members` row (and 404 without one). Admin pages need no member binding.
- **The Calendrier de gestion** (`/administration/calendrier`, admin only) is the `management_deadlines` table: one row per recurring obligation, carrying the date of its NEXT occurrence. The calendar and the read-only list both open `/administration/calendrier/:id`, the one place a deadline is edited; `/administration/calendrier/nouvelle` (declared form `deadline-new`, a page form never creates a row) is `$ref`'d before `:id`. Nothing rolls a date forward by itself: « Marquer comme fait » (on the deadline's page, or « Fait » in the list) runs `management-deadline-done`. « Supprimer » is only in the list: in 0.37 a `crud delete` on a lone button renders in a hidden island. The detail page cannot reload after « Fait » (an automation button drops `onSuccess.navigate`; a `fetch` body sends `$record.id` literally on a page-level binding), so its form auto-saves field by field — its « Mettre à jour » sends every field, a stale `due_date` included. The admin sidebar's header and footer are pinned from lg up: only the wrapper around the two sidebars scrolls (`lg:flex-1 lg:min-h-0 lg:overflow-y-auto`), and both wrappers are `max-lg:contents` so the phone top bar is unchanged.
- **The Trésorerie & prévisionnel** (`/administration/finances/tresorerie`, `/previsionnel`, `/previsionnel/nouveau` — declared form `scenario-new`, `$ref`'d before `:scenario` —, `/previsionnel/:scenario`, `/transactions`; admin only) replaces the « Trésorerie - La Plage Digitale » sheet. Ten tables (ids 11–20): `bank_accounts` (Pennylane mirror + the manual Livret A, `pennylane_id` `pl:<id>` / `manual:livret-a`), `transactions` (mirror filed on a `budget_line`, with `amount_in`/`amount_out` because a KPI cannot abs(), and the accountant's `needs_attention`/`attention_reason`), `budget_lines` (both lenses: `cash_group` = catégorie de trésorerie, `pcg_account`/`pnl_group` = type de dépense), `category_mappings` (Pennylane category first, regex rules after, catch-all last), `scenarios` (assumptions + the figures the engine writes, `scenario_key` unique), `budget_entries` (WIDE: one row per line, `m01`…`m12`; a filled cell replaces the projection), `budget_adjustments` (a monthly amount over a range; hire/raise on 641 adds employer charges on 645), `planned_items` (dated items; the sync's `inv:c:`/`inv:s:` rows for open invoices), and the computed `forecast_months` (line × month) and `forecast_balances` (month — what the charts bind: a chart with several `series` needs one row per x and one column per series; a `chartAggregate` chart takes ONE series). Text copies (`scenario_key`, `line_code`, `cash_group`, `is_baseline`) exist because a filter cannot traverse a relationship. `key`, `group` and `order` are reserved SQL words: never name a field so. `$startOfYear` does not exist: the engine writes the plan year only and every row carries `year`. Every record step — batch operators included — dispatches record automations once per row written: the engine writes only tables nothing watches, `treasury-forecast-on-planned` keeps to `source: manual` rows, and the engine skips a scenario computed after the edit (`$changedAt`). A scenario page polls (`refreshMode: poll`) because an automation button cannot reload the page. **A record-detail route's parameter is `:id` / `param: id`**: in 0.37 any other name (`:scenario`) answers 404 for every record.
- **The Espace Membre is personalised by formule.** `members.formules` (multi-select `fixe`, `nomade`, `flex`, `box`, `domiciliation`) is derived by `pennylane-sync` from the Pennylane subscriptions, Flex check-ins and accepted Flex sign-ups; `formule_source: manual` (set by an admin on `/administration/membres/:id`) is never overwritten. Every coworker page binds `dataSource: { table: members, mode: single, filter: [{ field: email, operator: eq, value: $currentUser.email }] }` — without the filter an admin binds the *first* member — and gates blocks with `visibility: { record: { field: formules, contains: <f> } }`. The sidebar's formule gates read that page record, so a coworker page left unbound shows every gated entry. `notIn`/`neq` do not work on a multi-select: there is no "not Flex" gate. An account with no `members` row gets a 404 on these pages. Member content (`member.*` keys) never carries a code or password.
- **A coworker changes their own sign-in e-mail** on `/espace-membre/compte` (`POST /api/auth/change-email`; the link goes to the new address, and lands on `/` — an endpoint form cannot hide a `callbackURL` field in 0.37). Because everything is keyed on the address, `member-email-sync` (auth `emailVerified` + `signIn`) follows `members.user_id` — the account id, set by `member-sign-up`, on each sign-in, and backfilled by `pennylane-sync` through `sovrium-admin` — and rewrites `members.email`, `member_email` on `invoices`/`mandates`/`checkins`/`mandate_requests`, and the Pennylane customer's `emails`. A new table keyed on `member_email` must be added to that list.
- **Invoice recipients** are the Pennylane customer's `emails`. A coworker edits them on `/espace-membre/factures` through `update-billing-emails` (the login email is always kept: the sync matches on it); `pennylane-sync` mirrors them into `members.billing_emails`. That field is the only one a coworker may write on `members` (table `update: [coworker, admin]`, row-level `write` on their own email, every other field `write: [admin]`).
- **Portal tables of Pennylane mirrors are `readOnly: true`** — an admin may create rows and would otherwise get « Nouvel enregistrement ». An invoice row opens its `pdf_url` (`onRowClick` navigate, new tab); the mandate is one card (a `list` with `limit: 1` and `record-field` children), not a table.
- **Direct debit runs on the Pennylane Compte Pro, not GoCardless.** « Mettre en place le prélèvement » calls `POST /pro_account/mandate_requests` with the customer id alone — Pennylane writes the mail and sends it to the customer's Pennylane `emails`, so no recipient, subject or return link can be set. The button sends the member row's `email` and `request-mandate` filters its three reads on it: row-level rules let an admin read every row, so unfiltered reads took the first member and refused on anyone's mandate or recent request. The button sits in a `list` bound to that row because a fetch body fills `$record.email` only from a list item. `$currentUser.email` and a page binding are sent as written in 0.37. A Compte Pro mandate has no id and no IBAN in the API: `pennylane-sync` keeps one `mandates` row per customer (`pennylane_id: pro-<customer id>`, the most relevant mandate), folds Pennylane's undocumented statuses into `active`/`pending`/`failed`/`ended` (`enabled`, `active` and `valid` — what a signed mandate answers — are active; raw value in `pennylane_status`, an unknown one is logged) and stores the signed PDF in `pdf_url`. `pdf_url` on `mandates` and `invoices` is `long-text`, not `url`: in 0.37 a `url` field is `VARCHAR(255)` on PostgreSQL and Pennylane's signed links run past 2 000 characters — SQLite has no limit, so test such a write on PostgreSQL. `pennylane-direct-debit` then switches every monthly subscription of that customer, whatever its amount, to `payment_method: pro_account_sepa_core`, so each is debited what Pennylane invoices it; Pennylane debits at least 14 days after the due date. « Vérifier mon mandat » (`verify-mandate`, same `email` body) re-reads the caller's mandate at once — Pennylane has no webhook for mandates — and hands the write to `verify-mandate-apply` (`automation-call`, so it writes as the system: a coworker may not write `mandates`); its status fold is a copy of `pennylane-sync`'s, keep the two alike. Pennylane's API cannot revoke a Compte Pro mandate, so there is no « supprimer » button.
- **Portal data is isolated by the tables, not the page.** Each portal table carries a `rowLevelPermissions.read` rule matching a stored email to `$currentUser.email`. Keep one on any table the portal reads; a relation-chain rule (`member.email`) fails on list reads in 0.30.
- **Flex.** `/flex` (public) explains the day pass and takes first-visit sign-ups into `flex_signups` (write-only for visitors, like `leads`; the billing address in parts — street, postal code, city, country — as Pennylane wants it). An admin presses « Valider » on the sign-up at `/administration/inscriptions-flex`: `flex-signup-validate` finds or creates the Pennylane customer, links the `members` row (`match_status: manual`), invites the person as a `coworker` and marks the sign-up `invited`; « Refuser » marks it `declined`. A Flex coworker checks in at `/espace-membre/presences` (sidebar « Présences »): an endpoint form posting to the records API, **not** a declared form — in 0.37 a declared form's submission skipped the table's row-level `create` rule and accepted another member's email, the records API enforces it. `flex-check-in` then dates the row (Europe/Paris), keeps one row per member per day (a full day replaces the half day) and stamps the amount HT (14 € / 7 €). Admins see and correct every check-in at `/administration/finances/flex` and every sign-up at `/administration/inscriptions-flex`; `members.association_member` (admin-ticked) gives one free full day per calendar year.
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
- `PENNYLANE_API_TOKEN` — Pennylane company token (read and write) for the portal's sync and mandate requests. Required: the app refuses to boot without it. The Trésorerie's sync also needs the `bank_accounts:readonly` and `categories:readonly` scopes on that token — without them `pennylane-treasury-sync` fails at `get-bank-accounts` with a 403 naming the scope.
- `SMTP_*` — needed for coworker invitations and password resets.
- `INVITE_API_KEY` — API key of an admin account, minted in `/_admin` (API keys) while signed in as an admin. `flex-signup-validate` sends the coworker invitation through the app's own `POST /api/auth/admin/invite-user` with it, and `pennylane-sync` reads the account ids for `members.user_id` (connection `sovrium-admin`, `config/connections/`): 0.37's automation `auth` actions cannot invite. Empty refuses every validation before anything is written. Declared in `app.yaml`'s `env:` block, like `BASE_URL`, which that connection also reads. Locally `BASE_URL` is loopback, which the outbound guard refuses: start with `SOVRIUM_ALLOW_PRIVATE_OUTBOUND=1` to exercise the invitation.
- `FLEX_SIGNUP_APPLY` — optional, default `'true'`; `'false'` makes « Valider » a dry run (the run says what it would create, link and invite, writes nothing).
- `DIRECT_DEBIT_APPLY` — optional, default `'true'`; `'false'` makes `pennylane-direct-debit` a dry run.
- `DEADLINES_SLACK_CHANNEL_ID` — required, the channel the Calendrier de gestion reminders go to (`C08HQQ2DT9A`); the Slack bot must be in it. `DEADLINES_APPLY` — optional, default `'true'`; `'false'` makes `management-reminders` a dry run.
- `FLEX_INVOICING_APPLY` — optional, default `'true'`; `'false'` makes the monthly Flex invoicing a dry run (logs and mails what it would create, writes nothing). Like the other `*_APPLY` flags it is declared in `app.yaml`'s `env:` block, not in `scalingo.json`.
- `PENNYLANE_COMPANY_ID` (default `'21901400'`), `TREASURY_SYNC_SINCE_DAYS` (default `'120'`), `TREASURY_COMFORT_THRESHOLD` (default `'10000'`) — the Trésorerie's three optional variables: the Pennylane link of a transaction, the hourly sync window, the « tendu » threshold of a scenario's low point. Dry runs are per call (`{"dryRun": "true"}` in the trigger body), not env flags.
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
- **`flex-check-in`** — on every new `checkins` row: dates it, drops a duplicate or a change to a day already billed, lets a full day replace the same day's half day, links the `members` row and stamps the amount.
- **`flex-signup-validate`** — the « Valider » button on a `new` Flex sign-up (manual trigger, admin). Reuses the Pennylane customer whose emails include the sign-up's e-mail (several → refused, nothing written), else creates it — `post-company-customer` when a company or SIRET is given, `post-individual-customer` otherwise, both added with `sovrium library add pennylane/<op>`, `external_reference: flex-signup-<id>`. Then upserts the `members` row (`pennylane_customer_id`, `match_status: manual`, `association_member` when ticked), invites the address as `coworker` unless it already has an account, and sets the sign-up `invited` with the customer id. Idempotent: a non-`new` sign-up is a no-op, and the customer id is kept on the sign-up as soon as it exists. On demand: `POST /api/automations/flex-signup-validate/trigger` with `{"signupId": "12", "dryRun": true}`.
- **`flex-invoicing`** — the 1st of each month at 06:00 (Europe/Paris) creates ONE finalized Pennylane invoice per linked member for the check-ins still `to_invoice` dated before the 1st (lines « Flex — journée complète » / « Flex — demi-journée », VAT `FR_200`, due +15 days, `external_reference: flex-<member id>-<YYYY-MM>`), marks the rows `invoiced` with the invoice id, and mails `TREASURER_EMAIL`. Unlinked members are skipped (rows stay `to_invoice`). It calls the `post-customer-invoices` operation, added with `sovrium library add pennylane/post-customer-invoices`. `FLEX_INVOICING_APPLY=false` (default `true`) makes it a dry run. The invoice is not e-mailed by the run (TODO: Pennylane answers 409 to `send_by_email` until the PDF exists). On demand: `POST /api/automations/flex-invoicing/trigger` with `{"dryRun": true}` (optionally `"month": "2026-09"`), same sign-in as below.
- **`management-reminders`** — every day at 09:00 (Europe/Paris) reads the active `management_deadlines` and posts in `DEADLINES_SLACK_CHANNEL_ID` at most two messages per occurrence: from `notice_days` before `due_date` (« Dans N jours »), then on the day (« C'est aujourd'hui »), the owner mentioned via `users.lookupByEmail`. With `create_notion_card`, the first one creates a `[Calendrier] <title>` card in the Notion task database (`Responsable` from the owner's Notion e-mail, `Date de clôture estimée`, `Statut` left to Notion's default). `notice_sent_for` / `dayof_sent_for` hold the `due_date` each message was sent for, written once Slack answered `ok` — a replay sends nothing, a new date re-arms both. A past deadline is never reminded nor rolled forward. Each row is handled on its own and the run fails at the end naming those that failed. On demand: `{"dryRun": true, "today": "2027-03-17", "channel": "C…"}`.
- **`management-deadline-done`** — « Marquer comme fait » (manual trigger, admin, `{"deadlineId": "3"}`): stamps `last_done_on`, switches a `once` row off, else moves `due_date` by whole periods (12/6/3/1 months) past today, the day clamped to the month's length from the original day.
- **`pennylane-treasury-sync`** — hourly (`'7 * * * *'`): mirrors the Pennylane bank accounts (`bank_accounts`, never a manual row), the categories (one `category_mappings` row each, `budget_line` never overwritten), the window's transactions (`TREASURY_SYNC_SINCE_DAYS`, or `{"since": "2025-01-01"}` in the body for the backfill; 50 per page under the 64 KiB cap) each filed on a line — Pennylane category mapping, then manual regex rules by priority, then the catch-all of its sign —, and the open customer/supplier invoices as `planned_items` (`inv:c:`/`inv:s:`, done once closed); then runs the engine. `matched` = |outstanding_balance| < 0,01 (no per-transaction call); `justified` = matched or no receipt required.
- **`treasury-forecast-compute`** (`config/actions/`, the one `actions:` template) — the engine, `$ref`'d by `treasury-forecast` (manual: the « Recalculer » buttons, `POST /api/automations/treasury-forecast/trigger {"scenarioId"?, "dryRun"?, "purge"?}`), the sync, `treasury-scenario-init` (record `create` on `scenarios`: copies the model) and `treasury-forecast-on-budget` / `-on-adjustment` / `-on-planned` (record triggers with `$vars { scenarioId: '{{trigger.data.record.scenario}}', changedAt: '{{trigger.data.record.updated_at}}' }`). Rules: actuals per line from `transactions` on cash accounts; projection `blend` (0,33 × YTD + 0,67 × trailing 12), `trailing12`, `shift_year`, `vat_estimate` (TVA of M−1), `zero`, `none`; prudence (`certain` → max, `prudent` → min × (1 − haircut)); current month = max(actual, budget ?? projection) + adjustments + dated items; opening = Pennylane balance now − net flows since 1 January; `check_delta` per past month must be 0. `treasury-seed` (manual, `{"dryRun": "true"}` first) loads lines, rules, the baseline, the Livret A (30 691,66 € as of 2026-06-24 — bank to confirm) and the first dated items; it never overwrites an admin's figures.
- **Run it on demand** (admin only, no need to wait for Monday):

  ```bash
  curl -s -c /tmp/sv.jar -H 'Content-Type: application/json' \
    -d '{"email":"<admin>","password":"<pwd>"}' http://localhost:3000/api/auth/sign-in/email
  curl -s -b /tmp/sv.jar -H 'Content-Type: application/json' \
    -d '{"dryRun":true,"channel":"C_TEST_CHANNEL"}' http://localhost:3000/api/automations/notion-hebdo/trigger
  ```

  `dryRun: true` skips the metrics row; `channel` overrides the destination. In production add `-H "Origin: $BASE_URL"` to both calls (CSRF), and read the run with `GET /api/automations/runs/<id>`.
- **Environment**: `NOTION_TOKEN`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`, `NOTION_TASKS_DATA_SOURCE_ID` are required at boot; `NOTION_METRICS_DATA_SOURCE_ID` is optional. Set them with `scalingo env-set` **before** pushing — a missing required variable refuses to start. Keep `formation.web.amount: 1`: the cron scheduler is in-process, a second container would post twice.
- **Slack app** (`A0C71BTPUCS`): bot scopes `chat:write`, `channels:read`, and `users:read` + `users:read.email` (blocked cards ping the people in « En attente de », matched by their Notion email — the Notion integration needs the *read user information including email* capability; without either, the name is shown instead); the bot must be invited to the channel (or have `chat:write.public`). Slack answers errors as HTTP 200 with `ok: false`, which the `assertPosted` step turns into a failed run.
- The code step is type-checked by `sovrium validate app.yaml`: annotate anything TypeScript cannot infer (an `opts = {}` parameter, `let x` without initial value).
