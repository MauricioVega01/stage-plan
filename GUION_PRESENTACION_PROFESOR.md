# GUION DE PRESENTACIÓN Y DEFENSA PRIVADO: STAGE PLAN (v4.0)
**Caso de Estudio:** Productora y Arriendo de Audio *DISTORSIONCL SPA*  
**Asignatura:** Proyecto Integrado (`TIHV43`) — INACAP Sede Maipú — Sección C1 · Grupo G10  
**Estudiante:** Mauricio Vega Castillo | **Docente:** Manuel Rojas

> *(Documento privado de preparación para la exposición oral ante comisión docente. No se adjunta en el informe Word oficial.)*

---

## 3 PILARES ESTRATÉGICOS PARA DEFENDER ANTE LA COMISIÓN

1. **Sistema Experto de Ingeniería Preventiva (no es un CRUD genérico):** Transforma parámetros simples del evento (medidas del salón o parcela, lotes combinados activos/pasivos, red 10A/16A o generador comercial) en cálculos deterministas de electroacústica, electrotecnia SEC RIC N° 03/10, rack de potencias para pasivos y presupuesto operativo en CLP.
2. **Estética Studio Cockpit 100% Zoom + Plano CAD Blueprint por Capas:** Por dentro ejecuta cálculos físicos estrictos (`@stageplan/shared`, `0,0286 ms`); por fuera entrega un entorno Dark Mode FOH libre de desplazamiento vertical global al 100% de zoom, con plano vectorial por 5 capas exclusivas (sin saturación visual al configurar), capa consolidada completa en `/reporte`, simulador Pioneer DJM, descarga PNG (300 DPI) y PDF Dual-Page offline.
3. **Calidad Verificable con 81 Pruebas Unitarias TDD (Vitest):** Las 11 suites en `@stageplan/shared` pasan al 100% (`81/81` en `186 ms`), verificando fórmulas SEC, impedancia Speakon, rack de potencias (`PA-01..PA-06`), división de líneas L1/L2/L3, retardos Haas, rutas DMX y Ley del Saco.

---

## ESTRUCTURA DE PRESENTACIÓN (8 A 10 MINUTOS)

### LÁMINA 1: Portada e Identidad del Proyecto
> "Buenos días profesor Manuel Rojas. Presento **Stage Plan (v4.0)**, plataforma web de pre-producción electroacústica, seguridad eléctrica SEC y gestión logística desarrollada para **DISTORSIONCL SPA** en **INACAP Sede Maipú** (Sección C1, Grupo G10). Resuelve un problema concreto en eventos en salones y parcelas: garantizar sonido potente y nítido combinando cajas activas y pasivas sin quemar etapas de potencia, sin botar automáticos y sin apagar generadores en los golpes de graves."

### LÁMINA 2: Diagnóstico del Problema en Terreno
> "Al levantar requerimientos con Amaro Artiaga identificamos cinco fallos recurrentes cuando se trabaja con dimensionamiento empírico sin cálculo normativo:
> 1. **Colapso de suministro en el drop:** Sobrecarga de circuitos de 10A (~1.760W continuos seguros) o generadores comerciales de 3.500W pico (cuya capacidad continua estable para audio ronda los ~2.142W tras el factor AVR del 72%).
> 2. **Saturación en mezclas híbridas:** Combinar cajas activas frontales con pasivas de menor potencia sin ajustar ganancia ni dimensionar adecuadamente el rack de potencias externa.
> 3. **Protección de amplificadores por impedancia:** Cargas pasivas en paralelo bajo 3,2 Ω activan el modo `PROTECT` del amplificador.
> 4. **Cancelación de graves:** Ubicar subwoofers separados en vez de agruparlos en clúster mono central a piso (+6 dB).
> 5. **Operación en parcelas sin cobertura móvil:** Necesidad de llevar la memoria técnica y el plano CAD resueltos en PDF offline."

### LÁMINA 3: Arquitectura Modular y Capacidades v4.0 (Demo en Vivo)
> - **Vista 0 (`/auth`) y Vista 1 (`/recinto`):** Login seguro y 8 presets rápidos más evaluación normativa de ruido vecinal D.S. N° 38 MMA.
> - **Vista 2 (`/equipos`):** Lotes Activo/Pasivo con **Rack de Potencias Sugerido** (headroom 1,6× RMS, impedancia 4/8 Ω, modelos *Crown / Powersoft / Lab Gruppen* y carga AC 220V sumada a la validación SEC).
> - **Vista 3 (`/plano-2d`):** Plano CAD Blueprint por **5 capas exclusivas** (inicia limpio en *Arquitectura & Audio*), postes guía SEC RIC N° 10 ($R \ge 6d$), simulador hardware **Pioneer DJM** y **Plan B**.
> - **Vista 4 (`/reporte`):** Previsualización del plano con **todas las capas activas (`Vista Completa`)**, descarga **PNG 300 DPI**, **Cotizador de Arriendo CLP** (Propios vs. Arriendo) y exportación **PDF Dual-Page** (Pág. 1 Memoria SEC + costos; Pág. 2 Lámina CAD horizontal).

---

## BANCO PRIVADO DE 21 PREGUNTAS Y RESPUESTAS PARA DEFENSA ORAL

1. **¿Por qué eligió Scrumban + PSP en vez de Scrum tradicional?** Porque Scrum puro exige ceremonias pensadas para equipos numerosos; Scrumban aporta Sprints de 14 días con límite `WIP = 1`, y PSP reemplaza la revisión por pares mediante compilación estricta (`vue-tsc` + `tsc`) y 81 pruebas automatizadas en Vitest.
2. **¿Cuál es la ruta crítica del cronograma?** `T01 → T02 → T04 → T05 → T06 → T08 → T09 → T10 → T12 → T13 → T15 → T18 → T20` (holgura = 0 días).
3. **¿Por qué separar `@stageplan/shared` en un monorepo?** Para ejecutar exactamente las mismas fórmulas físicas y esquemas Zod tanto en el navegador offline (`0,0286 ms`) como en el backend Express sin duplicar lógica.
4. **¿Qué estándar respalda las 5 vistas arquitectónicas?** La norma **ISO/IEC/IEEE 42010:2022** aplicada mediante el modelo **4+1 de Kruchten** (Escenarios, Lógica, Desarrollo, Procesos y Física).
5. **¿Cómo aplica la normativa SEC RIC N° 03 y RIC N° 10 en el código?** Evaluando doble criterio en `electrical.ts`: caída de tensión monofásica $\Delta V = \frac{2 \cdot L \cdot I \cdot \rho}{S} \le 3\%$ y ampacidad con $+20\%$ de holgura, además de postes guía esquineros con radio mínimo $R \ge 6d$.
6. **¿Por qué incluir postes guía esquineros en el Plano 2D?** Doblar cables multifilares en ángulos de $90^\circ$ fatiga el cobre y genera calentamiento Joule; los postes aseguran $R \ge 6d$ según RIC N° 10 y mantienen despejada la pista.
7. **¿Por qué los subwoofers van en un clúster central a piso?** Al agruparlos a menos de $\lambda/2$ (`< 1,7 m` a 100 Hz) sobre el suelo se acoplan en fase ganando $+6\text{ dB}$ acústicos sin consumo eléctrico adicional.
8. **¿Cómo calcula el Efecto Haas en las torres Delay?** Suma al tiempo de vuelo acústico ($v = 331.3 + 0.606 \cdot T$) una compensación psicoacústica Haas (`+3.0 ms`), manteniendo la localización sonora en el escenario frontal.
9. **¿Qué ocurre si se conectan 3 cajas pasivas de $8\ \Omega$ en paralelo?** La impedancia cae a $Z_{eq} = 8/3 = 2.67\ \Omega < 3.2\ \Omega$; el sistema activa la alerta roja `DANGER_PROTECT_SHORT` por riesgo de corte térmico en la etapa.
10. **¿Cómo dimensiona el Rack de Potencias cuando hay cajas pasivas?** En `calculatePowerAmpSizing` agrupa tops y subs pasivos por canal, calcula la impedancia de carga (4 Ω vs 8 Ω según cableado), aplica un headroom de **1,6× RMS** (`PA-02..PA-03`), sugiere amplificadores comerciales y suma su consumo eléctrico continuo a la red 220V.
11. **¿Qué demuestra el simulador Pioneer DJM?** Que se debe operar con un solo canal de graves activo (`0 dB`) y el entrante en *Low EQ Kill* (`-∞` a las 7:00), evitando sumar `+6 dB` en graves y disparar los 17 LEDs al rojo `CLIP`.
12. **¿Por qué el plano 2D tiene 5 capas exclusivas en `/plano-2d` y vista completa en `/reporte`?** Al configurar, mostrar todas las líneas a la vez generaba ruido visual; las capas exclusivas facilitan editar cada subsistema limpio, mientras que en el reporte final se consolida la vista completa (`ALL`) para inspección integral en terreno y PDF.
13. **¿Cómo funciona el módulo de Cotización de Arriendo CLP?** Permite alternar entre *Equipos Propios* y *Rider Arrendado*, estimando costo diario para tops, subs, racks de potencia, generador, luminarias DMX y técnicos de montaje, e incorporando el desglose en la Página 1 del PDF.
14. **¿Cómo aplica la Ley del Saco (Ley N° 20.949)?** `contingency-and-logistics.ts` detecta cualquier bulto mayor a `25 kg` y agrega la directiva obligatoria de manipulación entre dos personas o carro.
15. **¿Por qué usa SQLite `dev.db` en la PoC y PostgreSQL 16 en producción?** SQLite 3 con Prisma ORM (4 tablas 3FN en español + JSON) ofrece portabilidad total en local y auditoría directa en DB Browser; para Unidad 3 Prisma migra de forma transparente a PostgreSQL 16 (`schema_stageplan_pg16.sql` con 12 tablas, JSONB GIN, `audit_logs` y `pgcrypto`).
16. **¿Cómo mitiga OWASP A01 (Broken Access Control / IDOR)?** Todo endpoint protegido exige JWT válido (`authMiddleware`) y filtra consultas Prisma con `ownerId === req.user.id`, retornando `HTTP 404` ante recursos ajenos para impedir además enumeración de UUIDs.
17. **¿Cómo previene ataques de fuerza bruta sobre el login?** Mediante `express-rate-limit` (`10 req / 15 min` en `/api/auth/login`), hashing `bcrypt` (cost 12) y bloqueo temporal en base de datos por 15 minutos tras 5 intentos fallidos (`HTTP 423 Locked`).
18. **¿Cómo previene Inyección SQL (A03) y XSS?** Prisma ORM parametriza todas las consultas, Zod valida entradas en frontera y Vue 3 escapa plantillas automáticamente sin utilizar `v-html`.
19. **¿Por qué el PDF Dual-Page y el PNG 300 DPI se generan en el navegador?** Garantiza autonomía completa en parcelas sin señal móvil 4G/5G y elimina riesgos SSRF (A10) en el servidor.
20. **¿Qué respaldan los 81 tests unitarios y el benchmark?** Cubren los 11 módulos del motor de ingeniería en `186 ms` (`81/81 PASS`), mientras que 1.000 ejecuciones completas promediaron `0,0286 ms` frente a un límite SLA de `50 ms`.
21. **¿Qué queda acotado explícitamente para la fase de construcción (Unidad 3)?** El despliegue en VPS Ubuntu detrás de Nginx TLS 1.3, migración a PostgreSQL 16 con bitácora `audit_logs`, pruebas de carga `k6` y escaneo activo con `OWASP ZAP`.
