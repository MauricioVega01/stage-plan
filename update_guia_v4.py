import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_guia_v4():
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
    p0.text = "Preguntas orientadoras para el diagnóstico (v4.0) — Respuestas de ingeniería con ejemplos de ruteo, constructor multilote, impedancia y seguridad SEC (DISTORSIONCL SPA):"
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.runs[0].bold = True
    p0.runs[0].font.name = 'Arial'
    p0.runs[0].font.size = Pt(10.0)

    preguntas_respuestas = [
        (
            "¿Cuáles son las principales necesidades del negocio que requieren una solución de software y cómo afectan a las operaciones, a los empleados y a los clientes de la empresa?",
            "El cliente DISTORSIONCL SPA enfrenta 5 problemas críticos en terreno al calcular 'a ojo':\n"
            "1. Cortes de luz y colapso de generadores: Conectan los bajos y los medios al mismo enchufe casero de 10A o a un generador comercial cuyo AVR colapsa ante los transitorios del bombo.\n"
            "2. Caídas de voltaje en alargadores: Usan cables de 1.5 mm² en tiradas largas (>30m), cayendo a menos de 195V y provocando apagones térmicos de las cajas activas.\n"
            "3. Mezcla desigual de cajas activas y pasivas: Combinan por ejemplo 2 cajas activas frontales con 1 pasiva de menor potencia sin ajustar ganancia, provocando distorsión y rotura de la caja débil.\n"
            "4. Cortocircuito de amplificadores por impedancia Speakon: Conectan cajas pasivas en puente (Link) bajando de 3.2 Ohms y activando la protección PROTECT del amplificador.\n"
            "5. Cables sueltos y tropiezos: Falta de cálculo de cinta gris industrial para fijar cables al piso, además del aislamiento sin conectividad 4G/5G en parcelas (Curacaví, Lampa, Pirque).\n"
            "Esto genera sobrecostos por reposición de conos quemados, estrés en el personal técnico y pérdida de prestigio comercial."
        ),
        (
            "¿Qué tipos de software o tecnología ya utiliza la empresa y cómo se integran en sus procesos actuales? ¿Existen limitaciones o brechas que estas herramientas no cubren?",
            "Hoy usan planillas Excel y chats de WhatsApp. Sus limitaciones son:\n"
            "- Excel no visualiza la acústica del recinto ni genera un mapa de calor SPL.\n"
            "- No calcula automáticamente la ley de Ohm en paralelo para Speakon ni detecta cuellos de botella entre subwoofers y cajas de medios.\n"
            "- No divide automáticamente la instalación en 2 líneas de fuerza independientes (Línea 1 Subs vs Línea 2 Tops).\n"
            "- No calcula rollos de cinta gaffer ni verifica caídas de tensión bajo pliego SEC RIC N° 03 y RIC N° 10 en modo sin conexión."
        ),
        (
            "¿Cómo podríamos aplicar metodologías emergentes, como Design Thinking, DevOps o Agile, para desarrollar una solución adaptada a las necesidades del negocio?",
            "Aplicamos metodología Agile Kanban y Test-Driven Development (TDD) estricto con Vitest.\n"
            "En el tablero visual limitamos el trabajo en progreso (WIP <= 2). Cada funcionalidad crítica (cálculo de impedancia, atenuación SPL, retardo Haas y división de líneas de fuerza) cuenta con pruebas unitarias automatizadas previas a su integración (44 tests automatizados 100% aprobados)."
        ),
        (
            "¿De qué manera el diagnóstico de necesidades tecnológicas puede beneficiarse de técnicas como entrevistas, encuestas o análisis de datos de usuario? ¿Qué información clave debería recogerse para fundamentar una propuesta de solución?",
            "Mediante entrevistas en terreno y auditoría de 5 montajes reales descubrimos:\n"
            "- Se gasta 1 rollo de cinta de 50m cada 40m de cable tendido en piso.\n"
            "- El 80% de los técnicos desconoce la impedancia mínima de sus cajas pasivas al puentearlas.\n"
            "- El 70% del consumo eléctrico proviene exclusivamente de los sub-bajos en frecuencias de 30-80 Hz.\n"
            "- El público huye de las primeras filas si el SPL supera los 108 dBA por falta de torres de delay en el fondo."
        ),
        (
            "¿Cuáles son los posibles impactos éticos de la solución de software en los empleados, los clientes y otros actores relacionados con el negocio? ¿Cómo se puede asegurar la transparencia y el respeto a la privacidad en el diseño?",
            "El software antepone la vida humana, la seguridad física y la convivencia comunitaria:\n"
            "1. Prevención de tropiezos: Cuantificación obligatoria de cinta gris para sellar cables al suelo.\n"
            "2. Prevención de incendios: Semáforo de carga eléctrica continua (RMS) y transitoria (Peak).\n"
            "3. Convivencia vecinal: Simulación acústica según Decreto Supremo N° 38 del MMA de Chile para evitar contaminación acústica.\n"
            "4. Privacidad de datos: Protección anti-IDOR en base de datos PostgreSQL, garantizando aislamiento estricto de eventos por cliente."
        ),
        (
            "¿De qué modo la solución de software propuesta puede promover valores de ciudadanía, como la equidad de acceso, la inclusión de todos los usuarios y el cumplimiento de estándares éticos?",
            "Democratiza el acceso a ingeniería electroacústica profesional para pequeños sonidistas y DJ independientes de Chile, promoviendo el cumplimiento voluntario de la normativa SEC y previniendo la contaminación acústica comunitaria."
        ),
        (
            "¿Qué métricas o criterios deberíamos considerar para evaluar la efectividad y la sostenibilidad de la solución de software en el tiempo? ¿Cómo podemos incorporar la retroalimentación del usuario para futuras mejoras?",
            "Métricas clave de éxito:\n"
            "1. Generación de plano y cubicación en menos de 3 minutos.\n"
            "2. Cero incidentes de automáticos cortados o amplificadores en PROTECT.\n"
            "3. Cero accidentes por tropiezos en pista.\n"
            "4. 100% de disponibilidad de fichas en terreno mediante PDF offline y resumen exportable a WhatsApp."
        ),
        (
            "¿Cuáles son las principales problemáticas que enfrenta el área de estudio?",
            "Cálculo empírico 'al ojo', sobrecarga de alargadores, mezcla descalibrada de cajas activas y pasivas, puentes de impedancia erróneos en Speakon y falta de internet móvil en parcelas de eventos."
        ),
        (
            "¿Qué información de la cultura institucional del cliente y reglamentaria es relevante para el proyecto?",
            "Cultura ágil y práctica en terreno (lenguaje directo, visual y accesible con modo oscuro de alto contraste) y estricto apego a la normativa SEC: Pliego RIC 03 (caída de voltaje <= 3%) y RIC 10 (conductores flexibles para eventos)."
        ),
        (
            "¿Cuáles son los objetivos específicos del levantamiento de datos en las instalaciones propias del cliente?",
            "Inventariar el stock de cajas activas y pasivas con sus potencias RMS y Peak, medir los salones habituales, relevar la impedancia nominal de las cajas y cronometrar los tiempos de montaje."
        ),
        (
            "¿Qué recursos, tiempo y metodologías se necesitan para el levantamiento de datos?",
            "Recursos: Multímetro, medidor láser, fichas de parlantes y bitácora de eventos. Tiempo: 14 horas distribuidas en 2 semanas. Metodología: Levantamiento empírico y entrevistas estructuradas."
        ),
        (
            "¿Cómo se levantará y analizará la información del proyecto? ¿De qué manera los datos obtenidos cumplirán con la normativa vigente?",
            "Se incorporan en el motor determinista de STAGE PLAN, el cual calcula la ley de Ohm en paralelo, evalúa la ampacidad y caída de tensión SEC RIC 03/10 y simula el impacto acústico de la instalación."
        ),
        (
            "¿Qué propuestas de mejora se pueden desarrollar a partir de la información recopilada?",
            "Diseñar e implementar STAGE PLAN v4.0: Constructor Híbrido Multilote (RMS + Peak), división en 2 líneas eléctricas de fuerza, cálculo de impedancia Speakon, plano 2D interactivo con mapa de calor SPL, diagnóstico D.S. N° 38 MMA y exportación para WhatsApp y PDF offline."
        ),
    ]

    for q, a in preguntas_respuestas:
        p_q = t2_cell.add_paragraph()
        p_q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_q = p_q.add_run(f"\n{q}\n")
        r_q.bold = True
        r_q.font.name = 'Arial'
        r_q.font.size = Pt(9.5)
        r_q.font.color.rgb = COLOR_Q

        p_a = t2_cell.add_paragraph()
        p_a.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r_a = p_a.add_run(a)
        r_a.font.name = 'Arial'
        r_a.font.size = Pt(9.0)
        r_a.font.color.rgb = COLOR_ANSWER

    # 2. TABLA 5 ROW 1: DESARROLLO DE ACTIVIDADES v4.0
    t5_row1_cell = doc.tables[5].rows[1].cells[0]
    t5_row1_cell.text = ""

    p_dev_title = t5_row1_cell.add_paragraph()
    p_dev_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_dev = p_dev_title.add_run("DESARROLLO FORMAL DE LAS 4 ACTIVIDADES DEL DIAGNÓSTICO (UNIDAD 1 - v4.0)\n")
    r_dev.bold = True
    r_dev.font.size = Pt(11.0)
    r_dev.font.color.rgb = COLOR_TITLE

    actividades_desarrolladas = [
        (
            "Actividad 1: Antecedentes y Leyes de Chile que Aplican al Proyecto",
            "• Operación del cliente: DISTORSIONCL SPA ejecuta montajes de audio e iluminación en salones y parcelas de Santiago. En el 70% de los casos operan en parcelas con tomas domiciliarias de 10A o generadores portátiles a combustión.\n"
            "• Regla SEC RIC N° 03 (Caída de voltaje): Exige que en circuitos terminales no se exceda el 3% de caída (máx 6.6V en 220V). STAGE PLAN calcula sección de 2.5 mm² o 4.0 mm² según corriente y metros.\n"
            "• Regla SEC RIC N° 10 (Cables seguros para eventos): Dispone el uso de conductores flexibles clase 5 con aislamiento para servicio pesado (goma H07RN-F) y protecciones termomagnéticas coordinadas.\n"
            "• Prevención de riesgos laborales: Encintado obligatorio de canalizaciones que atraviesen la pista mediante cinta gris industrial (gaffer tape).\n"
            "• Decreto Supremo N° 38 MMA (Ruido Comunitario): Establece límites máximos permisibles de ruido en fuentes fijas para proteger a receptores vecinales.\n"
            "• Protección de datos (Ley 19.628 / 21.719): Resguardo de credenciales y aislamiento multitenant anti-IDOR."
        ),
        (
            "Actividad 2: Levantamiento de Requerimientos (Funcionales y No Funcionales v4.0)",
            "• Metodología de levantamiento: Auditorías de montajes reales y entrevistas en terreno con sonidistas de DISTORSIONCL SPA.\n"
            "• Requerimientos Funcionales (v4.0):\n"
            "  - RF01: Autenticación segura y control de acceso por sesión.\n"
            "  - RF02: Dimensionamiento de recintos (ancho, largo, altura, materialidad) y ubicación de tomas eléctricas.\n"
            "  - RF03: Constructor Híbrido Multilote: Entrada de múltiples lotes combinando cajas activas y pasivas con Watts RMS y Peak.\n"
            "  - RF04: Ruteo Espacial Asimétrico: Colocación de cajas frontales estéreo y asignación de cajas sobrantes a delays con retardo Haas y Gain Matching.\n"
            "  - RF05: Mono Cluster de Bajos: Agrupamiento central obligatorio en piso para acoplamiento mutuo (+6 dB) y veto de pole mounts.\n"
            "  - RF06: Asistente de Impedancia Speakon: Cálculo en paralelo de Ohms y alerta roja PROTECT (< 3.2 Ω).\n"
            "  - RF07: División en 2 Líneas Eléctricas de Fuerza: Separación automática de Línea 1 (Sub-bajos) y Línea 2 (Tops + Cabina DJ).\n"
            "  - RF08: Evaluación Eléctrica Dual: Comparación de régimen RMS continuo y picos dinámicos contra enchufes 10A/16A o generadores (72% AVR).\n"
            "  - RF09: Plano 2D con Mapa de Calor SPL: Visualización interactiva de cobertura sonora y zonas de seguridad auditiva.\n"
            "  - RF10: Auditoría Vecinal D.S. N° 38 MMA: Estimación de decibeles hacia la vivienda vecina más cercana.\n"
            "  - RF11: Exportación y Movilidad: Generación de reporte PDF offline y botón de copia de resumen para WhatsApp.\n"
            "• Requerimientos No Funcionales:\n"
            "  - RNF01: Rendimiento determinista con cálculo en < 50 ms.\n"
            "  - RNF02: Seguridad Anti-IDOR verificada por pertenencia de usuario.\n"
            "  - RNF03: Operación 100% offline para el técnico en terreno.\n"
            "  - RNF04: 44 pruebas automatizadas con Vitest (100% aprobadas).\n"
            "  - RNF05: Interfaz responsiva con diseño accesible industrial de alto contraste."
        ),
        (
            "Actividad 3: Priorización del Proyecto (Técnica MoSCoW v4.0)",
            "• Must Have (Obligatorio v4.0):\n"
            "  - HU01: Autenticación segura de usuarios.\n"
            "  - HU02: Constructor Híbrido Multilote (Activas + Pasivas, RMS y Peak).\n"
            "  - HU03: Validación eléctrica dual (RMS continuo vs. pico en generador AVR 72%) y división en 2 líneas de fuerza.\n"
            "  - HU04: Asistente de impedancia Speakon en paralelo (< 3.2 Ω PROTECT).\n"
            "  - HU05: Ruteo de cables y cálculo de cinta gris gaffer para piso.\n"
            "• Should Have (Diferenciadores de alto impacto):\n"
            "  - HU06: Plano 2D con Mapa de Calor Acústico (SPL Heatmap).\n"
            "  - HU07: Asignación asimétrica de delay con efecto Haas y Gain Matching.\n"
            "  - HU08: Diagnóstico de cuello de botella Top/Sub y simulación D.S. N° 38 MMA.\n"
            "  - HU09: Reporte PDF para terreno y resumen rápido para WhatsApp.\n"
            "• Could Have (Evolución futura): Integración con catálogo de fabricantes mediante API externa.\n"
            "• Won't Have (Exclusiones deliberadas): Sincronización remota en vivo en zonas sin señal y soporte de bandas orquestales complejas."
        ),
        (
            "Actividad 4: Tecnologías Utilizadas, Arquitectura y TDD",
            "• Monorepo Full-Stack TypeScript: Paquete compartido (@stageplan/shared) que garantiza consistencia matemática entre frontend y backend sin duplicidad lógica.\n"
            "• Frontend: Vue 3 con Composition API, TailwindCSS, Canvas/SVG reactivo y jsPDF para compilación local de documentos.\n"
            "• Backend: Node.js, Express, esquemas Zod y Prisma ORM sobre PostgreSQL con políticas de autorización anti-IDOR.\n"
            "• Aseguramiento de Calidad TDD: 44 pruebas unitarias automatizadas con Vitest ejecutadas en < 5 segundos que cubren todos los algoritmos electroacústicos y eléctricos.\n"
            "• Compromiso ético y normativo: Cumplimiento riguroso de normas SEC RIC 03/10 y protección comunitaria frente al ruido."
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
    print("✓ TIHV43_GUÍA_ABPRO_U1.docx actualizado a v4.0 exitosamente.")

if __name__ == '__main__':
    update_guia_v4()

