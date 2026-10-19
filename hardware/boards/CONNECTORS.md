# GroovePush panel boards — connector contract

> Single source of truth for every board-to-board connector. Both ends of each cable are drawn
> from this table. **All cables are 1:1** (pin n ↔ pin n). Positions on the panel:
> `../panel/panel-coordinates.csv`. Carrier side: `../../apps/processor/PIN_MAP.md`.

```
 Brain carrier J5 (IDC 2×15) ══ribbon══ PCB-A J1
 Brain carrier J15 (Shield socket) → perfboard adapter ──JST-SH 4── PCB-A J2  (I2C)
                                                    └──JST-PH 4── NeoTrellis M4 (UART)
 PCB-A J3 (JST-SH 6)  ── PCB-F J1        faders
 PCB-A J4 (JST-SH 10) ── PCB-K1 J1       I2C, LED data, +5V, MCP INT
 PCB-K1 J2 (JST-SH 10) ── PCB-K2 J1      mode keys + LED data out/return
```

## PCB-A J1 — IDC 2×15 box header (to carrier J5, ribbon 1:1)

| Pin | Net | Teensy | Pin | Net | Teensy |
|---|---|---|---|---|---|
| 1 | +5V | — | 2 | +5V | — |
| 3 | GND | — | 4 | GND | — |
| 5 | ENC1_A | 2 | 6 | GND | — |
| 7 | ENC1_B | 3 | 8 | ENC5_A | 22 |
| 9 | ENC2_A | 4 | 10 | ENC2_B | 5 |
| 11 | FADER4 | 17 (A3) | 12 | FADER3 | 16 (A2) |
| 13 | ENC3_A | 9 | 14 | FADER2 | 15 (A1) |
| 15 | ENC3_B | 10 | 16 | FADER1 | 14 (A0) |
| 17 | ENC4_A | 11 | 18 | — (spare, Teensy 13) | 13 |
| 19 | ENC4_B | 12 | 20 | INT_K (MCP 0x21/0x22) | 41 |
| 21 | ENC5_B | 24 | 22 | INT_A (MCP 0x20) | 40 |
| 23 | ENC6_A | 26 | 24 | ENC8_B | 35 |
| 25 | ENC6_B | 30 | 26 | LED_DIN (5 V, buffered on carrier) | 28 |
| 27 | ENC8_A | 34 | 28 | ENC7_A | 31 |
| 29 | ENC7_B | 32 | 30 | +3V3 | — |

## PCB-A J2 — JST-SH 4, I2C in (Qwiic / STEMMA QT order)

| 1 | 2 | 3 | 4 |
|---|---|---|---|
| GND | +3V3 | SDA | SCL |

The 4.7 kΩ I2C pull-ups are on PCB-A (the carrier relies on the Audio Shield's, which GroovePush
doesn't fit).

## PCB-A J3 ↔ PCB-F J1 — JST-SH 6, faders

| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| +3V3 | FADER1 | FADER2 | FADER3 | FADER4 | GND |

## PCB-A J4 ↔ PCB-K1 J1 — JST-SH 10, keys board

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| +5V | +5V | GND | GND | +3V3 | SDA | SCL | LED_DIN | INT_K | GND |

## PCB-K1 J2 ↔ PCB-K2 J1 — JST-SH 10, mode keys

| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| +5V | GND | LED_K2_IN | LED_K2_RET | KEY_BROWSE | KEY_MIX | KEY_DEVICE | KEY_NOTE | KEY_SESSION | GND |

## MCP23017 allocation (supersedes the provisional table in PIN_MAP.md)

| MCP | Addr | Board | GPA0–GPA6 | GPB0–GPB6 |
|---|---|---|---|---|
| U1 | 0x20 | PCB-A | ENC1–ENC7 switches | GPB0 ENC8 switch; GPB1–6 spare |
| U1 | 0x21 | PCB-K1 | PLAY, STOP, RECORD, LOOP, METRO, SHIFT, BANK_L | BANK_R, OCT_DN, OCT_UP, DELETE, DUPLICATE, QUANTIZE, NEW |
| U2 | 0x22 | PCB-K1 | UNDO, BROWSE, MIX, DEVICE, NOTE, SESSION, spare | spare |

GPA7/GPB7 are never used (output-only erratum). Keys and encoder switches pull to GND; the MCP's
internal pull-ups are enabled in firmware. INT_K is shared by 0x21 and 0x22: configure both as
open-drain (`IOCON.ODR = 1`); PCB-K1 has a 10 kΩ pull-up.

## LED chain (SK6812MINI-EA, 20 LEDs, data at 5 V)

`LED_DIN` (carrier) → PCB-K1 → **PCB-K2** (indices 0–4: BROWSE, MIX, DEVICE, NOTE, SESSION) →
back to PCB-K1 → edit block (5–9: QUANTIZE, DUPLICATE, DELETE, UNDO, NEW) → front row (10–19:
SHIFT, PLAY, STOP, RECORD, LOOP, METRO, BANK_L, BANK_R, OCT_DN, OCT_UP). Cap brightness in
firmware: 20 × 60 mA at full white is 1.2 A.
