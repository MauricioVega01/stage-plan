import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_sumativa_v32():
    doc = docx.Document('Formato_propuesto_sumativa 01_2026.bak.docx')

    COLOR_BODY = RGBColor(0x33, 0x33, 0x33)
    COLOR_TITLE = RGBColor(0x1F, 0x49, 0x7D)
    FONT_NAME = 'Open Sans'
    FONT_LIGHT = 'Open Sans Light'

    for s in doc.styles:
        if s.name in ['Estilo3', 'Título1', 'Normal']:
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    def set_p_text(p, text_runs):
        p.text = ""
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for t, bold, italic, color, size in text_runs:
            r = p.add_run(t)
            r.bold = bold
            r.italic = italic
            r.font.name = FONT_NAME if bold else FONT_LIGHT
            r.font.size = Pt(size)
            r.font.color.rgb = color

    # Carátula
    set_p_text(doc.paragraphs[1], [
        ("STAGE PLAN (v3.2)\n", True, False, COLOR_TITLE, 22.0),
        ("Sistema Web de Planificación Logística, Ruteo Inteligente de Enchufes, Cálculo de Cables y Cinta para Eventos DJ", False, False, COLOR_TITLE, 14.0)
    ])

    set_p_text(doc.paragraphs[6], [
        ("Carrera: Analista Programador | Asignatura: Proyecto Integrado (TIHV43)\n"
         "Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA\n"
         "Sede: INACAP Santiago | Periodo: Primavera 2026", False, True, RGBColor(0x66, 0x66, 0x66), 10.0)
    ])

    # P[8]
    doc.paragraphs[8].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # P[9] Resumen Ejecutivo v3.2
    set_p_text(doc.paragraphs[9], [
        ("¿Qué problema resuelve este proyecto?\n", True, False, COLOR_TITLE, 11.0),
        ("En los eventos y fiestas con DJ en Chile, casi todos los problemas de sonido y electricidad ocurren porque los técnicos calculan los cables y los enchufes 'al ojo' o por intuición. Por ejemplo: conectan todos los parlantes y las luces al primer enchufe que pillan cerca de la cabina, cruzan cables sueltos por el medio de la pista de baile donde la gente camina, o tiran un alargador largo y delgado de más de 30 metros.\n\n"
         "Esto provoca fallas graves en terreno:\n"
         "1. Se corta la luz a mitad de la fiesta porque el automático del enchufe no aguanta la carga.\n"
         "2. El voltaje baja tanto que los amplificadores de sonido se apagan o se queman.\n"
         "3. La gente se tropieza con cables sueltos en el piso, lo que puede botar un parlante o desconectar el sonido.\n"
         "4. En parcelas de eventos (Curacaví, Lampa, Pirque) no hay señal de celular (4G/5G), por lo que el técnico no puede consultar información en internet una vez que llega al lugar.\n\n", False, False, COLOR_BODY, 10.0),
        ("¿Cuál es la solución que entrega STAGE PLAN (v3.2)?\n", True, False, COLOR_TITLE, 11.0),
        ("STAGE PLAN es una herramienta web simple que se usa antes de salir al evento (con internet). El técnico ingresa las medidas del salón, ubica sus parlantes en la pantalla y marca dónde están los enchufes de pared o el generador.\n\n"
         "El software actúa de forma inteligente:\n"
         "• Cálculo de cable por equipo: Mide la distancia exacta que necesita cada parlante hacia el enchufe (sumando la bajada del trípode al piso más el recorrido por la orilla de la pared con 10% de holgura para no dejar cables tirantes).\n"
         "• Ruteo inteligente de enchufes: Si el salón tiene 2 o más enchufes, el sistema conecta cada parlante al enchufe que le quede más cerca y que todavía tenga capacidad libre, equilibrando la carga para que ningún enchufe se caliente.\n"
         "• Si hay un solo enchufe: Calcula todo hacia ese único punto y, si se va a sobrecargar, avisa con luz roja.\n"
         "• Sugerencia de nuevos enchufes: Si un enchufe está al límite o un parlante queda a más de 25 metros, el sistema sugiere en qué pared convendría pedirle al dueño del local que habilite una toma adicional.\n"
         "• Cálculo de cinta adhesiva industrial gris (gaffer tape): Mide cuántos metros de cable cruzarán por zonas de paso de gente y calcula cuántos metros de cinta gris pegada al piso necesitas y cuántos rollos de 50 metros debes comprar para evitar tropiezos.\n"
         "• Reporte descargable para usar sin internet: Con un solo clic, genera un PDF en el teléfono para llevar en modo avión con la lista de cables, cinta, atriles y el orden de encendido seguro.", False, False, COLOR_BODY, 10.0)
    ])

    doc.paragraphs[10].text = ""

    # P[15] Objetivo
    set_p_text(doc.paragraphs[15], [
        ("El propósito de STAGE PLAN es eliminar los errores de cálculo en eventos de sonido e iluminación, entregando una herramienta intuitiva que optimiza los metros de cable, previene tropiezos del público mediante el encintado seguro al piso, equilibra el uso de los enchufes disponibles y asegura la continuidad del evento sin cortes de energía.", False, False, COLOR_BODY, 10.0)
    ])

    # P[16] Objetivo General
    set_p_text(doc.paragraphs[16], [
        ("Objetivo General: ", True, False, COLOR_BODY, 10.0),
        ("Desarrollar una aplicación web responsiva e intuitiva que permita a los operadores de DISTORSIONCL SPA ubicar sus equipos en el espacio, calcular de forma inteligente la distancia y calibre de cable hacia los enchufes más cercanos, estimar la cinta de seguridad gris requerida para el piso y exportar un reporte PDF para terreno sin conexión a internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[17] Objetivos Específicos
    set_p_text(doc.paragraphs[17], [
        ("Objetivos Específicos:\n", True, False, COLOR_BODY, 10.0),
        ("1. Levantar los problemas reales de cableado y enchufes en terreno de DISTORSIONCL SPA, como cables tirantes, tropiezos de invitados y enchufes sobrecargados.\n"
         "2. Programar el motor de cálculo espacial y ruteo inteligente con pruebas automáticas (TDD con Vitest), asegurando que el software asigne los equipos al enchufe más cercano y calcule con exactitud los metros de cable y rollos de cinta gris.\n"
         "3. Implementar un servidor seguro en Node.js/Express con PostgreSQL (Prisma ORM) que guarde los salones y planos garantizando que ningún usuario ajeno pueda ver datos de otra productora (seguridad anti-IDOR).\n"
         "4. Construir una interfaz visual en Vue 3 con un plano 2D interactivo y un generador de reportes PDF que funcione sin conexión a internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[20] Alcance - Incluye (v3.2 con ruteo y gaffer)
    set_p_text(doc.paragraphs[20], [
        ("¿Qué incluye el sistema? (Funcionalidades principales):\n", True, False, COLOR_BODY, 10.0),
        ("• Ubicación espacial de equipos en el plano: Permite posicionar la cabina del DJ, parlantes tops en trípodes, bajos en el piso y luces en coordenadas reales del salón.\n"
         "• Detección y soporte de múltiples enchufes: Permite registrar 1 o más enchufes de pared (10A o 16A) o generador portátil.\n"
         "• Ruteo inteligente: Si hay más de un enchufe, conecta cada equipo a la toma más cercana con capacidad disponible. Si hay uno solo, enruta todo hacia ese punto único.\n"
         "• Cálculo de cable por equipo: Calcula los metros de alargador que necesita cada parlante (distancia por la pared + 1.5m de subida al trípode + 10% de holgura).\n"
         "• Estimación de cinta adhesiva industrial gris (gaffer): Mide los cables que cruzan por el suelo y calcula cuántos metros de cinta gris se necesitan (+20% de solapamiento para fijar al piso) y a cuántos rollos de 50 metros equivale.\n"
         "• Sugerencia de nuevos enchufes: Si un enchufe supera el 90% de carga o un parlante está a más de 25 metros, avisa dónde convendría instalar una toma adicional.\n"
         "• Semáforo de advertencia: Verde (seguro), Amarillo (cerca del límite) y Rojo (sobrecarga).\n"
         "• Estudio de sonido (SPL): Calcula los decibeles que llegan al fondo de la pista y avisa si se necesita parlante de refuerzo (delay).\n"
         "• Reporte PDF para terreno: Genera en 1 segundo un archivo descargable que se abre en modo avión con la lista de cables, cinta gaffer y checklist de montaje.", False, False, COLOR_BODY, 10.0)
    ])

    # P[21] Alcance - Excluye
    set_p_text(doc.paragraphs[21], [
        ("¿Qué queda fuera del sistema? (Límites claros):\n", True, False, COLOR_BODY, 10.0),
        ("• No es una app con sincronización bidireccional compleja sin internet (se calcula antes con conexión y se lleva el resultado en PDF para no generar errores de datos).\n"
         "• No incluye bandas en vivo con microfonía de batería o amplificadores de guitarra (acotado exclusivamente a formato DJ y eventos electrónicos).\n"
         "• No realiza la instalación física de enchufes ni reemplaza la firma legal de un instalador eléctrico autorizado por la SEC.", False, False, COLOR_BODY, 10.0)
    ])

    # P[23..25] Stakeholders
    set_p_text(doc.paragraphs[23], [
        ("Cliente / Beneficiario:\n", True, False, COLOR_BODY, 10.0),
        ("• Empresa: Productora y Arriendo de Audio DISTORSIONCL SPA. Representada por su técnico jefe de terreno y montajes.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[24], [
        ("Equipo de Desarrollo:\n", True, False, COLOR_BODY, 10.0),
        ("• Desarrollador Único (Analista Programador INACAP): Responsable de la arquitectura, programación, pruebas y documentación.\n"
         "• Docente Guía: Asesor y evaluador de la asignatura Proyecto Integrado (TIHV43).", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[25], [
        ("Otros Interesados:\n", True, False, COLOR_BODY, 10.0),
        ("• Asistentes y público del evento: Beneficiados directamente porque no sufren accidentes por tropezar con cables sueltos en el piso.\n"
         "• Dueños de parcelas: Beneficiados porque se cuidan los enchufes y automáticos de sus propiedades.", False, False, COLOR_BODY, 10.0)
    ])

    # P[27, 28] Supuestos y Restricciones
    set_p_text(doc.paragraphs[27], [
        ("Supuestos (Condiciones asumidas):\n", True, False, COLOR_BODY, 10.0),
        ("• El técnico planifica su evento previamente desde un computador o celular con conexión.\n"
         "• El técnico cuenta con un smartphone para leer el PDF en terreno.\n"
         "• Se dispone de cinta adhesiva industrial gris estándar (rollos de 50 metros) en bodega para las fijaciones de piso.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[28], [
        ("Restricciones (Limitaciones del proyecto):\n", True, False, COLOR_BODY, 10.0),
        ("• Plazo: 12 semanas del semestre académico de INACAP.\n"
         "• Normativa: Cumplimiento de las reglas de seguridad eléctrica de la SEC (Pliegos RIC 03 y RIC 10) y privacidad de datos (Ley 19.628).", False, False, COLOR_BODY, 10.0)
    ])

    # P[30..33] Hitos
    doc.paragraphs[30].text = "• Semana 1 y 2: Levantamiento con DISTORSIONCL SPA y diseño de la arquitectura de ruteo espacial."
    doc.paragraphs[31].text = "• Semana 3 a 5: Programación del motor de cálculo matemático, distancias y cinta gaffer con pruebas automáticas (TDD)."
    doc.paragraphs[32].text = "• Semana 6 a 9: Construcción del servidor seguro (Backend con Prisma) y pantallas interactivas en Vue 3."
    doc.paragraphs[33].text = "• Semana 10 a 12: Generador de informe PDF para celular, pruebas en terreno y presentación final."
    for idx in range(30, 34):
        doc.paragraphs[idx].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # P[38, 39] Cronograma
    set_p_text(doc.paragraphs[38], [
        ("El proyecto se ejecuta bajo la metodología Kanban combinada con pruebas automáticas (TDD). Para avanzar rápido y sin errores, se trabaja con un máximo de 2 tareas en paralelo en el tablero visual, asegurando que cada fórmula de cableado y cinta de seguridad esté 100% probada antes de diseñar las pantallas.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[39], [
        ("Cronograma de Fases de Trabajo (Kanban + TDD):", True, False, COLOR_BODY, 10.0)
    ])

    # Actualizar Tabla 0
    t = doc.tables[0]
    cronograma_data = [
        ['1. Definición y Levantamiento', 'Semana 1', 'Semana 2', '14 días', 'Ninguna'],
        ['2. Motor de Cálculo y Ruteo (TDD)', 'Semana 3', 'Semana 5', '21 días', 'Fase 1 aprobada'],
        ['3. Servidor y Base de Datos (Backend)', 'Semana 6', 'Semana 7', '14 días', 'Fase 2 aprobada'],
        ['4. Pantallas y Plano 2D (Frontend)', 'Semana 8', 'Semana 9', '14 días', 'Fases 2 y 3'],
        ['5. Reporte PDF en Celular y Pruebas', 'Semana 10', 'Semana 10', '7 días', 'Fase 4'],
        ['6. Entrega Final y Presentación', 'Semana 11', 'Semana 12', '14 días', 'Fases 1 a 5'],
        ['7. Cierre Formal del Proyecto', 'Semana 12', 'Semana 12', '3 días', 'Aprobación final'],
    ]
    for r_idx, row_values in enumerate(cronograma_data):
        row = t.rows[r_idx + 1]
        for c_idx, val in enumerate(row_values):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if len(p.runs) > 0:
                p.runs[0].font.name = 'Open Sans'
                p.runs[0].font.size = Pt(9.0)
                p.runs[0].font.color.rgb = COLOR_BODY

    # P[44] Descripción General con ejemplos
    set_p_text(doc.paragraphs[44], [
        ("STAGE PLAN actúa como un copiloto logístico inteligente para el técnico. Por ejemplo:\n"
         "Si el técnico tiene que armar una fiesta en una parcela con 2 parlantes y 2 bajos, y el salón tiene 2 enchufes de pared (uno cerca de la cabina y otro al fondo a la derecha), el software no tira todos los cables al mismo enchufe como se hace tradicionalmente. Conecta inteligentemente el parlante derecho al enchufe de la derecha (ahorrando 18 metros de cable cruzando la pista) y el parlante izquierdo a la cabina.\n"
         "Además, si detecta que 20 metros de cable tienen que pasar por donde baila la gente, el sistema le dice: 'Lleva 1 rollo de 50m de cinta gris para pegar los cables al piso y evitar tropiezos'. Toda esta información se resume en un reporte limpio que se descarga al celular en 1 segundo.", False, False, COLOR_BODY, 10.0)
    ])

    # P[46] Historias de Usuario con ejemplos v3.2
    set_p_text(doc.paragraphs[46], [
        ("Historias de Usuario Explicadas con Ejemplos Cotidianos (v3.2):\n\n", True, False, COLOR_TITLE, 11.0),
        ("• HU01 (Cuentas Seguras y Privadas):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Productor de eventos.\n"
         "  - Quiero: Iniciar sesión con mi usuario y clave protegida.\n"
         "  - Para: Guardar mis salones y configuraciones sin que otra productora pueda ver mis datos (protección anti-IDOR).\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU02 (Cálculo de Metraje por Equipo y Ruteo Inteligente):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Operador técnico.\n"
         "  - Quiero: Ver cuántos metros de cable necesita cada parlante según su posición en el salón.\n"
         "  - Para: Saber exactamente qué alargadores cargar en la camioneta y conectar cada equipo al enchufe más cercano que tenga capacidad libre.\n"
         "  - Ejemplo: Un parlante a 14 metros del enchufe necesita un alargador de 16 metros por la orilla más 1.5 metros de bajada del trípode (19 metros de cable sugerido).\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU03 (Cálculo de Carga Eléctrica y Generadores):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Técnico de sonido.\n"
         "  - Quiero: Saber si el enchufe o generador va a soportar los equipos.\n"
         "  - Para: Ver una luz roja de alerta antes de que se corte la luz o se queme el alternador.\n"
         "  - Ejemplo: Un generador de 5 kVA entrega 4.000W reales (factor 0.8). Si le conecto 4.200W, el sistema prende luz roja de sobrecarga.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU04 (Cálculo de Cinta Adhesiva Gris para Piso - Gaffer):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Encargado de seguridad y montaje.\n"
         "  - Quiero: Saber cuántos metros de cable cruzan por el suelo donde pasa el público.\n"
         "  - Para: Saber cuántos rollos de cinta adhesiva industrial gris debo comprar para pegarlos al piso y evitar tropiezos.\n"
         "  - Ejemplo: Para 40 metros de cable en el piso, el sistema calcula 48 metros de cinta con solapamiento y me dice: 'Compra 1 rollo de 50 metros (te sobrarán 2 metros)'.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU05 (Sugerencia de Nuevos Enchufes y Sonido):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Productor técnico.\n"
         "  - Quiero: Que el sistema me avise si conviene pedir un enchufe adicional al dueño del salón y si faltan parlantes de refuerzo (delay).\n"
         "  - Para: No forzar alargadores de más de 25 metros y asegurar que la música se escuche impecable en toda la pista.\n"
         "  - Ejemplo: En un salón largo de 28 metros, sugiere instalar una toma cerca de la pista para colocar parlantes de refuerzo con 41 milisegundos de retardo temporal.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU06 (Reporte PDF Autónomo en Modo Avión):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Técnico en terreno.\n"
         "  - Quiero: Descargar el reporte completo en PDF antes de salir de la oficina.\n"
         "  - Para: Tener el mapa de conexiones, la lista de alargadores, los rollos de cinta y el orden de encendido en mi celular aunque esté en una parcela sin internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[48..50] Requerimientos Funcionales v3.2
    set_p_text(doc.paragraphs[48], [
        ("RF01 (Login seguro): ", True, False, COLOR_BODY, 10.0),
        ("Ingreso y registro con contraseña protegida (bcrypt) y sesión segura mediante token JWT.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[49], [
        ("RF02 (Gestión de salones y enchufes): ", True, False, COLOR_BODY, 10.0),
        ("Permite registrar las medidas del salón y la ubicación de 1 o varios enchufes de pared o generador.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[50], [
        ("RF03 (Ubicación de equipos en el plano): ", True, False, COLOR_BODY, 10.0),
        ("Permite ubicar la cabina del DJ, parlantes y luces en coordenadas reales dentro del salón.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF04 (Ruteo inteligente y cálculo de cables): ", True, False, COLOR_BODY, 10.0),
        ("Calcula la distancia de cable hacia el enchufe más cercano disponible. Si hay 1 solo enchufe, calcula todo hacia ese punto. Si un equipo está a más de 25m o el circuito supera el 90%, sugiere habilitar una toma adicional.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF05 (Cálculo de cinta gris para piso): ", True, False, COLOR_BODY, 10.0),
        ("Calcula los metros de cable que pasan por el suelo y entrega la cantidad exacta de rollos de 50m de cinta industrial gris (gaffer tape) para fijarlos al piso.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF06 (Estudio de sonido SPL y Delay): ", True, False, COLOR_BODY, 10.0),
        ("Calcula los decibeles a 1m, en primera fila y en el fondo, avisando si se requiere parlante de refuerzo con retardo temporal en milisegundos.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF07 (Descarga de PDF sin conexión): ", True, False, COLOR_BODY, 10.0),
        ("Genera en el celular el reporte operativo completo listo para abrirse en modo avión sin consumir internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[52..54] RNF
    set_p_text(doc.paragraphs[52], [
        ("RNF01 (Velocidad instantánea): ", True, False, COLOR_BODY, 10.0),
        ("El ruteo inteligente y el cálculo de cables y cinta se ejecutan en menos de 50 milisegundos en la pantalla.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[53], [
        ("RNF02 (Seguridad total anti-IDOR): ", True, False, COLOR_BODY, 10.0),
        ("Ningún usuario puede ver ni modificar los planos o salones de otra productora, incluso si intenta cambiar la dirección en la barra del navegador.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[54], [
        ("RNF03 (Funcionamiento 100% en modo avión): ", True, False, COLOR_BODY, 10.0),
        ("El PDF exportado no depende de internet: se guarda directamente en la memoria del teléfono.\n\n", False, False, COLOR_BODY, 10.0),
        ("RNF04 (Pruebas automáticas TDD): ", True, False, COLOR_BODY, 10.0),
        ("El motor de ruteo y cubicación cuenta con 28 pruebas automatizadas con Vitest que aseguran cero fallas de cálculo.\n\n", False, False, COLOR_BODY, 10.0),
        ("RNF05 (Diseño vertical para celular): ", True, False, COLOR_BODY, 10.0),
        ("La pantalla se adapta fluidamente a cualquier smartphone vertical sin desbordes de texto.", False, False, COLOR_BODY, 10.0)
    ])

    # P[56] Criterios de Aceptación con Números
    set_p_text(doc.paragraphs[56], [
        ("Criterios de Aceptación con Ejemplos Demostrables (v3.2):\n\n", True, False, COLOR_TITLE, 11.0),
        ("• Prueba de Ruteo Inteligente Multi-Toma: ", True, False, COLOR_BODY, 10.0),
        ("Con un enchufe en la izquierda (0,0) y otro en la derecha (10,0), el sistema asigna el parlante izquierdo (1,1) al enchufe 1 y el parlante derecho (9,1) al enchufe 2, equilibrando la corriente y evitando cruzar cables por el centro.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prueba de 1 Solo Enchufe: ", True, False, COLOR_BODY, 10.0),
        ("Si el local tiene solo 1 enchufe de 2.000W y conectamos equipos por 1.900W (95% de uso), el sistema enruta todo hacia ese enchufe pero emite una sugerencia clara: 'El enchufe está al límite (95%); si es posible, solicite habilitar una toma adicional para evitar cortes'.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prueba de Cinta Adhesiva Gris (Gaffer): ", True, False, COLOR_BODY, 10.0),
        ("Para 40 metros de cable que pasan por el suelo transitado, el motor calcula 40 x 1.20 = 48 metros de cinta gris con solapamiento y entrega la sugerencia: 'Llevar 1 rollo de 50 metros (sobrarán 2 metros para detalles)'. Si son 90 metros de cable en piso, calcula 108m de cinta y exige 3 rollos de 50m.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prueba de Distancia Mayor a 25 Metros: ", True, False, COLOR_BODY, 10.0),
        ("Si un parlante queda a 28 metros de tendido de la toma más cercana, el sistema emite aviso de distancia excesiva recomendando colocar una toma intermedia para que el parlante no pierda fuerza eléctrica.", False, False, COLOR_BODY, 10.0)
    ])

    # P[60..64] Metodología y Seguridad
    set_p_text(doc.paragraphs[60], [
        ("¿Por qué elegimos Kanban + Pruebas Automáticas (TDD)?\n\n", True, False, COLOR_TITLE, 11.0),
        ("Se descartó Scrum porque exige reuniones diarias y roles que no aplican a un proyecto individual. Con Kanban tenemos un tablero visual simple con máximo 2 tareas a la vez para no perder el foco. Y con TDD (Test-Driven Development) escribimos primero la prueba matemática y luego el código; así nos aseguramos de que el cálculo de metros de cable, los rollos de cinta gris y el ruteo de enchufes funcionen con 100% de exactitud.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[62], [
        ("Este método permitió validar semana a semana con DISTORSIONCL SPA que las distancias calculadas y la cantidad de cinta sugerida correspondan a lo que el técnico gasta realmente en sus eventos.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[64], [
        ("Seguridad TI y Cuidado de las Personas (Explicadas simples):\n\n", True, False, COLOR_TITLE, 11.0),
        ("• Nadie puede ver recintos ajenos (Anti-IDOR): ", True, False, COLOR_BODY, 10.0),
        ("El servidor valida que el usuario sea el dueño del recinto antes de entregar cualquier dato. Si alguien intenta cambiar el ID en la barra del navegador, se le bloquea el acceso de inmediato.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prevención de tropiezos y accidentes físicos: ", True, False, COLOR_BODY, 10.0),
        ("El cálculo de cinta gris industrial (gaffer tape) cumple el principio ético de cuidar la integridad física de los invitados y del personal, evitando caídas o desconexiones accidentales.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Aviso legal de la SEC: ", True, False, COLOR_BODY, 10.0),
        ("Para actuar con responsabilidad profesional, cada reporte incluye el aviso obligatorio de que el software es una guía de ayuda previa y no reemplaza la certificación de un electricista autorizado por la SEC.", False, False, COLOR_BODY, 10.0)
    ])

    # P[67] Conclusión
    set_p_text(doc.paragraphs[67], [
        ("Conclusión del Diagnóstico:\n", True, False, COLOR_TITLE, 11.0),
        ("STAGE PLAN v3.2 demuestra cómo el software puede resolver problemas muy concretos de terreno: saber qué cable tirar, a qué enchufe conectarlo para no sobrecargarlo, cuánta cinta gris llevar para no provocar accidentes y cómo orientar los parlantes para que la música suene bien. Con 28 pruebas automáticas aprobadas y un diseño pensado para celulares sin internet, el proyecto está completamente maduro, probado y listo para su defensa.", False, False, COLOR_BODY, 10.0)
    ])

    # P[70, 74]
    set_p_text(doc.paragraphs[70], [
        ("• Superintendencia de Electricidad y Combustibles (SEC). (2020). Pliego Técnico Normativo RIC N° 03 y RIC N° 10.\n"
         "• Biblioteca del Congreso Nacional de Chile. (1999). Ley N° 19.628: Sobre protección de la vida privada y datos personales.\n"
         "• Beck, Kent. (2003). Test-Driven Development: By Example. Desarrollo guiado por pruebas.\n"
         "• Davis, D., & Patronis, E. (2012). Sound System Engineering. Ingeniería de sistemas de sonido.", False, False, COLOR_BODY, 9.5)
    ])
    set_p_text(doc.paragraphs[74], [
        ("• Anexo 1: Matriz de Trazabilidad (Historias de Usuario vs. Requerimientos vs. Pruebas).\n"
         "• Anexo 2: Reporte de 28 Pruebas Unitarias Automatizadas con Vitest (100% de éxito).\n"
         "• Anexo 3: Ejemplo de Reporte Operativo en PDF con cubicación de cinta gaffer y ruteo inteligente.\n"
         "• Anexo 4: Esquema de base de datos relacional Prisma y diagrama de arquitectura monorepo.", False, False, COLOR_BODY, 9.5)
    ])

    doc.save('Formato_propuesto_sumativa 01_2026.docx')
    print("Formato_propuesto_sumativa 01_2026.docx updated to v3.2 successfully.")

if __name__ == '__main__':
    update_sumativa_v32()

