import { describe, it, expect } from 'vitest';
import {
  calculateCableSizing,
  validateCircuitCapacity,
  validateGeneratorCapacity,
  getSectionByAmpacity,
  roundToNextCommercialSection,
  calculatePassiveAmplification,
  calculateSplCoverage,
  calculateSupportInventory,
  MOUNTING_PROTOCOL_STEPS,
  generateSmartPlacementFromBatches,
  analyzePassiveImpedance,
  analyzeHybridRig,
  evaluateTopToSubBalance,
  evaluateNeighborhoodNoise,
} from '../src/index.js';

describe('⚡ HU02: Dimensiones del recinto y cálculo de cableado (RIC 03 / RIC 10)', () => {
  it('Caso de prueba oficial HU02: 1.800W, 220V, L=30m, holgura 20%, caída máx 3%', () => {
    const result = calculateCableSizing({
      powerWatts: 1800,
      voltage: 220,
      distanceMeters: 30,
      safetyMarginPct: 20,
      maxVoltageDropPct: 3.0,
      copperResistivity: 0.0175,
      powerFactorLoad: 1.0,
    });

    expect(result.nominalCurrentAmps).toBe(8.18);
    expect(result.designCurrentAmps).toBe(9.82);
    expect(result.theoreticalCrossSectionMm2).toBe(1.56);
    expect(result.determiningCriterion).toBe('VOLTAGE_DROP');
    expect(result.commercialCrossSectionMm2).toBe(2.5);
    expect(result.suggestedLengthMeters).toBe(33);
    expect(result.actualVoltageDropVolts).toBe(4.12);
    expect(result.actualVoltageDropPct).toBe(1.87);
    expect(result.warningRolledCable).toContain('Desenrolle completamente los alargadores');
  });

  it('Debe determinar criterio por AMPACITY cuando la corriente predomina sobre la distancia', () => {
    const result = calculateCableSizing({
      powerWatts: 4000,
      voltage: 220,
      distanceMeters: 5, // Muy corta distancia
      safetyMarginPct: 20,
      maxVoltageDropPct: 3.0,
    });
    expect(result.determiningCriterion).toBe('AMPACITY');
    expect(result.commercialCrossSectionMm2).toBeGreaterThanOrEqual(2.5);
  });

  it('Cobertura de utilidades de cable y ampacidad para calibres mayores', () => {
    expect(getSectionByAmpacity(12)).toBe(1.5);
    expect(getSectionByAmpacity(20)).toBe(2.5);
    expect(getSectionByAmpacity(25)).toBe(4.0);
    expect(getSectionByAmpacity(32)).toBe(6.0);
    expect(getSectionByAmpacity(45)).toBe(10.0);
    expect(getSectionByAmpacity(60)).toBe(16.0);
    expect(getSectionByAmpacity(100)).toBe(16.0); // Máximo contemplado

    expect(roundToNextCommercialSection(1.2)).toBe(1.5);
    expect(roundToNextCommercialSection(3.2)).toBe(4.0);
    expect(roundToNextCommercialSection(8.0)).toBe(10.0);
    expect(roundToNextCommercialSection(25.0)).toBe(16.0);
  });
});

describe('🔌 HU03: Carga eléctrica, kW/kVA y dimensionamiento de audio', () => {
  it('Caso (a) Circuito: 2.000W en enchufe de 10A (220V) -> ALERTA CRÍTICA', () => {
    const result = validateCircuitCapacity(2000, 10, 20, 220, 1.0);
    expect(result.nominalCurrentAmps).toBe(9.09);
    expect(result.designCurrentAmps).toBe(10.91);
    expect(result.usageRatio).toBe(1.091);
    expect(result.alertLevel).toBe('CRITICAL');
    expect(result.alertMessage).toContain('ALERTA CRÍTICA');
  });

  it('Circuito: debe generar advertencia si el uso está entre 90% y 100%', () => {
    const result = validateCircuitCapacity(1700, 10, 20, 220, 1.0);
    expect(result.alertLevel).toBe('WARNING');
    expect(result.alertMessage).toContain('ADVERTENCIA');
  });

  it('Circuito: debe ser INFO si la carga está holgada (< 90%)', () => {
    const result = validateCircuitCapacity(1000, 10, 20, 220, 1.0);
    expect(result.alertLevel).toBe('INFO');
  });

  it('Caso (b) Generador: 5 kVA (FP 0.8 = 4.0 kW) con carga de 3.5 kW -> ALERTA CRÍTICA', () => {
    const result = validateGeneratorCapacity(3500, 5, 0.8, 20);
    expect(result.designPowerWatts).toBe(4200);
    expect(result.usageRatio).toBe(1.05);
    expect(result.alertLevel).toBe('CRITICAL');
    expect(result.alertMessage).toContain('ALERTA CRÍTICA');
  });

  it('Generador: debe emitir WARNING si está entre 90% y 100%', () => {
    const result = validateGeneratorCapacity(3100, 5, 0.8, 20); // 3.1 * 1.2 = 3.72 kW / 4.0 = 93%
    expect(result.alertLevel).toBe('WARNING');
  });

  it('Generador: debe ser INFO si la capacidad es holgada', () => {
    const result = validateGeneratorCapacity(2000, 5, 0.8, 20);
    expect(result.alertLevel).toBe('INFO');
  });

  it('Caso (c) Audio pasivo: 2 cajas de 400W RMS / 8 ohm en paralelo en 1 canal', () => {
    const result = calculatePassiveAmplification({
      boxesCount: 2,
      boxRmsWatts: 400,
      boxImpedanceOhms: 8,
      wiring: 'PARALLEL',
      headroomFactor: 1.5,
      minAmpImpedance: 4,
      ampEfficiency: 0.8,
    });

    expect(result.equivalentImpedanceOhms).toBe(4);
    expect(result.totalChannelRmsWatts).toBe(800);
    expect(result.recommendedAmpWattsPerChannel).toBe(1200);
    expect(result.networkPowerMusicalWatts).toBe(500);
    expect(result.networkPowerConservativeWatts).toBe(1000);
    expect(result.isBelowMinImpedance).toBe(false);
    expect(result.alertLevel).toBe('INFO');
  });

  it('Audio pasivo: conexión en SERIE', () => {
    const result = calculatePassiveAmplification({
      boxesCount: 2,
      boxRmsWatts: 250,
      boxImpedanceOhms: 8,
      wiring: 'SERIES',
    });
    expect(result.equivalentImpedanceOhms).toBe(16);
    expect(result.totalChannelRmsWatts).toBe(500);
  });

  it('Caso (c) [Variación BVA]: impedancia inferior a la mínima del amplificador', () => {
    const result = calculatePassiveAmplification({
      boxesCount: 4,
      boxRmsWatts: 300,
      boxImpedanceOhms: 8,
      wiring: 'PARALLEL',
      minAmpImpedance: 4, // 8 / 4 = 2 ohm < 4 ohm
    });
    expect(result.equivalentImpedanceOhms).toBe(2);
    expect(result.isBelowMinImpedance).toBe(true);
    expect(result.alertLevel).toBe('CRITICAL');
  });
});

describe('🪵 HU04: Inventario de soportes y disposición a piso', () => {
  it('Caso de prueba oficial HU04: 2 subwoofers y 4 tops (2 en pole mount)', () => {
    const result = calculateSupportInventory({
      subsCount: 2,
      topsCount: 4,
      topsMountedOnSubPole: 2,
      totalOutletsRequired: 8,
    });

    expect(result.subsAtFloorCount).toBe(2);
    expect(result.poleMountsCount).toBe(2);
    expect(result.tripodStandsCount).toBe(2);
    expect(result.powerStripsCount).toBe(2);
    expect(result.totalOutletsSupplied).toBe(12);
    expect(result.spareOutletsCount).toBe(4);
    expect(result.warningDiscrepancy).toBeUndefined();
  });

  it('Inventario: debe alertar discrepancia si piden más pole mounts que subs disponibles', () => {
    const result = calculateSupportInventory({
      subsCount: 1,
      topsCount: 4,
      topsMountedOnSubPole: 3,
      totalOutletsRequired: 4,
    });
    expect(result.poleMountsCount).toBe(1);
    expect(result.tripodStandsCount).toBe(3);
    expect(result.warningDiscrepancy).toBeDefined();
  });

  it('Protocolo de montaje: debe contener los 5 pasos obligatorios', () => {
    expect(MOUNTING_PROTOCOL_STEPS.length).toBe(5);
    expect(MOUNTING_PROTOCOL_STEPS[0].title).toContain('Piso');
    expect(MOUNTING_PROTOCOL_STEPS[2].instruction).toContain('Desenrollar');
  });
});

describe('🔊 HU05: Cobertura SPL y Layout 2D', () => {
  it('Caso de prueba oficial HU05: Sensibilidad 98 dB @ 1W/1m, 500W, fondo a 16m', () => {
    const result = calculateSplCoverage({
      sensitivityDb: 98,
      powerRmsWatts: 500,
      distanceFirstRowMeters: 4,
      distanceBackMeters: 16,
      splTargetDb: 98,
      maxSplDropThresholdDb: 10,
    });

    expect(result.splAt1mDb).toBe(125.0);
    expect(result.splAtFirstRowDb).toBe(113.0);
    expect(result.splAtBackDb).toBe(100.9);
    expect(result.splDropFirstRowToBackDb).toBe(12.1);
    expect(result.recommendDelayFill).toBe(true);
    expect(result.recommendationReason.some(r => r.includes('caída sonora'))).toBe(true);
  });

  it('SPL en fondo bajo objetivo dB y exceso de distancia de agudos en exterior (> 20m)', () => {
    const result = calculateSplCoverage({
      sensitivityDb: 92,
      powerRmsWatts: 200,
      distanceFirstRowMeters: 4,
      distanceBackMeters: 25,
      splTargetDb: 98,
      maxSplDropThresholdDb: 15,
      isIndoor: false,
    });
    expect(result.recommendDelayFill).toBe(true);
    expect(result.recommendationReason.some(r => r.includes('absorción'))).toBe(true);
    expect(result.recommendationReason.some(r => r.includes('debajo de los 98 dB'))).toBe(true);
    expect(result.indoorAcousticNote).toContain('exterior');
  });

  it('SPL en recinto cerrado indoor (< 30m sin alerta de absorción)', () => {
    const result = calculateSplCoverage({
      sensitivityDb: 102,
      powerRmsWatts: 1000,
      distanceFirstRowMeters: 4,
      distanceBackMeters: 10,
      splTargetDb: 95,
      maxSplDropThresholdDb: 12,
      isIndoor: true,
    });
    expect(result.recommendDelayFill).toBe(false);
    expect(result.indoorAcousticNote).toContain('reverberante');
  });
});

describe('🎛️ Stage Plan v4.0: Constructor Híbrido Multilote (RMS + Peak), Impedancia y Vecinos', () => {
  it('Lotes Mixtos (2 Cajas Activas 500W RMS + 1 Pasiva 350W RMS): asigna A y B al frente y C como refuerzo Delay con Gain Matching', () => {
    const items = generateSmartPlacementFromBatches({
      venueWidthM: 12,
      venueDepthM: 22,
      batches: [
        {
          id: 'b1',
          category: 'top_box',
          systemType: ' PASSIVE' as any,
          quantity: 1,
          modelLabel: 'Caja Pasiva 12"',
          coneSizeInches: 12,
          rmsWatts: 350,
          peakWatts: 700,
          impedanceOhms: 8,
        },
        {
          id: 'b2',
          category: 'top_box',
          systemType: 'ACTIVE',
          quantity: 2,
          modelLabel: 'Caja Activa 15"',
          coneSizeInches: 15,
          rmsWatts: 500,
          peakWatts: 1000,
        },
        {
          id: 'b3',
          category: 'sub_bass',
          systemType: 'ACTIVE',
          quantity: 1,
          modelLabel: 'Sub Activo 18"',
          coneSizeInches: 18,
          rmsWatts: 800,
          peakWatts: 1600,
        },
        {
          id: 'b4',
          category: 'sub_bass',
          systemType: 'PASSIVE',
          quantity: 1,
          modelLabel: 'Sub Pasivo 18"',
          coneSizeInches: 18,
          rmsWatts: 600,
          peakWatts: 1200,
          impedanceOhms: 8,
        },
      ].map(b => ({ ...b, systemType: b.systemType.trim() as 'ACTIVE' | 'PASSIVE' })),
    });

    const tops = items.filter(i => i.category === 'top_box');
    const subs = items.filter(i => i.category === 'sub_bass');

    expect(tops.length).toBe(3);
    expect(subs.length).toBe(2);

    // Las 2 de mayor potencia (500W RMS Activas) deben ser A y B en el frente
    expect(tops[0].tag).toBe('A');
    expect(tops[0].rmsWatts).toBe(500);
    expect(tops[1].tag).toBe('B');
    expect(tops[1].rmsWatts).toBe(500);

    // La 3ra caja (350W RMS Pasiva) debe ser C en DELAY_RING_1 con retardo > 0 y gainMatchingDb negativo
    expect(tops[2].tag).toBe('C');
    expect(tops[2].rmsWatts).toBe(350);
    expect(tops[2].zone).toBe('DELAY_RING_1');
    expect(tops[2].delayMs).toBeGreaterThan(25);
    expect(tops[2].gainMatchingDb).toBeLessThan(0);
  });

  it('Separación de Líneas Eléctricas: analyzeHybridRig divide Sub-Bajos en Línea 1 y Tops+DJ en Línea 2', () => {
    const items = generateSmartPlacementFromBatches({
      venueWidthM: 10,
      venueDepthM: 18,
      batches: [
        {
          id: 't1',
          category: 'top_box',
          systemType: 'ACTIVE',
          quantity: 2,
          modelLabel: 'Top Activo',
          coneSizeInches: 15,
          rmsWatts: 500,
          peakWatts: 1000,
        },
        {
          id: 's1',
          category: 'sub_bass',
          systemType: 'ACTIVE',
          quantity: 2,
          modelLabel: 'Sub Activo',
          coneSizeInches: 18,
          rmsWatts: 1000,
          peakWatts: 2000,
        },
      ],
    });

    const analysis = analyzeHybridRig(items, [
      { id: 'o1', name: 'Tablero Principal', maxAmps: 16, maxWatts: 3520, posX: 0, posY: 0 },
    ]);

    expect(analysis.totalRmsAudioWatts).toBe(3000);
    expect(analysis.totalPeakAudioWatts).toBe(6000);
    expect(analysis.electricalLines.line1SubsWatts).toBeGreaterThan(700);
    expect(analysis.electricalLines.line2TopsCtrlWatts).toBeGreaterThan(1100);
  });

  it('Calculadora de Impedancia en Paralelo: 2 cajas de 8Ω en Link dan 4Ω (HIGH_LOAD) y 3 cajas de 8Ω dan 2.67Ω (DANGER_PROTECT_SHORT)', () => {
    const twoBoxesLink = analyzePassiveImpedance(
      [
        {
          id: 'p1',
          category: 'top_box',
          systemType: 'PASSIVE',
          quantity: 2,
          modelLabel: 'Pasiva 8 Ohm',
          coneSizeInches: 15,
          rmsWatts: 400,
          peakWatts: 800,
          impedanceOhms: 8,
        },
      ],
      'PARALLEL_SPEAKON_LINK'
    );
    expect(twoBoxesLink.topsEffectiveOhms).toBe(4);
    expect(twoBoxesLink.status).toBe('HIGH_LOAD_4_OHM');

    const threeBoxesLink = analyzePassiveImpedance(
      [
        {
          id: 'p2',
          category: 'top_box',
          systemType: 'PASSIVE',
          quantity: 3,
          modelLabel: 'Pasiva 8 Ohm',
          coneSizeInches: 15,
          rmsWatts: 400,
          peakWatts: 800,
          impedanceOhms: 8,
        },
      ],
      'PARALLEL_SPEAKON_LINK'
    );
    expect(threeBoxesLink.topsEffectiveOhms).toBe(2.67);
    expect(threeBoxesLink.status).toBe('DANGER_PROTECT_SHORT');
  });

  it('Detector de Cuello de Botella (Top-to-Sub Balance): detecta déficit de subgraves y recomienda atenuar Tops', () => {
    const deficit = evaluateTopToSubBalance({
      totalTopRmsWatts: 2000,
      totalSubRmsWatts: 500,
      topsCount: 4,
      subsCount: 1,
    });
    expect(deficit.status).toBe('SUB_BASS_DEFICIT');
    expect(deficit.topTrimAdjustmentDb).toBeLessThan(0);
  });

  it('Simulador de Ruido a Vecinos (D.S. N° 38 MMA): alerta multa en exterior nocturno a 20m y cumple en ladrillo cerrado a 80m', () => {
    const highRisk = evaluateNeighborhoodNoise({
      spl1mContinuousDba: 122,
      neighborDistanceM: 20,
      enclosureType: 'OPEN_AIR',
      scheduleShift: 'NIGHTTIME_21_07',
    });
    expect(highRisk.status).toBe('HIGH_RISK_MUNICIPAL_FINE');
    expect(highRisk.excessDba).toBeGreaterThan(10);

    const compliant = evaluateNeighborhoodNoise({
      spl1mContinuousDba: 115,
      neighborDistanceM: 120,
      enclosureType: 'BRICK_CONCRETE_CLOSED',
      scheduleShift: 'DAYTIME_07_21',
    });
    expect(compliant.status).toBe('COMPLIANT_SAFE');
  });
});
