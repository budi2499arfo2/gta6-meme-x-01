// Entry program for gta6-meme-x-01: copies POST.json to the output dir.
// The house reads the post itself from X; this file only hands over the URL.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
console.log("copied POST.json to", outDir);
