# 01 · Borrador de Claude — Temporada 1 "Dos cerebros, un banco"

> Etapa 1 + Etapa 2 del pipeline de contenido. Fuente: lectura de los dos repos el 2026-10-22
> (`jdavidguerrero/groovepush` @ `65c1c4f`, `jdavidguerrero/grooveforge-brain` @ `c32a4f9`).
> Lo que sigue alimenta a `02_optimizacion_codex.md` y termina en `BIBLIA_PRODUCCION_FINAL.md`.
>
> **Dos reglas heredadas del Brain que este borrador respeta**
> (`grooveforge-brain/apps/docs/content/00-content-playbook.md` §1 y `01-modelo-rampa-y-apertura.md` §3.3):
> 1. **Nunca muestres lo que no existe.** Cada toma lleva un estado: ✅ existe hoy · ⏳ se graba cuando exista.
> 2. **Política de apertura.** Engines: se muestran snippets y concepto, no el fuente completo. Modelos TinyML: números
>    y concepto, nunca pesos, dataset ni receta de quantización. FX, enclosure y protocolo: abiertos.

---

## ETAPA 1 — Análisis técnico

### 1.1 El porqué y la propuesta única

Son dos instrumentos hermanos sobre el mismo cerebro (Teensy 4.1, Cortex-M7 a 600 MHz):

| | **GrooveForge Brain** (Studio) | **GroovePush** |
|---|---|---|
| Qué es | Synth de escritorio: 6 arquitecturas clásicas (Model D, Juno-106, Prophet-5, OB-6, DX7 de 4 operadores, ARP 2600) + FX + TinyML | Clon DIY de Ableton Push 3: grid 8×4 (NeoTrellis M4), 8 encoders, 4 faders, 28 botones por MCP23017 |
| Cabeza | Pi 3B + DSI 5" 800×480, LVGL (`apps/studio-head`) | Pi 5 + Waveshare 7" 1280×720 multitouch, Qt 6/QML (`apps/gui`) |
| Regla de oro | El audio nunca depende de la cabeza: controles cableados al Teensy (ADR-004) | La MIDI de performance nunca toca la red: USB-MIDI directo, < 5 ms (CLAUDE.md, principio 1) |
| Lo que comparten | La **portadora** del Brain: GroovePush la reusa sin modificarla (gap G-H10, `hardware/boards/CONNECTORS.md`); misma identidad visual (ADR-0003); misma tecla Choc V2 + SK6812-MINI-E (ADR-0004) |

**La propuesta única, en una frase:** un solo maker en Bogotá, en sus ratos libres, construye un synth y su
controlador con el mismo PCB portador, spec-first, y documenta cada error con números. No es "cómo hacer un MIDI
controller": es la intersección DSP + embedded + música + IA en el borde, con resultados audibles y medidos.

### 1.2 Decisiones críticas de ingeniería (lo que demuestra nivel)

| # | Decisión | Dónde está | Por qué impresiona |
|---|---|---|---|
| D1 | `tanhf` ×7 por muestra → 5 tanh con aproximante Padé [7/6] | `brain/apps/docs/theory/fidelidad-engines.md` §1, `src/dsp/fast_math.h`, `src/dsp/zdf_ladder.h` | El ladder costaba ~8 % de CPU por voz (48 % con 6 voces, medido 2026-10-15). **Esperado** ~1 %/voz (8× menos), error < 2·10⁻⁵; la CPU real con 6 voces está pendiente de medir on-device (§9.4) |
| D2 | DX7 de 4 operadores como **objeto de audio propio** | `brain/apps/docs/adr/ADR-005-dx7-cuatro-operadores.md`, `src/engines/dx7_core.*` | La Teensy Audio Library procesa en bloques de 128 muestras: un lazo de feedback llega 2.9 ms tarde y deja de ser FM. Además el DX7 hace modulación de *fase*, no de frecuencia |
| D3 | Un filtro por familia de chip: ladder ZDF (Moog/ARP), ZDF con carácter IR3109 (Juno) y CEM3320 (Prophet), SVF trapezoidal (OB-6 SEM, notch −80 dB) | `fidelidad-engines.md` §4 y §9.4, `src/dsp/zdf_ladder.h`, `src/dsp/sem_svf_core.h` | Citas reales: Huovilainen DAFx 2004, Zavalishin 2018 |
| D4 | Envelopes RC exponenciales con overshoot (ataque apunta a 1.3, corta en 1.0) | `src/dsp/analog_env.h`, `fidelidad-engines.md` §2 | El "punch" analógico explicado con un capacitor |
| D5 | Osciladores polyBLEP | `src/dsp/polyblep_core.h`, `fidelidad-engines.md` §8 | Aliasing bajo 5 kHz en C6: **−70 dB vs −23 dB** del saw ingenuo (medido offline) |
| D6 | Validación offline: el mismo código DSP compilado con clang en el Mac, contra la teoría (Bessel para FM, curvas de envelope, afinación de filtros) + WAVs | `brain/apps/firmware-teensy/tools/offline/validate_engines.cpp` (commit `a68aaf5`) | Testear DSP sin hardware, con números |
| D7 | Bridge Teensy↔cabeza: `[CMD][LEN][SEQ][PAYLOAD][CRC8]`, CRC-8 poly 0x07, UART 921600 | `brain/apps/docs/02-bridge-protocol.md`, `apps/bridge-protocol/include/` | Protocolo binario propio, con timeout de frame parcial (`e4150bb`) |
| D8 | GroovePush: dos protocolos a la vez — binario `[0xAA][CMD][LEN][PAYLOAD][XOR]` al M4/Pi y SysEx a Ableton | `groovepush/apps/processor/include/shared/BinaryProtocol.h`, `apps/remote-script/consts.py` | Un controlador serio habla tres idiomas: USB-MIDI, SysEx y binario |
| D9 | Una sola fuente de verdad para pines y conectores, y los dos lados del cable generados desde la tabla | `groovepush/apps/processor/PIN_MAP.md`, `hardware/boards/CONNECTORS.md`, `set_idc_pinout.py` del Brain | Cables 1:1, sin cruces |
| D10 | PCB por script: coordenadas del panel → colocación → Freerouting → DRC 0/0/0 → fab | `groovepush/hardware/panel/panel-coordinates.csv`, `hardware/boards/tools/place_pcb_*.py`, `route_board.py`, `export_fab.py` | El enclosure y la PCB salen de la misma tabla |
| D11 | Etapa de entrada validada por SPICE antes de pedir la placa (pad 0/−10/−20 dB, VREF 1.65 V, CV con 5.2 ms de asentamiento) | `brain/apps/docs/variants/studio/theory/03-studio-input-stage.md`, `apps/hardware/kicad/studio/sim/` | Nadie hace protoboard de lo que ensambla JLC: se simula |
| D12 | El filtro analógico 2N3904 sale del synth y se vuelve add-on por CV (pin 29, PWM filtrado) | `brain/apps/docs/adr/ADR-003-filtro-analogico-add-on.md` | Una decisión de producto valiente, con números de headroom |
| D13 | TinyML: 3 modelos int8 (key, chord, beat) en flash vía `.rodata`, sin copiar a RAM | `brain/apps/docs/sprints/23-key-detector.md`, `25-beat-follower.md`, `apps/firmware-teensy/src/ml/` | "Redes neuronales en un microcontrolador" — 🟡 solo concepto y números |

### 1.3 Puntos de fricción (el conflicto narrativo)

Cada uno es un error real, con commit o documento que lo prueba:

| # | El problema | La evidencia | El desenlace |
|---|---|---|---|
| F1 | **El clic que desaparecía.** Los EC11 dan 2 pulsos por detent y el firmware dividía entre 4: respondía un clic de cada dos | commit `625c304` | `ENC_SHIFT = 1` |
| F2 | **El valor que tiembla solo.** El contacto vibra ±1 pulso en reposo; `raw >> 1` sube y baja el parámetro | `src/ui/detent.h` (commit `3f3dc1b`) | Detents con histéresis: 15 líneas de C++ |
| F3 | **El cutoff que no bajaba de 83 Hz.** El Brain manda cada edición por CC; el computador se la devuelve; CC 74 lineal = 63 Hz por paso | commit `a3c588c` | CC logarítmico + ignorar el eco 150 ms |
| F4 | **El pin 13 tiene un LED.** ENC R-A del Studio va al pin 13 de la Teensy, que tiene LED + 470 Ω. PJRC dice no usar `INPUT_PULLUP` ahí | `brain/apps/hardware/kicad/studio/docs/auditoria-fabricacion-2026-10-22.md` F1 | Pedido de PCB **retenido**. Dato cruzado: en GroovePush ese mismo pin quedó como *spare* (`CONNECTORS.md`, J1.18) |
| F5 | **La fuente USB-C que no enciende.** La portadora recibe solo VBUS/GND; sin resistencias Rd en CC1/CC2 una fuente USB-C puede no habilitar la salida | auditoría F2 | Definir el módulo de panel completo |
| F6 | **3 A que no son 3 A.** Fusible mSMD300 (hold 3 A, trip 5 A), JST-XH genérico, IDC de 1 A por contacto; ~73 mV de caída solo en cobre a 2.5 A | auditoría F3 | Presupuesto de corriente y prueba de carga real |
| F7 | **El selector que no existe.** El pad pide un DP3T real; la lista de compras decía "ON-ON-ON u ON-OFF-ON" | auditoría F4 | Tabla de continuidad antes de comprar |
| F8 | **El pin que solo es salida.** GPA7/GPB7 del MCP23017 son solo-salida (erratum); METRONOME estaba ahí | `groovepush/GAPS_AND_IMPROVEMENTS.md` G-P12 (commit `02591ff`) | Movido a GPB0 y verificado con el net lister de KiCad |
| F9 | **El encoder que se comía el cable de la pantalla.** El mapa de Block 0 puso Enc3/Enc4 en los pines 7/8 = `Serial2`, el enlace a la GUI | G-P14 (commit `853ab24`) | Re-mapeo a la portadora; puertos centralizados en `Config.h` |
| F10 | **Me equivoqué de grid.** En julio se decidió "NeoTrellis por I2C"; el grid real es un NeoTrellis M4 por UART | G-P2 REVERSED (commit `7dccd30`) | Corregir docs y volver al camino UART a 1 Mbps |
| F11 | **El botón que no hacía nada.** `CMD_UNDO` (0x4D) existía en ambos lados, pero ningún handler lo atendía | G-P13 (commit `45897b3`) | `TransportManager.trigger_undo()` → `Song.undo()` |
| F12 | **El DX7 que no era FM.** Usaba `frequencyModulation()`, 2 operadores, sin feedback | `auditoria-tecnica-2026-05.md`, ADR-005 | Objeto propio de 4 operadores |
| F13 | **El filtro que era el corazón del precio y nunca existió.** Conversor exponencial sin definir, ~2 Vpp de headroom a 5 V para 1 Vrms | `auditoria-tecnica-2026-05.md` §1 punto 2, ADR-003 | Sale del synth; vuelve como add-on |
| F14 | **La auditoría que también se equivoca.** De 13 "bloqueantes" de una auditoría externa, 4 eran reales y 5 falsos | `brain/.../lecciones-para-groovepush.md` §8 | Verificar cada hallazgo contra los archivos |
| F16 | **El filtro que desafinaba al resonar.** La auto-oscilación del ladder caía −859 ¢ a 1.76 kHz y −1913 ¢ a 5 kHz | `fidelidad-engines.md` §8 (validación offline 2026-10-18) | **±5 ¢ de 110 Hz a 12 kHz** tras el ZDF (§9.4) |
| F17 | **El click del re-disparo.** El envelope saltaba de 0.50 a 0 al tocar otra nota | `fidelidad-engines.md` §8 → §9.4 | Sigue desde el nivel actual |
| F15 | **El ruido de la protoboard.** Probable lazo de tierra / cables largos, no firmware | `lecciones-para-groovepush.md` §7 | El plano de GND es parte del diseño |

---

## ETAPA 2 — Arquitectura de la serie

**Título de temporada:** *Dos cerebros, un banco* — construyendo un synth y un Push clone con el mismo Teensy.
**Formato:** 8 episodios de 10-15 min. Arco: del sonido (lo que ya existe) al PCB (lo que está por pedirse), y
termina en la decisión de pedirlo o no. Los episodios alternan Brain y GroovePush para que el espectador vea que las
lecciones de uno se pasan al otro.

**Estados de grabación hoy (2026-10-22):**
- ✅ Brain Studio en protoboard suena (sketch48: USB host MIDI → voz → I2S → LINE OUT; sketch49 con engines reales).
- ✅ Cabeza de Studio corre (LVGL, kiosk, PERFORM/PANEL).
- ✅ Esquemáticos, PCBs ruteadas con DRC 0/0/0, fab outputs, renders del enclosure (ambos repos).
- ⏳ GroovePush en protoboard: el prototipo anterior fue desmontado; Block 1 (primera nota USB-MIDI) no ha empezado.
- ⏳ PCBs físicas: el pedido está retenido por la auditoría del 2026-10-22.
- ⏳ El ladder 2N3904: no existe prototipo.

---

### EP1 — "Desarmé mi Push clone para construir un synth" (12 min)

**Enfoque:** el origen. Tenía un Push clone que funcionaba (clips, mixer, Remote Script), lo desarmó, y al lado
nació un synth. Los dos comparten cerebro. Se presentan las reglas que gobiernan toda la serie.

**Hook (0:00-0:45):** plano cerrado de la protoboard del Brain; tecla del controlador USB → nota del Model D con el
cutoff abriéndose (sketch49). Corte a la caja de piezas del Push desmontado. VO: *"Este synth funciona. Este
controlador lo desarmé. Y los dos van a usar exactamente la misma placa."*

**Bloques:**
1. **Las dos máquinas (0:45-3:00)** — mostrar `groovepush/CLAUDE.md` (diagrama de arquitectura) y
   `grooveforge-brain/CLAUDE.md` (audio path). Teensy 4.1 en mano.
2. **Las reglas inviolables (3:00-5:30)** — los 4 principios de GroovePush (MIDI de performance nunca toca la red,
   el audio nunca sale de la máquina) y la regla del Brain (el audio no depende de la cabeza, ADR-004 §1).
3. **Spec-first (5:30-8:00)** — `specs/openspec/`, `specs/adr/0001…0004`, `brain/apps/docs/00…06`. Por qué un maker
   solo trabaja con ADRs. Mostrar el commit `56e3aca` (harness SDD + agentes).
4. **La portadora compartida (8:00-10:30)** — `groovepush/hardware/boards/CONNECTORS.md` (diagrama de cables) y el
   render de la portadora del Brain. El PCB-S: un adaptador sin componentes que se monta en los zócalos vacíos del
   Audio Shield para sacar I2C y UART5.
5. **Lo que viene (10:30-12:00)** — mapa de la temporada.

**Clímax / demo:** ✅ sketch48 en cámara: controlador USB al host del Teensy, nota, audio por LINE OUT al monitor.
Medidor de nivel en pantalla.

**Shorts:**
1. **Mind-blow** — *"Un adaptador sin un solo componente"*: PCB-S, dos headers de 1×14 sobre los zócalos del Audio
   Shield; reusar la portadora del synth en el controlador sin rediseñarla. Archivo: `CONNECTORS.md` §PCB-S.
2. **Build/ASMR** — caja del Push desmontado → protoboard del Brain sonando. Sonido de las teclas Choc y del primer
   acorde. ✅
3. **Polémica** — *"Ableton cobra ~$1.000 por el Push 3. Yo lo estoy construyendo y esta es la regla que no voy a
   romper"*: la MIDI de performance nunca pasa por WiFi ni por la Pi. Diagrama de `CLAUDE.md`.

---

### EP2 — "6 synths legendarios en un microcontrolador de $30" (15 min)

**Enfoque:** DSP. Cómo cada engine emula a su original y dónde hace trampa. Pilar más fuerte para audiencia de
audio. 🟡 Apertura: snippets y fórmulas sí, fuente completo no.

**Hook:** seis notas, seis engines, mismo acorde, cortes de 2 s cada uno con el nombre en pantalla. VO: *"Un Moog,
un Juno, un Prophet, un OB-6, un DX7 y un ARP. En un chip que cabe en la uña."*

**Bloques:**
1. **La tabla de la vergüenza (0:45-3:00)** — `fidelidad-engines.md` §0: el porcentaje estimado de fidelidad de cada
   engine (Prophet 65 % de sonido, OB-6 35 %…). Honestidad como gancho.
2. **El filtro que se comía la CPU (3:00-6:00)** — `tanhf` ×7 por muestra, ~200 ciclos cada una, 48 % de CPU con
   6 voces. La fórmula Padé [7/6] en pantalla. Snippet de `fast_math.h`.
3. **Aliasing (6:00-8:30)** — saw ingenuo vs polyBLEP; espectrograma de los WAV de `tools/offline`. Número en
   pantalla: −23 dB → −70 dB en C6.
4. **El capacitor del envelope (8:30-10:30)** — `analog_env.h`: overshoot 1.3, curva cóncava como el CEM3310.
5. **Un filtro por chip (10:30-13:00)** — tabla de §4: ladder ZDF, OTA (IR3109/CEM3320), SEM SVF con morph.
6. **Cómo sé que suena bien sin oídos de oro (13:00-15:00)** — `validate_engines.cpp` y la tabla de §8 / §9.4: el
   ladder resonaba −1913 ¢ desafinado a 5 kHz; ahora ±5 ¢ de 110 Hz a 12 kHz. Las ❌ de la tabla se muestran tal cual.

**Clímax / demo:** ✅ barrido del cutoff con resonancia alta hasta la auto-oscilación del ladder, en el Brain real,
con el espectro de la cabeza de Studio en pantalla.

**Shorts:**
1. **Mind-blow** — *"Mi filtro desafinaba 19 semitonos al resonar"*: −1913 ¢ a 5 kHz → ±5 ¢ con el ladder ZDF.
   (Alternativa: Padé [7/6] vs `tanhf`; decir "8× menos, esperado" hasta medir en la Teensy.)
2. **Build/ASMR** — el mismo acorde por los 6 engines, cámara sobre el encoder ENGINE y la pantalla. ✅
3. **Polémica** — *"Mi Juno-106 suena al 50 %. Y te enseño por qué"*: la tabla de fidelidad; IR3109 vs OTA ladder.
   Comparativa con las reissues de $2.000-3.000 (`00-master-strategy.md` §1).

---

### EP3 — "El DX7 que no era FM" (11 min)

**Enfoque:** un solo engine en profundidad, porque tiene el mejor conflicto: la auditoría de mayo descubrió que no era
FM real. ADR-005 lo arregla con un objeto de audio propio.

**Hook:** dos versiones de un "E.PIANO": la vieja (`frequencyModulation`, 2 operadores) y la nueva (4 operadores
con feedback). VO: *"Este sonido tenía un bug que solo se oye en los agudos."*

**Bloques:**
1. **Qué es FM, en 90 segundos (0:45-3:00)** — modulación de fase vs de frecuencia; por qué el timbre cambia con la
   nota en la versión mala.
2. **El muro de los 128 samples (3:00-6:00)** — por qué el grafo de la Teensy Audio Library no puede hacer feedback
   de operador (2.9 ms de retraso a 44.1 kHz). ADR-005 en pantalla.
3. **El objeto propio (6:00-8:30)** — `dx7_core.h` (snippet del operador y del feedback), algoritmos, formas W1-W8
   (commit `7012b01`).
4. **Probar contra Bessel (8:30-10:00)** — bandas laterales medidas vs teoría en `validate_engines.cpp`.

**Clímax / demo:** ✅ feedback del operador subiendo poco a poco: de seno a metálico a ruido.

**Shorts:**
1. **Mind-blow** — *"Por qué tu synth FM no puede tener feedback"*: los bloques de 128 muestras.
2. **Build/ASMR** — perilla de feedback de 0 a máximo, solo audio y la forma de onda en la cabeza. ✅
3. **Polémica** — *"Yamaha usó 6 operadores. Yo uso 4. ¿Hago trampa?"*: ADR-005, tabla de las tres versiones del
   DX7 que convivían en el repo (spec 6 op, UI 4 op, firmware 2 op).

---

### EP4 — "El clic que desaparecía" (12 min)

**Enfoque:** encoders y la frontera hardware-firmware. Episodio de debugging puro: tres bugs del Brain (F1-F3) y dos
del Push (F8, F9). Ideal para ingenieros.

**Hook:** cámara cenital sobre un encoder; se gira despacio, clic, clic, clic, y el número en pantalla sube solo cada
dos clics. VO: *"Este encoder tiene un bug. No es el encoder."*

**Bloques:**
1. **Cuadratura en el analizador (0:45-3:00)** — señales A/B, 2 pulsos por detent medidos. ⏳ si no hay analizador
   lógico: osciloscopio o `sketch26` imprimiendo la cuenta cruda.
2. **Bug 1: dividir entre 4 (3:00-4:30)** — commit `625c304`.
3. **Bug 2: el valor que tiembla (4:30-6:30)** — `src/ui/detent.h` completo en pantalla (es corto y es abierto).
4. **Bug 3: el cutoff que no bajaba de 83 Hz (6:30-9:00)** — CC 74 lineal, 63 Hz por paso, el eco del DAW, commit
   `a3c588c`.
5. **En el Push: los pines que no son lo que parecen (9:00-12:00)** — GPA7/GPB7 del MCP23017 (G-P12) y los
   encoders sobre `Serial2` (G-P14). `PIN_MAP.md` antes/después.

**Clímax / demo:** ✅ en el Brain, el cutoff baja ahora de forma continua por debajo de 83 Hz con el DAW conectado.

**Shorts:**
1. **Mind-blow** — *"15 líneas que arreglan cualquier encoder barato"*: histéresis de `detent.h`.
2. **Build/ASMR** — macro del EC11 girando, con la traza A/B sincronizada. ⏳ (necesita el analizador/osciloscopio).
3. **Polémica** — *"El bug estaba en Ableton… o eso creía"*: el eco de MIDI que cuantizaba el cutoff.

---

### EP5 — "Una pantalla que obedece" (12 min)

**Enfoque:** la cabeza. Brain: Pi 3B + LVGL por UART con el bridge protocol. Push: Pi 5 + Qt/QML + 7" multitouch.
Por qué dos stacks distintos y una sola identidad visual (ADR-0003).

**Hook:** con el synth sonando, se desconecta la alimentación de la Pi. La pantalla se apaga; el audio sigue. VO:
*"Mi synth tiene un Linux adentro. Y lo puedo matar en pleno show."* ⏳ **verificar en cámara antes de prometerlo**:
la regla está en ADR-004 §1 (controles cableados al Teensy) pero no hay un test documentado de corte de la Pi.

**Bloques:**
1. **El frame (0:45-3:30)** — `[CMD][LEN][SEQ][PAYLOAD][CRC8]`, CRC-8 0x07, 921600 8N1. `02-bridge-protocol.md` §1.
2. **El bug del frame a medias (3:30-5:00)** — timeout de frame parcial también en GOT_CMD (commit `e4150bb`).
3. **UI_STATE: la cabeza no decide nada (5:00-7:30)** — `variants/studio/theory/04-studio-ui-state.md`; la cabeza
   solo pinta lo que el Teensy le manda (commit `e09d698`).
4. **Kiosko (7:30-9:00)** — systemd + udev (commit `3d074e4`), y el bug de `--uart /dev/ttyAMA0` (commit `a83de21`).
5. **El hermano en Qt (9:00-12:00)** — `groovepush/apps/gui/SerialController.cpp`, handshake + ping;
   `specs/adr/0003…` (tabla de tokens que no coincidían: teal `#00D4AA` vs `#1D9E75`).

**Clímax / demo:** ✅ vista PERFORM con la onda y el filtro animados en tiempo real mientras se toca (commit
`a3e2394`).

**Shorts:**
1. **Mind-blow** — *"Un byte que salva tu show"*: CRC-8 explicado con un frame real.
2. **Build/ASMR** — arranque en kiosko: pantalla negra → logo → PERFORM, con la onda moviéndose. ✅
3. **Polémica** — *"Pioneer y Roland meten Linux en sus equipos. Yo lo saqué del camino del audio"*: la regla del
   audio que no depende de la cabeza.

---

### EP6 — "Del CSV a la placa: diseñar PCBs con scripts" (14 min)

**Enfoque:** hardware. Cómo una tabla de coordenadas del panel produce el enclosure y las PCBs; DRC 0/0/0; Choc V2
con LED por debajo; reglas de JLC para pagar poco.

**Hook:** time-lapse de `place_pcb_a.py` + Freerouting sobre la PCB-A de GroovePush, que termina en "DRC: 0
violations, 0 unconnected". VO: *"No toqué el mouse para colocar estos componentes."*

**Bloques:**
1. **Una tabla manda (0:45-3:00)** — `groovepush/hardware/panel/panel-coordinates.csv` y el render del enclosure v2
   (`docs/design/claude-design-2026-10-19-v2/GroovePush 3D v2.html`).
2. **Colocar y rutear por script (3:00-6:30)** — `hardware/boards/tools/place_pcb_*.py`, `route_board.py`,
   `clean_vias.py`, `add_gnd_pours.py`. Lista de reglas de `lecciones-para-groovepush.md` §1.
3. **El contrato de conectores (6:30-9:00)** — `CONNECTORS.md`, IDC 2×15 1:1, JST-SH Qwiic.
4. **Teclas con luz (9:00-11:30)** — Choc V2 + SK6812-MINI-E montado por debajo (ADR-0004); una sola cadena de LEDs
   y un solo `write` por frame.
5. **Cómo pagar menos en JLC (11:30-14:00)** — SMD Economic en una cara, THT a mano, ≤ 100 × 100 mm, varios diseños
   en el mismo carrito, revisar rotaciones del CPL.

**Clímax / demo:** ✅ visor 3D de KiCad / GerbView de las cinco placas de GroovePush (PCB-A, F, K1, K2, S), commit
`80f0654`.

**Shorts:**
1. **Mind-blow** — *"El LED va debajo de la tecla"*: SK6812-MINI-E invertido y la ventana en el PCB.
2. **Build/ASMR** — time-lapse del autorouter + giro 3D de la placa. ✅
3. **Polémica** — *"La regla de los 100 mm que te ahorra la mitad del pedido"*: costo por tamaño en JLC.

---

### EP7 — "La auditoría que frenó el pedido" (13 min)

**Enfoque:** el episodio de conflicto de la temporada. Todo pasa DRC, todo está ruteado, y aun así no se manda a
fabricar. Por qué DRC no sabe que un pin tiene un LED.

**Hook:** el carrito de JLC con las placas cargadas, el cursor sobre "Pagar"… y se cierra la pestaña. VO: *"DRC
cero errores. ERC cero errores. Y no voy a pedir estas placas."*

**Bloques:**
1. **Lo que DRC no sabe (0:45-2:30)** — `auditoria-fabricacion-2026-10-22.md` §Método: DRC ve geometría, no
   circuitos internos de módulos ni piezas compradas.
2. **F1: el pin 13 (2:30-5:30)** — esquema oficial de la Teensy 4.1 (LED D3 + R1 470 Ω), ruta `ENC2.A → J2.18 → J5.18
   → pin 13`. Giro: en GroovePush ese pin quedó *spare* en `CONNECTORS.md`.
3. **F2: USB-C no es solo VBUS (5:30-8:00)** — CC1/CC2 y las Rd; la TVS "5.0" que clampa a 9.2 V.
4. **F3: la cuenta de los amperios (8:00-10:00)** — 2.5 A de Pi + Teensy + LEDs + host MIDI; 29 mΩ y 73 mV en cobre.
5. **F4: comprar por función, no por palanca (10:00-11:30)** — la tabla de continuidad del DP3T.
6. **También audito la auditoría (11:30-13:00)** — 13 bloqueantes, 4 reales, 5 falsos (`lecciones…` §8).

**Clímax / demo:** ⏳ en banco: encoder conectado al pin 13 con `INPUT_PULLUP`, multímetro/osciloscopio en la fase A
mostrando el nivel en reposo, y el mismo encoder en otro pin. (Es la prueba de cierre que pide la auditoría.)

**Shorts:**
1. **Mind-blow** — *"El pin de la Teensy que nunca deberías usar como entrada"*: pin 13 + LED + pull-up interno.
2. **Build/ASMR** — la medición en banco del pin 13. ⏳
3. **Polémica** — *"Mi PCB pasó DRC y estaba mal"*: DRC limpio ≠ placa que funciona.

---

### EP8 — "Saqué el filtro analógico de mi synth" (14 min) — final de temporada

**Enfoque:** la decisión más difícil: el ladder de 8 transistores 2N3904, el corazón del precio de $599, no entra al
Brain v1. Se cuenta con números y se abre la Temporada 2 (add-on + GroovePush manejando al Brain). También aquí entra
TinyML como "lo que sí está adentro". 🟡/🔴 apertura: ML solo concepto y números.

**Hook:** esquemático del ladder en pantalla, se tacha. VO: *"Este circuito era la razón por la que mi synth iba a
costar $599. Lo saqué."*

**Bloques:**
1. **Por qué el ladder era el riesgo #1 (0:45-4:00)** — `auditoria-tecnica-2026-05.md` §1: conversor exponencial sin
   definir, ~2 Vpp de headroom a 5 V para 1 Vrms; el doble ladder = 48 dB/oct.
2. **ADR-003 (4:00-6:30)** — el filtro como add-on con alimentación propia; el Brain saca CV de cutoff por el pin 29.
3. **La CV, simulada (6:30-8:30)** — doble RC de 4.7 k / 100 nF + seguidor MCP6004; 5.2 ms de asentamiento y
   ~348 µVpp de ripple en `03-studio-input-stage.md` / `sim/input_stage_sim.py`.
4. **Lo que sí va adentro: IA en kilobytes (8:30-11:30)** — key detector 19 KB int8 en flash vía `.rodata`
   (`sprints/23-key-detector.md`); accuracy ~94 % **en datos sintéticos** (`sprints/25`). Scale lock (`sketch24`).
   ⏳ confirmar en banco que la inferencia corre en la Teensy antes de decir "on-device" en cámara.
5. **Temporada 2 (11:30-14:00)** — GroovePush manejando al Brain por el USB-A host (ADR-0002 Rev. 1, *dirección, no
   spec*), el add-on GrooveForge Ladder y el pedido de PCB.

**Clímax / demo:** ✅ el `MoogLadder4P` digital auto-oscilando y tocando una melodía con el tracking del teclado.

**Shorts:**
1. **Mind-blow** — *"Una red neuronal que cabe en 19 KB"*: el key detector y por qué no copia a RAM.
2. **Build/ASMR** — barrido del ladder digital en auto-oscilación, solo audio y la cabeza animada. ✅
3. **Polémica** — *"Behringer clona un Moog por $300. Yo saqué el filtro de mi synth de $599"*: ADR-003 y el doble
   filtrado.

---

## Matriz resumen

| Ep | Repo dominante | Short Mind-blow | Short Build/ASMR | Short Polémica | ¿Grabable hoy? |
|---|---|---|---|---|---|
| 1 | ambos | PCB-S sin componentes | Push desarmado → Brain sonando | La MIDI no pasa por WiFi | ✅ |
| 2 | Brain | Padé 8× menos CPU | 6 engines, 1 acorde | Mi Juno al 50 % | ✅ |
| 3 | Brain | FM sin feedback | Feedback 0 → máx | 4 vs 6 operadores | ✅ |
| 4 | ambos | Histéresis en 15 líneas | EC11 + traza A/B | El eco del DAW | ✅ / ⏳ analizador |
| 5 | ambos | CRC-8 | Arranque kiosko | Linux fuera del audio | ✅ / ⏳ test de corte |
| 6 | GroovePush | LED bajo la tecla | Autorouter time-lapse | La regla de 100 mm | ✅ |
| 7 | Brain → Push | El pin 13 | Medición pin 13 | DRC limpio ≠ placa buena | ⏳ medición |
| 8 | Brain | Red en 19 KB | Ladder digital | Behringer vs yo | ✅ / ⏳ inferencia |
