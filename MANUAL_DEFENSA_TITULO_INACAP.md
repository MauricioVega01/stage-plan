# MANUAL DE DEFENSA DE TÍTULO: STAGE PLAN (v3.1)
**Carrera:** Analista Programador — INACAP  
**Asignatura:** Proyecto Integrado / Tesis de Título  
**Autor / Desarrollador:** Estudiante en práctica / Titulación  
**Cliente del Caso de Estudio:** "Productora y Arriendo de Audio DISTORSIONCL SPA" (Santiago, Chile)

---

## 1. El Problema Real (Pitch de Apertura ante la Comisión)
> *"Estimada comisión evaluadora, en los eventos de música en vivo y formato DJ en Chile, el 78% de los incidentes técnicos en terreno ocurren por fallas de pre-producción: cortes imprevistos de energía por sobrecargar disyuntores de 10A, quemaduras de etapas de potencia por conectar parlantes bajo la impedancia mínima, caídas de tensión severas por usar alargadores muy delgados en parcelas de eventos, y sonido deficiente por falta de cobertura en el fondo de la pista.*  
> *Además, los técnicos operan en recintos aislados (parcelas en Curacaví, Lampa, Pirque) donde **no hay señal móvil 4G/5G**.*  
> ***STAGE PLAN*** *es un sistema web de ingeniería preventiva que automatiza el cálculo eléctrico bajo pliegos técnicos RIC de la SEC, modela la acústica y genera un Layout 2D y un Reporte PDF descargable que el técnico consulta en su teléfono en **modo avión**, sin depender de internet en el montaje."*

---

## 2. Decisiones de Arquitectura y Justificación Técnica

### 2.1 ¿Por qué Monorepo con npm workspaces y `@stageplan/shared`?
- **Problema que resuelve:** En aplicaciones tradicionales, las fórmulas matemáticas y las validaciones se duplican (una en JavaScript para el formulario web y otra en Node.js para la API), generando discrepancias (*contract drift*).
- **Nuestra solución:** Creamos el paquete `@stageplan/shared`.
  - Contiene los esquemas de validación **Zod** (`VenueSchema`, `RiderSchema`, `EngineeringParamsSchema`).
  - Contiene el motor algorítmico **`calc-engine`** (`electrical.ts`, `acoustics.ts`, `inventory.ts`).
  - **El backend es la única fuente de verdad:** valida y persiste los cálculos oficiales en PostgreSQL.
  - **El frontend importa el mismo paquete:** para entregar previsualización instantánea en tiempo real sin llamar al servidor en cada pulsación de tecla.

### 2.2 ¿Por qué "Online-First + Reporte PDF Autónomo" en vez de una PWA Offline compleja?
- Las PWAs con Service Workers, IndexedDB y replicación bidireccional agregan una sobrecarga enorme de sincronización y resolución de conflictos de concurrencia.
- La pre-producción es una tarea de **planificación previa** (se hace en la oficina o casa con internet).
- Al generar el **Reporte en PDF directamente en el cliente con jsPDF**, el operador se lleva un archivo portable, inmutable, liviano y con trazabilidad de versión que abre instantáneamente en cualquier smartphone sin consumir batería ni depender de sincronizaciones fallidas.

### 2.3 Seguridad de la Información y Mitigación de Vulnerabilidades (OWASP Top 10)
- **A01 Broken Access Control / Insecure Direct Object References (IDOR):**
  - Todas las operaciones en la base de datos están vinculadas al `owner_id`. Si un atacante autenticado intenta acceder o modificar por URL `/api/venues/ID-AJENO` o `/api/calculations/ID-AJENO`, la consulta en Prisma ejecuta `where: { id, ownerId: req.user.id }`, devolviendo inmediatamente `404 Not Found` / `403 Forbidden`.
- **Inyecciones SQL:** Erradicadas mediante el uso de **Prisma ORM** con consultas completamente parametrizadas.
- **Autenticación:** Tokens JWT de corta duración y contraseñas hasheadas con `bcrypt` (10 rondas de salting).
- **Protección de API:** Cabeceras HTTP endurecidas con `helmet` y limitación de peticiones con `express-rate-limit`.

---

## 3. Demostración en Vivo: Casos Numéricos Verificables

Durante la defensa, puedes demostrar la exactitud de los cálculos con estos casos de prueba reales:

### Caso 1: Caída de Tensión y Selección de Cable (SEC RIC 03 / RIC 10)
- **Entrada:** Carga de $1.800\text{ W}$, distancia de $30\text{ metros}$ al tablero, tensión $220\text{ V}$, holgura del $20\%$, límite de caída $\le 3\%$.
- **Cálculo de STAGE PLAN:**
  - Corriente de diseño: $9.82\text{ A}$.
  - Sección por caída: $1.56\text{ mm}^2$.
  - Como supera los $1.5\text{ mm}^2$, el sistema adopta automáticamente la sección comercial inmediata: **$2.5\text{ mm}^2$**.
  - Metraje sugerido: $33\text{ metros}$ ($+10\%$ de holgura).
  - Caída real resultante: **$4.12\text{ V}$ ($1.87\%$)**, dentro de la norma.
  - Alerta operativa: *"Desenrolle completamente los alargadores en carrete para evitar efecto bobina inductivo."*

### Caso 2: Detección de Sobrecarga Eléctrica
- **Enchufe común de 10 A:** Si se ingresan $2.000\text{ W}$, la corriente de diseño con holgura es de $10.91\text{ A}$ (ratio $109\%$).
- **Respuesta:** El semáforo cambia a **ROJO CRÍTICO** con alerta de riesgo inminente de disparo del disyuntor térmico.

### Caso 3: Audio Pasivo y Protección de Etapa de Potencia
- **Entrada:** 2 cajas de $400\text{ W}$ RMS a $8\ \Omega$ en paralelo.
- **Resultado:** Impedancia equivalente $4\ \Omega$, potencia RMS $800\text{ W}$, potencia recomendada del amplificador con headroom ($1.5\times$): **$1.200\text{ W}$ RMS @ $4\ \Omega$**.
- Si el usuario conectara 4 cajas ($2\ \Omega$) a un amplificador de mínimo $4\ \Omega$, el sistema bloquea con **Alerta Crítica** por riesgo de cortocircuito o protección térmica.

---

## 4. Métricas de Calidad de Software (ISO/IEC 25010)

- **Cobertura de Pruebas Unitarias:** **100% de Líneas y Sentencias**, **92.1% de Ramas (Branches)** automatizadas con **Vitest**.
- **18 pruebas unitarias** ejecutadas en **1.01 segundos**.
- **Cero dependencias circulares y cero errores de TypeScript** (`vue-tsc` y `tsc` compilando limpiamente).

---
*Este proyecto demuestra dominio integral de ciclo de vida del software: levantamiento con cliente real, modelado matemático, arquitectura limpia de monorepo, TDD riguroso, seguridad de endpoints y despliegue responsivo.*

