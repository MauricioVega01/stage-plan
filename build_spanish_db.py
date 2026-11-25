import sqlite3
import os
import json
from datetime import datetime, timedelta

def create_and_seed_spanish_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = OFF;")
    
    # Dropear tablas anteriores (ingles o previas)
    old_tables = [
        "shared_links", "rider_calculations", "venues", "users",
        "enlaces_compartidos", "calculos_rider", "recintos", "usuarios"
    ]
    for tbl in old_tables:
        cur.execute(f"DROP TABLE IF EXISTS {tbl};")
    
    cur.execute("PRAGMA foreign_keys = ON;")
    
    # DDL en Español
    cur.execute("""
    CREATE TABLE usuarios (
        id TEXT PRIMARY KEY,
        correo TEXT UNIQUE NOT NULL,
        clave_hash TEXT NOT NULL,
        nombre TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'ADMIN',
        fecha_creacion TEXT NOT NULL,
        fecha_actualizacion TEXT NOT NULL
    );
    """)
    
    cur.execute("""
    CREATE TABLE recintos (
        id TEXT PRIMARY KEY,
        usuario_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        nombre TEXT NOT NULL,
        ancho_metros REAL NOT NULL,
        largo_metros REAL NOT NULL,
        alto_metros REAL NOT NULL,
        tipo_entorno TEXT NOT NULL,
        distancia_electrica_metros REAL NOT NULL,
        fecha_creacion TEXT NOT NULL,
        fecha_actualizacion TEXT NOT NULL
    );
    """)
    
    cur.execute("""
    CREATE TABLE calculos_rider (
        id TEXT PRIMARY KEY,
        usuario_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        recinto_id TEXT NOT NULL REFERENCES recintos(id) ON DELETE CASCADE,
        version_motor TEXT NOT NULL,
        entrada_rider TEXT NOT NULL,
        parametros_usados TEXT NOT NULL,
        resultados_calculados TEXT NOT NULL,
        alertas_snapshot TEXT NOT NULL,
        fecha_creacion TEXT NOT NULL
    );
    """)
    
    cur.execute("""
    CREATE TABLE enlaces_compartidos (
        id TEXT PRIMARY KEY,
        usuario_id TEXT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        calculo_rider_id TEXT NOT NULL REFERENCES calculos_rider(id) ON DELETE CASCADE,
        token TEXT UNIQUE NOT NULL,
        fecha_expiracion TEXT NOT NULL,
        esta_revocado INTEGER NOT NULL DEFAULT 0,
        fecha_creacion TEXT NOT NULL
    );
    """)
    
    now = datetime.utcnow().isoformat() + "Z"
    exp = (datetime.utcnow() + timedelta(days=7)).isoformat() + "Z"
    
    # Seed Usuario
    user_id = "usr_mv_2026_01"
    cur.execute("""
    INSERT INTO usuarios (id, correo, clave_hash, nombre, rol, fecha_creacion, fecha_actualizacion)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        user_id,
        "mauricio.vega@distorsioncl.cl",
        "$2b$12$e8xL2/4K2xZ6c1L.oJbHh.n7wG7sK8x5Z4e.1wK6P9yO1f8hN6fWq", # bcrypt hash
        "Mauricio Vega Castillo",
        "ADMIN",
        now,
        now
    ))
    
    # Seed Recintos
    venue_curacavi = "rec_curacavi_001"
    venue_bellavista = "rec_bellavista_002"
    
    cur.execute("""
    INSERT INTO recintos (id, usuario_id, nombre, ancho_metros, largo_metros, alto_metros, tipo_entorno, distancia_electrica_metros, fecha_creacion, fecha_actualizacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        venue_curacavi,
        user_id,
        "Centro de Eventos Curacaví (Parcela Los Olivos)",
        25.0,
        12.0,
        4.5,
        "OUTDOOR_PARCELA",
        45.0,
        now,
        now
    ))
    
    cur.execute("""
    INSERT INTO recintos (id, usuario_id, nombre, ancho_metros, largo_metros, alto_metros, tipo_entorno, distancia_electrica_metros, fecha_creacion, fecha_actualizacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        venue_bellavista,
        user_id,
        "Club Subterráneo Bellavista",
        18.0,
        8.0,
        3.2,
        "INDOOR",
        15.0,
        now,
        now
    ))
    
    # Seed CalculoRider
    calc_id = "calc_curacavi_sub3250"
    rider_input = {
        "audio": {
            "systemType": "ACTIVE",
            "activeTops": [{"model": "RCF ART 715-A", "wattsRms": 500, "count": 2}],
            "activeSubs": [{"model": "RCF SUB 8003-AS", "wattsRms": 1000, "count": 2}],
            "delayTowers": [{"model": "RCF ART 710-A", "wattsRms": 300, "count": 1, "distanceMeters": 10}]
        },
        "supply": {
            "type": "GRID_CIRCUIT",
            "breakerAmps": 16,
            "lineVoltage": 220
        }
    }
    
    params_used = {
        "conductorMaterial": "COPPER",
        "tempOperatingC": 70,
        "maxVoltageDropPct": 3.0,
        "soundSpeedMs": 343.2
    }
    
    calculated_results = {
        "totalWatts": 2600,
        "designAmps": 14.18,
        "electricalSummary": {
            "recommendedSectionMm2": 2.5,
            "voltageDropVolts": 4.71,
            "voltageDropPct": 2.14,
            "secCompliant": 1,
            "normativeRule": "Pliego SEC RIC N° 03 (ΔV <= 3%)",
            "lineDivider": {
                "line1SubsWatts": 1600,
                "line1SubsAmps": 8.73,
                "line2TopsWatts": 1000,
                "line2TopsAmps": 5.45
            }
        },
        "acousticSummary": {
            "monoClusterCentral": True,
            "clusterGainDb": 6.0,
            "delayTowerHaasMs": 29.14,
            "splFront1m": 128.0,
            "splBack12m": 106.4,
            "sweetSpotDba": "96-102 dBA"
        },
        "cablingLogistics": {
            "xlrCablesRequired": 6,
            "speakonCablesRequired": 4,
            "powerExtensions25mm2": 2,
            "weightTotalKg": 18.5,
            "leyDelSacoCompliant": True
        }
    }
    
    alerts_snapshot = [
        {"level": "INFO", "code": "RIC03_OK", "message": "Caída de tensión 2.14% dentro del límite máximo de 3% SEC."},
        {"level": "INFO", "code": "HAAS_DELAY_SET", "message": "Torre lateral calibrada a 29.14 ms de retardo."},
        {"level": "INFO", "code": "IMPEDANCE_SAFE", "message": "Impedancia Speakon en paralelo 4.0 Ohms (Seguro >= 3.2 Ohms)."}
    ]
    
    cur.execute("""
    INSERT INTO calculos_rider (id, usuario_id, recinto_id, version_motor, entrada_rider, parametros_usados, resultados_calculados, alertas_snapshot, fecha_creacion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        calc_id,
        user_id,
        venue_curacavi,
        "4.0.0",
        json.dumps(rider_input),
        json.dumps(params_used),
        json.dumps(calculated_results),
        json.dumps(alerts_snapshot),
        now
    ))
    
    # Seed EnlaceCompartido
    link_id = "lnk_curacavi_transporte"
    cur.execute("""
    INSERT INTO enlaces_compartidos (id, usuario_id, calculo_rider_id, token, fecha_expiracion, esta_revocado, fecha_creacion)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (
        link_id,
        user_id,
        calc_id,
        "f8b9a7c2d1e4567890abcdef1234567890abcdef1234567890abcdef12345678",
        exp,
        0,
        now
    ))
    
    conn.commit()
    conn.close()
    print(f"[OK] Base de datos en espanol creada exitosamente en: {db_path}")

if __name__ == "__main__":
    paths = [
        r"stage-plan-main/dev.db",
        r"stage-plan-main/packages/backend/prisma/dev.db"
    ]
    for p in paths:
        create_and_seed_spanish_db(p)
