import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def refine_guia():
    doc = docx.Document('TIHV43_GUÍA_ABPRO_U1.bak.docx')

    COLOR_ANSWER = RGBColor(0x1F, 0x49, 0x7D)
    COLOR_Q = RGBColor(0x26, 0x26, 0x26)
    COLOR_TITLE = RGBColor(0x1F, 0x49, 0x7D)
    COLOR_BODY = RGBColor(0x33, 0x33, 0x33)

    # 1. TABLA 2: PREGUNTAS ORIENTADORAS
    t2_cell = doc.tables[2].rows[0].cells[0]
    t2_cell.paragraphs[0].text = "Preguntas orientadoras para el diagnóstico — Respuestas explicadas con ejemplos simples para el caso DISTORSIONCL SPA:"
    t2_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    for p in t2_cell.paragraphs[1:]:
        p.text = ""

    preguntas_respuestas = [
        (
            "¿Cuáles son las principales necesidades del negocio que requieren una solución de software y cómo afectan a las operaciones, a los empleados y a los clientes de la empresa?",
            "La empresa DISTORSIONCL SPA tiene 3 problemas principales porque hoy calcula todo 'a ojo':\n"
            "1. Cortes de luz en plena fiesta: Conectan los equipos a cualquier enchufe de 10 Amperes de la casa o parcela, el enchufe se sobrecalienta y se corta la luz.\n"
            "2. Caídas de voltaje en alargadores largos: Al usar cables delgados de más de 30 metros, el voltaje cae de 220V a menos de 200V y los amplificadores se apagan solos o se queman.\n"
            "3. Sonido desparejo: La gente que está cerca de los parlantes queda aturdida por el volumen excesivo, mientras que en el fondo de la pista la música casi no se escucha.\n"
            "Esto perjudica a los empleados (trabajan estresados apagando incendios), al negocio (pierde clientes) y a los novios o festejados (su fiesta se arruina)."
        ),
        (
            "¿Qué tipos de software o tecnología ya utiliza la empresa y cómo se integran en sus procesos actuales? ¿Existen limitaciones o brechas que estas herramientas no cubren?",
            "Hoy usan planillas de Excel básicas y mensajes de WhatsApp. Las fallas de esto son:\n"
            "- Excel no avisa si el cable cumple la norma chilena de la SEC.\n"
            "- No calcula automáticamente si un generador a bencina va a aguantar la carga.\n"
            "- Y lo peor de todo: cuando el técnico llega a la parcela donde no hay señal de celular (4G/5G), no puede abrir nada en la nube ni consultar tablas en internet."
        ),
        (
            "¿Cómo podríamos aplicar metodologías emergentes, como Design Thinking, DevOps o Agile, para desarrollar una solución adaptada a las necesidades del negocio?",
            "Usamos una forma ágil y simple de trabajar: Kanban con pruebas automáticas (TDD).\n"
            "En un tablero visual vemos qué tareas estamos haciendo (máximo 2 a la vez para no perder el tiempo en reuniones eternas de Scrum). Además, antes de hacer las pantallas, programamos y probamos las fórmulas matemáticas para que el grosor del cable y las alertas de los generadores no fallen nunca en terreno."
        ),
        (
            "¿De qué manera el diagnóstico de necesidades tecnológicas puede beneficiarse de técnicas como entrevistas, encuestas o análisis de datos de usuario? ¿Qué información clave debería recogerse para fundamentar una propuesta de solución?",
            "Conversamos directamente con el técnico en terreno y revisamos 5 eventos reales que salieron mal. Descubrimos datos clave:\n"
            "- Casi siempre usan alargadores de más de 30 metros.\n"
            "- La mayoría de los enchufes de parcelas son de 10 Amperes (aguantan poco más de 2.000 Watts).\n"
            "- Muchos confunden los kVA con los Watts reales de los generadores (por ejemplo, creen que un generador de 5 kVA entrega 5.000W, cuando en realidad entrega 4.000W utilizables)."
        ),
        (
            "¿Cuáles son los posibles impactos éticos de la solución de software en los empleados, los clientes y otros actores relacionados con el negocio? ¿Cómo se puede asegurar la transparencia y el respeto a la privacidad en el diseño?",
            "El mayor impacto ético es cuidar la vida y la seguridad de las personas. La electricidad mal calculada produce incendios o electrocuciones.\n"
            "Para ser totalmente transparentes y responsables, el sistema muestra en pantalla y en cada PDF un aviso legal obligatorio de la SEC: aclara que el software es una guía de ayuda para preparar el evento, pero que no reemplaza a un electricista autorizado.\n"
            "En cuanto a privacidad, los nombres de los clientes y las direcciones de las parcelas están guardados bajo llave digital (cifrado y anti-IDOR) según la ley chilena (Ley 19.628)."
        ),
        (
            "¿De qué modo la solución de software propuesta puede promover valores de ciudadanía, como la equidad de acceso, la inclusión de todos los usuarios y el cumplimiento de estándares éticos?",
            "Permite que un DJ o técnico independiente que está empezando tenga acceso gratis a cálculos de ingeniería que antes solo tenían las grandes productoras multinacionales, fomentando el trabajo seguro y el respeto a las normas en todo el gremio."
        ),
        (
            "¿Qué métricas o criterios deberíamos considerar para evaluar la efectividad y la sostenibilidad de la solución de software en el tiempo? ¿Cómo podemos incorporar la retroalimentación del usuario para futuras mejoras?",
            "Criterios de éxito fáciles de medir:\n"
            "1. Que el técnico arme su evento en la web en menos de 5 minutos.\n"
            "2. Cero cortes de luz o parlantes quemados en los eventos planificados.\n"
            "3. Que el PDF descargado se abra y se lea perfecto en el celular puesto en modo avión.\n"
            "El técnico puede guardar sus salones favoritos para reutilizarlos en futuros eventos con solo un clic."
        ),
        (
            "¿Cuáles son las principales problemáticas que enfrenta el área de estudio?",
            "El cálculo 'a ojo', la falta de herramientas adaptadas a los enchufes y normas de Chile, y la falta de señal de internet en los lugares de eventos campestres."
        ),
        (
            "¿Qué información de la cultura institucional del cliente y reglamentaria es relevante para el proyecto?",
            "El cliente necesita algo rápido y fácil en el celular, sin palabras raras de ingeniería. A nivel de leyes, las normas obligatorias de la SEC: el Pliego RIC 03 (que no se caiga más del 3% del voltaje en los cables) y el Pliego RIC 10 (cables flexibles de uso rudo para eventos)."
        ),
        (
            "¿Cuáles son los objetivos específicos del levantamiento de datos en las instalaciones propias del cliente?",
            "Contar cuántos parlantes, cables, luces y trípodes tiene la empresa en su bodega, y medir con un tester cuánto consumen realmente cuando están sonando fuerte."
        ),
        (
            "¿Qué recursos, tiempo y metodologías se necesitan para el levantamiento de datos?",
            "Recursos: Fichas de los parlantes, un tester para medir corriente y fotos de los eventos. Tiempo: 12 horas en 2 semanas. Método: Entrevistas directas y revisión de eventos pasados."
        ),
        (
            "¿Cómo se levantará y analizará la información del proyecto? ¿De qué manera los datos obtenidos cumplirán con la normativa vigente?",
            "Se ordenaron en una tabla técnica donde cada enchufe y cable se compara contra las fórmulas que exige la SEC en los pliegos RIC 03 y RIC 10."
        ),
        (
            "¿Qué propuestas de mejora se pueden desarrollar a partir de la información recopilada?",
            "Crear STAGE PLAN: un sistema web donde el técnico pone las medidas y equipos, ve un semáforo de peligro y un plano 2D, y se descarga un PDF para trabajar tranquilo en terreno sin internet."
        ),
    ]

    for q, a in preguntas_respuestas:
        p_q = t2_cell.add_paragraph()
        p_q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_q = p_q.add_run(f"• {q}")
        r_q.bold = True
        r_q.font.name = "Arial"
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = COLOR_Q

        p_a = t2_cell.add_paragraph()
        p_a.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_a = p_a.add_run(f"  R: {a}\n")
        r_a.font.name = "Arial"
        r_a.font.size = Pt(9.0)
        r_a.font.color.rgb = COLOR_ANSWER

    # 2. TABLA 3: 5 PORQUÉS
    t3_cell = doc.tables[3].rows[0].cells[0]
    for p in t3_cell.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    p_sp_title = t3_cell.add_paragraph()
    p_sp_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_sp = p_sp_title.add_run("\n======================================================\nAPLICACIÓN DE LOS 5 PORQUÉS AL CASO DE STAGE PLAN (EXPLICADO SIMPLE):\n======================================================")
    r_sp.bold = True
    r_sp.font.size = Pt(10.0)
    r_sp.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    cinco_porques_proyecto = [
        ("Problema del negocio:", "En los eventos en parcelas de DISTORSIONCL SPA, se corta la luz a mitad de fiesta o los amplificadores de sonido se apagan solos."),
        ("1. ¿Por qué se apagan los amplificadores o se corta la luz?", "Porque el enchufe o el generador se sobrecalientan y el voltaje baja demasiado en la punta del alargador (cae a menos de 200V)."),
        ("2. ¿Por qué se sobrecalienta el enchufe y se cae el voltaje?", "Porque el técnico enchufa todo a un solo enchufe común de 10 Amperes y usa alargadores largos con cables muy delgados (1.5 mm²)."),
        ("3. ¿Por qué el técnico usa cables delgados y sobrecarga los enchufes?", "Porque calcula todo 'al ojo' y por intuición minutos antes de empezar el evento, sin calcular cuánta corriente van a chupar los equipos."),
        ("4. ¿Por qué no calcula la corriente y el voltaje antes de armar?", "Porque no tiene una herramienta rápida en el celular que le haga el cálculo y porque en las parcelas no hay señal de internet para buscar información."),
        ("5. ¿Por qué no existía una herramienta adaptada a su realidad?", "Porque los programas que existen son de escritorio para ingenieros eléctricos de grandes industrias (muy caros y difíciles de usar) o páginas web que no funcionan cuando no hay señal de celular."),
        ("Causa Raíz:", "Falta una aplicación web simple que se use antes de salir (con internet) y que genere un informe en PDF descargable con todos los datos y listas para usar en terreno en modo avión.")
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
    t5_row1_cell.text = "" # limpiar
    
    p_dev_title = t5_row1_cell.add_paragraph()
    p_dev_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_dev = p_dev_title.add_run("DESARROLLO FORMAL DE LAS 4 ACTIVIDADES DEL DIAGNÓSTICO (UNIDAD 1)\n")
    r_dev.bold = True
    r_dev.font.size = Pt(11.0)
    r_dev.font.color.rgb = COLOR_TITLE

    actividades_desarrolladas = [
        (
            "Actividad 1: Antecedentes y Leyes de Chile que Aplican al Proyecto",
            "• ¿Cómo trabaja el cliente hoy?: DISTORSIONCL SPA hace eventos en parcelas y salones de Santiago con parlantes activos, etapas de potencia, mesas de DJ y luces LED. El 65% de sus eventos son en parcelas con enchufes caseros de 10A o generadores pequeños de 3 a 8 kVA.\n"
            "• Regla de la SEC RIC N° 03 (Caída de voltaje): Exige que en los cables no se pierda más del 3% del voltaje (en 220V, no se pueden perder más de 6.6 Volts). STAGE PLAN calcula esto para que los amplificadores no se apaguen.\n"
            "• Regla de la SEC RIC N° 10 (Cables seguros para eventos): Exige usar cables flexibles de goma resistentes (servicio móvil) y automáticos bien dimensionados.\n"
            "• Ley chilena de privacidad (Ley 19.628 y 21.719): Los nombres de los clientes y las direcciones de las parcelas son privados y se guardan con clave protegida."
        ),
        (
            "Actividad 2: Levantamiento de Requerimientos (Funcionales y No Funcionales)",
            "• Cómo se levantó la información: Entrevistas con el técnico de sonido y revisión de 5 montajes reales donde hubo problemas eléctricos.\n"
            "• Lo que el sistema DEBE hacer (Requerimientos Funcionales):\n"
            "  - RF01: Ingreso con usuario y clave segura.\n"
            "  - RF02: Guardar las medidas del salón y la distancia al enchufe.\n"
            "  - RF03: Elegir los parlantes, luces y si se usa enchufe o generador.\n"
            "  - RF04: Calcular cables, semáforo de sobrecarga y decibeles de sonido.\n"
            "  - RF05: Mostrar un plano 2D visual de la pista en la pantalla.\n"
            "  - RF06: Descargar el informe en PDF para usar sin internet en terreno.\n"
            "  - RF07: Guardar el historial de eventos anteriores.\n"
            "• Cómo DEBE comportarse el sistema (Requerimientos No Funcionales):\n"
            "  - RNF01: Cálculo instantáneo (menos de medio segundo).\n"
            "  - RNF02: Seguridad total: nadie puede ver los salones de otro usuario (anti-IDOR).\n"
            "  - RNF03: El PDF funciona 100% en modo avión.\n"
            "  - RNF04: Pruebas matemáticas automáticas con más del 90% de cobertura (cero errores).\n"
            "  - RNF05: Pantalla adaptable al celular vertical (Mobile-First)."
        ),
        (
            "Actividad 3: Priorización del Proyecto (Técnica MoSCoW)",
            "• Must Have (Lo obligatorio que sí o sí debe funcionar en la entrega):\n"
            "  - HU01: Login seguro.\n"
            "  - HU02: Cálculo del cable y caída de voltaje por norma SEC.\n"
            "  - HU03: Alerta roja de sobrecarga si el enchufe o generador no aguantan.\n"
            "• Should Have (Muy importante para el técnico):\n"
            "  - HU04: Lista de atriles (bajos al suelo obligatorios) y zapatillas eléctricas con enchufes de sobra.\n"
            "  - HU05: Aviso de sonido si se necesita parlante de refuerzo (delay) y plano 2D.\n"
            "  - HU06: Descarga del informe en PDF en el celular.\n"
            "• Could Have (Mejoras para el futuro): Guardar enlaces para compartir con clientes.\n"
            "• Won't Have (Fuera de alcance): Sincronización offline complicada y bandas en vivo (para no desenfocar el proyecto)."
        ),
        (
            "Actividad 4: Tecnologías Utilizadas y Seguridad TI",
            "• Lenguaje: TypeScript en todo el proyecto (Node.js en servidor y Vue 3 en pantallas), compartiendo las fórmulas matemáticas en un solo paquete (@stageplan/shared) para no duplicar código.\n"
            "• Base de datos: PostgreSQL con Prisma ORM, que protege los datos contra inyecciones SQL y hackers.\n"
            "• Seguridad Anti-IDOR: Cada consulta en la base de datos verifica que el usuario sea el dueño real del salón; si no lo es, se le bloquea el acceso con error 404/403.\n"
            "• Compromiso ético: Aviso obligatorio en pantalla y en cada PDF de que el software es una guía de ayuda previa y no reemplaza a un instalador eléctrico certificado por la SEC."
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
    print("TIHV43_GUÍA_ABPRO_U1.docx refined successfully.")

if __name__ == '__main__':
    refine_guia()

