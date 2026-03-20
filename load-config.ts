import type { AppConfig } from "sovrium";
import { parse } from "yaml";
import { Glob } from "bun";

async function loadYaml(path: string) {
  return parse(await Bun.file(path).text());
}

async function loadYamlDir(pattern: string) {
  const files: string[] = [];
  for await (const path of new Glob(pattern).scan(".")) {
    files.push(path);
  }
  files.sort();
  const results = await Promise.all(files.map(loadYaml));
  return results;
}

export async function loadConfig(): Promise<AppConfig> {
  const [theme, analytics, fr, en, components, pages] = await Promise.all([
    loadYaml("config/theme.yaml"),
    loadYaml("config/analytics.yaml"),
    loadYaml("config/languages/fr.yaml"),
    loadYaml("config/languages/en.yaml"),
    loadYamlDir("config/components/*.yaml"),
    loadYamlDir("config/pages/*.yaml"),
  ]);

  return {
    name: "la-plage-digitale",
    version: "1.0.0",
    description: "La Plage Digitale — Tiers-lieu de l'innovation à Strasbourg",
    theme,
    languages: {
      default: "fr",
      supported: [
        { code: "fr", locale: "fr-FR", label: "Français", direction: "ltr" as const },
        { code: "en", locale: "en-US", label: "English", direction: "ltr" as const },
      ],
      translations: { fr, en },
    },
    components,
    pages,
    analytics,
  };
}
