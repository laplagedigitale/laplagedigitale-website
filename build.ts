import { build } from "sovrium";
import { loadConfig } from "./load-config";

const config = await loadConfig();

const result = await build(config, {
  outputDir: "./dist",
  publicDir: "./public",
  deployment: "github-pages",
  generateSitemap: false,
  generateRobotsTxt: false,
});

console.log(`Built ${result.files.length} files to ${result.outputDir}`);
