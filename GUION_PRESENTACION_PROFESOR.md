# GUION DE PRESENTACIÓN Y DEFENSA: STAGE PLAN (v4.0)
## Caso de Estudio: Productora y Arriendo de Audio DISTORSIONCL SPA
### Asignatura: Proyecto Integrado (TIHV43) — INACAP

---

## 3 PILARES ESTRATÉGICOS PARA DEFENDER ANTE LA COMISIÓN
1. **No es un CRUD genérico; es un Sistema Experto de Ingeniería Preventiva:** Transforma variables simples ingresadas por el cliente (medidas del lugar, constructor multilote de cajas activas/pasivas con Watts RMS y Peak, enchufe de casa de 10A/16A o generador comercial de 3.500W) en decisiones automáticas de electroacústica y electrotecnia que previenen equipos quemados, generadores apagados en pleno drop, desbalance tonal y sonido saturado ("chicharriento").
2. **Contraste entre Complejidad Física Interna y UX Accesible ("Hard Techno Industrial"):** Por dentro resuelve cálculos deterministas de ingeniería de audio: retardos temporales en milisegundos para sincronización de torres (Efecto Haas: $t = d/343$), ley de Ohm en paralelo de impedancias Speakon, división automática en **2 Líneas de Fuerza Eléctrica** (Línea 1 Subs vs Línea 2 Tops) y caída de tensión dinámica ($\Delta V \le 3\%$) bajo pliego SEC RIC N° 03. Por fuera ofrece una interfaz de alto contraste pensada para baja visión en cabinas oscuras, con **Plano 2D**, botones `[i]` explicativos, botón de copia rápida a **WhatsApp** y descarga de **Ficha Técnica PDF en memoria del navegador**.
3. **Calidad Demostrable con 70 Pruebas Unitarias Automatizadas (Vitest TDD):** Cada cálculo acústico, eléctrico, de impedancia, ruteo de cables de poder y señal (`XLR`, `Speakon NL4`, `IEC C13`, `PowerCON`) y rollos de cinta Gaffer de 50m está verificado automáticamente con **70 de 70 tests aprobados (100% Pass en 10 suites)**.

---

## ESTRUCTURA PASO A PASO (8 A 10 MINUTOS)

### LÁMINA 1: Portada e Identidad del Proyecto
**Qué dices:**
> "Buenos días profesor y comisión. Hoy presento **Stage Plan (v4.0)**, un sistema experto de pre-producción electroacústica, constructor híbrido multilote, distribución espacial 2D y seguridad eléctrica desarrollado para la productora **DISTORSIONCL SPA**."
>
> "A diferencia de un sistema administrativo tradicional, Stage Plan resuelve un problema físico y operativo crítico en eventos electrónicos y fiestas en salones o parcelas: cómo lograr que el sonido suene potente, equilibrado y nítido en toda la pista combinando cajas activas y pasivas de diferente potencia sin romper conos, sin quemar amplificadores por baja impedancia, sin botar el automático de la casa y sin que el generador colapse en el golpe del bombo."

---

### LÁMINA 2: Diagnóstico del Problema (Los 5 Porqués en Terreno)
**Qué dices:**
> "Al levantar requerimientos con DISTORSIONCL SPA identificamos 5 fallos recurrentes cuando se monta 'al ojo':
> 1. **Colapso de energía en el drop:** Conectan cajas y sub-bajos a un enchufe doméstico de 10A (que solo soporta 1.760W continuos seguros) o a un generador comercial de '3.500 Watts' sin considerar que ese valor es pico de arranque y que para audio continuo solo entrega ~2.140W estables antes de que el regulador AVR caiga bajo 195V y apague las cajas.
> 2. **Saturación y mezcla desigual de cajas:** Al combinar por ejemplo 2 cajas activas frontales con 1 caja pasiva de menor potencia, la caja débil satura y distorsiona si no se ajusta y empareja su nivel de volumen (ganancia).
> 3. **Cortocircuito de amplificadores por impedancia:** Conectan cajas pasivas en puente (*Speakon Link*) bajando la carga bajo 3.2 Ohms, lo que activa la protección PROTECT del amplificador y apaga la música.
> 4. **Cancelación de graves ('Pasillo de la Muerte'):** Separan los subwoofers a izquierda y derecha en vez de agruparlos en bloque central a piso.
> 5. **Falta de conectividad en parcelas:** En zonas como Curacaví, Lampa o Pirque no hay señal móvil 4G/5G, por lo que el sonidista necesita llevar toda la ingeniería resuelta en un **Reporte Operativo PDF Offline** y compartir el resumen por WhatsApp antes de salir."

---

### LÁMINA 3: Alcance, Constructor Multilote e Inteligencia v4.0
**Qué dices:**
> "Stage Plan v4.0 incorpora 6 innovaciones deterministas de ingeniería:
> - **Constructor Híbrido Multilote (RMS + Peak):** Permite ingresar lotes combinados de cajas activas y pasivas con su potencia continua y pico. El algoritmo detecta automáticamente el par más potente para el frente principal (A, B a 0 dB) y envía las unidades adicionales o impares a delay lateral con ajuste preciso de ganancia para no saturarlas.
> - **División en 2 Líneas de Fuerza:** Separa automáticamente la instalación en Línea 1 (Sub-bajos, alto consumo de corriente) y Línea 2 (Tops + Cabina DJ), calculando el amperaje y los Watts por separado.
> - **Calculadora de Impedancia Speakon:** Aplica la ley de Ohm en paralelo y alerta en rojo si la resistencia cae bajo 3.2 Ohms (riesgo cortocircuito/PROTECT).
> - **Plano 2D con Mapa de Calor SPL:** Proyecta la presión sonora en la pista con gradientes radiales de color (rojo >105 dB, verde 96-102 dB sweet spot, azul <90 dB).
> - **Auditoría de Balance Tonal y Cobertura:** Diagnostica la relación de potencia entre cajas de medios-agudos y subwoofers para garantizar una presión sonora homogénea en toda la pista.
> - **Resumen WhatsApp en 1 Clic y Reporte PDF Offline:** Resumen técnico al portapapeles y ficha PDF completa descargable para terreno."

---

### LÁMINA 4: Arquitectura Monorepo TypeScript y Motor Determinista
**Qué dices:**
> "Construimos una arquitectura limpia basada en un **Monorepo TypeScript** con tres paquetes:
> 1. **`@stageplan/shared`:** Núcleo matemático puro, desacoplado de la vista, que concentra los cálculos de presión sonora ($SPL$), propagación acústica en recintos cerrados, impedancia Speakon en paralelo, ley de Ohm, separación de 2 líneas de fuerza y dimensionamiento bajo normas **SEC Pliegos RIC N° 03 y RIC N° 10**.
> 2. **`@stageplan/frontend`:** Interfaz en Vue 3 + Vite + TailwindCSS con estética **Hard Techno Industrial** de alto contraste, plano 2D reactivo con Mapa de Calor SPL dinámico, tipografía ampliada para baja visión, glosario interactivo `[i]` y botón de copia a WhatsApp.
> 3. **`@stageplan/backend`:** API REST en Node.js, Express y Prisma ORM sobre SQLite embebido (`dev.db`, directamente inspeccionable en DB Browser) con validación Zod y protección estricta anti-IDOR."

---

### LÁMINA 5: Inteligencia Acústica 2D y Calibración de Mixer DJM
**Qué dices:**
> "Cuando el usuario ingresa una combinación de equipos (por ejemplo 2 cajas activas frontales, 1 caja pasiva de delay y 2 sub-bajos en cluster):
> - Ubica las cajas **A y B** en el Frente Principal en trípodes a 2.2m operando a **0 dB Unity (perilla a las 12:00)**.
> - Envía la caja pasiva **C** como torre de delay lateral con **retardo Haas (+3.0 ms)** y **-2.2 dB de atenuación de ganancia** para emparejar la presión sonora sin saturarla.
> - Agrupa los subwoofers en un **Mono Cluster Central** en piso, ganando **+6 dB acústicos gratis** por acoplamiento mutuo y eliminando cancelaciones.
> - Además, entrega la **Tabla de Calibración Visual del Mixer DJM**: `Fader` al 10, `Trim` en `+3 a +6 dB` (ámbar), `Master` en `0 a +3 dB` (`+4 a +7 dBu` limpios, cero rojos) y la regla de transición con 2 canales (**un solo bajo a la vez / Low EQ Kill** para evitar barro y cancelaciones entre bombos)."

---

### LÁMINA 6: Las Reglas Críticas de Terreno y Seguridad SEC
**Qué dices:**
> "El sistema audita automáticamente las reglas de seguridad en terreno:
> 1. **Crossover HPF a 80–90 Hz en Cajas Top:** Libera ~40% de potencia desperdiciada en los tops y evita cancelaciones con el subwoofer.
> 2. **Ángulo de Apertura Horizontal:** Calcula la rotación hacia afuera para cruzar la dispersión de los parlantes sin cancelaciones de fase ni zonas muertas.
> 3. **Impedancia Mínima Speakon (3.2 Ω):** Bloquea conexiones en paralelo que puedan forzar a los amplificadores a modo de protección.
> 4. **División en 2 Líneas de Fuerza:** Previene que el consumo del bombo apague la mixer del DJ o las cajas de agudos.
> 5. **Caída de Tensión y Puesta a Tierra:** Exige cable de 2.5 mm² o 4.0 mm² bajo norma SEC RIC 03 y conectar barra de puesta a tierra al chasis del generador en parcelas."

---

### LÁMINA 7: Calidad de Software (70 Tests en Vitest) y Conclusión
**Qué dices:**
> "Para demostrar rigor de ingeniería de software, ejecutamos una suite automatizada en **Vitest** con **70 pruebas unitarias aprobadas al 100%** en 10 archivos de test (en solo 113 ms), validando desde el motor eléctrico SEC y el ruteo de cables hasta la ley de Ohm de impedancia pasiva, la división de 2 líneas de fuerza, la caída de tensión y la protección de generadores.
>
> En conclusión, **Stage Plan** transforma física acústica y normativa eléctrica SEC en una herramienta práctica, accesible y lista para operar en terreno sin internet. Muchas gracias."

---

## PREGUNTAS CLAVE DE LA COMISIÓN Y RESPUESTAS DE ALTO NIVEL

### 1. "¿Cómo maneja el sistema la combinación de cajas activas y pasivas de diferente potencia (por ejemplo 2 activas y 1 pasiva)?"
* **Respuesta:** "A través de nuestro algoritmo de distribución inteligente en el módulo `hybrid-roster.ts`. El sistema ordena las cajas por su potencia RMS: asigna las 2 unidades de mayor potencia al frente estéreo principal (A, B a 0 dB), y las unidades adicionales o impares (como la 3ª caja pasiva) las destina automáticamente como torres de refuerzo (delay) con retardo Haas en milisegundos y un factor de atenuación de ganancia proporcional a la diferencia de potencia. Así se evita que la caja más pequeña alcance el clip prematuramente o se queme."

### 2. "¿Por qué un generador de 3.500 Watts no aguanta 3.000 Watts de audio?"
* **Respuesta:** "Porque los '3.500 Watts' del sticker comercial son potencia pico de arranque (*Surge Watts*). Su potencia continua real ronda los 2.975W, y en audio electrónico los golpes del subwoofer producen escalones bruscos de corriente que frenan el motor y desestabilizan el regulador de voltaje del generador (AVR). Nuestro validador eléctrico aplica un factor de seguridad del 72% sobre la potencia continua (~2.142W seguros) para garantizar un margen dinámico y evitar que las cajas se apaguen por bajo voltaje (<195V)."

### 3. "¿Qué pasa si se conectan 3 cajas pasivas de 8 Ohms en paralelo a un solo canal de potencia?"
* **Respuesta:** "La ley de Ohm indica que $1 / Z = 1/8 + 1/8 + 1/8 = 3/8$, lo que resulta en una impedancia equivalente de $2.67\ \Omega$. Casi todos los amplificadores de audio profesional están diseñados para una carga mínima de $4\ \Omega$ (o $3.2\ \Omega$ con tolerancia). Al bajar a $2.67\ \Omega$, la corriente demandada excede el límite seguro de los transistores de salida, lo que activa el circuito de protección térmica/cortocircuito (*PROTECT*) apagando el canal. Stage Plan detecta esto inmediatamente, muestra una alerta roja con advertencia de corte y recomienda distribuir las cajas en canales de amplificación independientes."

### 4. "¿Por qué utilizas SQLite en el MVP y cómo almacenas la información?"
* **Respuesta:** "Para el MVP funcional elegimos **SQLite 3 (`dev.db`) con Prisma ORM**. Diseñamos 4 tablas normalizadas en tercera forma normal completamente en español (`usuarios`, `recintos`, `calculos_rider`, `enlaces_compartidos`) para garantizar integridad referencial estricta (`ON DELETE CASCADE`), y utilizamos campos `JSON` nativos para guardar los snapshots del rider y del cálculo sin sobrecargar la base de datos con tablas intermedias innecesarias. La gran ventaja operativa es que el archivo `dev.db` es 100% portable, no depende de servicios de red externos que puedan fallar en la defensa, y puedo auditar los datos directamente arrastrando el archivo a **DB Browser for SQLite**, donde se ven las tablas y columnas en español con nombres claros como `ancho_metros`, `distancia_electrica_metros` y `resultados_calculados`."

### 5. "¿Cómo garantizas que el sistema funcione en terreno si en las parcelas no hay internet?"
* **Respuesta:** "Mantuvimos la solución simple y eficaz: todo el motor matemático (`@stageplan/shared`) se ejecuta en el navegador del cliente con JavaScript compilado, y la ficha técnica se compila en memoria con `jsPDF`. Así, el técnico puede ingresar medidas, calcular cables, ver el plano 2D y descargar su PDF directamente en su teléfono o laptop sin depender de la señal móvil en terreno."
