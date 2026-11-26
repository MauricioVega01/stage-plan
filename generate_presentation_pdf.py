from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFillColor(colors.HexColor('#09090B'))
        self.rect(0, 580, 792, 32, fill=1, stroke=0)

        self.setFillColor(colors.HexColor('#DC2626'))
        self.rect(0, 577, 792, 3, fill=1, stroke=0)

        self.setFont('Helvetica-Bold', 10)
        self.setFillColor(colors.white)
        self.drawString(36, 592, "STAGE PLAN (v4.0)  |  Proyecto Integrado TIHV43 — INACAP Sede Maipú")

        self.setFont('Helvetica', 9)
        self.setFillColor(colors.HexColor('#D4D4D8'))
        self.drawRightString(756, 592, "Sistema de Pre-Producción Electroacústica, Eléctrica SEC y Logística (DISTORSIONCL SPA)")

        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.8)
        self.line(36, 32, 756, 32)

        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(36, 20, "Mauricio Vega Castillo · Sección C1 · Grupo G10  |  Caso de Estudio: DISTORSIONCL SPA")
        self.drawRightString(756, 20, f"Lámina {self._pageNumber} de {page_count}")

        self.restoreState()


def build_presentation_pdf():
    pdf_filename = "Presentacion_Proyecto_STAGE_PLAN_Profesor.pdf"

    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    title_cover_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=30,
        textColor=colors.HexColor('#09090B'),
        alignment=0
    )

    subtitle_cover_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#B91C1C'),
        alignment=0
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16.5,
        leading=20,
        textColor=colors.HexColor('#09090B'),
        spaceAfter=9
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.6,
        textColor=colors.HexColor('#1E293B')
    )

    bullet_style = ParagraphStyle(
        'SlideBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-10,
        spaceAfter=3
    )

    highlight_box_style = ParagraphStyle(
        'SlideHighlight',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.3,
        leading=13.0,
        textColor=colors.HexColor('#09090B')
    )

    story = []

    # LÁMINA 1: PORTADA
    story.append(Spacer(1, 20))
    badge_data = [[
        Paragraph("<font color='#DC2626'><b>PROYECTO INTEGRADO TIHV43  |  PRESENTACIÓN DE INGENIERÍA DE SOFTWARE</b></font>", styles['Normal'])
    ]]
    t_badge = Table(badge_data, colWidths=[480])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FECACA')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 12))

    story.append(Paragraph("STAGE PLAN (v4.0)", title_cover_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(
        "Plataforma Web de Pre-Producción Electroacústica, Plano CAD Blueprint, Rack de Potencias Pasivas, "
        "Cotización Operativa y Seguridad Eléctrica (SEC RIC 03 / RIC 10)",
        subtitle_cover_style
    ))
    story.append(Spacer(1, 14))

    meta_table_data = [[
        Paragraph(
            "<b>Institución:</b> INACAP Sede Maipú<br/>"
            "<b>Carrera:</b> Analista Programador | <b>Sección:</b> C1 | <b>Grupo:</b> G10<br/>"
            "<b>Autor:</b> Mauricio Vega Castillo | <b>Docente:</b> Manuel Rojas<br/>"
            "<b>Arquitectura:</b> Monorepo TypeScript (Vue 3.5 + Vue Router 4 + Express 4.21 + Prisma/SQLite)",
            body_style
        ),
        Paragraph(
            "<b>Cliente / Caso de Estudio:</b> Productora DISTORSIONCL SPA<br/>"
            "<b>Marco Normativo:</b> SEC Chile (RIC N° 03 / RIC N° 10), IEC 60268, D.S. N° 38 MMA y Ley N° 20.949<br/>"
            "<b>Calidad Verificada:</b> 81 de 81 Pruebas Unitarias Automatizadas en 11 Archivos Vitest (100% Pass)<br/>"
            "<b>Proyección U3:</b> Migración Prisma a PostgreSQL 16 (12 tablas + JSONB GIN) detrás de Nginx TLS 1.3",
            body_style
        ),
    ]]
    t_meta = Table(meta_table_data, colWidths=[355, 365])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # LÁMINA 2: DIAGNÓSTICO DEL PROBLEMA EN TERRENO
    story.append(Paragraph("1. Diagnóstico del Negocio y Problemática Física en Terreno", slide_title_style))

    col1 = [
        Paragraph("<b>El Problema: Dimensionamiento Empírico sin Cálculo Normativo</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("En eventos electrónicos y de DJ en salones y parcelas, las fallas recurrentes generan riesgos operativos:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>Colapso de Enchufes y Generadores:</b> Circuitos domésticos de 10A (1.760W continuos seguros) o generadores comerciales de 3.500W pico (~2.142W útiles AVR) se apagan en los golpes de graves.", bullet_style),
        Paragraph("• <b>Saturación y Compresión Térmica:</b> Cajas mal distribuidas y niveles de mixer en rojo (+10 dB) producen onda cuadrada y pérdida térmica de -3.2 dB.", bullet_style),
        Paragraph("• <b>Etapas Pasivas en Modo PROTECT:</b> Cajas pasivas en paralelo bajo 3.2 Ohms o amplificadores subdimensionados activan corte térmico.", bullet_style),
        Paragraph("• <b>Caídas de Tensión y Tropiezos:</b> Alargadores de 1.5 mm² a 35m pierden voltaje y el cableado sin postes guía sufre fatiga mecánica.", bullet_style),
    ]

    col2 = [
        Paragraph("<b>La Solución Determinista: STAGE PLAN (v4.0)</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("Un motor isomórfico que transforma datos del recinto en decisiones de ingeniería:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>Constructor Multilote + Rack de Potencias Pasivas:</b> Calcula impedancia de carga (4 / 8 Ohms), headroom 1.6x RMS, modelos comerciales y carga AC 220V integrada a SEC.", bullet_style),
        Paragraph("• <b>División en Líneas L1/L2/L3:</b> Separa subwoofers, tops/cabina e iluminación DMX evitando caídas de tensión en mezcladores.", bullet_style),
        Paragraph("• <b>Plano 2D Blueprint por 5 Capas + Vista Completa:</b> Edición limpia sin ruido visual en /plano-2d y mapa consolidado ALL en /reporte.", bullet_style),
        Paragraph("• <b>Cotizador Arriendo CLP, PNG 300 DPI y PDF Dual-Page:</b> Presupuesto diario en CLP, imagen para WhatsApp y memoria PDF offline (2 páginas).", bullet_style),
    ]

    t_p2 = Table([[col1, col2]], colWidths=[355, 355])
    t_p2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#FECACA')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#F0FDF4')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#BBF7D0')),
    ]))
    story.append(t_p2)
    story.append(PageBreak())

    # LÁMINA 3: INTELIGENCIA ACÚSTICA 2D Y ESTRUCTURA DE GANANCIA DJM
    story.append(Paragraph("2. Distribución Acústica Anti-Saturación y Calibración de Mixer DJM", slide_title_style))

    gain_data = [
        [
            Paragraph("<b>SECCIÓN / ZONA</b>", highlight_box_style),
            Paragraph("<b>PARÁMETRO ÓPTIMO</b>", highlight_box_style),
            Paragraph("<b>INDICADOR VISUAL</b>", highlight_box_style),
            Paragraph("<b>JUSTIFICACIÓN FÍSICA Y ELECTROACÚSTICA</b>", highlight_box_style)
        ],
        [
            Paragraph("<b>PA Frontal (Cajas A, B)</b>", body_style),
            Paragraph("Perilla 12:00 (0 dB Unity) + HPF 85 Hz", body_style),
            Paragraph("En trípode a 2.2m (Splay 12°-20°)", body_style),
            Paragraph("Cubre la primera zona sin forzar amplificadores. El corte HPF a 85 Hz libera headroom eléctrico y evita cancelación con los subwoofers.", body_style)
        ],
        [
            Paragraph("<b>Torres Delay (C, D, E, F)</b>", body_style),
            Paragraph("Al 52% y 76% del fondo + Retardo Haas", body_style),
            Paragraph("Verde Esmeralda en Plano 2D", body_style),
            Paragraph("Rellena el fondo sin aturdir la 1° fila. Aplica t_vuelo + 3.0 ms (Efecto Haas) manteniendo la localización sonora frontal.", body_style)
        ],
        [
            Paragraph("<b>Subwoofers (S1, S2...)</b>", body_style),
            Paragraph("Mono Cluster Central (< 1.7m entre conos)", body_style),
            Paragraph("Juntos al centro en piso (sin pole mount)", body_style),
            Paragraph("Suma coherente (+6 dB) más ganancia de piso. Elimina cancelaciones en el centro de la pista.", body_style)
        ],
        [
            Paragraph("<b>Canal Mixer (Trim) y Fader</b>", body_style),
            Paragraph("Trim: +3 a +6 dB | Fader: Tope en 10", body_style),
            Paragraph("Verde + 1 a 2 LEDs Ámbar (Cero Rojo)", body_style),
            Paragraph("Maximiza relación señal/ruido. En mezcla de 2 canales: <b>Low EQ Kill (1 solo bajo a la vez)</b>.", body_style)
        ],
        [
            Paragraph("<b>Master Mixer (XLR Out)</b>", body_style),
            Paragraph("0 dB a +3 dB (+4 a +7 dBu nominales)", body_style),
            Paragraph("Verde completo + 1er LED Ámbar", body_style),
            Paragraph("Entrega señal limpia balanceada. Superar rojo (+10 dB) satura conversores y recorta transientes.", body_style)
        ]
    ]

    t_gain = Table(gain_data, colWidths=[125, 145, 135, 315])
    t_gain.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_gain)
    story.append(PageBreak())

    # LÁMINA 4: SUMINISTRO ELÉCTRICO REAL Y CONSUMO DINÁMICO
    story.append(Paragraph("3. Modelado Eléctrico: Enchufe Domiciliario vs. Generador Comercial (3500W)", slide_title_style))

    elec_cards = [
        [
            Paragraph("<b>CONSUMO DINÁMICO DE AUDIO</b>", highlight_box_style),
            Paragraph("<b>RED DOMICILIARIA (10A / 16A)</b>", highlight_box_style),
            Paragraph("<b>GENERADOR COMERCIAL (3500 W)</b>", highlight_box_style),
        ],
        [
            Paragraph("• Consumo proporcional al cuadrado del voltaje (<b>P = V²/Z</b>).<br/>"
                      "• <b>En reposo:</b> ~25 W (0.1 A).<br/>"
                      "• <b>Régimen Club (1/5 RMS) vs Máximo Techno (1/3 RMS).</b><br/>"
                      "• El subwoofer demanda entre el <b>60% y 70%</b> de la energía total.<br/>"
                      "• Etapas pasivas suman consumo AC 220V calculado automáticamente.", body_style),
            Paragraph("• <b>Circuito 10 A (220V):</b> 2.200 W nominales -> <b>1.760 W continuos seguros (80%)</b>.<br/>"
                      "• <b>Circuito 16 A (220V):</b> 3.520 W nominales -> <b>2.816 W continuos seguros (80%)</b>.<br/>"
                      "• Los automáticos toleran picos transitorios breves pero disparan si la demanda continua supera el 80%.", body_style),
            Paragraph("• 3500 W comerciales indican arranque pico (<i>Surge</i>); potencia continua (<i>Running</i>) ~85% (<b>2.975 W</b>).<br/>"
                      "• Se aplica factor de seguridad <b>72% AVR = 2.142 W seguros</b>.<br/>"
                      "• Superar este margen desestabiliza el AVR bajo 195V y apaga amplificadores.", body_style),
        ]
    ]
    t_elec = Table(elec_cards, colWidths=[240, 240, 240])
    t_elec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#09090B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_elec)
    story.append(Spacer(1, 8))

    matrix_data = [
        [
            Paragraph("<b>Configuración de Equipos (Régimen Máximo 1/3 RMS)</b>", highlight_box_style),
            Paragraph("<b>Demanda Total c/ Cabina</b>", highlight_box_style),
            Paragraph("<b>Enchufe 10 A (1.760W)</b>", highlight_box_style),
            Paragraph("<b>Enchufe 16 A (2.816W)</b>", highlight_box_style),
            Paragraph("<b>Generador 3500W (2.142W)</b>", highlight_box_style),
        ],
        [
            Paragraph("2 Tops 1000W + 1 Sub 1000W (3000W RMS)", body_style),
            Paragraph("<b>~1.700 W continuos</b>", body_style),
            Paragraph("<font color='#D97706'><b>AL LÍMITE (96%)</b></font>", body_style),
            Paragraph("<font color='#16A34A'><b>SEGURO (60%)</b></font>", body_style),
            Paragraph("<font color='#16A34A'><b>SEGURO (79%)</b></font>", body_style),
        ],
        [
            Paragraph("2 Tops 1000W + 2 Subs 1000W (4000W RMS)", body_style),
            Paragraph("<b>~2.065 W continuos</b>", body_style),
            Paragraph("<font color='#DC2626'><b>DISPARA DISYUNTOR (117%)</b></font>", body_style),
            Paragraph("<font color='#16A34A'><b>SEGURO (73%)</b></font>", body_style),
            Paragraph("<font color='#D97706'><b>RIESGO AVR (96%)</b></font>", body_style),
        ],
        [
            Paragraph("4 Tops 1000W + 2 Subs 1500W (7000W RMS)", body_style),
            Paragraph("<b>~3.165 W continuos</b>", body_style),
            Paragraph("<font color='#DC2626'><b>INVIABLE</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>INVIABLE</b></font>", body_style),
            Paragraph("<font color='#DC2626'><b>COLAPSA (Exige >= 6 kVA)</b></font>", body_style),
        ]
    ]
    t_matrix = Table(matrix_data, colWidths=[210, 125, 125, 130, 130])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_matrix)
    story.append(PageBreak())

    # LÁMINA 5: LAS 5 REGLAS CRÍTICAS DE TERRENO
    story.append(Paragraph("4. Auditoría Automática de las 5 Reglas Críticas de Terreno", slide_title_style))

    field_data = [
        [
            Paragraph("<b>REGLA DE INGENIERÍA</b>", highlight_box_style),
            Paragraph("<b>FENÓMENO FÍSICO QUE PREVIENE</b>", highlight_box_style),
            Paragraph("<b>DIRECTRIZ AUTOMÁTICA DE STAGE PLAN</b>", highlight_box_style),
        ],
        [
            Paragraph("<b>1. Crossover HPF en Tops (80-90 Hz)</b>", body_style),
            Paragraph("En rango completo, los tops desperdician ~40% de energía reproduciendo subgraves y cancelan al subwoofer.", body_style),
            Paragraph("Exige filtro <b>HPF a 85 Hz</b> en cajas superiores dejando los 30-85 Hz al clúster central.", body_style),
        ],
        [
            Paragraph("<b>2. Ángulo de Apertura (Splay Angle)</b>", body_style),
            Paragraph("Cajas apuntadas en paralelo interfieren en el centro creando filtro de peine (<i>comb filtering</i>).", body_style),
            Paragraph("Calcula rotación óptima (<b>10° a 25° por lado</b>) cruzando bordes de cobertura sin interferencia.", body_style),
        ],
        [
            Paragraph("<b>3. Alineación de Fase y Postes RIC 10</b>", body_style),
            Paragraph("Retardo de grupo entre sub y top, y fractura de cobre por curvas vivas de 90° en esquinas.", body_style),
            Paragraph("Sugiere micro-retardo frontal y exige <b>Postes Guía esquineros (R >= 6d)</b> según SEC RIC N° 10.", body_style),
        ],
        [
            Paragraph("<b>4. Caída de Tensión en el Drop (ΔV <= 3%)</b>", body_style),
            Paragraph("Alargadores de 1.5 mm² a 35m sufren caídas severas de voltaje bajo carga de graves.", body_style),
            Paragraph("Asigna sección mínima <b>2.5 mm² o 4.0 mm²</b> y exige desenrollar el 100% del carrete.", body_style),
        ],
        [
            Paragraph("<b>5. Tierra Copperweld y Compresión Térmica</b>", body_style),
            Paragraph("Tierra flotante en generadores induce zumbido de 50 Hz y riesgo de descarga eléctrica.", body_style),
            Paragraph("Exige barra de puesta a tierra Copperweld y reporta pérdida de <b>-3.2 dB</b> por calentamiento de bobina.", body_style),
        ]
    ]

    t_field = Table(field_data, colWidths=[165, 265, 290])
    t_field.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_field)
    story.append(PageBreak())

    # LÁMINA 6: ARQUITECTURA, COCKPIT 100% ZOOM Y SEGURIDAD
    story.append(Paragraph("5. Arquitectura Monorepo, Studio Cockpit (100% Zoom) y Seguridad", slide_title_style))

    arch_col1 = [
        Paragraph("<b>Studio Cockpit Fullscreen y Blueprint 2D</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("Diseñado para operar sin scroll global al 100% de zoom en laptops y tablets:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>5 Rutas Modulares (Vue Router 4):</b> /auth, /recinto, /equipos, /plano-2d y /reporte con persistencia automática en localStorage.", bullet_style),
        Paragraph("• <b>Contraste WCAG 2.1 AA:</b> Dark Mode FOH (#080a10) que evita encandilamiento nocturno en cabina.", bullet_style),
        Paragraph("• <b>5 Capas Exclusivas Blueprint:</b> Arquitectura limpia al editar; Vista Completa (ALL) consolidada en /reporte.", bullet_style),
        Paragraph("• <b>Salida Terreno Autónoma:</b> PNG 300 DPI + PDF Dual-Page (Pág. 1 Memoria/Costos + Pág. 2 Lámina CAD) generados offline en cliente.", bullet_style),
    ]

    arch_col2 = [
        Paragraph("<b>Arquitectura Técnica, BD Híbrida y Seguridad OWASP</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("Separación en 3 paquetes TypeScript verificados con vue-tsc y tsc:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>@stageplan/shared:</b> 11 módulos físicos puros + Zod isomórfico + 81 pruebas unitarias en Vitest.", bullet_style),
        Paragraph("• <b>@stageplan/backend:</b> Express 4.21 + Helmet + RateLimit (10/15m login) + bcrypt (12 rondas) + bloqueo temporal HTTP 423 (5 fallos) + errorHandler.", bullet_style),
        Paragraph("• <b>Anti-IDOR (A01):</b> Consultas filtradas por ownerId === req.user.id en Prisma retornando HTTP 404 para impedir enumeración.", bullet_style),
        Paragraph("• <b>Persistencia Híbrida:</b> SQLite 3 (dev.db, 4 tablas 3FN en español + JSON) en PoC; migración a PostgreSQL 16 (12 tablas + JSONB GIN) en Unidad 3.", bullet_style),
    ]

    t_arch2 = Table([[arch_col1, arch_col2]], colWidths=[355, 355])
    t_arch2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (0,0), 1, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#EFF6FF')),
        ('BOX', (1,0), (1,0), 1, colors.HexColor('#BFDBFE')),
    ]))
    story.append(t_arch2)
    story.append(PageBreak())

    # LÁMINA 7: VALIDACIÓN TDD (81 TESTS EN 11 SUITES) Y CONCLUSIONES
    story.append(Paragraph("6. Calidad de Software Verificada (81/81 Vitest TDD) y Conclusiones", slide_title_style))

    metrics_data = [
        [
            Paragraph("<b>SUITES DE PRUEBAS AUTOMATIZADAS (@stageplan/shared)</b>", highlight_box_style),
            Paragraph("<b>CASOS VERIFICADOS</b>", highlight_box_style),
            Paragraph("<b>RESULTADO VITEST</b>", highlight_box_style),
            Paragraph("<b>ESTADO</b>", highlight_box_style),
        ],
        [
            Paragraph("<b>calc-engine.spec.ts</b> (SEC RIC 03/10, Impedancia, Multilote RMS/Peak y 2 Líneas)", body_style),
            Paragraph("23 tests unitarios", body_style),
            Paragraph("<b>23 / 23 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>routing-and-gaffer.spec.ts & power-distribution.spec.ts</b> (Manhattan, Z1..Z4, Gaffer 50m)", body_style),
            Paragraph("18 tests (10 + 8)", body_style),
            Paragraph("<b>18 / 18 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>hybrid-roster.spec.ts & cabling.spec.ts</b> (Rigging, Rack Pasivo PA-01..06, XLR/Speakon)", body_style),
            Paragraph("10 tests (8 + 2)", body_style),
            Paragraph("<b>10 / 10 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>lighting-dmx.spec.ts & dj-setup-audio.spec.ts</b> (Luminarias x1, DMX512 y Booth DJ)", body_style),
            Paragraph("12 tests (8 + 4)", body_style),
            Paragraph("<b>12 / 12 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>stage-acoustic-* & contingency-logistics & qa-gap-branches</b> (SPL, Haas, RT60, Ley del Saco)", body_style),
            Paragraph("18 tests (5+2+6+5)", body_style),
            Paragraph("<b>18 / 18 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>TOTAL SUITE DE INGENIERÍA STAGE PLAN (0,0286 ms/cálculo)</b>", highlight_box_style),
            Paragraph("<b>11 archivos .spec.ts</b>", highlight_box_style),
            Paragraph("<b>81 de 81 aprobados</b>", highlight_box_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", highlight_box_style),
        ],
    ]
    t_metrics = Table(metrics_data, colWidths=[315, 125, 145, 135])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F0FDF4')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 8))

    sec_summary = [[
        Paragraph(
            "<b>Valor Académico y Rigor Técnico:</b><br/>"
            "Stage Plan integra modelado acústico, electrotecnia normativa SEC, diseño Cockpit 100% zoom, "
            "seguridad API OWASP y validación continua mediante 81 pruebas unitarias TDD en Vitest.",
            body_style
        ),
        Paragraph(
            "<b>Impacto Operacional en DISTORSIONCL SPA:</b><br/>"
            "Previene disparos eléctricos y daño de etapas pasivas, estima costos diarios de arriendo CLP y "
            "entrega un PDF Dual-Page completo con el plano CAD para montaje autónomo en terreno.",
            body_style
        )
    ]]
    t_sec = Table(sec_summary, colWidths=[355, 355])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec)

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF de presentacion actualizado exitosamente:", pdf_filename)


if __name__ == '__main__':
    build_presentation_pdf()
