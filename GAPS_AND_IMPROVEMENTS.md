# GroovePush — Gaps & Improvements

_Analysis date: 2026-07-16 · Contrasts the current code against the new specs:_
_[`specs/openspec/push-controller.md`](specs/openspec/push-controller.md) (adopts_
_[`push-controller-groovepilot.md`](specs/push-controller-groovepilot.md)),_
_[`specs/openspec/gui.md`](specs/openspec/gui.md) (adopts_
_[`push-controller-gui-design.md`](specs/push-controller-gui-design.md)),_
_[`specs/openspec/processor.md`](specs/openspec/processor.md)._

---

## 0. Executive summary

The current repo is a **mature Ableton session/mixer controller**: a Push-clone that
triggers clips, drives the mixer, and mirrors Live on a 5" screen over a SysEx-based
serial link. It works and is well-structured (`LiveController`, `GUIInterface`,
`NeoTrellisLink` on the Teensy; `SerialController` + Qt models on the GUI; a rich
Python Remote Script).

The new specs describe a **different product layered on top**: an AI mix-copilot surface.
A code survey found **zero** occurrences of every core target concept — `zmq`,
`gp-bridged`, port `9878`, `features`, `score`, `pairing`, `Avahi`, `backend`,
`groovepilot`, `purple`/`#8B5CF6` — across `apps/gui` and `apps/processor`. So the
intelligence layer is **not started**; the existing controller is the **foundation** to
extend, not throw away.

### Maturity vs target

| Capability | Status | Where |
|---|---|---|
| Session/mixer/clip control over SysEx | ✅ Built | `LiveController`, `MidiCommands.h`, Remote Script |
| GUI shell, models, serial link, handshake/ping | ✅ Built | `SerialController`, `*Model.{h,cpp}`, `Main.qml` |
| USB-MIDI to Live (SysEx + some note/CC) | 🟡 Partial | `LiveController.cpp` (SysEx), `Piezo`/`Theremin`/`CapButtons` (note/CC) |
| Class-compliant note/CC for pads/encoders/faders | ❌ Missing | needed for PLAY/GEN — R-PROC-1/2 |
| `gp-bridged` daemon (plugin link, backend, bus) | ❌ Missing | entire RPi intelligence layer — R-PUSHCTRL-4/5 |
| Controller Bridge in plugin (TCP 9878) | ❌ Missing (plugin repo) | R-PUSHCTRL-1..3 |
| ZeroMQ bus + QML-as-pure-view | ❌ Missing | GUI does its own serial — R-GUI-8 |
| 7 AI mode screens + soft-key bar | ❌ Missing | current UI is tabbed Live-mirror — R-GUI-3/4 |
| Theme tokens (teal/purple, scale, bundled fonts) | ❌ Mismatch | `PushCloneTheme` is cyan/Helvetica — R-GUI-1/2 |
| Mix Score / spectrum / FIX / AUDIT / COPILOT / SOUND / GEN | ❌ Missing | R-GUI-5/6/7, R-PUSHCTRL-7 |
| mDNS pairing + token + API-key store | ❌ Missing | R-PUSHCTRL-9 |

---

## 1. Processor (`apps/processor`)

**Obsolete / to reconcile**
- **G-P1 (urgent)** — Encoder pin map disagrees between `PIN_DISTRIBUTION.md` (8 encoders
  on pins 0,1,2,3,6,7,8,9,10,11,12,24–28) and `include/shared/Config.h`
  (`ENCODER_PINS_ACTIVE {2,3,4,5,6,9,10,11}`, `NUM_ENCODERS_ACTIVE 4`). One is stale.
  Pick the truth, update both + `hardware/` before any encoder work.
- **G-P2** — NeoTrellis link is doubly specified: I2C (`0x2E`/`0x2F`, this build +
  `hardware/`) vs bit-banged UART on the M4's I2C pads (`UART_CONNECTIONS.md`,
  `Config.h` `UART_RX_PIN 21`). Decide and delete the losing path.
- **G-P3** — Two `Config.h` (`include/Config.h` and `include/shared/Config.h`) and two
  `include/*` trees; confirm which is authoritative and drop the duplicate.

**Missing (for the new specs)**
- **G-P4 (urgent)** — No **JSON-lines UART** to the RPi (R-PROC-3). The current
  Teensy↔GUI path is SysEx/binary via `GUIInterface`; the `gp-bridged` bus expects
  `{"ev":"enc",…}` lines. New adapter needed (keep SysEx to Live).
- **G-P5** — Pads only trigger clips via SysEx; no **class-compliant note-on/off with a
  velocity curve** (R-PROC-1). Blocks PLAY and GEN audition.
- **G-P6** — Encoders/faders don't emit **MIDI-mappable relative CC/CC** to Live
  (R-PROC-2); today they feed SysEx mixer commands only.
- **G-P7** — No **LED frame renderer** driven by RPi frames with teal/purple semantics
  (R-PROC-4); LED state is currently clip-state driven only.
- **G-P8** — No **MIDI-clock-slaved audition sequencer** (R-PROC-5) and no **GEN step
  editing/diff** (R-PROC-6).
- **G-P9** — No **scale-aware isomorphic PLAY layout** (R-PROC-7).

**Improvements**
- **G-P10** — `src/teensy/main.cpp` hand-parses serial with `strtok`/global buffers;
  as UART grows to JSON, move to a small framed line reader with tests (`test_*` env).

---

## 2. GUI (`apps/gui`)

**Obsolete / mismatch**
- **G-G1 (urgent)** — `PushCloneTheme.qml` is a **cyan/Helvetica/Monaco** theme with **no
  `scale`, no purple-AI semantics, no teal `#00D4AA`, no bundled fonts** — it contradicts
  design §3/§4 (R-GUI-1/2). Rework into a `Theme` singleton with the exact tokens and
  `scale = Screen.width/800`, or add a new `qml/Theme/` tree and migrate (decide: G-G1).
- **G-G2** — `Main.qml` uses **tab navigation** (Session/Mix/Device/Browse/Note) with
  Device/Browse/Note as "Coming soon" placeholders. The target is **encoder-first mode
  switching** with an 8-cell soft-key bar (R-GUI-3/4). The tab/NavigationBar model and the
  placeholders are obsolete for the new UX.
- **G-G3** — Stray duplicate `apps/gui/CMakeLists 2.txt` (carried from the old repo) — delete.

**Missing**
- **G-G4 (urgent)** — GUI owns its own serial link (`SerialController` + `QSerialPort`),
  violating "**no networking in QML / pure view over the bus**" (R-GUI-8). Needs a
  **ZeroMQ bus client** seam; `SerialController` becomes (at most) a fallback transport.
- **G-G5** — None of the **7 mode screens** exist (HOME/Score, GEN, PLAY, COPILOT, SOUND,
  AUDIT, SETTINGS/PAIRING) — R-GUI-4..7.
- **G-G6** — No **Mix Score ring / spectrum / dimension rows** (R-GUI-5); no `GpScoreRing`,
  `GpSpectrum`, `GpStepGrid`, `GpChatView`, `GpSoftKeyBar`, `GpConnectionDots`, `GpToast`,
  `GpQuotaChip` components (design §8).
- **G-G7** — No **SSE streaming chat** rendering, no **QR hand-off**, no quota/429 surfaces
  (R-GUI-7).
- **G-G8** — No **pairing/first-boot** flow (mDNS spinner, 6-digit code, API-key confirm) —
  design §6.7, R-PUSHCTRL-9.
- **G-G9** — No **General Sans / JetBrains Mono** in `resources.qrc` (R-GUI-2).

**Improvements**
- **G-G10** — Reusable component library is thin (`ClipPad`, `MixChannelStrip`,
  `TransportBar`, `NavigationBar`); build the `Gp*` set against the Theme singleton.
- **G-G11** — Verify 60 fps budget rules (no `Canvas`, no per-frame JS timers) as new
  meters land (R-GUI-9).

---

## 3. Remote Script (`apps/remote-script`)

The Remote Script is mature (transport, clip R/W, track scan, session ring). For the new
specs it is **consumed by the plugin relay**, so mostly it just needs contract alignment.

- **G-RS1** — Confirm the relay message catalog (parent §3.2: `get_session`,
  `write_midi_clip`, `read_midi_clip`, `create_midi_track`, `start_track_scan`,
  `subscribe_events`, `apply_param_batch`, …) is fully implemented in `_dispatch`; fill
  any gap. The spec claims these exist — **verify**, don't assume.
- **G-RS2** — Keep SysEx command IDs in `consts.py` in lockstep with firmware
  `MidiCommands.h` (3-endpoint contract). Add a conformance check (see G-I3).
- **G-RS3 (hygiene)** — 15 tracked `.py` files had **uncommitted edits** in the live
  Ableton folder at import; the monorepo now holds that state — reconcile and adopt the
  monorepo as source of truth, deploy via `update_pushclone.sh`.
- **G-RS4** — Large reference blobs (`lom_full.txt`, the 1.1 MB LOM PDF) live beside code;
  PDF is now gitignored — consider moving references under `docs/`.

---

## 4. Integration — new components that don't exist yet

These are net-new and the bulk of the work (parent §6 phases):

- **G-I1** — **Controller Bridge** in the VST3 plugin (TCP 9878): opt-in, mDNS advertise,
  pairing code, token store, whitelisted relay, plan-gating, push channels
  (`features_frame`/`score_update`/`connection_state`). Lives in the **plugin repo**
  (external), tracked here as a dependency (R-PUSHCTRL-1..3).
- **G-I2** — **`gp-bridged`** daemon on the RPi (Python 3.12): Avahi discovery + pairing,
  plugin link w/ reconnect, backend client (API-key, SSE chat, midi/generate, tools/call,
  audit, usage), ZeroMQ bus, UART to Teensy, systemd unit, `POST /plugin/log`. **New
  workspace** — suggest `apps/bridged` (R-PUSHCTRL-4/5).
- **G-I3** — **Protocol/contract conformance**: a single source-of-truth for command IDs
  and payloads across firmware / Remote Script / GUI / bridge, plus a test that fails when
  they drift (owned by `qa-hardware-test`).
- **G-I4** — **Security**: API key in root-owned `0600` `/etc/groovepilot/credentials`,
  never in QML/logs; mDNS TXT carries no PII (R-PUSHCTRL-9).
- **G-I5** — **Degraded-mode matrix** (parent §4.9) implemented and testable by pulling
  cables mid-flow (R-PUSHCTRL-8).

---

## 5. Hardware follow-ups (from Phase 3)

- **G-H1** — Assign KiCad **footprints** (schematic-only today) before PCB layout.
- **G-H2** — Map the **Teensy 4.1 socket** pins to the real footprint (J1 pins are logical).
- **G-H3** — Run **ERC in KiCad 10** (no `kicad-cli` in the analysis env).
- **G-H4** — Select a **3.3 V-compatible IR** sensor or add a divider (analog board).
- **G-H5** — Reconcile the schematic's **I2C NeoTrellis** with firmware config (ties to G-P2).

---

## 6. Urgent refactorings (do first — they unblock everything else)

1. **G-P1 / G-P2 / G-P3** — settle the pin map, the NeoTrellis link, and the duplicate
   `Config.h`/`include` trees. Every firmware and hardware task depends on this truth.
2. **G-I2 scaffold** — stand up `apps/bridged` with the ZeroMQ bus and a fake plugin +
   mocked backend, so the GUI and firmware can develop against a real bus early.
3. **G-G1** — land the `Theme` singleton with correct tokens + `scale`; nothing else in the
   new GUI should be built on the old cyan theme.
4. **G-P4 + G-G4** — introduce the **JSON-lines UART ⇄ ZeroMQ** seam so QML stops owning
   the transport (R-GUI-8) and the daemon owns the links.
5. **G-P5/G-P6** — add the **class-compliant note/CC USB-MIDI** path (keeps <5 ms budget)
   so PLAY and GEN audition are possible.

## 7. Priority matrix

| Priority | Items | Theme |
|---|---|---|
| **P0 — unblockers** | G-P1, G-P2, G-P3, G-I2 (scaffold), G-G1 | source-of-truth + foundations |
| **P1 — core plumbing** | G-P4, G-G4, G-I1, G-I3, G-P5, G-P6 | the bus + performance MIDI |
| **P2 — copilot features** | G-G5..G-G8, G-P7..G-P9, G-I4, G-I5 | screens + AI flows |
| **P3 — polish/hygiene** | G-P10, G-G3, G-G10, G-G11, G-RS3/4, G-H1..H5 | cleanup + resilience |

> Next: [`specs/openspec/*.tasks.md`](specs/openspec/) will turn P0/P1 into ordered,
> verifiable tasks (SDD step 2 via `/tasks`). See the Phase 5 roadmap.
