---
name: La Plage Digitale
description: Tiers-lieu et coworking à Strasbourg — the 2026 charte graphique as built in Sovrium
colors:
  ink-navy: "#273a61"
  ink-navy-deep: "#1c2b4a"
  ink-navy-300: "#5d6a88"
  ink-navy-200: "#929caf"
  ink-navy-100: "#e4e6eb"
  seaside-blue: "#6290bc"
  seaside-blue-300: "#8fb2d6"
  seaside-blue-200: "#b5cce4"
  seaside-blue-100: "#e3ecf5"
  sun-orange: "#f08137"
  sun-orange-300: "#f6a66b"
  sun-orange-200: "#f9c296"
  sun-orange-100: "#fde3cc"
  plage-magenta: "#cf1769"
  plage-magenta-300: "#e0538f"
  plage-magenta-200: "#ec8bb3"
  plage-magenta-100: "#f9dbe8"
  forest: "#455b32"
  sage: "#92aa58"
  amber: "#f9af25"
  coral-red: "#e83d3b"
  paper: "#fbf8f4"
  sand: "#f4ede4"
  card-white: "#ffffff"
typography:
  display:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "4.5rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "3.25rem"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.025em"
  headline-section:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  title:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.25
  title-small:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.35
  lead:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  body-small:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "0.9375rem"
    lineHeight: 1.55
  caption:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "0.8125rem"
    lineHeight: 1.4
  label:
    fontFamily: "SUSE, system-ui, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.16em"
rounded:
  tile: "1rem"
  panel: "1.5rem"
  full: "9999px"
spacing:
  gutter: "1rem"
  gutter-sm: "1.5rem"
  gutter-lg: "2rem"
  card: "1.5rem"
  card-lg: "2rem"
  section: "5rem"
  section-sm: "6rem"
  container: "80rem"
components:
  button-primary:
    backgroundColor: "{colors.sun-orange}"
    textColor: "{colors.ink-navy}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-primary-hover:
    backgroundColor: "{colors.sun-orange-300}"
    textColor: "{colors.ink-navy}"
  button-navy:
    backgroundColor: "{colors.ink-navy}"
    textColor: "{colors.card-white}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-navy-hover:
    backgroundColor: "{colors.ink-navy-deep}"
  button-outline-inverse:
    backgroundColor: "transparent"
    textColor: "{colors.card-white}"
    rounded: "{rounded.full}"
    padding: "12px 24px"
  button-outline-inverse-hover:
    backgroundColor: "{colors.card-white}"
    textColor: "{colors.ink-navy}"
  button-magenta:
    backgroundColor: "{colors.plage-magenta}"
    textColor: "{colors.card-white}"
    rounded: "{rounded.full}"
    padding: "10px 20px"
  button-magenta-hover:
    backgroundColor: "{colors.plage-magenta-300}"
  chip:
    backgroundColor: "{colors.seaside-blue-100}"
    textColor: "{colors.ink-navy}"
    rounded: "{rounded.full}"
    padding: "4px 12px"
  card-pinned:
    backgroundColor: "{colors.card-white}"
    textColor: "{colors.ink-navy}"
    rounded: "{rounded.panel}"
    padding: "24px"
  card-panel:
    backgroundColor: "{colors.card-white}"
    textColor: "{colors.ink-navy}"
    rounded: "{rounded.panel}"
    padding: "32px"
  note:
    backgroundColor: "{colors.seaside-blue-100}"
    textColor: "{colors.ink-navy}"
    rounded: "{rounded.panel}"
    padding: "12px"
  site-header:
    backgroundColor: "{colors.card-white}"
    textColor: "{colors.ink-navy}"
    height: "80px"
  admin-sidebar:
    backgroundColor: "{colors.ink-navy}"
    textColor: "{colors.ink-navy-100}"
    width: "256px"
---

# Design System: La Plage Digitale

The tokens above mirror `config/design.yaml`, which is the source of truth: Sovrium compiles it into the stylesheet at boot. Where this file and `design.yaml` disagree, `design.yaml` wins and this file is stale. The frontmatter keys are descriptive names; the Sovrium token each one maps to is the plain name (`ink-navy` → `navy`, `seaside-blue-100` → `blue-100`, `sun-orange` → `orange`, `plage-magenta` → `magenta`, `paper` → `background`, `card-white` → `white`/`surface`). The markup writes the Sovrium names (`bg-navy`, `text-magenta`, `rounded-panel`).

## Overview

**Creative North Star: "The Neighbourhood Noticeboard"**

La Plage looks like the association's noticeboard: white cards pinned on a warm sand-and-paper wall, each with a colour tab along its top edge, headlines set in heavy, tight SUSE capitals like the signage on the building. People, events and offers are pinned up front. Nothing here is a product dashboard; it is a place where a community posts what is going on and how to join in.

The palette is the 2026 charte: ink navy leads and carries almost all text, the dark hero bands and the Administration's sidebar. Sun orange is the call to act, plage magenta the community's accent, seaside blue the calm one for tags, notes and secondary links. The ground is never pure white: paper (`#fbf8f4`) for pages, sand (`#f4ede4`) for alternating bands and the Espace Membre sidebar, so the white cards read as pinned sheets. Depth is soft and friendly: generous 1.5rem corners, pills for every action, navy-tinted shadows that lift a card a few pixels on hover.

The two signed-in spaces keep the same materials at a quieter volume. The Espace Membre is the noticeboard's back room (sand sidebar, the same cards); the Administration puts the board on a navy wall (navy sidebar, orange marker for the active space). Both are tools first: the colour tabs and pills stay, the display type does not.

It is not corporate SaaS (no cold grey dashboards, gradient heroes or startup clichés) and not a generic coworking chain (no anonymous plants-and-laptops imagery, no black-and-white-with-one-accent look).

**Key Characteristics:**
- Warm ground (paper, sand), white pinned cards, ink navy text.
- One face, SUSE, from light body text to heavy signage capitals.
- Pills for every action and tag; 1.5rem corners for every card.
- A coloured top edge says which offer or room a card belongs to.
- Soft navy-tinted shadows that lift on hover.
- Real photographs of the place and its people, never stock.

## Colors

A warm, sunny charte anchored in a deep ink navy: three bright brand colours, each with lighter tints, over sand and paper.

### Primary
- **Ink Navy** (`ink-navy`): the voice of the system. All headings and body text, the hero and CTA bands, the Administration sidebar, the dark button. Its deep shade (`ink-navy-deep`) is the hover and the active sidebar entry on navy. `ink-navy-300` is muted text (captions, meta), `ink-navy-200` a quiet label on navy, `ink-navy-100` borders, dividers and the light text on navy.

### Secondary
- **Sun Orange** (`sun-orange`): the call to act. The primary button fill, the eyebrow over a navy hero, the Administration's « Administration » marker, the Flex offer's tab. Fills and accents only. `sun-orange-300` is its hover; `sun-orange-100` a warm note background (with an amber border for warnings).
- **Seaside Blue** (`seaside-blue`): the calm accent. The Nomade tab, the focus ring, chart series 1. Its 100 tint is the system's default chip, tag and note background.

### Tertiary
- **Plage Magenta** (`plage-magenta`): the community's colour, read from the logo. Highlighted words, community and event accents, the meeting-room tab, the « Rejoindre » button, the hover of the light chips on navy. It holds white text and works as text on white.

### Palette secondaire
- **Forest** (`forest`) and **Sage** (`sage`): the green pair. Sage marks success (paid, active mandate).
- **Amber** (`amber`): warnings and attention, as a border or fill, never text.
- **Coral Red** (`coral-red`): errors and destructive actions.

### Neutral
- **Paper** (`paper`): the page ground.
- **Sand** (`sand`): alternating section bands, the Espace Membre sidebar, the neutral hover of a blue chip.
- **Card White** (`card-white`): cards, the sticky header, panels.

### Named Rules
**The Navy Voice Rule.** Text is ink navy (or its 300 shade when muted). Brand colours carry text only where they pass AA: magenta on white, white on magenta or navy.

**The Orange Is a Fill Rule.** Orange and amber are never text on white or paper. Navy text sits on them. (The charte's own rule.)

**The Colour Tab Rule.** A card's 4px top edge carries its offer: Fixe navy, Nomade blue, Flex orange, Salles de réunion magenta. Keep the mapping wherever an offer appears.

## Typography

**Display Font:** SUSE (with `system-ui, sans-serif`), self-hosted as a variable font, 300–800, from `/fonts/fonts.css`
**Body Font:** the same SUSE

**Character:** one geometric sans plays every role. Its heavy weights, set tight and large, are the building's signage; at 400 with loose leading it reads as friendly body text.

### Hierarchy
- **Display** (800, 4.5rem, 1, −0.03em): the home hero only, from `sm` up; below that the hero drops to Headline.
- **Headline** (800, 3.25rem, 1.05, −0.025em): page titles (h1).
- **Headline Section** (700, 2.5rem, 1.1, −0.02em): section titles (h2).
- **Title** (700, 1.5rem, 1.25): card and block titles (h3).
- **Title Small** (600, 1.125rem, 1.35): offer card titles, small headings (h4).
- **Lead** (400, 1.25rem, 1.55): the paragraph under a page or section title, held to `max-w-2xl` (42rem).
- **Body** (400, 1rem, 1.65): running text, held to `max-w-3xl` (48rem) at most.
- **Body Small** (0.9375rem, 1.55) and **Caption** (0.8125rem, 1.4): card text, meta, chips, footnotes.
- **Label / Overline** (700, 0.8125rem, 1.2, 0.16em, uppercase): the eyebrow above every section title, and the sidebar group headings.

The markup applies a step with arbitrary-value utilities (`[font-size:var(--text-h2)] [line-height:var(--text-h2--line-height)] …`): the steps are CSS variables, not Tailwind size classes.

### Named Rules
**The Eyebrow Rule.** Every public section opens with an overline eyebrow, then its Headline Section title, then a Lead. The eyebrow is orange on navy, magenta or navy on light grounds.

**The Signage Is Public Rule.** Display and the 800 weights belong to the public site. The two spaces start at Headline and mostly work at Title and below.

## Layout

- **Container:** `max-w-7xl` (80rem) centred, with a gutter of 1rem, 1.5rem from `sm`, 2rem from `lg`. Text blocks narrow to `max-w-3xl` (48rem) or `max-w-2xl` (42rem).
- **Section rhythm:** each public section is a full-width band with `py-20` (5rem), `py-24` (6rem) from `sm`. Bands alternate paper, sand and white, with a navy band for the hero and the closing call to action.
- **Grids:** offers, rooms, people and supporters sit in responsive card grids (1 column, 2 from `sm`/`md`, 3–4 from `lg`). Supporter logos are square tiles.
- **Header:** sticky, 80px tall, translucent white with a blur and a navy-100 bottom border; the navigation menu shows from `lg`, a sheet below.
- **App shells:** the Espace Membre and the Administration put a sidebar beside the page's `<main>`. From `lg` the sidebar is a 16rem (256px) full-height column whose header and footer are pinned and only the middle scrolls; below `lg` it collapses into a top bar with a pill trigger.
- **Breakpoints:** `sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px.

## Elevation & Depth

Layered and soft. White cards float on the warm ground with navy-tinted shadows (never grey or black), and lift on hover: the shadow steps from md to lg and the card rises 4px (`hover:-translate-y-1`). Flat colour bands (navy, sand, white) do the large-scale layering; shadows are for things you can pick up.

### Shadow Vocabulary
- **Resting hairline** (`sm`, `0 1px 2px 0 rgb(39 58 97 / 0.06)`): small controls and inset tiles.
- **Pinned card** (`md`, `0 8px 24px -8px rgb(39 58 97 / 0.18)`): every card at rest.
- **Lifted card** (`lg`, `0 24px 48px -16px rgb(39 58 97 / 0.28)`): a card under the pointer, a featured panel.

### Named Rules
**The Navy Shadow Rule.** Shadows are tinted with ink navy (`rgb(39 58 97 / …)`). A neutral black shadow does not belong here.

**The Lift Means Link Rule.** A card that lifts on hover is clickable as a whole. A static card keeps its md shadow.

## Shapes

Soft and round, in three steps:
- **Pill** (`full`): every button, chip, tag, badge, language and filter control, the sidebar trigger.
- **Panel** (`panel`, 1.5rem): every card, panel, note and large image.
- **Tile** (`tile`, 1rem): small inset surfaces (a logo plate, a list item inside a note).

Portraits are circles with a 4px orange-100 ring. The one hard edge in the system is the 4px coloured top border on offer and room cards, cut flat by the card's `overflow-hidden`.

The engine's own components (shadcn since Sovrium 0.38) round on their own steps (`rounded-lg` buttons, `rounded-xl` cards). That is why the charte's corners carry their own names (`tile`, `panel`): redefining `sm`…`xl` turned every engine field and card into a pill.

## Components

### Buttons
Friendly, confident pills with bold labels.
- **Shape:** pill (`rounded-full`), bold label, `px-6 py-3` (`px-5 py-2.5` and `text-sm` in compact places).
- **Primary (orange):** sun orange fill, navy label; hover to orange-300. The main call to act on every surface.
- **Navy:** navy fill, white label; hover to navy-deep. The call to act on light ground when orange is already used nearby.
- **Outline inverse:** 2px white border, white label, on navy; hover fills white with a navy label. The secondary choice in a navy hero.
- **Magenta:** magenta fill, white label; hover to magenta-300. « Rejoindre », community actions.
- **Hover / Focus:** colour transition (`transition-colors`). Focus uses the engine's ring in seaside blue.

### Chips
- **Style:** pill, seaside-blue-100 fill, navy label in caption or `text-sm` semibold, `px-3 py-1`.
- **Link chip:** hovers to sand. On navy, a translucent white chip (`bg-white/10`, navy-100 label) hovers to magenta with a white label.

### Cards / Containers
- **Pinned card:** white, 1.5rem corners, md shadow, `p-6` (`p-8` from `sm` on panels). Clickable ones lift to lg and rise 4px.
- **Offer / room card:** a pinned card with a 4px coloured top edge (the Colour Tab Rule) and `overflow-hidden` so photos run edge to edge under it.
- **Logo tile:** a square white panel, centred logo, `p-4`/`p-5`, lifts on hover.
- **Note:** a seaside-blue-100 panel with navy `text-sm` and 1.5rem corners; the warning variant is orange-100 with an amber border.

### Inputs / Fields
The engine's shadcn fields, re-coloured by the tokens: white field, ink-navy-200 (`input`) border, navy text, seaside blue focus ring, coral red error. Forms sit inside a pinned card.

### Navigation
- **Site header:** sticky white bar, logo in colour (48px tall) on the left, navigation menu at `text-md` in navy, language switcher and a pill call to act on the right.
- **Espace Membre sidebar:** on sand, navy entries, overline group headings, the current page in white with semibold text.
- **Administration sidebar:** on navy, white logo, orange « Administration » overline, navy-100 entries hovering to navy-deep, the current page navy-deep in white semibold; from `lg` a pinned footer with the account links and, for an admin who is also a coworker, a white-outlined « Mon Espace Membre → » pill. See Administration (Operate).
- **Footer:** a navy band (navy-100 text) under the charte stripe, with the white logo and four link columns from `lg`.

### Hero band (signature)
A full-width navy section: orange overline eyebrow, a white Display/Headline title held to `max-w-4xl`, a navy-100 Lead, then a row of pills (orange primary, then outline inverse). Beside it, a real photograph of the place pinned like a print: a white panel (`p-3`, `p-5` from `sm`, md shadow) holding the photo with tile corners, over an orange panel offset 12px (20px from `sm`) down and to the right.

### Charte stripe (signature)
An 8px band at the top of the footer, cut in four equal blocks: seaside blue, plage magenta, sun orange, sage. It is the charte's colour sequence; use it as a divider at the edge of the site, not as decoration inside content.

## Administration (Operate)

The Administration is a tool for a few volunteers. Each page answers one question: what is waiting, and where do I act on it? New domains (Lieu, Communauté › Contacts & adhésions, Gouvernance) copy the four patterns below and do not invent their own. Markup is Sovrium YAML; the class strings below are the ones the pages ship with.

### Shell and page head
- **Shell:** a `flex` with `min-h-screen flex flex-col lg:flex-row bg-background` holds `component: admin-nav` and a `section` with `flex-1 min-w-0 px-4 py-8 sm:px-8 lg:px-12 lg:py-10 space-y-8` (`space-y-12` on the dashboard, `space-y-6` on a form page).
- **Head:** h1 `text-3xl font-bold text-navy`, intro `text-text-muted mt-2 max-w-2xl`, and the page's primary action beside them (`flex flex-col sm:flex-row sm:items-end justify-between gap-4`, button `self-start sm:self-auto`). A section title (h2) is `text-xl font-semibold text-navy`.

### Sidebar IA
- **Groups, in order:** Pilotage (Tableau de bord, Calendrier, Demandes), Communauté (Membres, Inscriptions Flex), Finances, Contenu. A new domain gets its own group: **Lieu** between Communauté and Finances, **Gouvernance** after Finances. Each entry is a place where a queue gets worked, not a table.
- **Compte** (Mon compte, Console Sovrium, Voir le site) is a sidebar group below `lg` only (`lg:[&_[data-sidebar-group=Compte]]:hidden`). From `lg` up the same links sit in the pinned footer (`rounded-lg px-3 py-2 text-navy-100 hover:text-white hover:bg-navy-700`), above the white-outlined « Mon Espace Membre → » pill.
- **On navy:** group labels `navy-150` (7.0:1, because `navy-200` is 4.1:1), entries `navy-100`, hover and current entry `navy-700` with white text (the current one semibold), icons `navy-200`.
- **One entry, many pages:** a section with several pages gets ONE sidebar entry on its route prefix (`activeMatch: prefix`), plus a pill sub-nav at the top of each page: a `nav` with the entry's `aria-label` and `flex flex-wrap gap-2 -mt-4`. Every pill is `inline-flex items-center min-h-10 px-4 rounded-full text-sm font-semibold transition-colors`. The current page is the navy pill with `aria-current: page`; the others are outline pills. Copy `admin-finances-transactions.yaml` (Opérations) or `admin-finances-invoices.yaml` (Facturation). An address that moves gets a redirect in `config/redirects.yaml`.

### Actions
**The Three Pills Rule.** A pill's colour says what it does. All three share `inline-flex items-center px-5 py-2.5 rounded-full text-sm focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-navy transition-colors`.
- **Orange creates, or is the page's one primary action:** `font-bold text-navy-700 hover:text-navy-700 bg-orange hover:bg-orange-300`. The label is navy-700 because that is 5.3:1 on orange; plain navy is 4.24:1. Use at most one per page (« + Nouvelle échéance » in `admin-calendar.yaml`, the invitation in `admin-members.yaml`).
- **Navy acts on this record:** `font-bold text-white hover:text-white bg-navy hover:bg-navy-700` (« Marquer comme fait » in `admin-calendar-deadline.yaml`, « Valider » in `admin-flex-signup.yaml`).
- **Outline navigates, or is the secondary choice:** `font-semibold text-navy hover:text-navy bg-white border border-navy-200 hover:bg-navy-100` (« Voir le prévisionnel → » in `admin-finances-treasury.yaml`, « Refuser »).
- **Row actions** inside a table use the engine's `type: actions` (`outline`, `ghost`, `destructive`), not pills.

**The Explicit Hover Text Rule.** Every pill sets its hover text colour explicitly (`hover:text-white`, `hover:text-navy`, `hover:text-navy-700`). Without it, the engine's link hover colour lands on the label at 2.4:1.

### Pattern A: list
Copy `admin-members.yaml` (one table) or `admin-finances-transactions.yaml` (tabs).
- **Toolbar:** the table sits in a card (`p-4 sm:p-6`). Above it goes a `div` with `role: toolbar`, `aria-label: Outils du tableau` and `mb-4 flex flex-wrap items-center gap-2`. It holds a `search-input` (`h-9 w-full sm:w-72`, with an `aria-label`), a `filter-bar` (`fieldsFrom`), and « Exporter en CSV » (`variant: outline`, `size: sm`, `sm:ml-auto`). The shared-filter channel is the page name.
- **Tables are `readOnly: true`,** so the engine adds no « Nouvel enregistrement » button. To create, use the orange pill in the page head.
- **Queues are tabs with an address:** `defaultTab: $query.onglet` plus a `query.onglet` enum, so the dashboard can link straight to a tab. Where a queue exists, « À traiter » (`a-traiter`) comes first, then « Toutes » (`admin-flex-signups.yaml`, `admin-demandes.yaml`).
- **Seven columns at most:** only what is needed to decide. The rest goes on the detail page, which a row click opens (`onRowClick: { type: navigate, path: /administration/<x>/$record.id }`; a Pennylane mirror opens its source in a new tab instead).
- **Empty messages teach.** An `emptyMessage` says what the empty state means or what will fill it (« Aucune échéance pour le moment : ajoutez la première avec « Nouvelle échéance ». »).

### Pattern B: detail
Copy `admin-flex-signup.yaml` (read, then decide) or `admin-calendar-deadline.yaml` (edit in place).
- **Binding:** the page binds `dataSource: { table, mode: single, param: id }` on an `:id` route.
- **Back link first:** `← <Liste>` with `inline-flex items-center min-h-11 text-sm text-text-muted hover:text-navy`.
- **Head row:** `flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4`. On the left, the record's name as h1 over a meta row (`flex flex-wrap items-center gap-3 mt-2 text-text-muted`: the date in `font-semibold text-navy`, the status as a chip, `inline-flex px-3 py-1 rounded-full text-sm font-semibold text-navy bg-blue-100`). On the right, the actions.
- **Actions that need `$record.id`** sit in a `list` bound to the row: `id eq $param.id` plus the state they apply to, `limit: 1`, `hideWhenEmpty`. A button fills `$record.id` only from a list item, and the state filter removes the buttons once the decision is made.
- **Body:** a grid of cards, `grid grid-cols-1 xl:grid-cols-2 gap-6 items-start` (or `xl:grid-cols-3` with an `autoSave` form spanning two). Each card is `p-4 sm:p-6 space-y-4` with an h2, then label/value rows: `grid grid-cols-1 sm:grid-cols-[10rem_1fr] gap-x-4 gap-y-3 text-sm`, with the label in `text-text-muted` and the value a `record-field` in `text-navy`.

### Pattern C: new record
Copy `admin-calendar-new.yaml`. The route is `<liste>/nouvelle` (or `nouveau`), `$ref`'d in `app.yaml` before the `:id` page. The page is the back link, then one card (`p-6 sm:p-8 max-w-2xl`) holding a declared form (`formRef`, `headingLevel: h1`) that creates the row.

### Pattern D: dashboard
Copy `config/pages/admin.yaml`.
- **« À faire » comes first:** one `kpi` per queue a person works (`kpiAggregate: count`), in `grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4`. Each tile is wrapped in a link, with an `aria-label`, to where that queue is worked (to the right tab through `?onglet=`): `block rounded-panel transition duration-200 ease-out hover:-translate-y-1 hover:shadow-lg focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-navy [&>*]:h-full` (the Lift Means Link Rule). `thresholds: [{ value: 0, color: green }, { value: 1, color: yellow }]`: an empty queue is green, a waiting one yellow, never red.
- **Then sections:** an h2 with « Voir … → » on the right (`flex items-center justify-between gap-4`; the link is `inline-flex items-center min-h-11 text-sm font-semibold text-navy underline decoration-blue underline-offset-4 hover:decoration-navy`), and the content in a card. The « Chiffres » tiles are there to watch, so they are not links.

**The No Red Zero Rule.** Show a figure an automation computes through a `list` bound to its computed row (`computed_at isNotEmpty`, `limit: 1`). Its `listDisplay.emptyMessage` says what to run. A KPI over no row reads 0 in red, which says the association is broke when the figure simply hasn't been computed yet.

## Do's and Don'ts

### Do:
- **Do** write colours, corners and type through the tokens in `config/design.yaml` (`bg-navy`, `rounded-panel`, `var(--text-h2)`), never as raw hex or pixel values in the markup.
- **Do** set every action and tag as a pill, and every card as a 1.5rem panel.
- **Do** keep the offer colours: Fixe navy, Nomade blue, Flex orange, Salles de réunion magenta.
- **Do** open public sections with eyebrow, title, lead, and alternate the band grounds (paper, sand, white, navy).
- **Do** use real photographs of La Plage, its rooms and its people (`public/images/`).
- **Do** keep text at WCAG AA: navy on paper is 10.6:1, navy-300 on paper 5.1:1, magenta on white 5.3:1.

### Don't:
- **Don't** set orange or amber text on white or paper (the charte's rule).
- **Don't** use seaside blue as text on white: it is 3.4:1. The small semibold `text-blue` links (partner and venue names on the public pages) do it today and fail AA; they should move to navy or magenta. The header's « Espace membre » link turning orange on hover breaks the orange rule the same way.
- **Don't** add more navy-on-orange at body size: it is 4.24:1, just under AA. The orange pills use it today with 16px bold labels, and so does the orange 13px eyebrow on navy; both need orange-300 (5.7:1 with navy) or a larger label to pass.
- **Don't** rely on the ink-navy-200 field border alone to show a field: it is 2.8:1 against white, under the 3:1 non-text minimum.
- **Don't** use grey or black shadows, square corners on cards, or a pure white page ground.
- **Don't** redefine `radius` `sm`…`xl` in `design.yaml`: the engine's components would all turn into pills.
- **Don't** drift into corporate SaaS (cold grey dashboards, gradient heroes, startup clichés) or a generic coworking chain look (anonymous plants-and-laptops stock, black and white with a single accent).
