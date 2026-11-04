---
target: Administration space
total_score: 25
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 4
target_identity: "file:/Users/thomasjeanneau/Codes/laplagedigitale-website-admin-ux/config/pages/admin.yaml"
target_fingerprint: "sha256:12191dbad1959b00ad620b7b7ef2cf56e90a34e6c4f499ff30561d50ae9be3f1"
target_path: /Users/thomasjeanneau/Codes/laplagedigitale-website-admin-ux/config/pages/admin.yaml
timestamp: 2026-11-04T11-27-55Z
slug: config-pages-admin-yaml
---
# Critique — Administration de l'association (/administration/*)

Method: dual-agent (A: design review · B: detector + browser). Rendered HTML scanned (the detector cannot read Sovrium YAML).

## Design Health Score — 25/40 (Acceptable)
| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 2 | Uncomputed KPIs shown as a red 0 / 0,00 €; no « dernière synchro »; « rechargez la page » after Fait |
| 2 | Match system / real world | 3 | Raw labels leak (« Pennylane » column = match_status, raw customer id) |
| 3 | User control & freedom | 2 | « + Nouvelle ligne » on members, flex_signups, posts bypasses the flows |
| 4 | Consistency & standards | 2 | Primary pill magenta on some pages, orange on others; filter-bar/export only on 2 pages; two « Tableau de bord » |
| 5 | Error prevention | 3 | Auto-save deadline form still submits a stale due_date |
| 6 | Recognition vs recall | 3 | 22 sidebar entries, Compte below the fold; Flex actions off-screen (17 columns) |
| 7 | Flexibility & efficiency | 2 | No filters/export on Membres, Factures, Rapprochements; KPI tiles not links |
| 8 | Aesthetic & minimalist | 3 | Calm; engine table footer on every table; long intros |
| 9 | Error recovery | 2 | Generic toasts; engine errors name raw tables (« Management Deadlines : non disponible ») |
| 10 | Help & documentation | 3 | Good intros/descriptions; nothing on Recalculer / sync |

## Priority issues
- [P1] Empty/uncomputed values read as alarms (admin.yaml, admin-finances-forecast.yaml « Autonomie (mois) » red 0). Gate on a computed baseline scenario, else a note linking to Prévisionnel.
- [P1] Hover makes primary CTA text unreadable: engine hover colour overrides text-white → 2.4:1 on magenta, 4.3:1 on orange. Add explicit hover text colour.
- [P1] Rogue row creation: add readOnly: true to members (admin-members.yaml:63), flex_signups, posts tables.
- [P1] Inscriptions Flex: 17 columns, Valider/Refuser off-screen. Cut to 7 columns, « À traiter » / « Toutes » tabs, detail page /inscriptions-flex/:id.
- [P2] Dashboard is 15 equal counters. Lead with an « À faire » block of link tiles (échéances en retard, Flex à valider, demandes, rapprochements, points comptables).
- [P2] One action-colour rule: orange = create/primary, navy = act on a record, outline = navigation.
- [P2] Sidebar past scannability: regroup (see IA) and pin Compte/Console/Voir le site in the footer.

## Persona red flags
- Volunteer board member (monthly): lands on zeros and a red 0; two « Tableau de bord »; jargon (lettrée, ligne, point comptable); can't find Compte.
- Mathieu (daily ops): no overdue flag in the Calendrier list; no formule filter on Membres; horizontal scroll to validate Flex; no last-sync time.
- Treasurer: Trésorerie/Prévisionnel empty until someone presses Recalculer, with nothing saying so; « Compte »/« Ligne » show « — »; no export on « Sans catégorie », unexplained.

## Minor
check-cross on Calendrier « Active »; admin-member formules form without autoSave; 11px text-xs notes; unify search size h-9 w-full sm:w-72 in a role=toolbar; glyph-only ✓/✗ cells and unlabelled clickable rows (engine); Transactions tabs wrap at 390px.

## Questions
- Should /administration be a to-do list rather than a list of numbers?
- Does a monthly board member need the same 22-entry sidebar as Mathieu?
- Should every Pennylane mirror page show its last sync and one « Ouvrir dans Pennylane »?
