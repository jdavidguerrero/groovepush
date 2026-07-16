# Processor — Task List

> Derived from: `processor.md` (SPEC-PROC) + `../../ROADMAP.md`.
> Do tasks top to bottom, one at a time. Check the box only with verification evidence.

## Block 0 — Source of truth (P0 unblocker)

| Task | Satisfies | Agent | Verify by | Done |
|------|-----------|-------|-----------|:----:|
| T-B0-1 — Reconcile encoder pin map (single conflict-free map in `PIN_MAP.md` + `Config.h`) | G-P1 / SPEC-PROC C-3 | firmware-engineer | `pio run -e teensy41` **SUCCESS** (24 s, 2026-07-16); one coherent map | ☑ |
| T-B0-2 — Decide NeoTrellis link = I2C (0x2E/0x2F); park UART-M4 path | G-P2 | hardware-engineer | `PIN_MAP.md` + `Config.h` state I2C authoritative; UART-M4 marked deprecated | ☑ |
| T-B0-3 — Remove orphan `include/Config.h` (dead, contradictory values) | G-P3 | firmware-engineer | nothing includes bare `Config.h`; `pio run -e teensy41` SUCCESS | ☑ |
| T-B0-4 — Protoboard wiring diagram + powered bench (Teensy LED blinks) | G-H(bench) | industrial-designer | photo of powered protoboard; onboard LED blink sketch runs | ☐ |

**Evidence (T-B0-1/3)**: `teensy41 SUCCESS 00:00:24` — FLASH 72976 B, RAM1 vars 22720 B.

## Block 1 — MIDI 101 (next)

| Task | Satisfies | Agent | Verify by | Done |
|------|-----------|-------|-----------|:----:|
| T-B1-1 — One button → USB-MIDI note-on/off | R-PROC-1 | firmware-engineer | Ableton MIDI monitor shows the note | ☐ |
| T-B1-2 — Basic velocity curve | R-PROC-1 | firmware-engineer | different velocity by force/timing | ☐ |
| T-B1-3 — Measure pad→note latency | R-PROC-1 (AC-1) | qa-hardware-test | logged < 5 ms | ☐ |

> Blocks 2–12: generate their task rows with `/tasks processor` (and `/tasks gui`) as each
> block starts. Full plan in `../../ROADMAP.md`.

## Notes / decisions while implementing
- Authoritative pin map lives in `apps/processor/PIN_MAP.md`; `Config.h` mirrors it.
- I2C bus = default `Wire` (pins 18/19); buttons on 2× MCP23017 free the analog pins.
- Encoders avoid Serial1 (0/1 → RPi), I2C (18/19), faders (14–17), piezo/IR (20–25).
