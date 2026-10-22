# BIBLIA DE PRODUCCIÓN — Temporada 1 · "Dos cerebros, un banco"

> Documento maestro. Fusiona `01_borrador_claude.md` (estructura y precisión técnica) con
> `02_optimizacion_codex.md` (retención, packaging y rodaje), después de auditar el 02 contra los dos repos.
> Fecha: 2026-10-22. Repos: `groovepush` @ `65c1c4f`, `grooveforge-brain` @ `c32a4f9`.
>
> **Procedencia del 02:** Codex no se pudo invocar desde el contenedor de esta sesión (sin CLI ni credenciales de
> OpenAI). El 02 lo escribió Claude en el rol de Codex. Si después corrés el prompt real (`02_prompt_codex.md`),
> repetí la auditoría de la §1 sobre ese archivo antes de reemplazar nada de aquí.

**Cómo se usa:** antes de grabar un episodio, leé su ficha (§4), corré la lista de la §5 y grabá en el orden de la
tabla de sesión. Las tomas ⏳ no se graban hasta que existan: **nunca mostramos lo que no existe**.

---

## 1. Auditoría técnica del 02 (qué se corrigió y por qué)

| Ep | Lo que proponía el 02 | Problema | Versión final |
|---|---|---|---|
| 1 | "Desarmé el controlador que me costó un año" · título "Tiré un año de trabajo a la basura" | El tiempo no está documentado, y no se tiró nada: el código se reusa (`ROADMAP.md`: "reusamos los drivers y envs `test_*`") | "Desarmé mi Push clone que funcionaba" |
| 2 | Título "6 synths, 1 chip, 0 % de CPU sobrante" | Falso: el objetivo es ≤ 60 % de CPU (`01` §5.2) y la CPU real con 6 voces no está medida | Eliminado |
| 2 | "8× menos CPU" como hecho | Es el resultado **esperado**; falta medirlo en la Teensy (`fidelidad-engines.md` §1, §9.4) | Se dice "esperado" o se usa el dato medido: −1913 ¢ → ±5 ¢ |
| 2 | "Un chip de 30 dólares" | La placa Teensy 4.1 cuesta alrededor de eso; el chip no se vende suelto en ese formato | "una placa de ~30 dólares" |
| 3 | Título/miniatura "NO ERA FM", "mi synth FM no hacía FM" | **Técnicamente falso:** el engine viejo *sí* hacía modulación de frecuencia (`frequencyModulation()`). El DX7 hace modulación de **fase** (ADR-005). El error era otro | "Mi DX7 no era un DX7" · miniatura **"FASE, NO FRECUENCIA"** no entra en 3 palabras → **"NO ERA DX7"** |
| 3 | "Suena roto 3 octavas arriba" | La auditoría de mayo dice que el timbre cambia con la nota y hay aliasing arriba; cuánto "roto" se oye se comprueba al grabar | Se graba primero; si no se oye claro, el hook pasa a la comparación de espectros |
| 4 | "Por qué los encoders de Ableton no tiemblan y los míos sí" | No hay ninguna medición del Push de Ableton en los repos | "Por qué tu encoder barato tiembla (y cómo lo arreglé)" |
| 4 | "Culpé a Ableton" | El commit `a3c588c` habla del eco del **computador**, sin nombrar el DAW ni que se culpara a Ableton | "Mi filtro no bajaba de 83 Hz. El culpable era un eco" |
| 5 | "Le quité la computadora a mi synth en pleno show" | La regla existe (ADR-004 §1: controles cableados al Teensy), pero **no hay prueba documentada** de cortar la Pi con audio | ⏳ hook condicional: se graba solo si la prueba pasa en banco. Plan B en la ficha |
| 5 | "Pioneer mete Linux en el camino del audio. Yo no." | Afirmación sobre la arquitectura interna de un tercero que no está verificada | "Mi synth tiene Linux adentro. El audio no pasa por él" (sin nombrar marca) |
| 5 | "Mi pantalla se congelaba por un byte" | Casi: el commit `e4150bb` dice que un byte suelto que parecía CMD dejaba la recepción **esperando LEN para siempre** | "Un byte suelto colgaba mi protocolo" |
| 6 | "Freerouting" para GroovePush | GroovePush rutea con su **router propio por grilla** (`grid_route.py`, `finish_routing.py`, `repair_routes.py`, commit `80f0654`). Freerouting es el flujo del Brain (`lecciones…` §8) | Se nombra cada herramienta en su repo |
| 6 | "No coloqué ni un componente con el mouse" | Colocación por script (`place_pcb_*.py`) sí; no está documentado que no haya habido ajustes a mano | "Los componentes los colocó un script" |
| 6 | "Un milímetro me cuesta el doble" · "por menos que una cena" | El salto de precio sobre 100 × 100 mm existe (la auditoría avisa "no asumir la misma tarifa"), pero "el doble" y "una cena" no están cotizados | "100 mm: la frontera del precio base", con captura de la cotización real |
| 7 | "Nunca uses este pin como entrada" | PJRC desaconseja **`INPUT_PULLUP`** en el pin 13, no toda entrada | "Nunca le pongas INPUT_PULLUP a este pin" |
| 7 | "13 bloqueantes, 4 reales" junto a F1-F4 | Son dos auditorías distintas: los 13/4/5 son de la auditoría del 2026-10-18 (`lecciones…` §8); F1-F4 son de la del 2026-10-22 | Se presentan como dos momentos |
| 8 | "Una red neuronal más chica que esta foto" | El key detector ocupa 19 KB int8; vale como imagen si la foto en pantalla pesa más. La accuracy ~94 % es **en datos sintéticos** (`sprints/25`) | Se mantiene la imagen; el 94 % siempre con "sintético" |
| 8 | "On-device" implícito | La auditoría de mayo decía que la inferencia aún no corría en la Teensy; no hay medición posterior en lo leído | ⏳ verificar en banco antes de decir "corre en la Teensy" |
| 8 | Pesos / arquitectura del modelo | Política 🔴 (`01-modelo-rampa-y-apertura.md` §3.3) | Solo concepto y números |

**Se mantuvo del 02** (sin cambios): la regla "resultado en el segundo 0, pregunta antes del 5, promesa antes del
15"; los setups A-F + V; la sesión global de audio; casi todos los hooks visuales.

---

## 2. Reglas de la temporada

1. **Tono:** de ingeniero a creador. Números reales, archivo real en pantalla, errores contados con su commit.
2. **Estados:** ✅ existe y se graba hoy · ⏳ se graba cuando exista o cuando la prueba pase.
3. **Apertura** (`grooveforge-brain/apps/docs/content/01-modelo-rampa-y-apertura.md` §3.3):
   - 🟢 Abierto: FX, enclosure, protocolo, decisiones, errores, `detent.h`, scripts de PCB.
   - 🟡 Superficie: engines (snippets de ≤ 20 líneas y fórmulas, nunca un `.cpp` completo), valores finales del
     filtro, gerbers de producción.
   - 🔴 Cerrado: pesos, dataset, arquitectura exacta y receta de quantización de los modelos; backend de GroovePilot.
4. **En pantalla:** VS Code oscuro, fuente ≥ 20 pt, ruta del archivo visible en cada captura.
5. **Precios de marcas:** decir "desde ~" y mostrar la fuente el día de grabación. No afirmar cómo está construido
   por dentro un producto de otra marca.
6. **CTA único por pieza:** lista de email (playbook §6) o "comentá si querés probarlo" (beta testers).

---

## 3. Estado de lo grabable (2026-10-22)

| Qué | Estado | Fuente |
|---|---|---|
| Brain Studio en protoboard con sonido (USB host → voz → I2S → LINE OUT) | ✅ | `sketches/48-studio-e2e-hw.cpp`, `49-studio-brain.cpp` |
| Cabeza de Studio (LVGL, kiosk, PERFORM/PANEL) | ✅ | `apps/studio-head`, commits `a3e2394`, `3d074e4` |
| Validación offline de engines + WAVs | ✅ | `tools/offline/validate_engines.cpp` |
| PCBs de GroovePush y del Brain ruteadas, DRC 0/0/0, fab | ✅ (en pantalla) | `hardware/boards/fab/`, `apps/hardware/kicad/studio/fab/` |
| Enclosure GroovePush v2 (render) | ✅ (render) | `docs/design/claude-design-2026-10-19-v2/` |
| GroovePush en protoboard, primera nota USB-MIDI | ⏳ Block 1 sin empezar | `ROADMAP.md` |
| PCBs físicas | ⏳ pedido retenido | `auditoria-fabricacion-2026-10-22.md` |
| Ladder 2N3904 | ⏳ sin prototipo (add-on futuro) | ADR-003 |
| Inferencia TinyML en la Teensy | ⏳ verificar | `auditoria-tecnica-2026-05.md` §1.6 |
| Corte de la Pi con audio sonando | ⏳ probar | ADR-004 §1 |

**Orden de publicación recomendado** (por lo que ya se puede grabar, no por número): EP2 → EP3 → EP4 → EP6 → EP1 →
EP5 → EP7 → EP8. EP1 funciona mejor como "tráiler" cuando ya hay 3 episodios fuera.

---

## 4. Fichas por episodio

### EP1 — Desarmé mi Push clone para construir un synth (12 min)

**Título principal:** *Desarmé mi Push clone para construir un synth*
**A/B:** (R) *1 placa, 2 instrumentos: el truco que me ahorró rediseñar* · (M) *El Push 3 cuesta desde ~$1.000. Yo
construyo el mío* · (N) *Una placa de ~$30 y dos instrumentos* · (C) *Mi synth y mi controlador tienen el mismo cerebro*
**Miniatura:** mitad izquierda el Push desmontado en fondo oscuro con cables sueltos; mitad derecha la protoboard del
Brain iluminada en teal `#1D9E75` (paleta de ADR-0003). Flecha curva entre ambas. Cara abajo a la derecha mirando la
placa. Texto: **"MISMO CEREBRO"**.

**Hook final (0-15 s):**
- [0-2] Nota del Model D a volumen, cutoff abriéndose; macro de la Teensy. ✅
- [2-6] Caja del Push desmontado sobre la mesa. VO: *"Desarmé mi Push clone. Funcionaba."*
- [6-11] Las dos placas lado a lado. VO: *"Porque este synth y ese controlador van a usar el mismo cerebro… y la misma
  placa portadora."*
- [11-15] Texto "1 Teensy · 2 instrumentos". VO: *"Te muestro cómo, y las reglas que no voy a romper."*

**Bloques y archivos en pantalla:**
1. Las dos máquinas — `groovepush/CLAUDE.md` (diagrama), `grooveforge-brain/CLAUDE.md` (audio path).
2. Las reglas — principios 1 y 4 de `groovepush/CLAUDE.md`; ADR-004 §1 del Brain.
3. Spec-first — `specs/openspec/`, `specs/adr/0001…0004`, `brain/apps/docs/00…06`, commit `56e3aca`.
4. La portadora compartida — `hardware/boards/CONNECTORS.md` (diagrama + tabla de PCB-S), render de la portadora.
5. Mapa de la temporada.

**Clímax:** ✅ sketch48: controlador al USB host, nota, LINE OUT al monitor con medidor.

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo (≤ 45 s) | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | Dedo sobre una placa sin componentes: *"Esta placa no tiene ni un componente y me ahorró rediseñar"* | PCB-S: dos headers 1×14 en los zócalos vacíos del Audio Shield sacan I2C (18/19) y Serial5 (20/21) hacia el panel y el M4 | `CONNECTORS.md` §PCB-S | ✅ render / ⏳ física |
| 2 | Build/ASMR | Golpe de la caja desmontada; el acorde entra en el segundo 2 | Del Push desarmado a la protoboard sonando, sin voz | — | ✅ |
| 3 | Polémica | Router WiFi tachado: *"Esto nunca va a tocar una nota de mi Push"* | Push 3 desde ~$1.000; el mío manda la MIDI de performance por USB directo (< 5 ms), nunca por red ni por la Pi | `groovepush/CLAUDE.md` principio 1 | ✅ |

**Sesión:** A+E+V protoboard (10') → A+E sketch48 (10') → A+V caja (5') → A placas (5') → C docs (15') → D conectores
(10') → F narración (20').

---

### EP2 — Metí 6 synths legendarios en un microcontrolador (15 min)

**Título principal:** *Metí 6 synths legendarios en un microcontrolador*
**A/B:** (R) *Emulando un Moog, un Juno y un DX7 en un Cortex-M7* · (M) *Moog, Roland, Yamaha… en una placa de ~$30* ·
(E) *Mi Juno-106 suena al 50 % (y te muestro por qué)* · (N) *Mi filtro desafinaba 19 semitonos*
**Miniatura:** Teensy al centro en macro; detrás, seis siluetas de los synths en gris; solo el Juno en color con un
"50 %" rojo. Texto: **"6 SYNTHS"**.

**Hook final (0-15 s):**
- [0-6] Seis cortes de 1 s: un acorde por cada engine, nombre gigante. ✅
- [6-10] Teensy en la punta del dedo. VO: *"Seis synths clásicos. En una placa de 30 dólares."*
- [10-15] Tabla de fidelidad con el Juno en rojo. VO: *"Y uno suena a la mitad. Te digo cuál, y cómo lo mido."*

**Bloques y archivos:**
1. La tabla de la vergüenza — `fidelidad-engines.md` §0 (estimaciones de 2026-10-16, decirlo).
2. El filtro que se comía la CPU — `tanhf` ×7 por muestra, ~200 ciclos, 48 % con 6 voces (medido); Padé [7/6]
   en pantalla; snippet de `src/dsp/fast_math.h`. "8× menos" = **esperado**.
3. Aliasing — saw ingenuo vs polyBLEP: **−23 dB → −70 dB** en C6 (`fidelidad-engines.md` §8). Espectrogramas de
   `tools/offline`.
4. El capacitor del envelope — `src/dsp/analog_env.h`; la curva de ataque pasó de 0.83 a 0.63 a mitad de tiempo
   (§9.4).
5. Un filtro por chip — §4 y §9.4: ZDF ladder (Model D/ARP), ZDF con carácter IR3109 (Juno) y CEM3320 (Prophet),
   SEM SVF (OB-6, notch −80 dB). Citas: Huovilainen 2004, Zavalishin 2018.
6. Cómo lo mido — `validate_engines.cpp`: resonancia del ladder −1913 ¢ a 5 kHz → **±5 ¢ de 110 Hz a 12 kHz**.
   Mostrar las ❌ de §8 tal cual.

**Clímax:** ✅ barrido del cutoff hasta la auto-oscilación en el Brain, con el espectro en la cabeza.

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | Pico de espectro corriéndose: *"Mi filtro desafinaba 19 semitonos al resonar"* | A 5 kHz la auto-oscilación caía 1913 cents; con el ladder ZDF quedó en ±5 ¢ de 110 Hz a 12 kHz. Validado offline con el mismo código del firmware | `fidelidad-engines.md` §8, §9.4 | ✅ |
| 2 | Build/ASMR | Acorde + nombre del engine cada 1 s | Encoder ENGINE girando, pantalla cambiando, sin voz | — | ✅ |
| 3 | Polémica | "50 %" sobre el Juno: *"Mi Juno-106 suena al 50 %"* | La tabla honesta; IR3109 vs ladder Moog; las reissues cuestan miles (`00-master-strategy.md` §1), acá medimos qué falta | `fidelidad-engines.md` §0, §4 | ✅ |

**Sesión:** E 6 engines (20') → A+E+V encoder ENGINE (10') → A+E barrido (10') → C docs/snippets (25') → C correr
`./build.sh && ./validate_engines out` (15') → F (20').

---

### EP3 — Mi DX7 no era un DX7 (11 min)

**Título principal:** *Mi DX7 no era un DX7*
**A/B:** (R) *Programé FM de verdad porque la librería no podía* · (M) *Yamaha usó 6 operadores. Yo uso 4* · (N) *128
muestras que rompen cualquier synth FM* · (C) *Mi DX7 tenía un bug que solo se oye en los agudos*
**Miniatura:** forma de onda limpia arriba y otra deformada abajo separadas por un rayo; "DX7" en estilo LCD verde.
Texto: **"NO ERA DX7"**.

**Hook final (0-15 s):**
- [0-4] E.PIANO viejo en nota grave. ✅ (checkout de un commit anterior a ADR-005)
- [4-7] Misma patch tres octavas arriba. VO: *"Escuchá cómo cambia."* (⚠️ si la diferencia no se oye clara, usar
  los espectros de las dos notas lado a lado)
- [7-12] Versión nueva, misma nota. VO: *"Mi DX7 modulaba la frecuencia. El de Yamaha modula la fase."*
- [12-15] *"Y arreglarlo chocó contra un número: 128."*

**Bloques y archivos:**
1. FM vs PM en 90 s — por qué el timbre cambia con la nota si se modula la frecuencia.
2. El muro de los 128 samples — ADR-005: el grafo procesa en bloques de 128 (2.9 ms a 44.1 kHz); el feedback de
   operador llega tarde.
3. El objeto propio — snippet de `src/engines/dx7_core.h` (operador + feedback), formas W1-W8 (commit `7012b01`).
4. Contra Bessel — §8: bandas laterales iguales a J_n(I) en dos notas.
5. Las tres versiones del DX7 que convivían: spec 6 op, UI 4 op, firmware 2 op (tabla de ADR-005).

**Clímax:** ✅ feedback del operador de 0 a máximo: de seno a metálico a ruido.

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | "128" en pantalla: *"Por este número tu synth FM no puede tener feedback"* | Bloques de 128 muestras = 2.9 ms; un operador que se modula a sí mismo necesita la muestra anterior | ADR-005 | ✅ |
| 2 | Build/ASMR | Seno → ruido en 3 s, sin voz | Perilla de feedback y la onda en la cabeza | — | ✅ |
| 3 | Polémica | "6 → 4": *"Yamaha usó 6 operadores. Yo uso 4"* | Qué se pierde y qué se gana; el repo tenía tres DX7 distintos a la vez | ADR-005 | ✅ |

**Sesión:** E viejo/nuevo (15') → A+E+V feedback (10') → C docs (20') → F (15').

---

### EP4 — El clic que desaparecía (12 min)

**Título principal:** *El clic que desaparecía*
**A/B:** (R) *15 líneas que arreglan cualquier encoder barato* · (C) *Por qué tu encoder barato tiembla (y cómo lo
arreglé)* · (E) *Mi filtro no bajaba de 83 Hz. El culpable era un eco* · (N) *2 clics, 1 paso: el bug del encoder*
**Miniatura:** macro de un EC11 con dedo girando, traza A/B superpuesta en verde, "?" rojo. Texto: **"1 DE 2"**.

**Hook final (0-15 s):**
- [0-5] Cenital: clic, clic, el número sube una vez. VO: *"Dos clics. Un paso."* ✅ (firmware con divisor 4)
- [5-10] Encoder quieto, el número tiembla. VO: *"Y cuando no lo toco, se mueve solo."* ✅ (`raw >> 1`)
- [10-15] *"Tres bugs. Ninguno era el encoder."*

**Bloques y archivos:**
1. Cuadratura — A/B, 2 pulsos por detent medidos (2026-10-19). ⏳ analizador u osciloscopio; plan B:
   `sketches/26-encoder-test.cpp` imprimiendo la cuenta cruda.
2. Bug 1: dividir entre 4 — commit `625c304`.
3. Bug 2: el temblor — `src/ui/detent.h` completo (🟢 abierto), commit `3f3dc1b`.
4. Bug 3: 83 Hz — CC 74 lineal (63 Hz/paso), el computador devuelve el CC, log + ignorar el eco 150 ms; commit
   `a3c588c`.
5. En GroovePush: GPA7/GPB7 solo-salida (G-P12, commit `02591ff`) y Enc3/Enc4 sobre `Serial2` (G-P14, commit
   `853ab24`); `apps/processor/PIN_MAP.md`, `GAPS_AND_IMPROVEMENTS.md`.

**Clímax:** ✅ cutoff bajando de forma continua por debajo de 83 Hz con el computador conectado.

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | Número temblando: *"Tu encoder barato no está roto"* | El contacto vibra ±1 pulso; contar detents con histéresis (`DetentCounter::update`) | `src/ui/detent.h` | ✅ |
| 2 | Build/ASMR | Macro EC11 + traza A/B | Giro lento, los dos canales desfasados, sin voz | — | ⏳ instrumento |
| 3 | Polémica | Display clavado en "83 Hz": *"Mi filtro no bajaba de 83 Hz"* | CC 74 lineal = 63 Hz por paso; el eco del computador cuantizaba cada edición al paso 1 = 82.8 Hz | commit `a3c588c` | ✅ |

**Sesión:** A+V encoder con bug (10') → B+V A/B (20') → A temblor/arreglo (10') → A+E cutoff (15') → C commits y
PIN_MAP (20') → F (15').

---

### EP5 — Mi synth tiene Linux adentro. El audio no pasa por él (12 min)

**Título principal:** *Mi synth tiene Linux adentro. El audio no pasa por él*
**A/B:** (C) *Le quité la computadora a mi synth mientras sonaba* (⏳ solo si la prueba pasa) · (R) *Una pantalla
que no puede matar el audio* · (E) *Un byte suelto colgaba mi protocolo* · (N) *921.600 baudios y un byte de CRC*
**Miniatura:** mano sacando el cable de la Pi, pantalla negra, medidor de audio en verde. Texto: **"SIGUE SONANDO"**
(⏳ misma condición; si no, **"UN BYTE"** sobre un frame en hex).

**Hook final (0-15 s):**
- **Opción A** (si la prueba de corte pasa en banco): [0-3] synth sonando con la pantalla animada → [3-6] mano tira
  del cable de la Pi → [6-10] pantalla negra, el audio sigue. VO: *"Le acabo de quitar la computadora a mi synth."*
  → [10-15] *"Y siguió sonando. Así se diseña para que pase."*
- **Opción B** (✅ hoy): [0-4] frame en hex, un byte en rojo. VO: *"Este byte colgaba la comunicación de mi synth."*
  → [4-10] pantalla de la cabeza congelada / animación detenida (recreación con el commit anterior a `e4150bb`) →
  [10-15] *"Arreglarlo me obligó a diseñar una pantalla que no manda nada."*

**Bloques y archivos:**
1. El frame — `[CMD][LEN][SEQ][PAYLOAD][CRC8]`, CRC-8 poly 0x07, 921600 8N1 (`02-bridge-protocol.md` §1,
   `apps/bridge-protocol/include/`).
2. El byte suelto — commit `e4150bb`: la recepción esperaba LEN para siempre; timeout de frame parcial.
3. La cabeza solo pinta — `variants/studio/theory/04-studio-ui-state.md`, commit `e09d698`.
4. Kiosko — systemd + udev (commit `3d074e4`), `--uart /dev/ttyAMA0` (commit `a83de21`).
5. El hermano en Qt — `groovepush/apps/gui/SerialController.cpp` (handshake + ping), ADR-0003 (tabla de tokens que
   no coincidían, teal `#00D4AA` vs `#1D9E75`).

**Clímax:** ✅ vista PERFORM con onda y filtro animados mientras se toca (commit `a3e2394`).

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | Frame en hex, byte en rojo: *"Un byte salva tu show"* | Qué detecta un CRC-8 y qué pasa con un frame a medias | `02-bridge-protocol.md` §1, `e4150bb` | ✅ |
| 2 | Build/ASMR | Pantalla negra → PERFORM | Arranque en kiosko en time-lapse | — | ✅ |
| 3 | Polémica | *"Mi synth tiene Linux. El audio no pasa por él"* | Controles cableados al Teensy; la Pi solo dibuja. Sin nombrar marcas | ADR-004 §1 | ✅ texto / ⏳ prueba de corte |

**Sesión:** A+E+V prueba de corte (10', decide la opción del hook) → A+V kiosko (5') → A+E PERFORM (10') → C
docs/commits (25') → F (15').

---

### EP6 — Una tabla diseñó mi PCB (14 min)

**Título principal:** *Una tabla diseñó mi PCB (y mi caja)*
**A/B:** (R) *Diseño PCBs con scripts* · (N) *5 placas, 0 errores de DRC* · (E) *100 mm: la frontera del precio de
tu PCB* · (M) *Las teclas de mi Push clone tienen la luz por debajo*
**Miniatura:** render 3D de la PCB-A con rutas a medio completar, cursor del mouse tachado. Texto: **"SIN MOUSE"**.

**Hook final (0-15 s):**
- [0-5] Time-lapse del router propio llenando la PCB-A. ✅
- [5-9] "DRC: 0 violations, 0 unconnected" en verde. VO: *"Los componentes de esta placa los colocó un script."*
- [9-15] `panel-coordinates.csv` en pantalla. VO: *"Y esta tabla diseña a la vez la placa y la caja. Te muestro el
  pipeline."*

**Bloques y archivos:**
1. Una tabla manda — `hardware/panel/panel-coordinates.csv`, render `docs/design/claude-design-2026-10-19-v2/`.
2. Colocar y rutear — GroovePush: `place_pcb_*.py`, `grid_route.py`, `finish_routing.py`, `repair_routes.py`,
   `add_gnd_pours.py` (commit `80f0654`). Brain: Freerouting `.dsn` → `.ses` + `clean_vias.py`
   (`lecciones-para-groovepush.md` §8).
3. Contrato de conectores — `CONNECTORS.md`: IDC 2×15 1:1, JST-SH en orden Qwiic.
4. Teclas con luz — Choc V2 + SK6812-MINI-E en la cara inferior (ADR-0004); una sola cadena, un solo `write` por
   frame (`lecciones…` §6).
5. Pagar menos en JLC — SMD Economic en una cara, THT a mano, ≤ 100 × 100 mm, varios diseños en un carrito,
   revisar rotaciones del CPL (`lecciones…` §2). Captura de la cotización real.

**Clímax:** ✅ visor 3D de KiCad con las cinco placas (PCB-A, F, K1, K2, S).

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | Tecla con la luz saliendo por debajo: *"El LED va debajo de la tecla"* | SK6812-MINI-E montado invertido con ventana en la PCB | ADR-0004 | ✅ render / ⏳ física |
| 2 | Build/ASMR | Time-lapse del router | Hasta DRC 0/0/0 y giro 3D | — | ✅ |
| 3 | Polémica | Dos contornos, 100 y 101 mm: *"Este milímetro cambia el precio"* | Cotización real en pantalla; por qué la portadora mide 97 × 100 mm | auditoría 2026-10-22 (dimensiones), `lecciones…` §1 | ✅ |

**Sesión:** D+V router (30', acelerar) → D render y 3D (15') → D conectores + cotización (15') → A+V tecla (10') →
F (15').

---

### EP7 — No pagué este pedido de PCB (13 min)

**Título principal:** *No pagué este pedido de PCB. Esta es la razón*
**A/B:** (E) *Mi PCB pasó DRC y estaba mal* · (R) *La auditoría que encontró 4 fallas en una placa "perfecta"* ·
(N) *El pin 13: nunca le pongas INPUT_PULLUP* · (C) *DRC dice que está bien. La Teensy dice que no*
**Miniatura:** carrito de JLC con "Pay" tachado; zoom circular al pin 13 con el LED encendido. Texto: **"NO PAGUÉ"**.

**Hook final (0-15 s):**
- [0-4] Carrito de JLC, cursor sobre "Pay". ✅
- [4-7] Se cierra la pestaña. VO: *"DRC cero errores. ERC cero errores. Y no pago."*
- [7-12] Zoom al pin 13. VO: *"Porque este pin tiene un LED que ningún software de PCB ve."*
- [12-15] *"Y hay tres problemas más."*

**Bloques y archivos:**
1. Lo que DRC no sabe — `brain/apps/hardware/kicad/studio/docs/auditoria-fabricacion-2026-10-22.md` §Método.
2. F1: pin 13 — esquema oficial de PJRC (LED D3 + R1 470 Ω), ruta `ENC2.A → J2.18 → J5.18 → J2.14 → pin 13`.
   Cruce: en GroovePush J1.18 quedó "spare (Teensy 13)" (`CONNECTORS.md`).
3. F2: USB-C — la portadora solo recibe VBUS/GND; Rd en CC1/CC2; la TVS "5.0" clampa a 9.2 V.
4. F3: amperios — fusible mSMD300 (hold 3 A / trip 5 A), XH genérico, IDC 1 A/contacto; ~29 mΩ y ~73 mV en cobre a
   2.5 A (estimación, decirlo).
5. F4: el selector — DP3T real; tabla de continuidad.
6. Auditar la auditoría — la auditoría anterior (2026-10-18): 13 "bloqueantes", 4 reales, 5 falsos
   (`lecciones…` §8).

**Clímax:** ⏳ en banco: encoder en el pin 13 con `INPUT_PULLUP` vs otro pin; nivel de la fase A en reposo y al
girar. Es la prueba de cierre de F1. Si todavía no se hizo, el episodio se publica después.

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | Macro del LED de la Teensy: *"Nunca le pongas INPUT_PULLUP a este pin"* | LED + 470 Ω en el pin 13 tiran la línea hacia abajo; PJRC lo advierte | auditoría F1 | ✅ |
| 2 | Build/ASMR | Punta del multímetro en el pin, número en pantalla | La medición de cierre | — | ⏳ |
| 3 | Polémica | "DRC ✓" que pasa a "✗": *"Mi PCB pasó DRC y estaba mal"* | DRC ve geometría, no módulos ni piezas compradas | auditoría §Método | ✅ |

**Sesión:** D carrito (5') → A+V macro pin 13 (5') → B+V medición (20') → C+D auditoría y KiCad (25') → F (15').

---

### EP8 — Saqué el filtro analógico de mi synth (14 min) · final de temporada

**Título principal:** *Saqué el filtro analógico de mi synth*
**A/B:** (E) *La decisión que cambió el precio de mi synth* · (R) *Una red neuronal de 19 KB dentro de un synth* ·
(M) *Hay clones de Moog por ~$300. Yo le saqué el filtro al mío* · (N) *8 transistores que no entraron*
**Miniatura:** esquemático del ladder con una X roja; a la derecha el Brain con la pantalla encendida. Texto:
**"LO SAQUÉ"**.

**Hook final (0-15 s):**
- [0-4] Esquemático del ladder impreso, se tacha con marcador. VO: *"Este circuito era la razón del precio de mi
  synth."* ✅
- [4-8] *"Lo saqué."*
- [8-15] Auto-oscilación del `MoogLadder4P` digital tocando una melodía. VO: *"Lo que lo reemplaza suena así. Esta es
  la decisión más difícil del proyecto."* ✅

**Bloques y archivos:**
1. El riesgo #1 — `auditoria-tecnica-2026-05.md` §1: conversor exponencial sin definir, ~2 Vpp de headroom a 5 V
   para 1 Vrms, doble ladder = 48 dB/oct.
2. ADR-003 — el ladder como add-on con alimentación propia; CV de cutoff por el pin 29.
3. La CV simulada — `variants/studio/theory/03-studio-input-stage.md`, `sim/input_stage_sim.py`: 5.2 ms de
   asentamiento, ~348 µVpp de ripple (dentro del modelo, decirlo).
4. Lo que sí va adentro — key detector de 19 KB int8 leído desde flash (`sprints/23`); ~94 % **en datos
   sintéticos** (`sprints/25`); scale lock (`sketch24`). 🟡 sin pesos ni arquitectura. ⏳ verificar inferencia en la
   Teensy antes de decir "corre en el synth".
5. Temporada 2 — GroovePush manejando al Brain por el USB-A host (ADR-0002 Rev. 1, **dirección, no spec**), el
   add-on y el pedido de PCB.

**Clímax:** ✅ ladder digital en auto-oscilación con tracking del teclado.

**Shorts:**
| # | Ángulo | Hook 0-3 s | Cuerpo | Archivo | Estado |
|---|---|---|---|---|---|
| 1 | Mind-blow | "19 KB" gigante: *"Una red neuronal más chica que esta foto"* | Int8 en `.rodata`: flash, no RAM. Número de accuracy siempre con "sintético" | `sprints/23`, `25` | ✅ concepto / ⏳ on-device |
| 2 | Build/ASMR | Silbido de auto-oscilación, sin voz | Barrido del ladder digital con la cabeza animada | — | ✅ |
| 3 | Polémica | *"Hay clones de Moog por 300. Yo le saqué el filtro al mío"* | Por qué un filtro mono global sobre 6 engines poly era un problema, y por qué add-on | ADR-003 | ✅ |

**Sesión:** A tachar esquemático (5') → A+E+V auto-oscilación (15') → A+E scale lock (10') → C docs (20') → F (20').

---

## 5. Lista previa a cada sesión

- [ ] Las tomas ⏳ del episodio están verificadas en banco (o el episodio se pospone).
- [ ] Commit del firmware de la sesión anotado (para "antes/después": el commit anterior al fix).
- [ ] Ninguna captura muestra un `.cpp` completo de un engine ni archivos de `apps/training/models/*/artifacts/`.
- [ ] Precios de marcas comprobados el mismo día, con la fuente guardada.
- [ ] Cadena de audio E igual a la sesión global (mismo nivel, 48 kHz / 24 bit).
- [ ] Cámara V encendida en cada toma marcada "+V".

## 6. Sesión global de audio (una vez, para toda la temporada)

En setup E, con la misma cadena: 6 engines × el mismo acorde · auto-oscilación del ladder · DX7 viejo/nuevo en
grave y agudo · feedback del operador 0 → máx · cutoff antes/después de `a3c588c` · scale lock · arranque de la
cabeza (sonido ambiente). Nombrar los archivos `epN_tomaM_descripcion.wav`.

## 7. Pendientes que dependen del proyecto, no del rodaje

| Bloquea | Qué hace falta | Dónde |
|---|---|---|
| EP7 clímax | Prueba de cierre de F1 (pin 13) | `auditoria-fabricacion-2026-10-22.md` §Orden de cierre 1 |
| EP5 opción A | Prueba de cortar la Pi con audio sonando | ADR-004 §1 |
| EP8 bloque 4 | Inferencia TinyML en la Teensy, medida | `apps/firmware-teensy/src/ml/` |
| EP2 "8× menos" | CPU real con 6 voces | `fidelidad-engines.md` §9.4 "Pendiente on-device" |
| Temporada 2 | GroovePush en protoboard (Block 1+), PCBs físicas, add-on del ladder | `ROADMAP.md`, ADR-003 |
