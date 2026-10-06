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
  auth.yaml                    # strategies, sign-up policy, roles
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
    login.yaml                 # coworker sign-in
    portal.yaml                # coworker portal (invoices, direct debit)
  tables/                      # data the portal reads, one per file
    members.yaml
    invoices.yaml
    mandates.yaml
    mandate-requests.yaml
    payment-matches.yaml       # log of the payment matching (admin only)
  automations/                 # Pennylane sync, mandate request, payment matching
    member-sign-up.yaml
    pennylane-auto-match.yaml
    pennylane-match-pending.yaml
    pennylane-sync.yaml
    request-mandate.yaml
library/
  connection/pennylane.yaml    # installed by `sovrium library`; see below
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

## Coworker portal

`/portal` is where a coworker finds their own Pennylane invoices, with payment
status and PDF, and asks for a GoCardless direct-debit mandate. A page cannot
call an external API while it renders, so Pennylane is **mirrored into tables**
and the pages read those tables:

| Automation                | When                 | Does                                                                 |
| ------------------------- | -------------------- | -------------------------------------------------------------------- |
| `member-sign-up`          | account created      | files a `members` row for a `coworker` account                       |
| `pennylane-match-pending` | every 30 min         | links each unlinked member to the Pennylane customer with that email |
| `pennylane-sync`          | every 15 min         | mirrors the linked members' invoices and GoCardless mandates         |
| `request-mandate`         | the portal's button  | asks Pennylane to email the coworker their GoCardless signing link   |

**Isolation is the tables' job, not the page's.** Every portal table has a
row-level rule matching the row's email to the signed-in user's email, so the
records API, the page and an automation the coworker starts all serve only
their own rows; another coworker's record answers `404`. Only admins and the
automations write.

**Onboarding a coworker:**

1. Invite them from `/_admin/users` with the role **`coworker`**. That fires
   `member-sign-up`, which files their `members` row.
2. Within 30 minutes they are linked to the Pennylane customer whose emails
   include their login email. If none or several match, the row reads
   `not_found`: set `pennylane_customer_id` yourself and `match_status` to
   `manual` in `/_admin` — the matcher then leaves it alone.
3. An account switched to `coworker` *after* it was created fires nothing — add
   its `members` row by hand (the email is enough).

Pennylane's invoice PDF link (`public_file_url`) expires 30 minutes after it is
issued; the 15-minute sync rewrites it, so the link on screen still opens.

The Pennylane connection lives in `library/connection/pennylane.yaml`, where
`sovrium library add` wrote it. Leave it there unedited so later
`sovrium library add pennylane/<operation>` calls can keep extending it.

Sovrium 0.30 behaviours the config works around, each noted where it applies:
the `signIn` auth event does not fire on an email-and-password sign-in; neither
an auth- nor a cron-triggered run may call another automation; a row rule
through a relationship (`member.email`) fails on list reads; and an `or` filter
on an automation `list` step matches nothing.

## Payment matching

`pennylane-auto-match` runs every morning at 06:30 (Europe/Paris), before
Pennylane's dunning emails go out, so a client who has paid is not reminded.
It reads the incoming transfers still to allocate (`outstanding_balance` not
zero — a transfer already matched is never reused) and the open customer
invoices, and matches a pair in Pennylane only when the amount is exact and
either the bank label carries the invoice number (as written, or just its
7-digit sequence, which survives a missing "F" or a wrong month) or the amount,
client name and date clearly agree ahead of any other candidate. Doubtful pairs
are never written: they land in `payment_matches` as `review`.

Each run logs every pair in `payment_matches` and mails a summary to
`TREASURER_EMAIL` when something was matched, failed, or is newly to review.
Set `AUTOMATCH_APPLY=false` to make it a dry run (pairs logged as
`would_apply`, nothing written to Pennylane).

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

- **`PENNYLANE_API_TOKEN`** — a Pennylane *company* API token with **read and
  write** access (Settings › Connectivity › Developers). Write access is what
  lets the portal send a mandate request and `pennylane-auto-match` match
  payments to invoices. The app refuses to boot without it.
- **`AUTOMATCH_APPLY`** — optional, default `true`. `false` turns the payment
  matching into a dry run.
- **`TREASURER_EMAIL`** — optional, default `tresorerie@laplagedigitale.fr`:
  where the payment-matching summary goes (needs the `SMTP_*` variables).

Two more variables seed the first administrator:

- **`AUTH_ADMIN_EMAIL`** — `contact@laplagedigitale.fr`.
- **`AUTH_ADMIN_PASSWORD`** (`generator: secret`) — generated per app, so a
  review app never shares production's admin credentials. Read it back with
  `scalingo --app <name> env`.

Seeding runs only against a *fresh* database and only when both variables are
set; on later boots it no-ops rather than duplicating or modifying an existing
user. The startup banner confirms it with an `Admin:` line.

> [!NOTE]
> **The site stays public.** Every page except `/portal` is readable without a
> session; `/portal` admits the `coworker` and `admin` roles. `allowSignUp` is
> `false`, so nobody can create their own account; the default is `true`, which
> would let anyone sign up on a public site. Coworkers are invited.

`addons` provisions PostgreSQL (`postgresql-starter-512`). Scalingo injects
`DATABASE_URL` from the add-on, which is why that variable is not declared in
`env` — Sovrium switches from its embedded SQLite to Postgres on seeing it.
The add-on is **required now that auth is on**: Scalingo rebuilds the container
filesystem on every deploy, so a SQLite database would throw away every user
account on each release.

**Email is required by the portal.** Coworker invitations and password resets
are mailed, so set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`,
`SMTP_FROM` (and optionally `SMTP_FROM_NAME`, `SMTP_SECURE`) with
`scalingo env-set`. Until then the startup banner says mail is not sent. (The
mandate email itself is sent by Pennylane, not by this app.)

The `formation` pins one **M** container. Do not size it back down — an `S`
container crashes on deploy: Sovrium compiles the stylesheet at boot, and that
does not fit in `S`.

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

> [!WARNING]
> `PENNYLANE_API_TOKEN` has no value in the manifest, so a review app asks for
> one. Do not give it production's token: its crons would read the real
> company's invoices, and its mandate button would email real customers.

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
