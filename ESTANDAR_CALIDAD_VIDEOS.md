# 🏆 ESTÁNDAR DE ORO: PRODUCCIÓN DE VIDEOS DE CÓMICS (ALTA RETENCIÓN)

Este documento fija el **Estándar de Oro Canónico** validado y perfeccionado tras la recreación de *Deathstroke vs Liga de la Justicia*. Todo video futuro debe adherirse de forma estricta e intransigente a estos cuatro pilares.

---

## 1. PRECISIÓN VISUAL 1:1 CANÓNICA (CERO RELLENO O PORTADAS DESALINEADAS)
- **Correspondencia visual absoluta**: Cada frase de la locución debe mostrar exactamente la acción o el personaje descrito en ese instante preciso.
- **Composición Vertical 1080x1920 (Canvas Apilado / Split)**:
  - Cuando una escena narre dos acciones consecutivas en el mismo evento (ej. la trampa de explosivos/espada a Flash + el golpe al hígado a Zatanna), se compone un canvas vertical apilado de dos paneles (`create_stacked_canvas`), asegurando que ambas viñetas sean nítidas y claramente legibles.
  - El encuadre debe calibrarse con micro-ajustes de centrado vertical (`top_centering`, `bot_centering`) para no recortar cabezas, máscaras, armas o globos de diálogo icónicos.
- **Regla de oro anti-desalineación**:
  - Queda terminantemente prohibido utilizar portadas de números no relacionados (ej. funerales, variantes) o viñetas genéricas cuando se está narrando combate directo.

---

## 2. FONÉTICA Y FLUIDEZ NATURAL EN ESPAÑOL (`es-US-Studio-B`)
- **Adaptación fonética inteligente**:
  - El motor TTS de Google Cloud (`es-US-Studio-B`) debe recibir textos optimizados para dicción nativa en español.
  - Adaptar o traducir nombres o abreviaturas que generen tropiezos o deletreos extraños:
    - Usar *"el Doctor Luz"* en lugar de *"Dr. Light"*.
    - Usar *"Linterna Verde"* en lugar de *"Kyle Rayner"*.
    - Usar *"el universo de los cómics"* o *"DC Comics"* en vez de siglas aisladas.
    - Usar términos directos y anatómicos claros (*"golpeó a Zatanna en el abdomen anulando su magia"*).
  - La redacción debe incorporar puntuación precisa (comas y puntos) para modular el ritmo, las pausas de respiración y la intensidad dramática.

---

## 3. FORMATO DE MÁXIMA RETENCIÓN (28 A 32 SEGUNDOS)
- **Estructura fija en 4 escenas de impacto sostenido**:
  - **Escena 1 (Gancho & Reto)**: ~6.5 - 7.5s (20 a 24 palabras). Pregunta provocadora o contexto de muerte/amenaza.
  - **Escena 2 (Choque Inicial)**: ~6.5 - 7.5s (18 a 22 palabras). Demostración directa de táctica y poder.
  - **Escena 3 (Escalada y Brutalidad)**: ~6.5 - 7.5s (18 a 22 palabras). Momento de máxima tensión y daño.
  - **Escena 4 (Clímax Legendario)**: ~6.5 - 7.5s (18 a 22 palabras). Giro decisivo y desenlace heroico o trágico.
- **Métricas obligatorias**:
  - Conteo de palabras totales del guion: **80 a 92 palabras**.
  - Duración del video final: estrictamente entre **28.0s y 32.5s** (sweet spot probado de retención para Shorts y Reels).

---

## 4. ESPECIFICACIONES TÉCNICAS Y LOGS
- **Resolución**: Pure Vertical 1080x1920 (9:16) Full-Bleed sin bandas negras ni letterboxing.
- **Cámara Ken Burns**: Movimiento continuo y visible (18% - 22% zoom/pan) alternando patrones dinámicos (`zoom-in`, `zoom-out`, `pan-down`, `pan-up`).
- **Subtítulos**: Sincronización Whisper palabra por palabra en formato ASS dinámico (resaltado amarillo/blanco en zona segura).
- **Miniaturas**: DESACTIVADAS (`NO_THUMB=1` y `generate_thumbnail=False`). 0 archivos `*_thumb.jpg`.
- **Almacenamiento**: 100% local en `C:\Users\Vanes\Downloads\video\Comics`. Cero subidas a la nube o carpetas OneDrive.
- **Bitácora y Estrategia**:
  - Actualización automática en `published_ledger.json`.
  - Actualización automática en `videos_log.csv`.
  - Recompilación y sincronización del PDF `Guia_Viral_SEO_Videos_Comics_Alta_Retencion.pdf` en `Downloads` y en `Downloads\video\Comics`.
