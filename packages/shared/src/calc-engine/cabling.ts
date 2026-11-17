// ======================================================================
// CALC-ENGINE: CABLING & SIGNALS MODULE (STAGE PLAN v3.3)
// Cubicación completa de cables de poder, señal de audio, red, retorno DJ e iluminación DMX
// Diseñado para DISTORSIONCL SPA con lenguaje claro y ejemplos cotidianos
// ======================================================================

export interface EquipmentCableItem {
  id: string;
  name: string;
  category: 'audio_active' | 'audio_passive' | 'dj_gear' | 'dj_booth_monitor' | 'lighting' | 'effect' | 'other';
  // Posición en metros respecto a cabina DJ (o nodo central de control)
  distanceToDjBoothMeters: number;
  // Tipo de alimentación eléctrica
  powerCordType: 'iec_c13' | 'powercon' | 'schuko_direct' | 'none'; // 'iec_c13' es el típico de PC
  // Tipo de señal requerida
  signalType: 'xlr' | 'rca' | 'ethernet' | 'dmx' | 'speakon' | 'none';
  // Si requiere daisy chain / linkeo con el siguiente (ej. DMX o link de audio/red)
  linkWithNext?: boolean;
  linkDistanceMeters?: number;
}

export interface CableInventorySummary {
  // Cables de Poder (Alimentación individual por equipo)
  powerCordsIecPc: number;          // Típicos de PC (IEC C13 a Schuko) para consolas, monitores, luces básicas
  powerCordsPowercon: number;       // PowerCON azules/grises para cajas profesionales y cabezas móviles
  powerCordsDirect: number;         // Enchufes directos / transformadores de 220V

  // Retorno de Cabina (Monitoreo DJ / Booth Monitor)
  djBoothMonitorCount: number;      // Parlante(s) de retorno al lado del DJ para mezcla en vivo
  djBoothXlrCablesCount: number;    // Cables XLR cortos (3m a 5m) dedicados a salida BOOTH OUT del mixer

  // Cables de Señal de Audio Principal (PA / Cajas de público)
  audioXlrCables: {
    lengthMeters: number;
    count: number;
    description: string;
  }[];
  totalXlrMeters: number;
  totalXlrCount: number;

  audioRcaCablesCount: number;      // Pares RCA / Jack 6.3 para tornamesas, reproductores y mixer DJ
  ethernetLinkCablesCount: number;  // Cables RJ45 de red para linkear CDJs (Pioneer Pro DJ Link)

  // Cables de Iluminación y Control DMX
  dmxCablesCount: number;           // Cables DMX (XLR de 3 pines / 120 ohm) para linkear luces en cadena
  totalDmxMeters: number;

  // Cables de Carga / Parlantes Pasivos
  speakonCablesCount: number;       // Cables Speakon NL4 para conexión amplificador a caja pasiva

  // Alertas y Consejos Prácticos en Lenguaje Claro
  recommendations: string[];
}

/**
 * Normaliza las tiradas de cable a medidas estándar de arriendo / bodega:
 * 3m, 5m, 10m, 15m, 20m
 */
export function roundToStandardCableSize(meters: number): number {
  if (meters <= 3) return 3;
  if (meters <= 5) return 5;
  if (meters <= 10) return 10;
  if (meters <= 15) return 15;
  return Math.ceil(meters / 5) * 5;
}

/**
 * Calcula la lista completa de cables de poder y señal requeridos para el rider técnico,
 * incluyendo monitores de retorno para la cabina DJ.
 */
export function calculateCablingInventory(items: EquipmentCableItem[]): CableInventorySummary {
  let powerCordsIecPc = 0;
  let powerCordsPowercon = 0;
  let powerCordsDirect = 0;

  let djBoothMonitorCount = 0;
  let djBoothXlrCablesCount = 0;

  let totalXlrMeters = 0;
  let totalXlrCount = 0;
  const xlrMap: Record<number, number> = {};

  let audioRcaCablesCount = 0;
  let ethernetLinkCablesCount = 0;
  let dmxCablesCount = 0;
  let totalDmxMeters = 0;
  let speakonCablesCount = 0;

  for (const item of items) {
    // 1. Cables de poder individuales (del equipo a la zapatilla o enchufe)
    if (item.powerCordType === 'iec_c13') {
      powerCordsIecPc++;
    } else if (item.powerCordType === 'powercon') {
      powerCordsPowercon++;
    } else if (item.powerCordType === 'schuko_direct') {
      powerCordsDirect++;
    }

    // 2. Detección especial de Parlante de Retorno DJ (Booth Monitor)
    if (item.category === 'dj_booth_monitor') {
      djBoothMonitorCount++;
      djBoothXlrCablesCount++;
      // El retorno está al lado de la cabina: requiere cable corto estándar de 3m o 5m
      const boothLength = item.distanceToDjBoothMeters <= 2 ? 3 : 5;
      totalXlrCount++;
      totalXlrMeters += boothLength;
      xlrMap[boothLength] = (xlrMap[boothLength] || 0) + 1;
      continue;
    }

    // 3. Cables de señal generales
    if (item.signalType === 'xlr') {
      totalXlrCount++;
      // Distancia con holgura del 20% para esquinas y atril
      const realMeters = Math.max(3, item.distanceToDjBoothMeters * 1.2);
      const standardLength = roundToStandardCableSize(realMeters);
      totalXlrMeters += standardLength;
      xlrMap[standardLength] = (xlrMap[standardLength] || 0) + 1;
    } else if (item.signalType === 'rca') {
      audioRcaCablesCount++;
    } else if (item.signalType === 'ethernet') {
      ethernetLinkCablesCount++;
    } else if (item.signalType === 'dmx') {
      dmxCablesCount++;
      const dist = item.linkDistanceMeters ? Math.max(2, item.linkDistanceMeters) : 3;
      totalDmxMeters += roundToStandardCableSize(dist);
    } else if (item.signalType === 'speakon') {
      speakonCablesCount++;
    }
  }

  const audioXlrCables = Object.entries(xlrMap).map(([lengthStr, count]) => ({
    lengthMeters: Number(lengthStr),
    count,
    description: `Cable de audio balanceado XLR (Canon) de ${lengthStr} metros`,
  }));

  const recommendations: string[] = [];

  if (djBoothMonitorCount > 0) {
    recommendations.push(
      `Retorno DJ (Booth Monitor): Se configuró ${djBoothMonitorCount} caja(s) de retorno al lado del DJ con cable XLR de 3m/5m desde la salida 'BOOTH OUT' del mixer para que el DJ escuche sin eco ni retardo de la pista.`
    );
  }

  if (powerCordsIecPc > 0) {
    recommendations.push(
      `Llevar al menos ${powerCordsIecPc + 2} cables de poder tipo PC (IEC C13) incluyendo 2 de repuesto por seguridad.`
    );
  }

  if (ethernetLinkCablesCount > 0) {
    recommendations.push(
      `Se requieren ${ethernetLinkCablesCount} cables de red Ethernet (RJ45) para linkear las reproductoras CDJ / mixer y compartir música desde un solo pendrive.`
    );
  }

  if (dmxCablesCount > 0) {
    recommendations.push(
      `Para las luces se necesitan ${dmxCablesCount} cables DMX en cadena (total ${totalDmxMeters}m). Importante: no usar cables de micrófono comunes para tramos largos de DMX para evitar parpadeos en los focos.`
    );
  }

  recommendations.push(
    'Separación de cables: Procurar no pasar los cables de señal de audio (XLR/RCA) pegados en paralelo a los alargadores de 220V para evitar zumbidos de fondo ("hum" o tierra).'
  );

  return {
    powerCordsIecPc,
    powerCordsPowercon,
    powerCordsDirect,
    djBoothMonitorCount,
    djBoothXlrCablesCount,
    audioXlrCables,
    totalXlrMeters,
    totalXlrCount,
    audioRcaCablesCount,
    ethernetLinkCablesCount,
    dmxCablesCount,
    totalDmxMeters,
    speakonCablesCount,
    recommendations,
  };
}
