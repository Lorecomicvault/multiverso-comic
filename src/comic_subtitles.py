import os
import re

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = min(99, int(round((seconds - int(seconds)) * 100)))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_comic_ass(words, output_ass_path, font_name="Bangers",
                       box_bgr="&H00181818", text_bgr="&H00FFFFFF", highlight_bgr="&H0000F0FF",
                       keywords=None, alignment=5, margin_v=20, font_size=58):
    """
    Construye subtítulos ASS con BorderStyle: 3 (Caja rectangular de narrador de cómic).
    - box_bgr: Color de la caja (&H00BBGGRR). Por defecto: #181818 (Negro carbón mate)
    - text_bgr: Color del texto normal. Por defecto: Blanco (&H00FFFFFF)
    - highlight_bgr: Color de palabras clave. Por defecto: #00F0FF (Amarillo Neón Eléctrico en BGR)
    """
    kw_set = {k.upper() for k in (keywords or [])}

    header = f"""[Script Info]
Title: Comic Narrator Box
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ComicNormal,{font_name},{font_size},{text_bgr},&H00000000,{box_bgr},&H00000000,-1,0,0,0,100,100,1.2,0,3,9,4,{alignment},20,20,{margin_v},1
Style: ComicHighlight,{font_name},{int(font_size*1.1)},{highlight_bgr},&H00000000,{box_bgr},&H00000000,-1,0,0,0,105,105,1.2,0,3,10,4.5,{alignment},20,20,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for w in words:
        start_t = format_ass_time(w["start"])
        end_t = format_ass_time(w["end"])
        clean = re.sub(r'^[^\w¿¡]+|[^\w?!\.]+$', '', w["word"]).upper()
        if not clean:
            continue
        
        is_highlight = clean in kw_set
        style = "ComicHighlight" if is_highlight else "ComicNormal"
        anim = r"{\fscx122\fscy122\t(0,70,\fscx105\fscy105)}" if is_highlight else r"{\fscx112\fscy112\t(0,60,\fscx100\fscy100)}"
        events.append(f"Dialogue: 0,{start_t},{end_t},{style},,0,0,0,,{anim}{clean}")

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    return output_ass_path
