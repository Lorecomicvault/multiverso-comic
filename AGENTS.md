# GUÍA Y REGLAS PERMANENTES PARA AGENTES: MULTIVERSO COMIC

## 1. PRECISIÓN VISUAL 1:1 CANÓNICA (OBLIGATORIA EN TODOS LOS VIDEOS)
- **Correspondencia visual absoluta (Ver lo que se escucha)**:
  - Cada segundo de locución debe coincidir milimétricamente con lo que el usuario ve en pantalla.
  - Si se narra una mutación (ej. tumores de Bruce Banner, necrosis de Ben Grimm), la viñeta DEBE ser esa mutación explícita.
  - Si se narra un asesinato o mutilación (ej. Magneto destrozado por sierras circulares, Bullseye atravesado), la viñeta DEBE ser ese momento exacto.
  - Si una viñeta disponible muestra otra escena, la narración escrita debe adaptarse a describir la viñeta exacta, jamás inventar acciones no visibles.

## 2. PROHIBICIÓN ABSOLUTA DE DOCUMENTOS Y HOJAS DE TEXTO
- Queda terminantemente prohibido utilizar páginas con texto mecanografiado, notas manuscritas, diarios, cartas o documentos oficiales (ej. el cuaderno de Phil Sheldon en Marvel Ruins).
- Todo fotograma debe componerse de arte ilustrado a color de cómics oficiales.
- Todo pipeline de descarga debe aplicar el filtro `Quality Shield` (`mean_sat < 15.0 and mean_val > 175.0` => rechazo automático).

## 3. ESPECIFICACIONES DE FORMATO Y DURACIÓN
- 4 escenas estrictas.
- 55 a 65 palabras en total para la narración (sweet spot de 20 a 28 segundos).
- Resolución vertical 1080x1920 (9:16) con Ken Burns dinámico y subtítulos Whisper palabra por palabra.
