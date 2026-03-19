import { start } from "sovrium";
import { parse } from "yaml";

const config = parse(await Bun.file("app.yaml").text());

await start(config, {
  publicDir: "./public",
});
