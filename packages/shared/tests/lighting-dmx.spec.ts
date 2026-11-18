import { describe, it, expect } from 'vitest';
import {
  calculateLightingAndDmxRig,
  roundToStandardDmxLength,
  LIGHTING_PRESETS,
  type LightingBatchInput,
} from '../src/calc-engine/lighting-dmx.js';

describe('Lighting, FX (Fog/Laser) & Physical DMX Cabling Engine (HU06 / CU-05)', () => {
  it('devuelve estructura vacía sin alertas cuando no hay iluminación ni efectos', () => {
    const res = calculateLightingAndDmxRig([], 10, 14);
    expect(res.totalFixtureUnits).toBe(0);
    expect(res.totalLightingWatts).toBe(0);
    expect(res.totalDmxCablesCount).toBe(0);
    expect(res.requiresDedicatedLine3).toBe(false);
  });

  it('normaliza largos DMX a estándares comerciales reales (1.5m, 3m, 5m, 10m, 15m, 20m)', () => {
    expect(roundToStandardDmxLength(1.2)).toBe(1.5);
    expect(roundToStandardDmxLength(2.6)).toBe(3);
    expect(roundToStandardDmxLength(4.9)).toBe(5);
    expect(roundToStandardDmxLength(8.1)).toBe(10);
    expect(roundToStandardDmxLength(14.5)).toBe(15);
    expect(roundToStandardDmxLength(19.0)).toBe(20);
  });

  it('suma correctamente los Watts de focos PAR, cabezas móviles, láser y máquina de humo separando carga térmica en Línea 3', () => {
    const batches: LightingBatchInput[] = [
      {
        id: 'b1',
        name: 'PAR LED',
        fixtureType: 'PAR_LED',
        quantity: 4,
        nominalWatts: 120,
        zone: 'TRUSS_LEFT',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 2.5,
      },
      {
        id: 'b2',
        name: 'Cabeza Móvil Beam',
        fixtureType: 'MOVING_HEAD',
        quantity: 2,
        nominalWatts: 320,
        zone: 'TRUSS_RIGHT',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 16,
      },
      {
        id: 'b3',
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

    const res = calculateLightingAndDmxRig(batches, 12, 16);
    expect(res.totalFixtureUnits).toBe(7);
    expect(res.dmxControlledUnits).toBe(6); // Humo sin DMX no suma cables DMX
    expect(res.totalLightingWatts).toBe(4 * 120 + 2 * 320 + 1500); // 2620W
    expect(res.thermalEffectsWatts).toBe(1500);
    expect(res.nonThermalLightingWatts).toBe(1120);
    expect(res.requiresDedicatedLine3).toBe(true);
    expect(res.hasThermalLoad).toBe(true);
    expect(res.alerts.some((a) => a.includes('CARGA TÉRMICA'))).toBe(true);
  });

  it('traza cables físicos desde DMX OUT (Cabina) calculando troncales y puentes cortos por zona', () => {
    const batches: LightingBatchInput[] = [
      {
        id: 'b1',
        name: 'PAR LED',
        fixtureType: 'PAR_LED',
        quantity: 3,
        nominalWatts: 100,
        zone: 'CENTER_BOOTH',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 2.5,
      },
    ];

    const res = calculateLightingAndDmxRig(batches, 8, 12);
    // 1 troncal desde DMX OUT al primer foco + 2 puentes cortos de 1.5m entre foco 1->2 y 2->3
    expect(res.totalDmxCablesCount).toBe(3);
    expect(res.dmxRuns[0].kind).toBe('TRUNK');
    expect(res.dmxRuns[0].from).toContain('DMX OUT');
    expect(res.dmxRuns[1].kind).toBe('LINK');
    expect(res.dmxRuns[1].lengthMeters).toBe(1.5);
    expect(res.terminators120OhmCount).toBe(1);
  });

  it('recomienda Splitter DMX óptico cuando hay torres izquierda y derecha separadas >= 8m o > 32 equipos', () => {
    const batches: LightingBatchInput[] = [
      {
        id: 'l1',
        name: 'PAR Izq',
        fixtureType: 'PAR_LED',
        quantity: 2,
        nominalWatts: 120,
        zone: 'TRUSS_LEFT',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 2.5,
      },
      {
        id: 'r1',
        name: 'PAR Der',
        fixtureType: 'PAR_LED',
        quantity: 2,
        nominalWatts: 120,
        zone: 'TRUSS_RIGHT',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 2.5,
      },
    ];

    const res = calculateLightingAndDmxRig(batches, 10, 15);
    expect(res.needsDmxSplitter).toBe(true);
    expect(res.terminators120OhmCount).toBe(2); // 1 terminador al final de cada rama
    expect(res.recommendations.some((r) => r.includes('SPLITTER DMX'))).toBe(true);
  });

  it('detecta mezcla de conectores DMX 3-pin y 5-pin exigiendo adaptadores', () => {
    const batches: LightingBatchInput[] = [
      {
        id: 'm1',
        name: 'PAR 3-pin',
        fixtureType: 'PAR_LED',
        quantity: 2,
        nominalWatts: 100,
        zone: 'TRUSS_LEFT',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 2.5,
      },
      {
        id: 'm2',
        name: 'Beam Pro 5-pin',
        fixtureType: 'MOVING_HEAD',
        quantity: 2,
        nominalWatts: 300,
        zone: 'TRUSS_LEFT',
        dmxConnector: 'DMX_5PIN',
        unitWeightKg: 15,
      },
    ];

    const res = calculateLightingAndDmxRig(batches, 6, 10);
    expect(res.needs3To5PinAdapter).toBe(true);
    expect(res.alerts.some((a) => a.includes('adaptadores DMX 3-pin'))).toBe(true);
  });

  it('emite alerta obligatoria de seguridad ocular (>= 2.7m) cuando se agrega un Láser', () => {
    const batches: LightingBatchInput[] = [
      {
        id: 'las1',
        name: 'Láser RGB 2W',
        fixtureType: 'LASER',
        quantity: 1,
        nominalWatts: 75,
        zone: 'CENTER_BOOTH',
        dmxConnector: 'DMX_3PIN',
        unitWeightKg: 4.5,
      },
    ];

    const res = calculateLightingAndDmxRig(batches, 10, 14);
    expect(res.hasLaserUnit).toBe(true);
    expect(res.alerts.some((a) => a.includes('SEGURIDAD LÁSER'))).toBe(true);
  });

  it('provee catálogo de presets reales incluyendo PAR, Cabeza Móvil, Láser y Humo', () => {
    const types = LIGHTING_PRESETS.map((p) => p.fixtureType);
    expect(types).toContain('PAR_LED');
    expect(types).toContain('MOVING_HEAD');
    expect(types).toContain('LASER');
    expect(types).toContain('FOG_MACHINE');
  });
});
