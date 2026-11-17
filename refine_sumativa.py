import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def refine_sumativa():
    doc = docx.Document('Formato_propuesto_sumativa 01_2026.bak.docx')

    COLOR_BODY = RGBColor(0x33, 0x33, 0x33) # Gris oscuro nítido y legible
    COLOR_TITLE = RGBColor(0x1F, 0x49, 0x7D)
    FONT_NAME = 'Open Sans'
    FONT_LIGHT = 'Open Sans Light'

    # Ajustamos el estilo base Estilo3 y Título1 para alineación a la izquierda (LEFT)
    # Esto elimina de raíz el estiramiento de palabras de Word
    for s in doc.styles:
        if s.name in ['Estilo3', 'Título1', 'Normal']:
            s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Helper para asignar texto limpio, alineado a la izquierda
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
    p_sub = doc.paragraphs[1]
    set_p_text(p_sub, [
        ("STAGE PLAN (v3.1)\n", True, False, COLOR_TITLE, 22.0),
        ("Sistema Web de Planificación Logística, Dimensionamiento Eléctrico y Distribución Espacial para Eventos en Formato DJ", False, False, COLOR_TITLE, 14.0)
    ])

    p_meta = doc.paragraphs[6]
    set_p_text(p_meta, [
        ("Carrera: Analista Programador | Asignatura: Proyecto Integrado (TIHV43)\n"
         "Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA\n"
         "Sede: INACAP Santiago | Periodo: Primavera 2026", False, True, RGBColor(0x66, 0x66, 0x66), 10.0)
    ])

    # P[8] Título RESUMEN EJECUTIVO
    doc.paragraphs[8].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # P[9] Resumen Ejecutivo - Redacción Clara, Explicada con Ejemplos Simples
    p_res = doc.paragraphs[9]
    set_p_text(p_res, [
        ("¿Qué problema resuelve este proyecto?\n", True, False, COLOR_TITLE, 11.0),
        ("En la mayoría de los eventos con DJ o música en vivo en Chile, los técnicos calculan los cables, la electricidad y los parlantes 'al ojo' o por pura costumbre. Por ejemplo, es muy común que conecten los equipos de sonido y las luces a cualquier enchufe de pared que encuentren, o que tiren un alargador largo y delgado de más de 30 metros hacia el escenario.\n\n"
         "Esto provoca problemas graves y frecuentes en terreno: se corta la luz a mitad de la fiesta porque el automático no aguanta, o el voltaje baja tanto que los amplificadores se apagan o se queman. Además, en muchas parcelas de eventos (como en Curacaví, Lampa o Pirque) no hay señal de celular (4G/5G), por lo que el técnico no puede consultar manuales en internet ni usar sistemas en la nube cuando ya está en el lugar.\n\n", False, False, COLOR_BODY, 10.0),
        ("¿Cuál es la solución que creamos?\n", True, False, COLOR_TITLE, 11.0),
        ("STAGE PLAN es una aplicación web pensada para usarse antes de salir de casa o de la oficina (con conexión a internet). El usuario ingresa las medidas del salón (por ejemplo, 10 metros de ancho por 16 de fondo) y qué equipos va a llevar (cuántos parlantes, cuántas luces y si se enchufa a la pared o a un generador).\n\n"
         "El sistema hace los cálculos de ingeniería de forma automática aplicando las reglas oficiales de la SEC (Superintendencia de Electricidad y Combustibles):\n"
         "1. Le dice exactamente qué grosor de cable necesita para que no se caiga el voltaje ni se caliente el cable.\n"
         "2. Le muestra un semáforo (Verde, Amarillo o Rojo) que avisa si el enchufe o el generador van a aguantar la carga.\n"
         "3. Le indica si en el fondo de la pista la música se va a escuchar bien o si necesita poner parlantes de refuerzo (delay).\n"
         "4. Le entrega un plano 2D visual en la pantalla con la posición de la cabina del DJ y los parlantes.\n\n", False, False, COLOR_BODY, 10.0),
        ("El beneficio clave para el terreno:\n", True, False, COLOR_TITLE, 11.0),
        ("Con un solo botón, la aplicación genera un archivo PDF descargable en el celular del técnico. Así, cuando llega a una parcela sin señal de internet, abre el PDF en modo avión y tiene su lista de materiales completa, el metraje de cables y la guía paso a paso para conectar y encender todo sin peligro de incendio ni cortes de luz.", False, False, COLOR_BODY, 10.0)
    ])

    doc.paragraphs[10].text = "" # limpiar lineamientos genéricos

    # P[15] Objetivo del Proyecto
    p_obj_desc = doc.paragraphs[15]
    set_p_text(p_obj_desc, [
        ("El propósito de STAGE PLAN es evitar que los eventos fracasen por fallas eléctricas o mal sonido. Transforma un proceso que hoy se hace 'al ojo' en una planificación digital simple, rápida y segura, permitiendo que un técnico arme su evento en menos de 5 minutos con la certeza de que la instalación eléctrica cumple la norma chilena y funcionará sin interrupciones.", False, False, COLOR_BODY, 10.0)
    ])

    # P[16] Objetivo General
    p_og = doc.paragraphs[16]
    set_p_text(p_og, [
        ("Objetivo General: ", True, False, COLOR_BODY, 10.0),
        ("Desarrollar una aplicación web fácil de usar desde el celular o computador que permita a técnicos y DJs de la productora DISTORSIONCL SPA calcular la electricidad, los cables y la distribución del sonido antes de cada evento, generando un informe en PDF descargable que se pueda consultar en terreno sin conexión a internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[17] Objetivos Específicos
    p_oe = doc.paragraphs[17]
    set_p_text(p_oe, [
        ("Objetivos Específicos:\n", True, False, COLOR_BODY, 10.0),
        ("1. Levantar la información real de los montajes de DISTORSIONCL SPA, identificando fallas típicas como sobrecarga de automáticos de 10A, confusión entre kVA y kW en generadores y pérdida de volumen en pistas largas.\n"
         "2. Programar el motor de cálculo matemático (calc-engine) con pruebas automatizadas (TDD con Vitest), asegurando que cada fórmula de cables (norma SEC RIC 03/10) y de sonido (decibeles SPL) entregue resultados 100% exactos.\n"
         "3. Construir un servidor seguro (Backend) con Node.js, Express y base de datos PostgreSQL, garantizando que cada usuario solo pueda ver y modificar sus propios recintos guardados (seguridad anti-IDOR).\n"
         "4. Diseñar una interfaz moderna y clara (Frontend en Vue 3) que muestre un plano 2D del recinto y permita descargar el informe en PDF con un solo clic directamente en el teléfono del usuario.", False, False, COLOR_BODY, 10.0)
    ])

    # P[20] Alcance - Incluye (con ejemplos)
    p_inc = doc.paragraphs[20]
    set_p_text(p_inc, [
        ("¿Qué incluye el sistema? (Funcionalidades principales):\n", True, False, COLOR_BODY, 10.0),
        ("• Registro e inicio de sesión seguro: Cada técnico tiene su usuario y contraseña protegida.\n"
         "• Registro del lugar del evento (Recinto): Medidas de ancho, largo y distancia hasta el enchufe (por ejemplo: salón de 10x16 metros a 30 metros del enchufe).\n"
         "• Configuración de equipos (Rider técnico): Cantidad de parlantes (tops y bajos), potencia en Watts, luces y fuente de energía (enchufe de pared de 10A/16A o generador a bencina).\n"
         "• Cálculo automático de cables: Indica los metros necesarios (+10% de holgura para no dejarlo tirante) y el grosor de cable comercial obligatorio (por ejemplo: cable de 2.5 mm² para que no se caiga el voltaje).\n"
         "• Semáforo de advertencia eléctrica: Verde si todo está seguro, Amarillo si está cerca del límite, y Rojo si el automático se va a cortar.\n"
         "• Cálculo de sonido (SPL): Calcula cuántos decibeles llegarán al fondo de la pista y avisa si se necesita agregar un parlante de refuerzo (delay).\n"
         "• Inventario de fierros y alargadores: Dice exactamente cuántos atriles se necesitan y cuántas zapatillas eléctricas con enchufes de sobra.\n"
         "• Plano 2D en pantalla: Dibuja la cabina del DJ, los parlantes en el suelo y los cables a escala.\n"
         "• Descarga de Reporte PDF: Un documento listo para llevar en el celular que funciona sin internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[21] Alcance - Excluye
    p_exc = doc.paragraphs[21]
    set_p_text(p_exc, [
        ("¿Qué queda fuera del sistema? (Límites claros):\n", True, False, COLOR_BODY, 10.0),
        ("• No es una aplicación con sincronización compleja sin internet: Para no complicar el sistema con errores de datos, el cálculo se hace antes con internet y se lleva el resultado en PDF.\n"
         "• No soporta bandas en vivo completas: Está enfocado exclusivamente en eventos formato DJ y música grabada (no incluye micrófonos de batería ni amplificadores de guitarra).\n"
         "• No controla ecualizadores ni mesas de sonido en tiempo real.\n"
         "• No reemplaza la firma legal de un instalador eléctrico autorizado por la SEC: Es una guía de pre-producción para no cometer errores técnicos.", False, False, COLOR_BODY, 10.0)
    ])

    # P[23..25] Stakeholders
    set_p_text(doc.paragraphs[23], [
        ("Cliente y Beneficiario:\n", True, False, COLOR_BODY, 10.0),
        ("• Productora y Arriendo de Audio DISTORSIONCL SPA (Santiago, Chile). Representada por su técnico de sonido e iluminación jefe de terreno.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[24], [
        ("Equipo de Desarrollo:\n", True, False, COLOR_BODY, 10.0),
        ("• Desarrollador Único (Scrum Master / Developer): Estudiante de Analista Programador de INACAP, a cargo del diseño, programación, pruebas y documentación.\n"
         "• Docente Guía: Profesor de la asignatura Proyecto Integrado, a cargo de la evaluación y retroalimentación académica.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[25], [
        ("Otros Interesados:\n", True, False, COLOR_BODY, 10.0),
        ("• DJs y Operadores de montaje: Usuarios que leen el PDF en terreno para saber qué cable conectar y en qué orden encender los equipos.\n"
         "• Dueños de parcelas y recintos: Beneficiados porque se evitan cortocircuitos e incendios en sus instalaciones.", False, False, COLOR_BODY, 10.0)
    ])

    # P[27, 28] Supuestos y Restricciones
    set_p_text(doc.paragraphs[27], [
        ("Supuestos (Lo que damos por hecho):\n", True, False, COLOR_BODY, 10.0),
        ("• El técnico planifica su evento con tiempo desde un computador o celular con conexión a internet.\n"
         "• El técnico cuenta con un teléfono inteligente capaz de abrir documentos PDF.\n"
         "• Los datos de potencia y parlantes que ingresa el usuario corresponden a los Watts reales (RMS) indicados por el fabricante.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[28], [
        ("Restricciones (Limitaciones del proyecto):\n", True, False, COLOR_BODY, 10.0),
        ("• Plazo: Debe completarse en el semestre académico de 12 semanas.\n"
         "• Equipo: Es desarrollado por un solo estudiante (por eso se eligió un método de trabajo ágil y ordenado sin burocracia).\n"
         "• Leyes y normas: Debe respetar la normativa eléctrica de la SEC (Pliegos RIC 03 y RIC 10) y la ley chilena de privacidad de datos (Ley 19.628).", False, False, COLOR_BODY, 10.0)
    ])

    # P[30..33] Hitos
    doc.paragraphs[30].text = "• Semana 1 y 2: Levantamiento de información con DISTORSIONCL SPA y diseño de la arquitectura."
    doc.paragraphs[31].text = "• Semana 3 a 5: Programación del motor de cálculo matemático con pruebas unitarias automáticas (TDD)."
    doc.paragraphs[32].text = "• Semana 6 a 9: Creación del servidor (Backend), base de datos y la interfaz web con el plano 2D (Frontend)."
    doc.paragraphs[33].text = "• Semana 10 a 12: Generador de informe PDF en el celular, pruebas finales y defensa del proyecto."
    for idx in range(30, 34):
        doc.paragraphs[idx].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # P[38, 39] Cronograma
    set_p_text(doc.paragraphs[38], [
        ("El proyecto se organiza en 5 etapas prácticas a lo largo de 12 semanas. Para avanzar de forma ordenada y sin atrasos, se utiliza un tablero visual de tareas (Kanban), donde no se pueden hacer más de 2 tareas al mismo tiempo. Además, antes de hacer las pantallas bonitas, se programó y probó el motor matemático para asegurar que ningún cálculo falle.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[39], [
        ("Cronograma de Fases de Trabajo:", True, False, COLOR_BODY, 10.0)
    ])

    # P[44] Descripción General de la Solución
    set_p_text(doc.paragraphs[44], [
        ("STAGE PLAN funciona como un asistente inteligente para el técnico. Por ejemplo: si el técnico tiene que sonorizar un matrimonio en una parcela con 2 parlantes de 400W y 2 bajos de 800W, y el único enchufe disponible está a 30 metros en la cocina de la parcela, el técnico abre STAGE PLAN, ingresa estos números y el sistema le dice de inmediato:\n"
         "- 'Cuidado: estás consumiendo 9.8 Amperes con el margen de seguridad; un enchufe común de 10A está al límite'.\n"
         "- 'Usa un alargador de 33 metros con cable grueso de 2.5 mm²; si usas un cable delgado de 1.5 mm², el voltaje se te va a caer a 213V y los parlantes se van a apagar'.\n"
         "- 'Debes llevar 2 atriles de fierro para los parlantes y 2 tubos para montar sobre los bajos'.\n"
         "Toda esta información se resume en un reporte limpio que se descarga al teléfono en 1 segundo.", False, False, COLOR_BODY, 10.0)
    ])

    # P[46] Historias de Usuario con Ejemplos Claros
    set_p_text(doc.paragraphs[46], [
        ("Historias de Usuario Explicadas con Ejemplos Cotidianos:\n\n", True, False, COLOR_TITLE, 11.0),
        ("• HU01 (Cuentas Seguras):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Productor de eventos.\n"
         "  - Quiero: Iniciar sesión con mi correo y clave privada.\n"
         "  - Para: Que mis salones y configuraciones queden guardados y ningún otro usuario pueda verlos ni modificarlos.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU02 (Cálculo de Cables y Caída de Voltaje):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Operador técnico.\n"
         "  - Quiero: Poner la distancia en metros desde el escenario hasta el enchufe.\n"
         "  - Para: Saber qué grosor de cable debo llevar en la camioneta para que los equipos no se apaguen por bajo voltaje.\n"
         "  - Ejemplo: Para 1.800 Watts a 30 metros, el sistema me exige cable de 2.5 mm² y me sugiere 33 metros de largo.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU03 (Cálculo de Carga Eléctrica y Generadores):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Técnico de sonido.\n"
         "  - Quiero: Indicar si me conecto a un enchufe de pared de 10A o a un generador a bencina de 5 kVA.\n"
         "  - Para: Ver una luz roja de advertencia si voy a sobrecargar la corriente o si el generador no va a aguantar.\n"
         "  - Ejemplo: Un generador de 5 kVA no da 5.000 Watts reales, sino 4.000 Watts (por el factor 0.8). Si pongo 4.200 Watts, el sistema me frena con alerta roja.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU04 (Lista de Atriles y Zapatillas):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Encargado de bodega y logística.\n"
         "  - Quiero: Que el sistema me diga cuántos fierros y zapatillas cargar en la camioneta.\n"
         "  - Para: No llegar al evento y darme cuenta de que me faltó un trípode para un parlante.\n"
         "  - Ejemplo: Si llevo 2 bajos al suelo y 4 parlantes arriba, me calcula 2 tubos sobre los bajos y 2 trípodes libres.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU05 (Sonido y Plano 2D):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Productor técnico.\n"
         "  - Quiero: Ver un plano 2D de la pista de baile y saber a qué volumen llegará la música al fondo.\n"
         "  - Para: Saber si el público del fondo va a escuchar bien o si necesito poner parlantes de refuerzo (delay).\n"
         "  - Ejemplo: En un salón de 28 metros, el sonido cae 16 decibeles; el sistema me avisa que ponga 2 parlantes a mitad de salón con 41 milisegundos de retardo.\n\n", False, False, COLOR_BODY, 10.0),
        ("• HU06 (Reporte PDF en Modo Avión):\n", True, False, COLOR_BODY, 10.0),
        ("  - Como: Técnico en terreno.\n"
         "  - Quiero: Descargar el reporte completo en PDF antes de salir.\n"
         "  - Para: Revisar el checklist y el orden de encendido en la parcela aunque no tenga ni una barra de señal de celular.", False, False, COLOR_BODY, 10.0)
    ])

    # P[48..50] Requerimientos Funcionales Explicados
    set_p_text(doc.paragraphs[48], [
        ("RF01 (Login seguro): ", True, False, COLOR_BODY, 10.0),
        ("El sistema permite registrarse e ingresar con contraseña encriptada (bcrypt) y sesión protegida por token JWT.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[49], [
        ("RF02 (Gestión de salones): ", True, False, COLOR_BODY, 10.0),
        ("Permite guardar salones con su ancho, largo y distancia al enchufe, asegurando que nadie más pueda espiar los datos de otro usuario.", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[50], [
        ("RF03 (Configuración de equipos): ", True, False, COLOR_BODY, 10.0),
        ("Permite elegir la cantidad y potencia de los parlantes, las luces y si se usará red de pared o generador.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF04 (Motor de cálculo matemático): ", True, False, COLOR_BODY, 10.0),
        ("Calcula en segundos la corriente con 20% de holgura de seguridad, el grosor de cable por norma SEC, la potencia del amplificador y la caída de decibeles de sonido.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF05 (Plano 2D interactivo): ", True, False, COLOR_BODY, 10.0),
        ("Dibuja un plano esquemático en la pantalla mostrando la posición de la cabina del DJ, los parlantes en el suelo y el tablero eléctrico.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF06 (Descarga de PDF sin red): ", True, False, COLOR_BODY, 10.0),
        ("Genera en un clic un archivo PDF dentro del celular del usuario, listo para abrirse sin gastar datos móviles.\n\n", False, False, COLOR_BODY, 10.0),
        ("RF07 (Historial de eventos): ", True, False, COLOR_BODY, 10.0),
        ("Guarda los cálculos anteriores para poder reutilizar los datos de un salón ya visitado sin tener que medir todo de nuevo.", False, False, COLOR_BODY, 10.0)
    ])

    # P[52..54] Requerimientos No Funcionales Explicados
    set_p_text(doc.paragraphs[52], [
        ("RNF01 (Velocidad del cálculo): ", True, False, COLOR_BODY, 10.0),
        ("El sistema hace todos los cálculos matemáticos en menos de medio segundo (inmediato al escribir).", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[53], [
        ("RNF02 (Seguridad contra accesos no autorizados): ", True, False, COLOR_BODY, 10.0),
        ("Aunque alguien intente cambiar el número de identificación en la barra del navegador, el sistema no le permite ver datos de recintos ajenos (protección anti-IDOR).", False, False, COLOR_BODY, 10.0)
    ])
    set_p_text(doc.paragraphs[54], [
        ("RNF03 (Funciona en modo avión): ", True, False, COLOR_BODY, 10.0),
        ("El PDF generado es 100% independiente: contiene todos los datos y se abre en cualquier celular sin internet.\n\n", False, False, COLOR_BODY, 10.0),
        ("RNF04 (Calidad y cero errores): ", True, False, COLOR_BODY, 10.0),
        ("El motor de cálculo tiene pruebas automáticas con más del 90% de cobertura; si una fórmula da un resultado incorrecto, el sistema avisa de inmediato antes de publicarlo.\n\n", False, False, COLOR_BODY, 10.0),
        ("RNF05 (Adaptable al celular): ", True, False, COLOR_BODY, 10.0),
        ("La pantalla se adapta perfectamente a la pantalla vertical de cualquier teléfono móvil sin que los textos se corten ni se salgan de los bordes.", False, False, COLOR_BODY, 10.0)
    ])

    # P[56] Criterios de Aceptación con Números Reales
    set_p_text(doc.paragraphs[56], [
        ("Criterios de Aceptación (Cómo demostramos que el sistema funciona):\n\n", True, False, COLOR_TITLE, 11.0),
        ("• Prueba de Cable (Ejemplo real): ", True, False, COLOR_BODY, 10.0),
        ("Si conectamos 1.800 Watts a 30 metros de distancia, la corriente sube a 9.82 Amperes con el margen de seguridad. Un cable delgado de 1.5 mm² provocaría una caída de voltaje peligrosa. El sistema exige automáticamente cable grueso de 2.5 mm² y entrega una caída de voltaje segura de solo 4.12 Volts (1.87%).\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prueba de Sobrecarga (Ejemplo real): ", True, False, COLOR_BODY, 10.0),
        ("Si conectamos 2.000 Watts a un enchufe domiciliario de 10A, la corriente necesaria es 10.91A. Como supera los 10A, el sistema prende una luz ROJA CRÍTICA avisando que el automático se va a cortar.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prueba de Generador (Ejemplo real): ", True, False, COLOR_BODY, 10.0),
        ("Si alquilamos un generador de 5 kVA, el sistema sabe que entrega 4.000 Watts reales (factor 0.8). Si le enchufamos 4.200 Watts, enciende luz ROJA avisando que el generador se va a apagar por sobrecarga.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Prueba de Sonido (Ejemplo real): ", True, False, COLOR_BODY, 10.0),
        ("En una pista de 16 metros, la música sale a 125 decibeles del parlante, llega a 113 dB en la primera fila y cae a 100.9 dB en el fondo. Como la diferencia es mayor a 10 dB, el sistema avisa que se necesita poner parlantes de refuerzo (delay) para emparejar el sonido.", False, False, COLOR_BODY, 10.0)
    ])

    # P[60] Comparación de Metodologías Explicada Sencilla
    set_p_text(doc.paragraphs[60], [
        ("¿Por qué elegimos Kanban y pruebas automáticas (TDD) en vez de otros métodos?\n\n", True, False, COLOR_TITLE, 11.0),
        ("1. Cascada tradicional: Se descartó porque es muy rígida. Si nos dábamos cuenta de que un cálculo eléctrico necesitaba un ajuste al final, teníamos que rehacer todo el proyecto desde cero.\n\n"
         "2. Scrum tradicional: Se descartó porque Scrum está pensado para equipos grandes con muchas reuniones diarias (Dailies, Retrospectivas). Al ser un proyecto desarrollado por una sola persona, esas reuniones eran una pérdida de tiempo innecesaria.\n\n"
         "3. Kanban + TDD (Nuestra elección): Es la combinación perfecta. Usamos un tablero visual donde vemos qué tareas están pendientes, cuáles se están haciendo (máximo 2 a la vez para no perder el foco) y cuáles están listas. Además, con TDD (Test-Driven Development) primero escribimos la prueba matemática y luego el código; así nos aseguramos de que ninguna fórmula tenga errores antes de pasar a la siguiente etapa.", False, False, COLOR_BODY, 10.0)
    ])

    # P[62] Selección de Metodología
    set_p_text(doc.paragraphs[62], [
        ("Esta forma de trabajo permitió entregarle avances rápidos a DISTORSIONCL SPA semana a semana, validando que el grosor de los cables y las alertas de los generadores coincidieran exactamente con lo que el técnico necesita en sus eventos reales.", False, False, COLOR_BODY, 10.0)
    ])

    # P[64] Seguridad TI y Ética Explicadas Claras
    set_p_text(doc.paragraphs[64], [
        ("Seguridad y Ética Profesional (Explicadas de forma clara):\n\n", True, False, COLOR_TITLE, 11.0),
        ("• Protección contra 'mirar datos ajenos' (Anti-IDOR): ", True, False, COLOR_BODY, 10.0),
        ("En muchos sistemas web mal hechos, si un usuario cambia el número del salón en la barra de internet (por ejemplo de /recinto/1 a /recinto/2), puede ver los eventos de otra productora. En STAGE PLAN eso es imposible: el servidor revisa que el usuario sea el dueño real de ese dato; si no lo es, le bloquea el acceso de inmediato.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Cuidado con los datos personales: ", True, False, COLOR_BODY, 10.0),
        ("Cumplimos con la ley chilena (Ley 19.628). Los nombres de los clientes y las direcciones de las parcelas son totalmente privados y no se comparten con nadie.\n\n", False, False, COLOR_BODY, 10.0),
        ("• Responsabilidad y ética (Aviso legal de la SEC): ", True, False, COLOR_BODY, 10.0),
        ("La electricidad es peligrosa y un mal cálculo puede provocar un incendio o electrocutar a alguien. Para actuar con ética profesional, el software incluye un aviso obligatorio en la pantalla y en cada PDF que aclara: 'Este software es una guía de ayuda para la pre-producción y no reemplaza la inspección de un instalador eléctrico certificado por la SEC'.", False, False, COLOR_BODY, 10.0)
    ])

    # P[67] Conclusiones
    set_p_text(doc.paragraphs[67], [
        ("Conclusión del Diagnóstico:\n", True, False, COLOR_TITLE, 11.0),
        ("Este proyecto demuestra que la tecnología puede resolver un problema real y riesgoso en los eventos en Chile. Al cambiar el cálculo 'a ojo' por una herramienta web simple que genera un PDF para usar sin internet en las parcelas, logramos que los técnicos ahorren tiempo, eviten que la música se corte a mitad de fiesta y cuiden la seguridad de las personas. La arquitectura monorepo y las pruebas matemáticas garantizan que el software es sólido, seguro y listo para ser defendido ante la comisión evaluadora de INACAP.", False, False, COLOR_BODY, 10.0)
    ])

    # P[70] Referencias
    set_p_text(doc.paragraphs[70], [
        ("• Superintendencia de Electricidad y Combustibles (SEC). (2020). Pliego Técnico Normativo RIC N° 03: Alimentadores y sistemas de distribución.\n"
         "• Superintendencia de Electricidad y Combustibles (SEC). (2020). Pliego Técnico Normativo RIC N° 10: Instalaciones de uso general y eventos provisorios.\n"
         "• Biblioteca del Congreso Nacional de Chile. (1999). Ley N° 19.628: Sobre protección de la vida privada y datos personales.\n"
         "• Beck, Kent. (2003). Test-Driven Development: By Example. Desarrollo guiado por pruebas.\n"
         "• Davis, D., & Patronis, E. (2012). Sound System Engineering. Ingeniería de sistemas de sonido.", False, False, COLOR_BODY, 9.5)
    ])

    # P[74] Anexos
    set_p_text(doc.paragraphs[74], [
        ("• Anexo 1: Matriz de Trazabilidad (Historias de Usuario vs. Requerimientos vs. Pruebas).\n"
         "• Anexo 2: Reporte de Pruebas Unitarias Automatizadas con Vitest (100% de éxito).\n"
         "• Anexo 3: Ejemplo de Reporte Operativo en PDF generado para un evento en Curacaví.\n"
         "• Anexo 4: Esquema de base de datos relacional Prisma y diagrama de componentes.", False, False, COLOR_BODY, 9.5)
    ])

    doc.save('Formato_propuesto_sumativa 01_2026.docx')
    print("Formato_propuesto_sumativa 01_2026.docx refined successfully.")

if __name__ == '__main__':
    refine_sumativa()

