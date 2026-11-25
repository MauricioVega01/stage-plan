-- =============================================================================
-- STAGE PLAN — Esquema Completo Ejecutable para PostgreSQL 16 (12 Tablas)
-- Modelo Híbrido: Relacional Normalizado (3FN) + Documentos JSONB (Índices GIN)
-- Cumplimiento Normativo: SEC Pliego Técnico RIC N° 03 y RIC N° 10,
--                         D.S. N° 38 MMA (Ruido Vecinal), Ley N° 20.949 (Ley del Saco)
--                         y Ley N° 19.628 / N° 21.719 (Protección de Datos)
-- Caso de Estudio: DISTORSIONCL SPA | Autor: Mauricio Vega Castillo (Grupo G10)
-- =============================================================================

BEGIN;

-- 0. Extensión criptográfica y UUID nativa
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. Catálogo fijo de roles RBAC (1 = operador_foh, 2 = administrador, 3 = invitado_chofer)
CREATE TABLE roles (
  id          smallint PRIMARY KEY,
  nombre      text NOT NULL UNIQUE CHECK (nombre IN ('operador_foh', 'administrador', 'invitado_chofer')),
  descripcion text NOT NULL
);

INSERT INTO roles (id, nombre, descripcion) VALUES
  (1, 'operador_foh', 'Operador Técnico / DJ Owner con CRUD sobre sus recintos, riders y cálculos'),
  (2, 'administrador', 'Administrador de plataforma con auditoría global, logs y revocación de enlaces'),
  (3, 'invitado_chofer', 'Auxiliar logístico o chofer con acceso de solo lectura vía enlace temporal');

-- 2. Usuarios del sistema (alineada con prisma/schema.prisma + controles RBAC y anti-fuerza bruta)
CREATE TABLE users (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email             text NOT NULL UNIQUE,
  password_hash     text NOT NULL, -- Bcrypt cost factor 12
  name              text NOT NULL CHECK (char_length(trim(name)) >= 2),
  rol_id            smallint NOT NULL DEFAULT 1 REFERENCES roles(id) ON DELETE RESTRICT,
  organizacion      text NOT NULL DEFAULT 'DISTORSIONCL SPA',
  activo            boolean NOT NULL DEFAULT true,
  intentos_fallidos integer NOT NULL DEFAULT 0 CHECK (intentos_fallidos >= 0),
  bloqueado_hasta   timestamptz,
  token_version     integer NOT NULL DEFAULT 0 CHECK (token_version >= 0),
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_users_rol_id ON users (rol_id);

-- 3. Recintos y parámetros ambientales (D.S. N° 38 MMA)
CREATE TABLE venues (
  id                         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id                   uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name                       text NOT NULL CHECK (char_length(trim(name)) BETWEEN 2 AND 100),
  width_meters               double precision NOT NULL CHECK (width_meters >= 1.0 AND width_meters <= 500.0),
  depth_meters               double precision NOT NULL CHECK (depth_meters >= 1.0 AND depth_meters <= 500.0),
  height_meters              double precision NOT NULL CHECK (height_meters >= 1.0 AND height_meters <= 50.0),
  environment_type           text NOT NULL CHECK (environment_type IN ('INDOOR', 'OUTDOOR_PARCELA', 'OUTDOOR_OPEN')),
  electrical_distance_meters double precision NOT NULL CHECK (electrical_distance_meters >= 1.0 AND electrical_distance_meters <= 500.0),
  neighbor_distance_meters   double precision NOT NULL DEFAULT 35.0 CHECK (neighbor_distance_meters >= 5.0 AND neighbor_distance_meters <= 2000.0),
  enclosure_wall_type        text NOT NULL DEFAULT 'OPEN_AIR' CHECK (enclosure_wall_type IN ('OPEN_AIR', 'TENT_CANVAS', 'METAL_WAREHOUSE', 'BRICK_CONCRETE_CLOSED')),
  schedule_shift             text NOT NULL DEFAULT 'NIGHTTIME_21_07' CHECK (schedule_shift IN ('NIGHTTIME_21_07', 'DAYTIME_07_21')),
  event_duration_hours       smallint NOT NULL DEFAULT 7 CHECK (event_duration_hours >= 1 AND event_duration_hours <= 24),
  created_at                 timestamptz NOT NULL DEFAULT now(),
  updated_at                 timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_venues_owner_id ON venues (owner_id);

-- 4. Catálogo maestro de equipos (Modelo No Estructurado JSONB para atributos polimórficos)
CREATE TABLE equipment_catalog (
  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  category   text NOT NULL CHECK (category IN ('TOP_SPEAKER', 'SUBWOOFER', 'POWER_AMP', 'LIGHTING_DMX', 'DJ_GEAR')),
  brand      text NOT NULL,
  model      text NOT NULL,
  specs_json jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (brand, model)
);
CREATE INDEX idx_equipment_catalog_specs_gin ON equipment_catalog USING gin (specs_json jsonb_path_ops);

-- 5. Cálculos de montaje y resultados integrales (Modelo Híbrido Relacional + JSONB)
CREATE TABLE rider_calculations (
  id                 uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id           uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  venue_id           uuid NOT NULL REFERENCES venues(id) ON DELETE CASCADE,
  engine_version     text NOT NULL DEFAULT '1.0.0',
  rider_input        jsonb NOT NULL DEFAULT '{}'::jsonb,
  params_used        jsonb NOT NULL DEFAULT '{}'::jsonb,
  calculated_results jsonb NOT NULL DEFAULT '{}'::jsonb,
  alerts_snapshot    jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at         timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_rider_calculations_owner_id ON rider_calculations (owner_id);
CREATE INDEX idx_rider_calculations_venue_id ON rider_calculations (venue_id);
CREATE INDEX idx_rider_calculations_results_gin ON rider_calculations USING gin (calculated_results jsonb_path_ops);
CREATE INDEX idx_rider_calculations_input_gin ON rider_calculations USING gin (rider_input jsonb_path_ops);

-- 6. Lotes multilote de cajas acústicas y subwoofers (Activa vs Pasiva + Amplificación Power)
CREATE TABLE equipment_lots (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calculation_id       uuid NOT NULL REFERENCES rider_calculations(id) ON DELETE CASCADE,
  catalog_id           uuid REFERENCES equipment_catalog(id) ON DELETE SET NULL,
  lot_role             text NOT NULL CHECK (lot_role IN ('TOP_PA', 'SUBWOOFER', 'DELAY_TOWER', 'BOOTH_MONITOR')),
  label                text NOT NULL,
  technology           text NOT NULL CHECK (technology IN ('ACTIVE', 'PASSIVE')),
  quantity             integer NOT NULL CHECK (quantity >= 1 AND quantity <= 64),
  cone_inches          smallint NOT NULL CHECK (cone_inches IN (8, 10, 12, 15, 18, 21)),
  rms_watts            integer NOT NULL CHECK (rms_watts > 0),
  peak_watts           integer NOT NULL CHECK (peak_watts >= rms_watts),
  power_amp_watts      integer CHECK (power_amp_watts IS NULL OR power_amp_watts > 0),
  impedance_ohms       numeric(4,2) CHECK (impedance_ohms IS NULL OR impedance_ohms >= 2.0),
  wiring_mode          text CHECK (wiring_mode IS NULL OR wiring_mode IN ('INDEPENDENT_CHANNELS', 'PARALLEL_SPEAKON_LINK')),
  is_protect_alert     boolean NOT NULL DEFAULT false,
  weight_kg_unit       numeric(5,2) NOT NULL DEFAULT 22.0 CHECK (weight_kg_unit > 0 AND weight_kg_unit <= 120.0)
);
CREATE INDEX idx_equipment_lots_calc_id ON equipment_lots (calculation_id);

-- 7. Luminarias DMX individuales (conteo unitario x1, consumo en Watts y metraje desde Cabina)
CREATE TABLE lighting_fixtures (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calculation_id   uuid NOT NULL REFERENCES rider_calculations(id) ON DELETE CASCADE,
  name             text NOT NULL,
  fixture_type     text NOT NULL CHECK (fixture_type IN ('PAR_LED_X1', 'MOVING_HEAD', 'STROBE_BLINDER', 'LASER_EFFECT', 'HAZER_SMOKE')),
  quantity         integer NOT NULL CHECK (quantity >= 1),
  watts_per_unit   integer NOT NULL CHECK (watts_per_unit > 0),
  dmx_channels     smallint NOT NULL CHECK (dmx_channels >= 1 AND dmx_channels <= 512),
  mount_zone       text NOT NULL CHECK (mount_zone IN ('TRUSS_LEFT', 'TRUSS_RIGHT', 'TRUSS_CENTER', 'FLOOR_TOTEM')),
  dmx_cable_meters numeric(6,2) NOT NULL CHECK (dmx_cable_meters >= 1.0)
);
CREATE INDEX idx_lighting_fixtures_calc_id ON lighting_fixtures (calculation_id);

-- 8. Circuitos eléctricos SEC RIC N° 03 / RIC N° 10 y Postes Guía de radio de curvatura
CREATE TABLE electrical_circuits (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calculation_id       uuid NOT NULL REFERENCES rider_calculations(id) ON DELETE CASCADE,
  line_code            text NOT NULL CHECK (line_code IN ('L1_SUBS', 'L2_TOPS_BOOTH', 'L3_LIGHTING_FX')),
  power_strip_code     text NOT NULL, -- Ej: Z1 (10A), Z2 (16A), Z3 (10A), Z4 (10A)
  breaker_amps         smallint NOT NULL CHECK (breaker_amps IN (10, 16, 20, 25, 32)),
  load_watts           numeric(8,2) NOT NULL CHECK (load_watts >= 0),
  load_amps            numeric(6,2) NOT NULL CHECK (load_amps >= 0),
  run_meters           numeric(6,2) NOT NULL CHECK (run_meters > 0),
  cable_section_mm2    numeric(4,2) NOT NULL CHECK (cable_section_mm2 IN (1.50, 2.50, 4.00, 6.00)),
  voltage_drop_pct     numeric(4,2) NOT NULL CHECK (voltage_drop_pct >= 0 AND voltage_drop_pct <= 3.00),
  guide_posts_count    smallint NOT NULL DEFAULT 2 CHECK (guide_posts_count >= 0),
  min_bend_radius_mm   numeric(6,2) NOT NULL CHECK (min_bend_radius_mm >= 48.0),
  sec_compliant        boolean NOT NULL DEFAULT true
);
CREATE INDEX idx_electrical_circuits_calc_id ON electrical_circuits (calculation_id);

-- 9. Ruteo de señales de audio balanceado, Pro DJ Link, Speakon y DMX512
CREATE TABLE audio_routes (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  calculation_id uuid NOT NULL REFERENCES rider_calculations(id) ON DELETE CASCADE,
  source_device  text NOT NULL, -- Ej: Pioneer DJM-900NXS2 Master Out / Booth Out
  target_device  text NOT NULL, -- Ej: PA Top A (XLR) / Power Ch A / Truss Izq
  signal_type    text NOT NULL CHECK (signal_type IN ('XLR_BALANCED', 'TRS_TO_XLR_BOOTH', 'SPEAKON_NL4', 'RJ45_PRO_DJ_LINK', 'DMX512_3PIN')),
  length_meters  numeric(6,2) NOT NULL CHECK (length_meters > 0),
  haas_delay_ms  numeric(6,2) NOT NULL DEFAULT 0.0 CHECK (haas_delay_ms >= 0)
);
CREATE INDEX idx_audio_routes_calc_id ON audio_routes (calculation_id);

-- 10. Enlaces temporales compartidos para bodega/chofer (alineada con prisma/schema.prisma)
CREATE TABLE shared_links (
  id                   uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id             uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  rider_calculation_id uuid NOT NULL REFERENCES rider_calculations(id) ON DELETE CASCADE,
  token                text NOT NULL UNIQUE,
  expires_at           timestamptz NOT NULL,
  is_revoked           boolean NOT NULL DEFAULT false,
  created_at           timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_shared_links_calc_id ON shared_links (rider_calculation_id);

-- 11. Bitácora inmutable de auditoría de seguridad (Anti-IDOR, Auth y PDF)
CREATE TABLE audit_logs (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id     uuid REFERENCES users(id) ON DELETE SET NULL,
  event_type  text NOT NULL CHECK (event_type IN ('LOGIN_OK', 'LOGIN_FAIL', 'IDOR_BLOCKED_403', 'CALC_CREATED', 'PDF_EXPORTED', 'LINK_REVOKED')),
  resource_id uuid,
  ip_address  inet,
  detail_json jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX idx_audit_logs_event_time ON audit_logs (event_type, created_at DESC);

-- 12. Registro de retroalimentación de usuarios y trazabilidad UX/UI (DISTORSIONCL SPA)
CREATE TABLE user_feedback (
  id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id        uuid REFERENCES users(id) ON DELETE SET NULL,
  app_version    text NOT NULL,
  screen_name    text NOT NULL,
  finding        text NOT NULL,
  action_taken   text NOT NULL,
  status         text NOT NULL CHECK (status IN ('IMPLEMENTADO', 'VERIFICADO', 'PENDIENTE')),
  created_at     timestamptz NOT NULL DEFAULT now()
);

-- =============================================================================
-- Trigger PL/pgSQL: Validación estricta de seguridad eléctrica y de impedancia
-- =============================================================================
CREATE OR REPLACE FUNCTION fn_validate_sec_and_impedance()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  IF TG_TABLE_NAME = 'electrical_circuits' THEN
    IF NEW.voltage_drop_pct > 3.00 THEN
      RAISE EXCEPTION 'Incumplimiento SEC RIC N° 03/10: caída de tensión %.2f%% supera máximo permitido de 3.00%%', NEW.voltage_drop_pct;
    END IF;
  ELSIF TG_TABLE_NAME = 'equipment_lots' THEN
    IF NEW.technology = 'PASSIVE' AND NEW.impedance_ohms IS NOT NULL AND NEW.impedance_ohms < 3.20 AND NEW.is_protect_alert = false THEN
      RAISE EXCEPTION 'Impedancia Speakon crítica (%.2f Ohms < 3.20 Ohms) requiere is_protect_alert = true', NEW.impedance_ohms;
    END IF;
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_validate_sec_circuit
  BEFORE INSERT OR UPDATE ON electrical_circuits
  FOR EACH ROW EXECUTE FUNCTION fn_validate_sec_and_impedance();

CREATE TRIGGER trg_validate_lot_impedance
  BEFORE INSERT OR UPDATE ON equipment_lots
  FOR EACH ROW EXECUTE FUNCTION fn_validate_sec_and_impedance();

COMMIT;

-- =============================================================================
-- Consultas Híbridas de Auditoría (SQL Relacional + Operadores JSONB)
-- =============================================================================
-- 1) Auditoría de cumplimiento SEC y trazabilidad por evento:
-- SELECT u.name AS operador, v.name AS recinto, rc.engine_version,
--        ec.line_code, ec.cable_section_mm2, ec.voltage_drop_pct,
--        (rc.calculated_results->'acousticSummary'->>'sweetSpotDb')::numeric AS sweet_spot_dba
-- FROM users u
-- JOIN venues v ON u.id = v.owner_id
-- JOIN rider_calculations rc ON v.id = rc.venue_id
-- JOIN electrical_circuits ec ON rc.id = ec.calculation_id
-- WHERE ec.sec_compliant = true
--   AND rc.calculated_results @> '{"cabling": {"secCompliant": true}}'::jsonb;
--
-- 2) Inventario de cajas pasivas con amplificación Power externa y alerta Speakon:
-- SELECT v.name AS recinto, el.label, el.quantity, el.power_amp_watts, el.impedance_ohms, el.is_protect_alert
-- FROM equipment_lots el
-- JOIN rider_calculations rc ON el.calculation_id = rc.id
-- JOIN venues v ON rc.venue_id = v.id
-- WHERE el.technology = 'PASSIVE'
-- ORDER BY el.impedance_ohms ASC;
