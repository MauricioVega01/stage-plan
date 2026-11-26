# PROYECTO INTEGRADO (TIHV43) – UNIDAD 2: DISEÑO DE LA SOLUCIÓN DE SOFTWARE
## INFORME TÉCNICO: EVALUACIÓN SUMATIVA 2

**Institución:** Instituto Profesional INACAP – Sede Maipú  
**Área Académica:** Tecnologías de Información y Ciberseguridad  
**Carrera:** Analista Programador / Ingeniería en Informática  
**Asignatura:** Proyecto Integrado (`TIHV43`)  
**Sección:** C1 | **Grupo:** G10 (Modalidad Solo-Developer bajo Scrumban + PSP)  
**Autor:** Mauricio Vega Castillo  
**Docente Guía:** Manuel Rojas  
**Empresa Contraparte:** Productora y Arriendo de Audio *DISTORSIONCL SPA* (Operador Técnico: Amaro Artiaga)  
**Sistema:** **STAGE PLAN** — Plataforma Web de Pre-Producción Logística, Ruteo Eléctrico SEC RIC N° 03/10, Acústica Espacial Haas, Dimensionamiento de Potencias Pasivas y Cotización Operativa  
**Fecha de Entrega:** Noviembre de 2026

---

## RESUMEN EJECUTIVO

**STAGE PLAN** es una plataforma web responsiva de pre-producción electroacústica desarrollada y validada para la empresa contraparte **DISTORSIONCL SPA** (operador técnico Amaro Artiaga), en el marco de la Unidad 2 de Proyecto Integrado (`TIHV43`, Sección C1, Grupo G10, INACAP Sede Maipú). La solución sustituye el dimensionamiento empírico sin cálculo normativo de instalaciones temporales de sonido, cableado de escenario y fuerza eléctrica, aplicando de forma determinista los Pliegos Técnicos Normativos **SEC RIC N° 03 y RIC N° 10**, el **Decreto Supremo N° 38 MMA** sobre emisión de ruidos y la **Ley N° 20.949** (Ley del Saco).

Este documento consolida los seis ejes técnicos de diseño: (1) planificación ágil **Scrumban + PSP** en 4 Sprints de 14 días (20 tareas con ruta crítica y tablero Kanban `WIP = 1`); (2) arquitectura **4+1 (ISO/IEC/IEEE 42010:2022)** en monorepo TypeScript (`@stageplan/frontend`, `@stageplan/shared`, `@stageplan/backend`); (3) experiencia **UX/UI Dark Mode FOH (WCAG 2.1 AA)** en formato **Studio Cockpit** calibrado al 100% de zoom con 5 vistas en Vue Router, plano vectorial 2D por 5 capas exclusivas (**Blueprint Dark**) con Vista Completa consolidada en reporte, postes guía SEC RIC N° 10, dimensionamiento automático de rack de potencias pasivas, cotizador de arriendo en CLP, réplica Pioneer DJM y exportación **PDF Dual-Page** + **PNG 300 DPI**; (4) persistencia híbrida en **SQLite 3 (`dev.db`)** con Prisma ORM (4 tablas normalizadas 3FN en español + documentos JSON) y esquema objetivo proyectado para **PostgreSQL 16**; (5) estándares de programación segura con Zod, `bcrypt` (cost 12), bloqueo temporal `HTTP 423`, `express-rate-limit`, control Anti-IDOR (`HTTP 404`), `errorHandler` y matriz **OWASP Top 10 (2021)**; y (6) aseguramiento de calidad verificado con **81 pruebas unitarias en Vitest (11 archivos, 100% PASS en 186 ms)** y latencia promedio medida de **0,0286 ms**.

> *Nota metodológica de alcance (Unidad 2 — Diseño y Prueba de Concepto):* Conforme a la Guía ABPRO Unidad 2, este informe corresponde a la fase de Diseño de la Solución. El prototipo operativo y las 81 pruebas TDD se presentan como Prueba de Concepto (PoC) verificable en local, manteniendo para la etapa de construcción (Unidad 3) el despliegue en VPS Linux con PostgreSQL 16, bitácora `audit_logs`, pruebas de carga `k6` y escaneo `OWASP ZAP`.

---

## ACTIVIDADES FORMATIVAS DE LA UNIDAD 2 (GUÍA ABPRO)

### Parte 1: Brainstorming Categorizado

| Categoría Temática | Ideas Levantadas en Lluvia de Ideas | Problemática Resuelta en Terreno |
| :--- | :--- | :--- |
| **1. Seguridad Eléctrica SEC** | I1: Calibre automático ($\Delta V \le 3\%$); I2: Líneas aisladas L1/L2/L3; I3: Postes guía esquineros ($R \ge 6d$, RIC N° 10). | Disparos termomagnéticos, calentamiento Joule y fatiga mecánica de conductores. |
| **2. Acústica y Gain Staging** | I4: Clúster mono de subs (+6 dB); I5: Retardos Haas para Delays; I6: Réplica Pioneer DJM (VU vertical + Low Kill). | Saturación (*clipping*), cancelaciones de graves y daño de bobinas. |
| **3. Equipamiento Mixto y Potencias** | I7: Lotes Activa/Pasiva con cálculo de rack de potencias (headroom 1,6×) y alerta Speakon ($< 3,2\ \Omega$); I8: Carga AC 220V de etapas. | Apagado en modo PROTECT, subdimensionamiento de amplificadores y distorsión térmica. |
| **4. Logística y Costos** | I9: Alerta Ley del Saco N° 20.949; I10: Lista cables poder/señal; I11: Plan B; I16: Cotizador de arriendo CLP. | Lesiones lumbares, olvido de cables, parálisis ante falla y falta de presupuesto rápido. |
| **5. Operación Autónomo-Terreno** | I12: Plano 2D Blueprint por capas y vista completa en reporte; I13: PDF Dual-Page + PNG 300 DPI; I14: WhatsApp; I15: SharedLink. | Ruido visual al configurar, parcelas rurales sin 4G/5G y descoordinación en despacho. |

### Parte 2: Matriz de Priorización Ponderada

| Ranking | Propuesta Evaluada | Imp. (40%) | Viab. (30%) | Urg. (30%) | Puntaje | Decisión de Alcance |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | I1+I2: Cálculo SEC RIC 03/10 ($\Delta V \le 3\%$) y separación L1/L2/L3 | 5.0 | 5.0 | 5.0 | **5.00** | MVP Obligatorio (S1–S2) |
| **2** | I7+I8: Lotes Activa/Pasiva, Rack de Potencias y alerta Speakon $< 3,2\ \Omega$ | 5.0 | 4.8 | 4.8 | **4.88** | MVP Obligatorio (S2–S4) |
| **3** | I3+I12: Plano 2D Blueprint por capas + Postes Guía RIC 10 ($R \ge 6d$) | 4.9 | 4.5 | 5.0 | **4.81** | Core (S4) |
| **4** | I4+I5+I6: Clúster Mono + Delays Haas + Réplica Pioneer DJM | 4.6 | 4.7 | 4.5 | **4.60** | Core (S4) |
| **5** | I9+I10+I13: D.S. N° 38 MMA + Ley del Saco + PDF Dual-Page Offline | 4.5 | 4.6 | 4.2 | **4.44** | Core (S3–S4) |
| **6** | I11+I14+I16: Plan B + WhatsApp + Cotizador de Arriendo CLP | 4.1 | 4.8 | 3.9 | **4.25** | Complemento (S4) |

---

## 1. METODOLOGÍA DE DESARROLLO Y PLANIFICACIÓN

### 1.1 Selección y justificación (Scrumban + PSP)
Dado el desarrollo individual por Mauricio Vega Castillo (Sección C1, Grupo G10), se adoptó **Scrumban + PSP (*Personal Software Process*)**: cuatro Sprints de 14 días, tablero Kanban con `WIP = 1` en curso y compuerta automatizada TDD (`vue-tsc` + `tsc` + **81 pruebas Vitest**) que reemplaza la revisión por pares.

### 1.2 Cronograma, Recursos y Ruta Crítica (`T01`–`T20`)
- **Dedicación:** 180 horas totales (M. Vega) + 8 horas de validación en terreno con Amaro Artiaga (*DISTORSIONCL SPA*).
- **Ruta Crítica (holgura = 0 días):** `T01 → T02 → T04 → T05 → T06 → T08 → T09 → T10 → T12 → T13 → T15 → T18 → T20`.
- **Seguimiento:** Jira Software + GitHub (`https://github.com/MauricioVega01/stage-plan`, rama `main`).
- **Figura 1:** [diag-01-scrumban-cronograma-kanban.png](file:///C:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/entrega_sumativa_02/diagrams/diag-01-scrumban-cronograma-kanban.png).

---

## 2. ARQUITECTURA DE LA SOLUCIÓN – PARADIGMA 4+1 (ISO/IEC/IEEE 42010:2022)

1. **Stack Tecnológico Real:**
   - **Frontend SPA:** Vue 3.5 + Vite 6.4 + Vue Router 4 (5 rutas: `/auth`, `/recinto`, `/equipos`, `/plano-2d`, `/reporte`) + Tailwind CSS 3.4 + composable `useStagePlanState.ts` con persistencia automática en `localStorage`.
   - **Núcleo Isomórfico (`@stageplan/shared`):** TypeScript 5.7 + Zod 3.24 (11 módulos puros + 11 suites Vitest con **81 tests**).
   - **Backend API (`@stageplan/backend`):** Node.js 24 + Express 4.21 + Helmet + CORS + `express-rate-limit` + `bcrypt` (cost 12) + JWT (`12h`) + Prisma ORM 6.4 sobre **SQLite 3 (`dev.db`)** en PoC (proyectado a **PostgreSQL 16** en Unidad 3).
   - **Salida Terreno:** `jsPDF` 2.5 + `jspdf-autotable` + rasterización SVG/Canvas (PDF Dual-Page y PNG 300 DPI client-side).
2. **Las 5 Vistas del Modelo 4+1:**
   - Escenarios (`diag-03`), Lógica (`diag-04`), Desarrollo (`diag-05`), Procesos BPMN 2.0 (`diag-06`) y Física/Despliegue (`diag-02`).

---

## 3. DISEÑO DE EXPERIENCIA E INTERFAZ DE USUARIO (UX/UI)

- **Studio Cockpit Fullscreen (100% Zoom):** Grilla `100vh` sin desplazamiento vertical global en escritorio (`1440×900`) y adaptable a smartphone (`412×915`), paleta Dark Mode FOH (`#080a10`) WCAG 2.1 AA (`≥ 4.5:1`) y telemetría fija en barra superior e inferior.
- **Retroalimentación con DISTORSIONCL SPA (4 Iteraciones):**
  - *Iteración 1:* Presets 1-clic y copia rápida a WhatsApp.
  - *Iteración 2:* Lotes Activa/Pasiva con cables XLR/Speakon sin sobrantes.
  - *Iteración 3:* Postes guía SEC RIC N° 10 ($R \ge 6d$) y réplica hardware Pioneer DJM (`17 LEDs` + *Low Kill*).
  - *Iteración 4:* Studio Cockpit al 100% de zoom, Plano 2D Blueprint con 5 capas exclusivas (y Vista Completa `ALL` en `/reporte`), dimensionamiento de Rack de Potencias Pasivas (`calculatePowerAmpSizing`, headroom 1,6×), Cotizador de Arriendo CLP y PDF Dual-Page + PNG 300 DPI.

---

## 4. MODELO Y ADMINISTRACIÓN DE BASE DE DATOS

- **Implementación PoC (SQLite 3 `dev.db` + Prisma ORM):** 4 tablas normalizadas 3FN en español (`usuarios` incluyendo `intentos_fallidos` y `bloqueado_hasta`, `recintos`, `calculos_rider` con 4 columnas JSON, y `enlaces_compartidos`), auditables con `json_extract` en *DB Browser for SQLite* (Figura 12: `diag-07-modelo-datos-der.png`).
- **Proyección Producción Unidad 3 (PostgreSQL 16):** Esquema físico extendido de 12 tablas en `entrega_sumativa_02/sql/schema_stageplan_pg16.sql` con JSONB, índices GIN, triggers `CHECK`, `audit_logs` y `pgcrypto`.

---

## 5. ESTÁNDARES DE PROGRAMACIÓN SEGURA Y OWASP TOP 10 (2021)

- **Implementado en PoC:** Validación Zod en frontera (`HTTP 400`), `bcrypt` (12 rondas), `loginLimiter` (`10 req/15m`), `apiLimiter` (`200 req/15m`), bloqueo temporal por 15 minutos tras 5 fallos (`HTTP 423 Locked`), JWT (`12h`) validado en `authMiddleware` con exigencia fatal de `JWT_SECRET` en producción, control Anti-IDOR por `ownerId` en `VenueController` y `CalculationController` retornando `HTTP 404` (evita enumeración de UUIDs), `helmet()`, CORS acotado y manejo centralizado `errorHandler` sin fuga de *stack traces*.
- **Proyectado Unidad 3:** RBAC multi-rol granular, endpoints de `enlaces_compartidos`, tabla `audit_logs`, cookies `HttpOnly; SameSite=Strict`, `token_version`, TLS 1.3 + HSTS y `pgcrypto`.

---

## 6. PLAN DE PRUEBAS Y ASEGURAMIENTO DE LA CALIDAD

- **Vitest v3.2.7 (`packages/shared`):** **11 archivos passed (11), 81 tests passed (81), 186 ms en ejecución de tests**.
- **Chequeo estático y build (`npm run lint`, `npm run build`):** `tsc` + `vue-tsc` + `vite build` con **0 errores**.
- **Benchmark (1.000 iteraciones):** `0,0286 ms` promedio (`p95 = 0,0479 ms`, `< 50 ms` SLA).
- **Verificación E2E en navegador:** Inspección de rutas, presets, rack pasivo, capas Blueprint, cotizador de arriendo y exportación PDF Dual-Page al 100% de zoom y vista móvil `412×915`.

---

## CONCLUSIONES Y TRAZABILIDAD

1. **Cumplimiento de ingeniería:** Transformación del montaje empírico hacia pre-producción determinista bajo SEC RIC N° 03/10, D.S. N° 38 MMA, Ley del Saco N° 20.949, amplificación pasiva y costos CLP.
2. **Scrumban + PSP:** Desarrollo individual controlado mediante `WIP = 1`, compilación estricta y 81 tests TDD.
3. **Arquitectura 4+1 y Persistencia Híbrida:** Separación limpia en monorepo TypeScript y coexistencia ordenada entre `dev.db` (PoC SQLite) y `schema_stageplan_pg16.sql` (Producción U3).
4. **Usabilidad y Seguridad:** Cockpit 100% zoom, PDF Dual-Page autónomo y controles defensivos implementados en API.

> **Versión oficial compilada para entrega:** [Proyecto_Integrado_U2_Mauricio_Vega_G10_FINAL.docx](file:///C:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/entrega_sumativa_02/Proyecto_Integrado_U2_Mauricio_Vega_G10_FINAL.docx)
