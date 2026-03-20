import { start } from "sovrium";
import { loadConfig } from "./load-config";

const config = await loadConfig();

await start(config, {
  publicDir: "./public",
});
