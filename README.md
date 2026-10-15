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
    connexion.yaml             # the one sign-in page (coworkers, admins and editors)
    app-landing.yaml           # /app — "Mes espaces", routes each role
    portal*.yaml               # the Espace Membre, the coworker space (/espace-membre/*)
    admin*.yaml                # the Administration de l'association (/administration/*)
  tables/                      # data the Espace Membre reads, one per file
    members.yaml
    invoices.yaml
    mandates.yaml
    mandate-requests.yaml
    payment-matches.yaml       # log of the payment matching (admin only)
  automations/                 # Pennylane sync, mandate request, payment matching
    member-sign-up.yaml
    pennylane-auto-match.yaml
    pennylane-sync.yaml
    request-mandate.yaml
    pennylane-direct-debit.yaml
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

## Espace Membre — the coworker space

`/espace-membre` (« Espace Membre ») is where a coworker administers their place
at La Plage: their formule, their Pennylane invoices (payment status and PDF),
their direct-debit mandate (Pennylane Compte Pro), the meeting rooms, the practical guide
and community life — everything that used to live in the Notion « Kit du
Plagiste ». It is an app shell: a sidebar (`espace-membre-nav`) beside

| Page | Path | Shows |
| ---- | ---- | ----- |
| Accueil | `/espace-membre` | formule badges and one card per formule held, the Flex check-in card, what is left to pay, latest invoices, mandate, first steps |
| Ma formule | `/espace-membre/formule` | what each formule held includes, how to change it |
| Factures / Prélèvement | `/espace-membre/factures`, `/prelevement` | invoices; the mandate and its request button |
| Salles de réunion | `/espace-membre/salles` | the four rooms; Google Calendar booking (Fixe) or the request form; room rules |
| Présences | `/espace-membre/presences` | the Flex check-in (sidebar entry for Flex members only) |
| Guide pratique | `/espace-membre/guide` | access, Wi-Fi, printing, kitchen, furniture, parking, lockers and mail, safety, contacts |
| Vie de la communauté | `/espace-membre/communaute` | Slack, Conseil de la Plage, rituals, events, the association |
| Règlement & documents | `/espace-membre/documents` | the gist of the rules and the four PDFs in `public/documents/` |
| Partenaires | `/espace-membre/partenaires` | partner discounts |
| Compte | `/espace-membre/compte` | display name, password, sign-out |

The old `/portal` and `/login` addresses redirect.

**Personalised by formule.** `members.formules` (multi-select: `fixe`,
`nomade`, `flex`, `box`, `domiciliation`) says what the member rents.
`pennylane-sync` derives it from the member's active Pennylane subscriptions
(by amount, then by label), their Flex check-ins of the last 90 days and an
accepted Flex sign-up. An admin corrects it on `/administration/membres/:id`
with source « Fixée à la main », which the sync never overwrites. Every
coworker page binds the signed-in member's own row
(`dataSource: { table: members, mode: single, filter: email = $currentUser.email }`)
and gates its formule blocks with `visibility: { record: { field: formules, contains: … } }`.
Sovrium cannot gate on "does not contain", so nothing is shown *only* to
non-Flex members. **An account with no `members` row gets a 404** on these
pages: `member-sign-up` files one for every new coworker and admin; add it by
hand (the email is enough) for an older account.

**No code or password goes into these pages** — not the Wi-Fi password, nor a
door, alarm, locker or mailbox code: they stay on site, at reception.

The **Administration de l'association** (`/administration/*`) has the same
shape: one sidebar (`admin-nav`), three sections.

- **Membres** — the members, the invitations, one member's space read-only,
  and the Flex sign-ups to validate.
- **Finances** — an overview, every member invoice, the Flex check-ins to
  invoice (editable), the Compte Pro direct-debit mandates and requests, and the
  `pennylane-auto-match` log. All of it is a Pennylane mirror: read-only here,
  corrected in Pennylane.
- **Contenu** — the blog: a dashboard, the post lists (all, drafts,
  published) and the editor. « Nouvel article » asks for the title and the
  address, creates the draft and opens it in the editor
  (`/administration/contenu/articles/:id`): a blank page — title, then the
  rich-text body, typeset as the blog prints it, images uploaded into
  `blog-images` — with the article's details (status, date, address,
  summary, categories, author, cover) in a column beside it. A draft saves
  itself as you type; a published article saves on « Mettre à jour » only.

Admins see all of it. The `editor` role sees only « Contenu » and its account
page; every other admin page refuses it.

Both spaces share one sign-in, `/connexion`, which sends everyone to `/app`.
That page forwards each role straight to its space: a coworker to
`/espace-membre`, an admin to `/administration`, an editor to
`/administration/contenu`. An admin whose `members` row is linked to Pennylane
— a coworker too — gets « Mon Espace Membre » in the Administration's sidebar,
and every admin gets « Administration de l'association » in the Espace Membre's.
The old `/editor/*`, `/espace-membre/membres` and `/espace-membre/flex`
addresses redirect. A page cannot
call an external API while it renders, so Pennylane is **mirrored into tables**
and the pages read those tables:

| Automation                | When                 | Does                                                                 |
| ------------------------- | -------------------- | -------------------------------------------------------------------- |
| `member-sign-up`          | account created      | files a `members` row for a `coworker` or `admin` account            |
| `pennylane-sync`          | every 15 min         | links each unlinked member to the Pennylane customer with that email, mirrors every linked member's invoices and Compte Pro mandates (one row per Pennylane customer), and derives each member's formules (Fixe, Nomade, Flex, Box, Domiciliation) from their subscriptions and check-ins |
| `request-mandate`         | the mandate button   | asks Pennylane to email the coworker the link to sign a Compte Pro SEPA mandate |
| `update-billing-emails`   | the recipients form on Factures | writes the addresses a coworker's invoices go to into their Pennylane customer (`emails`), then `members.billing_emails` |
| `member-email-sync`       | e-mail confirmed, sign-in | when a coworker confirmed a new sign-in address, moves their `members` row, every `member_email` copy and their Pennylane recipients to it (followed by `members.user_id`) |
| `pennylane-direct-debit`  | daily 05:45          | moves every monthly subscription (any amount) whose customer has an active Compte Pro mandate to Compte Pro direct debit (`pro_account_sepa_core`), and mails the treasurer what changed |
| `flex-check-in`           | a Flex check-in      | dates the new `checkins` row, keeps one row per member per day (a full day replaces the half day) and stamps its amount HT |
| `flex-signup-validate`    | « Valider » on a sign-up | finds or creates the Pennylane customer, links the member to it, invites them as a coworker |
| `flex-invoicing`          | 1st of month 06:00   | creates one Pennylane invoice per linked member for last month's Flex days, marks them `invoiced`, mails the treasurer |
| `management-reminders`    | daily 09:00          | reminds the Calendrier de gestion's deadlines in Slack (N days before, then on the day), mentioning the owner, and creates the Notion card when asked |
| `management-deadline-done`| « Marquer comme fait » | moves a deadline to its next occurrence (or switches a one-off off) |

**Isolation is the tables' job, not the page's.** Every portal table has a
row-level rule matching the row's email to the signed-in user's email, so the
records API, the page and an automation the coworker starts all serve only
their own rows; another coworker's record answers `404`. Only admins and the
automations write.

**Onboarding a coworker:**

1. Invite them from **`/administration/membres`** (admins only: « Inviter un
   membre ») — or from `/_admin/users` with the role **`coworker`**. The
   invitation creates the account at once, which fires `member-sign-up` and
   files their `members` row, so the sync starts before they accept.
2. Within 15 minutes they are linked to the Pennylane customer whose emails
   include their login email, and all their invoices (every status but
   drafts and proformas) appear in the Espace Membre. If none or several match, the row reads
   `not_found`: set `pennylane_customer_id` yourself and `match_status` to
   `manual` in `/_admin` — the matcher then leaves it alone.
3. An account switched to `coworker` *after* it was created fires nothing — add
   its `members` row by hand (the email is enough).

**Members pages (admins only).** `/administration/membres` lists every member
with their Pennylane link and the pending invitations (resend, revoke); a row
opens `/administration/membres/:id`, that member's space read-only — their
invoices, what is left to pay, their mandate and their Flex check-ins. No
session is swapped and nothing can be sent on the member's behalf. The members
table also carries the « Adhérent » box (`association_member`).
`/administration/inscriptions-flex` lists the Flex sign-ups, and
`/administration/finances/flex` every Flex check-in (editable).

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

## Flex — the day pass

Flex (14 € HT a full day, 7 € HT a half day, no booking) used to run on a
Notion page and an Airtable form. It now runs here:

1. **Sign-up** — a newcomer fills the form on **`/flex`**; it lands in
   `flex_signups` (visitors write, only admins read). On
   **`/administration/inscriptions-flex`** an admin presses **« Valider »** on the sign-up,
   and `flex-signup-validate` does the rest in one run:
   - reuses the Pennylane customer whose emails include the sign-up's e-mail,
     or creates it (a company customer when a company or SIRET is given, an
     individual one otherwise) with the billing address, phone, SIRET and VAT
     number. Several customers with that e-mail stop the run: link the member
     by hand;
   - links the `members` row to it at once (`match_status: manual`, so the
     sync never unlinks it) and ticks `association_member` if they joined the
     association;
   - invites the person as a `coworker` — the same e-mail as « Inviter un
     membre » — unless the address already has an account;
   - sets the sign-up's « Suivi » to « Invité·e » and keeps the customer id.

   A Pennylane error leaves everything as it was; pressing again after any
   failure picks up where the run stopped, never creating a second customer.
   « Refuser » sets « Sans suite ». A sign-up sent before the address was
   split in parts is read from its single address line (« … 67000
   Strasbourg »); if that fails, fill in postal code and city on the row.
2. **Check-in** — each visit, the coworker opens **`/espace-membre/presences`**
   and picks half day or full day. The day is set by `flex-check-in`; checking in
   again as a full day replaces the morning's half day. A billing-details change
   goes through contact+flex@ (no per-check-in override).
3. **Invoicing** — on the 1st at 06:00, `flex-invoicing` bills every check-in
   still `to_invoice` dated before the 1st: one finalized Pennylane invoice per
   member, dated that day, due 15 days later, then `pennylane-sync` mirrors it
   into the member's Factures. An association member's first full day of the
   year is `offered` (0 €). A member not linked to Pennylane is skipped and
   named in the treasurer's mail; their days are billed once they are linked.
   A billed row carries its invoice id and is never billed twice, and each
   invoice carries `external_reference` `flex-<member id>-<YYYY-MM>` so a rerun
   reuses it. The run does not e-mail the invoice (Pennylane needs a few minutes
   to build the PDF): send it from Pennylane.

Set `FLEX_INVOICING_APPLY=false` to preview: the run then only logs and mails
what it would create. An admin can also start it by hand:
`POST /api/automations/flex-invoicing/trigger` with `{"dryRun": true}` (and
`"month": "YYYY-MM"` to bill up to the end of another month).

## Calendrier de gestion

`/administration/calendrier` (admins) holds what the association has to think
of each year — activity report, general assembly, fire extinguishers, summer
offers… — on a month calendar coloured by pôle, with the same rows as a list.
Each deadline has its own page (`/administration/calendrier/:id`) where it is
edited, with its procedure and a link to its Notion page; new ones are added on
`/administration/calendrier/nouvelle`. The dashboard shows what is overdue and
the next 60 days.

A row carries the date of its **next** occurrence, a recurrence (year,
semester, quarter, month, once), how many days ahead to warn and an owner's
e-mail. Every morning at 09:00 `management-reminders` posts in the channel
`DEADLINES_SLACK_CHANNEL_ID`:

1. **N days before** — « Dans N jours », the owner mentioned (Slack
   `users.lookupByEmail`), the procedure's first lines; with « Créer une carte
   Notion » ticked, a `[Calendrier] …` card is created in the Notion task
   database with the owner and the date, so the Monday digest follows it;
2. **on the day** — « C'est aujourd'hui ».

Nothing moves the date by itself: « Marquer comme fait » on the deadline's page
moves it to the next occurrence (a 31st stays a month-end) or switches a
one-off deadline off. A deadline nobody marked stays overdue on the dashboard
and is not reminded again. Each message is stamped on the row once Slack
accepted it, so a replay never sends twice.

To test (admin session, see the curl under « Automations » in `CLAUDE.md`):

```bash
POST /api/automations/management-reminders/trigger
{"dryRun": true, "today": "2027-03-17", "channel": "C0123456789"}
```

`DEADLINES_APPLY=false` makes every run a dry run. The Slack bot must be in the
channel.

## Payment matching

`pennylane-auto-match` runs every morning at 06:30 (Europe/Paris), before
Pennylane's dunning emails go out, so a client who has paid is not reminded.
It reads the bank transactions still to allocate (`outstanding_balance` not
zero — a transaction already matched is never reused) and matches them on two
sides with the same rules:

- **customer** — incoming transfers against open customer invoices;
- **supplier** — outgoing payments (transfers, card payments, direct debits)
  against open supplier invoices in euros we have paid but Pennylane has not
  matched yet.

A pair is matched in Pennylane only when the amount is exact and either the
bank label carries the invoice number or the amount, counterparty name and
date clearly agree ahead of any other candidate. On the customer side the
number also counts by its 7-digit sequence alone, which survives a missing "F"
or a wrong month; a supplier's number follows its own format, so only the
number as written counts. The name is recognised from the label or, more
reliably, from the customer or supplier Pennylane has already attached to the
transaction. Doubtful pairs are never written: they land in `payment_matches`
as `review`.

Each run logs every pair in `payment_matches` (its `side` column says which)
and mails a summary to `TREASURER_EMAIL` when something was matched, failed,
or is newly to review. Set `AUTOMATCH_APPLY=false` to make the whole run a dry
run (pairs logged as `would_apply`, nothing written to Pennylane). The supplier
side is a dry run until `AUTOMATCH_SUPPLIER_APPLY=true`.

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
- **`AUTOMATCH_SUPPLIER_APPLY`** — optional, default `false`: the supplier side
  of the payment matching only logs `would_apply` until this is `true`.
- **`FLEX_INVOICING_APPLY`** — optional, default `true`. `false` turns the
  monthly Flex invoicing into a dry run (nothing created in Pennylane, no
  check-in marked).
- **`DIRECT_DEBIT_APPLY`** — optional, default `true`. `false` turns
  `pennylane-direct-debit` into a dry run (it mails what it would switch).
- **`INVITE_API_KEY`** — an API key minted in `/_admin` (API keys) by an
  **admin** account. `flex-signup-validate` sends the coworker invitation
  through the app's own admin endpoint with it, at `BASE_URL`: Sovrium 0.37's
  automations can create a user but not invite one. Without it every
  validation is refused before anything is written. The invitation names the
  key's owner as the inviter; demoting or banning that owner, or revoking the
  key, stops the invitations.
- **`FLEX_SIGNUP_APPLY`** — optional, default `true`. `false` makes « Valider »
  a dry run: the run says which customer it would reuse or create and writes
  nothing.
- **`DEADLINES_SLACK_CHANNEL_ID`** — the channel (`C…`) the Calendrier de
  gestion reminders go to. Required: set it before deploying, and invite the
  bot there.
- **`DEADLINES_APPLY`** — optional, default `true`. `false` turns
  `management-reminders` into a dry run (it logs the messages it would send).
- **`TREASURER_EMAIL`** — optional, default `tresorerie@laplagedigitale.fr`:
  where the payment-matching, direct-debit and Flex invoicing summaries go
  (needs the `SMTP_*` variables).

Two more variables seed the first administrator:

- **`AUTH_ADMIN_EMAIL`** — `contact@laplagedigitale.fr`.
- **`AUTH_ADMIN_PASSWORD`** (`generator: secret`) — generated per app, so a
  review app never shares production's admin credentials. Read it back with
  `scalingo --app <name> env`.

Seeding runs only against a *fresh* database and only when both variables are
set; on later boots it no-ops rather than duplicating or modifying an existing
user. The startup banner confirms it with an `Admin:` line.

> [!NOTE]
> **The site stays public.** Every page except `/espace-membre/*` and `/administration/*` is
> readable without a session; `/espace-membre` admits the `coworker` and `admin`
> roles, `/administration` the `admin` role — and the `editor` role on
> `/administration/contenu/*` and `/administration/compte` only. `allowSignUp` is
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
mandate email itself is sent by Pennylane, not by this app, to the customer's
Pennylane e-mails.)

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
