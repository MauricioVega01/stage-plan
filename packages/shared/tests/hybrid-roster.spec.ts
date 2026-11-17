import { describe, it, expect } from 'vitest';
import {
  analyzeHybridRig,
  generateSmartAcousticPlacement,
  RigEquipmentItem,
  OutletPoint,
} from '../src/calc-engine/hybrid-roster';

describe('Hybrid Rig & Equipment Roster Engine (STAGE PLAN v3.4 - DISTORSIONCL SPA)', () => {
  it('TC-01: Procesa mezcla híbrida (Cajas Activas + Sub Bajos Pasivos) con etiquetas y cables específicos', () => {
    const items: RigEquipmentItem[] = [
      // Caja Acústica Izquierda ACTIVA en atril
      {
        id: 'top-1',
        tag: 'A',
        name: 'Caja Acústica Izquierda',
        category: 'top_box',
        systemType: 'ACTIVE',
        rmsWatts: 450,
        posX: 2,
        posY: 2,
      },
      // Caja Acústica Derecha ACTIVA en atril
      {
        id: 'top-2',
        tag: 'B',
        name: 'Caja Acústica Derecha',
        category: 'top_box',
        systemType: 'ACTIVE',
        rmsWatts: 450,
        posX: 8,
        posY: 2,
      },
      // Sub Bajo Izquierdo PASIVO a piso
      {
        id: 'sub-1',
        tag: 'S1',
        name: 'Sub Bajo Izquierdo',
        category: 'sub_bass',
        systemType: 'PASSIVE',
        rmsWatts: 800,
        posX: 3,
        posY: 2,
      },
      // Sub Bajo Derecho PASIVO a piso
      {
        id: 'sub-2',
        tag: 'S2',
        name: 'Sub Bajo Derecho',
        category: 'sub_bass',
        systemType: 'PASSIVE',
        rmsWatts: 800,
        posX: 7,
        posY: 2,
      },
      // Foco Iluminación
      {
        id: 'light-1',
        tag: 'L1',
        name: 'Foco Par LED Escenario',
        category: 'lighting',
        systemType: 'ACTIVE',
        rmsWatts: 120,
        posX: 5,
        posY: 1,
      },
    ];

    const outlets: OutletPoint[] = [
      { id: 'out-1', name: 'Enchufe Pared Izquierda', maxAmps: 16, maxWatts: 3520, posX: 0, posY: 2 },
      { id: 'out-2', name: 'Enchufe Pared Derecha', maxAmps: 16, maxWatts: 3520, posX: 10, posY: 2 },
    ];

    const result = analyzeHybridRig(items, outlets, { x: 5, y: 2 });

    // Verificación de conteo híbrido
    expect(result.activeTopsCount).toBe(2);
    expect(result.passiveTopsCount).toBe(0);
    expect(result.activeSubsCount).toBe(0);
    expect(result.passiveSubsCount).toBe(2);

    // Cajas A y B son activas: se conectan a energía y requieren cable XLR
    const boxA = result.roster.find(r => r.tag === 'A')!;
    expect(boxA.powerCableType).toBe('IEC_PC');
    expect(boxA.signalCableType).toBe('XLR_AUDIO');
    expect(boxA.assignedOutletName).toBe('Enchufe Pared Izquierda');
    expect(boxA.powerCableMeters).toBeGreaterThan(0);

    const boxB = result.roster.find(r => r.tag === 'B')!;
    expect(boxB.assignedOutletName).toBe('Enchufe Pared Derecha');

    // Sub Bajos S1 y S2 son pasivos: NO se enchufan a la pared (0m de 220V al parlante), requieren Speakon
    const sub1 = result.roster.find(r => r.tag === 'S1')!;
    expect(sub1.powerCableType).toBe('NONE_PASSIVE');
    expect(sub1.powerCableMeters).toBe(0);
    expect(sub1.signalCableType).toBe('SPEAKON_PASIVO');

    // Requiere 1 amplificador externo para los 2 sub bajos pasivos
    expect(result.externalAmpsRequiredCount).toBe(1);
    expect(result.speakonCablesCount).toBe(2);

    // Foco L1 usa cable DMX
    const light1 = result.roster.find(r => r.tag === 'L1')!;
    expect(light1.signalCableType).toBe('DMX_LIGHT');

    // Cálculo de cinta gaffer
    expect(result.totalFloorTapeMeters).toBeGreaterThan(0);
    expect(result.floorTapeRolls50m).toBeGreaterThanOrEqual(1);
  });

  it('TC-02: Distribución Acústica Inteligente (PA Frontal + Torres Delay en Pista + Mono Cluster Central de Subs)', () => {
    const items = generateSmartAcousticPlacement({
      venueWidthM: 12,
      venueDepthM: 24,
      topsCount: 6,
      topsSystemType: 'ACTIVE',
      topsRmsWatts: 1000,
      subsCount: 2,
      subsSystemType: 'ACTIVE',
      subsRmsWatts: 1000,
      temperatureCelsius: 20,
    });

    const outlets: OutletPoint[] = [
      { id: 'out-1', name: 'Tablero Principal 220V', maxAmps: 32, maxWatts: 7040, posX: 0, posY: 2 },
    ];

    const analysis = analyzeHybridRig(items, outlets, { x: 6, y: 1.2 });

    expect(analysis.frontTopsCount).toBe(2); // Cajas A y B en el frente
    expect(analysis.delayTopsCount).toBe(4); // Cajas C, D (Anillo 1) y E, F (Anillo 2) en pista

    const boxA = analysis.roster.find(r => r.tag === 'A')!;
    const boxC = analysis.roster.find(r => r.tag === 'C')!;
    const boxE = analysis.roster.find(r => r.tag === 'E')!;
    const sub1 = analysis.roster.find(r => r.tag === 'S1')!;
    const sub2 = analysis.roster.find(r => r.tag === 'S2')!;

    expect(boxA.zone).toBe('PA_FRONT_L');
    expect(boxA.delayMs).toBe(0);

    expect(boxC.zone).toBe('DELAY_RING_1');
    expect(boxC.posY).toBeGreaterThan(10); // A ~52% de 24m = 12.5m
    expect(boxC.delayMs).toBeGreaterThan(30); // Tiempo de vuelo + 3ms Haas

    expect(boxE.zone).toBe('DELAY_RING_2');
    expect(boxE.posY).toBeGreaterThan(boxC.posY);
    expect(boxE.delayMs).toBeGreaterThan(boxC.delayMs);

    // Subwoofers agrupados en bloque central (< 1.7m entre centros para suma coherente +6 dB)
    expect(sub1.zone).toBe('SUB_CENTER_CLUSTER');
    expect(Math.abs(sub2.posX - sub1.posX)).toBeLessThanOrEqual(1.7);
  });
});

