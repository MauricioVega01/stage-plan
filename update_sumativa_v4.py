import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def update_sumativa_v4():
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
        ("STAGE PLAN (v4.0)\n", True, False, COLOR_TITLE, 22.0),
        ("Sistema Web de Planificación Logística, Ruteo Inteligente, Constructor Híbrido Multilote y Seguridad SEC", False, False, COLOR_TITLE, 14.0)
    ])

    set_p_text(doc.paragraphs[6], [
        ("Carrera: Analista Programador | Asignatura: Proyecto Integrado (TIHV43)\n"
         "Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA\n"
         "Sede: INACAP Santiago | Periodo: Primavera 2026", False, True, RGBColor(0x66, 0x66, 0x66), 10.0)
    ])

    doc.paragraphs[8].alignment = WD_ALIGN_PARAGRAPH.LEFT

    # P[9] Resumen Ejecutivo v4.0
    set_p_text(doc.paragraphs[9], [
        ("¿Qué problema resuelve este proyecto?\n", True, False, COLOR_TITLE, 11.0),
        ("En los eventos y fiestas con DJ en Chile, casi todos los problemas de sonido y electricidad ocurren porque los técnicos calculan los cables, los parlantes y los enchufes 'al ojo' o por intuición. Por ejemplo: conectan todos los parlantes y las luces al primer enchufe que pillan cerca de la cabina, cruzan cables sueltos por el medio de la pista de baile donde la gente camina, tiran alargadores domésticos de más de 30 metros, o combinan cajas activas y pasivas de diferente potencia sin saber cómo nivelarlas.\n\n"
         "Esto provoca fallas graves en terreno:\n"
         "1. Se corta la luz o colapsa el generador a mitad de la fiesta porque el golpe del bajo (transitorio) desestabiliza el regulador de voltaje (AVR) o dispara el automático.\n"
         "2. El voltaje baja tanto por cables delgados que los amplificadores de sonido se apagan o se queman.\n"
         "3. Al mezclar cajas activas y pasivas sin calibración, la caja más pequeña satura y se rompe antes que las demás.\n"
         "4. Conectar cajas pasivas en puente (Speakon Link) sin calcular la impedancia baja la carga a menos de 3.2 Ohms, activando la protección de cortocircuito (PROTECT) del amplificador.\n"
         "5. La gente se tropieza con cables sueltos en el piso, y en parcelas de eventos (Curacaví, Lampa, Pirque) no hay señal de celular (4G/5G) para consultar manuales.\n\n", False, False, COLOR_BODY, 10.0),
        ("¿Cuál es la solución que entrega STAGE PLAN (v4.0)?\n", True, False, COLOR_TITLE, 11.0),
        ("STAGE PLAN es una herramienta web simple que se usa antes de salir al evento (con internet). El técnico ingresa las medidas del salón, sus equipos en un Constructor Híbrido Multilote y marca su fuente de energía (enchufe de casa o generador comercial en Watts o kVA).\n\n"
         "El software actúa de forma inteligente mediante 6 pilares de ingeniería:\n"
         "• Constructor Híbrido Multilote (RMS + Peak): Permite ingresar múltiples lotes de cajas y sub-bajos combinando simultáneamente unidades activas y pasivas con su potencia continua (RMS) y de pico (Peak). El algoritmo Asymmetric Rigging ubica el par más potente en el frente (A, B) y las cajas adicionales o impares (ej. una 3ª caja pasiva) como torres de delay con retardo Haas y atenuación de ganancia automática (Gain Matching).\n"
         "• División en 2 Líneas Eléctricas: Separa automáticamente la instalación en Línea 1 (Fuerza Sub-Bajos) y Línea 2 (Medios-Agudos + Cabina DJ) para no sobrecargar zapatillas ni desestabilizar la mixer DJ.\n"
         "• Calculadora de Impedancia Speakon: Aplica la ley de Ohm en paralelo (8Ω // 8Ω = 4Ω) y alerta en rojo si la combinación cae bajo 3.2Ω (riesgo cortocircuito/PROTECT).\n"
         "• Plano 2D con Mapa de Calor SPL: Muestra en tiempo real la dispersión acústica, zonas de confort (>105 dBA peligro auditivo, 96-102 dBA sweet spot) y la ubicación exacta de cada equipo en trípode y subwoofers en bloque central acoplado.\n"
         "• Detección de Cuello de Botella Acústico y Norma Vecinal D.S. N° 38 MMA: Evalúa el balance de potencia Sub/Top y proyecta la atenuación de decibeles hacia la vivienda vecina más cercana para evitar partes municipales.\n"
         "• Resumen WhatsApp y Reporte PDF para Modo Avión: Permite copiar un resumen técnico listo para WhatsApp en 1 clic y descargar la ficha técnica completa en PDF para operar sin señal de internet.", False, False, COLOR_BODY, 10.0)
    ])

    doc.paragraphs[10].text = ""

    # P[15] Objetivo
    set_p_text(doc.paragraphs[15], [
        ("El propósito de STAGE PLAN es eliminar los errores de cálculo en eventos de sonido e iluminación, entregando una herramienta intuitiva que optimiza los metros de cable, previene tropiezos del público mediante el encintado seguro al piso, equilibra el uso de los enchufes disponibles, calibra combinaciones de parlantes desiguales y asegura la continuidad del evento sin cortes de energía.", False, False, COLOR_BODY, 10.0)
    ])

    # P[16] Objetivo General
    set_p_text(doc.paragraphs[16], [
        ("Objetivo General: ", True, False, COLOR_BODY, 10.0),
        ("Desarrollar una aplicación web responsiva e intuitiva que permita a los operadores de DISTORSIONCL SPA configurar inventarios híbridos de parlantes (activos y pasivos con Watts RMS y Peak), calcular de forma inteligente la ubicación espacial 2D con retardo Haas, dividir las líneas de fuerza eléctrica bajo norma SEC, verificar la impedancia en Ohms y exportar un reporte PDF para terreno sin conexión a internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[17] Objetivos Específicos
    set_p_text(doc.paragraphs[17], [
        ("Objetivos Específicos:\n", True, False, COLOR_BODY, 10.0),
        ("1. Levantar los problemas reales de cableado, enchufes y mezclas de equipos en terreno de DISTORSIONCL SPA, como sobrecargas en generadores, cables tirantes y desbalance tonal entre cajas y bajos.\n"
         "2. Programar el motor de cálculo espacial y ruteo inteligente con pruebas automáticas (44 tests unitarios TDD con Vitest), asegurando la asignación asimétrica por potencia RMS, el cálculo de retardo Haas, la ley de Ohm de impedancia y la división de líneas eléctricas.\n"
         "3. Implementar un servidor seguro en Node.js/Express con PostgreSQL (Prisma ORM) que guarde los salones y planos garantizando que ningún usuario ajeno pueda ver datos de otra productora (seguridad anti-IDOR).\n"
         "4. Construir una interfaz visual en Vue 3 con un plano 2D interactivo dotado de mapa de calor SPL, simulador de vúmetros de mixer DJM y generador de reportes PDF que funcione sin conexión a internet.", False, False, COLOR_BODY, 10.0)
    ])

    # P[20] Alcance - Incluye (v4.0)
    set_p_text(doc.paragraphs[20], [
        ("¿Qué incluye el sistema? (Funcionalidades principales):\n", True, False, COLOR_BODY, 10.0),
        ("• Constructor de Equipos Multilote: Permite combinar simultáneamente cajas activas y pasivas de distinta potencia (Watts RMS y Peak) tanto en cajas acústicas (tops) como en sub-bajos.\n"
         "• Distribución Espacial Asimétrica: Asigna automáticamente las 2 cajas de mayor RMS al frente estéreo y las unidades adicionales o impares como torres de delay con retardo Haas y Gain Matching.\n"
         "• Sub-Bajos en Mono Cluster Central: Ubicación de todos los subwoofers agrupados en el suelo al centro (< 1.7m de separación) para ganar +6 dB gratis por acoplamiento mutuo, prohibiendo el uso de pole mounts.\n"
         "• Asistente de Impedancia Speakon: Calcula la resistencia en paralelo (Ohms) para cajas pasivas y alerta riesgo de cortocircuito o activación de protección PROTECT (< 3.2 Ω).\n"
         "• División en 2 Líneas de Fuerza Eléctrica: Separa Línea 1 (Subwoofers) y Línea 2 (Tops + Cabina DJ) con amperaje y Watts calculados por separado.\n"
         "• Evaluación Eléctrica Dual (RMS vs. Peak): Evalúa el consumo térmico continuo contra la capacidad del enchufe y los picos transitorios contra el margen dinámico del generador (AVR 72%).\n"
         "• Mapa de Calor Acústico (SPL Heatmap 2D): Representación gráfica en el plano 2D de zonas de confort auditivo, sweet spot de pista y caída sonora.\n"
         "• Diagnóstico Vecinal D.S. N° 38 MMA: Estimación de decibeles hacia la vivienda vecina más cercana según tipo de muro y horario diurno/nocturno.\n"
         "• Simulador de Vúmetros Mixer DJM: Guía visual para calibrar Trim (+3/+6 dB), Fader al 10, Master en 0/+3 dB y regla de corte Low EQ Kill (un solo bajo a la vez).\n"
         "• Reporte PDF Offline y Copia Rápida para WhatsApp: Descarga de ficha técnica completa en PDF y botón para copiar resumen al portapapeles en 1 clic.", False, False, COLOR_BODY, 10.0)
    ])

    # P[21] Alcance - Excluye
    set_p_text(doc.paragraphs[21], [
        ("¿Qué queda fuera del sistema? (Límites claros):\n", True, False, COLOR_BODY, 10.0),
        ("• No es una app con sincronización bidireccional compleja sin internet (se calcula antes con conexión y se lleva el resultado en PDF para no generar errores de datos).\n"
         "• No incluye bandas en vivo con microfonía de batería o amplificadores de guitarra (acotado exclusivamente a formato DJ y eventos electrónicos).\n"
         "• No realiza la instalación física de enchufes ni reemplaza la firma legal de un instalador eléctrico autorizado por la SEC.", False, False, COLOR_BODY, 10.0)
    ])

    doc.save('Formato_propuesto_sumativa 01_2026.docx')
    doc.save('Proyecto Integrado 1.docx')
    print("✓ Documentos Formato_propuesto_sumativa 01_2026.docx y Proyecto Integrado 1.docx actualizados a v4.0 exitosamente.")

if __name__ == '__main__':
    update_sumativa_v4()

