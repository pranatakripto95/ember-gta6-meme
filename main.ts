// Ember GTA 6 Meme — entry program (Node 22, standard library only).
//
// The entry is the X post itself: the house reads the post from X (its
// first picture, the meme, and its text) and hands that to the judge.
// Nothing this program writes about the post is judged, so all it does
// is copy POST.json from the repository root into the output directory,
// where the gate reads it.
//
// Run locally the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
try {
  copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
} catch (err) {
  console.error(`could not copy POST.json from ${botDir}: ${err.message}`);
  process.exit(1);
}
