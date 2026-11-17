import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_guia_v32():
    doc = docx.Document('TIHV43_GUÍA_ABPRO_U1.bak.docx')

    COLOR_ANSWER = RGBColor(0x1F, 0x49, 0x7D)
    COLOR_Q = RGBColor(0x26, 0x26, 0x26)
    COLOR_TITLE = RGBColor(0x1F, 0x49, 0x7D)

    # 1. TABLA 2: PREGUNTAS ORIENTADORAS
    t2_cell = doc.tables[2].rows[0].cells[0]
    tc = t2_cell._tc
    w_p_list = tc.findall(docx.oxml.ns.qn('w:p'))
    for wp in w_p_list[1:]:
        tc.remove(wp)

    p0 = t2_cell.paragraphs[0]
    p0.text = "Preguntas orientadoras para el diagnóstico (v3.2) — Respuestas claras con ejemplos sobre ruteo de cables, enchufes y cinta gris (DISTORSIONCL SPA):"
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.runs[0].bold = True
    p0.runs[0].font.name = 'Arial'
    p0.runs[0].font.size = Pt(10.0)

    preguntas_respuestas = [
        (
            "¿Cuáles son las principales necesidades del negocio que requieren una solución de software y cómo afectan a las operaciones, a los empleados y a los clientes de la empresa?",
            "El cliente DISTORSIONCL SPA tiene 4 problemas graves porque hoy calcula todo 'a ojo':\n"
            "1. Cortes de luz: Conectan todos los parlantes a un solo enchufe casero de 10A, el enchufe se sobrecalienta y salta el automático a mitad de la fiesta.\n"
            "2. Caídas de voltaje: Usan alargadores delgados de más de 30 metros; el voltaje baja de 220V a menos de 200V y los amplificadores se apagan solos.\n"
            "3. Cables sueltos y tropiezos: Tiran cables cruzando por donde camina la gente sin calcular cuánta cinta adhesiva gris necesitan para pegarlos al piso, arriesgando caídas de invitados o que alguien desenchufe un parlante de una patada.\n"
            "4. Falta de inteligencia al repartir enchufes: Si el salón tiene 2 enchufes en paredes opuestas, no saben cómo repartir la carga y sobrecargan uno solo innecesariamente.\n"
            "Esto estresa al personal técnico, perjudica el prestigio de la productora y arruina eventos en vivo."
        ),
        (
            "¿Qué tipos de software o tecnología ya utiliza la empresa y cómo se integran en sus procesos actuales? ¿Existen limitaciones o brechas que estas herramientas no cubren?",
            "Hoy usan planillas de Excel básicas y mensajes de WhatsApp. Sus limitaciones son:\n"
            "- Excel no sabe dónde están ubicados los parlantes ni calcula los metros de cable que van por la pared o por el suelo.\n"
            "- No calcula automáticamente cuántos rollos de cinta gris se necesitan para pegar los cables al piso.\n"
            "- No sugiere si conviene pedirle al dueño del local habilitar un enchufe adicional.\n"
            "- En parcelas de eventos (Curacaví, Lampa, Pirque) no hay señal de celular (4G/5G), por lo que planillas en la nube quedan inutilizables en terreno."
        ),
        (
            "¿Cómo podríamos aplicar metodologías emergentes, como Design Thinking, DevOps o Agile, para desarrollar una solución adaptada a las necesidades del negocio?",
            "Trabajamos con Kanban y pruebas automáticas (TDD con Vitest).\n"
            "En un tablero visual vemos qué tareas están pendientes y cuáles en curso (máximo 2 a la vez). Con TDD programamos primero las pruebas matemáticas del ruteo de cables y la cinta gaffer; así nos aseguramos de que el software entregue resultados exactos antes de ponerlo en producción."
        ),
        (
            "¿De qué manera el diagnóstico de necesidades tecnológicas puede beneficiarse de técnicas como entrevistas, encuestas o análisis de datos de usuario? ¿Qué información clave debería recogerse para fundamentar una propuesta de solución?",
            "Conversamos con el técnico en terreno y revisamos 5 eventos reales. Datos clave descubiertos:\n"
            "- Los técnicos gastan en promedio 1 rollo de cinta gris de 50m cada 40m de cable en piso.\n"
            "- La mayoría de los salones tienen al menos 2 enchufes, pero los técnicos casi siempre usan uno solo por comodidad.\n"
            "- Los alargadores de más de 25 metros provocan pérdidas notorias de potencia en los parlantes."
        ),
        (
            "¿Cuáles son los posibles impactos éticos de la solución de software en los empleados, los clientes y otros actores relacionados con el negocio? ¿Cómo se puede asegurar la transparencia y el respeto a la privacidad en el diseño?",
            "El mayor impacto ético es cuidar la vida y la integridad física de las personas:\n"
            "1. Cuidar de tropiezos: El cálculo obligatorio de cinta gris para piso previene caídas y accidentes de invitados.\n"
            "2. Cuidar de incendios: El semáforo de sobrecarga previene que los enchufes ardan por calentamiento continuo.\n"
            "3. Aviso legal de la SEC: Se estampa en cada pantalla y PDF que el sistema es una guía previa y no reemplaza a un electricista certificado.\n"
            "4. Privacidad: Los nombres y direcciones de las parcelas se guardan con clave y aislamiento por usuario (anti-IDOR) según la Ley 19.628."
        ),
        (
            "¿De qué modo la solución de software propuesta puede promover valores de ciudadanía, como la equidad de acceso, la inclusión de todos los usuarios y el cumplimiento de estándares éticos?",
            "Permite que DJs jóvenes y técnicos independientes que recién comienzan accedan gratis a una herramienta que antes solo tenían grandes productoras, fomentando la seguridad laboral y el respeto a las normas eléctricas chilenas."
        ),
        (
            "¿Qué métricas o criterios deberíamos considerar para evaluar la efectividad y la sostenibilidad de la solución de software en el tiempo? ¿Cómo podemos incorporar la retroalimentación del usuario para futuras mejoras?",
            "Métricas clave:\n"
            "1. Planificación en menos de 5 minutos.\n"
            "2. Cero cables tirantes o sueltos sin encintar en terreno.\n"
            "3. Cero automáticos cortados por sobrecarga.\n"
            "4. Que el PDF descargado se abra y se lea perfecto en el celular en modo avión.\n"
            "El sistema permite guardar los salones para reutilizar las medidas en futuros eventos."
        ),
        (
            "¿Cuáles son las principales problemáticas que enfrenta el área de estudio?",
            "El cálculo 'al ojo', cables sueltos en el piso sin fijar, saturación de un solo enchufe existiendo otros disponibles en el local, y la falta de internet móvil en parcelas de agrado."
        ),
        (
            "¿Qué información de la cultura institucional del cliente y reglamentaria es relevante para el proyecto?",
            "El técnico necesita un lenguaje simple y directo (sin jerga matemática que maree) y cumplir las normas de la SEC: Pliego RIC 03 (caída de voltaje no mayor al 3%) y Pliego RIC 10 (cables flexibles de uso rudo para eventos)."
        ),
        (
            "¿Cuáles son los objetivos específicos del levantamiento de datos en las instalaciones propias del cliente?",
            "Registrar las medidas de los salones más comunes, contar los rollos de cinta gaffer que usan al mes y medir cuántos metros de cable se necesitan para llegar a cada esquina del escenario."
        ),
        (
            "¿Qué recursos, tiempo y metodologías se necesitan para el levantamiento de datos?",
            "Recursos: Huincha de medir, fichas de los parlantes y registro de montajes anteriores. Tiempo: 12 horas en 2 semanas. Metodología: Levantamiento empírico y entrevistas directas."
        ),
        (
            "¿Cómo se levantará y analizará la información del proyecto? ¿De qué manera los datos obtenidos cumplirán con la normativa vigente?",
            "Se ingresan las medidas y consumos en el motor de cálculo de STAGE PLAN, que compara cada alargador con las fórmulas de caída de voltaje y ampacidad que exige la SEC en los pliegos RIC 03 y RIC 10."
        ),
        (
            "¿Qué propuestas de mejora se pueden desarrollar a partir de la información recopilada?",
            "Construir STAGE PLAN v3.2: un sistema que calcula el metraje de cable por equipo, reparte la carga entre los enchufes disponibles, calcula cuánta cinta gris llevar para el piso y entrega un PDF para usar sin internet."
        ),
    ]

    for q, a in preguntas_respuestas:
        p_q = t2_cell.add_paragraph()
        p_q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_q = p_q.add_run(f"• {q}")
        r_q.bold = True
        r_q.font.name = 'Arial'
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = COLOR_Q

        p_a = t2_cell.add_paragraph()
        p_a.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_a = p_a.add_run(f"  R: {a}\n")
        r_a.font.name = 'Arial'
        r_a.font.size = Pt(9.0)
        r_a.font.color.rgb = COLOR_ANSWER

    # 2. TABLA 3: 5 PORQUÉS
    t3_cell = doc.tables[3].rows[0].cells[0]
    for p in t3_cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    p_sp_title = t3_cell.add_paragraph()
    p_sp_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_sp = p_sp_title.add_run("\n======================================================\nAPLICACIÓN DE LOS 5 PORQUÉS AL CASO DE STAGE PLAN (v3.2):\n======================================================")
    r_sp.bold = True
    r_sp.font.size = Pt(10.0)
    r_sp.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    cinco_porques_proyecto = [
        ("Problema del negocio:", "En los eventos en parcelas de DISTORSIONCL SPA, se corta la luz a mitad de fiesta, los amplificadores se apagan o los invitados se tropiezan con cables sueltos en el piso."),
        ("1. ¿Por qué se corta la luz y la gente se tropieza?", "Porque enchufan todo a un solo enchufe casero de 10A y cruzan cables por el medio de la pista de baile sin fijarlos con cinta adhesiva al suelo."),
        ("2. ¿Por qué sobrecargan un solo enchufe y dejan cables sueltos?", "Porque el técnico conecta todo al enchufe que le queda más cerca de la cabina sin revisar si hay otros enchufes en el salón y no calcula cuánta cinta gris debe llevar en la camioneta."),
        ("3. ¿Por qué no reparte los enchufes ni lleva suficiente cinta?", "Porque planifica el montaje 'al ojo' y por apuro minutos antes de empezar, sin saber la distancia exacta a cada enchufe ni los metros de cable que van por el piso."),
        ("4. ¿Por qué no calcula las distancias y los enchufes antes de salir?", "Porque no cuenta con una herramienta en el celular que le calcule el ruteo de cables y porque en las parcelas no hay señal de internet para buscar tablas técnicas."),
        ("5. ¿Por qué no existía una herramienta adaptada a su trabajo?", "Porque los programas existentes son para ingenieros eléctricos de grandes industrias (difíciles y caros) o páginas web que no funcionan cuando no hay señal de celular."),
        ("Causa Raíz Identificada:", "La falta de una aplicación web simple que se use antes de salir (con internet) y que calcule inteligentemente a qué enchufe conectar cada equipo, cuántos metros de cable y cuántos rollos de cinta gris se necesitan, generando un reporte PDF listo para usar en terreno en modo avión.")
    ]

    for item, desc in cinco_porques_proyecto:
        p_item = t3_cell.add_paragraph()
        p_item.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r1 = p_item.add_run(f"{item} ")
        r1.bold = True
        r1.font.size = Pt(9.5)
        r2 = p_item.add_run(desc)
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = COLOR_ANSWER

    # 3. TABLA 5 ROW 1: DESARROLLO DE ACTIVIDADES
    t5_row1_cell = doc.tables[5].rows[1].cells[0]
    t5_row1_cell.text = ""

    p_dev_title = t5_row1_cell.add_paragraph()
    p_dev_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_dev = p_dev_title.add_run("DESARROLLO FORMAL DE LAS 4 ACTIVIDADES DEL DIAGNÓSTICO (UNIDAD 1 - v3.2)\n")
    r_dev.bold = True
    r_dev.font.size = Pt(11.0)
    r_dev.font.color.rgb = COLOR_TITLE

    actividades_desarrolladas = [
        (
            "Actividad 1: Antecedentes y Leyes de Chile que Aplican al Proyecto",
            "• ¿Cómo opera el cliente?: DISTORSIONCL SPA realiza montajes de sonido e iluminación en salones y parcelas de Santiago. En el 65% de los casos operan en parcelas con enchufes de pared de 10A o generadores portátiles a bencina.\n"
            "• Regla de la SEC RIC N° 03 (Caída de voltaje): Exige que en los alargadores no se pierda más del 3% del voltaje (en 220V, máximo 6.6 Volts). STAGE PLAN calcula el grosor del cable por equipo para que los parlantes no se apaguen.\n"
            "• Regla de la SEC RIC N° 10 (Cables seguros para eventos): Exige cables flexibles de goma de uso rudo y protecciones termomagnéticas coordinadas.\n"
            "• Prevención de accidentes físicos: Fijación obligatoria de cables al suelo con cinta adhesiva industrial gris (gaffer tape) en áreas transitadas.\n"
            "• Privacidad de datos (Ley 19.628 y 21.719): Los nombres de los clientes y las ubicaciones de los eventos se guardan protegidos con clave y aislamiento por usuario."
        ),
        (
            "Actividad 2: Levantamiento de Requerimientos (Funcionales y No Funcionales)",
            "• Cómo se levantó la información: Entrevistas con el técnico jefe de DISTORSIONCL SPA y análisis de 5 eventos con fallas de cableado y sobrecargas.\n"
            "• Requerimientos Funcionales (Lo que hace el sistema):\n"
            "  - RF01: Ingreso seguro con usuario y clave encriptada.\n"
            "  - RF02: Registro de medidas del salón y ubicación de 1 o varios enchufes.\n"
            "  - RF03: Ubicación de los parlantes, cabina DJ y luces en el plano del salón.\n"
            "  - RF04: Ruteo inteligente: conecta cada equipo al enchufe más cercano disponible; si hay uno solo, calcula todo hacia ese punto; y si supera los 25m o el 90% de uso, sugiere instalar una toma adicional.\n"
            "  - RF05: Cálculo de cinta gris para piso: mide los cables que cruzan el suelo y entrega la cantidad exacta de rollos de 50 metros.\n"
            "  - RF06: Estudio de sonido (SPL) con aviso de parlantes de refuerzo (delay) y retardo en milisegundos.\n"
            "  - RF07: Descarga de reporte PDF para llevar al evento en modo avión.\n"
            "• Requerimientos No Funcionales (Cómo se comporta el sistema):\n"
            "  - RNF01: Velocidad instantánea (cálculo en menos de 50 milisegundos).\n"
            "  - RNF02: Seguridad anti-IDOR: nadie puede ver los salones de otra productora.\n"
            "  - RNF03: Funciona 100% en modo avión sin consumir internet.\n"
            "  - RNF04: 28 pruebas automáticas con Vitest (100% aprobadas).\n"
            "  - RNF05: Adaptado a la pantalla vertical de cualquier celular."
        ),
        (
            "Actividad 3: Priorización del Proyecto (Técnica MoSCoW)",
            "• Must Have (Obligatorio en el MVP):\n"
            "  - HU01: Login seguro.\n"
            "  - HU02: Cálculo de cable por equipo y ruteo inteligente multi-enchufe.\n"
            "  - HU03: Alerta roja de sobrecarga si el enchufe o generador no aguantan.\n"
            "• Should Have (Muy importante para el técnico):\n"
            "  - HU04: Cálculo de rollos de cinta adhesiva gris para piso (evitar tropiezos) e inventario de atriles.\n"
            "  - HU05: Sugerencia de nuevos enchufes si la distancia supera 25m y cálculo de parlantes de refuerzo (delay).\n"
            "  - HU06: Reporte PDF descargable para terreno.\n"
            "• Could Have (Mejoras futuras): Compartir reportes por enlace temporal con el dueño del salón.\n"
            "• Won't Have (Fuera de alcance): Sincronización offline compleja y bandas en vivo (para no desenfocar el proyecto de titulación)."
        ),
        (
            "Actividad 4: Tecnologías Utilizadas y Seguridad TI",
            "• Lenguaje: TypeScript en todo el proyecto (Node.js en servidor y Vue 3 en pantallas), compartiendo las fórmulas matemáticas en un solo paquete (@stageplan/shared) para no duplicar código.\n"
            "• Base de datos: PostgreSQL con Prisma ORM, que protege los datos contra ataques y hackers.\n"
            "• Seguridad Anti-IDOR: Cada consulta en la base de datos verifica que el usuario sea el dueño real del salón; si no lo es, se le bloquea el acceso con error 404/403.\n"
            "• Compromiso ético y físico: Prevención de caídas de personas con el cálculo de cinta gris para piso y aviso obligatorio de la SEC en cada reporte emitido."
        ),
    ]

    for tit, cont in actividades_desarrolladas:
        p_act = t5_row1_cell.add_paragraph()
        p_act.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_act_t = p_act.add_run(f"\n{tit}\n")
        r_act_t.bold = True
        r_act_t.font.size = Pt(10.0)
        r_act_t.font.color.rgb = COLOR_TITLE

        r_act_c = p_act.add_run(cont)
        r_act_c.font.size = Pt(9.0)
        r_act_c.font.color.rgb = COLOR_ANSWER

    doc.save('TIHV43_GUÍA_ABPRO_U1.docx')
    print("TIHV43_GUÍA_ABPRO_U1.docx updated to v3.2 successfully.")

if __name__ == '__main__':
    update_guia_v32()

