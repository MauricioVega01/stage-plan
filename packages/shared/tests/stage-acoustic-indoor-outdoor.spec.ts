import { describe, it, expect } from 'vitest';
import {
  StageAcousticEngine,
  AudioBox,
  VenueEnvironment,
} from '../src/calc-engine/stage-acoustic-engine';

describe('StageAcousticEngine - Dual Environment Validation (Outdoor vs Indoor)', () => {
  const standardBoxes: AudioBox[] = [
    {
      id: 'top-1',
      name: 'Top QSC K12.2',
      type: 'TOP',
      powerRms: 1000,
      sensitivity: 98,
      potentiometerGainDb: 4,
      quantity: 2,
    },
    {
      id: 'sub-1',
      name: 'Sub KS118',
      type: 'SUB',
      powerRms: 1000,
      sensitivity: 97,
      potentiometerGainDb: 4,
      quantity: 2,
    },
  ];

  it('TC-01: ESPACIO ABIERTO (Outdoor) - Atenuación libre por inverso del cuadrado (-6 dB/doble)', () => {
    const outdoorVenue: VenueEnvironment = {
      areaM2: 400,
      lengthM: 25,
      widthM: 16,
      temperatureCelsius: 22,
      targetSplDba: 102,
      environmentType: 'OUTDOOR_OPEN',
    };

    const result = StageAcousticEngine.calculate(standardBoxes, outdoorVenue, 800);

    // En outdoor no hay RT60
    expect(result.frontSystem.reverberationTimeRt60Seconds).toBeUndefined();

    // A 10m en campo libre cae exactamente 20 dB: 141 - 20 = 121 dB peak
    const at10m = result.frontSystem.splAtDistances.find(d => d.distanceM === 10)!;
    expect(at10m.splPeak).toBeCloseTo(121.0, 0);

    // Acoplamiento de suelo puro (+6 dB half-space)
    expect(result.tonalBalance.boundaryGainAppliedDb).toBe(6.0);
    expect(result.tonalBalance.status).toBe('OPTIMAL');
  });

  it('TC-02: ESPACIO CERRADO (Indoor) - Incorpora campo reverberante (Hopkins-Stryker) y tiempo RT60', () => {
    const indoorVenue: VenueEnvironment = {
      areaM2: 400,
      lengthM: 25,
      widthM: 16,
      heightM: 4.0,
      temperatureCelsius: 20,
      targetSplDba: 102,
      environmentType: 'INDOOR_CLOSED',
      absorptionCoefficient: 0.18, // Salón con reverberación estándar
    };

    const result = StageAcousticEngine.calculate(standardBoxes, indoorVenue, 800);

    // Debe calcular el tiempo de reverberación RT60 y la constante de sala R
    expect(result.frontSystem.reverberationTimeRt60Seconds).toBeDefined();
    expect(result.frontSystem.reverberationTimeRt60Seconds).toBeGreaterThan(1.0);
    expect(result.frontSystem.roomConstantR).toBeDefined();

    // En cerrado, a 25m (fondo) el nivel se sostiene más alto que en abierto gracias al campo reverberante
    const outdoorResult = StageAcousticEngine.calculate(standardBoxes, { ...indoorVenue, environmentType: 'OUTDOOR_OPEN' }, 800);
    const indoorBack = result.frontSystem.splAtDistances.find(d => d.distanceM === 25)!;
    const outdoorBack = outdoorResult.frontSystem.splAtDistances.find(d => d.distanceM === 25)!;

    expect(indoorBack.splPeak).toBeGreaterThan(outdoorBack.splPeak);

    // En cerrado, los subwoofers reciben ganancia acústica adicional (+9 dB en lugar de +6 dB)
    expect(result.tonalBalance.boundaryGainAppliedDb).toBe(9.0);
  });
});

