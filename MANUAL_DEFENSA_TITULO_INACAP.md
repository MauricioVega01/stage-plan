# MANUAL DE DEFENSA DEL PROYECTO: STAGE PLAN (v4.0)
**Carrera:** Analista Programador — INACAP Sede Maipú (Sección C1 · Grupo G10)  
**Asignatura:** Proyecto Integrado (`TIHV43`)  
**Autor:** Mauricio Vega Castillo | **Docente:** Manuel Rojas  
**Cliente del Caso de Estudio:** Productora y Arriendo de Audio *DISTORSIONCL SPA*

---

## 1. El Problema Real (Pitch de Apertura)
> *"En eventos de música en vivo y formato DJ en Chile, la mayoría de las fallas en terreno ocurren por ausencia de pre-producción normativa: cortes de energía por sobrecargar disyuntores de 10A, protección térmica en amplificadores pasivos por baja impedancia Speakon, caídas de tensión en alargadores extensos y desbalance acústico hacia la pista o viviendas cercanas.*  
> *Además, muchos montajes ocurren en parcelas rurales (Curacaví, Lampa, Pirque) sin cobertura móvil estable.*  
> ***STAGE PLAN (v4.0)*** *automatiza el cálculo eléctrico SEC (RIC N° 03 y N° 10), la acústica espacial Haas, el dimensionamiento de rack de potencias pasivas, la cotización diaria en CLP y genera un Plano CAD 2D junto a un Reporte PDF Dual-Page utilizable sin internet."*

---

## 2. Decisiones de Arquitectura y Justificación Técnica

### 2.1 Monorepo TypeScript (`npm workspaces`) y `@stageplan/shared`
- **Problema que resuelve:** Evita duplicar fórmulas físicas y reglas de validación entre cliente y servidor (*contract drift*).
- **Implementación actual:**
  - **`@stageplan/shared`:** Esquemas Zod (`VenueSchema`, `RiderSchema`, `EngineeringParamsSchema`) y 11 módulos `calc-engine` (`electrical.ts`, `acoustics.ts`, `hybrid-roster.ts` con `calculatePowerAmpSizing`, `stage-acoustic-engine.ts`, `cabling.ts`, etc.).
  - **`@stageplan/backend`:** API REST Express 4.21 + Prisma ORM 6.4 sobre SQLite 3 (`dev.db`) con migración proyectada a PostgreSQL 16 (`schema_stageplan_pg16.sql`). Recalcula en servidor sin confiar en totales enviados desde el cliente.
  - **`@stageplan/frontend`:** SPA Vue 3.5 + Vite 6.4 + Vue Router 4 (5 vistas en diseño Studio Cockpit 100% zoom) + `useStagePlanState.ts` (`localStorage`).

### 2.2 Operación Autónoma en Terreno con PDF Dual-Page y PNG 300 DPI
- La pre-producción se ejecuta en navegador y persiste automáticamente en `localStorage`.
- `pdfReport.ts` compila client-side con `jsPDF` un reporte de 2 páginas: **Página 1** (Memoria técnica SEC, inventario, rack pasivo, Ley del Saco y presupuesto CLP) y **Página 2** (Lámina horizontal CAD 2D con todas las capas activas), además de exportar el plano como **PNG 300 DPI** para mensajería rápida.

### 2.3 Seguridad de la Información y OWASP Top 10
- **Anti-IDOR (A01):** Toda operación sobre `Venue` o `RiderCalculation` exige `ownerId === req.user.id` en Prisma ORM, retornando **`HTTP 404`** si el recurso no pertenece al usuario autenticado (evitando enumeración de UUIDs).
- **Inyecciones SQL y XSS (A03):** Consultas parametrizadas con Prisma ORM, validación Zod en frontera y auto-escapado nativo de Vue 3 sin uso de `v-html`.
- **Autenticación y Fuerza Bruta (A02/A07):** Contraseñas hasheadas con **`bcrypt` (12 rondas)**, JWT firmado (`12h`), `loginLimiter` (**10 peticiones / 15 min**) y bloqueo temporal de cuenta por 15 minutos tras 5 fallos retornando **`HTTP 423 Locked`**.
- **Cabeceras y Manejo de Errores (A05/A09):** `helmet()`, CORS acotado a `FRONTEND_URL`, `asyncHandler` y `errorHandler` centralizado sin exposición de *stack traces*.

---

## 3. Casos Numéricos Verificables en Demostración

### Caso 1: Caída de Tensión y Selección de Conductor (SEC RIC 03/10)
- **Entrada:** Carga de $1.800\text{ W}$, distancia $30\text{ m}$, $220\text{ V}$, holgura $20\%$, caída máxima $\le 3\%$.
- **Resultado:** Corriente de diseño $9,82\text{ A}$; sección comercial adoptada **$2,5\text{ mm}^2$**; metraje sugerido $33\text{ m}$; caída real resultante **$4,12\text{ V}$ ($1,87\%$)**.

### Caso 2: Detección de Sobrecarga en Enchufe 10A
- **Entrada:** $2.000\text{ W}$ en circuito $10\text{ A}$ → corriente de diseño $10,91\text{ A}$ ($109\%$).
- **Resultado:** Alerta crítica por riesgo inminente de disparo termomagnético.

### Caso 3: Audio Pasivo, Impedancia Speakon y Rack de Potencias
- **2 tops pasivos $400\text{ W}$ RMS @ $8\ \Omega$ en canales independientes:** Headroom $1,6\times$ → exige **$640\text{ W}$ RMS/canal @ $8\ \Omega$** más carga AC 220V integrada al cálculo SEC.
- **3 cajas $8\ \Omega$ en paralelo:** $Z_{eq} = 2,67\ \Omega < 3,2\ \Omega$ → alerta roja `DANGER_PROTECT_SHORT` por riesgo de corte en modo PROTECT.

---

## 4. Métricas Verificadas de Calidad (Vitest + TypeScript)
- **Pruebas unitarias TDD:** **81/81 tests aprobados en 11 archivos** (`100% PASS` en `186 ms` de ejecución de tests).
- **Rendimiento del motor:** Latencia promedio de `0,0286 ms` en 1.000 iteraciones.
- **Compilación estricta:** `tsc --noEmit`, `vue-tsc --noEmit` y `vite build` con **0 errores**.
