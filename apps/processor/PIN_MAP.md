# Teensy 4.1 — Authoritative Pin Map (single source of truth)

> **This file is the source of truth for pin assignments.** `include/shared/Config.h`
> mirrors it. `PIN_DISTRIBUTION.md` is kept for power/LED/protocol notes but its old pin
> table is **superseded here** (see Block 0 / gap G-P1, G-P2, G-P3 in `../../GAPS_AND_IMPROVEMENTS.md`).
> Reconciled 2026-07-16 during the from-scratch rebuild. Wire the protoboard to **this** map.

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

## Analog (12-bit ADC)
| Function | Analog | Teensy pin |
|---|---|---|
| Fader 1–4 (ALPS B50K) | A0–A3 | 14, 15, 16, 17 |
| Piezo 1–4 (drum, 1 MΩ bleed) | A6–A9 | 20, 21, 22, 23 |
| IR 1–2 (Sharp, theremin) | A10–A11 | 24, 25 |

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
