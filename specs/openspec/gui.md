# GUI — OpenSpec

> **Id**: SPEC-GUI
> **Status**: Draft
> **Owners**: gui-engineer
> **Parent**: [`push-controller.md`](push-controller.md) (SPEC-PUSHCTRL)
> **Normative design source**: [`../push-controller-gui-design.md`](../push-controller-gui-design.md) (GUI Design & Brand Spec v1.0)
> **Target**: Qt 6 / QML on Raspberry Pi 5, 5" DSI 800×480 (`apps/gui`)
> **Version**: 0.1

## 1. Purpose & context
The GUI is the 5" instrument display. Today it is a **Live-mirroring controller UI**
(tabbed Session/Mix/Device/Browse/Note, `SerialController` + `ClipGridModel`,
`MixerModel`, `TrackListModel`, `SceneListModel`, `PushCloneTheme` singleton). The target
reframes it as an **encoder-first AI-copilot surface** with 7 mode screens and a soft-key
bar. The full visual/brand contract is the **normative design source**; this spec assigns
requirement ids and the C++/QML architecture constraints.

## 2. Scope
- **In scope**: the mode screens (HOME/Score, GEN, PLAY, COPILOT, SOUND, AUDIT,
  SETTINGS/PAIRING), the persistent chrome (top bar + 8-cell soft-key bar), the Theme
  singleton, and the bus-client seam to `gp-bridged`.
- **Out of scope**: networking/AI (owned by `gp-bridged`); MIDI (owned by the Teensy).

## 3. Constraints (inviolable — from design source §1, §10)
- C-1: **Glanceable** — one primary value per screen, mono numerals, `bgBase` always.
- C-2: **Encoder-first** — every flow completable without touch; 8 soft keys mirror the
  8 physical encoders/buttons.
- C-3: **Screen & LEDs are one language** — teal = audio/interactive, **purple = AI only**.
- C-4: **No sockets/HTTP in QML** — the GUI is a pure view over the `gp-bridged` bus (§8).
- C-5: **No hardcoded hex/px** — Theme singleton + `Theme.scale` only.

## 4. Requirements

| Id | Requirement | Design § |
|----|-------------|----------|
| R-GUI-1 | A `Theme` singleton holds the exact tokens (teal `#00D4AA`, purple `#8B5CF6` AI-only, bg `#09090B`/`#141418`, semantic, type roles) and a `scale = Screen.width/800`. | §3 |
| R-GUI-2 | Bundle **General Sans** + **JetBrains Mono** via `.qrc` FontLoader in Theme; every number mono, every word sans; no system-font dependence. | §3 |
| R-GUI-3 | Persistent **top bar** (mode · session key/BPM · RS/BE/HW dots · quota chip) and **8-cell soft-key bar** mirroring the encoders, with focus/active/AI states. | §5 |
| R-GUI-4 | Seven **mode screens** per design §6, switched by a StackLayout with a 180 ms slide+fade. | §6 |
| R-GUI-5 | HOME shows the **Mix Score ring** (Shape, count-up 1.5 s), 7-band spectrum (teal gradient, 10–20 Hz, `Behavior` smoothed), and 7 dimension rows. | §6.1, §7 |
| R-GUI-6 | GEN shows the **step grid mirroring pads 1:1**, purple ghost → teal committed, streaming GENERATE state, VARIATION overlay. | §6.2 |
| R-GUI-7 | COPILOT streams SSE chat token-by-token (purple accent, caret blink), curated quick-actions, QR hand-off; 429 → amber toast. | §6.4 |
| R-GUI-8 | The GUI is a **pure view over the bus**: subscribes to `features_frame`/`score_update`/`session_state`/chat; publishes intents. No networking in QML. | §8 |
| R-GUI-9 | Performance: 60 fps on RPi 5 with spectrum animating — `Shape`/scene-graph (no `Canvas`), no per-frame JS timers, fonts loaded once. | §8 |
| R-GUI-10 | Degraded-mode surfaces ("Plugin offline", offline banner, plan locks) render as explicit states. | design §6, parent §4.9 |

## 5. Interfaces & contracts
- Bus client (new C++/Python bridge exposed to QML) ⇄ `gp-bridged` (ZeroMQ). Replaces the
  current `SerialController`-drives-everything model for AI data (transport/session may
  still use serial short-term — see gap G-G4).
- Theme singleton API: colors/fonts/sizes/scale — the only place hex/px live.

## 6. Acceptance criteria
- AC-1 (R-GUI-1/2): grepping components finds **no** inline hex or px; fonts render from qrc.
- AC-2 (R-GUI-4..7): each AI flow in normative §4 is drivable from soft keys + encoders.
- AC-3 (R-GUI-9): spectrum animates at ≥ 60 fps on RPi 5 (measured).
- AC-4 (R-GUI-8): with `gp-bridged` mocked, screens render from bus messages headless.

## 7. Open questions / risks
- Migration order: refit `PushCloneTheme` → `Theme` in place, or new `qml/Theme/` tree
  (design §8 layout) and port screens? (gap G-G1.)
- `features_frame` rate the QML scene can sustain on RPi 5 (parent §7.2).

## 8. Change log
- 0.1 — initial draft from current GUI + design source v1.0.
