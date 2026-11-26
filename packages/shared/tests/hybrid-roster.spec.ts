import { describe, it, expect } from 'vitest';
import {
  analyzeHybridRig,
  generateSmartAcousticPlacement,
  calculatePowerAmpSizing,
  RigEquipmentItem,
  OutletPoint,
  SpeakerBatchInput,
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

describe('Power Amp Sizing Engine (Cajas Pasivas & Headroom 1.6x)', () => {
  it('PA-01: Sistema 100% activo retorna 0 amplificadores externos y 0W AC adicionales', () => {
    const batches: SpeakerBatchInput[] = [
      { id: 't1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'RCF 715', coneSizeInches: 15, rmsWatts: 700, peakWatts: 1400 },
      { id: 's1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 2, modelLabel: 'RCF 8003', coneSizeInches: 18, rmsWatts: 1100, peakWatts: 2200 },
    ];
    const res = calculatePowerAmpSizing(batches, 'INDEPENDENT_CHANNELS');
    expect(res.hasPassiveSpeakers).toBe(false);
    expect(res.hasPassiveUnits).toBe(false);
    expect(res.totalAmplifiersCount).toBe(0);
    expect(res.totalAdditionalAcPowerWatts).toBe(0);
    expect(res.suggestedRackModels).toEqual([]);
  });

  it('PA-02: 2 tops pasivos de 8 Ω (400W RMS c/u) en canales independientes exigen 640W RMS/ch @ 8 Ω', () => {
    const batches: SpeakerBatchInput[] = [
      { id: 't1', category: 'top_box', systemType: 'PASSIVE', quantity: 2, modelLabel: 'Top Pasivo 15"', coneSizeInches: 15, rmsWatts: 400, peakWatts: 800, impedanceOhms: 8 },
    ];
    const res = calculatePowerAmpSizing(batches, 'INDEPENDENT_CHANNELS');
    expect(res.hasPassiveSpeakers).toBe(true);
    expect(res.passiveTopsCount).toBe(2);
    expect(res.totalAmplifiersCount).toBe(1);
    expect(res.topsAmplifier?.loadImpedanceOhms).toBe(8);
    expect(res.topsAmplifier?.wattsPerChannelRms).toBe(640);
    expect(res.totalAdditionalAcPowerWatts).toBeGreaterThan(0);
  });

  it('PA-03: 4 tops pasivos de 8 Ω en paralelo (PARALLEL_SPEAKON_LINK) calculan carga de 4 Ω y 2 cajas/canal', () => {
    const batches: SpeakerBatchInput[] = [
      { id: 't1', category: 'top_box', systemType: 'PASSIVE', quantity: 4, modelLabel: 'Top Pasivo 12"', coneSizeInches: 12, rmsWatts: 350, peakWatts: 700, impedanceOhms: 8 },
    ];
    const res = calculatePowerAmpSizing(batches, 'PARALLEL_SPEAKON_LINK');
    expect(res.topsAmplifier?.loadImpedanceOhms).toBe(4);
    expect(res.topsAmplifier?.wattsPerChannelRms).toBe(Math.round(2 * 350 * 1.6));
    expect(res.topsAmplifier?.suggestedCommercialModel).toContain('Crown XTi 4002');
  });

  it('PA-04: 2 subwoofers pasivos de 1200W RMS recomiendan etapa gama alta Powersoft X4 / FP10000Q', () => {
    const batches: SpeakerBatchInput[] = [
      { id: 's1', category: 'sub_bass', systemType: 'PASSIVE', quantity: 2, modelLabel: 'Sub Doble 18"', coneSizeInches: 18, rmsWatts: 1200, peakWatts: 2400, impedanceOhms: 8 },
    ];
    const res = calculatePowerAmpSizing(batches, 'INDEPENDENT_CHANNELS');
    expect(res.subsAmplifier).toBeDefined();
    expect(res.subsAmplifier?.wattsPerChannelRms).toBe(Math.round(1200 * 1.6));
    expect(res.subsAmplifier?.suggestedCommercialModel).toContain('Powersoft X4');
  });

  it('PA-05: Sistema mixto (Tops pasivos + Subs pasivos + Tops activos) exige 2 amplificadores en rack', () => {
    const batches: SpeakerBatchInput[] = [
      { id: 't1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'PA Activo', coneSizeInches: 15, rmsWatts: 600, peakWatts: 1200 },
      { id: 't2', category: 'top_box', systemType: 'PASSIVE', quantity: 2, modelLabel: 'Delay Pasivo', coneSizeInches: 12, rmsWatts: 300, peakWatts: 600, impedanceOhms: 8 },
      { id: 's1', category: 'sub_bass', systemType: 'PASSIVE', quantity: 2, modelLabel: 'Sub Pasivo 18"', coneSizeInches: 18, rmsWatts: 800, peakWatts: 1600, impedanceOhms: 8 },
    ];
    const res = calculatePowerAmpSizing(batches, 'INDEPENDENT_CHANNELS');
    expect(res.totalAmplifiersCount).toBe(2);
    expect(res.suggestedRackModels.length).toBe(2);
    expect(res.passiveTopsCount).toBe(2);
    expect(res.passiveSubsCount).toBe(2);
  });

  it('PA-06: Mantiene consistencia entre alias de interfaz (hasPassiveUnits y technicalRackDirective)', () => {
    const batches: SpeakerBatchInput[] = [
      { id: 't1', category: 'top_box', systemType: 'PASSIVE', quantity: 2, modelLabel: 'Top 12"', coneSizeInches: 12, rmsWatts: 350, peakWatts: 700, impedanceOhms: 8 },
    ];
    const res = calculatePowerAmpSizing(batches, 'INDEPENDENT_CHANNELS');
    expect(res.hasPassiveUnits).toBe(res.hasPassiveSpeakers);
    expect(res.technicalRackDirective).toBe(res.technicalSummaryDirective);
    expect(res.technicalRackDirective).toContain(`${res.totalAdditionalAcPowerWatts}W`);
  });
});

