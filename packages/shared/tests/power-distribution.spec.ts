import { describe, it, expect } from 'vitest';
import {
  calculatePowerDistribution,
  roundToCommercialExtensionLength,
} from '../src/calc-engine/power-distribution.js';
import {
  analyzeHybridRig,
  generateSmartPlacementFromBatches,
  type SpeakerBatchInput,
  type OutletPoint,
} from '../src/calc-engine/hybrid-roster.js';
import { calculateLightingAndDmxRig, type LightingBatchInput } from '../src/calc-engine/lighting-dmx.js';

function buildRigFromBatches(batches: SpeakerBatchInput[], width = 10, depth = 16) {
  const items = generateSmartPlacementFromBatches({
    venueWidthM: width,
    venueDepthM: depth,
    batches,
  });
  const outlets: OutletPoint[] = [
    { id: 'out-1', name: 'Tablero 220V SEC', maxAmps: 16, maxWatts: 3520, posX: 0.5, posY: 0.5 },
  ];
  return analyzeHybridRig(items, outlets, { x: width / 2, y: 1.2 });
}

describe('Power Distribution, Extension Cords & Power Strips Engine (HU07 / CU-06)', () => {
  const sampleBatches: SpeakerBatchInput[] = [
    {
      id: 'tops-act',
      category: 'top_box',
      systemType: 'ACTIVE',
      quantity: 2,
      modelLabel: 'JBL PRX 15',
      coneSizeInches: 15,
      rmsWatts: 500,
      peakWatts: 1000,
      impedanceOhms: 8,
    },
    {
      id: 'subs-act',
      category: 'sub_bass',
      systemType: 'ACTIVE',
      quantity: 2,
      modelLabel: 'Sub 18 Activo',
      coneSizeInches: 18,
      rmsWatts: 1000,
      peakWatts: 2000,
      impedanceOhms: 8,
    },
  ];

  it('normaliza alargadores a longitudes comerciales reales (5m, 10m, 15m, 20m, 25m, 30m)', () => {
    expect(roundToCommercialExtensionLength(4)).toBe(5);
    expect(roundToCommercialExtensionLength(9.2)).toBe(10);
    expect(roundToCommercialExtensionLength(14.8)).toBe(15);
    expect(roundToCommercialExtensionLength(22)).toBe(25);
    expect(roundToCommercialExtensionLength(29)).toBe(30);
  });

  it('calcula zapatillas separadas para Cabina DJ (Z1 L2) y Sub Cluster Industrial 16A (Z2 L1)', () => {
    const rig = buildRigFromBatches(sampleBatches, 10, 16);
    const plan = calculatePowerDistribution({
      venueWidthMeters: 10,
      venueDepthMeters: 16,
      electricalDistanceMeters: 12,
      djBoothWatts: 300,
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
    });

    const zBooth = plan.powerStrips.find((z) => z.zone === 'DJ_BOOTH');
    const zSubs = plan.powerStrips.find((z) => z.zone === 'SUB_CLUSTER');

    expect(zBooth).toBeDefined();
    expect(zBooth!.line).toBe('LINE_2_TOPS_CTRL');
    expect(zBooth!.usedSockets).toBe(4);
    expect(zBooth!.surgeProtectedRecommended).toBe(true);

    expect(zSubs).toBeDefined();
    expect(zSubs!.line).toBe('LINE_1_SUBS');
    expect(zSubs!.ratingAmps).toBe(16);
    expect(zSubs!.usedSockets).toBe(2);
    expect(plan.totalSocketsRequired).toBeGreaterThanOrEqual(8);
  });

  it('asigna 0 bocas de 220V en trípodes para cajas PASIVAS y genera recomendación Speakon', () => {
    const passiveBatches: SpeakerBatchInput[] = [
      {
        id: 'tops-pas',
        category: 'top_box',
        systemType: 'PASSIVE',
        quantity: 2,
        modelLabel: 'Caja Pasiva 15"',
        coneSizeInches: 15,
        rmsWatts: 400,
        peakWatts: 800,
        impedanceOhms: 8,
      },
    ];
    const rig = buildRigFromBatches(passiveBatches, 10, 14);
    const plan = calculatePowerDistribution({
      venueWidthMeters: 10,
      venueDepthMeters: 14,
      electricalDistanceMeters: 10,
      djBoothWatts: 300,
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
    });

    expect(plan.passiveBoxesWithout220vCount).toBe(2);
    expect(plan.extensionCords.filter((e) => e.zone === 'PA_FRONT_L' || e.zone === 'PA_FRONT_R')).toHaveLength(0);
    expect(plan.recommendations.some((r) => r.includes('CAJAS PASIVAS SIN 220V'))).toBe(true);
  });

  it('bloquea daisy-chain y divide en 2 zapatillas independientes cuando Cabina DJ supera 6 bocas', () => {
    const rig = buildRigFromBatches(sampleBatches, 10, 16);
    const plan = calculatePowerDistribution({
      venueWidthMeters: 10,
      venueDepthMeters: 16,
      electricalDistanceMeters: 10,
      djBoothWatts: 500,
      djBoothDevices: ['Mixer', 'CDJ-1', 'CDJ-2', 'Notebook', 'Interfaz', 'Router', 'Retorno DJ'],
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
    });

    const boothStrips = plan.powerStrips.filter((z) => z.zone === 'DJ_BOOTH');
    expect(boothStrips).toHaveLength(2);
    expect(plan.daisyChainPreventionTriggered).toBe(true);
    expect(plan.alerts.some((a) => a.includes('ANTI DAISY-CHAIN'))).toBe(true);
  });

  it('crea toma dedicada en Línea 3 (16A, cable >= 2.5mm²) cuando se incluye Máquina de Humo 1500W', () => {
    const rig = buildRigFromBatches(sampleBatches, 10, 16);
    const lightBatches: LightingBatchInput[] = [
      {
        id: 'f1',
        name: 'PAR LED',
        fixtureType: 'PAR_LED',
        quantity: 4,
        nominalWatts: 120,
        zone: 'TRUSS_LEFT',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 2.5,
      },
      {
        id: 's1',
        name: 'Máquina de Humo 1500W',
        fixtureType: 'FOG_MACHINE',
        quantity: 1,
        nominalWatts: 1500,
        zone: 'FLOOR',
        dmxConnector: 'NONE',
        unitWeightKg: 7.5,
        isThermalLoad: true,
      },
    ];
    const lightRes = calculateLightingAndDmxRig(lightBatches, 10, 16);

    const plan = calculatePowerDistribution({
      venueWidthMeters: 10,
      venueDepthMeters: 16,
      electricalDistanceMeters: 15,
      djBoothWatts: 300,
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
      lightingAnalysis: lightRes,
    });

    const line3Strips = plan.powerStrips.filter((z) => z.line === 'LINE_3_LIGHTING_FX');
    expect(line3Strips.length).toBe(2);
    const smokeExt = plan.extensionCords.find((e) => e.label.includes('Humo'));
    expect(smokeExt).toBeDefined();
    expect(smokeExt!.crossSectionMm2).toBeGreaterThanOrEqual(2.5);
    expect(plan.lineTotalsWatts.line3LightingAndFx).toBe(1980);
  });

  it('consolida el resumen de alargadores comerciales y advierte sobre adaptadores 16A chilenos', () => {
    const rig = buildRigFromBatches(sampleBatches, 12, 20);
    const plan = calculatePowerDistribution({
      venueWidthMeters: 12,
      venueDepthMeters: 20,
      electricalDistanceMeters: 20,
      djBoothWatts: 300,
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
    });

    expect(plan.extensionCordSummary.length).toBeGreaterThan(0);
    expect(plan.totalPowerStrips16A).toBeGreaterThanOrEqual(1);
    expect(plan.recommendations.some((r) => r.includes('16A'))).toBe(true);
  });

  it('crea zona perimetral de zapatilla y alargadores para Torres de Delay activas (4 cajas)', () => {
    const fourTops: SpeakerBatchInput[] = [
      {
        id: 't4',
        category: 'top_box',
        systemType: 'ACTIVE',
        quantity: 4,
        modelLabel: 'RCF ART 15',
        coneSizeInches: 15,
        rmsWatts: 500,
        peakWatts: 1000,
        impedanceOhms: 8,
      },
    ];
    const rig = buildRigFromBatches(fourTops, 10, 22);
    const plan = calculatePowerDistribution({
      venueWidthMeters: 10,
      venueDepthMeters: 22,
      electricalDistanceMeters: 10,
      djBoothWatts: 300,
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
    });

    expect(plan.powerStrips.some((z) => z.zone === 'DELAY_ZONE')).toBe(true);
    expect(plan.extensionCords.filter((e) => e.zone === 'DELAY_ZONE').length).toBe(2);
  });

  it('divide automáticamente Sub Cluster en 2 zapatillas industriales si supera 2.816W (80% de 16A)', () => {
    const megaSubs: SpeakerBatchInput[] = [
      {
        id: 'sub-mega',
        category: 'sub_bass',
        systemType: 'ACTIVE',
        quantity: 6,
        modelLabel: 'Sub 18 Doble',
        coneSizeInches: 18,
        rmsWatts: 1500,
        peakWatts: 3000,
        impedanceOhms: 8,
      },
    ];
    const rig = buildRigFromBatches(megaSubs, 14, 24);
    const plan = calculatePowerDistribution({
      venueWidthMeters: 14,
      venueDepthMeters: 24,
      electricalDistanceMeters: 15,
      djBoothWatts: 300,
      roster: rig.roster,
      externalAmpsCount: rig.externalAmpsRequiredCount,
    });

    const subStrips = plan.powerStrips.filter((z) => z.zone === 'SUB_CLUSTER');
    expect(subStrips.length).toBe(2);
    expect(plan.daisyChainPreventionTriggered).toBe(true);
  });
});
