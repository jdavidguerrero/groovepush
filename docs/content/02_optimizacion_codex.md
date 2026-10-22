# 02 · Optimización de retención y packaging (rol Codex)

> **Procedencia:** en esta sesión no se pudo invocar a Codex: el contenedor no tenía la CLI `codex` ni credenciales
> de OpenAI. Este archivo lo escribió **Claude en el rol de Codex**, con el prompt exacto de la Etapa 3
> (`02_prompt_codex.md`). Para tener la versión de OpenAI, corré ese prompt en tu máquina y repetí la Etapa 4.
>
> Entrada: `01_borrador_claude.md`. Criterio del rol: cortar todo lo que demora la promesa, priorizar la retención y
> el CTR. Lo técnico se audita en la Etapa 4.

---

## 1. Auditoría de retención

**Diagnóstico general del borrador:** los hooks tienen buena imagen, pero en varios episodios llega primero la
explicación y después el resultado ("Las dos máquinas", "Qué es FM en 90 segundos"). Regla aplicada: **resultado o
problema en el segundo 0, una pregunta abierta antes del segundo 5 y la promesa del episodio antes del 15.** Nada de
logo, saludo ni "en este video…".

### EP1
- **0-15 s (reescrito):** [0-2] Nota del Model D a todo volumen, cutoff abriéndose, plano macro de la Teensy. [2-6]
  Corte seco a la caja del Push desmontado cayendo sobre la mesa. VO: *"Desarmé el controlador que me costó un año."*
  [6-11] Las dos placas lado a lado, el mismo chip. VO: *"Porque este synth y ese Push van a compartir el mismo
  cerebro… y la misma placa."* [11-15] Texto en pantalla: "1 Teensy · 2 instrumentos". VO: *"Hoy te muestro cómo."*
- **Short 1, 0-3 s:** dedo señalando una placa vacía de componentes. VO: *"Esta placa no tiene ni un componente. Y
  salva mi proyecto."*
- **Short 2, 0-3 s:** sin voz; golpe de la caja desmontada, y en el segundo 2 entra el acorde.
- **Short 3, 0-3 s:** un router WiFi tachado en rojo. VO: *"Esto nunca va a tocar una nota de mi Push."*

### EP2
- **0-15 s:** [0-6] seis cortes de 1 s, seis engines, un acorde, nombre gigante en cada corte. [6-10] Teensy en la
  punta del dedo. VO: *"Seis synths que juntos cuestan más que un auto usado. En un chip de 30 dólares."* [10-15]
  Tabla de fidelidad con el Juno en rojo. VO: *"Y uno suena a la mitad. Te digo cuál y por qué."*
- **Short 1, 0-3 s:** espectro con un pico corriéndose. VO: *"Mi filtro desafinaba 19 semitonos."*
- **Short 2, 0-3 s:** acorde + nombre del engine, cada 1 s.
- **Short 3, 0-3 s:** "50 %" gigante sobre una foto del Juno. VO: *"Mi Juno-106 suena al 50 %."*

### EP3
- **0-15 s:** [0-4] E.PIANO viejo en nota grave: suena bien. [4-7] La misma nota 3 octavas arriba: suena roto. VO:
  *"Escuchá esto."* [7-12] Versión nueva, misma nota: limpia. VO: *"Mi DX7 tenía un bug que solo se oye arriba."*
  [12-15] *"Y la causa son 128 muestras."*
- **Short 1, 0-3 s:** "128" en pantalla. VO: *"Por este número tu synth FM no puede tener feedback."*
- **Short 2, 0-3 s:** el operador pasa de seno a ruido en 3 s, sin voz.
- **Short 3, 0-3 s:** "6 → 4". VO: *"Yamaha usó 6 operadores. Yo uso 4."*

### EP4
- **0-15 s:** [0-5] cenital: clic, clic, el número en pantalla sube solo una vez. VO: *"Dos clics. Un paso."* [5-10]
  Encoder en reposo, el número tiembla solo. VO: *"Y cuando no lo toco, se mueve."* [10-15] *"Tres bugs, ninguno era
  el encoder. Vamos."*
- **Short 1, 0-3 s:** número temblando en reposo. VO: *"Tu encoder barato no está roto."*
- **Short 2, 0-3 s:** macro del EC11 + traza A/B entrando por la derecha.
- **Short 3, 0-3 s:** cutoff clavado en "83 Hz". VO: *"Mi filtro no bajaba de 83 Hz. Culpé a Ableton."*

### EP5
- **0-15 s:** [0-3] synth sonando con la pantalla animada. [3-6] Mano tira del cable de alimentación de la Pi. [6-10]
  Pantalla negra, el audio sigue. VO: *"Le acabo de quitar la computadora a mi synth."* [10-15] *"Y no le importó. Esto
  es lo que cuesta diseñar así."*
- **Short 1, 0-3 s:** un frame en hex con un byte en rojo. VO: *"Un byte salva tu show."*
- **Short 2, 0-3 s:** pantalla negra → PERFORM en time-lapse.
- **Short 3, 0-3 s:** cable desconectado + audio sigue. VO: *"Pioneer pone Linux en el camino del audio. Yo no."*

### EP6
- **0-15 s:** [0-5] time-lapse del autorouter llenando la PCB. [5-9] "DRC: 0 violations" en verde. VO: *"No coloqué
  ni un componente con el mouse."* [9-15] CSV en pantalla. VO: *"Una tabla de Excel diseñó esta placa y la caja. Te
  muestro el pipeline."*
- **Short 1, 0-3 s:** tecla levantada, luz saliendo por debajo. VO: *"El LED va debajo de la tecla."*
- **Short 2, 0-3 s:** autorouter time-lapse.
- **Short 3, 0-3 s:** dos placas, una de 100 mm y otra de 101 mm. VO: *"Un milímetro me cuesta el doble."*

### EP7
- **0-15 s:** [0-4] carrito de JLC, cursor sobre "Pagar". [4-7] se cierra la pestaña. VO: *"DRC cero errores. Y no
  pago."* [7-12] zoom al pin 13 de la Teensy. VO: *"Porque este pin tiene un secreto que ningún software ve."* [12-15]
  *"Y encontré tres más."*
- **Short 1, 0-3 s:** zoom al LED naranja de la Teensy. VO: *"Nunca uses este pin como entrada."*
- **Short 2, 0-3 s:** punta del multímetro tocando el pin, número en pantalla.
- **Short 3, 0-3 s:** "DRC ✓" que se vuelve "✗". VO: *"Mi PCB pasó DRC y estaba mal."*

### EP8
- **0-15 s:** [0-4] esquemático del ladder, se tacha con marcador rojo. VO: *"Este circuito justificaba el precio de
  mi synth."* [4-8] *"Lo saqué."* [8-15] auto-oscilación del filtro digital tocando una melodía. VO: *"Y lo que lo
  reemplazó suena así. Esta es la decisión más difícil del proyecto."*
- **Short 1, 0-3 s:** "19 KB" gigante. VO: *"Una red neuronal más chica que esta foto."*
- **Short 2, 0-3 s:** silbido de auto-oscilación subiendo, sin voz.
- **Short 3, 0-3 s:** logo genérico "clon de $300" vs el Brain. VO: *"Clonan un Moog por 300. Yo le saqué el filtro
  al mío."*

---

## 2. Packaging y CTR (A/B)

Psicologías: **C** curiosidad extrema · **R** reto de ingeniería · **M** comparativa con marca · **E** error /
confesión · **N** número concreto.

### EP1
1. (C) Desarmé mi Push clone para construir un synth
2. (R) 1 placa, 2 instrumentos: el truco de diseño que me ahorró meses
3. (M) Ableton cobra $1.000 por el Push 3. Yo construyo el mío
4. (E) Tiré un año de trabajo a la basura (a propósito)
5. (N) Un Teensy de $30 y dos instrumentos de verdad
- **Miniatura:** mitad izquierda el Push desmontado en fondo oscuro, cables sueltos; mitad derecha la protoboard del
  Brain iluminada en teal. Flecha curva de un lado al otro. Cara del creador abajo a la derecha, mirando la placa.
  Texto: **"MISMO CEREBRO"**.

### EP2
1. (C) Metí 6 synths legendarios en un chip del tamaño de una uña
2. (R) Emulando un Moog, un Juno y un DX7 en un Cortex-M7
3. (M) Moog, Roland, Yamaha… en $30 de hardware
4. (E) Mi Juno-106 suena al 50 % (y te muestro por qué)
5. (N) 6 synths, 1 chip, 0 % de CPU sobrante
- **Miniatura:** la Teensy al centro en macro; detrás, seis siluetas de los synths clásicos en gris. Una sola en
  color (el Juno) con un "50 %" rojo encima. Texto: **"6 SYNTHS"**.

### EP3
1. (C) Mi DX7 tenía un bug que solo se oye en los agudos
2. (R) Programé FM real porque la librería no podía
3. (M) Yamaha usó 6 operadores. Yo uso 4
4. (E) Durante meses mi synth FM no hacía FM
5. (N) 128 muestras que rompen cualquier synth FM
- **Miniatura:** forma de onda limpia arriba y rota abajo, separadas por un rayo; "DX7" estilo display LCD verde.
  Texto: **"NO ERA FM"**.

### EP4
1. (C) El clic que desaparecía
2. (R) 15 líneas que arreglan cualquier encoder barato
3. (M) Por qué los encoders de Ableton no tiemblan y los míos sí
4. (E) Culpé a Ableton. El bug era mío
5. (N) 2 clics, 1 paso: el bug del encoder
- **Miniatura:** macro de un encoder EC11 con dedo girando; traza A/B superpuesta en verde; un "?" rojo. Texto:
  **"1 DE 2"**.

### EP5
1. (C) Le quité la computadora a mi synth en pleno show
2. (R) Una pantalla que no puede matar el audio
3. (M) Pioneer mete Linux en sus equipos. Yo lo saqué del audio
4. (E) Mi pantalla se congelaba por un byte
5. (N) 921.600 baudios y un byte de CRC
- **Miniatura:** mano sacando el cable de la Pi, pantalla negra, medidor de audio en verde vivo. Texto: **"SIGUE SONANDO"**.

### EP6
1. (C) Una hoja de cálculo diseñó mi PCB
2. (R) Diseño PCBs sin tocar el mouse
3. (M) Placas tipo Push 3 por menos que una cena
4. (E) Un milímetro que duplica el precio de tu PCB
5. (N) 5 placas, 0 errores de DRC
- **Miniatura:** render 3D de la PCB-A con el autorouter a medio camino; cursor del mouse tachado. Texto: **"SIN MOUSE"**.

### EP7
1. (C) No pagué este pedido de PCB. Esta es la razón
2. (R) La auditoría que encontró 4 fallas en una placa "perfecta"
3. (M) DRC dice que está bien. La Teensy dice que no
4. (E) Mi PCB pasó DRC y estaba mal
5. (N) El pin 13: el pin que nunca deberías usar
- **Miniatura:** captura del carrito de JLC con botón "Pay" tachado; zoom circular al pin 13 con el LED encendido.
  Texto: **"NO PAGUÉ"**.

### EP8
1. (C) Saqué el filtro analógico de mi synth
2. (R) Una red neuronal en 19 KB dentro de un synth
3. (M) Behringer clona un Moog por $300. Yo hice esto
4. (E) La decisión que cambió el precio de mi synth
5. (N) 8 transistores que no entraron
- **Miniatura:** el esquemático del ladder con una X roja gigante; a la derecha el Brain con la pantalla encendida.
  Texto: **"LO SAQUÉ"**.

---

## 3. Master Shot List

**Lógica:** cada episodio se graba en **una sesión** agrupando por *setup* (no por orden del guion), así no se
mueven luces ni cámaras más de una vez. Los Shorts se graban **verticales en la misma toma** (cámara 2 en 9:16) o se
reencuadran de un master 4K.

**Setups:**

| Código | Setup | Equipo |
|---|---|---|
| **A** | Cenital macro sobre el banco | cámara cenital 4K, macro, luz suave + contraluz teal |
| **B** | Banco de medición | osciloscopio/analizador lógico/multímetro, cámara 45° + captura de pantalla del instrumento |
| **C** | Pantalla: código y docs | OBS 1440p/4K, VS Code tema oscuro, fuente grande (≥ 20 pt) |
| **D** | Pantalla: KiCad / 3D / JLC | OBS, KiCad, visor 3D, navegador |
| **E** | Audio directo | LINE OUT → interfaz, 48 kHz / 24 bit, sin compresión; grabar siempre en paralelo con A |
| **F** | Talking head | cámara frontal, micrófono de solapa |
| **V** | Vertical dedicada | celular en 9:16 junto a la cámara A |

### EP1 — orden de sesión
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | A+E+V | Protoboard del Brain: nota del Model D, cutoff abriéndose (sketch49) | hook, Short 2 | 10 min |
| 2 | A+E | sketch48: controlador USB al host, nota, medidor | clímax | 10 min |
| 3 | A+V | Caja del Push desmontado cayendo, piezas | hook, Short 2 | 5 min |
| 4 | A | Teensy en mano, placas lado a lado | hook, bloque 1 | 5 min |
| 5 | C | `groovepush/CLAUDE.md` (diagrama), `grooveforge-brain/CLAUDE.md` (audio path), `specs/adr/` | bloques 1-3, Short 3 | 15 min |
| 6 | D | `hardware/boards/CONNECTORS.md` §PCB-S, render de la portadora | bloque 4, Short 1 | 10 min |
| 7 | F | bloques 2-5 y CTAs | todo | 20 min |

### EP2
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | E | Mismo acorde × 6 engines (3 tomas por engine) | hook, Short 2 | 20 min |
| 2 | A+E+V | Encoder ENGINE + pantalla cambiando | hook, Short 2 | 10 min |
| 3 | A+E | Barrido del cutoff hasta auto-oscilación | clímax | 10 min |
| 4 | C | `fidelidad-engines.md` §0, §1, §4, §8, §9.4; `fast_math.h`, `analog_env.h`, `polyblep_core.h` (snippets) | bloques 1-5, Shorts 1/3 | 25 min |
| 5 | C | Correr `tools/offline/build.sh && ./validate_engines out`, abrir espectrogramas | bloques 3/6 | 15 min |
| 6 | F | Explicaciones y Short 3 a cámara | todo | 20 min |

### EP3
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | E | E.PIANO viejo vs nuevo, nota grave y aguda (checkout de un commit anterior a ADR-005) | hook | 15 min |
| 2 | A+E+V | Feedback del operador de 0 a máximo | clímax, Short 2 | 10 min |
| 3 | C | ADR-005, `dx7_core.h` (snippet), reporte Bessel de `validate_engines` | bloques 2-4, Shorts 1/3 | 20 min |
| 4 | F | FM en 90 s, Short 3 | todo | 15 min |

### EP4
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | A+V | Encoder cenital con el valor en pantalla (firmware con el bug: divisor 4) | hook, Short 1 | 10 min |
| 2 | B+V | Analizador lógico/osciloscopio en A/B, 2 pulsos por detent | bloque 1, Short 2 | 20 min |
| 3 | A | Encoder en reposo, valor temblando (`raw >> 1`), luego con `detent.h` | bloque 3 | 10 min |
| 4 | A+E | Cutoff con el DAW conectado: antes clavado en 83 Hz, después continuo | bloque 4, clímax, Short 3 | 15 min |
| 5 | C | commits `625c304`, `3f3dc1b`, `a3c588c`; `detent.h` completo; `PIN_MAP.md`; G-P12/G-P14 de `GAPS_AND_IMPROVEMENTS.md` | bloques 2-5 | 20 min |
| 6 | F | narración | todo | 15 min |

### EP5
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | A+E+V | Synth sonando, desconectar la Pi, audio sigue | hook, Short 3 | 10 min |
| 2 | A+V | Arranque en kiosko hasta PERFORM | Short 2 | 5 min |
| 3 | A+E | PERFORM con onda y filtro animados tocando | clímax | 10 min |
| 4 | C | `02-bridge-protocol.md` §1, frame en hex, commits `e4150bb`, `e09d698`, `3d074e4`, `a83de21`; `SerialController.cpp`; ADR-0003 (tabla de tokens) | bloques 1-5, Short 1 | 25 min |
| 5 | F | narración | todo | 15 min |

### EP6
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | D+V | `place_pcb_a.py` + `route_board.py` en time-lapse hasta DRC 0/0/0 | hook, Short 2 | 30 min (grabación larga, se acelera) |
| 2 | D | `panel-coordinates.csv` → render v2 → visor 3D de las 5 placas | bloques 1, clímax | 15 min |
| 3 | D | `CONNECTORS.md`, carrito de JLC con 100 vs 101 mm | bloques 3/5, Short 3 | 15 min |
| 4 | A+V | Tecla Choc V2 + SK6812-MINI-E (pieza física si existe) | Short 1 | 10 min |
| 5 | F | narración | todo | 15 min |

### EP7
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | D | Carrito de JLC, cursor a "Pay", cerrar | hook | 5 min |
| 2 | A+V | Macro del pin 13 y del LED de la Teensy | hook, Short 1 | 5 min |
| 3 | B+V | Encoder en pin 13 con `INPUT_PULLUP` vs otro pin, multímetro/osciloscopio en la fase A | clímax, Short 2 | 20 min |
| 4 | C+D | `auditoria-fabricacion-2026-10-22.md` F1-F4, esquema de PJRC, ruta de la red en KiCad, `CONNECTORS.md` J1.18 | bloques 1-6, Short 3 | 25 min |
| 5 | F | narración | todo | 15 min |

### EP8
| # | Setup | Toma | Para | Duración |
|---|---|---|---|---|
| 1 | A | Esquemático impreso del ladder, tacharlo con marcador | hook | 5 min |
| 2 | A+E+V | Auto-oscilación del ladder digital tocando una melodía | hook, clímax, Short 2 | 15 min |
| 3 | A+E | Scale lock (sketch24): notas "malas" corregidas | bloque 4 | 10 min |
| 4 | C | ADR-003, `auditoria-tecnica-2026-05.md` §1, `03-studio-input-stage.md` (CV), `sprints/23` y `25` | bloques 1-4, Shorts 1/3 | 20 min |
| 5 | F | Decisión, Temporada 2 | todo | 20 min |

### Bloque global de audio (una sola sesión para toda la temporada)
Grabar en **E** una vez, con el mismo nivel y cadena: los 6 engines con el mismo acorde, el barrido de auto-oscilación,
el DX7 viejo/nuevo, el feedback del operador, el cutoff antes/después del bug de 83 Hz y el scale lock. Así toda la
temporada suena coherente y los Shorts se pueden editar sin volver al banco.
