# Processor / Firmware — OpenSpec

> **Id**: SPEC-PROC
> **Status**: Draft
> **Owners**: firmware-engineer, qa-hardware-test
> **Parent**: [`push-controller.md`](push-controller.md) (SPEC-PUSHCTRL)
> **Targets**: Teensy 4.1 (`apps/processor`, env `teensy41`) + NeoTrellis pad grid
> **Version**: 0.1

## 1. Purpose & context
The processor is the real-time I/O hub: it scans encoders/faders/piezo/IR/buttons, merges
NeoTrellis pad events, presents a **class-compliant USB-MIDI** device to the host, and
streams control events to the RPi for the GUI. Today it is a mature **session/mixer
controller** over SysEx (`LiveController`, `GUIInterface`, `NeoTrellisLink`, `UIBridge`,
`ViewManager`). This spec keeps that and adds the performance-MIDI + GEN/PLAY surfaces the
AI copilot needs.

## 2. Scope
- **In scope**: USB-MIDI note/CC output, pad/encoder/fader/piezo/IR/button drivers, the
  Teensy↔RPi UART, the Teensy↔NeoTrellis link, LED frame rendering, a MIDI-clock-slaved
  local audition sequencer, GEN-mode step editing.
- **Out of scope**: AI, scoring, backend calls (RPi/plugin own those); PCB (`hardware/`).

## 3. Constraints (inviolable)
- C-1: Performance MIDI (pads/encoders/faders/piezo) → USB-MIDI, **< 5 ms**, never via RPi.
- C-2: Shared constants live in `include/shared/Config.h`; keep Teensy & M4 in sync.
- C-3: Teensy pins are 3.3 V. Honor `PIN_DISTRIBUTION.md`.

## 4. Requirements

| Id | Requirement | Rationale |
|----|-------------|-----------|
| R-PROC-1 | Pads emit class-compliant **note-on/off with a velocity curve** over USB-MIDI (in addition to the existing SysEx clip-trigger path). | Target §Phase 3; PLAY/GEN need real notes, not only clip SysEx |
| R-PROC-2 | Encoders emit **relative CC**; faders emit CC; piezo emit notes; IR emit CC — all USB-MIDI, MIDI-mappable in Live. | Target §3.4, §4.8 |
| R-PROC-3 | Teensy↔RPi UART uses **JSON lines** both ways: up `{"ev":"enc\|btn\|fader\|pad",…}`, down `{"led":…}` / mode frames. | Target §3.4 |
| R-PROC-4 | A **LED frame renderer** drives pad/button colors from RPi frames, with the teal(audio)/purple(AI) semantics. | Target §4.1, §4.3, design §4 |
| R-PROC-5 | A **local audition sequencer** slaved to Live's MIDI clock plays GEN previews via USB-MIDI. | Target §4.3, §Phase 3 |
| R-PROC-6 | **GEN step editing**: toggling steps locally produces a diff sent to the RPi so COMMIT writes the edited pattern. | Target §4.3, §Phase 3 |
| R-PROC-7 | **Scale-aware PLAY** grid layout (isomorphic 4ths) computed on Teensy+RPi from session key; no backend. | Target §4.4 |
| R-PROC-8 | Existing session/mixer/clip/transport SysEx control (`MidiCommands.h`) is preserved and kept working alongside the new note/CC path. | No regression |
| R-PROC-9 | Handshake + heartbeat/ping link management to both the RPi and (via NeoTrellisLink) the pad board remains. | Existing `CMD_HANDSHAKE`/`CMD_PING_TEST` |

## 5. Interfaces & contracts
- USB-MIDI: notes (pads/piezo), relative CC (encoders), CC (faders/IR), SysEx (session).
- SysEx catalog: `include/MidiCommands.h`; framing/consts: `include/shared/*`.
- UART to RPi: JSON lines (new) — supersedes/extends the current `GUIInterface` binary/SysEx
  serial path (see gap G-P4).
- Pin map: `PIN_DISTRIBUTION.md` (authoritative), reconciled with `hardware/`.

## 6. Acceptance criteria
- AC-1 (R-PROC-1): pad → Live note latency **< 5 ms** measured on the bench.
- AC-2 (R-PROC-4/5): LED preview of a generated drum pattern matches the notes committed.
- AC-3 (R-PROC-3): `gp-bridged` receives well-formed JSON-line events for every control.
- AC-4 (R-PROC-8): session/mix control still passes its existing manual test after the
  note/CC path is added.

## 7. Open questions / risks
- GEN audition sound source (Live armed track vs onboard) — see parent §7.3.
- Reconcile **I2C NeoTrellis** (hardware/) vs **UART NeoTrellis M4** (`UART_CONNECTIONS.md`).
- Encoder pin-map conflict between `PIN_DISTRIBUTION.md` and `Config.h` (gap G-P1).

## 8. Change log
- 0.1 — initial draft from current firmware + target Phase 3.
