import { describe, it, expect } from 'vitest';
import {
  calculateDistances,
  calculateGafferTape,
  routeEquipmentToOutlets,
  type Point2D,
  type ElectricalOutlet,
  type EquipmentLoad,
} from '../src/calc-engine/routing.js';

describe('STAGE PLAN v3.2 - Suite TDD de Ruteo, Distancias y Gaffer', () => {
  describe('1. Cálculo de distancia por equipo con 1 solo enchufe', () => {
    it('TC-01: debe calcular correctamente la distancia euclidiana y perimetral de un parlante a (2, 14) con enchufe en (0, 0)', () => {
      const equipmentPos: Point2D = { x: 2, y: 14 };
      const outletPos: Point2D = { x: 0, y: 0 };

      const { euclidean, perimeter } = calculateDistances(equipmentPos, outletPos);

      // Euclidiana: sqrt(2^2 + 14^2) = sqrt(200) ≈ 14.14 m
      expect(euclidean).toBeCloseTo(14.14, 2);

      // Perimetral / Tendido rectangular por pared o borde: |2 - 0| + |14 - 0| = 16 m
      expect(perimeter).toBe(16.0);
    });

    it('debe contemplar holgura de elevación y subida al trípode (+10% estándar)', () => {
      const equipmentPos: Point2D = { x: 2, y: 14 };
      const outletPos: Point2D = { x: 0, y: 0 };

      const { perimeter, suggestedCableMeters } = calculateDistances(equipmentPos, outletPos, { heightMeters: 1.5 });

      expect(perimeter).toBe(16.0);
      // (16 + 1.5) * 1.1 = 19.25 -> 20m redondeado al techo
      expect(suggestedCableMeters).toBeGreaterThanOrEqual(19);
    });
  });

  describe('2. Enrutamiento inteligente con capacidad y proximidad', () => {
    const outlets: ElectricalOutlet[] = [
      { id: 'outlet-1', name: 'Enchufe Escenario Izquierdo', position: { x: 0, y: 0 }, maxPowerWatts: 2200 },
      { id: 'outlet-2', name: 'Enchufe Escenario Derecho', position: { x: 10, y: 0 }, maxPowerWatts: 2200 },
    ];

    it('TC-02: asigna Parlante A al enchufe 1 (más cercano) y Parlante B al enchufe 2', () => {
      const equipment: EquipmentLoad[] = [
        { id: 'spk-a', name: 'Parlante Top Izquierdo', position: { x: 1, y: 1 }, powerWatts: 600 },
        { id: 'spk-b', name: 'Parlante Top Derecho', position: { x: 9, y: 1 }, powerWatts: 600 },
      ];

      const result = routeEquipmentToOutlets(equipment, outlets);

      const assignA = result.assignments.find((a) => a.equipmentId === 'spk-a');
      const assignB = result.assignments.find((a) => a.equipmentId === 'spk-b');

      expect(assignA).toBeDefined();
      expect(assignA?.outletId).toBe('outlet-1');

      expect(assignB).toBeDefined();
      expect(assignB?.outletId).toBe('outlet-2');
    });

    it('TC-03: reasigna inteligentemente al siguiente enchufe disponible cuando el más cercano excede su capacidad', () => {
      const outletsSmall: ElectricalOutlet[] = [
        { id: 'outlet-1', name: 'Toma A', position: { x: 0, y: 0 }, maxPowerWatts: 1000 },
        { id: 'outlet-2', name: 'Toma B', position: { x: 5, y: 0 }, maxPowerWatts: 2500 },
      ];

      const equipment: EquipmentLoad[] = [
        { id: 'sub-1', name: 'Subwoofer 1', position: { x: 1, y: 0 }, powerWatts: 800 },
        { id: 'sub-2', name: 'Subwoofer 2', position: { x: 1.5, y: 0 }, powerWatts: 800 },
      ];

      const result = routeEquipmentToOutlets(equipment, outletsSmall);

      const assignSub1 = result.assignments.find((a) => a.equipmentId === 'sub-1');
      const assignSub2 = result.assignments.find((a) => a.equipmentId === 'sub-2');

      expect(assignSub1?.outletId).toBe('outlet-1');
      expect(assignSub2?.outletId).toBe('outlet-2');
    });
  });

  describe('3. Sugerencia de nuevo enchufe y alertas de seguridad', () => {
    it('TC-04: debe alertar y sugerir un nuevo enchufe cuando el circuito único supera el 90% de su capacidad', () => {
      const singleOutlet: ElectricalOutlet[] = [
        { id: 'outlet-single', name: 'Enchufe Único Salón', position: { x: 0, y: 0 }, maxPowerWatts: 2000 },
      ];

      const equipment: EquipmentLoad[] = [
        { id: 'load-1', name: 'Sistema Principal', position: { x: 2, y: 2 }, powerWatts: 1900 },
      ];

      const result = routeEquipmentToOutlets(equipment, singleOutlet);

      expect(result.needsAdditionalOutlet).toBe(true);
      const capacityAlert = result.recommendations.find((r) => r.type === 'ADD_OUTLET_CAPACITY');
      expect(capacityAlert).toBeDefined();
      expect(capacityAlert?.friendlyMessage).toMatch(/enchufe o circuito adicional/i);
    });

    it('TC-05: debe sugerir un nuevo enchufe cuando la distancia de tendido supera los 25 metros', () => {
      const outlets: ElectricalOutlet[] = [
        { id: 'outlet-front', name: 'Enchufe Cabina', position: { x: 0, y: 0 }, maxPowerWatts: 3000 },
      ];

      const farEquipment: EquipmentLoad[] = [
        { id: 'delay-spk', name: 'Parlante de Refuerzo Fondo', position: { x: 6, y: 22 }, powerWatts: 400 },
      ];

      const result = routeEquipmentToOutlets(farEquipment, outlets);

      expect(result.needsAdditionalOutlet).toBe(true);
      const distanceAlert = result.recommendations.find((r) => r.type === 'ADD_OUTLET_DISTANCE');
      expect(distanceAlert).toBeDefined();
      expect(distanceAlert?.friendlyMessage).toMatch(/25 metros/i);
    });
  });

  describe('4. Cálculo de cinta industrial gris (Gaffer Tape)', () => {
    it('TC-06: calcula los metros de cinta requeridos para 40m en suelo con +20% y convierte a rollos de 50m', () => {
      // 40m * 1.20 = 48m de cinta. Cabe en 1 rollo de 50m.
      const tape = calculateGafferTape({ floorTransitMeters: 40 });

      expect(tape.transitDistanceMeters).toBe(40);
      expect(tape.requiredTapeMetersWithMargin).toBe(48);
      expect(tape.standardRolls50m).toBe(1);
      expect(tape.spareMeters).toBe(2);
    });

    it('TC-07: calcula rollos correctamente cuando el metraje supera los 50m (ej. 90m de suelo transitado)', () => {
      // 90m * 1.20 = 108m. Requiere 3 rollos de 50m (150m total). Sobran 42m.
      const tape = calculateGafferTape({ floorTransitMeters: 90 });

      expect(tape.requiredTapeMetersWithMargin).toBe(108);
      expect(tape.standardRolls50m).toBe(3);
      expect(tape.spareMeters).toBe(42);
    });

    it('retorna 0 rollos y aviso seguro si no hay cables en suelo transitado', () => {
      const tape = calculateGafferTape({ floorTransitMeters: 0 });

      expect(tape.standardRolls50m).toBe(0);
      expect(tape.requiredTapeMetersWithMargin).toBe(0);
    });
  });

  describe('5. Verificación de lenguaje accesible para usuarios no técnicos', () => {
    it('TC-09: genera mensajes claros, comprensibles y sin jerga eléctrica intimidante', () => {
      const outlets: ElectricalOutlet[] = [
        { id: 'out-1', name: 'Toma General', position: { x: 0, y: 0 }, maxPowerWatts: 2000 },
      ];
      const heavyLoads: EquipmentLoad[] = [
        { id: 'eq-1', name: 'Luces y Amplificadores', position: { x: 2, y: 26 }, powerWatts: 2100, requiresFloorTransit: true },
      ];

      const result = routeEquipmentToOutlets(heavyLoads, outlets);

      expect(result.gafferTape.friendlySummary).toMatch(/cinta gris para piso/i);
      expect(result.gafferTape.friendlySummary).not.toMatch(/amperaje inductivo|reactancia/i);

      for (const rec of result.recommendations) {
        expect(rec.friendlyMessage).toBeTruthy();
        expect(rec.friendlyMessage).not.toContain('formula SEC');
        expect(rec.friendlyMessage).not.toContain('rho del cobre');
      }
    });
  });
});

