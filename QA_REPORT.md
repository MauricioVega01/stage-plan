# REPORTE DE AUDITORÍA TÉCNICA Y QA INTEGRAL
**Proyecto:** StagePlan Monorepo  
**Rol:** Senior Staff Software Engineer & Lead QA Architect  
**Fecha:** 25 de Noviembre de 2026  
**Entorno de Auditoría:** Windows 11 / Node.js v20.x / npm v10.x  
**Modo de Ejecución:** Auditoría Estricta de Solo Lectura (Read-Only)

---

## 1. Resumen Ejecutivo

### 1.1 Diagnóstico General del Proyecto
**Estado Global:** ⚠️ **CON RIESGOS (Riesgo Alto de Despliegue)**

El proyecto **StagePlan** presenta una base de ingeniería sólida y bien estructurada en su paquete central isomórfico (`@stageplan/shared`), evidenciando **70/70 pruebas unitarias aprobadas con 100% de éxito** y una cobertura de líneas superior al 94.5%. Asimismo, la base de datos ha sido satisfactoriamente normalizada al idioma español bajo SQLite/Prisma, y los tipos TypeScript reflejan coherencia conceptual entre el modelo físico y acústico.

Sin embargo, el proyecto **no es desplegable a producción en este momento** debido a un error de compilación sintáctico bloqueante en el frontend. Adicionalmente, se identificaron fallas arquitectónicas en el manejo de excepciones del backend, inconsistencias de seguridad entre la documentación entregable y la implementación de autenticación, y una acumulación crítica de deuda técnica en el componente principal de la interfaz de usuario.

---

### 1.2 Los 3 Puntos Más Urgentes que Debes Saber Hoy

1. 🔴 **Build Blocker en Frontend (TS1128):**  
   El comando `npm run build` falla de forma irreversible en `@stageplan/frontend` debido a código duplicado y una llave de cierre huérfana en [App.vue](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/frontend/src/App.vue#L2125-L2127). Esto impide generar el artefacto de distribución para producción (`dist/`).
2. 🟠 **Ausencia de `try/catch` y Manejo Centralizado de Excepciones en Backend:**  
   Los controladores de recintos ([venue.controller.ts](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/venue.controller.ts#L7-L97)) y cálculos ([calculation.controller.ts](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/calculation.controller.ts#L18-L200)) ejecutan consultas asíncronas a la base de datos sin encapsulación defensiva. Cualquier error de red, concurrencia o violación de integridad referencial produce un `UnhandledPromiseRejection` y un error HTTP 500 no controlado.
3. 🟠 **Discrepancia de Seguridad Crítica en Autenticación (Falta de Bloqueo tras 5 Intentos):**  
   Mientras la documentación de requisitos y diseño de software especifica formalmente una política de bloqueo temporal de cuentas tras 5 intentos fallidos de autenticación, la implementación real en [auth.controller.ts](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/auth.controller.ts#L47-L66) carece de contador de intentos, marcas de tiempo de bloqueo y control de tasa (*rate limiting*). Además, existe un fallback de clave secreta JWT en texto plano si no se define la variable de entorno.

---

## 2. Mapa de Arquitectura y Flujos

```mermaid
graph TD
    subgraph Monorepo["StagePlan Monorepo (npm workspaces)"]
        subgraph Shared["@stageplan/shared (Isomórfico)"]
            SharedTypes["Domain Types & Interfaces"]
            SharedZod["Zod Validation Schemas"]
            SharedPhysics["Acoustic & Structural Engines"]
            SharedTests["70 Unit Tests (Vitest)"]
        end

        subgraph Backend["@stageplan/backend (Express + TypeScript)"]
            BRouter["Express REST Router"]
            BAuth["JWT Auth Middleware"]
            BControllers["Controllers (Venue, Calc, Auth)"]
            PrismaORM["Prisma Client ORM"]
            SQLiteDB[("SQLite Database (dev.db)")]
        end

        subgraph Frontend["@stageplan/frontend (Vue 3 + Vite)"]
            VueApp["App.vue (God Component ~3,150 L)"]
            SvgRender["LayoutSvg2D & Canvas 3D"]
            PdfService["PDF Engine (jsPDF + html2canvas)"]
            Tailwind["TailwindCSS UI Layer"]
        end
    end

    VueApp -->|Usa validaciones y cálculos| SharedPhysics
    BControllers -->|Valida con schemas compartidos| SharedZod
    VueApp -->|Peticiones HTTP REST| BRouter
    BRouter --> BAuth
    BAuth --> BControllers
    BControllers --> PrismaORM
    PrismaORM --> SQLiteDB
    VueApp --> SvgRender
    VueApp --> PdfService
```

### 2.1 Descripción de Capas
- **`@stageplan/shared`:** Librería central de dominio. Contiene constantes físicas y acústicas (ISO 9613-1, ANSI S1.26, SPL inverso del cuadrado), esquemas de validación Zod y tipos TypeScript compartidos. Es la capa de mayor calidad y cobertura del monorepo.
- **`@stageplan/backend`:** API REST basada en Express 4.19 y TypeScript 5.4. Utiliza Prisma 5.14 como ORM interactuando con SQLite local (`dev.db`). Implementa autenticación basada en tokens JWT con firmas `HS256` y roles de usuario (`ADMIN`, `ENGINEER`).
- **`@stageplan/frontend`:** Aplicación Single Page Application (SPA) basada en Vue 3.4 con Composition API, Vite 5.2 y TailwindCSS. Integra previsualización técnica 2D en SVG interactivo y exportación a PDF de memorias de cálculo.

### 2.2 Puntos Más Frágiles de los Flujos Críticos
1. **Flujo de Autenticación:** El endpoint `/api/auth/login` es vulnerable a ataques de fuerza bruta por diccionario al carecer de limitador de tasa (*rate limit*) y del contador de bloqueo estipulado en la documentación.
2. **Flujo de Modelado y Cálculo:** La interfaz ejecuta los cálculos físicos en el cliente en tiempo real (`onMounted` / `watchers`). Al estar alojado el 90% del estado en un único componente de más de 3,100 líneas ([App.vue](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/frontend/src/App.vue)), cualquier excepción en una propiedad computada bloquea la totalidad del wizard interactivo.
3. **Flujo de Persistencia de Proyectos:** Las llamadas a `POST /api/venues` y `POST /api/calculations` envían payloads extensos. Si el backend rechaza una petición o Prisma falla por bloqueo de base de datos SQLite (frecuente en operaciones de escritura concurrentes), la interfaz no ofrece mecanismo de reintento automático ni cola de sincronización offline.

---

## 3. Resultados de Ejecución (Build / Lint / Tests)

### 3.1 Proceso de Construcción (`npm run build`)
| Paquete | Comando Ejecutado | Resultado | Detalle / Causa Raíz |
| :--- | :--- | :---: | :--- |
| `@stageplan/shared` | `tsc -p tsconfig.json` | **EXITOSO** | Compilación limpia de tipos e interfaces de dominio. |
| `@stageplan/backend` | `tsc -p tsconfig.json` | **EXITOSO** | Transpilación completa a CommonJS en `dist/`. |
| `@stageplan/frontend` | `vue-tsc --noEmit && vite build` | ❌ **FALLIDO** | **Exit code 2.** Error `TS1128: Declaration or statement expected` en `src/App.vue:2127:1`. |

### 3.2 Suites de Pruebas Unitarias (`npm test`)
- **Herramienta:** Vitest v1.6.0.
- **Ámbito:** `@stageplan/shared`.
- **Resultados:**
  - **Suites evaluadas:** 10/10 archivos pasados (100%).
  - **Tests ejecutados:** 70/70 pasados (100%).
  - **Tiempo de ejecución:** 169 ms.
  - **Módulos verificados:** Atenuación sonora, SPL combinado, cobertura acústica, rigidez/cargas estructurales, balance de pesos, validaciones Zod de recintos y escenarios.

### 3.3 Cobertura de Código (`npm run test:coverage`)
- **Líneas:** 94.53%
- **Sentencias (Statements):** 94.53%
- **Funciones:** 97.29%
- **Ramas (Branches):** 78.93%
- **Incidencia:** El script de cobertura falló con código 1 porque el archivo [vitest.config.ts](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/shared/vitest.config.ts#L32) exige un umbral estricto del 90.00% en *Branches*, situándose la ejecución real 11.07% por debajo del umbral mínimo configurado.

### 3.4 Análisis Estático de Código (`npm run lint`)
- **Estado:** ⚠️ **No Operativo / Simulado.**
- **Diagnóstico:** El script raíz contiene `"lint": "echo \"Linting workspaces...\""`. No existe configuración activa de ESLint ni Prettier en el pipeline, lo que permitió que errores de sintaxis flagrantes como el de `App.vue` pasaran desapercibidos antes del build.

### 3.5 Auditoría de Vulnerabilidades (`npm audit`)
- **Total de Vulnerabilidades:** 19 (4 Críticas, 7 Altas, 8 Moderadas).
- **Hallazgos Principales:**
  - `tinypool <=2.1.1` (Crítica): Prototype Pollution y ejecución de código arbitrario vía worker thread options.
  - `tar <=7.5.20` (Alta): Arbitrary file creation/overwrite vía symlinks maliciosos.
  - `dompurify` (Alta): Potencial Cross-Site Scripting (XSS) en parseo de HTML.

---

## 4. Matriz de Hallazgos (QA)

### 4.1 Severidad Crítica (Bloqueante)

#### [BUILD-01] Error de Sintaxis por Código Duplicado y Llave Huérfana
- **Ubicación:** [packages/frontend/src/App.vue:2125-2127](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/frontend/src/App.vue#L2125-L2127)
- **Qué está pasando:** La función de navegación entre pasos del wizard contiene un bloque duplicado con una llave de cierre adicional fuera de ámbito:
  ```typescript
  2123:   currentStep.value = stepId;
  2124:   window.scrollTo({ top: 0, behavior: 'smooth' });
  2125: }
  2126:   window.scrollTo({ top: 0, behavior: 'smooth' });
  2127: }
  ```
- **Impacto / Riesgo:** Invalida el árbol sintáctico del script Vue. El analizador de tipos `vue-tsc` interrumpe el proceso de build, impidiendo cualquier despliegue o release de la aplicación web.
- **Solución Propuesta:** Eliminar las líneas 2126 y 2127 para cerrar limpiamente la función `goToStep`.

---

### 4.2 Severidad Alta

#### [BACK-01] Ausencia de Bloques `try/catch` y Manejo Global de Errores en Controladores
- **Ubicación:**  
  - [packages/backend/src/controllers/venue.controller.ts:7-97](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/venue.controller.ts#L7-L97)  
  - [packages/backend/src/controllers/calculation.controller.ts:18-200](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/calculation.controller.ts#L18-L200)
- **Qué está pasando:** Los métodos asíncronos invocan operaciones de base de datos (`prisma.recinto.create`, `prisma.calculo.findMany`, etc.) sin encapsulación en `try/catch`. Tampoco se cuenta con un wrapper de tipo `express-async-errors` o middleware capturador de errores al final de la cadena de Express.
- **Impacto / Riesgo:** Un fallo transitorio de la base de datos SQLite (ej. `SQLITE_BUSY` por bloqueo de archivo) o una violación de restricción única no controlada deja la conexión HTTP colgada o responde un error 500 crudo exponiendo el stack trace de Prisma al cliente.
- **Solución Propuesta:** Implementar un middleware centralizado de captura de errores `errorHandler(err, req, res, next)` en Express y envolver los controladores con un helper asíncrono `asyncHandler` que canalice los fallos a través de `next(error)`.

#### [SEC-01] Falta de Implementación del Bloqueo de Cuenta tras 5 Intentos Fallidos
- **Ubicación:** [packages/backend/src/controllers/auth.controller.ts:47-66](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/auth.controller.ts#L47-L66)
- **Qué está pasando:** La función `login` valida la contraseña con `bcrypt.compare`. Si no coincide, retorna inmediatamente un error 401 (`"Credenciales inválidas"`), sin persistir intentos fallidos, sin registrar marcas de tiempo ni bloquear al usuario.
- **Impacto / Riesgo:** Discrepancia grave con el documento de arquitectura y requisitos de seguridad entregables. Deja al sistema vulnerable a ataques de fuerza bruta continuos contra credenciales administrativas.
- **Solución Propuesta:** Extender la tabla `usuario` en Prisma con los campos `intentos_fallidos` (Int) y `bloqueado_hasta` (DateTime nullable). En el controlador de login, incrementar el contador ante credenciales erróneas y bloquear la cuenta durante 15 minutos al alcanzar el quinto intento consecutivo.

#### [SEC-02] Fallback Inseguro de Clave Secreta JWT en Texto Plano
- **Ubicación:**  
  - [packages/backend/src/middlewares/auth.ts:26](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/middlewares/auth.ts#L26)  
  - [packages/backend/src/controllers/auth.controller.ts:73](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/src/controllers/auth.controller.ts#L73)
- **Qué está pasando:** Se utiliza la expresión `process.env.JWT_SECRET || 'dev_only_stageplan_secret_key'`.
- **Impacto / Riesgo:** Si el contenedor o servidor arranca sin la variable de entorno explícita en producción, se emitirán tokens firmados con una clave pública conocida, permitiendo a cualquier atacante forjar tokens con rol `ADMIN`.
- **Solución Propuesta:** Forzar validación en el arranque del servidor (`server.ts`). Si `process.env.JWT_SECRET` no está definido en entornos de producción (`NODE_ENV === 'production'`), arrojar una excepción fatal e impedir el inicio del proceso.

---

### 4.3 Severidad Media

#### [ARCH-01] Componente Monolítico de Interfaz ("God Component")
- **Ubicación:** [packages/frontend/src/App.vue:1-3150](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/frontend/src/App.vue)
- **Qué está pasando:** `App.vue` concentra en un solo archivo más de 3,150 líneas de código: gestión completa del estado global, controladores de formularios de los 5 pasos del wizard, llamadas REST a la API, fórmulas de simulación acústica en tiempo real, renderizado SVG directo y manipulación de localStorage.
- **Impacto / Riesgo:** Dificulta el mantenimiento, la depuración y la realización de pruebas unitarias de frontend. Provoca re-renderizados innecesarios del lienzo SVG técnico al actualizar campos menores de texto en el formulario.
- **Solución Propuesta:** Descomponer `App.vue` en componentes especializados utilizando Composition API: `StepVenue.vue`, `StepStage.vue`, `StepAcoustic.vue`, `StepStructural.vue`, `StepSummary.vue`, y extraer el estado a un composable dedicado (`useStagePlannerState.ts`).

#### [QA-01] Cobertura de Ramas por Debajo del Umbral de Calidad
- **Ubicación:** [packages/shared/vitest.config.ts:32](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/shared/vitest.config.ts#L32)
- **Qué está pasando:** El umbral configurado es del 90.00% en `branches`, pero la cobertura alcanzada en la suite es de 78.93%.
- **Impacto / Riesgo:** Las ramas no cubiertas corresponden a condiciones de borde en cálculos acústicos extremos (ej. factores de directividad atípicos o casos donde las distancias son cero o negativas).
- **Solución Propuesta:** Agregar casos de prueba en `packages/shared/src/tests/` para escenarios límite (distancias mínimas, valores fuera de rango y manejo de excepciones en schemas Zod).

#### [TOOL-01] Carencia de Linter Activo en el Monorepo
- **Ubicación:** [package.json:16](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/package.json#L16)
- **Qué está pasando:** El comando `"lint"` es un comando `echo` simulado.
- **Impacto / Riesgo:** No hay verificación de convenciones de código, imports no utilizados ni detección temprana de errores de sintaxis o variables no inicializadas antes de intentar compilar.
- **Solución Propuesta:** Configurar ESLint 9 / TypeScript-ESLint en la raíz del monorepo y vincularlo al hook de pre-commit (`husky` o similar).

---

### 4.4 Severidad Baja

#### [CFG-01] Desincronización entre Plantilla de Entorno y Configuración Real
- **Ubicación:** [packages/backend/.env.example:5](file:///c:/Users/WIT2026/Documents/stage-plan-main/stage-plan-main/packages/backend/.env.example#L5)
- **Qué está pasando:** `.env.example` contiene `DATABASE_URL="postgresql://postgres:postgres@localhost:5432/stageplanner_db"` mientras que el archivo `.env` de desarrollo y el schema de Prisma están configurados para SQLite (`file:./dev.db`).
- **Impacto / Riesgo:** Confusión para nuevos desarrolladores al clonar el repositorio e intentar ejecutar migraciones de Prisma.
- **Solución Propuesta:** Actualizar `.env.example` para reflejar el driver SQLite por defecto o documentar claramente la alternancia entre entornos SQLite y PostgreSQL.

---

## 5. Plan de Acción Priorizado

### Fase 1: Bloqueantes y Quick Wins (Inmediato - Día 1)
1. **Corregir Syntax Error en Frontend:** Eliminar líneas 2126-2127 en `App.vue` y verificar que `npm run build` termine con éxito (0 errores).
2. **Endurecer Secrets en Backend:** Requerir `JWT_SECRET` en `server.ts` y fallar el arranque si no existe en producción.
3. **Sincronizar `.env.example`:** Actualizar la cadena de conexión de base de datos a SQLite para coincidir con la arquitectura actual.

### Fase 2: Estabilidad y Resiliencia Backend (Semana 1)
1. **Implementar `asyncHandler` y Middleware de Errores:** Envolver todos los endpoints de `venue.controller.ts` y `calculation.controller.ts` para capturar excepciones de Prisma de manera elegante.
2. **Implementar Política de Seguridad de Bloqueo de Cuentas:** Añadir campos `intentos_fallidos` y `bloqueado_hasta` en el schema de Prisma y aplicar la lógica en `auth.controller.ts`.
3. **Añadir Rate Limiting:** Configurar `express-rate-limit` en la ruta `/api/auth/login` (máximo 5 peticiones por minuto por IP).

### Fase 3: Seguridad de Dependencias y QA Riguroso (Semana 2)
1. **Resolver Vulnerabilidades de Paquetes:** Ejecutar auditoría y actualización controlada de paquetes (`npm audit fix` para `dompurify` y actualización de dependencias de desarrollo).
2. **Alcanzar Umbral de Cobertura de Ramas (90%):** Escribir tests unitarios adicionales en `@stageplan/shared` para cubrir casos de borde en cálculos físicos.
3. **Instalar y Configurar ESLint:** Reemplazar el script `lint` simulado por una configuración real de ESLint + TypeScript.

### Fase 4: Refactorización y Deuda Técnica (Semana 3)
1. **Modularizar `App.vue`:** Descomponer el componente en submódulos por paso del wizard (`components/wizard/Step*.vue`).
2. **Centralizar Estado Reactivo:** Extraer la lógica de cálculo y reactividad a un composable desacoplado.

---
*Reporte emitido conforme a las mejores prácticas de ingeniería de software y control de calidad (ISO/IEC 25010).*
