# Content — build series (live in Notion)

The GroovePush rebuild doubles as a build/education series. The content calendar now
lives in Notion (connector authorized 2026-07-16):

- **Hub page**: https://app.notion.com/p/39f0e740c31c8170bef5cd93bb571fc0
- **Content Calendar database**: https://app.notion.com/e90994ce8f334503996a4c7d362bb45e
  — 13 rows (Block 0–12), one page per block with `Milestone`, `Topic`, `Format`,
  `Status`, `Video Hook`, `Depends On`. Block 0 is marked **Done**; each page's content
  is the full script (hook, talking points, shot list, code to show, deliverable,
  verification).

The files in this folder are the **source** used to populate Notion — keep them in sync
if you edit content directly here, or edit in Notion and this folder becomes historical.

- [`content-calendar.csv`](content-calendar.csv) — flat table mirroring the Notion database.
- [`block-00-script.md`](block-00-script.md) — Block 0's script (also in Notion).

## Season 1 production pipeline (2026-10-22)

YouTube series + Shorts covering both GroovePush and GrooveForge Brain, built in four stages:

- [`01_borrador_claude.md`](01_borrador_claude.md) — technical analysis of both repos + season/Shorts draft.
- [`02_optimizacion_codex.md`](02_optimizacion_codex.md) — retention, titles/thumbnails, master shot list
  (written by Claude in the Codex role: Codex was not available in that session; see
  [`02_prompt_codex.md`](02_prompt_codex.md) to run the real prompt).
- [`BIBLIA_PRODUCCION_FINAL.md`](BIBLIA_PRODUCCION_FINAL.md) — **the master document to record from**: 02 audited
  against the repos and merged with 01.

## Script format (per block)
Each block's script follows the same shape so recording is mechanical:
- **Hook** (first 10 s) · **What we build** · **Talking points** (the concept: MIDI, ADC,
  I2C, …) · **Shot list** (build / code / demo) · **Code to show** · **Deliverable** ·
  **Verification shown on camera**.

## Blocks
See [`../../ROADMAP.md`](../../ROADMAP.md) for the full technical roadmap; each block there
maps 1:1 to a page in the Notion database.
