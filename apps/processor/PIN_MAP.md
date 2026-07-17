# Teensy 4.1 — Authoritative Pin Map (single source of truth)

> **This file is the source of truth for pin assignments.** `include/shared/Config.h`
> mirrors it. `PIN_DISTRIBUTION.md` is kept for power/LED/protocol notes but its old pin
> table is **superseded here** (see Block 0 / gap G-P1, G-P2, G-P3 in `../../GAPS_AND_IMPROVEMENTS.md`).
> Reconciled 2026-07-16 during the from-scratch rebuild. Wire the protoboard to **this** map.

## Phase 1 scope (protoboard, current)
Building **now**: NeoTrellis (I2C), 8× encoders (EC11 with integrated switch), 4× faders,
2× MCP23017 (8 encoder switches + 4 populated transport buttons). **Not** in this phase:
- ❌ Piezo, IR/theremin — **removed from this device** (future standalone e-drum module).
- ❌ Capacitive touch buttons — **removed**, replaced by MCP23017 pushbuttons.
- ⏸️ WS2812B LED strip — **deferred to PCB** (parts on hand are SMD, not protoboard-friendly).
Their pin reservations below are kept so the KiCad PCB design (Fase 3) stays valid, but
nothing is wired for these on the bench right now.

## Why the old tables were wrong
- Old docs put I2C on pins **4/5** — those are **not** a hardware I2C bus on Teensy 4.1.
  The firmware already uses the default `Wire` bus = **pins 18 (SDA) / 19 (SCL)**.
- Old encoder pins overlapped the IR analog pins (24/25) and used non-existent/awkward
  pins (33/34 in `ENCODER_PINS_EXPANSION`).
- Buttons are handled by **2× MCP23017 over I2C**, so they need **no** Teensy GPIO
  (frees the analog pins the old map double-booked as "capacitive buttons").

## Reserved / fixed
| Function | Teensy pin(s) | Notes |
|---|---|---|
| Serial1 → Raspberry Pi (GUI) | RX1 = **0**, TX1 = **1** | hardware UART; do not reuse |
| Built-in LED | **13** | status |
| I2C `Wire` (NeoTrellis + MCP23017) | SDA = **18**, SCL = **19** | 4.7 kΩ pull-ups; A4/A5 |
| USB | native | class-compliant USB-MIDI to the host |

## Encoders (8 × quadrature A/B)
`ENCODER_PINS` = `{2,3, 4,5, 6,7, 8,9, 10,11, 12,26, 27,28, 29,30}`

| Encoder | A | B | Stage |
|---|---|---|---|
| Enc1 | 2 | 3 | active |
| Enc2 | 4 | 5 | active |
| Enc3 | 6 | 7 | active |
| Enc4 | 8 | 9 | active |
| Enc5 | 10 | 11 | expansion |
| Enc6 | 12 | 26 | expansion |
| Enc7 | 27 | 28 | expansion |
| Enc8 | 29 | 30 | expansion |

Encoder **push-switches** → MCP23017 `0x20` (GPA0–6 + GPB0), not Teensy GPIO.

## MCP23017 button allocation (verified against `hardware/processor.kicad_sch`)
Each MCP23017 has 16 GPIO (GPA0-7, GPB0-7), but **GPA7/GPB7 are output-only** (silicon
erratum) → **14 usable inputs/chip max**. This build wires **8 pins/chip**: GPA0-6 (7) +
GPB0 (1), library pin numbers 0-6 and 8 (Adafruit_MCP23X17: 0-7=GPA0-7, 8-15=GPB0-7).
**Never use library pin 7 or 15** (GPA7/GPB7) for a button.

| MCP | Addr | Pin (lib #) | Function | Phase 1 status |
|---|---|---|---|---|
| #1 | 0x20 | 0–6, 8 | ENC_1..ENC_8 (encoder push-switches) | ✅ all 8 wired now |
| #2 | 0x21 | 0 | PLAY | ✅ populated now |
| #2 | 0x21 | 1 | STOP | ✅ populated now |
| #2 | 0x21 | 2 | RECORD | ✅ populated now |
| #2 | 0x21 | 3 | LOOP | ✅ populated now |
| #2 | 0x21 | 4 | UNDO | ✅ populated now — sends `CMD_UNDO` (0x4D) → `Song.undo()` |
| #2 | 0x21 | 5 | _(sin asignar)_ | wired, unpopulated — decidir función después, sin rework |
| #2 | 0x21 | 6 | SHIFT | ✅ populated now |
| #2 | 0x21 | 8 | METRONOME | ✅ populated now — **hoy reasignado** a cambio de modo mixer, no es click de metrónomo literal (pendiente de decisión, ver `GAPS_AND_IMPROVEMENTS.md`) |

**Physical pushbuttons to buy: 7** (Play/Stop/Record/Loop/Undo/Shift/Metronome — encoder
switches are built into the EC11s, no separate part; 1 slot on MCP #2 still free).
See `lib/ButtonManager/ButtonManager.cpp`.

Botones "de pantalla" (Push real los tiene físicos, aquí van táctiles para mantener el
tamaño reducido): Delete, Duplicate, Quantize, Redo, Add Track/Device, Octave, Scale,
Layout, Session/Note toggle. Ver soft-key bar en `specs/push-controller-gui-design.md`.

## Analog (12-bit ADC)
| Function | Analog | Teensy pin | Status |
|---|---|---|---|
| Fader 1–4 (ALPS B50K) | A0–A3 | 14, 15, 16, 17 | ✅ Phase 1 |
| Piezo 1–4 (drum, 1 MΩ bleed) | A6–A9 | 20, 21, 22, 23 | ❌ removed (future e-drum) |
| IR 1–2 (Sharp, theremin) | A10–A11 | 24, 25 | ❌ removed (future e-drum) |

## LEDs
| Function | Teensy pin | Notes |
|---|---|---|
| WS2812B NeoPixel data | **33** | via 3.3→5 V level shifter, 330 Ω series |

## I2C device addresses
| Address | Device |
|---|---|
| 0x2E / 0x2F | NeoTrellis pad grid (Seesaw, I2C) — **authoritative link** |
| 0x20 | MCP23017 #1 — encoder switches |
| 0x21 | MCP23017 #2 — extra/transport buttons |

## Decision: NeoTrellis link = I2C (not UART-M4)
The build uses the **I2C NeoTrellis** (Seesaw, `0x2E/0x2F`) on `Wire`. The alternative
**NeoTrellis M4 over bit-banged UART** (`UART_CONNECTIONS.md`, `UART_RX_PIN/TX_PIN`, the
`neotrellis_m4` PlatformIO env) is **parked/deprecated** — do not wire it. Remove that
path in a later cleanup task (tracked as G-P2).

## Pin usage summary (no conflicts)
```
0,1   Serial1 (RPi)        14-17 Faders A0-A3
2-12  Encoders 1-6A        18,19 I2C (SDA/SCL)
13    LED                  20-25 Piezo A6-A9 + IR A10-A11
26-30 Encoders 6B-8        33    NeoPixel data
```
