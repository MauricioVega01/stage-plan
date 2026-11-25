import os

# ========================================================
# 1. LIMPIEZA DE INFORME MARKDOWN
# ========================================================
with open(r'stage-plan-main/INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    l = line
    # Brainstorming
    if '3. Equipamiento Mixto y DMX' in l:
        l = '| **3. Equipamiento de Audio Mixto** | I7: Selector de tecnología Activa vs. Pasiva con dimensionamiento de amplificador externo y alerta de impedancia Speakon ($< 3.2\\ \\Omega$); I8: Cálculo de potencia continua (RMS) vs. pico de audio. | Apagado de etapas en modo `PROTECT` y distorsión por sobrecarga en cajas pasivas. |\n'
    elif '4. Logística y Normativa Chilena' in l:
        l = '| **4. Logística y Seguridad Física** | I9: Alerta preventiva de peso máximo (**Ley del Saco N° 20.949**); I10: Lista de empaque de cables de poder y señal; I11: Plan de contingencia ante falla de caja principal. | Lesiones lumbares por bultos pesados, olvido de cables indispensables y parálisis ante falla de equipo. |\n'
    elif '5. Operación Terreno Offline' in l:
        l = '| **5. Operatividad y Logística de Terreno** | I12: Plano 2D a escala con canalización perimetral; I13: Generación de reporte técnico en PDF; I14: Resumen de requerimientos formateado para WhatsApp; I15: Enlace temporal de consulta para chofer. | Descoordinación entre bodega, transporte y montaje, y falta de planos claros al momento de armar. |\n'
    # Cronograma
    elif '| **T03** |' in l:
        l = '| **T03** | S1 | Diseño Arquitectura 4+1 (5 vistas) y modelo híbrido DER 4 tablas SQLite | M. Vega | 09-Oct – 11-Oct | T02 | Must | No |\n'
    elif '| **T07** |' in l:
        l = '| **T07** | S2 | Implementación `stage-acoustic-engine.ts` (Cluster Mono + Retardos Haas) | M. Vega | 22-Oct – 24-Oct | T05 | Must | No |\n'
    elif '| **T08** |' in l:
        l = '| **T08** | S2 | Implementación ruteo de cables de audio (`cabling.ts`), cabina DJ y 70 tests Vitest | M. Vega | 25-Oct – 28-Oct | T06, T07 | Must | **SÍ** |\n'
    # Historias de Usuario
    elif '| **HU02** |' in l:
        l = '| **HU02** | Geometría y distancias del recinto | 3 | Must | **Dado** un recinto con medidas `<= 0` o `> 500 m`, **cuando** intenta validar, **entonces** Zod rechaza la entrada; con medidas válidas calcula el metraje necesario de cables. |\n'
    elif '| **HU05** |' in l:
        l = '| **HU05** | Ruteo y cálculo de cables de audio (XLR y Speakon) | 5 | Must | **Dado** un montaje con 2 tops frontales y 2 subwoofers, **cuando** procesa el cálculo, **entonces** determina la cantidad exacta de cables balanceados XLR y Speakon requeridos sin faltantes. |\n'
    # Pruebas unitarias
    elif '| **PU-06** |' in l:
        l = '| **PU-06** | Unitaria | `stage-acoustic-engine.ts` | Entorno Indoor vs. Parcela abierta | Ajusta atenuación y cobertura sonora según distancia | **PASS** |\n'
    elif '| **PU-07** |' in l:
        l = '| **PU-07** | Unitaria | `cabling.ts` | 2 Tops + 2 Subs en recinto 25m | Calcula cantidad exacta de cables XLR balanceados y Speakon | **PASS** |\n'
    elif 'tests/lighting-dmx.spec.ts' in l:
        continue
    # Preguntas Anexo C
    elif '11. **¿Por qué un foco PAR LED se contabiliza' in l:
        l = '11. **¿Cómo calcula STAGE PLAN la cantidad exacta de cables de audio?** Determina la distancia desde la cabina DJ hacia el frente y las torres de delay, calculando el metraje de cables balanceados XLR y los cables Speakon NL4 necesarios según las cajas activas y pasivas utilizadas.\n'
    elif '12. **¿Cómo cumple el software con el D.S. N° 38 MMA?**' in l:
        l = '12. **¿Cómo dimensiona el sistema la cobertura y presión sonora?** Aplica la ley del inverso del cuadrado para estimar la atenuación de presión sonora por distancia en decibeles (dB), garantizando que el frente principal y las torres de delay cubran homogéneamente la pista sin zonas muertas.\n'
    elif '18. **¿Qué demuestran los 70 tests unitarios en Vitest?**' in l:
        l = '18. **¿Qué demuestran los 70 tests unitarios en Vitest?** Cubren los archivos de cálculo matemático (eléctrico, cables, impedancia pasiva, acústica indoor/outdoor, DJ setup, distribución de zapatillas y contingencia) ejecutándose en 113 ms con 100% PASS.\n'

    # Reemplazos en línea generales
    l = l.replace('Iluminación DMX y Gain Staging Hardware', 'y Gestión de Cables de Escenario')
    l = l.replace('sonido, iluminación DMX y fuerza eléctrica', 'sonido y fuerza eléctrica')
    l = l.replace('PostgreSQL 16 (12 tablas 3FN + `JSONB` GIN)', 'SQLite 3 (4 tablas 3FN + campos `JSON`)')
    l = l.replace('`CU-05` (Iluminación DMX x1)', '`CU-05` (Ruteo Cables Audio)')
    l = l.replace('`CU-02` (Recinto/D.S. 38)', '`CU-02` (Dimensiones del Recinto)')
    l = l.replace('Paso 1 (Recinto y D.S. 38)', 'Paso 1 (Dimensiones del Recinto)')
    l = l.replace('Paso 2 (Equipos Activo/Pasivo + Power + DMX)', 'Paso 2 (Equipos Activo/Pasivo + Amplificador)')
    l = l.replace('Paso 4 (Reporte Camioneta, Ley del Saco y PDF Offline)', 'Paso 4 (Reporte de Carga, Ley del Saco y Reporte PDF)')
    l = l.replace('Olvido de cables DMX/Speakon/zapatillas', 'Olvido de cables de poder, Speakon o zapatillas')
    l = l.replace('fiscalizaciones D.S. N° 38.', 'auditoría de eventos pasados.')
    l = l.replace('además un foco PAR LED es x1 (no un par) y necesito metros reales de DMX desde cabina', 'además necesito el cálculo exacto de cables Speakon y de señal desde cabina')
    l = l.replace('conteo unitario x1 en iluminación y cálculo métrico DMX desde `DMX OUT`.', 'y cálculo métrico de cables balanceados XLR y Speakon sin sobrantes.')
    l = l.replace('eléctrico+acústico+DMX+DJ', 'eléctrico+acústico+cables+DJ')
    l = l.replace('Ingresar Recinto y Vecinos D.S. 38', 'Ingresar Dimensiones del Recinto')
    l = l.replace('Configurar Tops/Subs Activo-Pasivo + DMX x1', 'Configurar Tops/Subs Activo-Pasivo y Cables')
    l = l.replace('D[(PostgreSQL 16 :5432<br/>12 Tablas 3FN + JSONB GIN)]', 'D[(SQLite 3 dev.db<br/>4 Tablas 3FN + JSON)]')
    l = l.replace('en Modo Avión', 'directamente en el navegador')
    l = l.replace('operatividad **Offline-First** en parcelas rurales.', 'operatividad ágil en estaciones de trabajo y terreno.')

    new_lines.append(l)

with open(r'stage-plan-main/INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('[OK] INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md procesado exitosamente línea por línea.')

# ========================================================
# 2. LIMPIEZA DE GENERATE_SUMATIVA_02_DOCX.PY
# ========================================================
with open(r'stage-plan-main/generate_sumativa_02_docx.py', 'r', encoding='utf-8') as f:
    doc_lines = f.readlines()

new_doc_lines = []
for line in doc_lines:
    l = line
    if '3. Equipos Mixtos y DMX' in l or '3. Equipamiento de Audio Mixto' in l:
        l = '        ["3. Equipamiento de Audio Mixto", "I7: Lotes Activa/Pasiva con amplificador y alerta Speakon; I8: Potencia continua vs pico.", "Apagado en modo PROTECT y distorsión por sobrecarga en cajas pasivas."],\n'
    elif '4. Normativa y Logística' in l or '4. Logística y Seguridad Física' in l:
        l = '        ["4. Logística y Seguridad Física", "I9: Alerta preventiva peso máximo Ley del Saco; I10: Lista cables poder y señal; I11: Plan contingencia.", "Lesiones lumbares, olvido de cables y parálisis ante falla."],\n'
    elif '["HU05",' in l:
        l = '        ["HU05", "Ruteo y metraje de cables de audio (XLR / Speakon)", "5", "Must", "Dada una configuración de 2 Tops y 2 Subs, calcula los cables XLR y Speakon exactos sin faltantes."],\n'
    elif '["Iteración 2",' in l:
        l = '        ["Iteración 2", "Soportar cajas activas/pasivas con amplificador y cálculo de cables Speakon.", "Selector Activo/Pasivo y cálculo métrico de cables de audio sin sobrantes.", "Integrado"],\n'
    elif '["PU-07",' in l:
        l = '        ["PU-07", "Unitaria", "cabling.ts", "2 Tops + 2 Subs en 25m: Cables XLR y Speakon necesarios", "PASS"],\n'
    elif 'tests/lighting-dmx.spec.ts' in l:
        continue
    elif '¿Por qué un foco PAR LED se cuenta x1' in l:
        l = '            ["11", "¿Cómo dimensiona el sistema los cables de audio necesarios?", "Calcula la distancia desde la cabina hacia el PA frontal y torres de delay, determinando la cantidad y metraje exacto de cables XLR y Speakon NL4 sin cruces peligrosos por la pista."],\n'
    elif '¿Cómo valida el D.S. N° 38 MMA?' in l or '¿Cómo se evalúa la cobertura sonora' in l:
        l = '            ["12", "¿Cómo se evalúa la cobertura sonora en el recinto?", "Aplica la atenuación por distancia en decibeles (dB) para asegurar presión sonora homogénea en la pista sin sobreexigir los amplificadores ni generar zonas muertas."],\n'

    l = l.replace('eléctrico SEC + acústica Haas + lotes pasivos + DMX + DJ setup', 'eléctrico SEC + acústica Haas + lotes pasivos + cables + DJ setup')
    l = l.replace('Olvido de cables DMX/Speakon/zapatillas', 'Olvido de cables de poder, Speakon o zapatillas')
    l = l.replace('DMX bajo', 'cables de audio bajo')
    l = l.replace('Ruteo SEC y DMX', 'Ruteo SEC y Cables de Audio')
    l = l.replace('control hardware DMX', 'control de iluminación')
    l = l.replace('Modo Avión', 'modo local')

    new_doc_lines.append(l)

with open(r'stage-plan-main/generate_sumativa_02_docx.py', 'w', encoding='utf-8') as f:
    f.writelines(new_doc_lines)

print('[OK] generate_sumativa_02_docx.py procesado exitosamente línea por línea.')
