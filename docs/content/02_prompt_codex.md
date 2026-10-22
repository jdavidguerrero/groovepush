# Prompt de la Etapa 3 para Codex (OpenAI)

En la sesión del 2026-10-22, Codex no se pudo invocar desde el contenedor: no estaban la CLI `codex` ni las
credenciales de OpenAI. Por eso, `02_optimizacion_codex.md` lo escribió Claude haciendo el rol de Codex. Para
obtener la versión real de OpenAI, corré esto desde la raíz del repo `groovepush`:

```bash
npm install -g @openai/codex && codex login
codex exec --sandbox workspace-write "$(sed -n '/^> /s/^> //p' docs/content/02_prompt_codex.md)"
```

Después, pedile a Claude que repita la Etapa 4 sobre el nuevo `02_optimizacion_codex.md`.

## Prompt (verbatim)

> Actúa como Especialista en Retención Viral de YouTube/TikTok y Productor de Rodaje. Lee `docs/content/01_borrador_claude.md` y genera un archivo `docs/content/02_optimizacion_codex.md` que contenga: 1. **Auditoría de Retención:** Reescribe los primeros 15 segundos de cada video de YouTube y los primeros 3 segundos (gancho visual + verbal) de cada Short para eliminar cualquier introducción lenta. 2. **Packaging y CTR (Pruebas A/B):** Genera 5 variantes de títulos virales por episodio usando distintas psicologías (curiosidad extrema, reto de ingeniería, comparativa contra marcas líderes como Pioneer/Ableton/Roland) y describe el diseño visual exacto de la Miniatura (Thumbnail) con máximo 3 palabras de texto. 3. **Master Shot List (Tabla de Grabación):** Crea una tabla de rodaje agrupando todas las tomas físicas de cámara (hardware, soldadura, pruebas), capturas de pantalla de código/PCB y grabaciones de audio necesarias para grabar el episodio largo y sus 3 Shorts en una sola sesión eficiente.
