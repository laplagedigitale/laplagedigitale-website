# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Three audiences, each on its own surface. When their needs compete, **public visitors come first**.

1. **Public visitors** (primary) — freelancers, founders, innovators, creatives and companies looking for a place to work in Strasbourg. They compare the offers (Fixe, Nomade, Flex, meeting rooms, domiciliation), want to know what the place and the community are like, and decide whether to visit, sign up for a Flex day or contact the team.
2. **Coworkers** — members using the Espace Membre (`/espace-membre/*`) to see their formule, pay and download their Pennylane invoices, set up the Compte Pro direct-debit mandate, check in for Flex days, book or request meeting rooms, and read the practical guide (access, Wi-Fi, printing, kitchen, lockers…). The content is personalised by formule.
3. **The association's admins and editors** — the people who run La Plage, using the Administration (`/administration/*`): Calendrier de gestion, members, Flex sign-ups and check-ins, invoices and payment matching, treasury and forecast, site content. Editors only reach Contenu.

## Product Purpose

La Plage Digitale is a tiers-lieu with a 600 m² coworking space in central Strasbourg. The site does three jobs: make visitors want to join (and tell them how), give coworkers one place to manage their membership instead of the old Notion « Kit du Plagiste » and email threads, and give the association's volunteers and team the tools to run the place (deadlines, billing, cash forecast) without spreadsheets.

Success: a visitor understands the offers and acts (visit, Flex sign-up, contact); a coworker finds an answer or completes a task without asking the team; an admin sees what needs doing and does it in the app.

## Positioning

Run by an association, not a company: a tiers-lieu in the former Coop premises, where the community comes first and the coworking is the heart of the place rather than the whole of it. Meet-ups, sharing and serendipity are the point, not a perk.

## Operating Context

- Open to visitors Monday to Friday, 9:00–17:00; visits are the usual first step.
- Billing, customers, subscriptions and direct debit live in Pennylane (Compte Pro); the site mirrors them and never replaces Pennylane as the record.
- The team coordinates in Slack and Notion; the Calendrier de gestion posts reminders to Slack and can create Notion cards.
- Flex is a day pass: first visit through the public sign-up, admin validation, then self check-in in the Espace Membre and monthly invoicing.
- Association membership exists alongside the coworking formules (one free Flex day a year for association members).

## Capabilities and Constraints

- Built entirely in Sovrium configuration (`app.yaml` + `config/`): components come from Sovrium's closed vocabulary and are styled with utility classes and `design.*` tokens. There is no custom front-end code and no package manager.
- Three locales: French is the source language; English and German are translations through the `$t:` dictionary. Any new copy needs all three.
- Sign-ups are closed (`allowSignUp: false`): accounts are created by admins or by the Flex validation flow.
- Formules: `fixe`, `nomade`, `flex`, `box`, `domiciliation`. Public prices currently quoted: Fixe 275 € HT/month, Nomade 175 €/month, Flex 14 €/day (7 € half day), meeting rooms from 87 € for 4 h, plus domiciliation.
- Pages are `noindex` while the site is pre-launch.

## Brand Commitments

- **Name**: La Plage Digitale, « la Plage » for short; its members are « Plagistes ».
- **Charte graphique 2026** (« 2026-02 charte plage.pdf »): the palette and type in `config/design.yaml` are binding, and so are the logos in `public/brand/` (`logo-couleurs.svg`, `logo-blanc.svg`). Navy leads; orange and amber are fills and accents only, never text on white.
- **Voice**: French first, warm and associative — convivial and community-minded, never corporate SaaS. **Tutoiement**: address the visitor as « tu ».
  - Applied 2026-11: French copy uses « tu » (legal and privacy pages stay neutral), German « du », English a neutral « you ».

## Evidence on Hand

- Real photography of the place, the team and events in `public/images/pages/` (accueil, espace-cowork, les-entreprises, les-formules, nos-activites, nos-cowork, nos-soutiens, qui-sommes-nous, site) and blog images in `public/images/blog/`.
- Real supporters on the Nos soutiens page, real board and team on Qui sommes-nous, real coworker companies on Nos coworkers / Les entreprises.
- The association's founding documents in `public/documents/`: statuts, règlement intérieur associatif, règlement d'utilisation des locaux, charte des valeurs.
- **Never fabricate** coworkers, testimonials, quotes, figures, partners or photos. Use only what the repository or the team provides; ask when something is missing.

## Product Principles

1. **The visitor's decision comes first.** On the public site, every page should help someone understand the place and take the next step: visit, Flex day, contact.
2. **Community over square metres.** Show people, events and the association before desks and amenities.
3. **Self-service for members.** A coworker should get an answer or finish a task in the Espace Membre without writing to the team.
4. **Pennylane is the record.** The app mirrors and acts on billing data; it never invents or contradicts it.
5. **Honest and real.** Real photos, real names, real numbers, or nothing.

## Accessibility & Inclusion

WCAG 2.2 AA is a hard requirement across all three surfaces. The charte's own rule applies: orange and amber are never used as text on white; navy text sits on them.
