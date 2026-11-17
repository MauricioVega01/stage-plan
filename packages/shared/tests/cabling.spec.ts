import { describe, it, expect } from 'vitest';
import {
  calculateCablingInventory,
  roundToStandardCableSize,
  EquipmentCableItem,
} from '../src/calc-engine/cabling';

describe('Cabling & Signals Engine (STAGE PLAN v3.3 - DISTORSIONCL SPA)', () => {
  it('TC-01: Redondea correctamente distancias a estándares comerciales de cables', () => {
    expect(roundToStandardCableSize(2)).toBe(3);
    expect(roundToStandardCableSize(4)).toBe(5);
    expect(roundToStandardCableSize(7)).toBe(10);
    expect(roundToStandardCableSize(12)).toBe(15);
    expect(roundToStandardCableSize(18)).toBe(20);
  });

  it('TC-02: Cubica cables de poder, señales XLR, DMX y RETORNO DJ (Booth Monitor)', () => {
    const items: EquipmentCableItem[] = [
      // 2 Parlantes activos principales (a 8m de la cabina DJ)
      {
        id: 'top-l',
        name: 'Top Izquierdo QSC K12.2',
        category: 'audio_active',
        distanceToDjBoothMeters: 8,
        powerCordType: 'iec_c13', // Típico de PC
        signalType: 'xlr',
      },
      {
        id: 'top-r',
        name: 'Top Derecho QSC K12.2',
        category: 'audio_active',
        distanceToDjBoothMeters: 8,
        powerCordType: 'iec_c13',
        signalType: 'xlr',
      },
      // RETORNO DJ (Booth Monitor) al lado de la mesa
      {
        id: 'booth-monitor',
        name: 'Retorno DJ Activo Yamaha DBR10',
        category: 'dj_booth_monitor',
        distanceToDjBoothMeters: 1.5,
        powerCordType: 'iec_c13',
        signalType: 'xlr',
      },
      // 2 Subwoofers activos (a 6m de cabina DJ)
      {
        id: 'sub-l',
        name: 'Subwoofer QSC KS118',
        category: 'audio_active',
        distanceToDjBoothMeters: 6,
        powerCordType: 'powercon',
        signalType: 'xlr',
      },
      // Cabina DJ: 2 CDJs + 1 Mixer
      {
        id: 'cdj-1',
        name: 'Pioneer CDJ-3000 (1)',
        category: 'dj_gear',
        distanceToDjBoothMeters: 0,
        powerCordType: 'iec_c13',
        signalType: 'ethernet', // Cable link
      },
      {
        id: 'cdj-2',
        name: 'Pioneer CDJ-3000 (2)',
        category: 'dj_gear',
        distanceToDjBoothMeters: 0,
        powerCordType: 'iec_c13',
        signalType: 'ethernet', // Cable link
      },
      {
        id: 'mixer-dj',
        name: 'Pioneer DJM-900NXS2',
        category: 'dj_gear',
        distanceToDjBoothMeters: 0,
        powerCordType: 'iec_c13',
        signalType: 'rca', // Conexión local RCA
      },
      // Luces: 2 Focos LED par en cadena DMX
      {
        id: 'par-1',
        name: 'Foco Par LED 1',
        category: 'lighting',
        distanceToDjBoothMeters: 5,
        powerCordType: 'iec_c13',
        signalType: 'dmx',
        linkDistanceMeters: 3,
      },
      {
        id: 'par-2',
        name: 'Foco Par LED 2',
        category: 'lighting',
        distanceToDjBoothMeters: 7,
        powerCordType: 'iec_c13',
        signalType: 'dmx',
        linkDistanceMeters: 3,
      },
    ];

    const result = calculateCablingInventory(items);

    // Retorno DJ verificado
    expect(result.djBoothMonitorCount).toBe(1);
    expect(result.djBoothXlrCablesCount).toBe(1);

    // Verificación de cables de poder tipo PC (IEC C13)
    // 2 Tops + 1 Retorno + 2 CDJs + 1 Mixer + 2 Luces = 8 cables
    expect(result.powerCordsIecPc).toBe(8);
    expect(result.powerCordsPowercon).toBe(1);

    // Verificación de cables de audio XLR: 2 tops + 1 sub + 1 retorno = 4 cables
    expect(result.totalXlrCount).toBe(4);

    // Verificación de cables DJ (RCA y Ethernet Link)
    expect(result.audioRcaCablesCount).toBe(1);
    expect(result.ethernetLinkCablesCount).toBe(2);

    // Verificación de cables DMX para iluminación
    expect(result.dmxCablesCount).toBe(2);
    expect(result.totalDmxMeters).toBe(6);

    // Verificación de recomendaciones en lenguaje claro
    expect(result.recommendations.some(r => r.includes('Retorno DJ (Booth Monitor)'))).toBe(true);
    expect(result.recommendations.some(r => r.includes('BOOTH OUT'))).toBe(true);
  });
});
