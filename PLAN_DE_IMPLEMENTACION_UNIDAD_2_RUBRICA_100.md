# PLAN DE IMPLEMENTACIÓN ESTRATÉGICO: UNIDAD 2 (RÚBRICA TIHV43)
## Asignatura: Proyecto Integrado (TIHV43) – INACAP Sede Maipú
### Proyecto: STAGE PLAN (v4.0) | Autor: Mauricio Vega Castillo | Sección: C1 · Grupo: G10

---

## 1. IDENTIFICACIÓN Y CONTEXTO DEL PROYECTO

- **Institución:** Instituto Profesional INACAP – Sede Maipú.
- **Carrera:** Analista Programador / Ingeniería en Informática.
- **Asignatura:** Proyecto Integrado (Código: TIHV43) | **Sección:** C1 | **Grupo:** G10.
- **Evaluación:** Evaluación Sumativa 2 (Ponderación 100 puntos / Escala 1.0 a 7.0).
- **Alumno / Desarrollador:** Mauricio Vega Castillo.
- **Modalidad Operativa:** Solo-Developer (Desarrollo individual bajo marco formal Scrumban + Personal Software Process).
- **Caso de Estudio / Cliente:** Productora y Arriendo de Audio DISTORSIONCL SPA.
- **Solución Tecnológica:** STAGE PLAN (v4.0) – Monorepo TypeScript (Vue 3 + Vue Router 4 + Node.js/Express + Prisma ORM + SQLite `dev.db` [Proy. U3: PostgreSQL 16] + Vitest TDD).

---

## 2. DIAGNÓSTICO RETROSPECTIVO: CORRECCIONES RESPECTO A LA ENTREGA 1

| Debilidad Detectada en la Entrega 1 | Causa Raíz en Rúbrica Académica | Corrección Aplicada en la Entrega 2 |
| :--- | :--- | :--- |
| **Inconsistencia de equipo** | Figuraba "Grupo G10" pero en el cuerpo decía "Desarrollador Único" sin justificación formal. | Se adopta el marco formal **Scrumban + PSP**. Se justifica cómo se compensa la falta de equipo mediante un **Quality Gate automatizado (81 tests TDD + `vue-tsc`/`tsc`)**. |
| **Formato y carátula rota** | Placeholders de Word sin rellenar y títulos pegados. | Estructura limpia, tipografía institucional (`Open Sans`), carátula oficial completa (Sede Maipú · C1 · G10 · Docente Manuel Rojas) y eliminación total de placeholders. |
| **Lenguaje coloquial** | Uso de modismos informales en la redacción técnica. | Redacción impersonal formal con vocabulario de ingeniería: *"dimensionamiento empírico sin cálculo normativo"*, *"canalización superficial con cinta gaffer según protocolo"*, *"acometidas bajo pliego SEC RIC N° 10"*. |
| **Cronograma plano** | Tabla genérica de 6 semanas sin dependencias reales ni horas estimadas. | Cronograma formal de 4 Sprints y 20 tareas (`T01`–`T20`), 180 horas-hombre estimadas, estimación MoSCoW y **Ruta Crítica** explícita. |
| **Falta de rigor en casos de uso** | Descripciones breves sin estructura formal. | Especificación estructurada con precondiciones, flujos principales y excepciones numeradas conectadas a las operaciones de clase. |

---

## 3. MATRIZ MAESTRA DE CUMPLIMIENTO DE RÚBRICA (15 CRITERIOS / 100 PUNTOS)

| Criterio Rúbrica | Pts | Exigencia de Nivel Superior INACAP | Evidencia en STAGE PLAN (v4.0) |
| :--- | :---: | :--- | :--- |
| **2.1.1.1. Metodología y fases** | 5 | Actividades y fases alineadas, con plazos y responsables asignados. | Metodología Scrumban + PSP. Cronograma de 4 Sprints y 20 tareas (`T01`–`T20`, 180 hrs) asignadas a Mauricio Vega Castillo. |
| **2.1.1.2. Dependencias y prioridades** | 5 | Dependencias y prioridades correctamente identificadas. | Backlog MoSCoW, dependencias Finish-to-Start y ruta crítica explícita (`T01→...→T20`). |
| **2.1.2.3. Paradigma 4+1 (ISO 42010)** | 5 | Los 5 puntos de vista definidos con precisión y alineados a la solución. | Vistas Escenarios (`CU-00`..`CU-08`), Lógica (Clases), Desarrollo (Monorepo), Procesos (BPMN 2.0) y Física (PoC local + VPS U3). |
| **2.1.2.4. Tecnologías e infraestructura** | 5 | Identificación justificada considerando necesidades futuras. | Vue 3.5 + Vite 6.4 + Vue Router 4 + Tailwind 3.4 + `useStagePlanState` (`localStorage`); TypeScript/Zod; Node 24/Express 4.21; SQLite/Prisma (PoC) → PostgreSQL 16 (U3); `jsPDF`. |
| **2.1.3.5. Prototipos interactivos** | 5 | Prototipo completamente funcional cubriendo interacciones clave. | Cockpit 100% zoom con 5 rutas URL, Rack de Potencias Pasivas (`1.6×`), Plano Blueprint 5 capas, Pioneer DJM, Cotizador Arriendo CLP y PDF Dual-Page + PNG 300 DPI. |
| **2.1.3.6. Consistencia visual y adaptabilidad** | 5 | Diseño consistente y adaptable a múltiples dispositivos. | Dark Mode técnico FOH (`#080a10`), contraste WCAG 2.1 AA, responsive para escritorio (`1440×900`) y smartphone (`412×915`). |
| **2.1.3.7. Retroalimentación de usuarios** | 5 | Retroalimentación integrada en iteraciones verificables. | 4 iteraciones documentadas junto a Amaro Artiaga (DISTORSIONCL SPA), incluyendo Blueprint por capas, Rack Pasivo, Arriendo CLP y PDF Dual-Page. |
| **2.1.4.8. Entidades y relaciones óptimas** | **10** | Modelo completo con integridad referencial PK/FK. | DER en 3FN implementado en SQLite `dev.db` y Prisma (`usuarios`, `recintos`, `calculos_rider`, `enlaces_compartidos` con UUIDs y `ON DELETE CASCADE`) + proyección PG16 (12 tablas). |
| **2.1.4.9. Bases estructuradas y no estructuradas** | 5 | Uso eficaz de datos estructurados y semiestructurados con ejemplos reales. | Modelo híbrido: tablas relacionales 3FN + columnas `JSON` consultables mediante `json_extract` en DB Browser (proyectado a `JSONB` con índices GIN en PG16 U3). |
| **2.1.5.10. Autenticación y autorización** | **10** | Políticas robustas alineadas a buenas prácticas. | `bcrypt` (cost 12), JWT (`12h`) en `authMiddleware`, bloqueo temporal `HTTP 423` tras 5 fallos, `loginLimiter` (`10/15m`) y Anti-IDOR `ownerId` (`HTTP 404`); RBAC multi-rol y cookies `HttpOnly` proyectados para U3. |
| **2.1.5.11. Amenazas y mitigación (OWASP)** | **10** | Identificación de amenazas con medidas documentadas. | Matriz completa OWASP Top 10 (A01–A10) diferenciando controles implementados en PoC (Prisma parametrizado, Zod, Helmet, CORS, Anti-IDOR 404) y controles de despliegue U3 (`audit_logs`, `pgcrypto`, TLS 1.3). |
| **2.1.5.12. Estándares de codificación segura** | **10** | Estándares documentados e implementados. | Validación Zod isomórfica en frontera, `helmet()`, `asyncHandler` + `errorHandler` sin fuga de *stack traces* y verificación estricta de `JWT_SECRET` en producción. |
| **2.1.6.13. Pruebas unitarias, integrales y rendimiento** | **10** | Plan de pruebas ejecutado con evidencia. | **81/81 pruebas unitarias TDD aprobadas en 11 archivos Vitest (`186 ms`)** + benchmark medido de `0,0286 ms` promedio (1.000 iteraciones); pruebas `k6` acotadas a U3. |
| **2.1.6.14. Herramientas automatizadas y manuales** | 5 | Uso balanceado y efectivo de herramientas. | Automatizadas: Vitest v3.2.7, `vue-tsc`, `tsc`, Vite. Manuales / E2E: Puppeteer/DevTools (`1440×900` y `412×915`) y validación en terreno. |
| **2.1.6.15. Responde preguntas del profesor** | 5 | Respuestas claras con fundamentos técnicos sólidos. | Preparación privada en `GUION_PRESENTACION_PROFESOR.md` (fórmulas SEC RIC N° 03/10, acústica Haas, arquitectura, BD y OWASP). |

---

## 4. ESPECIFICACIÓN TÉCNICA REAL DEL PROYECTO

### 4.1 Motor de Ingeniería (`@stageplan/shared` — 11 módulos y 81 tests en 11 archivos)
1. **Caída de Tensión (SEC RIC N° 10):** $\Delta V = \frac{2 \cdot L \cdot I \cdot \rho}{S}$, $\Delta V_{\%} = \left(\frac{\Delta V}{220}\right)\cdot 100 \le 3\%$ ($\rho = 0.0175\ \Omega\cdot\text{mm}^2/\text{m}$).
2. **Impedancia Speakon y Rack Pasivo (`hybrid-roster.ts`):** $\frac{1}{Z_{eq}} = \sum \frac{1}{Z_i}$ (alerta si $Z_{eq} < 3.2\ \Omega$); `calculatePowerAmpSizing` dimensiona amplificadores con headroom $1.6\times$ RMS y calcula carga AC 220V.
3. **Atenuación Acústica (Sabine RT60 / Campo Libre):** $\text{SPL}(d) = \text{SPL}_{1m} - 20 \cdot \log_{10}(d)$.

### 4.2 Archivos Oficiales de Entrega (Evaluación Sumativa 2)
- `entrega_sumativa_02/Proyecto_Integrado_U2_Mauricio_Vega_G10_FINAL.docx` (Informe Word oficial compilado vía `generate_sumativa_02_docx.py`).
- `entrega_sumativa_02/diagrams/` (8 diagramas regenerados vía `generate_u2_diagrams.py`).
- `entrega_sumativa_02/prototipo/capturas/` (capturas reales al 100% zoom + móvil + mosaico).
- `entrega_sumativa_02/sql/dev.db` y `entrega_sumativa_02/sql/schema_stageplan_pg16.sql`.
- `Grupo G10_Seccion C1_Mauricio_Vega.zip` (paquete consolidado final sin archivos `.env`).
