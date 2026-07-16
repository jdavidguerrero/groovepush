# Content — build series (Notion-ready)

The GroovePush rebuild doubles as a build/education series. This folder holds the
**Notion-ready** content plan so you can import it when you connect the Notion connector.

## How to set it up in Notion
1. Create a **database** called "GroovePush Content Calendar".
2. **Import** [`content-calendar.csv`](content-calendar.csv) into it (Notion → Import → CSV).
   Suggested property types: `Block` (Title), `Status` (Select: Not started / Ready to
   record / Recorded / Edited / Published), `Format` (Multi-select), `Depends On` (Relation
   to same DB), `Video` (Text/URL).
3. For each row, open the page and paste the matching **script** from
   `block-NN-script.md` (Block 0's is provided; later blocks get a script as they start).
4. Optionally add views: **Board by Status** (kanban) and **Timeline by Block**.

> When the Notion connector is authorized (claude.ai connector settings), I can create the
> database + pages directly instead of the CSV import.

## Script format (per block)
Each `block-NN-script.md` follows the same shape so recording is mechanical:
- **Hook** (first 10 s) · **What we build** · **Talking points** (the concept: MIDI, ADC,
  I2C, …) · **Shot list** (build / code / demo) · **Code to show** · **Deliverable** ·
  **Verification shown on camera**.

## Blocks
See [`../../ROADMAP.md`](../../ROADMAP.md) for the full technical roadmap; each block there
maps 1:1 to a row in the calendar and a script here.

| Block | Script |
|---|---|
| 0 — Source of truth + bench | [`block-00-script.md`](block-00-script.md) ✅ |
| 1–12 | generated as each block starts |
