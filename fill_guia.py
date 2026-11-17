import docx
from docx.shared import Pt, RGBColor

def fill_guia():
    doc = docx.Document('TIHV43_GUÍA_ABPRO_U1.bak.docx')

    # Color para las respuestas insertadas: azul oscuro formal / texto legible que armoniza perfectamente
    COLOR_ANSWER = RGBColor(0x1F, 0x49, 0x7D)
    COLOR_Q = RGBColor(0x26, 0x26, 0x26)

    # 1. PARTE 1: PREGUNTAS ORIENTADORAS (Tabla 2)
    # Reemplazaremos el contenido de la celda de la Tabla 2 manteniendo la pregunta y añadiendo la respuesta detallada
    t2_cell = doc.tables[2].rows[0].cells[0]
    
    # Limpiamos párrafos existentes de t2_cell
    # Dejamos el primer párrafo como introducción
    t2_cell.paragraphs[0].text = "Preguntas orientadoras para el diagnóstico del problema informático — Respuestas oficiales del proyecto STAGE PLAN (DISTORSIONCL SPA):"
    
    # Limpiamos el resto
    for p in t2_cell.paragraphs[1:]:
        p.text = ""

    preguntas_respuestas = [
        (
            "¿Cuáles son las principales necesidades del negocio que requieren una solución de software y cómo afectan a las operaciones, a los empleados y a los clientes de la empresa?",
            "El cliente DISTORSIONCL SPA enfrenta tres problemáticas críticas derivadas del cálculo empírico (\"al ojo\") en la pre-producción de eventos técnicos y DJs: (1) Caídas de tensión severas en alargadores extensos en recintos de eventos y parcelas; (2) Cortes intempestivos de energía por sobrecarga en disyuntores de 10A o generadores portátiles mal dimensionados; y (3) Fallas de inteligibilidad y cobertura acústica deficiente en el fondo de la pista. Estas fallas paralizan eventos en vivo, dañan el prestigio de la productora y generan costos imprevistos por reposición de amplificadores y transductores quemados."
        ),
        (
            "¿Qué tipos de software o tecnología ya utiliza la empresa y cómo se integran en sus procesos actuales? ¿Existen limitaciones o brechas que estas herramientas no cubren?",
            "Actualmente la empresa gestiona sus requerimientos mediante hojas de cálculo aisladas (Excel) y mensajes informales por WhatsApp. Las brechas principales son: nula validación de la normativa chilena de la SEC (Pliegos RIC N° 03 y RIC N° 10), inexistencia de alertas automáticas por sobrecarga de generadores (kVA vs. kW), falta de trazabilidad algorítmica y, fundamentalmente, la imposibilidad de operar en terreno cuando se asiste a parcelas sin conectividad a internet móvil."
        ),
        (
            "¿Cómo podríamos aplicar metodologías emergentes, como Design Thinking, DevOps o Agile, para desarrollar una solución adaptada a las necesidades del negocio?",
            "Se implementa un enfoque ágil adaptado que combina Kanban (con límite de trabajo en curso WIP=2) y Test-Driven Development (TDD con Vitest). La metodología permite iterar de manera temprana y continua con el operador técnico de DISTORSIONCL SPA, asegurando que cada fórmula matemática de caída de tensión y acústica cuente con pruebas automatizadas que garanticen cero errores antes de pasar a producción."
        ),
        (
            "¿De qué manera el diagnóstico de necesidades tecnológicas puede beneficiarse de técnicas como entrevistas, encuestas o análisis de datos de usuario? ¿Qué información clave debería recogerse para fundamentar una propuesta de solución?",
            "Mediante entrevistas semi-estructuradas al técnico de sonido y la observación directa de montajes reales, se recopiló un histórico de 3 a 5 eventos con fallas recurrentes. Los datos clave levantados fueron: metrajes de cable utilizados, potencias RMS de cajas acústicas, impedancias nominales, capacidad de los empalmes eléctricos y la topología física del público respecto a los parlantes."
        ),
        (
            "¿Cuáles son los posibles impactos éticos de la solución de software en los empleados, los clientes y otros actores relacionados con el negocio? ¿Cómo se puede asegurar la transparencia y el respeto a la privacidad en el diseño?",
            "El impacto ético fundamental es la seguridad de las personas: una falla de cálculo eléctrico en un evento masivo puede causar incendios por efecto Joule o electrocuciones. Para asegurar la transparencia y la ética profesional, el sistema incorpora obligatoriamente en pantalla y en cada reporte PDF un Disclaimer Normativo que estipula que el software es una herramienta de estimación de pre-producción que no sustituye la certificación legal de un instalador eléctrico autorizado por la SEC. En cuanto a privacidad, los datos de los recintos y clientes se resguardan bajo cifrado y aislamiento estricto por usuario (anti-IDOR) conforme a la Ley N° 19.628 y 21.719."
        ),
        (
            "¿De qué modo la solución de software propuesta puede promover valores de ciudadanía, como la equidad de acceso, la inclusión de todos los usuarios y el cumplimiento de estándares éticos?",
            "Promueve la equidad al permitir que pequeños operadores independientes y DJs accedan a cálculos de ingeniería eléctrica y acústica de alta precisión sin incurrir en software privativo de alto costo. Asimismo, fomenta la cultura de cumplimiento normativo y prevención de riesgos laborales en el gremio de eventos técnicos."
        ),
        (
            "¿Qué métricas o criterios deberíamos considerar para evaluar la efectividad y la sostenibilidad de la solución de software en el tiempo? ¿Cómo podemos incorporar la retroalimentación del usuario para futuras mejoras?",
            "Métricas clave: reducción del tiempo de pre-producción a menos de 5 minutos (RNF05), cero caídas de tensión por encima del 3% en terreno, tasa de pruebas unitarias aprobadas >= 90% (RNF08), y legibilidad 100% offline del PDF en modo avión (RNF10). La retroalimentación se incorpora mediante la funcionalidad de duplicar y ajustar configuraciones pasadas en el historial."
        ),
        (
            "¿Cuáles son las principales problemáticas que enfrenta el área de estudio?",
            "El dimensionamiento artesanal y sin respaldo ingenieril de los montajes de sonido e iluminación, la falta de herramientas de cálculo adaptadas a la normativa chilena de la SEC, y la carencia de señal 4G/5G en recintos de eventos y parcelas que invalida el uso de sistemas web convencionales dependientes de la nube en terreno."
        ),
        (
            "¿Qué información de la cultura institucional del cliente y reglamentaria es relevante para el proyecto?",
            "La necesidad de rapidez y simplicidad en la toma de decisiones del operador técnico, y el marco reglamentario obligatorio establecido por la SEC en el Pliego Técnico RIC N° 03 (caída de tensión máxima admisible del 3% en alimentadores) y RIC N° 10 (protecciones diferenciales y cordones flexibles de servicio pesado)."
        ),
        (
            "¿Cuáles son los objetivos específicos del levantamiento de datos en las instalaciones propias del cliente?",
            "Registrar el inventario real de cajas acústicas (activas y pasivas), potencias nominales de amplificadores, calibres y longitudes de cables existentes, y verificar los consumos reales mediante pinza amperimétrica en ensayos de sonido."
        ),
        (
            "¿Qué recursos, tiempo y metodologías se necesitan para el levantamiento de datos?",
            "Recursos: fichas técnicas de fabricantes, multímetro digital, pinza amperimétrica y registro fotográfico de montajes. Tiempo: 12 horas cronológicas distribuidas en 2 semanas. Metodología: Levantamiento empírico-documental y entrevistas semi-estructuradas."
        ),
        (
            "¿Cómo se levantará y analizará la información del proyecto? ¿De qué manera los datos obtenidos cumplirán con la normativa vigente?",
            "Se consolidan en una matriz técnica de requerimientos donde cada variable eléctrica (Watts, Volts, Amperios, metros) se procesa bajo las fórmulas oficiales del RIC N° 03 (S = 2*rho*L*I / dV) y las tablas de ampacidad de conductores de servicio móvil del RIC N° 10."
        ),
        (
            "¿Qué propuestas de mejora se pueden desarrollar a partir de la información recopilada?",
            "Desarrollar el paquete @stageplan/shared con el módulo calc-engine, crear el visualizador Layout 2D en SVG reactivo y automatizar la generación del Reporte Operativo autónomo en PDF con protocolo de encendido seguro y checklist de materiales."
        ),
    ]

    for q, a in preguntas_respuestas:
        p_q = t2_cell.add_paragraph()
        r_q = p_q.add_run(f"• {q}")
        r_q.bold = True
        r_q.font.name = "Arial"
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = COLOR_Q

        p_a = t2_cell.add_paragraph()
        r_a = p_a.add_run(f"  R: {a}\n")
        r_a.font.name = "Arial"
        r_a.font.size = Pt(9.0)
        r_a.font.color.rgb = COLOR_ANSWER

    # 2. PARTE 2: TECNICA DE LOS 5 PORQUÉS (Tabla 3)
    # Se agregan al final de la celda los 5 Porqués específicos del proyecto STAGE PLAN
    t3_cell = doc.tables[3].rows[0].cells[0]
    p_sp_title = t3_cell.add_paragraph()
    r_sp = p_sp_title.add_run("\n======================================================\nAPLICACIÓN DE LA TÉCNICA DE LOS 5 PORQUÉS AL PROYECTO STAGE PLAN:\n======================================================")
    r_sp.bold = True
    r_sp.font.size = Pt(10.0)
    r_sp.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)

    cinco_porques_proyecto = [
        ("Problema Inicial del Negocio:", "En los montajes de eventos en parcelas de DISTORSIONCL SPA, ocurren cortes de energía imprevistos y caídas de tensión que apagan los amplificadores de sonido."),
        ("1. ¿Por qué se apagan los amplificadores o se corta la energía?", "Porque el circuito eléctrico o el generador portátil se sobrecarga térmicamente y el voltaje en el extremo del alargador cae por debajo de los 200V."),
        ("2. ¿Por qué cae el voltaje y se sobrecarga el circuito?", "Porque el operador técnico conecta todo el equipamiento a un solo enchufe domiciliario de 10A y utiliza alargadores de cable muy delgados (1.5 mm²) de más de 30 metros de longitud."),
        ("3. ¿Por qué el técnico utiliza calibres inadecuados y sobrecarga los enchufes?", "Porque el dimensionamiento de los cables, potencias y circuitos se realiza de forma empírica ('a ojo') minutos antes del evento, sin calcular la caída de tensión ni la corriente de diseño."),
        ("4. ¿Por qué no se calculan previamente las variables eléctricas y acústicas?", "Porque el operador no cuenta con una herramienta digital ágil que automatice la normativa SEC en la pre-producción y carece de conexión a internet en la parcela para consultar tablas técnicas."),
        ("5. ¿Por qué no existe una herramienta adaptada a su flujo de trabajo?", "Porque las soluciones de software existentes son de diseño eléctrico industrial de escritorio (complejas y costosas) o aplicaciones web en la nube que quedan inutilizables sin cobertura móvil en terreno."),
        ("Causa Raíz Identificada:", "La carencia de un sistema de pre-producción automatizado (Online-First) con base en la normativa SEC (RIC 03/10) que genere un Reporte Operativo autónomo y descargable en PDF, legible en terreno sin conexión a internet.")
    ]

    for item, desc in cinco_porques_proyecto:
        p_item = t3_cell.add_paragraph()
        r1 = p_item.add_run(f"{item} ")
        r1.bold = True
        r1.font.size = Pt(9.5)
        r2 = p_item.add_run(desc)
        r2.font.size = Pt(9.0)
        r2.font.color.rgb = COLOR_ANSWER

    # 3. ACTIVIDADES FORMATIVAS Y EVALUACION SUMATIVA (Tabla 5)
    # Tabla 5 contiene las actividades 1 a 4. Row 1 está vacía en la plantilla.
    # Llenaremos Row 1 con el informe de diagnóstico y desarrollo formal del proyecto
    t5_row1_cell = doc.tables[5].rows[1].cells[0]
    
    p_dev_title = t5_row1_cell.add_paragraph()
    r_dev = p_dev_title.add_run("DESARROLLO FORMAL DE LAS ACTIVIDADES DE DIAGNÓSTICO (UNIDAD 1 - STAGE PLAN)\n")
    r_dev.bold = True
    r_dev.font.size = Pt(11.0)
    r_dev.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    actividades_desarrolladas = [
        (
            "Actividad 1: Identificación de Antecedentes y Marco Normativo Vigente",
            "• Antecedentes Tecnológicos: La productora DISTORSIONCL SPA opera en eventos en la Región Metropolitana con equipamiento electroacústico (cajas activas, etapas de potencia clase D/AB, consolas digitales e iluminación LED DMX). El 65% de sus eventos se realizan en recintos aislados o parcelas de agrado con empalmes monofásicos limitados (10A o 16A) o grupos electrógenos portátiles a gasolina (3 a 8 kVA).\n"
            "• Normativa SEC - Pliego Técnico RIC N° 03: Establece que la caída de tensión máxima no debe superar el 3% en alimentadores ni el 5% en el punto más alejado de la carga. STAGE PLAN adopta 3% como umbral estricto (6.6V en 220V).\n"
            "• Normativa SEC - Pliego Técnico RIC N° 10: Regula las instalaciones provisorias para eventos y ferias, exigiendo el uso de cordones flexibles de servicio móvil pesado y protecciones termomagnéticas y diferenciales coordinadas.\n"
            "• Legislación de Ciberseguridad y Privacidad: Cumplimiento con la Ley N° 19.628 de Protección de la Vida Privada y adecuación a la Ley N° 21.719, garantizando consentimiento explícito, finalidad acotada, cifrado en tránsito (HTTPS) y eliminación definitiva de cuentas y recintos privados."
        ),
        (
            "Actividad 2: Planificación del Levantamiento de Datos y Clasificación de Requisitos",
            "• Técnicas de Recopilación: Entrevistas semi-estructuradas al técnico de sonido, revisión de 5 riders técnicos históricos de eventos reales, y contraste físico con instrumentos de medición (multímetro True-RMS y decibelímetro homologado).\n"
            "• Requisitos Funcionales Clave: RF01 (Autenticación JWT), RF02 (Gestión de Recintos y distancias), RF03 (Rider técnico audio/luces/energía), RF04 (Motor unificado calc-engine eléctrico y acústico), RF05 (Layout 2D en SVG), RF06 (Descarga PDF offline autónomo) y RF07 (Historial versionado).\n"
            "• Requisitos No Funcionales Clave: RNF01 (Tiempo de respuesta motor < 50ms), RNF02 (Aislamiento de acceso anti-IDOR por owner_id), RNF03 (Portabilidad 100% offline del PDF), RNF04 (Cobertura TDD >= 90% con Vitest) y RNF05 (Diseño responsivo Mobile-First)."
        ),
        (
            "Actividad 3: Especificación de Necesidades y Product Backlog Priorizado (MoSCoW)",
            "• Must Have (Obligatorios MVP): HU01 (Autenticación segura y aislamiento de cuenta), HU02 (Dimensionamiento geométrico y cálculo de conductor por caída de tensión y ampacidad), HU03 (Carga eléctrica, conversión kVA a kW con FP=0.8, impedancia y protección de etapas).\n"
            "• Should Have (Importantes): HU04 (Inventario logístico: subs obligatoriamente a piso, cálculo exacto de atriles y zapatillas con tomas de reserva), HU05 (Estudio acústico SPL a 1m, 4m y fondo con alerta de refuerzo delay, más Layout SVG 2D), HU06 (Reporte Operativo en PDF autónomo con checklist y secuencia de encendido seguro en 5 pasos).\n"
            "• Could Have (Deseables): HU07 (Historial de recintos y duplicación rápida de configuraciones), HU08 (Enlace compartido temporal con expiración de lectura)."
        ),
        (
            "Actividad 4: Determinación de Metodologías y Necesidades de Seguridad TI",
            "• Lenguaje de Programación: TypeScript 5.7 sobre Node.js (Backend) y Vue 3 Composition API (Frontend), compartiendo el paquete @stageplan/shared para asegurar validación isomórfica con Zod y eliminar desajustes de tipos.\n"
            "• Base de Datos: PostgreSQL relacional gestionado a través de Prisma ORM, garantizando integridad referencial, transacciones concurrentes seguras y consultas 100% parametrizadas (inmunidad contra SQL Injection).\n"
            "• Arquitectura e Infraestructura: Arquitectura Monorepo por capas limpias (Clean Architecture). Despliegue en PaaS gestionado (Render / Railway) con conexión HTTPS automática, cabeceras seguras (helmet) y rate limiting contra ataques de denegación de servicio.\n"
            "• Impacto Ético y Profesional: Mitigación de riesgos contra la vida y la propiedad mediante alertas eléctricas conservadoras (evaluadas a factor de uso 1.0) y estampado indeleble del Disclaimer SEC en todos los reportes emitidos."
        ),
    ]

    for tit, cont in actividades_desarrolladas:
        p_act = t5_row1_cell.add_paragraph()
        r_act_t = p_act.add_run(f"\n{tit}\n")
        r_act_t.bold = True
        r_act_t.font.size = Pt(10.0)
        r_act_t.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

        r_act_c = p_act.add_run(cont)
        r_act_c.font.size = Pt(9.0)
        r_act_c.font.color.rgb = COLOR_ANSWER

    doc.save('TIHV43_GUÍA_ABPRO_U1.docx')
    print("TIHV43_GUÍA_ABPRO_U1.docx successfully filled.")

if __name__ == '__main__':
    fill_guia()

