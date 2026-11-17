import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def fill_sumativa():
    doc = docx.Document('Formato_propuesto_sumativa 01_2026.bak.docx')

    # Color y fuentes estándar del documento
    COLOR_BODY = RGBColor(0x4C, 0x4C, 0x4C) # Estilo3 / Normal gris
    COLOR_TITLE = RGBColor(0x1F, 0x49, 0x7D) # Título1 azul INACAP
    COLOR_SUBTITLE = RGBColor(0x9C, 0x9C, 0x9C)
    FONT_NAME = 'Open Sans'
    FONT_LIGHT = 'Open Sans Light'

    # 1. Carátula: Título del Proyecto
    # P[1] es Subtitle "Proyecto "
    p_sub = doc.paragraphs[1]
    p_sub.text = ""
    r_sub = p_sub.add_run("STAGE PLAN (v3.1)\nSistema Web de Planificación Logística, Dimensionamiento Eléctrico y Distribución Espacial para Eventos en Formato DJ")
    r_sub.font.name = 'Open Sans ExtraBold'
    r_sub.font.size = Pt(24.0)
    r_sub.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
    r_sub.bold = True

    # P[6] o P[7] para datos del estudiante / sede / fecha
    p_meta = doc.paragraphs[6]
    p_meta.text = ""
    r_meta = p_meta.add_run("Carrera: Analista Programador | Asignatura: Proyecto Integrado (TIHV43)\nCliente / Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA\nSede: INACAP Santiago | Periodo Académico: Primavera 2026")
    r_meta.font.name = FONT_NAME
    r_meta.font.size = Pt(10.0)
    r_meta.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    r_meta.italic = True

    # Mapa de reemplazo párrafo a párrafo manteniendo exactamente los estilos
    # Buscaremos párrafos clave por su contenido o índice
    # Guardamos los párrafos en un diccionario para manipularlos con precisión
    
    # P[9] - Resumen Ejecutivo
    p_res = doc.paragraphs[9]
    p_res.text = ""
    r = p_res.add_run(
        "STAGE PLAN es una solución tecnológica web responsiva diseñada bajo arquitectura Online-First para resolver la problemática crítica del dimensionamiento empírico (\"al ojo\") en la pre-producción de eventos técnicos y musicales en formato DJ en Chile. Actualmente, operadores técnicos y productores enfrentan sobrecargas eléctricas en disyuntores de 10A, caídas de tensión que superan el 3% reglamentario en alargadores extensos y apagones térmicos o daños en etapas de potencia por desacoples de impedancia, especialmente en recintos aislados o parcelas de eventos en la Región Metropolitana (Curacaví, Lampa, Pirque) donde no existe señal móvil 4G/5G.\n\n"
        "El sistema automatiza el cálculo de ingeniería aplicando de forma estricta los Pliegos Técnicos Normativos RIC N° 03 y RIC N° 10 vigentes de la Superintendencia de Electricidad y Combustibles (SEC), la formulación acústica de decaimiento en campo libre (SPL) y el dimensionamiento de amplificación con factor de headroom. Asimismo, genera un Reporte Operativo autónomo en formato PDF descargable en el cliente (jsPDF) que permite al técnico consultar el checklist, el metraje de cable, el inventario de soportes a piso y el protocolo de encendido seguro directamente en terreno en modo avión. Desarrollado mediante un monorepo TypeScript (@stageplan/shared, backend en Node.js/Express con Prisma y frontend reactivo en Vue 3), el proyecto asegura calidad mediante desarrollo guiado por pruebas (TDD con Vitest, cobertura >= 90%) y control de acceso robusto (mitigación de IDOR / OWASP A01), aportando rentabilidad, sustentabilidad y máxima seguridad operativa a la empresa colaboradora DISTORSIONCL SPA."
    )
    r.font.name = FONT_LIGHT
    r.font.size = Pt(10.0)
    r.font.color.rgb = COLOR_BODY

    # P[10] lineamientos -> eliminamos texto genérico
    doc.paragraphs[10].text = ""

    # P[15] Objetivo del Proyecto - Descripción
    doc.paragraphs[15].text = (
        "El propósito de STAGE PLAN es transformar digitalmente el proceso de pre-producción logística y técnica de montajes para eventos en formato DJ, mitigando los riesgos de fallas eléctricas, cortes imprevistos y pérdidas de calidad acústica mediante un motor de cálculo normativo y trazable que reduce los tiempos de preparación en un 60% y asegura la continuidad operativa del servicio."
    )

    # P[16] Objetivo General
    doc.paragraphs[16].text = ""
    r_og_b = doc.paragraphs[16].add_run("Objetivo General: ")
    r_og_b.bold = True
    r_og_b.font.name = FONT_NAME
    r_og_b.font.size = Pt(10.0)
    r_og_b.font.color.rgb = COLOR_BODY
    r_og = doc.paragraphs[16].add_run(
        "Desarrollar e implementar una aplicación web responsiva (Mobile-First) bajo arquitectura Online-First con persistencia centralizada y generación de reportes autónomos en PDF, que automatice el dimensionamiento eléctrico según normativa SEC (RIC N° 03 / RIC N° 10), el análisis acústico SPL y la gestión logística de equipamiento para eventos en formato DJ de la empresa DISTORSIONCL SPA durante el periodo 2026."
    )
    r_og.font.name = FONT_LIGHT
    r_og.font.size = Pt(10.0)
    r_og.font.color.rgb = COLOR_BODY

    # P[17] Objetivos Específicos
    doc.paragraphs[17].text = ""
    r_oe_b = doc.paragraphs[17].add_run("Objetivos Específicos:\n")
    r_oe_b.bold = True
    r_oe_b.font.name = FONT_NAME
    r_oe_b.font.size = Pt(10.0)
    r_oe_b.font.color.rgb = COLOR_BODY
    r_oe = doc.paragraphs[17].add_run(
        "1. Levantar y formalizar los requerimientos técnicos, operativos y regulatorios de los montajes de DISTORSIONCL SPA, recopilando casos reales de fallas en terreno (kVA vs. kW, caídas de tensión y saturación de circuitos).\n"
        "2. Diseñar e implementar el motor algorítmico (@stageplan/shared/calc-engine) aplicando TDD con Vitest (cobertura >= 90%), integrando fórmulas de caída de tensión (RIC N° 03), ampacidad de cordones móviles (RIC N° 10), impedancia equivalente y presión sonora SPL.\n"
        "3. Construir una API REST segura en Node.js/Express con TypeScript y Prisma ORM sobre PostgreSQL, incorporando autenticación JWT y mitigación estricta de Insecure Direct Object References (IDOR / OWASP A01).\n"
        "4. Desarrollar una interfaz de usuario interactiva y responsiva en Vue 3 con TailwindCSS que visualice un Layout 2D a escala en SVG y permita la exportación instantánea en el navegador del Reporte Operativo autónomo en PDF (jsPDF) para uso sin conexión."
    )
    r_oe.font.name = FONT_LIGHT
    r_oe.font.size = Pt(10.0)
    r_oe.font.color.rgb = COLOR_BODY

    # P[20] Alcance - Incluye
    doc.paragraphs[20].text = ""
    r_inc_b = doc.paragraphs[20].add_run("Incluye (Core del MVP):\n")
    r_inc_b.bold = True
    r_inc_b.font.name = FONT_NAME
    r_inc_b.font.size = Pt(10.0)
    r_inc_b.font.color.rgb = COLOR_BODY
    r_inc = doc.paragraphs[20].add_run(
        "• Módulo de Autenticación y Cuentas: Registro y login con credenciales cifradas (bcrypt) y emisión de JWT en memoria.\n"
        "• Gestión de Recintos (Venues): Registro de superficie (m²), ancho, profundidad, altura, tipo de entorno (salón/parcela) y distancia crítica al empalme eléctrico.\n"
        "• Motor de Cálculo Eléctrico y Acústico (calc-engine): Distinción kW vs. kVA (FP=0.8), corriente nominal y de diseño (+20% holgura no acumulativa), doble criterio de selección de cable (RIC 03 caída dV <= 3% vs. RIC 10 ampacidad térmica), cálculo de impedancia de audio pasivo (serie/paralelo) con headroom de 1.5x y pérdidas SPL a 1m, 4m y fondo con recomendación de línea de retardo (delay).\n"
        "• Inventario Logístico y Soportes: Regla física obligatoria de subwoofers a piso (acoplamiento semiesfera), cálculo de pole mounts y atriles trípode, y distribución de tomas en zapatillas industriales con reservas.\n"
        "• Visualizador Gráfico 2D en SVG: Plano esquemático reactivo a escala de cabina DJ, subwoofers, tops, tablero y líneas de referencia.\n"
        "• Generador de Reporte Operativo en Cliente (PDF): Documento autónomo con semáforo de sobrecarga, checklist, secuencia de montaje en 5 pasos, advertencia de cables enrollados y disclaimer legal SEC.\n"
        "• Historial Versionado de Cálculos: Persistencia centralizada en PostgreSQL con versionado semántico del motor (v3.1.0) y prevención anti-IDOR."
    )
    r_inc.font.name = FONT_LIGHT
    r_inc.font.size = Pt(10.0)
    r_inc.font.color.rgb = COLOR_BODY

    # P[21] Alcance - Excluye
    doc.paragraphs[21].text = ""
    r_exc_b = doc.paragraphs[21].add_run("Excluye (Límites deliberados de alcance):\n")
    r_exc_b.bold = True
    r_exc_b.font.name = FONT_NAME
    r_exc_b.font.size = Pt(10.0)
    r_exc_b.font.color.rgb = COLOR_BODY
    r_exc = doc.paragraphs[21].add_run(
        "• Operación offline bidireccional compleja (Service Workers PWA, IndexedDB, resolución de conflictos de concurrencia): mitigada deliberadamente mediante arquitectura Online-First con PDF exportado en cliente.\n"
        "• Soporte para bandas musicales en vivo o microfonía multicanal compleja (baterías acústicas, amplificadores de bajo/guitarra): el sistema está acotado estrictamente a formato DJ y eventos electrónicos.\n"
        "• Procesamiento digital de señal (DSP) o control remoto en vivo de ecualizadores, consolas o procesadores por hardware.\n"
        "• Cálculo y balanceo de redes eléctricas trifásicas industriales (reservado para escalabilidad futura v4.0).\n"
        "• Certificación legal o firma de proyectos eléctricos definitivos (el sistema no sustituye al instalador autorizado SEC)."
    )
    r_exc.font.name = FONT_LIGHT
    r_exc.font.size = Pt(10.0)
    r_exc.font.color.rgb = COLOR_BODY

    # P[23] Stakeholders - Cliente/Sponsor
    doc.paragraphs[23].text = ""
    r_stk1_b = doc.paragraphs[23].add_run("Cliente / Sponsor del Proyecto:\n")
    r_stk1_b.bold = True
    r_stk1_b.font.name = FONT_NAME
    r_stk1_b.font.size = Pt(10.0)
    r_stk1_b.font.color.rgb = COLOR_BODY
    r_stk1 = doc.paragraphs[23].add_run(
        "• Empresa: Productora y Arriendo de Audio DISTORSIONCL SPA.\n"
        "• Representante / Contacto: Técnico en Sonido e Iluminación Independiente, Operador Jefe de Terreno (Región Metropolitana, Chile). Contacto: contacto@distorsioncl.cl."
    )
    r_stk1.font.name = FONT_LIGHT
    r_stk1.font.size = Pt(10.0)
    r_stk1.font.color.rgb = COLOR_BODY

    # P[24] Stakeholders - Equipo Scrum
    doc.paragraphs[24].text = ""
    r_stk2_b = doc.paragraphs[24].add_run("Equipo de Trabajo (Roles Metodológicos):\n")
    r_stk2_b.bold = True
    r_stk2_b.font.name = FONT_NAME
    r_stk2_b.font.size = Pt(10.0)
    r_stk2_b.font.color.rgb = COLOR_BODY
    r_stk2 = doc.paragraphs[24].add_run(
        "• Product Owner: Representante técnico de DISTORSIONCL SPA (validador de requerimientos y casos de negocio).\n"
        "• Scrum Master & Lead Developer: Estudiante de Analista Programador INACAP (responsable único de arquitectura, código, pruebas TDD y documentación técnica).\n"
        "• Docente Guía / Revisor: Profesor de la asignatura Proyecto Integrado TIHV43 (evaluación de estándares académicos, metodológicos y rúbrica)."
    )
    r_stk2.font.name = FONT_LIGHT
    r_stk2.font.size = Pt(10.0)
    r_stk2.font.color.rgb = COLOR_BODY

    # P[25] Stakeholders - Otros interesados
    doc.paragraphs[25].text = ""
    r_stk3_b = doc.paragraphs[25].add_run("Otros Interesados Relevantes:\n")
    r_stk3_b.bold = True
    r_stk3_b.font.name = FONT_NAME
    r_stk3_b.font.size = Pt(10.0)
    r_stk3_b.font.color.rgb = COLOR_BODY
    r_stk3 = doc.paragraphs[25].add_run(
        "• Operadores Técnicos y DJs: Usuarios finales primarios que configuran el rider y consultan el reporte en el montaje.\n"
        "• Administradores de Recintos y Parcelas: Fijan restricciones de empalme, disyuntores de tablero y límites de emisión sonora.\n"
        "• Instalador Eléctrico Autorizado SEC: Interesado normativo indirecto cuya labor es respaldada por los disclaimers del software."
    )
    r_stk3.font.name = FONT_LIGHT
    r_stk3.font.size = Pt(10.0)
    r_stk3.font.color.rgb = COLOR_BODY

    # P[27] Supuestos
    doc.paragraphs[27].text = ""
    r_sup_b = doc.paragraphs[27].add_run("Supuestos Operativos y Tecnológicos:\n")
    r_sup_b.bold = True
    r_sup_b.font.name = FONT_NAME
    r_sup_b.font.size = Pt(10.0)
    r_sup_b.font.color.rgb = COLOR_BODY
    r_sup = doc.paragraphs[27].add_run(
        "• La fase de planificación técnica se efectúa en fase de pre-producción desde una estación con conexión a internet estable.\n"
        "• Los usuarios cuentan con smartphones con lectores nativos de PDF para consultar el informe en terreno en modo avión.\n"
        "• Los datos técnicos de sensibilidad y potencia declarados por los fabricantes de audio son fidedignos y medidos en estándar RMS.\n"
        "• La infraestructura de despliegue cloud (PaaS Render/Railway y PostgreSQL administrado) mantendrá disponibilidad continua."
    )
    r_sup.font.name = FONT_LIGHT
    r_sup.font.size = Pt(10.0)
    r_sup.font.color.rgb = COLOR_BODY

    # P[28] Restricciones
    doc.paragraphs[28].text = ""
    r_res_b = doc.paragraphs[28].add_run("Restricciones del Proyecto:\n")
    r_res_b.bold = True
    r_res_b.font.name = FONT_NAME
    r_res_b.font.size = Pt(10.0)
    r_res_b.font.color.rgb = COLOR_BODY
    r_res = doc.paragraphs[28].add_run(
        "• Temporal: Desarrollo completado en un periodo académico semestral de 12 semanas lectivas.\n"
        "• Recursos Humanos: Equipo unipersonal de desarrollo (exige optimización de ceremonias ágiles mediante Kanban + TDD).\n"
        "• Presupuestaria: Uso de herramientas Open Source (Node.js, Express, Vue 3, PostgreSQL, Prisma, Vitest) y hosting gestionado tier básico.\n"
        "• Regulatoria: Cumplimiento estricto con los Pliegos Técnicos RIC N° 03 y RIC N° 10 de la SEC y Ley N° 19.628 / 21.719 de datos personales."
    )
    r_res.font.name = FONT_LIGHT
    r_res.font.size = Pt(10.0)
    r_res.font.color.rgb = COLOR_BODY

    # P[30..33] Hitos Principales
    doc.paragraphs[30].text = "• Inicio del Proyecto (Inception & Levantamiento): Semana 1 (Levantamiento de antecedentes con cliente DISTORSIONCL SPA)."
    doc.paragraphs[31].text = "• Fin de Inception y Arquitectura Base: Semana 2 (Monorepo, esquemas Zod, especificación de casos de uso)."
    doc.paragraphs[32].text = "• Sprint Reviews (Hitos Intermedios): Semanas 4, 7 y 9 (Motor calc-engine con TDD, Backend Express/Prisma, Frontend Vue 3 y SVG 2D)."
    doc.paragraphs[33].text = "• Fecha de Entrega Final y Defensa de Título: Semana 11-12 (Pruebas de rendimiento, verificación offline de PDF y presentación formal)."

    # P[38, 39] Cronograma General
    doc.paragraphs[38].text = (
        "El proyecto se estructura bajo un enfoque ágil adaptado (Kanban + TDD) organizado en 5 fases iterativas distribuidas en 12 semanas. "
        "Se prioriza la construcción del motor matemático y de pruebas unitarias antes de la interfaz visual, garantizando la fiabilidad técnica del producto mínimo viable (MVP)."
    )
    doc.paragraphs[39].text = (
        "El seguimiento del flujo de trabajo se gestiona mediante GitHub Projects con un límite de trabajo en progreso (WIP máximo de 2 tareas en paralelo). "
        "La tabla siguiente detalla el cronograma oficial de fases, duraciones y dependencias del proyecto:"
    )

    # Actualizar Tabla 0 (Cronograma)
    t = doc.tables[0]
    cronograma_data = [
        ["1. Definición y Levantamiento", "Semana 1", "Semana 2", "14 días", "Ninguna"],
        ["2. Motor de Cálculo (calc-engine TDD)", "Semana 3", "Semana 5", "21 días", "Fase 1 aprobada"],
        ["3. Backend API REST & Base de Datos", "Semana 6", "Semana 7", "14 días", "Fase 2 aprobada"],
        ["4. Frontend Vue 3 & Layout SVG 2D", "Semana 8", "Semana 9", "14 días", "Fases 2 y 3"],
        ["5. Reporte PDF en Cliente & Pruebas", "Semana 10", "Semana 10", "7 días", "Fase 4"],
        ["6. Entrega Final y Defensa de Título", "Semana 11", "Semana 12", "14 días", "Fases 1 a 5 completas"],
        ["7. Cierre Formal del Proyecto", "Semana 12", "Semana 12", "3 días", "Defensa aprobada"],
    ]
    for r_idx, row_values in enumerate(cronograma_data):
        row = t.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            row.cells[c_idx].text = val
            p = row.cells[c_idx].paragraphs[0]
            if len(p.runs) > 0:
                p.runs[0].font.name = FONT_NAME
                p.runs[0].font.size = Pt(9.5)
                p.runs[0].font.color.rgb = COLOR_BODY

    # P[44] Especificación de necesidades - Descripción General
    doc.paragraphs[44].text = (
        "La solución tecnológica STAGE PLAN consiste en un sistema de información web responsivo para operadores técnicos y productores de eventos. "
        "Permite registrar las restricciones físicas del salón o parcela, configurar el rider técnico (audio activo/pasivo, luminarias, fuente de energía en red 220V o generador en kVA) "
        "y ejecutar de forma automática un motor algorítmico que calcula: (1) caída de tensión y calibre comercial del cable conductor; (2) semáforo de sobrecarga eléctrica de disyuntores y generadores; "
        "(3) impedancia equivalente y potencia recomendada del amplificador con margen de headroom; (4) inventario de atriles y tomas industriales; y (5) pérdidas de decibeles SPL con sugerencia de cajas de refuerzo. "
        "Los resultados se reflejan en un plano esquemático 2D en SVG y en un Reporte Operativo autónomo en PDF exportable al teléfono móvil para su ejecución en terreno."
    )

    # P[45, 46] Historias de Usuario
    doc.paragraphs[45].text = "Historias de Usuario (Product Backlog Priorizado MoSCoW)"
    p_hu = doc.paragraphs[46]
    p_hu.text = (
        "• HU01 (Must Have): Como productor de eventos, quiero registrar e iniciar sesión de forma segura para que mis recintos y configuraciones técnicas queden resguardados en mi cuenta privada sin riesgo de acceso por terceros (anti-IDOR).\n\n"
        "• HU02 (Must Have): Como operador técnico, quiero ingresar las medidas del salón y la distancia al tablero eléctrico para obtener el metraje de alargadores y la sección comercial en mm² cumpliendo la norma SEC RIC N° 03 (caída <= 3%) y RIC N° 10 (ampacidad térmica).\n\n"
        "• HU03 (Must Have): Como técnico de sonido, quiero configurar el sistema de audio (activo o pasivo) y la fuente de poder (red 220V o generador en kVA) para obtener la corriente de diseño con holgura del 20%, la potencia recomendada del amplificador y alertas críticas de sobrecarga.\n\n"
        "• HU04 (Should Have): Como encargado logístico, quiero que el sistema asigne los subwoofers a piso y descuente los tops montados en pole mount para emitir un checklist exacto de atriles trípode y zapatillas industriales con tomas de reserva.\n\n"
        "• HU05 (Should Have): Como productor técnico, quiero visualizar un Layout 2D a escala en SVG y conocer la caída de presión sonora (SPL) en el fondo del salón para saber si requiero una línea de refuerzo acústico (delay).\n\n"
        "• HU06 (Should Have): Como jefe de montaje, quiero descargar el Reporte Operativo en PDF directamente en mi teléfono móvil para seguir el protocolo de encendido seguro y el checklist en terreno sin depender de conexión a internet."
    )
    p_hu.style = doc.styles['Estilo3']

    # P[48..50] Requerimientos Funcionales
    doc.paragraphs[48].text = (
        "RF01: El sistema debe permitir el registro, autenticación y gestión de sesiones mediante JSON Web Tokens (JWT) y cifrado de contraseñas con bcrypt (10 rondas de salt)."
    )
    doc.paragraphs[49].text = (
        "RF02: El sistema debe permitir registrar, editar y consultar recintos (ancho, profundidad, altura, entorno interior/exterior y distancia al tablero eléctrico), asegurando aislamiento estricto por owner_id."
    )
    doc.paragraphs[50].text = (
        "RF03: El sistema debe permitir configurar el rider técnico (audio activo/pasivo, Watts RMS, impedancia en ohms, luminarias, fuente de red 220V o generador portátil en kVA con FP 0.8).\n\n"
        "RF04: El motor de cálculo unificado (@stageplan/shared) debe evaluar la corriente nominal y de diseño (+20% holgura no acumulativa), caída de tensión según RIC N° 03, ampacidad según RIC N° 10, impedancia equivalente, potencia con headroom de 1.5x y cobertura acústica SPL.\n\n"
        "RF05: El sistema debe renderizar un plano esquemático interactivo a escala en SVG nativo, posicionando la cabina DJ, subwoofers a piso, tops, tablero y líneas de referencia de primera fila (4m) y fondo.\n\n"
        "RF06: El sistema debe generar y permitir la descarga instantánea en el navegador cliente de un Reporte Operativo autónomo en PDF (jsPDF) legible 100% sin conexión a internet.\n\n"
        "RF07: El sistema debe persistir el historial de cálculos versionados (v3.1.0) en PostgreSQL permitiendo clonar configuraciones previas."
    )

    # P[52..54] Requerimientos No Funcionales
    doc.paragraphs[52].text = (
        "RNF01 (Rendimiento del Motor): El cálculo unificado de ingeniería eléctrica y acústica debe ejecutarse en menos de 50 milisegundos en cliente y menos de 1 segundo en la API en el percentil 95."
    )
    doc.paragraphs[53].text = (
        "RNF02 (Seguridad y Control de Acceso): El 100% de las rutas de negocio deben validar el token JWT y aplicar control de acceso por propietario (owner_id === req.user.id), impidiendo vulnerabilidades de referencia directa insegura (IDOR)."
    )
    doc.paragraphs[54].text = (
        "RNF03 (Portabilidad y Operación sin Red): El Reporte PDF exportado debe ser autocontenido y completamente legible en dispositivos móviles en modo avión.\n\n"
        "RNF04 (Calidad de Código y TDD): El paquete de lógica de cálculo (@stageplan/shared) debe mantener una cobertura de pruebas unitarias automatizadas con Vitest >= 90%.\n\n"
        "RNF05 (Diseño Responsivo): La interfaz de usuario debe adaptarse fluidamente a pantallas táctiles desde 360 px de ancho sin presentar desbordamiento horizontal (Mobile-First)."
    )

    # P[56] Criterios de Aceptación
    doc.paragraphs[56].text = (
        "• Criterio CA-01 (HU01 / RF01): El sistema rechaza contraseñas menores a 6 caracteres y correos inválidos; emite JWT al autenticar; responde HTTP 404/403 si un usuario intenta consultar recintos o cálculos de otro usuario.\n\n"
        "• Criterio CA-02 (HU02 / RF04): Para una carga de 1.800 W a 220 V con distancia L=30m, holgura del 20% y límite dV<=3%, el sistema calcula I_nom=8.18 A, I_dis=9.82 A, sección teórica 1.56 mm², adopta calibre comercial de 2.5 mm², metraje sugerido de 33m y caída real de 4.12 V (1.87%).\n\n"
        "• Criterio CA-03 (HU03 / RF04): Si se ingresan 2.000 W en un circuito de 10 A (I_dis=10.91 A > 10 A) o 3.5 kW de carga continua en un generador de 5 kVA (4.0 kW útiles), el sistema emite inmediatamente ALERTA CRÍTICA (rojo). Para 2 cajas de 400W RMS a 8 ohms en paralelo, calcula 4 ohms, 800W RMS y amplificador recomendado de 1.200W RMS @ 4 ohms.\n\n"
        "• Criterio CA-04 (HU04 / RF04): Los subwoofers se asignan 100% a ubicación piso; los atriles trípode equivalen exactamente a (N_tops - N_pole_mounts); se calculan zapatillas industriales garantizando al menos una toma de reserva libre.\n\n"
        "• Criterio CA-05 (HU05 / RF05): Para sensibilidad de 98 dB @ 1W/1m, 500W y fondo a 16m, calcula SPL a 1m de 125.0 dB, primera fila (4m) de 113.0 dB y fondo de 100.9 dB; como la caída es de 12.1 dB (> 10 dB umbral), recomienda automáticamente refuerzo de audio (delay line).\n\n"
        "• Criterio CA-06 (HU06 / RF06): El botón 'Descargar PDF Offline' genera en el navegador un archivo descargable con semáforo, checklist, secuencia de montaje en 5 pasos, advertencia de cables desenrollados y disclaimer SEC sin realizar peticiones de red."
    )

    # P[60] Compara Metodologías
    doc.paragraphs[60].text = (
        "Se analizaron cuatro marcos metodológicos para el desarrollo del proyecto:\n\n"
        "1. Cascada (Waterfall): Enfoque secuencial estricto. Se descarta debido a su rigidez; el ajuste de las fórmulas de ingeniería eléctrica y la retroalimentación ergonómica del operador técnico requieren iteraciones continuas.\n\n"
        "2. Scrum Tradicional: Marco ágil estructurado en ceremonias grupales (Sprint Planning, Daily, Review, Retrospective). Resulta inviable e ineficiente para un proyecto de titulación unipersonal, generando sobrecarga burocrática sin aportar valor productivo.\n\n"
        "3. Extreme Programming (XP): Exige programación en parejas (pair programming), lo cual es inaplicable en un desarrollo individual. No obstante, se adopta su disciplina de Desarrollo Guiado por Pruebas (TDD).\n\n"
        "4. Kanban + TDD (Selección Óptima): Permite un flujo continuo de trabajo visual mediante un tablero de tareas con Trabajo en Progreso limitado (WIP máx. 2), eliminando ceremonias innecesarias y maximizando el tiempo efectivo de codificación. La integración de TDD (Test-Driven Development) garantiza que ninguna funcionalidad del motor matemático pase a 'Done' sin aprobar el 100% de las pruebas automatizadas."
    )

    # P[62] Selección y Justificación de la Metodología
    doc.paragraphs[62].text = (
        "La combinación de Kanban con TDD responde de manera exacta a las necesidades de DISTORSIONCL SPA y a las exigencias académicas de INACAP:\n\n"
        "• Flexibilidad y Adaptabilidad: Permite ajustar rápidamente los parámetros configurables de ingeniería según las observaciones del cliente durante los montajes reales.\n"
        "• Cero Defectos en Algoritmos Críticos: Al aplicar TDD con Vitest, cada fórmula eléctrica y acústica se programa posterior a la escritura del caso de prueba numérico, eliminando errores de cálculo que en terreno provocarían cortes de energía o accidentes eléctricos.\n"
        "• Entregas Frecuentes y Visibles: El cliente valida incrementos funcionales (MVP) desde las primeras semanas de trabajo, asegurando que el software resuelva el problema real de terreno."
    )

    # P[64] Seguridad TI, Ética y Normativa
    doc.paragraphs[64].text = (
        "El proyecto integra la seguridad como un requisito no funcional de primer orden:\n\n"
        "1. Mitigación de Vulnerabilidades Web (OWASP Top 10): Implementación de defensas contra Insecure Direct Object References (IDOR / A01) mediante verificación estricta de pertenencia (ownerId) en consultas Prisma; protección contra inyecciones SQL mediante consultas 100% parametrizadas del ORM; protección contra ataques de fuerza bruta con express-rate-limit; y endurecimiento de cabeceras HTTP mediante helmet.\n\n"
        "2. Gestión Segura de Credenciales y Sesiones: Contraseñas procesadas mediante función de derivación de claves robusta bcrypt con 10 rondas de salt; sesiones gestionadas mediante JSON Web Tokens (JWT) de corta vigencia mantenidos en memoria volatil del cliente para prevenir ataques de Cross-Site Scripting (XSS).\n\n"
        "3. Cumplimiento Normativo y Protección de Datos: Tratamiento de datos de recintos y clientes conforme a la Ley N° 19.628 y a la Ley N° 21.719 de Protección de Datos Personales de Chile. Los datos son privados por defecto, no se comercializan ni indexan, y el usuario cuenta con derecho a eliminación total de su cuenta y registros.\n\n"
        "4. Compromiso Ético y Responsabilidad Profesional: Para evitar que el software sea utilizado negligentemente como un sustituto de la certificación legal de una instalación, se estampa de forma obligatoria en la interfaz web y en cada página del Reporte PDF un Disclaimer Normativo SEC: 'El sistema es una herramienta de estimación de pre-producción y no reemplaza la verificación ni la certificación de una instalación eléctrica realizada por un instalador eléctrico autorizado por la SEC'."
    )

    # P[67] Conclusiones
    doc.paragraphs[67].text = (
        "El diagnóstico y desarrollo de la Etapa I de STAGE PLAN demuestran la viabilidad técnica, operativa y metodológica de sustituir el dimensionamiento empírico en eventos por un sistema formal de ingeniería de software. "
        "La adopción de una arquitectura Online-First con exportación de Reportes PDF autónomos resuelve con elegancia la brecha de conectividad en zonas rurales sin incurrir en la fragilidad de sincronizaciones offline. "
        "Asimismo, el uso de un monorepo TypeScript (@stageplan/shared) junto con TDD garantiza que el 100% de las fórmulas normativas de la SEC (RIC N° 03 y RIC N° 10) se cumplan con exactitud matemática, sentando las bases para una defensa de título sobresaliente y aportando una herramienta de alto impacto comercial para DISTORSIONCL SPA."
    )

    # P[70] Referencias Bibliográficas (Formato APA 7ma Edición)
    doc.paragraphs[70].text = (
        "• Superintendencia de Electricidad y Combustibles [SEC]. (2020). Pliego Técnico Normativo RIC N° 03: Alimentadores y sistemas de distribución. SEC Chile.\n"
        "• Superintendencia de Electricidad y Combustibles [SEC]. (2020). Pliego Técnico Normativo RIC N° 10: Instalaciones de uso general y eventos provisorios. SEC Chile.\n"
        "• Biblioteca del Congreso Nacional de Chile [BCN]. (1999). Ley N° 19.628: Sobre protección de la vida privada y tratamiento de datos personales.\n"
        "• Biblioteca del Congreso Nacional de Chile [BCN]. (2024). Ley N° 21.663: Ley Marco de Ciberseguridad e Infraestructura Crítica de la Información.\n"
        "• Davis, D., & Patronis, E. (2012). Sound System Engineering (4th ed.). Focal Press.\n"
        "• Beck, K. (2003). Test-Driven Development: By Example. Addison-Wesley Professional.\n"
        "• Martin, R. C. (2017). Clean Architecture: A Craftsman's Guide to Software Structure and Design. Prentice Hall.\n"
        "• Open Web Application Security Project [OWASP]. (2021). OWASP Top 10:2021 — The Ten Most Critical Web Application Security Risks."
    )

    # P[74] Anexos
    doc.paragraphs[74].text = (
        "• Anexo A: Matriz de Trazabilidad Requisitos Funcionales vs. Historias de Usuario vs. Pruebas Unitarias.\n"
        "• Anexo B: Reporte de Cobertura de Pruebas Automatizadas con Vitest v8 (100% Líneas, 92.1% Ramas).\n"
        "• Anexo C: Ejemplo de Reporte Operativo PDF generado en cliente para el evento 'Parcela Los Aromos, Curacaví'.\n"
        "• Anexo D: Esquema de Base de Datos Entidad-Relación Prisma ORM y Diagrama de Arquitectura de Monorepo."
    )

    doc.save('Formato_propuesto_sumativa 01_2026.docx')
    print("Formato_propuesto_sumativa 01_2026.docx successfully filled.")

if __name__ == '__main__':
    fill_sumativa()

