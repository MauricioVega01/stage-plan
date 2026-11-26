# STAGE PLAN (v4.0)

> **Sistema Web de Planificación Logística, Ruteo Eléctrico SEC, Plano CAD Blueprint, Rack de Potencias Pasivas y Cotización Operativa para Eventos en Formato DJ**  
> **Proyecto Integrado (TIHV43) — Analista Programador | INACAP Sede Maipú (Sección C1 · Grupo G10)**  
> **Caso de Estudio:** Productora y Arriendo de Audio *DISTORSIONCL SPA*

---

## Resumen del Proyecto

**STAGE PLAN** es una plataforma de ingeniería preventiva para la pre-producción de eventos en formato DJ. Sustituye el dimensionamiento empírico sin cálculo normativo por modelado físico determinista, acústica de salas, electrotecnia bajo normativa chilena de la SEC (**Pliegos RIC N° 03 y RIC N° 10**), **Decreto Supremo N° 38 del MMA** y **Ley del Saco N° 20.949**.

Permite al operador configurar las dimensiones del recinto y sus equipos en formato **Studio Cockpit (100% zoom)**, obteniendo un plano CAD 2D por capas, dimensionamiento automático del rack de potencias para cajas pasivas, cotización operativa de arriendo en CLP, resumen para WhatsApp y un **Reporte Operativo PDF Dual-Page** generado client-side en el navegador para operar en terreno sin conexión móvil.

---

## Funcionalidades Clave (v4.0)

1. **Constructor Híbrido Multilote (RMS + Peak) y Rack de Potencias Pasivas (`calculatePowerAmpSizing`):**  
   Combina lotes heterogéneos activos y pasivos; cuando existen unidades pasivas calcula la impedancia de carga (4 Ω / 8 Ω), aplica headroom **1,6× RMS**, sugiere etapas de potencia comerciales y suma el consumo AC 220V al balance SEC.
2. **Asymmetric Rigging & Gain Matching + Clúster Mono Central:**  
   Asigna las cajas principales al PA Frontal (`A, B @ 0 dB Unity`), envía unidades adicionales a torres de retardo Haas con atenuación calculada en dB y agrupa subwoofers en bloque central a piso (< 1,7 m) para ganar `+6 dB` por acoplamiento mutuo.
3. **Asistente de Impedancia Speakon y División de Líneas L1/L2/L3:**  
   Evalúa impedancia en paralelo ($1/Z_{eq} = \sum 1/Z_i$) emitiendo alerta crítica **PROTECT** si cae bajo 3,2 Ω, y separa circuitos de fuerza L1 (Subwoofers), L2 (Tops + Cabina DJ) y L3 (Iluminación DMX).
4. **Plano 2D Blueprint CAD por 5 Capas Exclusivas + Vista Completa en Reporte:**  
   Separa la visualización en capas exclusivas al configurar (`Arquitectura & Audio`, `Cobertura SPL`, `Fuerza SEC L1/L2/L3`, `Audio & DMX`, `Vista Completa`) con postes guía SEC RIC N° 10 ($R \ge 6d$), consolidando todas las capas en `/reporte`.
5. **Diagnóstico Ambiental Vecinal (Decreto Supremo N° 38 MMA):**  
   Simula la atenuación sonora hacia la vivienda vecina más cercana contrastando contra límites diurnos y nocturnos según cerramiento.
6. **Cotizador de Arriendo CLP, PNG 300 DPI y PDF Dual-Page Offline:**  
   Alterna entre *Equipos Propios* y *Rider Arrendado CLP*, exporta el plano CAD a PNG 300 DPI y compila en navegador un PDF de 2 páginas (Pág. 1 Memoria SEC + costos; Pág. 2 Lámina CAD horizontal).

---

## Arquitectura del Monorepo

El proyecto está organizado como **Monorepo TypeScript (`npm workspaces`)**:

```text
stage-plan-main/
├── packages/
│   ├── shared/     # @stageplan/shared: 11 módulos matemáticos puros, Zod schemas y 81 tests Vitest
│   ├── frontend/   # @stageplan/frontend: Vue 3.5 + Vite 6.4 + Vue Router 4 + Tailwind 3.4 + useStagePlanState + jsPDF
│   └── backend/    # @stageplan/backend: Express 4.21 + Prisma ORM 6.4 (SQLite dev.db / Proy. PG16 U3) + Auth 423 + Anti-IDOR 404
├── entrega_sumativa_02/
│   ├── diagrams/   # 8 diagramas arquitectónicos y UML en SVG/HTML/PNG
│   ├── prototipo/  # Capturas reales al 100% de zoom y mosaico
│   └── sql/        # SQLite dev.db (PoC) y schema_stageplan_pg16.sql (Proyección U3)
└── package.json
```

---

## Pruebas Unitarias Automatizadas (TDD)

La suite automatizada ejecuta **81 pruebas unitarias en 11 archivos (`100% PASS`)** con **Vitest v3.2.7**:

```bash
# Ejecutar suite completa de pruebas
npm test
```

| Archivo de Prueba | Alcance Validado | Tests | Resultado |
|---|---|:---:|:---:|
| `calc-engine.spec.ts` | SEC RIC 03/10, capacidad red/generador, soportes y SPL | 23 | PASS |
| `routing-and-gaffer.spec.ts` | Algoritmo Manhattan multi-enchufe y cinta Gaffer 50 m | 10 | PASS |
| `hybrid-roster.spec.ts` | Asymmetric Rigging, Gain Matching y Rack de Potencias Pasivas (`PA-01..06`) | 8 | PASS |
| `power-distribution.spec.ts` | Distribución L1/L2/L3 y protecciones 80% | 8 | PASS |
| `lighting-dmx.spec.ts` | Luminarias x1, consumo térmico y bus DMX512 | 8 | PASS |
| `contingency-logistics.spec.ts` | Plan B contingencia, pesos y Ley del Saco N° 20.949 | 6 | PASS |
| `stage-acoustic-engine.spec.ts` | Clúster mono, Haas, Generador 3500W (72% AVR) y D.S. N° 38 MMA | 5 | PASS |
| `qa-gap-branches.spec.ts` | Casos borde eléctricos, acústicos y validaciones | 5 | PASS |
| `dj-setup-audio.spec.ts` | Cabina DJ (CDJ/XDJ, Pro DJ Link RJ45, Mixer y Booth) | 4 | PASS |
| `stage-acoustic-indoor-outdoor.spec.ts` | Acústica de salas (Sabine RT60 y Hopkins-Stryker) | 2 | PASS |
| `cabling.spec.ts` | Cableado dinámico (XLR, Speakon NL4, IEC C13, PowerCON) | 2 | PASS |
| **TOTAL** | **Suite Completa `@stageplan/shared`** | **81** | **100% PASS** |

---

## Puesta en Marcha Local

```bash
# Instalar dependencias del monorepo
npm install

# Ejecutar pruebas y verificación de tipos
npm test
npm run lint

# Iniciar frontend (http://localhost:5173)
npm run dev

# Compilar todos los paquetes
npm run build
```

---

## Autor

**Mauricio Vega Castillo**  
*Analista Programador | INACAP Sede Maipú — Sección C1 · Grupo G10*  
GitHub: [@MauricioVega01](https://github.com/MauricioVega01)
