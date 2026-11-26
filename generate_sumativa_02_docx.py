import os
import shutil
import docx
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "Formato_propuesto_sumativa 01_2026.docx")
if not os.path.exists(TEMPLATE_PATH):
    TEMPLATE_PATH = os.path.join(BASE_DIR, "Proyecto Integrado 1.docx")

ENTREGA_DIR = os.path.join(BASE_DIR, "entrega_sumativa_02")
DIAG_DIR = os.path.join(ENTREGA_DIR, "diagrams")
SHOT_DIR = os.path.join(ENTREGA_DIR, "prototipo", "capturas")

COLOR_TITLE = RGBColor(0x1F, 0x49, 0x7D)      # Azul institucional INACAP
COLOR_ACCENT = RGBColor(0xB9, 0x1C, 0x1C)     # Rojo técnico énfasis
COLOR_SUBTITLE = RGBColor(0x59, 0x59, 0x59)   # Gris medio
COLOR_BODY = RGBColor(0x26, 0x26, 0x26)       # Gris oscuro legible
COLOR_CAPTION = RGBColor(0x47, 0x55, 0x69)    # Gris pizarra pie de figura
FONT_NAME = "Open Sans"
FONT_MONO = "Consolas"


class DocBuilder:
    """Construye el documento secuencialmente insertando antes de <w:sectPr>."""
    def __init__(self, doc):
        self.doc = doc
        self.body = doc.element.body
        self.sectPr = self.body.find(qn("w:sectPr"))

    def _attach(self, el):
        if self.sectPr is not None:
            self.sectPr.addprevious(el)
        else:
            self.body.append(el)

    def add_page_break(self):
        p = self.doc.add_paragraph()
        r = p.add_run()
        r.add_break(docx.enum.text.WD_BREAK.PAGE)
        self._attach(p._p)
        return p

    def add_h1(self, text):
        p = self.doc.add_paragraph()
        try:
            p.style = self.doc.styles["Título1"]
        except KeyError:
            pass
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = FONT_NAME
        r.font.size = Pt(13.0)
        r.font.color.rgb = COLOR_TITLE
        self._attach(p._p)
        return p

    def add_h2(self, text, size=11.0):
        p = self.doc.add_paragraph()
        try:
            p.style = self.doc.styles["Título2"]
        except KeyError:
            pass
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = FONT_NAME
        r.font.size = Pt(size)
        r.font.color.rgb = COLOR_TITLE
        self._attach(p._p)
        return p

    def add_h3(self, text, size=10.2):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = FONT_NAME
        r.font.size = Pt(size)
        r.font.color.rgb = COLOR_TITLE
        self._attach(p._p)
        return p

    def add_p(self, text="", bold=False, italic=False, color=COLOR_BODY, size=10.0,
              align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=6, mono=False):
        p = self.doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if text:
            r = p.add_run(text)
            r.bold = bold
            r.italic = italic
            r.font.name = FONT_MONO if mono else FONT_NAME
            r.font.size = Pt(size)
            r.font.color.rgb = color
        self._attach(p._p)
        return p

    def add_code(self, code_text, title=None):
        if title:
            self.add_p(title, bold=True, color=COLOR_TITLE, size=9.5, space_before=4, space_after=2)
        tbl = self.doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.rows[0].cells[0]
        cell.text = ""
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            '<w:top w:val="single" w:sz="4" w:color="CBD5E1"/>'
            '<w:left w:val="single" w:sz="16" w:color="1F497D"/>'
            '<w:bottom w:val="single" w:sz="4" w:color="CBD5E1"/>'
            '<w:right w:val="single" w:sz="4" w:color="CBD5E1"/>'
            '</w:tcBorders>'
        )
        margins = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            '<w:top w:w="90" w:type="dxa"/><w:bottom w:w="90" w:type="dxa"/>'
            '<w:left w:w="140" w:type="dxa"/><w:right w:w="120" w:type="dxa"/>'
            '</w:tcMar>'
        )
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(shading)
        tcPr.append(borders)
        tcPr.append(margins)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(code_text)
        r.font.name = FONT_MONO
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
        self._attach(tbl._tbl)
        self.add_p("", space_after=4)
        return tbl

    def add_table(self, caption, headers, rows_data, col_widths=None):
        if caption:
            self.add_p(caption, bold=True, italic=True, color=COLOR_CAPTION, size=9.0, space_before=6, space_after=3)
        table = self.doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr
        tblBorders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            '<w:top w:val="single" w:sz="6" w:color="1F497D"/>'
            '<w:bottom w:val="single" w:sz="6" w:color="1F497D"/>'
            '<w:insideH w:val="single" w:sz="4" w:color="CBD5E1"/>'
            '<w:insideV w:val="single" w:sz="4" w:color="E2E8F0"/>'
            '<w:left w:val="none"/><w:right w:val="none"/>'
            '</w:tblBorders>'
        )
        tblPr.append(tblBorders)

        trPr = table.rows[0]._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for i, h_text in enumerate(headers):
            c = table.rows[0].cells[i]
            c.text = ""
            tcPr = c._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="1F497D"/>'))
            tcPr.append(parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                '<w:top w:w="70" w:type="dxa"/><w:bottom w:w="70" w:type="dxa"/>'
                '<w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
                '</w:tcMar>'
            ))
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(h_text))
            r.font.name = FONT_NAME
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        for r_idx, row_vals in enumerate(rows_data):
            row = table.rows[r_idx + 1]
            row._tr.get_or_add_trPr().append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            bg = "F2F5F8" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_vals):
                c = row.cells[c_idx]
                c.text = ""
                tcPr = c._tc.get_or_add_tcPr()
                tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg}"/>'))
                tcPr.append(parse_xml(
                    f'<w:tcMar {nsdecls("w")}>'
                    '<w:top w:w="55" w:type="dxa"/><w:bottom w:w="55" w:type="dxa"/>'
                    '<w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>'
                    '</w:tcMar>'
                ))
                p = c.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.08
                r = p.add_run(str(val))
                r.font.name = FONT_NAME
                r.font.size = Pt(8.2)
                r.font.color.rgb = COLOR_BODY
                if c_idx == 0:
                    r.bold = True

        if col_widths:
            for row in table.rows:
                for i, w in enumerate(col_widths):
                    row.cells[i].width = Inches(w)

        self._attach(table._tbl)
        self.add_p("", space_after=5)
        return table

    def add_figure(self, img_path, caption, width_inches=6.3):
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Imagen requerida no encontrada: {img_path}")
        p_img = self.doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.paragraph_format.keep_with_next = True
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(width_inches))
        self._attach(p_img._p)
        self.add_p(caption, italic=True, color=COLOR_CAPTION, size=8.8, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)


def clean_template_after_toc(doc):
    """Conserva portada (0..6) y Tabla de Contenidos (7), eliminando todo resto de plantilla antes de <w:sectPr>."""
    body = doc.element.body
    children = list(body)
    for idx in range(8, len(children)):
        el = children[idx]
        if el.tag != qn("w:sectPr"):
            body.remove(el)


def enable_update_fields(doc):
    """Marca <w:updateFields w:val="true"/> para que Word actualice TOC y número de página al abrir."""
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is None:
        uf = OxmlElement("w:updateFields")
        uf.set(qn("w:val"), "true")
        settings.append(uf)


def build_sumativa_02():
    doc = docx.Document(TEMPLATE_PATH)

    # Metadatos limpios del autor real
    cp = doc.core_properties
    cp.author = "Mauricio Vega Castillo"
    cp.last_modified_by = "Mauricio Vega Castillo"
    cp.title = "Proyecto Integrado (TIHV43) — Evaluación Sumativa 2: Diseño de la Solución STAGE PLAN"
    cp.subject = "Analista Programador — Sección C1 — Grupo G10 — INACAP Sede Maipú"
    cp.comments = ""

    enable_update_fields(doc)

    for s in doc.styles:
        if s.name in ["Estilo3", "Título1", "Normal"]:
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            s.font.name = FONT_NAME

    orig = list(doc.paragraphs)

    # 1. PORTADA OFICIAL
    p1 = orig[1]
    p1.text = ""
    r1 = p1.add_run("STAGE PLAN\n")
    r1.bold = True
    r1.font.name = FONT_NAME
    r1.font.size = Pt(24)
    r1.font.color.rgb = COLOR_TITLE
    r2 = p1.add_run(
        "Plataforma Web de Pre-Producción Logística, Ruteo Eléctrico SEC RIC N° 03/10, "
        "Acústica Espacial Haas, Dimensionamiento de Potencias Pasivas y Cotización Operativa"
    )
    r2.font.name = FONT_NAME
    r2.font.size = Pt(12.0)
    r2.font.color.rgb = COLOR_SUBTITLE

    for idx in range(2, 6):
        orig[idx].text = ""

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    def add_val_run(p, val_text, color_hex="1F497D"):
        r = OxmlElement("w:r")
        rPr = OxmlElement("w:rPr")
        rPr.append(OxmlElement("w:b"))
        c = OxmlElement("w:color")
        c.set(qn("w:val"), color_hex)
        rPr.append(c)
        f = OxmlElement("w:rFonts")
        f.set(qn("w:ascii"), FONT_NAME)
        f.set(qn("w:hAnsi"), FONT_NAME)
        rPr.append(f)
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), "22")
        rPr.append(sz)
        r.append(rPr)
        t = OxmlElement("w:t")
        t.text = val_text
        r.append(t)
        p.append(r)

    p6 = orig[6]
    p6.text = ""
    r6 = p6.add_run(
        "Carrera: Analista Programador | Asignatura: Proyecto Integrado (TIHV43)\n"
        "Sección: C1 | Grupo: G10 | Autor: Mauricio Vega Castillo | Docente: Manuel Rojas\n"
        "Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA\n"
        "Sede: INACAP Sede Maipú | Fecha de entrega: Noviembre de 2026"
    )
    r6.font.name = FONT_NAME
    r6.font.size = Pt(10.0)
    r6.font.color.rgb = COLOR_SUBTITLE
    r6.italic = True

    # Limpiar restos de plantilla posteriores al índice TOC
    clean_template_after_toc(doc)

    b = DocBuilder(doc)
    b.add_page_break()

    # 2. RESUMEN EJECUTIVO
    b.add_h1("RESUMEN EJECUTIVO")
    b.add_p(
        "STAGE PLAN es una plataforma web responsiva de pre-producción electroacústica desarrollada y validada para "
        "la empresa contraparte DISTORSIONCL SPA (operador técnico Amaro Artiaga), en el marco de la Unidad 2 de la "
        "asignatura Proyecto Integrado (TIHV43, Sección C1, Grupo G10, INACAP Sede Maipú). La solución sustituye el "
        "dimensionamiento empírico sin cálculo normativo de instalaciones temporales de sonido, cableado de escenario y "
        "fuerza eléctrica, aplicando de forma determinista los Pliegos Técnicos Normativos SEC RIC N° 03 y RIC N° 10, "
        "el Decreto Supremo N° 38 del Ministerio del Medio Ambiente (MMA) sobre emisión de ruidos y la Ley N° 20.949 "
        "(Ley del Saco)."
    )
    b.add_p(
        "Este informe técnico consolida los seis ejes de diseño exigidos para la evaluación: (1) planificación Scrumban + "
        "PSP en 4 Sprints de 14 días (20 tareas con ruta crítica y tablero Kanban con límite WIP=1); (2) arquitectura 4+1 "
        "(ISO/IEC/IEEE 42010:2022) estructurada como monorepo TypeScript; (3) diseño UX/UI Dark Mode FOH (WCAG 2.1 AA) en "
        "formato Studio Cockpit calibrado al 100% de zoom del navegador, con plano vectorial 2D por capas exclusivas "
        "(Blueprint Dark), postes guía SEC RIC N° 10, dimensionamiento automático de rack de potencias pasivas, cotizador "
        "de arriendo diario en CLP, réplica interactiva Pioneer DJM y exportación PDF Dual-Page; (4) persistencia híbrida "
        "en SQLite 3 (dev.db) mediante Prisma ORM (4 tablas normalizadas en 3FN en español + documentos JSON) con proyección "
        "documentada hacia PostgreSQL 16; (5) estándares de programación segura con validación Zod, bcrypt (cost 12), bloqueo "
        "temporal HTTP 423, limitación de tasa, protección Anti-IDOR y matriz OWASP Top 10 (2021); y (6) aseguramiento de "
        "calidad verificado mediante 81 pruebas unitarias automatizadas en Vitest (11 archivos, 100% PASS en 186 ms) y "
        "medición real de rendimiento de 0,0286 ms promedio por cálculo completo."
    )
    b.add_p(
        "Nota de alcance (Unidad 2 — Diseño y Prueba de Concepto): Conforme a la Guía ABPRO Unidad 2, este documento "
        "corresponde a la fase de Diseño de la Solución de Software. El código operativo exhibido (frontend Vue 3 con "
        "Vue Router, núcleo compartido @stageplan/shared, API Express/Prisma sobre SQLite y 81 pruebas TDD) funciona como "
        "prototipo interactivo funcional y prueba de concepto (PoC) verificable en local, manteniendo para la etapa de "
        "construcción y despliegue productivo (Unidad 3) la migración a PostgreSQL 16 en servidor VPS, la bitácora forense "
        "audit_logs, las pruebas de carga con k6 y el escaneo activo con OWASP ZAP.",
        italic=True, color=COLOR_CAPTION, size=9.2
    )

    # ACTIVIDADES FORMATIVAS U2
    b.add_h2("Actividades Formativas de la Unidad 2: Brainstorming y Matriz de Priorización (Guía ABPRO)")
    b.add_table(
        "Tabla 1. Parte 1 — Brainstorming categorizado de mejoras técnicas levantadas para DISTORSIONCL SPA.",
        ["Categoría Temática", "Ideas Levantadas en Lluvia de Ideas", "Problemática Resuelta en Terreno"],
        [
            ["1. Seguridad Eléctrica SEC", "I1: Calibre automático ΔV ≤ 3%; I2: Líneas aisladas L1/L2/L3; I3: Postes guía esquineros R ≥ 6d (RIC N° 10).", "Disparos termomagnéticos, sobrecalentamiento Joule y fatiga mecánica de conductores."],
            ["2. Acústica y Gain Staging", "I4: Clúster mono de subs (+6 dB); I5: Retardos Haas para Delays; I6: Réplica hardware Pioneer DJM (VU vertical + Low Kill).", "Saturación (clipping), cancelaciones de graves y daño de bobinas por dos bajos simultáneos."],
            ["3. Equipamiento Mixto y Potencias", "I7: Lotes Activa/Pasiva con cálculo de rack de potencias (headroom 1.6x) y alerta Speakon; I8: Carga AC 220V de etapas.", "Apagado en modo PROTECT, subdimensionamiento de amplificadores y distorsión térmica."],
            ["4. Logística y Costos", "I9: Alerta peso máximo Ley del Saco N° 20.949; I10: Lista cables poder/señal; I11: Plan B; I16: Cotizador de arriendo CLP.", "Lesiones lumbares, olvido de cables, parálisis ante falla y falta de presupuesto rápido."],
            ["5. Operación Autónomo-Terreno", "I12: Plano 2D Blueprint por capas y vista completa en reporte; I13: PDF Dual-Page + PNG 300 DPI; I14: WhatsApp; I15: SharedLink.", "Ruido visual al configurar, recintos rurales sin señal móvil y descoordinación en despacho."]
        ],
        [1.5, 2.7, 2.3]
    )
    b.add_table(
        "Tabla 2. Parte 2 — Matriz de priorización ponderada (Impacto 40%, Viabilidad 30%, Urgencia Normativa 30%).",
        ["Rank", "Propuesta Evaluada", "Imp.", "Viab.", "Urg.", "Puntaje", "Decisión de Alcance"],
        [
            ["1", "I1+I2: Cálculo SEC RIC 03/10 (ΔV ≤ 3%) y separación L1/L2/L3", "5.0", "5.0", "5.0", "5.00", "MVP Obligatorio (S1–S2)"],
            ["2", "I7+I8: Lotes Activa/Pasiva, Rack de Potencias y alerta Speakon < 3.2 Ω", "5.0", "4.8", "4.8", "4.88", "MVP Obligatorio (S2–S4)"],
            ["3", "I3+I12: Plano 2D Blueprint por capas + Postes Guía RIC 10 (R ≥ 6d)", "4.9", "4.5", "5.0", "4.81", "Core (S4)"],
            ["4", "I4+I5+I6: Clúster Mono + Delays Haas + Réplica Pioneer DJM", "4.6", "4.7", "4.5", "4.60", "Core (S4)"],
            ["5", "I9+I10+I13: D.S. N° 38 MMA + Ley del Saco + PDF Dual-Page Offline", "4.5", "4.6", "4.2", "4.44", "Core (S3–S4)"],
            ["6", "I11+I14+I16: Plan B + WhatsApp + Cotizador de Arriendo CLP", "4.1", "4.8", "3.9", "4.25", "Complemento (S4)"]
        ],
        [0.45, 2.55, 0.45, 0.45, 0.45, 0.65, 1.5]
    )

    # SECCIÓN 1: METODOLOGÍA
    b.add_h1("1. METODOLOGÍA DE DESARROLLO Y PLANIFICACIÓN")
    b.add_h2("1.1 Selección y justificación de la metodología de desarrollo (Scrumban + PSP)")
    b.add_p(
        "Dado que el proyecto es desarrollado de forma individual por Mauricio Vega Castillo (Sección C1, Grupo G10), "
        "se seleccionó el marco ágil híbrido Scrumban complementado con prácticas de PSP (Personal Software Process). "
        "El enfoque Cascada resulta rígido frente a las iteraciones recogidas con el operador de DISTORSIONCL SPA, "
        "mientras que Scrum puro introduce ceremonias diseñadas para equipos numerosos. Scrumban + PSP articula: "
        "(a) 4 Sprints fijos de 14 días con entregables verificables; (b) tablero Kanban con límite estricto WIP = 1 en la "
        "columna 'In Progress' para evitar cambios de contexto; y (c) compuerta de calidad automatizada (Quality Gate) "
        "compuesta por compilación estricta TypeScript (vue-tsc + tsc) y 81 pruebas unitarias TDD en Vitest que compensan "
        "la ausencia de revisión por pares."
    )

    b.add_h2("1.2 Cronograma de trabajo, hitos, dependencias, ruta crítica y estimación de recursos")
    b.add_table(
        "Tabla 3. Estimación de recursos humanos, técnicos e infraestructura del proyecto.",
        ["Tipo de Recurso", "Detalle Técnico / Rol Asignado", "Dedicación / Costo"],
        [
            ["Recurso Humano", "Mauricio Vega Castillo — Analista Programador (Arquitectura, Full-Stack, QA, Documentación)", "180 hrs (4 Sprints × 14 días)"],
            ["Contraparte Real", "Amaro Artiaga — Operador Técnico FOH de DISTORSIONCL SPA (Validación terreno)", "8 hrs sesiones de iteración UX"],
            ["Entorno Dev/QA", "Estación Windows 11, Node.js v24 LTS, SQLite 3 (dev.db) + Prisma, Vitest v3.2.7, GitHub", "$0 CLP (Open Source / Académico)"],
            ["Despliegue Cloud U3", "VPS Linux Ubuntu 22.04 LTS (2 vCPU, 4 GB RAM) + PostgreSQL 16 + Nginx TLS 1.3", "~$12.000 CLP/mes proyectado"]
        ],
        [1.3, 3.6, 1.6]
    )
    b.add_table(
        "Tabla 4. Cronograma de 20 tareas (T01–T20) con responsables, plazos, dependencias, MoSCoW y ruta crítica.",
        ["ID", "Sprint", "Actividad Técnica", "Resp.", "Plazo", "Dep.", "MoSCoW", "Crítica"],
        [
            ["T01", "S1", "Diagnóstico DISTORSIONCL SPA, Brainstorming y Priorización", "M. Vega", "01–04 Oct", "—", "Must", "SÍ"],
            ["T02", "S1", "Casos de Uso (CU-00..08) y contratos Zod (schemas.ts)", "M. Vega", "05–08 Oct", "T01", "Must", "SÍ"],
            ["T03", "S1", "Arquitectura 4+1 (5 vistas) y modelo híbrido DER 4 tablas", "M. Vega", "09–11 Oct", "T02", "Must", "No"],
            ["T04", "S1", "Setup Monorepo npm workspaces (shared, backend, frontend)", "M. Vega", "12–14 Oct", "T02", "Must", "SÍ"],
            ["T05", "S2", "Motor eléctrico SEC RIC 03/10 (electrical.ts, cabling.ts)", "M. Vega", "15–18 Oct", "T04", "Must", "SÍ"],
            ["T06", "S2", "Lotes Activa/Pasiva, Rack Potencias y Speakon (hybrid-roster.ts)", "M. Vega", "19–21 Oct", "T05", "Must", "SÍ"],
            ["T07", "S2", "Acústica espacial: Clúster mono +6 dB y retardos Haas", "M. Vega", "22–24 Oct", "T05", "Must", "No"],
            ["T08", "S2", "Ruteo cables audio, Setup DJ y suite TDD en Vitest", "M. Vega", "25–28 Oct", "T06, T07", "Must", "SÍ"],
            ["T09", "S3", "Prisma ORM (schema.prisma) + SQLite 3 (dev.db) 4 tablas 3FN + JSON", "M. Vega", "29–31 Oct", "T03, T08", "Must", "SÍ"],
            ["T10", "S3", "API Express: Helmet, CORS, RateLimit, Bcrypt(12), JWT y bloqueo 423", "M. Vega", "01–04 Nov", "T09", "Must", "SÍ"],
            ["T11", "S3", "Controladores Venues y Calculations con Anti-IDOR y errorHandler", "M. Vega", "05–07 Nov", "T10", "Must", "No"],
            ["T12", "S3", "Arquitectura modular Vue Router (5 rutas) + Dark Mode FOH WCAG AA", "M. Vega", "08–11 Nov", "T08, T10", "Must", "SÍ"],
            ["T13", "S4", "Cockpit 100% zoom, LayoutSvg2D Blueprint (5 capas) + Postes RIC 10", "M. Vega", "12–15 Nov", "T12", "Must", "SÍ"],
            ["T14", "S4", "Réplica hardware PioneerMixerSimulator.vue (17 LEDs + Kill)", "M. Vega", "16–18 Nov", "T12", "Should", "No"],
            ["T15", "S4", "Cotizador arriendo CLP, exportación PDF Dual-Page, PNG 300 DPI y Plan B", "M. Vega", "18–19 Nov", "T13, T14", "Must", "SÍ"],
            ["T16", "S4", "Validación UX con Amaro Artiaga (iteraciones de usabilidad y capas)", "M. Vega", "19–20 Nov", "T15", "Should", "No"],
            ["T17", "S4", "Auditoría OWASP Top 10 (A01–A10) y casos de seguridad", "M. Vega", "21–22 Nov", "T11, T15", "Must", "No"],
            ["T18", "S4", "Benchmark rendimiento (1.000 iters) y verificación 81/81 Vitest PASS", "M. Vega", "23–25 Nov", "T15, T17", "Must", "SÍ"],
            ["T19", "S4", "Regeneración de 8 diagramas vectoriales, capturas reales y mosaico", "M. Vega", "25–26 Nov", "T16, T18", "Must", "No"],
            ["T20", "S4", "Consolidación Informe Sumativa 2, empaquetado .zip y cierre", "M. Vega", "26 Nov", "T18, T19", "Must", "SÍ"]
        ],
        [0.42, 0.45, 2.38, 0.65, 0.78, 0.62, 0.62, 0.58]
    )
    b.add_p("Ruta Crítica del Proyecto (holgura = 0 días): T01 → T02 → T04 → T05 → T06 → T08 → T09 → T10 → T12 → T13 → T15 → T18 → T20.", bold=True, color=COLOR_ACCENT, size=9.2)
    b.add_figure(os.path.join(DIAG_DIR, "diag-01-scrumban-cronograma-kanban.png"), "Figura 1. Cronograma Scrumban + PSP (4 Sprints de 14 días), ruta crítica y tablero Kanban con límites WIP.")

    b.add_h2("1.3 Herramientas de gestión y seguimiento (Jira & GitHub)")
    b.add_p(
        "El seguimiento operativo se administra mediante Jira Software enlazado al repositorio GitHub "
        "(https://github.com/MauricioVega01/stage-plan, rama main), aplicando Conventional Commits (feat, fix, test, docs) "
        "vinculados a cada historia de usuario y criterio de aceptación."
    )

    b.add_h2("1.4 Product Backlog priorizado (Historias de Usuario y Criterios de Aceptación Gherkin)")
    b.add_table(
        "Tabla 5. Product Backlog priorizado por valor de seguridad y negocio (MoSCoW).",
        ["ID", "Historia de Usuario", "Pts", "Prio.", "Criterio de Aceptación (Gherkin)"],
        [
            ["HU01", "Autenticación JWT, bloqueo 423 y control Anti-IDOR", "5", "Must", "Dado un técnico autenticado, cuando solicita /api/venues/:uuidAjeno, entonces el controlador filtra por ownerId y retorna HTTP 404 evitando enumeración; tras 5 fallos de login bloquea 15 min con HTTP 423."],
            ["HU02", "Dimensiones ortogonales del recinto y D.S. N° 38", "3", "Must", "Dada una distancia <= 0 o > 500 m, Zod rechaza la entrada; con medidas válidas proyecta atenuación sonora (dBA) hacia la vivienda vecina."],
            ["HU03", "Cálculo SEC RIC 03/10 y líneas L1/L2/L3", "8", "Must", "Dado un tendido de 35 m con 3.250 W (220V), descarta 1.5 mm² y selecciona 2.5 mm² asegurando ΔV = 2.18% ≤ 3%."],
            ["HU04", "Lotes Activa/Pasiva, Rack de Potencias y Speakon", "5", "Must", "Dadas 3 cajas pasivas de 8 Ω en paralelo, calcula Zeq = 2.67 Ω < 3.2 Ω y dispara alerta DANGER_PROTECT_SHORT; si hay cajas pasivas, dimensiona etapas 19\" con headroom 1.6x y suma su consumo AC 220V."],
            ["HU05", "Ruteo y metraje de cables de audio (XLR / Speakon)", "5", "Must", "Dada una configuración de 2 Tops y 2 Subs, calcula la cantidad exacta de cables balanceados XLR y Speakon sin faltantes."],
            ["HU06", "Plano 2D Blueprint por capas y Postes Guía RIC 10", "8", "Must", "Dado un recinto de 28 m de fondo, renderiza capas exclusivas al configurar (sin ruido visual) y vista completa en reporte con postes guía (R ≥ 6d), clúster mono (+6 dB) y delays Haas."],
            ["HU07", "Réplica Hardware Pioneer DJM (VU + Kill)", "5", "Should", "Al activar 2 bajos simultáneos o forzar Master > 2:00, los 17 LEDs verticales saltan a +12/CLIP rojo y la perilla LOW rota 0°/-135°."],
            ["HU08", "Cotizador Arriendo CLP, Ley del Saco y PDF Dual-Page", "5", "Must", "Al pulsar Descargar PDF sin red, jsPDF compila Memoria Técnica SEC + costos CLP en Pág. 1 y Lámina CAD 2D completa horizontal en Pág. 2, además de permitir descarga PNG 300 DPI."]
        ],
        [0.5, 1.65, 0.35, 0.5, 3.5]
    )

    b.add_h2("1.5 Planificación de los 4 Sprints y Tablero Kanban")
    b.add_table(
        "Tabla 6. Planificación de los 4 Sprints fijos de 14 días bajo Scrumban + PSP.",
        ["Sprint", "Ventana Temporal", "Objetivo del Sprint (Sprint Goal)", "Entregable Verificado"],
        [
            ["Sprint 1", "01-Oct – 14-Oct", "Cerrar diagnóstico, contratos Zod, Arquitectura 4+1 y monorepo.", "CU-00..08, schemas.ts y monorepo configurado."],
            ["Sprint 2", "15-Oct – 28-Oct", "Construir motor determinista SEC, Haas, Pasivos y Ruteo bajo TDD.", "11 módulos TS y suite TDD en Vitest aprobada."],
            ["Sprint 3", "29-Oct – 11-Nov", "Implementar SQLite/Prisma (dev.db), API Express segura y Vue Router.", "API Anti-IDOR + 5 vistas modulares WCAG AA."],
            ["Sprint 4", "12-Nov – 26-Nov", "Integrar Cockpit 100%, Blueprint por capas, Rack Pasivo, Arriendo CLP y PDF Dual-Page.", "PoC funcional verificada, 81/81 tests Vitest PASS y entrega U2."]
        ],
        [0.75, 1.15, 2.6, 2.0]
    )
    b.add_p(
        "Política Kanban y Definition of Done (DoD): El flujo [ Backlog ] → [ Selected for Dev (WIP: 3) ] → "
        "[ In Progress (WIP: 1) ] → [ Testing / TDD (WIP: 2) ] → [ Done ] exige que ninguna tarea cierre sin compilación "
        "limpia (vue-tsc + tsc), 100% PASS en los 81 tests de Vitest, revisión en navegador al 100% de zoom y registro en GitHub."
    )

    # SECCIÓN 2: ARQUITECTURA 4+1
    b.add_h1("2. ARQUITECTURA DE LA SOLUCIÓN – PARADIGMA 4+1 (ISO/IEC/IEEE 42010:2022)")
    b.add_h2("2.1 Requerimientos tecnológicos y de infraestructura del negocio")
    b.add_table(
        "Tabla 7. Stack tecnológico justificado y hoja de ruta de infraestructura hacia Unidad 3.",
        ["Capa", "Tecnología y Versión Real", "Justificación Técnica", "Proyección / Escalabilidad (Unidad 3)"],
        [
            ["Frontend SPA", "Vue 3.5 + Vite 6.4 + Vue Router 4 + Tailwind 3.4", "Arquitectura modular en 5 rutas (/auth, /recinto, /equipos, /plano-2d, /reporte), estado reactivo centralizado en composable useStagePlanState.ts con persistencia localStorage.", "Empaquetado PWA con Service Worker e IndexedDB para sincronización offline."],
            ["Núcleo Shared", "TypeScript 5.7 + Zod 3.24 (11 módulos)", "Código isomórfico compartido por navegador y API: garantiza las mismas fórmulas físicas y validación estricta en frontera.", "Publicación como librería interna reutilizable en clientes móviles."],
            ["Backend API", "Node.js 24 + Express 4.21 + Helmet + RateLimit", "Ecosistema unificado TypeScript, validación Zod, bloqueo temporal HTTP 423, limitador de tasa y manejo centralizado de excepciones.", "Despliegue en contenedor Docker detrás de Nginx TLS 1.3 en VPS."],
            ["Persistencia", "SQLite 3 (dev.db) + Prisma ORM 6.4 (3FN + JSON)", "En PoC local (U2), 4 tablas normalizadas en español + campos JSON auditables directamente en DB Browser for SQLite.", "Migración transparente de provider en Prisma hacia PostgreSQL 16 (12 tablas + JSONB GIN)."],
            ["Auth / Seguridad", "bcrypt (cost 12) + jsonwebtoken (JWT 12h)", "Hashing resistente a fuerza bruta, verificación en authMiddleware con exigencia de JWT_SECRET en producción y Anti-IDOR por ownerId.", "Cookies HttpOnly/SameSite=Strict, token_version, pgcrypto y bitácora audit_logs."],
            ["Salida Terreno", "jsPDF 2.5 + jspdf-autotable + Canvas SVG", "Genera PDF Dual-Page (Memoria + Lámina CAD 2D horizontal) e imagen PNG 300 DPI client-side sin requerir conexión móvil en parcelas.", "Inclusión de código QR verificable para inspección técnica."]
        ],
        [0.95, 1.65, 2.25, 1.65]
    )

    b.add_h2("2.2 Vista de Escenarios: Caso de Uso Cero (CU-00) y Especificación Estructurada")
    b.add_p(
        "El Caso de Uso Cero (CU-00: Planificación Logística Integral) coordina al Operador Técnico FOH, al Chofer/Bodeguero "
        "y al Administrador mediante relaciones <<include>> (CU-01 Acceso JWT/Anti-IDOR, CU-02 Recinto y D.S. N° 38, "
        "CU-03 Ruteo SEC RIC 10 + Postes Guía, CU-05 Iluminación DMX y Cables, CU-08 PDF Dual-Page, Arriendo y Carga) y "
        "<<extend>> (CU-04 Cajas Activa/Pasiva + Rack de Potencias + Speakon, CU-06 Plano Blueprint + Pioneer DJM). "
        "En el caso crítico CU-03 se controlan tres excepciones principales: [E1] rechazo Zod fuera de rango (1..500 m); "
        "[E2] alerta SEC por sobrecarga de disyuntor o caída de tensión > 3%; y [E3] alerta PROTECT ante impedancia < 3.2 Ω."
    )
    b.add_figure(os.path.join(DIAG_DIR, "diag-03-escenarios-caso-uso-cero.png"), "Figura 2. Vista de Escenarios (4+1) — Caso de Uso Cero (CU-00), actores e inclusiones/extensiones.")

    b.add_h2("2.3 Vista Lógica: Diagrama de Clases del Dominio")
    b.add_p(
        "El diseño orientado a objetos desacopla las entidades persistentes (Usuario, Recinto, CalculoRider, EnlaceCompartido) "
        "de los motores matemáticos puros (CalculationEngine con calculatePowerAmpSizing, ElectricalSECValidator, "
        "StageAcousticEngine, LightingDmxCalculator, DjSetupAndGainSimulator y LogisticsAndRentalService), garantizando "
        "correspondencia directa entre los métodos modelados y las pruebas unitarias."
    )
    b.add_figure(os.path.join(DIAG_DIR, "diag-04-vista-logica-clases.png"), "Figura 3. Vista Lógica (4+1) — Diagrama de Clases UML del dominio STAGE PLAN v4.0.")

    b.add_h2("2.4 Vista de Desarrollo: Diagrama de Componentes Monorepo")
    b.add_p(
        "El proyecto se organiza como monorepo npm workspaces en tres paquetes desacoplados: @stageplan/frontend "
        "(Vue Router con 5 vistas especializadas: ViewAuth, ViewVenue, ViewAudioPower, ViewAcousticCanvas, ViewReportSummary, "
        "el composable useStagePlanState.ts, LayoutSvg2D.vue, PioneerMixerSimulator.vue y pdfReport.ts), @stageplan/shared "
        "(schemas.ts + 11 módulos calc-engine + 11 suites Vitest con 81 tests) y @stageplan/backend (server.ts, authMiddleware, "
        "errorHandler, controladores Auth/Venue/Calculation y Prisma ORM)."
    )
    b.add_figure(os.path.join(DIAG_DIR, "diag-05-vista-desarrollo-componentes.png"), "Figura 4. Vista de Desarrollo (4+1) — Diagrama de Componentes del Monorepo TypeScript.")

    b.add_h2("2.5 Vista de Procesos (BPMN 2.0) y 2.6 Vista Física de Despliegue")
    b.add_p(
        "La Vista de Procesos (Figura 5) modela mediante BPMN 2.0 los tres carriles operacionales con compuertas XOR de "
        "validación Zod, cumplimiento SEC (ΔV ≤ 3%) e impedancia Speakon (Zeq ≥ 3.2 Ω). La Vista Física (Figura 6) "
        "distingue claramente el entorno PoC ejecutable de Unidad 2 (SPA local + Express :3000 + SQLite dev.db + PDF autónomo) "
        "y la arquitectura objetivo de Unidad 3 (VPS Linux detrás de proxy inverso Nginx TLS 1.3 con PostgreSQL 16)."
    )
    b.add_figure(os.path.join(DIAG_DIR, "diag-06-vista-procesos-bpmn.png"), "Figura 5. Vista de Procesos (4+1) — Diagrama BPMN 2.0 de pre-producción y compuertas normativas SEC.")
    b.add_figure(os.path.join(DIAG_DIR, "diag-02-arquitectura-4plus1-despliegue.png"), "Figura 6. Vista Física y de Despliegue (4+1) — Arquitectura PoC local, proyección VPS TLS 1.3 y operación autónoma en terreno.")

    # SECCIÓN 3: UX/UI Y PROTOTIPO
    b.add_h1("3. DISEÑO DE EXPERIENCIA E INTERFAZ DE USUARIO (UX/UI)")
    b.add_h2("3.1 Definición de perfiles de usuario (User Personas)")
    b.add_table(
        "Tabla 8. User Personas representativos del flujo operacional de DISTORSIONCL SPA.",
        ["User Persona", "Rol y Contexto Operacional", "Puntos de Dolor", "Objetivo con STAGE PLAN"],
        [
            ["Amaro Artiaga (28)", "Operador FOH / DJ en parcelas nocturnas sin 4G (< 2h montaje).", "Cortes de luz, ruido visual en planos, dudas de etapas pasivas y clipping en cabina.", "Dimensionar en < 3 min al 100% de zoom y llevar PDF Dual-Page en terreno."],
            ["Cristián Morales (34)", "Chofer y Bodeguero encargado de carga de camioneta.", "Olvido de cables de poder o Speakon y bultos > 25 kg (Ley del Saco N° 20.949).", "Recibir checklist exacto, plano PNG 300 DPI y resumen por WhatsApp."],
            ["Mauricio Vega (Admin)", "Responsable técnico, costos y auditoría de montajes.", "Falta de historial técnico y estimación rápida de arriendo externo.", "Auditar cálculos en SQLite/Prisma y cotizar rider propio vs arrendado."]
        ],
        [1.25, 1.8, 1.75, 1.7]
    )

    b.add_h2("3.2 Priorización MoSCoW, arquitectura de información y sistema visual (WCAG 2.1 AA)")
    b.add_p(
        "Alcance MoSCoW: Must Have — Autenticación JWT y control Anti-IDOR, geometría ortogonal y ruido vecinal D.S. N° 38, "
        "cálculo eléctrico SEC RIC 03/10, lotes Activa/Pasiva con dimensionamiento de rack de potencias y alerta Speakon "
        "< 3.2 Ω, Plano 2D Blueprint por capas con postes guía RIC 10 y exportación PDF Dual-Page + PNG 300 DPI. "
        "Should Have — Réplica Pioneer DJM con vúmetros verticales, cotizador de arriendo en CLP y Plan B contingencia. "
        "Could Have — Copia WhatsApp en 1 clic y enlaces compartidos de consulta. Won't Have (fuera de alcance) — "
        "Procesamiento DSP de audio en tiempo real o control físico de luminarias por protocolo DMX."
    )
    b.add_p(
        "Sistema de Diseño Fullscreen Studio Cockpit (100% Zoom): Para eliminar scroll vertical innecesario en laptops y "
        "pantallas estándar al 100% de zoom, la aplicación adopta una grilla fullscreen de altura fija (100vh) con barra "
        "superior de navegación por rutas URL (/auth, /recinto, /equipos, /plano-2d, /reporte), barra inferior de "
        "telemetría en vivo y paleta Dark Mode técnico (#080a10 / #0c0e15) con contraste WCAG 2.1 AA (≥ 4.5:1), semáforo "
        "normativo (Verde #10B981, Ámbar #F59E0B, Rojo #DC2626) y adaptación responsive para escritorio (1440 px), tablet "
        "(768 px) y smartphone en terreno (412 px)."
    )
    b.add_figure(os.path.join(DIAG_DIR, "diag-08-mapa-navegacion-ux.png"), "Figura 7. Arquitectura de información y mapa de navegación Cockpit (5 rutas Vue Router y adaptación responsive).")

    b.add_h2("3.3 Prototipo funcional actual e integración de retroalimentación real")
    b.add_p(
        "Las Figuras 8 a 11 muestran capturas directas de la aplicación web en ejecución tras las cuatro iteraciones de "
        "mejora realizadas junto al operador de DISTORSIONCL SPA:"
    )
    b.add_figure(os.path.join(SHOT_DIR, "prototipo-mosaico-stageplan.png"), "Figura 8. Mosaico funcional actualizado (P01–P06) del prototipo web STAGE PLAN en configuración Studio Cockpit al 100% de zoom.")
    b.add_figure(os.path.join(SHOT_DIR, "prototipo-P05-plano-2d-postes-guia-sec.png"), "Figura 9. Captura real Vista 3 (/plano-2d) — Plano 2D Blueprint Dark con selector de 5 capas exclusivas, Postes Guía SEC RIC N° 10 y controles de zoom.")
    b.add_figure(os.path.join(SHOT_DIR, "prototipo-P04-simulador-pioneer-djm.png"), "Figura 10. Captura real Vista 3 — Réplica interactiva Pioneer DJM con vúmetros verticales de 17 LEDs, Low Kill y Master Rotary.")
    b.add_figure(os.path.join(SHOT_DIR, "prototipo-movil-terreno.png"), "Figura 11. Captura real adaptativa móvil (412×915 px) de Vista 4 (/reporte), verificando legibilidad y cotizador en terreno.", width_inches=2.7)

    b.add_table(
        "Tabla 9. Registro de retroalimentación recogida con DISTORSIONCL SPA (Amaro Artiaga) e iteraciones aplicadas.",
        ["Iteración", "Hallazgo / Solicitud del Usuario", "Mejora Implementada en STAGE PLAN", "Estado"],
        [
            ["Iteración 1", "Evitar ingreso manual repetitivo de Watts en terreno y facilitar envío al chofer.", "Catálogo de 8 escalas preset en 1 clic y botón de resumen técnico para WhatsApp.", "Integrado"],
            ["Iteración 2", "Combinar cajas activas y pasivas calculando cables Speakon y señal sin sobrantes.", "Selector Activa/Pasiva multilote y ruteo métrico exacto XLR / Speakon NL4.", "Integrado"],
            ["Iteración 3", "Evitar cruces de líneas sobre la pista y visualizar la regla de un solo bajo en DJM.", "LayoutSvg2D proporcional con Postes Guía R ≥ 6d (RIC 10) y PioneerMixerSimulator.vue.", "Integrado"],
            ["Iteración 4", "Reducir saturación visual del mapa al editar, dimensionar el rack de potencias pasivas, cotizar arriendo y adjuntar el plano completo al PDF.", "Diseño Studio Cockpit al 100% zoom, Plano Blueprint con 5 capas exclusivas (Vista Completa ALL en /reporte), calculatePowerAmpSizing (headroom 1.6x), cotizador CLP y PDF Dual-Page + PNG 300 DPI.", "Integrado"]
        ],
        [0.85, 2.2, 2.55, 0.9]
    )

    # SECCIÓN 4: BASE DE DATOS
    b.add_h1("4. MODELO Y ADMINISTRACIÓN DE BASE DE DATOS")
    b.add_h2("4.1 Implementación PoC en SQLite 3 + Prisma ORM y proyección a PostgreSQL 16")
    b.add_p(
        "Para garantizar un entorno de pruebas y demostración portable, autocontenido y verificable sin dependencias de "
        "servicios externos, la prueba de concepto de Unidad 2 implementa una arquitectura híbrida (Relacional 3FN + "
        "documentos JSON) sobre SQLite 3 (dev.db) administrado mediante Prisma ORM 6.4 (packages/backend/prisma/schema.prisma). "
        "Las 4 tablas núcleo en español garantizan integridad referencial estricta (llaves primarias UUID/TEXT, claves "
        "foráneas con ON DELETE CASCADE y control de intentos fallidos de login), mientras que las columnas JSON absorben "
        "la variabilidad polimórfica de equipos y resultados sin proliferación innecesaria de tablas pivote."
    )
    b.add_p(
        "De forma complementaria, se diseñó el esquema físico objetivo de producción para Unidad 3 en PostgreSQL 16 "
        "(entrega_sumativa_02/sql/schema_stageplan_pg16.sql), el cual expande el modelo a 12 tablas normalizadas, añade "
        "índices GIN (jsonb_path_ops) sobre documentos JSONB, triggers PL/pgSQL de validación SEC (ΔV ≤ 3%), bitácora "
        "inmutable audit_logs y soporte de cifrado pgcrypto. Gracias a Prisma ORM, la migración entre ambos motores se "
        "realiza cambiando la directiva datasource en schema.prisma."
    )

    b.add_h2("4.2 Diseño estructural implementado (DER 4 tablas 3FN en español + JSON)")
    b.add_figure(os.path.join(DIAG_DIR, "diag-07-modelo-datos-der.png"), "Figura 12. Diagrama Entidad-Relación (DER) del modelo híbrido implementado en SQLite (dev.db) y proyección PostgreSQL 16 (U3).")
    b.add_table(
        "Tabla 10. Diccionario de las 4 tablas normalizadas en español implementadas en SQLite (dev.db) y Prisma ORM.",
        ["#", "Tabla", "PK / FKs y Reglas Referenciales", "Atributos Estructurados y Campos JSON"],
        [
            ["1", "usuarios", "PK id (TEXT/UUID)", "correo (UNIQUE), clave_hash (bcrypt 12), nombre, rol ('ADMIN'), intentos_fallidos (INTEGER), bloqueado_hasta (DATETIME?), fecha_creacion, fecha_actualizacion"],
            ["2", "recintos", "PK id (TEXT/UUID) | FK usuario_id → usuarios CASCADE", "nombre, ancho_metros, largo_metros, alto_metros, tipo_entorno, distancia_electrica_metros, fecha_creacion, fecha_actualizacion"],
            ["3", "calculos_rider", "PK id | FK usuario_id, recinto_id CASCADE", "version_motor ('4.0.0'), entrada_rider (JSON), parametros_usados (JSON), resultados_calculados (JSON), alertas_snapshot (JSON), fecha_creacion"],
            ["4", "enlaces_compartidos", "PK id | FK usuario_id, calculo_rider_id CASCADE", "token (UNIQUE), fecha_expiracion, esta_revocado (INTEGER 0/1), fecha_creacion"]
        ],
        [0.3, 1.35, 2.35, 2.5]
    )
    b.add_code(
        '{\n'
        '  "totalWatts": 2600,\n'
        '  "designAmps": 14.18,\n'
        '  "electricalSummary": {\n'
        '    "recommendedSectionMm2": 2.5,\n'
        '    "voltageDropVolts": 4.71,\n'
        '    "voltageDropPct": 2.14,\n'
        '    "secCompliant": 1,\n'
        '    "normativeRule": "Pliego SEC RIC N° 03 (ΔV <= 3%)"\n'
        '  },\n'
        '  "acousticSummary": {\n'
        '    "monoClusterCentral": true,\n'
        '    "clusterGainDb": 6.0,\n'
        '    "delayTowerHaasMs": 29.14,\n'
        '    "sweetSpotDba": "96-102 dBA"\n'
        '  },\n'
        '  "cablingLogistics": {\n'
        '    "xlrCablesRequired": 6,\n'
        '    "speakonCablesRequired": 4,\n'
        '    "powerExtensions25mm2": 2,\n'
        '    "weightTotalKg": 18.5,\n'
        '    "leyDelSacoCompliant": true\n'
        '  }\n'
        '}',
        title="Ejemplo de documento JSON almacenado en calculos_rider.resultados_calculados (dev.db):"
    )

    b.add_h2("4.3 Estrategia de consultas híbridas SQL + JSON y migración a producción")
    b.add_code(
        "-- Consulta híbrida verificable directamente en DB Browser for SQLite sobre dev.db:\n"
        "SELECT u.nombre AS operador, r.nombre AS recinto, c.version_motor,\n"
        "       json_extract(c.resultados_calculados, '$.totalWatts') AS total_watts,\n"
        "       json_extract(c.resultados_calculados, '$.electricalSummary.recommendedSectionMm2') AS seccion_cable_mm2,\n"
        "       json_extract(c.resultados_calculados, '$.electricalSummary.voltageDropPct') AS caida_tension_pct,\n"
        "       json_extract(c.resultados_calculados, '$.acousticSummary.sweetSpotDba') AS sweet_spot_dba\n"
        "FROM usuarios u\n"
        "JOIN recintos r ON u.id = r.usuario_id\n"
        "JOIN calculos_rider c ON r.id = c.recinto_id\n"
        "WHERE json_extract(c.resultados_calculados, '$.electricalSummary.secCompliant') = 1;",
        title="Consulta SQL + extracción JSON (json_extract) sobre el archivo físico dev.db:"
    )

    # SECCIÓN 5: SEGURIDAD
    b.add_h1("5. ESTÁNDARES DE PROGRAMACIÓN SEGURA")
    b.add_h2("5.1 Matriz de roles, perfiles y control de acceso (RBAC y Anti-IDOR)")
    b.add_p(
        "En la PoC actual se implementa el control de propiedad estricto por usuario autenticado (ownerId === req.user.id) "
        "y el campo rol en la tabla usuarios. La tabla siguiente consolida la política RBAC completa, distinguiendo las "
        "capacidades ya operativas en la API de aquellas diseñadas para el despliegue multi-perfil de Unidad 3."
    )
    b.add_table(
        "Tabla 11. Matriz de Control de Acceso Basado en Roles (RBAC) y aislamiento Anti-IDOR.",
        ["Operación / Recurso", "Administrador (Diseñado U3)", "Operador FOH (Implementado PoC)", "Chofer / Invitado (Diseñado U3)"],
        [
            ["Autenticación (/api/auth/login, /me)", "Sí (Bcrypt + JWT)", "Sí (Bcrypt 12 + JWT 12h + Bloqueo 423)", "No (token de enlace temporal)"],
            ["CRUD Recintos propios (/api/venues/*)", "Auditoría global", "CRUD Propios (Anti-IDOR → HTTP 404 ajeno)", "Denegado (401/403)"],
            ["Ejecutar y listar cálculos (/calculate, /history)", "Auditoría global", "Crear / Leer Propios (ownerId === req.user.id)", "Denegado (403)"],
            ["Generar / Revocar enlaces_compartidos", "Revocación global", "Modelo BD creado (Endpoints planif. U3)", "Solo consumo lectura vigente"],
            ["Descarga PDF Terreno (Client-Side)", "Sí", "Sí (PDF Dual-Page y PNG 300 DPI offline)", "Solo lectura vía enlace"],
            ["Bitácora forense audit_logs", "Lectura completa (DDL PG16 U3)", "Denegado", "Denegado"]
        ],
        [2.1, 1.35, 1.75, 1.3]
    )

    b.add_h2("5.2 Lineamientos de codificación segura implementados y proyección OWASP Top 10")
    b.add_h3("a. Validación y saneamiento de entradas (Zod Isomórfico)")
    b.add_p(
        "Todas las peticiones HTTP (RegisterSchema, LoginSchema en auth.controller.ts, VenueSchema y RiderSchema en "
        "@stageplan/shared/src/schemas.ts) se validan con Zod antes de alcanzar lógica de cálculo o base de datos, "
        "imponiendo rangos físicos positivos y retornando HTTP 400 ante payloads malformados."
    )
    b.add_h3("b. Autenticación, bloqueo ante fuerza bruta, Anti-IDOR y Rate Limiting")
    b.add_p(
        "Controles implementados en backend: hashing con bcrypt (12 rondas de sal); bloqueo temporal automático de cuenta "
        "por 15 minutos tras 5 intentos fallidos consecutivos (intentos_fallidos y bloqueado_hasta en Prisma) devolviendo "
        "HTTP 423 Locked; limitador express-rate-limit configurado en 200 req/15 min para /api y 10 req/15 min específicos "
        "sobre /api/auth/login; firma JWT (12h) verificada en authMiddleware con bloqueo fatal de arranque en producción "
        "si falta JWT_SECRET; y control Anti-IDOR en VenueController y CalculationController exigiendo ownerId === req.user.id "
        "en cada consulta Prisma (retornando HTTP 404 para evitar enumeración de UUIDs). Para Unidad 3 se proyecta migrar el "
        "almacenamiento de sesión hacia cookies HttpOnly/SameSite=Strict e incorporar rotación por token_version."
    )
    b.add_h3("c. Gestión segura de errores y excepciones")
    b.add_p(
        "Las rutas asíncronas están encapsuladas con asyncHandler y canalizadas hacia el middleware centralizado errorHandler "
        "(packages/backend/src/middlewares/errorHandler.ts), impidiendo promesas no capturadas y devolviendo respuestas JSON "
        "normalizadas sin filtrar stack traces ni estructura interna al cliente."
    )
    b.add_h3("d. Cabeceras HTTP defensivas, cifrado y matriz OWASP Top 10 (2021)")
    b.add_p(
        "El servidor aplica helmet() (CSP, X-Frame-Options, nosniff y remoción de X-Powered-By) y política CORS acotada "
        "a FRONTEND_URL. El cifrado en tránsito TLS 1.3 con HSTS y el cifrado AES-256 en reposo (pgcrypto) corresponden "
        "al despliegue productivo en VPS de Unidad 3 conforme a la Ley N° 19.628 / N° 21.719."
    )
    b.add_table(
        "Tabla 12. Identificación de los 10 riesgos OWASP Top 10 (2021) y estado de mitigación en STAGE PLAN.",
        ["Categoría OWASP 2021", "Amenaza en STAGE PLAN", "Control Técnico (Implementado en PoC vs. Proyectado U3)"],
        [
            ["A01: Broken Access Control", "Manipulación UUID en /api/venues/:id o /calculations/:id (IDOR).", "Implementado: filtro obligatorio ownerId === req.user.id en Prisma retornando HTTP 404. Proy. U3: registro en audit_logs."],
            ["A02: Cryptographic Failures", "Robo de claves o captura de tokens en redes Wi-Fi de recintos.", "Implementado: bcrypt(12), .env excluido en .gitignore. Proy. U3: TLS 1.3 + HSTS en Nginx y pgcrypto en PG16."],
            ["A03: Injection", "SQLi en nombres de recinto o XSS en nombres de equipos/luminarias.", "Implementado: consultas parametrizadas Prisma ORM + validación Zod + escape automático en plantillas Vue 3 (sin v-html)."],
            ["A04: Insecure Design", "Aprobar cables subdimensionados o impedancias < 3.2 Ω.", "Implementado: reglas físicas inmutables en @stageplan/shared. Proy. U3: refuerzo con Triggers CHECK en PostgreSQL 16."],
            ["A05: Security Misconfiguration", "Cabecera X-Powered-By, CORS abierto * o arranque sin secreto.", "Implementado: helmet(), CORS acotado a FRONTEND_URL y salida fatal en server.ts si falta JWT_SECRET en producción."],
            ["A06: Vulnerable Components", "Librerías npm desactualizadas con vulnerabilidades conocidas.", "Implementado: bloqueo de versiones con package-lock.json y stack actualizado (Vue 3.5, Express 4.21, Prisma 6.4)."],
            ["A07: Auth & ID Failures", "Ataques de fuerza bruta sobre login o enumeración de cuentas.", "Implementado: loginLimiter (10 req/15m), bloqueo HTTP 423 por 15 min tras 5 fallos, mensajes genéricos. Proy. U3: token_version."],
            ["A08: Integrity Failures", "Alteración desde el cliente de consumos y secciones de cable.", "Implementado: CalculationController ejecuta nuevamente @stageplan/shared en servidor sin confiar en totales del cliente."],
            ["A09: Logging Failures", "Falta de trazabilidad forense ante intentos fallidos o IDOR.", "Implementado: errorHandler y contador intentos_fallidos en SQLite. Proy. U3: tabla inmutable audit_logs en PG16."],
            ["A10: SSRF", "Sondeo de puertos internos del servidor vía generación de PDF.", "Implementado: el servidor no realiza fetch a URLs de usuario; la exportación PDF Dual-Page corre 100% en el navegador."]
        ],
        [1.55, 1.95, 3.0]
    )

    # SECCIÓN 6: PLAN DE PRUEBAS Y QA
    b.add_h1("6. PLAN DE PRUEBAS Y ASEGURAMIENTO DE LA CALIDAD")
    b.add_h2("6.1 Estrategia TDD y balance de herramientas automatizadas y manuales")
    b.add_p(
        "El núcleo de cálculo @stageplan/shared se desarrolló aplicando Desarrollo Guiado por Pruebas (TDD) con Vitest v3.2.7, "
        "combinando herramientas automatizadas de verificación estática y rendimiento con pruebas manuales de API y usabilidad "
        "en dispositivos móviles y navegadores al 100% de zoom."
    )
    b.add_table(
        "Tabla 13. Herramientas automatizadas y manuales del plan de aseguramiento de calidad.",
        ["Tipo", "Herramienta", "Función en STAGE PLAN", "Estado"],
        [
            ["Automatizada", "Vitest v3.2.7", "Ejecución de 11 suites (81 pruebas unitarias) sobre los 11 módulos calc-engine.", "81/81 PASS (186 ms)"],
            ["Automatizada", "vue-tsc + tsc + Vite", "Comprobación estricta de tipos en 3 workspaces y compilación de producción.", "0 errores"],
            ["Automatizada", "Node perf_hooks / k6", "Benchmark de 1.000 iteraciones del motor local (medido) + carga API 5 VUs (U3).", "0,0286 ms prom. (local)"],
            ["Automatizada", "npm audit + OWASP ZAP", "Auditoría de dependencias y escaneo activo de rutas tras despliegue.", "Planificada VPS (U3)"],
            ["Manual", "Chrome DevTools / Puppeteer", "Inspección de rutas URL, zoom 100%, modal Pioneer DJM y exportación CAD/PDF.", "Verificada (0 errores)"],
            ["Manual", "Smartphone 412px + Terreno", "Validación ergonómica táctil, contraste Dark Mode y lectura en DISTORSIONCL SPA.", "Validada con operador"]
        ],
        [1.0, 1.5, 2.7, 1.3]
    )

    b.add_h2("6.2 Matriz de 20 casos de prueba (Unitarias, Funcionales, Integración, Seguridad y Usabilidad)")
    b.add_table(
        "Tabla 14. Matriz integral de casos de prueba ejecutados y proyectados.",
        ["ID", "Tipo", "Módulo / Endpoint", "Escenario y Resultado Esperado / Obtenido", "Estado"],
        [
            ["PU-01", "Unitaria", "electrical.ts", "Tendido 35 m, 3.250 W → selecciona 2.5 mm² con ΔV = 2.18% ≤ 3%.", "PASS"],
            ["PU-02", "Unitaria", "electrical.ts", "Carga 4.000 W en 10 m → prevalece ampacidad y asigna 4.0 mm².", "PASS"],
            ["PU-03", "Unitaria", "hybrid-roster.ts", "3 cajas pasivas 8 Ω en paralelo → Zeq = 2.67 Ω → DANGER_PROTECT_SHORT.", "PASS"],
            ["PU-04", "Unitaria", "hybrid-roster.ts (PA-01..06)", "Dimensionamiento de rack de potencias pasivas (headroom 1.6x, carga 4/8 Ω, consumo AC 220V).", "PASS"],
            ["PU-05", "Unitaria", "stage-acoustic-engine.ts", "Recinto 28 m con 4 subs y delays → +6 dB clúster, +44.3 ms / +60.7 ms Haas.", "PASS"],
            ["PU-06", "Unitaria", "stage-acoustic-engine.ts", "Evaluación Indoor (Sabine RT60) vs. Parcela abierta frente a cobertura y D.S. N° 38.", "PASS"],
            ["PU-07", "Unitaria", "cabling.ts", "2 Tops + 2 Subs en 25 m → cálculo exacto de cables XLR y Speakon NL4.", "PASS"],
            ["PU-08", "Unitaria", "dj-setup-audio.ts", "2× CDJ + Mixer DJM + Retorno + Power → rutas RCA, RJ45, TRS-XLR, Speakon.", "PASS"],
            ["PU-09", "Unitaria", "power-distribution.ts", "Asignación zapatillas Z1..Z4 (10A/16A) respetando 80% de capacidad continua.", "PASS"],
            ["PU-10", "Unitaria", "contingency-and-logistics.ts", "Subwoofer 38 kg (> 25 kg) → alerta obligatoria Ley del Saco N° 20.949.", "PASS"],
            ["PF-01", "Funcional", "PioneerMixerSimulator.vue", "2 bajos activos o Master > 2:00 → 17 LEDs en rojo +12/CLIP.", "PASS"],
            ["PF-02", "Funcional", "LayoutSvg2D.vue", "Selector de 5 capas Blueprint al editar y Vista Completa (ALL) en /reporte.", "PASS"],
            ["PF-03", "Funcional", "pdfReport.ts + useStagePlanState", "Captura CAD PNG 300 DPI + PDF Dual-Page (Memoria + Lámina landscape) y cotizador CLP.", "PASS"],
            ["PI-01", "Integración", "POST /api/auth/register + login", "Registro bcrypt(12) + emisión JWT (12h) en SQLite dev.db → HTTP 201 / HTTP 200.", "Planif. API E2E"],
            ["PI-02", "Integración", "POST /api/venues/:id/calculate", "Payload JSON → Zod → Engine v4.0 → Prisma → HTTP 201.", "Planif. API E2E"],
            ["PR-01", "Rendimiento", "@stageplan/shared (1.000×)", "Benchmark medido: promedio 0,0286 ms (p95: 0,0479 ms; p99: 0,3241 ms < 50 ms).", "PASS Medido"],
            ["PR-02", "Rendimiento", "API Express (k6, 5 VUs)", "Carga concurrente 60 s en /calculate → p95 < 250 ms y 0% errores 5xx.", "Planif. VPS U3"],
            ["PS-01", "Seguridad", "GET /api/venues/:uuidAjeno", "Control Anti-IDOR con JWT de otro usuario → HTTP 404 + aislamiento por ownerId.", "Implementado / U3 E2E"],
            ["PS-02", "Seguridad", "POST /api/auth/login", "5 fallos consecutivos → HTTP 423 Locked 15 min; >10 req/15m → Rate Limit 429.", "Implementado / U3 E2E"],
            ["PU-UX", "Usabilidad", "Desktop 100% + Móvil 412×915", "Cockpit fullscreen en 5 rutas URL sin desborde horizontal ni scroll roto.", "PASS Verificado"]
        ],
        [0.55, 0.85, 1.5, 2.85, 0.75]
    )

    b.add_h2("6.3 Evidencia de ejecución automatizada y benchmark (81/81 Vitest PASS)")
    b.add_p(
        "Prueba de Rendimiento (PR-01): Sobre 1.000 iteraciones completas en Node.js v24 del pipeline completo "
        "(eléctrico SEC + acústica Haas + lotes pasivos + cables + DJ setup), se registró una latencia promedio de "
        "0,0286 ms (p50 = 0,0158 ms, p95 = 0,0479 ms, p99 = 0,3241 ms, máx = 4,2926 ms), muy por debajo del umbral de 50 ms."
    )
    b.add_code(
        "RUN  v3.2.7 packages/shared\n"
        " ✓ tests/routing-and-gaffer.spec.ts (10 tests) 14ms\n"
        " ✓ tests/power-distribution.spec.ts (8 tests) 27ms\n"
        " ✓ tests/calc-engine.spec.ts (23 tests) 25ms\n"
        " ✓ tests/lighting-dmx.spec.ts (8 tests) 21ms\n"
        " ✓ tests/qa-gap-branches.spec.ts (5 tests) 14ms\n"
        " ✓ tests/hybrid-roster.spec.ts (8 tests) 30ms\n"
        " ✓ tests/stage-acoustic-engine.spec.ts (5 tests) 15ms\n"
        " ✓ tests/contingency-logistics.spec.ts (6 tests) 12ms\n"
        " ✓ tests/dj-setup-audio.spec.ts (4 tests) 12ms\n"
        " ✓ tests/stage-acoustic-indoor-outdoor.spec.ts (2 tests) 8ms\n"
        " ✓ tests/cabling.spec.ts (2 tests) 7ms\n\n"
        "Test Files  11 passed (11)\n"
        "     Tests  81 passed (81)\n"
        "  Duration  7.65s (tests 186ms)",
        title="Evidencia real de ejecución automatizada (npm test — Vitest v3.2.7):"
    )

    b.add_h2("6.4 Alineación del aseguramiento de calidad con OWASP Top 10")
    b.add_p(
        "Las validaciones estáticas (vue-tsc y tsc), los esquemas Zod isomórficos y las pruebas unitarias sobre límites "
        "físicos (SEC RIC N° 03/10 e impedancia Speakon) previenen en origen entradas fuera de rango y cálculos alterados "
        "desde el cliente (A03, A04 y A08), complementando los controles de acceso y autenticación del backend (A01 y A07) "
        "que serán sometidos a pruebas automatizadas de carga e intrusión tras el despliegue en Unidad 3."
    )

    # CONCLUSIONES
    b.add_h1("CONCLUSIONES")
    b.add_p(
        "1. Cumplimiento de los objetivos de ingeniería: STAGE PLAN transforma la pre-producción técnica de DISTORSIONCL SPA "
        "desde estimaciones empíricas hacia un flujo determinista trazable bajo normativa chilena (SEC RIC N° 03 y N° 10, "
        "Decreto Supremo N° 38 del MMA y Ley del Saco N° 20.949), integrando además dimensionamiento de amplificación para "
        "equipos pasivos y cotización operativa en CLP."
    )
    b.add_p(
        "2. Viabilidad del enfoque Scrumban + PSP en desarrollo individual: La planificación en 4 Sprints de 14 días con "
        "límite WIP = 1, respaldada por compilación estricta TypeScript y 81 pruebas unitarias en Vitest al 100% de "
        "aprobación (0,0286 ms promedio), permite sostener consistencia técnica y control de regresiones con un solo desarrollador."
    )
    b.add_p(
        "3. Arquitectura desacoplada y persistencia híbrida: El monorepo basado en vista 4+1 (ISO/IEC/IEEE 42010:2022) y "
        "la base de datos SQLite 3 (dev.db, 4 tablas 3FN en español + JSON) resuelven la portabilidad de la prueba de "
        "concepto en local mientras dejan estructurada la migración hacia PostgreSQL 16 para producción."
    )
    b.add_p(
        "4. Usabilidad en terreno y seguridad desde el diseño: El entorno Studio Cockpit calibrado al 100% de zoom, el plano "
        "Blueprint por capas con lámina PDF Dual-Page autónoma y los controles defensivos de la API (Zod, bcrypt, bloqueo "
        "HTTP 423, Anti-IDOR y errorHandler) cierran la fase de diseño lista para pasar a construcción y despliegue."
    )

    # REFERENCIAS BIBLIOGRÁFICAS
    b.add_h1("REFERENCIAS BIBLIOGRÁFICAS")
    refs = [
        "Beck, K. (2003). Test-Driven Development: By Example. Addison-Wesley Professional.",
        "Biblioteca del Congreso Nacional de Chile (BCN). (1999). Ley N° 19.628: Sobre protección de la vida privada (y modificación Ley N° 21.719).",
        "Biblioteca del Congreso Nacional de Chile (BCN). (2016). Ley N° 20.949: Modifica el Código del Trabajo para reducir el peso de las cargas de manipulación manual (Ley del Saco).",
        "Davis, D., & Patronis, E. (2012). Sound System Engineering (4th ed.). Focal Press.",
        "International Organization for Standardization. (2022). Systems and software engineering — Architecture description (ISO/IEC/IEEE Standard No. 42010:2022).",
        "Kruchten, P. (1995). Architectural Blueprints—The '4+1' View Model of Software Architecture. IEEE Software, 12(6), 42–50.",
        "Ministerio del Medio Ambiente (Chile). (2011). Decreto Supremo N° 38: Norma de emisión de ruidos generados por fuentes que indica.",
        "OWASP Foundation. (2021). OWASP Top 10:2021 — The Ten Most Critical Web Application Security Risks. https://owasp.org/Top10/es/",
        "Superintendencia de Electricidad y Combustibles (SEC). (2020). Pliegos Técnicos Normativos RIC N° 03 (Alimentadores) y RIC N° 10 (Instalaciones de Uso General). Resolución Exenta N° 33.877.",
        "W3C. (2018). Web Content Accessibility Guidelines (WCAG) 2.1 Level AA. https://www.w3.org/TR/WCAG21/"
    ]
    for rf in refs:
        b.add_p(f"• {rf}", size=9.2, space_after=3)

    # ANEXOS (SOLO ANEXO A DE TRAZABILIDAD SOBRIA Y ANEXO B MERMAID; SIN BANCO DE PREGUNTAS DE DEFENSA)
    b.add_h1("ANEXOS")
    b.add_h2("Anexo A. Matriz de Trazabilidad de Entregables (Unidad 2)")
    b.add_table(
        "Tabla 15. Correspondencia entre los componentes documentados y la evidencia técnica del proyecto.",
        ["Área / Requisito de Ingeniería", "Sección del Informe y Evidencia Verificable", "Estado"],
        [
            ["Actividades Formativas U2 (Guía ABPRO)", "Sección Actividades Formativas: Tablas 1 y 2 (Brainstorming + Matriz Priorización).", "Documentado"],
            ["Metodología, Cronograma, Dependencias y Backlog", "Sección 1.1–1.5: Scrumban+PSP, Tablas 3–6 (T01–T20, Ruta Crítica, Gherkin) y Figura 1.", "Documentado"],
            ["Arquitectura 4+1 (ISO/IEC/IEEE 42010) y Stack", "Sección 2.1–2.6: Tabla 7 (Vue Router, shared, Express, SQLite/PG16) y Figuras 2–6.", "Implementado en PoC"],
            ["Prototipo Interactivo, UX/UI y Retroalimentación", "Sección 3.1–3.3: Cockpit 100% zoom, Blueprint capas, Rack Pasivo, Arriendo, Figuras 7–11 y Tabla 9.", "Implementado en PoC"],
            ["Modelo de Datos Híbrido (3FN + JSON / PG16 U3)", "Sección 4.1–4.3: SQLite dev.db (4 tablas en español), Figura 12, Tabla 10 y schema_stageplan_pg16.sql.", "Implementado en PoC / Proyectado U3"],
            ["Seguridad, RBAC, Anti-IDOR y OWASP Top 10", "Sección 5.1–5.2: Tablas 11–12 (Zod, bcrypt 12, bloqueo 423, Anti-IDOR 404, errorHandler).", "Implementado en PoC / Proyectado U3"],
            ["Plan de Pruebas TDD, Rendimiento y Calidad", "Sección 6.1–6.4: Tablas 13–14, 81/81 tests Vitest PASS (11 suites) y benchmark 0,0286 ms.", "Ejecutado y Verificado"]
        ],
        [2.25, 3.15, 1.1]
    )

    b.add_h2("Anexo B. Código Fuente Mermaid de los Diagramas Principales")
    b.add_code(
        "flowchart LR\n"
        "  C[Navegador FOH: Vue 3 + Router + PDF Dual-Page] -->|HTTP Local / HTTPS U3| B[@stageplan/backend Express :3000]\n"
        "  C --> S[@stageplan/shared 11 Modulos + Zod + 81 Tests]\n"
        "  B --> S\n"
        "  B -->|Prisma ORM| D[(SQLite 3 dev.db: 4 Tablas 3FN + JSON)]\n"
        "  D -.->|Migracion U3| P[(PostgreSQL 16: 12 Tablas + JSONB GIN)]\n\n"
        "erDiagram\n"
        "  USUARIOS ||--o{ RECINTOS : posee\n"
        "  USUARIOS ||--o{ CALCULOS_RIDER : ejecuta\n"
        "  RECINTOS ||--o{ CALCULOS_RIDER : contiene\n"
        "  USUARIOS ||--o{ ENLACES_COMPARTIDOS : genera\n"
        "  CALCULOS_RIDER ||--o{ ENLACES_COMPARTIDOS : comparte",
        title="Código Mermaid reproducible (Arquitectura Monorepo/Datos y DER 4 tablas):"
    )

    out_entrega = os.path.join(ENTREGA_DIR, "Proyecto_Integrado_U2_Mauricio_Vega_G10_FINAL.docx")
    out_repo = os.path.join(BASE_DIR, "Proyecto_Integrado_U2_Mauricio_Vega_G10_FINAL.docx")
    doc.save(out_entrega)
    shutil.copy2(out_entrega, out_repo)
    print(f"DOCX SAVED: {out_entrega} ({os.path.getsize(out_entrega)/1024:.1f} KB)")
    print(f"DOCX COPY:  {out_repo}")


if __name__ == "__main__":
    build_sumativa_02()
