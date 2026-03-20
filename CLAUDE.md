## Sovrium Documentation

This project uses [Sovrium](https://sovrium.com), a configuration-driven application platform. The app is defined in `app.yaml` and started via `index.ts`.

### LLMs Documentation References

For complete Sovrium documentation, fetch these files:

- **Full reference**: `https://sovrium.com/llms-full.txt` — Complete docs (~2800 lines) covering schema, components, fields, actions, auth, themes, pages, and more.
- **JSON Schema**: `https://sovrium.com/schema/app.json` — Machine-readable schema for validation and autocompletion.

When working on `app.yaml` or any Sovrium configuration, **always fetch `https://sovrium.com/llms-full.txt`** to get the latest documentation before making changes.

### Key Concepts

- **Config-driven**: The entire app (data models, auth, pages, themes, analytics) is defined in a single YAML file (`app.yaml`).
- **Schema version**: 0.2.11
- **41 field types**, **64 component types**, built-in auth, RBAC permissions, i18n.
- App is started with `sovrium start app.yaml` or programmatically via `import { start } from 'sovrium'`.

### Project Setup

- Runtime: Bun (not Node.js)
- Entry point: `index.ts` — loads `app.yaml` and starts Sovrium
- Static assets: `./public` directory
- Use `bun run index.ts` to start the dev server
- Use `bun install` for dependencies

### CLI Commands

```bash
sovrium start app.yaml          # Start dev server
sovrium start app.yaml --watch  # Start with hot reload
sovrium build app.yaml          # Build static site
sovrium validate app.yaml       # Validate config
sovrium schema                  # Print JSON Schema
```

### Environment Variables

- `DATABASE_URL` — PostgreSQL connection string (required for tables/auth)
- `PORT` — Server port (default: 3000)
- `APP_SCHEMA` — Alternative to file path for config
- `SOVRIUM_BASE_URL` — Base URL for static builds
- `SOVRIUM_DEPLOYMENT` — Deployment target (e.g., `github-pages`)
- `SOVRIUM_GENERATE_SITEMAP` — Generate sitemap.xml
- `SOVRIUM_GENERATE_ROBOTS` — Generate robots.txt
