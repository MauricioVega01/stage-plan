import os
import re

informe_path = r"C:\Users\WIT2026\Documents\stage-plan-main\stage-plan-main\INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md"

with open(informe_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Resumen Ejecutivo
content = content.replace(
    "persistencia híbrida **PostgreSQL 16** (12 tablas normalizadas 3FN + documentos `JSONB` indexados con GIN)",
    "persistencia híbrida **SQLite 3 (`dev.db`) con Prisma ORM** (4 tablas normalizadas 3FN + documentos `JSON` nativos, consultable en DB Browser for SQLite) con proyección a PostgreSQL 16"
)

content = content.replace(
    "(*Mobile-First* y *Offline-First*)",
    "(*Mobile-First* y cálculo autónomo en cliente)"
)

# 2. Vista Física 2.6
content = content.replace(
    "Separa estrictamente la capa de ejecución local en terreno (navegador móvil con motor isomórfico y generación PDF offline) de la infraestructura cloud protegida por proxy inverso TLS 1.3 en puerto `:443`, aislando la API Express (`:3000`) y PostgreSQL 16 (`:5432`) en red interna.",
    "El MVP opera en la estación local mediante la SPA Vue 3 conectada a la API Express (`:3000`) y la base de datos embebida SQLite 3 (`dev.db`). Para la etapa productiva (Unidad 3), se proyecta el empaquetado en contenedores Docker detrás de un proxy inverso TLS 1.3 en puerto `:443`, aislando los servicios internos y facilitando la migración transparente de SQLite a PostgreSQL 16 mediante Prisma."
)

# 3. Sección 4 completa (Modelo y Administración de Base de Datos)
sec4_pattern = re.compile(r"### 4\. Modelo y Administración de Base de Datos.*?### 5\. Estándares de Programación Segura", re.DOTALL)

sec4_new = """### 4. Modelo y Administración de Base de Datos (Criterios 2.1.4.8 y 2.1.4.9)

#### 4.1 Selección y Justificación del Modelo Híbrido (Relacional 3FN + Documental JSON)
Para el MVP operacional de STAGE PLAN se seleccionó **SQLite 3 (`dev.db`) administrado a través de Prisma ORM**, implementando una arquitectura **Híbrida (Estructurada + No Estructurada)**:
* **Núcleo Estructurado (3FN):** Garantiza integridad referencial estricta (`ACID`), llaves primarias UUID/TEXT, llaves foráneas con reglas de integridad `ON DELETE CASCADE` entre usuarios, recintos, cálculos y enlaces compartidos.
* **Capa No Estructurada (`JSON` Nativo):** Resuelve la variabilidad y polimorfismo de los montajes de audio e iluminación almacenando snapshots inmutables de resultados (`rider_input`, `calculated_results`, `alerts_snapshot`) sin sobrecargar la base de datos con decenas de tablas pivote innecesarias para un MVP.
* **Ventajas Operacionales y de Auditoría Directa:** Al ser una base de datos autocontenida en un único archivo físico (`dev.db`), el desarrollador y el operador pueden inspeccionar, auditar o respaldar los datos de manera inmediata arrastrando el archivo a herramientas estándar como **DB Browser for SQLite**, garantizando portabilidad absoluta en terreno y cero fallas de conexión por servicios de red caídos.
* **Proyección a Producción (Unidad 3):** Gracias a la capa de abstracción de **Prisma ORM**, la migración desde SQLite hacia un clúster PostgreSQL 16 con índices GIN en la nube se realiza de forma transparente cambiando únicamente la directiva `datasource` en `schema.prisma`, manteniendo intacto el 100% del código de controladores y validaciones.

![Figura 12. Diagrama Entidad-Relación (DER) del Modelo Híbrido MVP (4 Tablas 3FN + Documentos JSON)](entrega_sumativa_02/diagrams/diag-07-modelo-datos-der.png)

#### 4.2 Diccionario de Entidades, Integridad Referencial y Documentos JSON del MVP

*Tabla 6. Diccionario de las 4 tablas normalizadas implementadas en Prisma y SQLite (`dev.db`).*

| # | Tabla | Clave Primaria (PK) | Claves Foráneas (FK) y Reglas | Atributos Estructurados | Campos No Estructurados (JSON) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | `users` | `id (TEXT/UUID)` | — | `email UNIQUE`, `passwordHash` (Bcrypt 12), `name`, `createdAt`, `updatedAt` | — |
| 2 | `venues` | `id (TEXT/UUID)` | `owner_id → users(id) ON DELETE CASCADE` | `name`, `width_meters`, `depth_meters`, `height_meters`, `environment_type`, `electrical_distance_meters` | — |
| 3 | `rider_calculations` | `id (TEXT/UUID)` | `owner_id → users(id) CASCADE`, `venue_id → venues(id) CASCADE` | `engine_version` (ej. "3.1.0"), `createdAt` | `rider_input` (lotes de audio/luces), `params_used`, `calculated_results` (resumen SEC/Haas), `alerts_snapshot` |
| 4 | `shared_links` | `id (TEXT/UUID)` | `owner_id → users(id) CASCADE`, `rider_calculation_id → rider_calculations(id) CASCADE` | `token UNIQUE`, `expires_at`, `is_revoked (INTEGER)`, `createdAt` | — |

*Ejemplo de Documento No Estructurado almacenado en la columna `calculated_results` (JSON):*
```json
{
  "totalWatts": 3250,
  "designAmps": 17.73,
  "electricalSummary": {
    "recommendedSectionMm2": 2.5,
    "voltageDropPct": 2.18,
    "secCompliant": true,
    "rule": "Pliego SEC RIC N° 03 (ΔV <= 3%)"
  },
  "guidePostsRic10": {
    "count": 4,
    "minBendRadiusMm": 72,
    "rule": "R >= 6 * diámetro conductor (RIC N° 10)"
  },
  "acousticSummary": {
    "monoClusterCentral": true,
    "clusterGainDb": 6.0,
    "delayTowerHaasMs": 44.3,
    "sweetSpotDba": "96-102 dBA"
  },
  "lightingDmx": {
    "totalFixtures": 4,
    "totalWatts": 480,
    "dmxCablesRequired": 4,
    "terminators120Ohm": 1
  }
}
```

#### 4.3 Estrategias de Integración y Consultas Híbridas SQL + JSON
La combinación entre datos relacionales transaccionales y atributos semiestructurados se consulta de manera directa y transparente. En SQLite se utilizan las funciones estándar de extracción JSON (`json_extract`):

```sql
-- Consulta híbrida auditable directamente en DB Browser for SQLite:
SELECT u.name AS operador, 
       v.name AS recinto, 
       rc.engine_version,
       json_extract(rc.calculated_results, '$.totalWatts') AS total_watts,
       json_extract(rc.calculated_results, '$.electricalSummary.recommendedSectionMm2') AS seccion_cable_mm2,
       json_extract(rc.calculated_results, '$.electricalSummary.voltageDropPct') AS caida_tension_pct,
       json_extract(rc.calculated_results, '$.acousticSummary.sweetSpotDba') AS sweet_spot_dba
FROM users u
JOIN venues v ON u.id = v.owner_id
JOIN rider_calculations rc ON v.id = rc.venue_id
WHERE json_extract(rc.calculated_results, '$.electricalSummary.secCompliant') = 1;
```
Esta consulta demuestra el cumplimiento pleno de los criterios **2.1.4.8** (integridad referencial relacional) y **2.1.4.9** (gestión eficaz de datos estructurados y semiestructurados en una sola fuente de datos accesible y portable).

---

### 5. Estándares de Programación Segura"""

content = sec4_pattern.sub(sec4_new, content)

# 4. Anexo A (Trazabilidad Rúbrica)
content = content.replace(
    "Sección 4.1–4.2 Tabla 6, Figura 12 (DER `diag-07`) y script ejecutable `sql/schema_stageplan_pg16.sql` (12 tablas 3FN + Triggers).",
    "Sección 4.1–4.2 Tabla 6 y Figura 12 (DER `diag-07`): 4 tablas maestras 3FN en SQLite (`dev.db`) con Prisma ORM (PK, FK, CASCADE, auditable en DB Browser)."
)

content = content.replace(
    "Sección 4.1–4.3: PostgreSQL 16 relacional + columnas `JSONB` (índices GIN), ejemplo JSON y consulta híbrida SQL+JSONB.",
    "Sección 4.1–4.3: SQLite 3 relacional + columnas `JSON` nativas (`json_extract`), ejemplo JSON funcional y consulta híbrida probada en DB Browser."
)

# 5. Anexo C (Preguntas de Defensa Oral)
content = content.replace(
    "Las entidades transaccionales y de seguridad (`users`, `venues`, `electrical_circuits`, `audit_logs`) exigen integridad referencial ACID en 3FN, mientras que las fichas técnicas polimórficas de equipos y snapshots de cálculo se modelan óptimamente en columnas `JSONB` con índices `GIN`.",
    "Para el MVP, las entidades transaccionales (`users`, `venues`, `rider_calculations`, `shared_links`) operan en SQLite 3 con integridad referencial 3FN, mientras que los snapshots de cálculo e inventario se almacenan en columnas JSON nativas. Esto permite que el archivo `dev.db` sea 100% portable y auditable en DB Browser for SQLite, dejando la migración a PostgreSQL 16 lista en Prisma para la Unidad 3."
)

with open(informe_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Informe Markdown actualizado exitosamente.")
