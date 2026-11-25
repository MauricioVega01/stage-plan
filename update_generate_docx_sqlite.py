import os
import re

script_path = r"C:\Users\WIT2026\Documents\stage-plan-main\stage-plan-main\generate_sumativa_02_docx.py"

with open(script_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Ajustar rutas relativas BASE_DIR y TEMPLATE_PATH
code = code.replace(
    'TEMPLATE_PATH = r"C:\\Users\\casa\\Downloads\\Formato_propuesto_sumativa 02_2026.docx"',
    'BASE_DIR = os.path.dirname(os.path.abspath(__file__))\n'
    'TEMPLATE_PATH = os.path.join(BASE_DIR, "Formato_propuesto_sumativa 01_2026.docx")\n'
    'if not os.path.exists(TEMPLATE_PATH):\n'
    '    TEMPLATE_PATH = os.path.join(BASE_DIR, "Proyecto Integrado 1.docx")'
)
code = code.replace(
    'BASE_DIR = r"D:\\Dev\\INACAP\\stage-plan-main\\stage-plan-main"',
    '# BASE_DIR dinamico ya definido arriba'
)

# 2. Resumen ejecutivo
code = code.replace(
    '(4) base de datos híbrida PostgreSQL 16 (12 tablas 3FN + columnas JSONB con índices GIN);',
    '(4) base de datos híbrida SQLite 3 dev.db con Prisma ORM (4 tablas normalizadas 3FN + documentos JSON nativos, auditable en DB Browser for SQLite);'
)

code = code.replace(
    'Estación Windows 11, Node.js v24 LTS, PostgreSQL 16, Vitest v3.2.7, GitHub',
    'Estación Windows 11, Node.js v24 LTS, SQLite 3 (dev.db) + Prisma, Vitest v3.2.7, GitHub'
)

code = code.replace(
    '["T09", "S3", "Prisma ORM (schema.prisma) + DDL PostgreSQL 16 (12 tablas)", "M. Vega", "29–31 Oct", "T03, T08", "Must", "SÍ"],',
    '["T09", "S3", "Prisma ORM (schema.prisma) + SQLite 3 (dev.db) 4 tablas 3FN + JSON", "M. Vega", "29–31 Oct", "T03, T08", "Must", "SÍ"],'
)

code = code.replace(
    '["Sprint 3", "29-Oct – 11-Nov", "Implementar persistencia PostgreSQL/Prisma, API segura y Wizard Vue 3.", "API Anti-IDOR + Wizard 5 pasos WCAG AA."],',
    '["Sprint 3", "29-Oct – 11-Nov", "Implementar persistencia SQLite/Prisma (dev.db), API segura y Wizard Vue 3.", "API Anti-IDOR + Wizard 5 pasos WCAG AA."],'
)

code = code.replace(
    '["Persistencia", "PostgreSQL 16 + Prisma ORM 6.4 (3FN + JSONB)", "Integridad ACID para seguridad/usuarios + JSONB GIN para riders variables.", "Réplica de solo lectura para analítica histórica."],',
    '["Persistencia", "SQLite 3 (dev.db) + Prisma ORM 6.4 (3FN + JSON)", "Integridad ACID para usuarios/recintos + JSON nativo para riders; auditable en DB Browser.", "Migración transparente a PostgreSQL 16 en VPS vía Prisma (Unidad 3)."],'
)

# 3. Reemplazar Tabla 10 (las 12 tablas por las 4 tablas maestras de Prisma)
old_table10 = '''    c43.add_figure(os.path.join(DIAG_DIR, "diag-07-modelo-datos-der.png"), "Figura 12. Diagrama Entidad-Relación (DER) del modelo híbrido PostgreSQL 16 (12 tablas 3FN + JSONB GIN).")
    c43.add_table(
        "Tabla 10. Resumen de entidades, claves primarias/foráneas y restricciones del script sql/schema_stageplan_pg16.sql.",
        ["#", "Tabla", "PK / FKs y Reglas Referenciales", "Restricciones CHECK y Campos JSONB"],
        [
            ["1", "roles", "PK id (smallint)", "UNIQUE nombre IN ('operador_foh','administrador','invitado_chofer')"],
            ["2", "users", "PK id (uuid) | FK rol_id → roles RESTRICT", "email UNIQUE, Bcrypt(12), intentos_fallidos >= 0, token_version"],
            ["3", "venues", "PK id (uuid) | FK owner_id → users CASCADE", "CHECK width/depth 1..500, neighbor_distance >= 5, D.S. 38"],
            ["4", "equipment_catalog", "PK id (uuid)", "UNIQUE(brand, model), specs_json JSONB + índice GIN"],
            ["5", "rider_calculations", "PK id | FK owner_id, venue_id CASCADE", "rider_input, params_used, calculated_results (JSONB GIN)"],
            ["6", "equipment_lots", "PK id | FK calculation_id CASCADE, catalog_id", "ACTIVE/PASSIVE, impedance_ohms >= 2.0, Trigger PROTECT"],
            ["7", "lighting_fixtures", "PK id | FK calculation_id CASCADE", "PAR_LED_X1, watts_per_unit > 0, dmx_cable_meters >= 1.0"],
            ["8", "electrical_circuits", "PK id | FK calculation_id CASCADE", "voltage_drop_pct <= 3.00, min_bend_radius_mm >= 48, Trigger SEC"],
            ["9", "audio_routes", "PK id | FK calculation_id CASCADE", "XLR_BALANCED, TRS_TO_XLR_BOOTH, SPEAKON_NL4, haas_delay_ms >= 0"],
            ["10", "shared_links", "PK id | FK owner_id, rider_calculation_id", "token UNIQUE, expires_at, is_revoked"],
            ["11", "audit_logs", "PK id (bigint) | FK user_id SET NULL", "event_type (IDOR_BLOCKED_403, LOGIN_FAIL), detail_json JSONB"],
            ["12", "user_feedback", "PK id (uuid) | FK user_id SET NULL", "Registro trazable de iteraciones UX con DISTORSIONCL SPA"]
        ],
        [0.3, 1.35, 2.35, 2.5]
    )'''

new_table10 = '''    c43.add_figure(os.path.join(DIAG_DIR, "diag-07-modelo-datos-der.png"), "Figura 12. Diagrama Entidad-Relación (DER) del modelo híbrido MVP (4 tablas 3FN + Documentos JSON).")
    c43.add_table(
        "Tabla 10. Diccionario de entidades, claves primarias/foráneas y reglas referenciales implementadas en Prisma y SQLite (dev.db).",
        ["#", "Tabla", "PK / FKs y Reglas Referenciales", "Atributos Estructurados y Campos JSON"],
        [
            ["1", "users", "PK id (TEXT/UUID)", "email UNIQUE, passwordHash (Bcrypt 12), name, createdAt, updatedAt"],
            ["2", "venues", "PK id (TEXT/UUID) | FK owner_id → users CASCADE", "name, width_meters, depth_meters, height_meters, environment_type, electrical_distance_meters"],
            ["3", "rider_calculations", "PK id | FK owner_id, venue_id CASCADE", "engine_version, rider_input (JSON), params_used (JSON), calculated_results (JSON), alerts_snapshot (JSON)"],
            ["4", "shared_links", "PK id | FK owner_id, rider_calculation_id CASCADE", "token UNIQUE, expires_at, is_revoked (INTEGER/BOOLEAN), createdAt"]
        ],
        [0.3, 1.35, 2.35, 2.5]
    )'''

code = code.replace(old_table10, new_table10)

# 4. Reemplazar consulta SQL en sección 4.3
old_sql = '''        "SELECT u.name AS operador, v.name AS recinto, ec.line_code, ec.cable_section_mm2, ec.voltage_drop_pct,\\n"
        "       (rc.calculated_results->'acousticSummary'->>'sweetSpotDba') AS sweet_spot_dba,\\n"
        "       (rc.calculated_results->'guidePostsRic10'->>'count')::int AS postes_guia_ric10\\n"
        "FROM users u\\n"
        "JOIN venues v ON u.id = v.owner_id\\n"
        "JOIN rider_calculations rc ON v.id = rc.venue_id\\n"
        "JOIN electrical_circuits ec ON rc.id = ec.calculation_id\\n"
        "WHERE ec.sec_compliant = true\\n"
        "  AND rc.calculated_results @> '{\\"electricalSummary\\": {\\"secCompliant\\": true}}'::jsonb;"'''

new_sql = '''        "-- Consulta h\\u00edbrida auditable directamente en DB Browser for SQLite:\\n"
        "SELECT u.name AS operador, v.name AS recinto, rc.engine_version,\\n"
        "       json_extract(rc.calculated_results, '$.totalWatts') AS total_watts,\\n"
        "       json_extract(rc.calculated_results, '$.electricalSummary.recommendedSectionMm2') AS seccion_cable_mm2,\\n"
        "       json_extract(rc.calculated_results, '$.electricalSummary.voltageDropPct') AS caida_tension_pct,\\n"
        "       json_extract(rc.calculated_results, '$.acousticSummary.sweetSpotDba') AS sweet_spot_dba\\n"
        "FROM users u\\n"
        "JOIN venues v ON u.id = v.owner_id\\n"
        "JOIN rider_calculations rc ON v.id = rc.venue_id\\n"
        "WHERE json_extract(rc.calculated_results, '$.electricalSummary.secCompliant') = 1;"'''

code = code.replace(old_sql, new_sql)

# 5. Pregunta 14
code = code.replace(
    '["14", "¿Por qué base de datos híbrida 3FN + JSONB?", "ACID 3FN asegura integridad referencial en usuarios, circuitos y auditoría, mientras JSONB con índices GIN absorbe el polimorfismo de equipos."],',
    '["14", "¿Por qué base de datos híbrida SQLite + JSON?", "Para el MVP, 4 tablas 3FN en SQLite aseguran integridad referencial y portabilidad total con dev.db (auditable en DB Browser), mientras campos JSON absorben el cálculo sin sobrediseñar tablas intermedias."],'
)

# 6. Tabla de Rúbrica Anexo A
code = code.replace(
    '["2.1.4.8 Define entidades y relaciones PK/FK (10 pts)", "Sección 4.2 Tabla 10, Figura 12 (DER) y script sql/schema_stageplan_pg16.sql.", "Destacado"],',
    '["2.1.4.8 Define entidades y relaciones PK/FK (10 pts)", "Sección 4.2 Tabla 10 y Figura 12 (DER): 4 tablas 3FN en SQLite (dev.db) con Prisma ORM.", "Destacado"],'
)

code = code.replace(
    '["2.1.4.9 Bases estructuradas y no estructuradas (5 pts)", "Sección 4.1–4.3: PostgreSQL 16 3FN + JSONB GIN + ejemplo JSON y consulta SQL.", "Destacado"],',
    '["2.1.4.9 Bases estructuradas y no estructuradas (5 pts)", "Sección 4.1–4.3: SQLite 3 3FN + columnas JSON nativas (json_extract) probadas en DB Browser.", "Destacado"],'
)

with open(script_path, "w", encoding="utf-8") as f:
    f.write(code)

print("[OK] generate_sumativa_02_docx.py actualizado con éxito.")
