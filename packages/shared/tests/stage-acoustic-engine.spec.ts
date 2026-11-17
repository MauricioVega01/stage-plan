import { describe, it, expect } from 'vitest';
import {
  StageAcousticEngine,
  PowerSourceValidator,
  evaluateFieldEngineering,
  AudioBox,
  VenueEnvironment,
} from '../src/calc-engine/stage-acoustic-engine';

describe('StageAcousticEngine Specification Validation (STAGE PLAN v3.5 - DISTORSIONCL SPA)', () => {
  it('Caso de Prueba 1: Escenario Base (2 Tops + 1 Subwoofer) detecta SUB_DEFICIT y calcula potencia real de red', () => {
    const boxes: AudioBox[] = [
      {
        id: 'top-1',
        name: 'Top QSC K12.2',
        type: 'TOP',
        powerRms: 1000,
        sensitivity: 98,
        potentiometerGainDb: 4, // Posición 2:00
        quantity: 2,
      },
      {
        id: 'sub-1',
        name: 'Sub KS118',
        type: 'SUB',
        powerRms: 1000,
        sensitivity: 97,
        potentiometerGainDb: 4,
        quantity: 1,
      },
    ];

    const venue: VenueEnvironment = {
      areaM2: 300,
      lengthM: 20,
      widthM: 15,
      temperatureCelsius: 20,
      targetSplDba: 102,
    };

    const result = StageAcousticEngine.calculate(boxes, venue, 800);

    // 1. Tops a 1m
    // Unit cont = 98 + 30 + 4 = 132 dB. Suma 2 tops = 132 + 3.01 = 135.0 dB cont. Peak = 135.0 + 6 = 141.0 dB.
    expect(result.frontSystem.spl1mContinuous).toBeCloseTo(135.0, 0);
    expect(result.frontSystem.spl1mPeak).toBeCloseTo(141.0, 0);

    // 2. Muestreo a 10m y 20m
    const d10 = result.frontSystem.splAtDistances.find(d => d.distanceM === 10)!;
    expect(d10.splAeq).toBeCloseTo(114.0, 0); // 141.0 - 20 - 7 = 114.0 dBA

    const d20 = result.frontSystem.splAtDistances.find(d => d.distanceM === 20)!;
    expect(d20.splAeq).toBeCloseTo(108.0, 0);

    // 3. Balance Tonal a 5m
    // Subs = 97 + 6 (piso) + 30 + 4 = 137 dB. Tops = 135 dB. Ratio = 137 - 135 = +2.0 dB.
    expect(result.tonalBalance.subToTopRatioDb).toBeCloseTo(2.0, 0);
    expect(result.tonalBalance.status).toBe('SUB_DEFICIT');

    // 4. Eléctrico: (3000 * 0.33) / 0.90 = 1100 W. Total = 1100 + 800 = 1900 W.
    expect(result.electricalRequirements.realAudioConsumptionWatts).toBe(1100);
    expect(result.electricalRequirements.totalActivePowerWatts).toBe(1900);
    expect(result.electricalRequirements.apparentPowerVa).toBe(2065);
    expect(result.electricalRequirements.minimumGeneratorKva).toBeCloseTo(2.99, 1);
  });

  it('Caso de Prueba 2: Escenario Optimizado (2 Tops + 2 Subs acoplados) con retardo Haas para delay', () => {
    const boxes: AudioBox[] = [
      {
        id: 'top-front',
        name: 'Top Frontal',
        type: 'TOP',
        powerRms: 1000,
        sensitivity: 98,
        potentiometerGainDb: 4,
        quantity: 2,
      },
      {
        id: 'sub-front',
        name: 'Sub Frontal Cluster',
        type: 'SUB',
        powerRms: 1000,
        sensitivity: 97,
        potentiometerGainDb: 4,
        quantity: 2, // 2 Subs en cluster suman +6 dB coherentes
      },
    ];

    const venue: VenueEnvironment = {
      areaM2: 300,
      lengthM: 25,
      widthM: 12,
      temperatureCelsius: 22,
      targetSplDba: 102,
    };

    const result = StageAcousticEngine.calculate(boxes, venue, 800);

    // Relación Sub/Top con 2 subs sube a +8.0 dB (OPTIMAL)
    expect(result.tonalBalance.subToTopRatioDb).toBeCloseTo(8.0, 0);
    expect(result.tonalBalance.status).toBe('OPTIMAL');

    // Retardo base a 22°C: c = 331.3 + 0.606(22) = 344.63 m/s.
    expect(result.delayLineRecommendation.haasCompensationMs).toBe(3.0);
    expect(result.delayLineRecommendation.totalDelayMs).toBeGreaterThan(30);
  });

  it('Caso de Prueba 3: Escenario de Alta Densidad (Festival 4 Tops + 4 Subs)', () => {
    const boxes: AudioBox[] = [
      {
        id: 'array-top',
        name: 'Line Array Top',
        type: 'TOP',
        powerRms: 1500,
        sensitivity: 102,
        potentiometerGainDb: 0,
        quantity: 4,
      },
      {
        id: 'sub-pro',
        name: 'Sub 18 Pro',
        type: 'SUB',
        powerRms: 2000,
        sensitivity: 99,
        potentiometerGainDb: 0,
        quantity: 4,
      },
    ];

    const venue: VenueEnvironment = {
      areaM2: 800,
      lengthM: 40,
      widthM: 20,
      temperatureCelsius: 15,
      targetSplDba: 104,
    };

    const result = StageAcousticEngine.calculate(boxes, venue, 1500);

    // Suma Tops: 102 + 10*log10(1500) + 10*log10(4) = 102 + 31.76 + 6.02 = 139.78 dB
    expect(result.frontSystem.spl1mContinuous).toBeCloseTo(139.8, 0);

    // Suma Subs (Cluster coherente + plano de tierra): (99 + 6) + 10*log10(2000) + 20*log10(4) = 105 + 33.01 + 12.04 = 150.05 dB
    expect(result.tonalBalance.subToTopRatioDb).toBeCloseTo(10.3, 0);
    expect(result.tonalBalance.status).toBe('OPTIMAL');

    // Potencia real audio: (14000 * 0.33) / 0.90 = 5133.3 W
    expect(result.electricalRequirements.realAudioConsumptionWatts).toBeCloseTo(5133, -1);
    // Generador: [(5133 + 1500) / 0.92] * 1.45 / 1000 = 10.46 kVA
    expect(result.electricalRequirements.minimumGeneratorKva).toBeCloseTo(10.46, 0);
  });

  it('Caso de Prueba 4: PowerSourceValidator evalúa Generador de 3500W vs Enchufe de Casa 10A / 16A', () => {
    // 2 Tops 1000W + 2 Subs 1000W + Cabina (2065W reales continuos)
    const gen3500 = PowerSourceValidator.evaluate(2065, {
      type: 'GENERATOR',
      generatorSurgeWatts: 3500, // ~2975W running -> ~2142W seguros continuos (96.4% -> WARNING)
    });
    expect(gen3500.status).toBe('WARNING_OVERLOAD_RISK');
    expect(gen3500.maxRecommendedGainDb).toBe(-3);

    // Misma carga en Enchufe Casa 10A (1760W seguros -> 117% -> CRITICAL)
    const home10A = PowerSourceValidator.evaluate(2065, {
      type: 'HOME_OUTLET',
      breakerAmps: 10,
    });
    expect(home10A.status).toBe('CRITICAL_TRIP_GUARANTEED');

    // Misma carga en Enchufe Casa 16A (2816W seguros -> 73.3% -> SAFE)
    const home16A = PowerSourceValidator.evaluate(2065, {
      type: 'HOME_OUTLET',
      breakerAmps: 16,
    });
    expect(home16A.status).toBe('SAFE');
  });

  it('Caso de Prueba 5: Auditoría de 5 Pilares Críticos de Terreno (HPF, Splay Angle, Fase Sub-Top, Vdrop en Drop y Tierra Copperweld)', () => {
    const audit = evaluateFieldEngineering({
      venueWidthM: 12,
      venueDepthM: 20,
      electricalDistanceM: 35,
      continuousCurrentAmps: 10,
      isGenerator: true,
      isOutdoor: true,
      subsCount: 2,
      driveRegime: 'MAX_TECHNO_1_3',
    });

    expect(audit.hpfCutoffHz).toBe(85);
    expect(audit.hpfPowerSavedPct).toBe(40);
    expect(audit.recommendedSplayAngleDeg).toBeGreaterThanOrEqual(10);
    expect(audit.frontTopsMicroDelayMs).toBe(3.5);
    expect(audit.requiresCopperweldGroundRod).toBe(true);
    expect(audit.voltageDropIf15Mm2V).toBeCloseTo(16.6, 0); // En pico de 20A a 35m con cable de 1.5mm², cae ~16.6V
  });
});

