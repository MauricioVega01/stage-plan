import { describe, it, expect } from 'vitest';
import {
  simulateContingencyPlan,
  calculateLoadLogistics,
  CHILE_LEY_DEL_SACO_MAX_KG,
} from '../src/calc-engine/contingency-and-logistics.js';

describe('Contingency Plan B (HU08 / CU-07) & Load Logistics / Ley del Saco (HU09 / CU-08)', () => {
  it('Plan B falla de generador -> 10A desconecta primero máquina de humo e iluminación para salvar el audio', () => {
    const plan = simulateContingencyPlan('GENERATOR_FAIL_TO_10A', {
      totalAudioSubsWatts: 900,
      totalAudioTopsAndBoothWatts: 750,
      thermalFxWatts: 1500,
      lightingLedWatts: 600,
      topsCount: 2,
      subsCount: 2,
      hasPassiveSpeakers: false,
    });

    expect(plan.severity).toBe('CRITICAL');
    expect(plan.steps[0].action).toContain('Humo');
    expect(plan.resultingWatts).toBeLessThanOrEqual(1760);
    expect(plan.isSystemSurvivable).toBe(true);
  });

  it('Plan B falla de 1 Top con 3+ cajas promueve torre Delay al frente; con 2 cajas ordena modo MONO', () => {
    const planWithDelay = simulateContingencyPlan('TOP_BOX_FAILURE', {
      totalAudioSubsWatts: 800,
      totalAudioTopsAndBoothWatts: 900,
      thermalFxWatts: 0,
      lightingLedWatts: 0,
      topsCount: 3,
      subsCount: 2,
      hasPassiveSpeakers: false,
    });
    expect(planWithDelay.steps.some((s) => s.action.includes('Delay'))).toBe(true);

    const planPair = simulateContingencyPlan('TOP_BOX_FAILURE', {
      totalAudioSubsWatts: 800,
      totalAudioTopsAndBoothWatts: 700,
      thermalFxWatts: 0,
      lightingLedWatts: 0,
      topsCount: 2,
      subsCount: 2,
      hasPassiveSpeakers: false,
    });
    expect(planPair.mixerDirective).toContain('MONO');
  });

  it('Plan B disparo de Línea 3 confirma que audio (L1/L2) sigue intacto y aísla carga térmica', () => {
    const plan = simulateContingencyPlan('LIGHTING_BREAKER_TRIP', {
      totalAudioSubsWatts: 1000,
      totalAudioTopsAndBoothWatts: 800,
      thermalFxWatts: 1500,
      lightingLedWatts: 480,
      topsCount: 2,
      subsCount: 2,
      hasPassiveSpeakers: false,
    });

    expect(plan.isSystemSurvivable).toBe(true);
    expect(plan.steps[0].action).toContain('L1 Subs y L2');
    expect(plan.resultingWatts).toBe(2280);
  });

  it('Plan B falla de 1 subwoofer sin otro de respaldo ajusta HPF en Tops a rango completo moderado', () => {
    const plan = simulateContingencyPlan('SUB_FAILURE', {
      totalAudioSubsWatts: 600,
      totalAudioTopsAndBoothWatts: 700,
      thermalFxWatts: 0,
      lightingLedWatts: 0,
      topsCount: 2,
      subsCount: 1,
      hasPassiveSpeakers: false,
    });
    expect(plan.steps.some((s) => s.action.includes('HPF'))).toBe(true);
  });

  it('Ley del Saco N° 20.949 (Chile): emite alerta ergonómica obligatoria si algún equipo supera 25 kg', () => {
    const res = calculateLoadLogistics({
      items: [
        { name: 'Subwoofer 18" Activo', quantity: 2, unitWeightKg: 38 },
        { name: 'Caja Top 15"', quantity: 2, unitWeightKg: 21 },
      ],
      extensionCordsCount: 4,
      powerStripsCount: 3,
      dmxCablesCount: 6,
      dmxTerminatorsCount: 1,
      gafferRolls50m: 1,
      usesGenerator: true,
      has16ASockets: true,
    });

    expect(res.leyDelSacoMaxKg).toBe(CHILE_LEY_DEL_SACO_MAX_KG);
    expect(res.heavyItemsRequiringTwoPeople).toHaveLength(1);
    expect(res.leyDelSacoAlert).toContain('LEY DEL SACO N° 20.949');
    expect(res.recommendedOperatorsCount).toBe(2);
    expect(res.checklist.some((c) => c.label.includes('Copperweld'))).toBe(true);
    expect(res.checklist.some((c) => c.label.includes('DMX'))).toBe(true);
  });

  it('clasifica vehículo correctamente según peso total (SUV vs Pickup vs Furgón)', () => {
    const light = calculateLoadLogistics({
      items: [{ name: 'Caja 12"', quantity: 2, unitWeightKg: 14 }],
      extensionCordsCount: 2,
      powerStripsCount: 2,
      dmxCablesCount: 0,
      dmxTerminatorsCount: 0,
      gafferRolls50m: 1,
      usesGenerator: false,
      has16ASockets: false,
    });
    expect(light.recommendedVehicle).toBe('SUV / Hatchback');
    expect(light.leyDelSacoAlert).toBeNull();

    const heavy = calculateLoadLogistics({
      items: [
        { name: 'Sub Doble 18"', quantity: 6, unitWeightKg: 65 },
        { name: 'Line Array Top', quantity: 4, unitWeightKg: 28 },
      ],
      extensionCordsCount: 8,
      powerStripsCount: 6,
      dmxCablesCount: 10,
      dmxTerminatorsCount: 2,
      gafferRolls50m: 2,
      usesGenerator: true,
      has16ASockets: true,
    });
    expect(heavy.recommendedVehicle).toBe('Furgón Utilitario (H1 / Sprinter)');
  });
});
