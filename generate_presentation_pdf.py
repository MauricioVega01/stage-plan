import shutil
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
        # Header bar (Hard Techno Industrial Dark + Red Accent)
        self.setFillColor(colors.HexColor('#09090B'))
        self.rect(0, 580, 792, 32, fill=1, stroke=0)
        
        self.setFillColor(colors.HexColor('#DC2626'))
        self.rect(0, 577, 792, 3, fill=1, stroke=0)

        self.setFont('Helvetica-Bold', 10)
        self.setFillColor(colors.white)
        self.drawString(36, 592, "STAGE PLAN (v4.0)  |  Proyecto Integrado TIHV43 — INACAP 2026")
        
        self.setFont('Helvetica', 9)
        self.setFillColor(colors.HexColor('#D4D4D8'))
        self.drawRightString(756, 592, "Sistema Experto Electroacústico, Temporal y Eléctrico (DISTORSIONCL SPA)")

        # Footer bar
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.8)
        self.line(36, 32, 756, 32)

        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#475569'))
        self.drawString(36, 20, "Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA  |  Carrera: Analista Programador")
        page_text = f"Lámina {self._pageNumber} de {page_count}"
        self.drawRightString(756, 20, page_text)

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

    # =========================================================================
    # LÁMINA 1: PORTADA
    # =========================================================================
    story.append(Spacer(1, 20))
    badge_data = [[
        Paragraph("<font color='#DC2626'><b>PROYECTO INTEGRADO TIHV43  |  DEFENSA DE INGENIERÍA DE SOFTWARE</b></font>", styles['Normal'])
    ]]
    t_badge = Table(badge_data, colWidths=[450])
    t_badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FECACA')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_badge)
    story.append(Spacer(1, 12))

    story.append(Paragraph("STAGE PLAN (v4.0)", title_cover_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Sistema Experto de Pre-Producción Electroacústica, Constructor Híbrido Multilote (RMS + Peak), División en 2 Líneas de Fuerza, Impedancia Speakon y Seguridad Eléctrica (SEC RIC 03 / RIC 10)", subtitle_cover_style))
    story.append(Spacer(1, 14))

    meta_table_data = [
        [
            Paragraph("<b>Institución:</b> INACAP Sede Santiago<br/><b>Carrera:</b> Analista Programador<br/><b>Asignatura:</b> Proyecto Integrado (TIHV43)<br/><b>Arquitectura:</b> Monorepo TypeScript (Vue 3 + Express + Prisma + Vitest)", body_style),
            Paragraph("<b>Cliente / Caso de Estudio:</b> Productora de Eventos DISTORSIONCL SPA<br/><b>Marco Normativo:</b> SEC Chile (RIC N° 03 / RIC N° 10), IEC 60268 y D.S. N° 38 MMA<br/><b>Calidad Verificada:</b> 44 de 44 Pruebas Unitarias Automatizadas (100% Pass)", body_style),
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[355, 365])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # =========================================================================
    # LÁMINA 2: DIAGNÓSTICO DEL PROBLEMA EN TERRENO
    # =========================================================================
    story.append(Paragraph("1. Diagnóstico del Negocio y Problemática Física en Terreno", slide_title_style))
    
    col1 = [
        Paragraph("<b>El Problema: Montajes 'Al Ojo' que Queman Equipos</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("En eventos electrónicos y fiestas de DJ en salones y parcelas, los errores físicos cuestan caro:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>Colapso de Enchufes y Generadores:</b> Conectan audio al máximo a un enchufe casero de 10A (máx 1.760W continuos) o a un generador comercial de '3.500W' (solo ~2.140W útiles para audio), apagando el sonido en pleno drop.", bullet_style),
        Paragraph("• <b>Sonido Saturado ('Chicharriento') y Compresión Térmica:</b> Amontonan todas las cajas adelante y llevan el mixer a rojo (+10 dB), calentando las bobinas a 200°C y perdiendo 3.2 dB reales.", bullet_style),
        Paragraph("• <b>'Pasillo de la Muerte' en Bajos:</b> Separan los subwoofers en L y R generando cancelaciones de fase en el centro de la pista.", bullet_style),
        Paragraph("• <b>Caídas de Voltaje y Riesgo de Tropiezos:</b> Usan alargadores delgados de 1.5 mm² a 35m (perdiendo >16V en el drop) y dejan cables sin cinta Gaffer.", bullet_style),
    ]

    col2 = [
        Paragraph("<b>La Solución Experta: STAGE PLAN (v4.0)</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("Un motor determinista que traduce datos simples del cliente en decisiones de ingeniería:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>Constructor Multilote Híbrido (RMS + Peak):</b> Combina cajas activas y pasivas desiguales (ej. 2 activas + 1 pasiva); el algoritmo <i>Asymmetric Rigging</i> ubica el par más potente al frente y cajas impares a delay con <i>Gain Matching</i>.", bullet_style),
        Paragraph("• <b>División en 2 Líneas de Fuerza:</b> Separa Línea 1 (Sub-bajos) y Línea 2 (Tops + DJ) para blindar el suministro y evitar caídas en generadores.", bullet_style),
        Paragraph("• <b>Asistente de Impedancia Speakon y Cuello de Botella:</b> Ley de Ohm en paralelo (alerta roja &lt; 3.2 &Omega; PROTECT) y auditoría de balance Top/Sub.", bullet_style),
        Paragraph("• <b>Plano 2D con Mapa de Calor SPL, D.S. N° 38, PDF y WhatsApp:</b> Zonas de confort auditivo, impacto vecinal, ficha técnica offline y copia en 1 clic.", bullet_style),
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

    # =========================================================================
    # LÁMINA 3: INTELIGENCIA ACÚSTICA 2D Y ESTRUCTURA DE GANANCIA DJM
    # =========================================================================
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
            Paragraph("En trípode a 2.2m (Ángulo Splay 12°-20°)", body_style),
            Paragraph("Cubre de 0 a 10m sin forzar amplificadores. El corte HPF a 85 Hz ahorra 40% de energía eléctrica y evita cancelación con el sub.", body_style)
        ],
        [
            Paragraph("<b>Torres Delay (C, D, E, F)</b>", body_style),
            Paragraph("Al 52% y 76% del fondo + Retardo Haas", body_style),
            Paragraph("Verde Esmeralda en Plano 2D", body_style),
            Paragraph("Rellena el fondo a 102-106 dBA sin aturdir la 1° fila. Aplica t_vuelo + 3.0 ms (Efecto Haas) para localizar el sonido en el DJ.", body_style)
        ],
        [
            Paragraph("<b>Subwoofers (S1, S2...)</b>", body_style),
            Paragraph("Mono Cluster Central (< 1.7m entre conos)", body_style),
            Paragraph("Juntos al centro en piso (Jamás L/R)", body_style),
            Paragraph("Suma coherente (+6 dB gratis) + rebote de piso (+6 dB outdoor / +9 dB indoor). Elimina el 'pasillo de la muerte'.", body_style)
        ],
        [
            Paragraph("<b>Canal Mixer (Trim) y Fader</b>", body_style),
            Paragraph("Trim: +3 a +6 dB | Fader: Tope en 10", body_style),
            Paragraph("Verde + 1 a 2 LEDs Ámbar (Cero Rojo)", body_style),
            Paragraph("Maximiza relación señal/ruido en el drop sin saturar el bus de suma interna. En mezcla de 2 canales: <b>Low EQ Kill (1 solo bajo a la vez)</b>.", body_style)
        ],
        [
            Paragraph("<b>Master Mixer (XLR Out)</b>", body_style),
            Paragraph("0 dB a +3 dB (+4 a +7 dBu nominales)", body_style),
            Paragraph("Verde completo + 1er LED Ámbar", body_style),
            Paragraph("Entrega 1.228V RMS limpios. Entrar a Rojo (+10 dB) activa el limitador D/A, aplasta el kick y genera onda cuadrada ('chicharreo').", body_style)
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

    # =========================================================================
    # LÁMINA 4: SUMINISTRO ELÉCTRICO REAL Y CONSUMO DINÁMICO NO LINEAL
    # =========================================================================
    story.append(Paragraph("3. Modelado Eléctrico: Enchufe de Casa vs. Generador Comercial (3500W)", slide_title_style))

    elec_cards = [
        [
            Paragraph("<b>CONSUMO DINÁMICO DE PARLANTES</b>", highlight_box_style),
            Paragraph("<b>ENCHUFE DOMICILIARIO (10A / 16A)</b>", highlight_box_style),
            Paragraph("<b>GENERADOR COMERCIAL (Ej: 3500 W)</b>", highlight_box_style),
        ],
        [
            Paragraph("• El consumo crece con el cuadrado del voltaje (<b>P = V²/Z</b>).<br/>"
                      "• <b>En silencio:</b> ~25 W (0.1 A).<br/>"
                      "• <b>Volumen moderado (1/8 RMS):</b> ~120 W.<br/>"
                      "• <b>Máximo Techno (1/3 RMS):</b> ~370-450 W continuos con picos de 1.000 W en el bombo.<br/>"
                      "• El subwoofer consume el <b>60%-70%</b> de toda la energía del evento.", body_style),
            Paragraph("• <b>Circuito 10 A (220V):</b> 2.200 W nominales -> <b>1.760 W continuos seguros (80%)</b>.<br/>"
                      "• <b>Circuito 16 A (220V):</b> 3.520 W nominales -> <b>2.816 W continuos seguros (80%)</b>.<br/>"
                      "• Los automáticos Curva C toleran picos cortos del bombo, pero saltan por temperatura si el promedio supera el 80%.", body_style),
            Paragraph("• '3500 Watts' indica arranque pico (<i>Surge</i>). Su potencia continua real (<i>Running</i>) es ~85% (<b>2.975 W</b>).<br/>"
                      "• Por los escalones de corriente del sub-bajo, se aplica factor del <b>72% AVR = 2.142 W seguros</b>.<br/>"
                      "• Si se supera ese umbral, el voltaje cae bajo 195V y las cajas se apagan por protección.", body_style),
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
            Paragraph("<b>Enchufe Casa 10 A (1.760W)</b>", highlight_box_style),
            Paragraph("<b>Enchufe Fuerza 16 A (2.816W)</b>", highlight_box_style),
            Paragraph("<b>Generador 3500 W (2.142W)</b>", highlight_box_style),
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
            Paragraph("<font color='#DC2626'><b>SALTA AUTOMÁTICO (117%)</b></font>", body_style),
            Paragraph("<font color='#16A34A'><b>SEGURO (73%)</b></font>", body_style),
            Paragraph("<font color='#D97706'><b>RIESGO AVR (96% -> -3dB)</b></font>", body_style),
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

    # =========================================================================
    # LÁMINA 5: LAS 5 REGLAS CRÍTICAS DE TERRENO
    # =========================================================================
    story.append(Paragraph("4. Auditoría Automática de las 5 Reglas Críticas de Terreno", slide_title_style))

    field_data = [
        [
            Paragraph("<b>REGLA DE INGENIERÍA</b>", highlight_box_style),
            Paragraph("<b>FENÓMENO FÍSICO QUE PREVIENE</b>", highlight_box_style),
            Paragraph("<b>DIRECTRIZ AUTOMÁTICA DE STAGE PLAN</b>", highlight_box_style),
        ],
        [
            Paragraph("<b>1. Crossover HPF en Tops (80-90 Hz)</b>", body_style),
            Paragraph("En rango completo, los tops gastan 40% de su energía intentando mover sub-graves y cancelan la onda del subwoofer.", body_style),
            Paragraph("Exige activar filtro <b>HPF a 85 Hz</b> en todas las cajas superiores para liberar headroom limpio y dejarle los 30-85 Hz al cluster de subwoofers.", body_style),
        ],
        [
            Paragraph("<b>2. Ángulo de Apertura (Splay Angle)</b>", body_style),
            Paragraph("Dos cajas apuntando rectas en paralelo chocan sus conos de 90°x60° al centro, creando filtro de peine (<i>comb filtering</i>).", body_style),
            Paragraph("Calcula según el ancho y fondo del salón el ángulo exacto de apertura (<b>10° a 25° por lado</b>) para cruzar los bordes de -6 dB sin interferencia.", body_style),
        ],
        [
            Paragraph("<b>3. Alineación de Fase Sub vs. Top</b>", body_style),
            Paragraph("El filtro interno del subwoofer introduce retardo de grupo (<i>group delay</i>), atrasando el golpe del bajo respecto al top.", body_style),
            Paragraph("Indica aplicar un micro-retardo de <b>+3.5 ms (2 a 5 ms)</b> a los tops frontales A y B en el DSP para que el bombo sume en fase y pegue en el pecho.", body_style),
        ],
        [
            Paragraph("<b>4. Caída de Tensión en el Drop (V_drop)</b>", body_style),
            Paragraph("Con un carrete doméstico de 1.5 mm² a 35m y picos de 20A en el drop, el voltaje cae <b>-16.6V</b> (< 204V), reiniciando las cajas.", body_style),
            Paragraph("Exige conductor de <b>2.5 mm²</b> (hasta 35m) o <b>4.0 mm²</b> (> 35m) y desenrollar el 100% del carrete para evitar efecto bobina.", body_style),
        ],
        [
            Paragraph("<b>5. Tierra Copperweld y Compresión Térmica</b>", body_style),
            Paragraph("Tierra flotante en generadores electrifica trípodes con el rocío e inyecta zumbido de 50 Hz (<i>Ground Hum</i>) en los cables XLR.", body_style),
            Paragraph("Exige clavar <b>barra de cobre (jabalina Copperweld)</b> al chasis del generador y alerta la pérdida de <b>-3.2 dB</b> por calentamiento de bobina (150-220°C).", body_style),
        ]
    ]

    t_field = Table(field_data, colWidths=[155, 265, 300])
    t_field.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_field)
    story.append(PageBreak())

    # =========================================================================
    # LÁMINA 6: ARQUITECTURA DE SOFTWARE, UX INDUSTRIAL Y CIBERSEGURIDAD
    # =========================================================================
    story.append(Paragraph("5. Arquitectura Monorepo, UX Accesible y Ciberseguridad", slide_title_style))

    arch_col1 = [
        Paragraph("<b>UX 'Hard Techno Industrial' para Baja Visión</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("Diseñado específicamente para operar en cabinas oscuras sin fatiga visual:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>Alto Contraste (WCAG AAA):</b> Paleta negro obsidiana (#050505), rojo industrial (#DC2626), blanco puro y amarillo de advertencia.", bullet_style),
        Paragraph("• <b>Campos Amplios y Vacíos al Inicio:</b> Inputs grandes (<i>py-3 px-4 text-base</i>) que obligan a ingresar medidas reales del evento sin valores prellenados engañosos.", bullet_style),
        Paragraph("• <b>Glosario Interactivo [i]:</b> Botones de ayuda al lado de cada métrica que explican conceptos complejos con ejemplos cotidianos.", bullet_style),
        Paragraph("• <b>Flujo de 2 Pasos:</b> Botón 'Confirmar y Validar Datos' que verifica todos los campos antes de desbloquear el 'Descargar PDF'.", bullet_style),
    ]

    arch_col2 = [
        Paragraph("<b>Arquitectura Técnica y Seguridad Anti-IDOR</b>", highlight_box_style),
        Spacer(1, 4),
        Paragraph("Separación estricta de responsabilidades en 3 paquetes TypeScript:", body_style),
        Spacer(1, 3),
        Paragraph("• <b>@stageplan/shared:</b> Motor acústico dual (Sabine RT60 + Hopkins-Stryker indoor y Ley Inverso del Cuadrado outdoor), ruteo híbrido y validador eléctrico.", bullet_style),
        Paragraph("• <b>@stageplan/frontend:</b> Vue 3 + Vite + TailwindCSS + jsPDF / AutoTable para generación instantánea de reportes en el navegador.", bullet_style),
        Paragraph("• <b>@stageplan/backend:</b> Node.js + Express + Prisma ORM (PostgreSQL) con validación por esquemas Zod y protección <b>Anti-IDOR</b> por <i>ownerId</i>.", bullet_style),
        Paragraph("• <b>Regla Estructural Estricta:</b> Cero uso de tubos <i>pole mount</i> sobre sub-bajos; cajas siempre en trípodes independientes y bajos en cluster a piso.", bullet_style),
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

    # =========================================================================
    # LÁMINA 7: VALIDACIÓN TDD (44 TESTS) Y CONCLUSIONES
    # =========================================================================
    story.append(Paragraph("6. Calidad de Software Demostrable (Vitest TDD) y Conclusiones", slide_title_style))

    metrics_data = [
        [
            Paragraph("<b>SUITE DE PRUEBAS AUTOMATIZADAS (@stageplan/shared)</b>", highlight_box_style),
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
            Paragraph("<b>routing-and-gaffer.spec.ts</b> (Multi-enchufe Manhattan y Cinta Gaffer 50m)", body_style),
            Paragraph("10 tests unitarios", body_style),
            Paragraph("<b>10 / 10 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>stage-acoustic-engine.spec.ts</b> (SPL, Haas, Generador 3500W, Top/Sub y D.S. 38 MMA)", body_style),
            Paragraph("5 tests unitarios", body_style),
            Paragraph("<b>5 / 5 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>stage-acoustic-indoor-outdoor.spec.ts</b> (Sabine RT60 y Hopkins-Stryker)", body_style),
            Paragraph("2 tests unitarios", body_style),
            Paragraph("<b>2 / 2 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>hybrid-roster.spec.ts & cabling.spec.ts</b> (Asymmetric Rigging, Gain Matching, Cables)", body_style),
            Paragraph("4 tests unitarios", body_style),
            Paragraph("<b>4 / 4 aprobados</b>", body_style),
            Paragraph("<font color='#16A34A'><b>100% PASS</b></font>", body_style),
        ],
        [
            Paragraph("<b>TOTAL SUITE DE INGENIERÍA STAGE PLAN</b>", highlight_box_style),
            Paragraph("<b>6 archivos de test</b>", highlight_box_style),
            Paragraph("<b>44 de 44 aprobados</b>", highlight_box_style),
            Paragraph("<font color='#16A34A'><b>CUMPLIDO</b></font>", highlight_box_style),
        ],
    ]
    t_metrics = Table(metrics_data, colWidths=[310, 125, 145, 140])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F0FDF4')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 8))

    sec_summary = [
        [
            Paragraph("<b>Valor Académico y Diferenciación:</b><br/>"
                      "Stage Plan supera el paradigma del CRUD tradicional al integrar modelado matemático acústico, psicoacústica temporal y validación eléctrica normativa en una arquitectura tipada y probada con 44 tests automatizados.", body_style),
            Paragraph("<b>Impacto Real para DISTORSIONCL SPA:</b><br/>"
                      "Elimina los cortes de energía en pleno evento, protege la vida útil de las cajas y sub-bajos evitando la compresión térmica y entrega un PDF listo para montar en terreno sin conexión a internet.", body_style)
        ]
    ]
    t_sec = Table(sec_summary, colWidths=[355, 355])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_sec)

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copyfile(pdf_filename, "Presentacion_Proyecto_STAGE PLAN_Profesor.pdf")
    print("PDF de presentacion actualizado exitosamente:", pdf_filename)

if __name__ == '__main__':
    build_presentation_pdf()
