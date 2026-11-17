# STAGE PLAN (v4.0) 🎛️⚡🔊

> **Sistema Web de Planificación Logística, Ruteo Inteligente, Constructor Híbrido Multilote y Seguridad Eléctrica SEC para Eventos en Formato DJ**  
> **Proyecto Integrado (TIHV43) — Analista Programador | INACAP 2026**  
> **Caso de Estudio:** Productora y Arriendo de Audio *DISTORSIONCL SPA*

---

## 📋 Resumen del Proyecto

**STAGE PLAN** es una plataforma de ingeniería preventiva para la pre-producción de eventos en formato DJ. Reemplaza el dimensionamiento empírico ("al ojo") por modelado físico determinista, acústica de salas, electrotecnia bajo normativa chilena de la SEC (Pliegos RIC N° 03 y RIC N° 10) y la norma ambiental de emisión de ruido D.S. N° 38 del Ministerio del Medio Ambiente.

Permite al operador ingresar los datos del recinto y sus equipos en la oficina (con internet), generando un plano 2D interactivo, cubicación de cableado, balance eléctrico y un **Reporte Operativo en PDF** que funciona 100% autónomo en terreno sin conexión móvil (modo avión en parcelas de agrado).

---

## 🚀 Innovaciones Clave (v4.0)

1. **Constructor Híbrido Multilote (RMS + Peak):**  
   Permite ingresar simultáneamente lotes heterogéneos de cajas acústicas y sub-bajos combinando unidades activas y pasivas con su potencia continua (RMS) y de pico (Peak).
2. **Asymmetric Rigging & Gain Matching:**  
   Algoritmo determinista que detecta el par más potente para el PA Frontal estéreo (A, B a 0 dB Unity) y envía automáticamente las unidades adicionales o impares (ej. 3ª caja pasiva) como torres de delay con retardo Haas y atenuación calculada en dB para proteger el cono de saturación.
3. **Mono Cluster Central de Subwoofers:**  
   Agrupa automáticamente los subwoofers en bloque central a piso (< 1.7 m de separación) para ganar +6 dB acústicos gratis por acoplamiento mutuo, prohibiendo el uso de tubos *pole mount* sobre sub-bajos.
4. **Asistente de Impedancia Speakon:**  
   Calcula la resistencia equivalente en paralelo ($1/Z_{eq} = \sum 1/Z_i$) y emite una alerta roja crítica de **PROTECT** si la carga desciende bajo los 3.2 Ω.
5. **División en 2 Líneas Eléctricas de Fuerza:**  
   Separa la instalación en Línea 1 (Fuerza Sub-Bajos) y Línea 2 (Medios-Agudos + Cabina DJ), blindando la mixer de caídas de tensión y desestabilización del regulador AVR en generadores.
6. **Plano 2D con Mapa de Calor Acústico (SPL Heatmap):**  
   Renderizado reactivo con gradientes radiales SVG que representan zonas de confort (>105 dBA rojo advertencia, 96-102 dBA verde sweet spot, <90 dBA azul caída).
7. **Diagnóstico Ambiental Vecinal (D.S. N° 38 MMA):**  
   Simula la atenuación de decibeles hacia la vivienda vecina más cercana evaluando el cumplimiento diurno y nocturno.
8. **Exportación Dual (PDF Offline & Resumen WhatsApp):**  
   Copia el resumen técnico al portapapeles en 1 clic y compila en cliente una ficha técnica completa de 5 páginas en PDF.

---

## 🏗️ Arquitectura del Monorepo

El proyecto está estructurado como un **Monorepo TypeScript**:

```
Proyecto Integrado/
├── packages/
│   ├── shared/     # @stageplan/shared: Núcleo matemático puro, Zod schemas, física acústica y fórmulas SEC
│   ├── frontend/   # @stageplan/frontend: SPA Vue 3 + Vite + TailwindCSS + jsPDF (Diseño Industrial Dark)
│   └── backend/    # @stageplan/backend: API REST Node.js + Express + Prisma ORM (PostgreSQL) anti-IDOR
├── Formato_propuesto_sumativa 01_2026.docx  # Documento sumativo de titulación
├── TIHV43_GUÍA_ABPRO_U1.docx                # Guía de aprendizaje y diagnóstico de negocio
├── Presentacion_Proyecto_STAGE_PLAN_Profesor.pdf # Presentación ejecutiva de defensa
├── GUION_PRESENTACION_PROFESOR.md           # Libreto de defensa ante la comisión evaluadora
└── package.json
```

---

## 🧪 Pruebas Unitarias Automatizadas (TDD)

El motor de cálculo cuenta con **44 pruebas unitarias automatizadas** con **Vitest**, logrando **100% de aprobación**:

```bash
# Ejecutar suite completa de pruebas
npm test
```

| Archivo de Prueba | Cobertura / Módulo Validado | Tests | Resultado |
|---|---|:---:|:---:|
| `calc-engine.spec.ts` | SEC RIC 03/10, Impedancia Speakon, Multilote RMS/Peak y 2 Líneas | 23 | ✅ PASS |
| `routing-and-gaffer.spec.ts` | Algoritmo Manhattan Multi-enchufe y Cubicación Cinta Gaffer | 10 | ✅ PASS |
| `stage-acoustic-engine.spec.ts` | SPL Indoor/Outdoor, Haas, Generador 3500W y D.S. N° 38 MMA | 5 | ✅ PASS |
| `stage-acoustic-indoor-outdoor.spec.ts` | Acústica de Salas (Sabine RT60 y Hopkins-Stryker) | 2 | ✅ PASS |
| `hybrid-roster.spec.ts` | Asymmetric Rigging & Gain Matching para cajas heterogéneas | 2 | ✅ PASS |
| `cabling.spec.ts` | Cableado Dinámico (XLR, Speakon NL4, IEC C13, PowerCON, DMX) | 2 | ✅ PASS |
| **TOTAL** | **Suite Completa de Ingeniería Electroacústica y Eléctrica** | **44** | **100% PASS** |

---

## 🛠️ Puesta en Marcha

### Prerrequisitos
- Node.js >= 18.x
- npm >= 9.x

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/MauricioVega01/stage-plan.git
cd stage-plan

# Instalar dependencias del monorepo
npm install
```

### Ejecución en Modo Desarrollo
```bash
# Iniciar frontend (disponible en red local y móvil en http://0.0.0.0:5173)
npm run dev

# Compilar todos los paquetes
npm run build
```

---

## 📜 Normativa y Referencias de Ingeniería

- **Superintendencia de Electricidad y Combustibles (SEC Chile):**
  - **Pliego Técnico Normativo RIC N° 03:** Caída de tensión máxima admisible en alimentadores y circuitos terminales ($\le 3\%$).
  - **Pliego Técnico Normativo RIC N° 10:** Instalaciones de uso general y eventos (conductores flexibles clase 5, canalizaciones seguras).
- **Ministerio del Medio Ambiente (MMA Chile):**
  - **Decreto Supremo N° 38:** Norma de emisión de ruidos generados por fuentes fijas.
- **IEC 60268:** Sound system equipment standards.

---

## 👤 Autor

**Mauricio Andrés Vega Castillo**  
*Carrera: Analista Programador | INACAP Sede Santiago*  
GitHub: [@MauricioVega01](https://github.com/MauricioVega01)  
Noviembre 2026
