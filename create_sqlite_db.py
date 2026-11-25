import sqlite3
import json
import os
import uuid
from datetime import datetime, timezone

def init_db(db_path):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY NOT NULL,
        email TEXT UNIQUE NOT NULL,
        passwordHash TEXT NOT NULL,
        name TEXT NOT NULL,
        createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS venues (
        id TEXT PRIMARY KEY NOT NULL,
        owner_id TEXT NOT NULL,
        name TEXT NOT NULL,
        width_meters REAL NOT NULL,
        depth_meters REAL NOT NULL,
        height_meters REAL NOT NULL,
        environment_type TEXT NOT NULL,
        electrical_distance_meters REAL NOT NULL,
        createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS rider_calculations (
        id TEXT PRIMARY KEY NOT NULL,
        owner_id TEXT NOT NULL,
        venue_id TEXT NOT NULL,
        engine_version TEXT NOT NULL,
        rider_input TEXT NOT NULL,
        params_used TEXT NOT NULL,
        calculated_results TEXT NOT NULL,
        alerts_snapshot TEXT NOT NULL,
        createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (venue_id) REFERENCES venues(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS shared_links (
        id TEXT PRIMARY KEY NOT NULL,
        owner_id TEXT NOT NULL,
        rider_calculation_id TEXT NOT NULL,
        token TEXT UNIQUE NOT NULL,
        expires_at DATETIME NOT NULL,
        is_revoked INTEGER NOT NULL DEFAULT 0,
        createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (rider_calculation_id) REFERENCES rider_calculations(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_venues_owner ON venues(owner_id);
    CREATE INDEX IF NOT EXISTS idx_calculations_owner ON rider_calculations(owner_id);
    CREATE INDEX IF NOT EXISTS idx_calculations_venue ON rider_calculations(venue_id);
    CREATE INDEX IF NOT EXISTS idx_shared_token ON shared_links(token);
    """)

    now_iso = datetime.now(timezone.utc).isoformat()

    # Usuario 1: Mauricio Vega (Técnico / Operador FOH DISTORSIONCL)
    user_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO users (id, email, passwordHash, name, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        "m.vegac@alumnos.inacap.cl",
        "$2b$12$K1bH/h7KjY0oZ8Q7Y0GqNuH3F9u2P1yQYV2y6V5tK4bN2r1jL8p6S", # Hash Bcrypt real
        "Mauricio Vega Castillo",
        now_iso,
        now_iso
    ))

    # Recinto 1: Parcela Curacaví
    venue1_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO venues (id, owner_id, name, width_meters, depth_meters, height_meters, environment_type, electrical_distance_meters, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        venue1_id,
        user_id,
        "Parcela Los Espinos, Curacaví",
        18.0,
        32.0,
        4.5,
        "OUTDOOR_PARCELA",
        35.0,
        now_iso,
        now_iso
    ))

    # Recinto 2: Galpón Bellavista
    venue2_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO venues (id, owner_id, name, width_meters, depth_meters, height_meters, environment_type, electrical_distance_meters, createdAt, updatedAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        venue2_id,
        user_id,
        "Galpón Estudio DISTORSIONCL, Recoleta",
        12.0,
        22.0,
        5.0,
        "INDOOR",
        15.0,
        now_iso,
        now_iso
    ))

    # Cálculo Rider Real en JSON
    calc_id = str(uuid.uuid4())
    rider_input = {
        "audio": {
            "systemType": "ACTIVE",
            "topsCount": 2,
            "topsRmsWatts": 700,
            "topsSensitivityDb": 98,
            "subsCount": 2,
            "subsRmsWatts": 1200,
            "topsMountedOnSubPole": True
        },
        "lighting": [
            {"type": "PAR_LED", "nominalWatts": 120, "quantity": 4}
        ],
        "djBoothNominalWatts": 450,
        "powerSource": {
            "type": "GRID_220V",
            "circuitBreakerAmps": "16A"
        },
        "hasHighInrushEquipment": False
    }

    params_used = {
        "nominalVoltage": 220,
        "safetyMarginPct": 20,
        "maxVoltageDropPct": 3.0,
        "copperResistivity": 0.0178,
        "powerFactorLoad": 0.95
    }

    calculated_results = {
        "totalWatts": 3250,
        "electrical": {
            "nominalCurrentAmps": 14.77,
            "designCurrentAmps": 17.73,
            "recommendedSectionMm2": 2.5,
            "voltageDropVolts": 4.80,
            "voltageDropPct": 2.18,
            "isSecCompliant": True,
            "standard": "SEC RIC N° 03 / RIC N° 10"
        },
        "acoustics": {
            "subwooferConfiguration": "MONO_CLUSTER_CENTER",
            "clusterGainDb": 6.0,
            "delayHaasMs": 35.0,
            "estimatedSweetSpotDba": 102
        },
        "cablingLogistics": {
            "powerCables25mm": 2,
            "dmxCables": 4,
            "xlrBalancedCables": 6,
            "heavyBaggageAlert": "Subwoofers 18in (36 kg c/u) exceden Ley N° 20.949: manipular entre 2 personas."
        }
    }

    alerts_snapshot = {
        "electricalAlert": "OK",
        "electricalMessage": "Caída de tensión 2.18% cumple norma SEC (< 3%). Conductor seleccionado: 2.5 mm².",
        "acousticsDelayRequired": True,
        "acousticsReasons": "Pista mayor a 25m: se recomienda torre de delay a 18m con retardo Haas de 35ms."
    }

    cursor.execute("""
        INSERT INTO rider_calculations (id, owner_id, venue_id, engine_version, rider_input, params_used, calculated_results, alerts_snapshot, createdAt)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        calc_id,
        user_id,
        venue1_id,
        "3.1.0",
        json.dumps(rider_input),
        json.dumps(params_used),
        json.dumps(calculated_results),
        json.dumps(alerts_snapshot),
        now_iso
    ))

    # Enlace compartido para el chofer
    link_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO shared_links (id, owner_id, rider_calculation_id, token, expires_at, is_revoked, createdAt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        link_id,
        user_id,
        calc_id,
        "chofer-distorsioncl-evento-curacavi-2026",
        "2026-12-31T23:59:59Z",
        0,
        now_iso
    ))

    conn.commit()
    conn.close()
    print(f"[OK] Base de datos creada con éxito en: {db_path}")

if __name__ == "__main__":
    targets = [
        r"C:\Users\WIT2026\Documents\stage-plan-main\stage-plan-main\packages\backend\prisma\dev.db",
        r"C:\Users\WIT2026\Documents\stage-plan-main\stage-plan-main\packages\backend\dev.db",
        r"C:\Users\WIT2026\Documents\stage-plan-main\stage-plan-main\dev.db"
    ]
    for t in targets:
        init_db(t)
