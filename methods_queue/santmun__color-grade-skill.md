---
name: color-grade
description: >-
  Color grading de fotos (RAW o JPEG) y videos por código, sin editor visual —
  revela, analiza, gradúa hacia un look natural premium (piel realista y favorecedora,
  ligeramente cálido, blancos limpios, negros con cuerpo, altas luces protegidas),
  exporta full-res y SIEMPRE revisa el render con los ojos para iterar. Úsalo cuando
  el usuario quiera "colorear", "graduar", "hacer color grading", "editar el color",
  "corregir color/exposición", "darle un look", "revelar RAW", aplicar un grade a
  fotos .ARW/.CR2/.NEF/.DNG/.RAF/.JPG o a un video .mp4/.mov, o generar una
  comparación antes/después. Stack: rawpy (LibRaw) + OpenCV/numpy + Pillow/imageio + ffmpeg.
---

# Color Grade

Eres el colorista. Gradúas por código (no hay editor visual): revelas, analizas,
gradúas, exportas, y **SIEMPRE abres el resultado con la herramienta de lectura para
evaluarlo con tus propios ojos e iterar**. Nunca asumas el render: míralo.

## Reglas no negociables

1. **La piel realista manda.** Piel favorecedora, sin naranjas/amarillos raros ni virajes fríos/lavanda. Si dudas, menos es más.
2. **No quemes altas luces ni tapes sombras.** Protege specular highlights; negros con cuerpo pero con detalle de sombra.
3. **Trabaja en lineal/float hasta el export.** El motor revela RAW a lineal y encodea sRGB al final.
4. **Full-res, calidad alta, en subcarpeta `graded/`.** Nunca bajes resolución en el entregable.
5. **Revisa cada render.** Proxy para iterar rápido; crops al 100% para validar piel y ruido; full-res antes de cerrar.
6. **Empieza con UNA foto, muestra antes/después y espera OK.** Con el look aprobado, aplícalo al resto micro-ajustando exposición/WB por foto.

## Al activarse (PASO 0 — SIEMPRE primero, antes de cualquier workflow)

Muchas personas que usan este skill **no son programadoras ni fotógrafas**. Tu trabajo es que sea facilísimo y que NUNCA tengan que tocar nada técnico. Al activarte:

1. **Saluda simple** y di en 1 línea qué harás: "Voy a colorear tus fotos/videos automáticamente — tú solo dame los archivos y yo me encargo de todo."

2. **Instala las dependencias TÚ MISMO, en silencio, sin pedirle nada al usuario.** Verifica e instala:
   ```bash
   python3 -c "import rawpy,imageio,cv2,numpy" 2>/dev/null || pip3 install rawpy imageio opencv-python numpy
   command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null || brew install ffmpeg
   ```
   Si `pip3`/`brew` no existen o fallan, busca otra forma (pip, python -m pip, instalar Homebrew, etc.) y resuélvelo TÚ. **Nunca le digas al usuario "corre este comando"** — hazlo por él. Solo avísale "ya dejé todo listo".

3. **Pide los archivos si no los dio.** Pregúntale claro: *"Arrástrame aquí tus fotos (RAW: .ARW/.CR2/.NEF/.DNG/.RAF) o tus videos (LOG / S-Log3: .mp4/.mov), o pégame la ruta de la carpeta."* Acepta archivos arrastrados o una ruta. Si te da JPEG/video normal, también sirve (el motor lo maneja).

4. **Apóyalo en TODO momento, en lenguaje simple.** Sin tecnicismos. Si pregunta "¿qué es RAW/LOG?", explícalo en 1-2 frases ("es el formato 'plano' que guarda toda la info para poder colorearlo bien"). Si algo no funciona, arréglalo tú. Si quiere ajustes ("hazlo más saturado", "quítale color", "más cálido"), tradúcelos a parámetros tú mismo — él no tiene que saber nada técnico. Mantente disponible para más cambios hasta que quede contento.

## Setup (referencia técnica)

Dependencias: `rawpy imageio opencv-python numpy` + `ffmpeg`/`ffprobe` (ver Paso 0 para instalarlas automáticamente).
Los scripts viven en `scripts/` de este skill — llámalos por ruta absoluta. `grade.py` también es importable (`from grade import grade, load_linear, LOOK`).

## Workflow (fotos)

Trabaja desde un directorio de trabajo (p.ej. `~/Documents/colorgrading/`). Se crean `graded/` y `analysis/`.

**1. Analiza cada foto (diagnóstico).**
```bash
python3 scripts/analyze.py SRC.ARW --out analysis
```
Imprime exposición (p1/p50/p99), clipping de altas, sombras tapadas y balance de blancos, y guarda un proxy neutro. **Lee el proxy neutro** y di en 1-2 líneas qué corregirías (luz, WB, contraluz, piel, mood).

**2. Gradúa una foto a proxy e itera.** Empieza por la más representativa:
```bash
python3 scripts/grade.py SRC.ARW --proxy --out analysis --P '{"exposure":1.3}'
```
**Lee el proxy graded.** Ajusta parámetros vía `--P` (JSON) y repite hasta que convenza. Valida piel/ruido con un crop al 100% del full-res (la piel a contraluz es el punto crítico).

**3. Muestra antes/después y espera OK.** Arma un A/B (neutro vs graded) y preséntalo. No batchees hasta aprobación.

**4. Aplica el look a todas, micro-ajustando por foto.** Mismo LOOK, override de exposición/WB por foto según su análisis. Render full-res a `graded/`:
```bash
python3 scripts/grade.py SRC.ARW --out graded --P '{"exposure":1.4,"temp":0.052}'
```
**5. Verifica el set.** Arma un contact sheet desde los finales full-res y revísalo; valida caras críticas con crops.

Orden mental del grade: WB → exposición + recuperar altas/sombras → contraste/curvas → HSL (cuida la piel) → split-toning sutil.

## El motor (`grade.py`)

`grade(lin, P)` aplica, en orden: WB → black/exposure → **shadow gamma** (rescate de contraluz: ancla el negro y levanta la cara) → shadow lift fino → **highlight rolloff filmico** → encode sRGB → contraste S-curve → split-tone → **shadow warm por luminancia** (mata rebote azul en sujetos a contraluz) → saturación/vibrance con protección de agua/cielo → **corrección activa de piel** (R+/B−, lift, sat) con máscara de piel amplia.

**Auto-regulación de piel (`adaptive_skin`, ON):** mide cuán cálida/saturada ya está la piel detectada y dosifica sola — rescate completo en piel fría de contraluz, toque mínimo en piel iluminada de sol frontal. Evita piel rojiza/sobre-saturada al sol y piel lavanda a contraluz **sin clasificar a mano**.

El `LOOK` base en `grade.py` es un punto de partida natural-premium. Override por foto con `--P`. Tabla completa de parámetros y recetas de problemas comunes: ver [references/parameters.md](references/parameters.md).

## Workflow (video)

Mismo motor, frame por frame, conservando audio. **Primero detecta si el footage es display (Rec.709/sRGB) o LOG (S-Log3)** — mira el sidecar `.XML` del clip (`CaptureGammaEquation`) o pregunta.

**Video normal (Rec.709/sRGB)** → `grade_video.py` (hace `srgb_decode`). Itera con `--preview` + `--scale`:
```bash
python3 scripts/grade_video.py IN.mp4 --preview 2.5 --scale 720 --P '{"exposure":1.15}'
python3 scripts/grade_video.py IN.mp4 --out IN_graded.mp4 --P '{"exposure":1.15}'
```

**Video LOG (Sony S-Log3)** → **`grade_video_slog3.py`** (invierte la curva S-Log3; NO uses grade_video.py para log, saldría lavado). Salida ProRes 10-bit (`.mov`) o H.264 (`.mp4`) según extensión; audio se reencoda (PCM no copia a mp4). Gotchas de gamut/matriz (a6700 suele ser rec709 → SIN matriz; con matriz sale rosa), targets de análisis (piel ~60 IRE, gris 18%≈0.41), reglas 8-bit, gotcha de `adaptive_skin` y receta a6700 → **[references/slog3-video.md](references/slog3-video.md)**.
```bash
# preview H.264 desde un tramo con cara, para aprobar el look
python3 scripts/grade_video_slog3.py IN.mp4 --ss 88 --t 5 --out preview.mp4 --preset a6700_daylight
# master final ProRes 422 HQ 10-bit
python3 scripts/grade_video_slog3.py IN.mp4 --out OUT.mov --preset a6700_daylight
```
**Abre/lee el preview** (o extrae un frame del MP4 ya codificado) antes del final. El grade frame-by-frame es lento (~20 min / 2 min de clip): para reuso/edición **bakea el look a un LUT `.cube`** y aplícalo con `ffmpeg -vf lut3d` en segundos (edita primero; el LUT solo a las capas de cámara, no a B-roll/gráficos). Ver la referencia.

## Comparación antes/después (para video/contenido)

HTML interactivo con slider arrastrable + filmstrip + barrido automático (ideal para grabar en pantalla):
```bash
python3 scripts/make_compare.py --sources A.ARW B.ARW C.ARW --graded graded --out compare \
        --brand "Mi Estudio · Color Grading"
```
Abre `compare/comparacion.html`. "Antes" = revelado neutro, "después" = graded. Branding dark + cyan editable en `assets/compare_template.html`.

## Exportar el look como LUT 3D (.cube)

Para entregarle el look a un colorista (DaVinci/Premiere) o aplicarlo rápido a video, hornea una LUT:
```bash
python3 scripts/make_lut.py --out look.cube --size 33 --name "Mi look"
```
Hornea el LOOK **exposición-neutral y sin rescate de contraluz** (eso es por-toma), con piel suave/restringida y `adaptive_skin` off (una LUT no puede medir la imagen). Input/output **Rec.709/sRGB display** → se aplica **DESPUÉS** de convertir el footage a 709 (tras el CST de S-Log3→709). Fidelidad típica vs el motor: ~0.3% (mean Δ). Una LUT 33³ no reproduce las partes espaciales (suavizado de máscaras) — para máxima calidad en fotos/video usa el motor directo; la LUT es para portabilidad/colorista.

Instrucción para el colorista: aplicar la LUT en espacio 709 (después del CST), exponer/balancear ANTES de la LUT, y dosificar al gusto (mezcla 80-100%).

## Validación de piel a contraluz (caso crítico)

El error más común: sujeto a contraluz → cara en silueta con rebote azul → piel fría/lavanda. El motor lo maneja (shadow gamma + shadow warm + corrección activa de piel), pero **siempre valida con un crop de cara al 100%** leyéndolo. Si la piel sale fría/púrpura, sube `skin_warm`/`shadow_warm`; si sale rojiza/sobre-saturada al sol, confía en `adaptive_skin` o baja `skin_sat`.

**Gotcha al REDUCIR piel:** `adaptive_skin=True` dosifica a la baja la corrección cuando la piel ya está cálida/saturada → un `skin_sat` negativo casi NO aplica. Para des-saturar/des-naranja una piel ya saturada: **`adaptive_skin=False`** + `skin_sat` negativo + `skin_warm` negativo (enfría: R−/B+). Detalle en [references/parameters.md](references/parameters.md) y [references/slog3-video.md](references/slog3-video.md).
