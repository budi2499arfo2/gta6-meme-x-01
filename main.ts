// Entry program for gta6-meme-x-01: copies POST.json to the output dir.
// The house reads the post itself from X; this file only hands over the URL.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(outDir, { recursive: true });
const src = join(botDir, "POST.json");
const dst = join(outDir, "POST.json");
copyFileSync(src, dst);
// Fail loudly if the handover did not land: a missing or truncated POST.json
// would otherwise be discovered only when the house reads the entry.
if (!existsSync(dst) || !readFileSync(dst).equals(readFileSync(src))) {
  throw new Error(`POST.json handover failed: ${dst} is missing or differs from ${src}`);
}
console.log("copied POST.json to", outDir);
