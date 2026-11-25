import { describe, it, expect } from 'vitest';
import { calculateCablingInventory, EquipmentCableItem } from '../src/calc-engine/cabling.js';
import {
  evaluateTopToSubBalance,
  evaluateNeighborhoodNoise,
} from '../src/calc-engine/stage-acoustic-engine.js';
import { analyzeDjSetupAndAudioRouting } from '../src/calc-engine/dj-setup-audio.js';
import { calculateLoadLogistics } from '../src/calc-engine/contingency-and-logistics.js';
import type { SpeakerBatchInput } from '../src/calc-engine/hybrid-roster.js';

describe('QA Branch Coverage Hardening (Branch Coverage > 90%)', () => {
  describe('Cabling Edge Cases & Minor Signal Types', () => {
    it('cubre tipos de cables schuko, speakon, rca, ethernet, dmx y retorno dj lejano', () => {
      const items: EquipmentCableItem[] = [
        {
          id: 'item-1',
          name: 'Power Directo Schuko',
          category: 'audio_active',
          distanceToDjBoothMeters: 5,
          powerCordType: 'schuko_direct',
          signalType: 'speakon',
        },
        {
          id: 'item-2',
          name: 'Reproductor RCA',
          category: 'lighting_fixture',
          distanceToDjBoothMeters: 2,
          powerCordType: 'powercon',
          signalType: 'rca',
        },
        {
          id: 'item-3',
          name: 'Enlace Ethernet',
          category: 'audio_active',
          distanceToDjBoothMeters: 3,
          powerCordType: 'iec_c13',
          signalType: 'ethernet',
        },
        {
          id: 'item-4',
          name: 'Luminaria DMX',
          category: 'lighting_fixture',
          distanceToDjBoothMeters: 4,
          linkDistanceMeters: 6,
          powerCordType: 'powercon',
          signalType: 'dmx',
        },
        {
          id: 'item-5',
          name: 'Monitor DJ Distante (> 2m)',
          category: 'dj_booth_monitor',
          distanceToDjBoothMeters: 4,
          powerCordType: 'iec_c13',
          signalType: 'xlr',
        },
      ];

      const res = calculateCablingInventory(items, 15);
      expect(res.powerCordsDirect).toBe(1);
      expect(res.speakonCablesCount).toBe(1);
      expect(res.audioRcaCablesCount).toBe(1);
      expect(res.ethernetLinkCablesCount).toBe(1);
      expect(res.dmxCablesCount).toBe(1);
      expect(res.djBoothMonitorCount).toBe(1);
    });
  });

  describe('Stage Acoustic Engine Balance & Neighborhood Noise Branches', () => {
    it('evalúa correctamente ramas de equilibrio TOP/SUB: NO_SUB, SUB_BASS_DEFICIT, BOTTLENECK y OPTIMAL', () => {
      // 1. Sin subwoofers
      const noSub = evaluateTopToSubBalance({
        totalTopRmsWatts: 1000,
        totalSubRmsWatts: 0,
        topsCount: 2,
        subsCount: 0,
      });
      expect(noSub.status).toBe('NO_SUBWOOFERS');
      expect(noSub.topTrimAdjustmentDb).toBe(-3);

      // 2. Sub déficit (< 45% energía)
      const subDeficit = evaluateTopToSubBalance({
        totalTopRmsWatts: 2000,
        totalSubRmsWatts: 500,
        topsCount: 2,
        subsCount: 1,
      });
      expect(subDeficit.status).toBe('SUB_BASS_DEFICIT');
      expect(subDeficit.topTrimAdjustmentDb).toBeLessThan(0);

      // 3. Top Headroom Bottleneck (> 75% sub energía y <= 2 tops)
      const bottleneck = evaluateTopToSubBalance({
        totalTopRmsWatts: 500,
        totalSubRmsWatts: 3000,
        topsCount: 2,
        subsCount: 4,
      });
      expect(bottleneck.status).toBe('TOP_HEADROOM_BOTTLENECK');

      // 4. Equilibrio Óptimo
      const optimal = evaluateTopToSubBalance({
        totalTopRmsWatts: 1000,
        totalSubRmsWatts: 1500,
        topsCount: 2,
        subsCount: 2,
      });
      expect(optimal.status).toBe('OPTIMAL_CLUB_BALANCE');
    });

    it('evalúa ramas de ruido vecinal: COMPLIANT_SAFE, BORDERLINE_CAUTION y HIGH_RISK en varios recintos', () => {
      // 1. Seguro y conforme (muro hormigón a 50m)
      const safe = evaluateNeighborhoodNoise({
        spl1mContinuousDba: 100,
        neighborDistanceM: 50,
        enclosureType: 'BRICK_CONCRETE_CLOSED',
        scheduleShift: 'DAYTIME_07_21',
      });
      expect(safe.status).toBe('COMPLIANT_SAFE');

      // 2. Precaución vecinal (Borderline: 105 dB a 50m en galpón metálico noche -> ~51.6 dBA vs 48 legal = +3.6 dB)
      const borderline = evaluateNeighborhoodNoise({
        spl1mContinuousDba: 105,
        neighborDistanceM: 50,
        enclosureType: 'METAL_WAREHOUSE',
        scheduleShift: 'NIGHT_21_07',
      });
      expect(borderline.status).toBe('BORDERLINE_CAUTION');

      // 3. Alto riesgo / Infracción (> 7 dB exceso al aire libre nocturno a 10m)
      const breach = evaluateNeighborhoodNoise({
        spl1mContinuousDba: 115,
        neighborDistanceM: 10,
        enclosureType: 'OPEN_AIR',
        scheduleShift: 'NIGHT_21_07',
      });
      expect(breach.status).toBe('HIGH_RISK_MUNICIPAL_FINE');
    });
  });

  describe('DJ Setup & Audio Routing Edge Cases', () => {
    it('detecta impedancia crítica en power de subs pasivos y monitores de cabina', () => {
      const dangerSubs: SpeakerBatchInput[] = [
        {
          id: 'sub-extreme-danger',
          category: 'sub_bass',
          systemType: 'PASSIVE',
          quantity: 4,
          modelLabel: 'Sub 4 Ohm Paralelo',
          coneSizeInches: 18,
          rmsWatts: 1000,
          peakWatts: 2000,
          impedanceOhms: 4,
          powerAmpModel: 'Powersoft K20 Custom',
        },
      ];

      const result = analyzeDjSetupAndAudioRouting({
        setupMode: 'ALL_IN_ONE_STANDALONE',
        playerCount: 2,
        playerAudioLinkType: 'RCA_ANALOG',
        linkEthernetProDj: false,
        linkMixerToEthernet: false,
        boothMonitorsCount: 2,
        boothMonitorType: 'ACTIVE',
        boothMonitorRmsWatts: 300,
        passiveWiringMode: 'PARALLEL_SPEAKON_LINK',
        speakerBatches: dangerSubs,
      });

      expect(result.alerts.length).toBeGreaterThan(0);
      expect(result.powerAmpsRequired.some((amp) => amp.isImpedanceDanger)).toBe(true);
      expect(result.recommendations.length).toBeGreaterThan(0);
    });
  });

  describe('Contingency and Logistics Vehicles and Ley del Saco', () => {
    it('recomienda vehículo y activa alerta ley del saco para bultos pesados', () => {
      const logisticsResult = calculateLoadLogistics({
        items: [
          { name: 'Top QSC K12.2', quantity: 4, unitWeightKg: 17.7 },
          { name: 'Sub QSC KS118', quantity: 2, unitWeightKg: 47 }, // > 25 kg
        ],
        extensionCordsCount: 4,
        powerStripsCount: 4,
        dmxCablesCount: 6,
        gafferRolls50m: 2,
      });

      expect(logisticsResult.grandTotalWeightKg).toBeGreaterThan(100);
      expect(logisticsResult.heavyItemsRequiringTwoPeople.length).toBeGreaterThan(0);
      expect(logisticsResult.leyDelSacoAlert).not.toBeNull();
    });
  });
});
