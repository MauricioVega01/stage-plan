# Matriz de Trazabilidad y Casos de Prueba Oficiales: STAGE PLAN (v4.0)
**Proyecto Integrado (TIHV43) — Analista Programador — INACAP Sede Maipú (Sección C1 · Grupo G10)**

Esta matriz vincula los Requerimientos Funcionales (RF), Historias de Usuario (HU), Casos de Prueba de Aceptación y Casos de Uso del sistema STAGE PLAN v4.0, respaldados por **81 pruebas unitarias automatizadas en 11 suites Vitest (100% PASS)**.

---

## 1. Mapeo de Trazabilidad Principal (81 Tests Unitarios Automatizados en Vitest)

| Requisito Funcional | Historia de Usuario | Módulo / Engine | Caso de Uso | Criterio de Aceptación y Caso Verificado |
|---|---|---|---|---|
| **RF01** | **HU01** | `auth` / JWT / Prisma | CU-01 | Validación de credenciales (`bcrypt` 12 rondas), JWT firmado (`12h`), limitación de tasa (`10/15m`), bloqueo temporal tras 5 intentos (`HTTP 423 Locked`) y control Anti-IDOR por `ownerId` (`HTTP 404` en recursos ajenos). |
| **RF02 & RF04** | **HU02** | `calc-engine/electrical` | CU-02 | **Caso Cableado y Caída de Tensión (SEC RIC 03/10):** Carga 1.800 W, 220 V, L = 30 m, holgura 20%, caída máx 3% (6,6 V): corriente diseño 9,82 A, sección comercial adoptada 2,5 mm², caída real 4,12 V (1,87%). |
| **RF03 & RF04** | **HU03** | `calc-engine/electrical` | CU-03 | **Caso Eléctrico y Suministro:** Circuito 10 A con 2.000 W (10,91 A diseño) dispara alerta crítica; generador 5 kVA (FP 0,8 = 4.0 kW) frente a 4,2 kW diseño dispara sobrecarga; generador comercial 3500W aplica factor seguro 72% AVR (~2.142 W). |
| **RF03 & v4** | **HU03b** | `calc-engine/hybrid-roster` | CU-04 | **Caso Impedancia Speakon y Rack de Potencias Pasivas (`calculatePowerAmpSizing`):** 2 cajas 8 Ω en paralelo = 4,0 Ω (seguro); 3 cajas 8 Ω en paralelo = 2,67 Ω (< 3,2 Ω → `DANGER_PROTECT_SHORT`). Para lotes pasivos dimensiona etapas 19" con headroom 1,6× RMS, sugiere modelo comercial y suma su consumo AC 220V al balance SEC. |
| **RF03 & v4** | **HU03c** | `calc-engine/hybrid-roster` | CU-03 | **División en Líneas Eléctricas L1/L2/L3:** Separa automáticamente Línea 1 (Subs), Línea 2 (Tops + Cabina DJ) y Línea 3 (Iluminación DMX) con cálculo independiente de Watts y Amperes. |
| **RF03 & v4** | **HU04** | `calc-engine/hybrid-roster` | CU-04 | **Asymmetric Rigging & Gain Matching:** Combina lotes activos y pasivos asignando las 2 cajas principales al frente estéreo (`A, B @ 0 dB`) y las adicionales a torre delay lateral con retardo Haas y atenuación proporcional en dB. |
| **RF04 & RF05** | **HU05** | `calc-engine/stage-acoustic-engine` | CU-02, CU-06 | **Acústica SPL, Retardos Haas y Plano 2D Blueprint:** Atenuación por distancia (Sabine RT60 / campo libre), mapa de calor SPL calibrado y separación en 5 capas exclusivas en `/plano-2d` con postes guía SEC RIC N° 10 (R ≥ 6d) y Vista Completa (`ALL`) en `/reporte`. |
| **RF05 & v4** | **HU05b** | `calc-engine/stage-acoustic-engine` | CU-06 | **Balance Top/Sub y Norma D.S. N° 38 MMA:** Detecta déficit de subgraves si la relación Sub/Top es insuficiente y proyecta dBA hacia la vivienda vecina según horario diurno/nocturno y tipo de cerramiento. |
| **RF06** | **HU06** | `pdfReport.ts` & `ViewReportSummary.vue` | CU-08 | **Cotizador Arriendo CLP, PNG 300 DPI y PDF Dual-Page:** Alterna entre *Equipos Propios* y *Rider Arrendado CLP*, captura el plano CAD completo (`ALL`) a PNG 300 DPI y genera PDF oficial de 2 páginas (Pág. 1 Memoria SEC + costos; Pág. 2 Lámina CAD horizontal). |
| **RF07** | **HU07** | `backend` (Prisma/SQLite) | CU-01 | Persistencia en `dev.db` (4 tablas 3FN en español + columnas JSON) con historial consultable por propietario y proyección de migración a PostgreSQL 16 (Unidad 3). |

---

## 2. Cobertura de Verificación
El conjunto de requerimientos funcionales se encuentra trazado y cubierto por **81 pruebas unitarias aprobadas en 11 archivos** (`npm test`), validación estática sin errores (`vue-tsc` + `tsc`) y compilación de producción Vite verificada.
