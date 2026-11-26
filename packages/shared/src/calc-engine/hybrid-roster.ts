// ======================================================================
// CALC-ENGINE: HARDWARE ROUTING, SMART PLACEMENT & CABLE ROSTER MODULE
// STAGE PLAN v3.7 - DISTORSIONCL SPA
// Distribución acústica inteligente por zonas (PA Frontal + Delay Lines + Mono Cluster de Subs)
// para evitar saturación ("chicharreo") y proteger los equipos trabajando con headroom limpio.
// ======================================================================

export type AudioBoxType = 'ACTIVE' | 'PASSIVE';

export type PlacementZone = 'PA_FRONT_L' | 'PA_FRONT_R' | 'SUB_CENTER_CLUSTER' | 'DELAY_RING_1' | 'DELAY_RING_2' | 'DJ_BOOTH';

export interface SpeakerBatchInput {
  id: string;
  category: 'top_box' | 'sub_bass';
  systemType: AudioBoxType;
  quantity: number;
  modelLabel: string;
  coneSizeInches: 10 | 12 | 15 | 18 | 21;
  rmsWatts: number;
  peakWatts: number;
  impedanceOhms?: 4 | 8 | 16;
  powerAmpModel?: string;
  powerAmpWatts?: number;
  powerAmpLocation?: 'DJ_BOOTH' | 'STAGE_RACK';
}

export interface PassiveImpedanceAnalysis {
  hasPassiveUnits: boolean;
  wiringMode: 'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK';
  passiveTopsCount: number;
  passiveSubsCount: number;
  topsEffectiveOhms: number | null;
  subsEffectiveOhms: number | null;
  minImpedanceOhms: number | null;
  status: 'NO_PASSIVE' | 'OPTIMAL_8_OHM' | 'HIGH_LOAD_4_OHM' | 'DANGER_PROTECT_SHORT';
  technicalDirective: string;
  speakonRoutingNote: string;
}

export interface RigEquipmentItem {
  id: string;
  tag: string; // Ej: "A", "B", "C", "D" para Cajas o "S1", "S2" para Sub Bajos
  name: string;
  category: 'top_box' | 'sub_bass' | 'dj_booth' | 'lighting' | 'other';
  systemType: AudioBoxType;
  rmsWatts: number;
  peakWatts?: number;
  coneSizeInches?: number;
  impedanceOhms?: number;
  // Posición 2D en metros en el recinto
  posX: number;
  posY: number;
  // Zona acústica asignada y retardo individual
  zone?: PlacementZone;
  zoneLabel?: string;
  delayMs?: number;
  recommendedGainNote?: string;
  gainMatchingDb?: number;
}

export interface OutletPoint {
  id: string;
  name: string;
  maxAmps: number;
  maxWatts: number;
  posX: number;
  posY: number;
}

export interface EquipmentRosterConnection {
  id: string;
  tag: string;
  name: string;
  category: 'top_box' | 'sub_bass' | 'dj_booth' | 'lighting' | 'other';
  systemType: AudioBoxType;
  rmsWatts: number;
  peakWatts: number;
  coneSizeInches: number;
  impedanceOhms: number;
  powerWatts220v: number;
  peakWatts220v: number;
  drawAmps: number;
  assignedOutletName: string;
  powerLineAssignment: 'LINE_1_SUBS' | 'LINE_2_TOPS_CTRL';
  powerCableMeters: number;
  powerCableType: 'IEC_PC' | 'POWERCON' | 'NONE_PASSIVE';
  signalCableType: 'XLR_AUDIO' | 'SPEAKON_PASIVO' | 'DMX_LIGHT' | 'RCA_DJ' | 'ETHERNET_LINK' | 'NONE';
  signalLengthMeters: number;
  signalOrigin: string;
  colorHex: string;
  badgeBg: string;
  // Datos de Ubicación Acústica Inteligente
  posX: number;
  posY: number;
  zone: PlacementZone;
  zoneLabel: string;
  delayMs: number;
  recommendedGainNote: string;
  gainMatchingDb: number;
}

export interface HybridRigAnalysis {
  roster: EquipmentRosterConnection[];
  totalPowerWatts220v: number;
  totalPeakWatts220v: number;
  totalRmsAudioWatts: number;
  totalPeakAudioWatts: number;
  totalAmps220v: number;
  activeTopsCount: number;
  passiveTopsCount: number;
  activeSubsCount: number;
  passiveSubsCount: number;
  frontTopsCount: number;
  delayTopsCount: number;
  externalAmpsRequiredCount: number;
  powerCordsIecCount: number;
  powerCordsPowerconCount: number;
  speakonCablesCount: number;
  xlrCablesCount: number;
  totalFloorTapeMeters: number;
  floorTapeRolls50m: number;
  placementStrategySummary: string;
  recommendations: string[];
  electricalLines: {
    line1SubsWatts: number;
    line1SubsPeakWatts: number;
    line1SubsAmps: number;
    line2TopsCtrlWatts: number;
    line2TopsCtrlPeakWatts: number;
    line2TopsCtrlAmps: number;
    phaseBalanceDirective: string;
  };
}

export function roundToStandardLength(meters: number): number {
  if (meters <= 3) return 3;
  if (meters <= 5) return 5;
  if (meters <= 10) return 10;
  if (meters <= 15) return 15;
  return Math.ceil(meters / 5) * 5;
}

/**
 * MOTOR DE UBICACIÓN ACÚSTICA INTELIGENTE (ANTI-SATURACIÓN / ANTI-CHICHARREO)
 * En lugar de amontonar todas las cajas al frente, distribuye las cajas según el largo de la pista
 * y la caída de presión sonora SPL:
 * - Cajas A y B: Frente Principal Izquierdo y Derecho (0m a 10m), elevadas a 2.2m en trípode, Ganancia a 0 dB (12:00).
 * - Si hay >= 4 cajas o el salón mide >= 14m de fondo: Cajas C y D pasan automáticamente a ser Torres de Refuerzo (Delay)
 *   en los costados de la pista (al 50-55% del fondo) con retardo Haas calibrado.
 * - Si hay >= 6 cajas: Cajas E y F forman un segundo anillo de Delay (al 75% del fondo) o doble frente abierto.
 * - Sub Bajos (S1, S2...): Agrupados juntos al centro del escenario en el suelo (Mono Cluster Central) para ganar +6 dB
 *   de acoplamiento mutuo coherente y eliminar cancelaciones ("pasillo de la muerte").
 */
export function generateSmartAcousticPlacement(params: {
  venueWidthM: number;
  venueDepthM: number;
  topsCount: number;
  topsSystemType: AudioBoxType;
  topsRmsWatts: number;
  subsCount: number;
  subsSystemType: AudioBoxType;
  subsRmsWatts: number;
  temperatureCelsius?: number;
}): RigEquipmentItem[] {
  const {
    venueWidthM,
    venueDepthM,
    topsCount,
    topsSystemType,
    topsRmsWatts,
    subsCount,
    subsSystemType,
    subsRmsWatts,
    temperatureCelsius = 20,
  } = params;

  const items: RigEquipmentItem[] = [];
  const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];
  const soundSpeed = 331.3 + 0.606 * temperatureCelsius; // ~343.4 m/s a 20°C

  // 1. Distribución Inteligente de Cajas Acústicas (Tops)
  for (let i = 0; i < topsCount; i++) {
    const tag = LETTERS[i] || `T${i + 1}`;
    const isLeft = i % 2 === 0;
    const pairIndex = Math.floor(i / 2); // 0 = Par frontal (A,B), 1 = 1er Par Delay (C,D), 2 = 2do Par Delay (E,F)

    let posX = isLeft ? 1.2 : Math.max(2, venueWidthM - 1.2);
    let posY = 2.0;
    let zone: PlacementZone = isLeft ? 'PA_FRONT_L' : 'PA_FRONT_R';
    let zoneLabel = isLeft ? 'Frente Izquierdo (PA Principal)' : 'Frente Derecho (PA Principal)';
    let delayMs = 0;
    let recommendedGainNote = 'Potenciómetro a las 12:00 (0 dB Unity) — Sin forzar amplificador';

    if (pairIndex === 0) {
      // Par A y B: Siempre en el Frente Principal (Escenario) a los extremos L y R
      posX = isLeft ? Math.max(1.0, venueWidthM * 0.12) : Math.min(venueWidthM - 1.0, venueWidthM * 0.88);
      posY = 2.0;
    } else if (pairIndex === 1) {
      // Par C y D: Primera Línea de Retardo (Delay Ring 1) a mitad de pista (~52% del largo)
      const delayDistFromFront = Number((venueDepthM * 0.52).toFixed(1));
      posY = Math.max(6.0, delayDistFromFront);
      posX = isLeft ? Math.max(0.8, venueWidthM * 0.08) : Math.min(venueWidthM - 0.8, venueWidthM * 0.92);
      zone = 'DELAY_RING_1';
      // Distancia acústica desde el PA frontal (ubicado en y=2.0)
      const acousticDist = Math.max(4, posY - 2.0);
      const flightMs = (acousticDist / soundSpeed) * 1000;
      delayMs = Number((flightMs + 3.0).toFixed(1)); // +3.0 ms Efecto Haas
      zoneLabel = `Torre Delay 1 (${ isLeft ? 'Izquierda' : 'Derecha' } a ${posY}m del fondo)`;
      recommendedGainNote = `Retardo DSP: ${delayMs} ms (incluye +3ms Haas) | Potenciómetro a las 11:00-12:00 (Relleno suave sin saturar)`;
    } else {
      // Par E, F, G, H: Segunda Línea de Retardo (Delay Ring 2) al 75-80% del largo para recintos largos
      const ringFactor = pairIndex === 2 ? 0.76 : 0.88;
      const delayDistFromFront = Number((venueDepthM * ringFactor).toFixed(1));
      posY = Math.max(10.0, delayDistFromFront);
      posX = isLeft ? Math.max(0.8, venueWidthM * 0.08) : Math.min(venueWidthM - 0.8, venueWidthM * 0.92);
      zone = 'DELAY_RING_2';
      const acousticDist = Math.max(8, posY - 2.0);
      const flightMs = (acousticDist / soundSpeed) * 1000;
      delayMs = Number((flightMs + 3.0).toFixed(1));
      zoneLabel = `Torre Delay 2 (${ isLeft ? 'Izquierda' : 'Derecha' } a ${posY}m)`;
      recommendedGainNote = `Retardo DSP: ${delayMs} ms (incluye +3ms Haas) | Potenciómetro a las 11:00 (Relleno posterior limpio)`;
    }

    items.push({
      id: `top-${i + 1}`,
      tag,
      name: `Caja Acústica ${tag}`,
      category: 'top_box',
      systemType: topsSystemType,
      rmsWatts: topsRmsWatts,
      posX: Number(posX.toFixed(1)),
      posY: Number(posY.toFixed(1)),
      zone,
      zoneLabel,
      delayMs,
      recommendedGainNote,
      peakWatts: topsRmsWatts * 2,
      coneSizeInches: 15,
      impedanceOhms: 8,
      gainMatchingDb: 0,
    });
  }

  // 2. Distribución Inteligente de Sub Bajos: MONO CLUSTER CENTRAL ACOPLADO A PISO
  // Jamás separados en L y R para evitar el "pasillo de la muerte" (cancelación de fase)
  // y ganar +6 dB por acoplamiento mutuo coherente.
  const centerX = venueWidthM / 2;
  const subSpacing = 0.85; // Menor a 1.7m (lambda/2 a 100Hz) para acoplamiento coherente perfecto
  const startSubX = centerX - ((subsCount - 1) * subSpacing) / 2;

  for (let i = 0; i < subsCount; i++) {
    const subX = Number((startSubX + i * subSpacing).toFixed(2));
    items.push({
      id: `sub-${i + 1}`,
      tag: `S${i + 1}`,
      name: `Sub Bajo S${i + 1} (Cluster Central)`,
      category: 'sub_bass',
      systemType: subsSystemType,
      rmsWatts: subsRmsWatts,
      peakWatts: subsRmsWatts * 2,
      coneSizeInches: 18,
      impedanceOhms: 8,
      posX: subX,
      posY: 1.6, // Al centro frente a la cabina DJ en el suelo
      zone: 'SUB_CENTER_CLUSTER',
      zoneLabel: 'Bloque Central en Piso (Mono Cluster Acoplado)',
      delayMs: 0,
      recommendedGainNote: 'Acoplamiento coherente (+6 dB gratis) — Corte LPF 80-90 Hz sin forzar bobina',
      gainMatchingDb: 0,
    });
  }

  return items;
}

/**
 * CONSTRUCTOR HÍBRIDO MULTILOTE (CAJAS Y SUBS MIXTOS ACTIVOS + PASIVOS CON RMS Y PEAK)
 * Ordena inteligentemente las unidades de mayor a menor potencia RMS para colocar el par más potente
 * en el PA Frontal (A y B) y destinar las cajas adicionales o impares (ej. 2 Activas + 1 Pasiva)
 * como Torres de Refuerzo Delay (C, D...) con compensación de ganancia (Gain Matching) y retardo Haas.
 */
export function generateSmartPlacementFromBatches(params: {
  venueWidthM: number;
  venueDepthM: number;
  batches: SpeakerBatchInput[];
  temperatureCelsius?: number;
}): RigEquipmentItem[] {
  const { venueWidthM, venueDepthM, batches, temperatureCelsius = 20 } = params;
  const soundSpeed = 331.3 + 0.606 * temperatureCelsius;
  const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L'];
  const items: RigEquipmentItem[] = [];

  // 1. Expandir y ordenar Cajas Acústicas (Tops) de mayor a menor potencia RMS
  const expandedTops: Array<{
    systemType: AudioBoxType;
    modelLabel: string;
    coneSizeInches: number;
    rmsWatts: number;
    peakWatts: number;
    impedanceOhms: number;
  }> = [];

  const expandedSubs: Array<{
    systemType: AudioBoxType;
    modelLabel: string;
    coneSizeInches: number;
    rmsWatts: number;
    peakWatts: number;
    impedanceOhms: number;
  }> = [];

  for (const batch of batches) {
    const qty = Math.max(0, Math.floor(batch.quantity || 0));
    const rms = Math.max(50, Number(batch.rmsWatts) || 400);
    const peak = Math.max(rms, Number(batch.peakWatts) || rms * 2);
    const ohms = batch.impedanceOhms || 8;
    const cone = batch.coneSizeInches || (batch.category === 'sub_bass' ? 18 : 15);

    for (let q = 0; q < qty; q++) {
      if (batch.category === 'top_box') {
        expandedTops.push({
          systemType: batch.systemType,
          modelLabel: batch.modelLabel || (batch.systemType === 'ACTIVE' ? `Caja Activa ${cone}"` : `Caja Pasiva ${cone}"`),
          coneSizeInches: cone,
          rmsWatts: rms,
          peakWatts: peak,
          impedanceOhms: ohms,
        });
      } else {
        expandedSubs.push({
          systemType: batch.systemType,
          modelLabel: batch.modelLabel || (batch.systemType === 'ACTIVE' ? `Sub Activo ${cone}"` : `Sub Pasivo ${cone}"`),
          coneSizeInches: cone,
          rmsWatts: rms,
          peakWatts: peak,
          impedanceOhms: ohms,
        });
      }
    }
  }

  // Ordenar Tops: mayor RMS primero; en empate, Activas primero para garantizar par frontal simétrico
  expandedTops.sort((a, b) => {
    if (b.rmsWatts !== a.rmsWatts) return b.rmsWatts - a.rmsWatts;
    if (a.systemType !== b.systemType) return a.systemType === 'ACTIVE' ? -1 : 1;
    return 0;
  });

  const maxTopRms = expandedTops.length > 0 ? Math.max(...expandedTops.map(t => t.rmsWatts)) : 500;

  for (let i = 0; i < expandedTops.length; i++) {
    const unit = expandedTops[i];
    const tag = LETTERS[i] || `T${i + 1}`;
    const isLeft = i % 2 === 0;
    const pairIndex = Math.floor(i / 2);

    let posX = isLeft ? 1.2 : Math.max(2, venueWidthM - 1.2);
    let posY = 2.0;
    let zone: PlacementZone = isLeft ? 'PA_FRONT_L' : 'PA_FRONT_R';
    let zoneLabel = isLeft ? 'Frente Izquierdo (PA Principal)' : 'Frente Derecho (PA Principal)';
    let delayMs = 0;

    // Diferencia de sensibilidad/potencia respecto a la caja más grande
    const gainDiffDb = Number((10 * Math.log10(unit.rmsWatts / maxTopRms)).toFixed(1));
    const gainMatchText =
      gainDiffDb < -0.4
        ? ` | Nivelar a ${gainDiffDb} dB para igualar techo térmico con frente (${maxTopRms}W RMS)`
        : '';

    let recommendedGainNote = `Potenciómetro a las 12:00 (0 dB Unity) — ${unit.rmsWatts}W RMS / ${unit.peakWatts}W Peak${gainMatchText}`;

    if (pairIndex === 0) {
      posX = isLeft ? Math.max(1.0, venueWidthM * 0.12) : Math.min(venueWidthM - 1.0, venueWidthM * 0.88);
      posY = 2.0;
    } else if (pairIndex === 1) {
      const delayDistFromFront = Number((venueDepthM * 0.52).toFixed(1));
      posY = Math.max(6.0, delayDistFromFront);
      // Si es una 3ra caja impar (ej. 2 Activas + 1 Pasiva), se ubica en el costado izquierdo como Side-Fill / Delay de pista
      const isSingleOddBox = expandedTops.length === 3 && i === 2;
      posX = isLeft ? Math.max(0.8, venueWidthM * 0.08) : Math.min(venueWidthM - 0.8, venueWidthM * 0.92);
      zone = 'DELAY_RING_1';
      const acousticDist = Math.max(4, posY - 2.0);
      const flightMs = (acousticDist / soundSpeed) * 1000;
      delayMs = Number((flightMs + 3.0).toFixed(1));
      zoneLabel = isSingleOddBox
        ? `Refuerzo Lateral / Side-Fill de Pista (a ${posY}m del escenario)`
        : `Torre Delay 1 (${isLeft ? 'Izquierda' : 'Derecha'} a ${posY}m del fondo)`;
      recommendedGainNote = `Retardo DSP: ${delayMs} ms (incluye +3ms Haas) | ${unit.rmsWatts}W RMS / ${unit.peakWatts}W Peak${gainMatchText}`;
    } else {
      const ringFactor = pairIndex === 2 ? 0.76 : 0.88;
      const delayDistFromFront = Number((venueDepthM * ringFactor).toFixed(1));
      posY = Math.max(10.0, delayDistFromFront);
      posX = isLeft ? Math.max(0.8, venueWidthM * 0.08) : Math.min(venueWidthM - 0.8, venueWidthM * 0.92);
      zone = 'DELAY_RING_2';
      const acousticDist = Math.max(8, posY - 2.0);
      const flightMs = (acousticDist / soundSpeed) * 1000;
      delayMs = Number((flightMs + 3.0).toFixed(1));
      zoneLabel = `Torre Delay 2 (${isLeft ? 'Izquierda' : 'Derecha'} a ${posY}m)`;
      recommendedGainNote = `Retardo DSP: ${delayMs} ms (incluye +3ms Haas) | ${unit.rmsWatts}W RMS / ${unit.peakWatts}W Peak${gainMatchText}`;
    }

    items.push({
      id: `top-${i + 1}`,
      tag,
      name: `${unit.modelLabel} (${tag})`,
      category: 'top_box',
      systemType: unit.systemType,
      rmsWatts: unit.rmsWatts,
      peakWatts: unit.peakWatts,
      coneSizeInches: unit.coneSizeInches,
      impedanceOhms: unit.impedanceOhms,
      posX: Number(posX.toFixed(1)),
      posY: Number(posY.toFixed(1)),
      zone,
      zoneLabel,
      delayMs,
      recommendedGainNote,
      gainMatchingDb: gainDiffDb,
    });
  }

  // 2. Expandir y ordenar Sub-Bajos en el MONO CLUSTER CENTRAL EN PISO (Cero tubos extensores)
  expandedSubs.sort((a, b) => b.rmsWatts - a.rmsWatts);
  const maxSubRms = expandedSubs.length > 0 ? Math.max(...expandedSubs.map(s => s.rmsWatts)) : 800;

  const centerX = venueWidthM / 2;
  const subSpacing = 0.85;
  const startSubX = centerX - ((expandedSubs.length - 1) * subSpacing) / 2;

  for (let i = 0; i < expandedSubs.length; i++) {
    const sub = expandedSubs[i];
    const subX = Number((startSubX + i * subSpacing).toFixed(2));
    const subDiffDb = Number((10 * Math.log10(sub.rmsWatts / maxSubRms)).toFixed(1));
    const subMatchNote =
      subDiffDb < -0.4
        ? ` | Atenuar sub mayor ${subDiffDb} dB para evitar tope mecánico (Xmax) en este cono`
        : '';

    items.push({
      id: `sub-${i + 1}`,
      tag: `S${i + 1}`,
      name: `${sub.modelLabel} (S${i + 1})`,
      category: 'sub_bass',
      systemType: sub.systemType,
      rmsWatts: sub.rmsWatts,
      peakWatts: sub.peakWatts,
      coneSizeInches: sub.coneSizeInches,
      impedanceOhms: sub.impedanceOhms,
      posX: subX,
      posY: 1.6,
      zone: 'SUB_CENTER_CLUSTER',
      zoneLabel: 'Bloque Central en Piso (Mono Cluster Acoplado)',
      delayMs: 0,
      recommendedGainNote: `Acoplamiento coherente (+6 dB gratis) — ${sub.rmsWatts}W RMS / ${sub.peakWatts}W Peak — LPF 85 Hz${subMatchNote}`,
      gainMatchingDb: subDiffDb,
    });
  }

  return items;
}

/**
 * CALCULADORA DE IMPEDANCIA EN PARALELO (LEY DE OHM PARA CAJAS Y SUBS PASIVOS)
 * Evalúa si las unidades pasivas conectadas por Speakon trabajan en 8 Ω, 4 Ω o caen bajo 3.2 Ω (riesgo PROTECT).
 */
export function analyzePassiveImpedance(
  batches: SpeakerBatchInput[],
  wiringMode: 'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK' = 'INDEPENDENT_CHANNELS'
): PassiveImpedanceAnalysis {
  const passiveTopUnits: number[] = [];
  const passiveSubUnits: number[] = [];

  for (const b of batches) {
    if (b.systemType !== 'PASSIVE') continue;
    const qty = Math.max(0, Math.floor(b.quantity || 0));
    const z = b.impedanceOhms || 8;
    for (let i = 0; i < qty; i++) {
      if (b.category === 'top_box') passiveTopUnits.push(z);
      else passiveSubUnits.push(z);
    }
  }

  const passiveTopsCount = passiveTopUnits.length;
  const passiveSubsCount = passiveSubUnits.length;
  const hasPassiveUnits = passiveTopsCount > 0 || passiveSubsCount > 0;

  if (!hasPassiveUnits) {
    return {
      hasPassiveUnits: false,
      wiringMode,
      passiveTopsCount: 0,
      passiveSubsCount: 0,
      topsEffectiveOhms: null,
      subsEffectiveOhms: null,
      minImpedanceOhms: null,
      status: 'NO_PASSIVE',
      technicalDirective: 'Sistema 100% Activo Autoamplificado: cada parlante tiene su propio amplificador Clase D interno calibrado de fábrica.',
      speakonRoutingNote: 'Conexión directa por señal balanceada XLR (no requiere amplificadores externos ni cables Speakon).',
    };
  }

  const calcParallelOhms = (ohmsList: number[], mode: 'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK'): number | null => {
    if (ohmsList.length === 0) return null;
    if (mode === 'INDEPENDENT_CHANNELS') {
      // Si se reparten en 2 canales estéreo (Ch A y Ch B) del amplificador:
      // Si hay 1 o 2 unidades, va 1 por canal; si hay >2 en un mismo power de 2 canales, se agrupan ceil(n/2) en el canal más cargado
      const maxUnitsOnOneChannel = Math.ceil(ohmsList.length / 2);
      const subset = ohmsList.slice(0, maxUnitsOnOneChannel);
      const invSum = subset.reduce((acc, z) => acc + 1 / z, 0);
      return Number((1 / invSum).toFixed(2));
    } else {
      // Modo Puente Paralelo (Speakon Link encadenado de caja a caja en un solo canal)
      const invSum = ohmsList.reduce((acc, z) => acc + 1 / z, 0);
      return Number((1 / invSum).toFixed(2));
    }
  };

  const topsEffectiveOhms = calcParallelOhms(passiveTopUnits, wiringMode);
  const subsEffectiveOhms = calcParallelOhms(passiveSubUnits, wiringMode);

  const candidates = [topsEffectiveOhms, subsEffectiveOhms].filter((v): v is number => v !== null);
  const minImpedanceOhms = candidates.length > 0 ? Math.min(...candidates) : null;

  let status: PassiveImpedanceAnalysis['status'] = 'OPTIMAL_8_OHM';
  let technicalDirective = '';
  let speakonRoutingNote = '';

  if (minImpedanceOhms !== null && minImpedanceOhms < 3.2) {
    status = 'DANGER_PROTECT_SHORT';
    technicalDirective = `¡ALERTA DE CORTOCIRCUITO / PROTECT (${minImpedanceOhms} Ω)! Al encadenar estas unidades pasivas en paralelo la impedancia cae bajo el límite seguro de 4 Ω. El amplificador externo se apagará por sobrecorriente o quemará sus transistores de salida. Cambia a "Canales Estéreo Independientes (Ch A / Ch B)" o agrega otro amplificador.`;
    speakonRoutingNote = `PROHIBIDO puentear más de 2 cajas de 8 Ω en el mismo canal (${minImpedanceOhms} Ω resultantes). Separa las tiradas Speakon NL4 directamente desde las borneras Ch 1 y Ch 2 del Power.`;
  } else if (minImpedanceOhms !== null && minImpedanceOhms <= 4.5) {
    status = 'HIGH_LOAD_4_OHM';
    technicalDirective = `Régimen de Alta Exigencia (${minImpedanceOhms} Ω por canal): La ley de Ohm en paralelo extrae el máximo amperaje del amplificador externo. Es seguro en etapas profesionales, pero exige ventilación despejada en el rack y cable Speakon de mínimo 2x2.5 mm².`;
    speakonRoutingNote = `Conexión en ${minImpedanceOhms} Ω: Verifica que los ventiladores del Power no estén obstruidos y usa conectores Neutrik Speakon NL4 con seguro giratorio.`;
  } else {
    status = 'OPTIMAL_8_OHM';
    technicalDirective = `Impedancia Nominal Óptima (${minImpedanceOhms} Ω por canal): El amplificador externo trabaja holgado, frío y con máximo factor de amortiguamiento (Damping Factor) para controlar el cono sin distorsión.`;
    speakonRoutingNote = `Cada unidad pasiva recibe su propio canal de amplificador a ${minImpedanceOhms} Ω mediante cable Speakon dedicado.`;
  }

  return {
    hasPassiveUnits: true,
    wiringMode,
    passiveTopsCount,
    passiveSubsCount,
    topsEffectiveOhms,
    subsEffectiveOhms,
    minImpedanceOhms,
    status,
    technicalDirective,
    speakonRoutingNote,
  };
}

export interface PowerAmpSizingResult {
  hasPassiveSpeakers: boolean;
  hasPassiveUnits: boolean;
  passiveTopsCount: number;
  passiveSubsCount: number;
  totalPassiveTopsRmsWatts: number;
  totalPassiveSubsRmsWatts: number;
  topsAmplifier?: {
    requiredChannels: number;
    wattsPerChannelRms: number;
    loadImpedanceOhms: number;
    recommendedHeadroomMultiplier: number;
    suggestedCommercialModel: string;
    directiveNote: string;
  };
  subsAmplifier?: {
    requiredChannels: number;
    wattsPerChannelRms: number;
    loadImpedanceOhms: number;
    recommendedHeadroomMultiplier: number;
    suggestedCommercialModel: string;
    directiveNote: string;
  };
  totalAmplifiersCount: number;
  totalAdditionalAcPowerWatts: number;
  suggestedRackModels: string[];
  technicalSummaryDirective: string;
  technicalRackDirective: string;
}

export function calculatePowerAmpSizing(
  batches: SpeakerBatchInput[],
  wiringMode: 'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK' = 'INDEPENDENT_CHANNELS'
): PowerAmpSizingResult {
  let passiveTopsCount = 0;
  let passiveSubsCount = 0;
  let totalPassiveTopsRmsWatts = 0;
  let totalPassiveSubsRmsWatts = 0;
  let topsUnitRms = 350;
  let subsUnitRms = 600;
  let topsImpedance = 8;
  let subsImpedance = 8;

  for (const b of batches) {
    if (b.systemType !== 'PASSIVE') continue;
    const qty = Math.max(0, Math.floor(b.quantity || 0));
    const rms = Math.max(0, b.rmsWatts || 0);
    const z = b.impedanceOhms || 8;
    if (b.category === 'top_box') {
      passiveTopsCount += qty;
      totalPassiveTopsRmsWatts += qty * rms;
      if (rms > 0) topsUnitRms = rms;
      if (z > 0) topsImpedance = z;
    } else {
      passiveSubsCount += qty;
      totalPassiveSubsRmsWatts += qty * rms;
      if (rms > 0) subsUnitRms = rms;
      if (z > 0) subsImpedance = z;
    }
  }

  const hasPassiveSpeakers = passiveTopsCount > 0 || passiveSubsCount > 0;
  if (!hasPassiveSpeakers) {
    return {
      hasPassiveSpeakers: false,
      hasPassiveUnits: false,
      passiveTopsCount: 0,
      passiveSubsCount: 0,
      totalPassiveTopsRmsWatts: 0,
      totalPassiveSubsRmsWatts: 0,
      totalAmplifiersCount: 0,
      totalAdditionalAcPowerWatts: 0,
      suggestedRackModels: [],
      technicalSummaryDirective: 'Sistema 100% Activo: No requiere etapas de potencia externas.',
      technicalRackDirective: 'Sistema 100% Activo: No requiere etapas de potencia externas.',
    };
  }

  // Regla Pro Audio Headroom: 1.6x RMS para evitar clipping y proteger bobinas
  const HEADROOM = 1.6;

  // Sizing para Tops Pasivos
  let topsAmplifier: PowerAmpSizingResult['topsAmplifier'];
  if (passiveTopsCount > 0) {
    const channels = 2;
    const boxesPerChannel = Math.max(1, Math.ceil(passiveTopsCount / channels));
    const loadOhms = wiringMode === 'PARALLEL_SPEAKON_LINK'
      ? Number((topsImpedance / boxesPerChannel).toFixed(1))
      : topsImpedance;
    const wattsPerCh = Math.round(boxesPerChannel * topsUnitRms * HEADROOM);

    let suggestedModel = 'Crown XLi 1500 / Powersoft Mezzo (2×600W @ 4Ω)';
    if (wattsPerCh > 1000) {
      suggestedModel = 'Crown XTi 4002 / Powersoft T604 (2×1200W @ 4Ω)';
    } else if (wattsPerCh > 600) {
      suggestedModel = 'Crown XLi 2500 / Behringer NX3000D (2×800W @ 4Ω)';
    }

    topsAmplifier = {
      requiredChannels: channels,
      wattsPerChannelRms: wattsPerCh,
      loadImpedanceOhms: loadOhms,
      recommendedHeadroomMultiplier: HEADROOM,
      suggestedCommercialModel: suggestedModel,
      directiveNote: `${passiveTopsCount} cajas tops pasivas (${boxesPerChannel} por canal a ${loadOhms} Ω): Exige ${wattsPerCh}W RMS por canal con margen de cresta 1.6×.`,
    };
  }

  // Sizing para Subs Pasivos
  let subsAmplifier: PowerAmpSizingResult['subsAmplifier'];
  if (passiveSubsCount > 0) {
    const channels = 2;
    const boxesPerChannel = Math.max(1, Math.ceil(passiveSubsCount / channels));
    const loadOhms = wiringMode === 'PARALLEL_SPEAKON_LINK'
      ? Number((subsImpedance / boxesPerChannel).toFixed(1))
      : subsImpedance;
    const wattsPerCh = Math.round(boxesPerChannel * subsUnitRms * HEADROOM);

    let suggestedModel = 'Crown XTi 4002 / Lab Gruppen IPD 2400 (2×1200W @ 4Ω)';
    if (wattsPerCh > 1600) {
      suggestedModel = 'Powersoft X4 / Lab Gruppen FP10000Q (2×2200W @ 4Ω)';
    } else if (wattsPerCh > 1000) {
      suggestedModel = 'Crown XTi 6002 / Behringer NX6000D (2×1600W @ 4Ω)';
    }

    subsAmplifier = {
      requiredChannels: channels,
      wattsPerChannelRms: wattsPerCh,
      loadImpedanceOhms: loadOhms,
      recommendedHeadroomMultiplier: HEADROOM,
      suggestedCommercialModel: suggestedModel,
      directiveNote: `${passiveSubsCount} subwoofers pasivos en ${loadOhms} Ω: Exige ${wattsPerCh}W RMS por canal con alto damping factor para control de graves.`,
    };
  }

  const totalAmplifiersCount = (topsAmplifier ? 1 : 0) + (subsAmplifier ? 1 : 0);
  const totalPassiveAudioRms = totalPassiveTopsRmsWatts + totalPassiveSubsRmsWatts;
  const totalAdditionalAcPowerWatts = Math.round((totalPassiveAudioRms * 0.35) / 0.85) + totalAmplifiersCount * 60;
  const technicalSummaryDirective = `Rack de ${totalAmplifiersCount} Etapa(s) de Potencia requerido: Consumo eléctrico adicional estimado en ${totalAdditionalAcPowerWatts}W continuos a 220V.`;

  const suggestedRackModels: string[] = [];
  if (topsAmplifier) suggestedRackModels.push(topsAmplifier.suggestedCommercialModel);
  if (subsAmplifier) suggestedRackModels.push(subsAmplifier.suggestedCommercialModel);

  return {
    hasPassiveSpeakers: true,
    hasPassiveUnits: true,
    passiveTopsCount,
    passiveSubsCount,
    totalPassiveTopsRmsWatts,
    totalPassiveSubsRmsWatts,
    topsAmplifier,
    subsAmplifier,
    totalAmplifiersCount,
    totalAdditionalAcPowerWatts,
    suggestedRackModels,
    technicalSummaryDirective,
    technicalRackDirective: technicalSummaryDirective,
  };
}

/**
 * Analiza la mezcla híbrida de hardware y genera el reporte de ruteo, cables, estrategia acústica
 * y separación automática en 2 Líneas Eléctricas (Línea 1 Fuerza Graves / Línea 2 Medios-Agudos + Cabina).
 */
export function analyzeHybridRig(
  items: RigEquipmentItem[],
  outlets: OutletPoint[],
  djBoothPos = { x: 5, y: 1.2 }
): HybridRigAnalysis {
  const roster: EquipmentRosterConnection[] = [];

  let activeTopsCount = 0;
  let passiveTopsCount = 0;
  let activeSubsCount = 0;
  let passiveSubsCount = 0;
  let frontTopsCount = 0;
  let delayTopsCount = 0;

  let totalPowerWatts220v = 0;
  let totalPeakWatts220v = 0;
  let totalRmsAudioWatts = 0;
  let totalPeakAudioWatts = 0;

  let line1SubsWatts = 0;
  let line1SubsPeakWatts = 0;
  let line2TopsCtrlWatts = 0;
  let line2TopsCtrlPeakWatts = 0;

  let powerCordsIecCount = 0;
  let powerCordsPowerconCount = 0;
  let speakonCablesCount = 0;
  let xlrCablesCount = 0;
  let totalFloorCablesMeters = 0;

  const safeOutlets = outlets.length > 0 ? outlets : [
    { id: 'out-1', name: 'Toma General 220V', maxAmps: 16, maxWatts: 3520, posX: 0, posY: 0 }
  ];

  for (const item of items) {
    // 1. Encontrar el enchufe más cercano (distancia Manhattan por orillas)
    let bestOutlet = safeOutlets[0];
    let minDistance = 99999;

    for (const out of safeOutlets) {
      const dist = Math.abs(item.posX - out.posX) + Math.abs(item.posY - out.posY);
      if (dist < minDistance) {
        minDistance = dist;
        bestOutlet = out;
      }
    }

    // Subida de 2.2m en trípode para cajas acústicas (por encima de las cabezas del público)
    const heightDrop = item.category === 'top_box' ? 2.2 : 0.3;
    const rawPowerMeters = (minDistance * 1.15) + heightDrop;
    const powerCableMeters = roundToStandardLength(rawPowerMeters);

    // Distancia hacia la cabina DJ para cables de audio/señal
    const distToDj = Math.abs(item.posX - djBoothPos.x) + Math.abs(item.posY - djBoothPos.y);
    const rawSignalMeters = (distToDj * 1.15) + heightDrop;
    const signalLengthMeters = roundToStandardLength(rawSignalMeters);

    const unitPeakWatts = item.peakWatts || item.rmsWatts * 2;
    const unitConeInches = item.coneSizeInches || (item.category === 'sub_bass' ? 18 : 15);
    const unitImpedanceOhms = item.impedanceOhms || 8;

    totalRmsAudioWatts += item.rmsWatts;
    totalPeakAudioWatts += unitPeakWatts;

    let powerWatts220v = 0;
    let peakWatts220v = 0;
    let powerCableType: EquipmentRosterConnection['powerCableType'] = 'NONE_PASSIVE';
    let signalCableType: EquipmentRosterConnection['signalCableType'] = 'NONE';
    let signalOrigin = 'Cabina DJ';
    let colorHex = '#3b82f6';
    let badgeBg = 'bg-blue-950 text-blue-300 border-blue-600';
    let powerLineAssignment: 'LINE_1_SUBS' | 'LINE_2_TOPS_CTRL' =
      item.category === 'sub_bass' ? 'LINE_1_SUBS' : 'LINE_2_TOPS_CTRL';

    const isDelayBox = item.zone === 'DELAY_RING_1' || item.zone === 'DELAY_RING_2';

    if (item.category === 'top_box') {
      if (isDelayBox) delayTopsCount++;
      else frontTopsCount++;

      if (item.systemType === 'ACTIVE') {
        activeTopsCount++;
        // Consumo continuo real con factor de servicio 1/3 (0.33) / eficiencia 0.90 para no sobredimensionar
        powerWatts220v = Math.round((item.rmsWatts * 0.33) / 0.90);
        peakWatts220v = Math.round((unitPeakWatts * 0.38) / 0.90);
        line2TopsCtrlWatts += powerWatts220v;
        line2TopsCtrlPeakWatts += peakWatts220v;
        powerCableType = 'IEC_PC';
        powerCordsIecCount++;
        signalCableType = 'XLR_AUDIO';
        signalOrigin = isDelayBox
          ? `Procesador DSP / Salida Delay (${item.delayMs} ms)`
          : 'Salida Master Cabina DJ (0 dB Line)';
        xlrCablesCount++;
        colorHex = isDelayBox ? '#10b981' : '#ef4444';
        badgeBg = isDelayBox
          ? 'bg-emerald-950 text-emerald-300 border-emerald-500'
          : 'bg-red-950 text-red-300 border-red-600';
      } else {
        passiveTopsCount++;
        powerWatts220v = 0;
        peakWatts220v = 0;
        powerCableType = 'NONE_PASSIVE';
        signalCableType = 'SPEAKON_PASIVO';
        signalOrigin = isDelayBox
          ? `Amplificador Delay c/ DSP (${item.delayMs} ms - Speakon ${unitImpedanceOhms}Ω)`
          : `Amplificador Frontal (Salida Speakon NL4 - ${unitImpedanceOhms}Ω)`;
        speakonCablesCount++;
        colorHex = '#f59e0b';
        badgeBg = 'bg-amber-950 text-amber-300 border-amber-600';
      }
    } else if (item.category === 'sub_bass') {
      if (item.systemType === 'ACTIVE') {
        activeSubsCount++;
        powerWatts220v = Math.round((item.rmsWatts * 0.33) / 0.90);
        peakWatts220v = Math.round((unitPeakWatts * 0.42) / 0.90);
        line1SubsWatts += powerWatts220v;
        line1SubsPeakWatts += peakWatts220v;
        powerCableType = 'POWERCON';
        powerCordsPowerconCount++;
        signalCableType = 'XLR_AUDIO';
        signalOrigin = 'Salida Sub / Crossover Mono Cabina DJ';
        xlrCablesCount++;
        colorHex = '#8b5cf6';
        badgeBg = 'bg-purple-950 text-purple-300 border-purple-600';
      } else {
        passiveSubsCount++;
        powerWatts220v = 0;
        peakWatts220v = 0;
        powerCableType = 'NONE_PASSIVE';
        signalCableType = 'SPEAKON_PASIVO';
        signalOrigin = `Amplificador de Sub Bajos (Speakon NL4 - ${unitImpedanceOhms}Ω)`;
        speakonCablesCount++;
        colorHex = '#06b6d4';
        badgeBg = 'bg-cyan-950 text-cyan-300 border-cyan-600';
      }
    } else if (item.category === 'lighting') {
      powerWatts220v = item.rmsWatts;
      peakWatts220v = item.rmsWatts;
      line2TopsCtrlWatts += powerWatts220v;
      line2TopsCtrlPeakWatts += peakWatts220v;
      powerCableType = 'IEC_PC';
      powerCordsIecCount++;
      signalCableType = 'DMX_LIGHT';
      signalOrigin = 'Controladora DMX / Cabina DJ';
      colorHex = '#eab308';
      badgeBg = 'bg-yellow-950 text-yellow-300 border-yellow-600';
    }

    const drawAmps = Number((powerWatts220v / (220 * 0.92)).toFixed(2));
    totalPowerWatts220v += powerWatts220v;
    totalPeakWatts220v += peakWatts220v;

    if (powerCableType !== 'NONE_PASSIVE') {
      totalFloorCablesMeters += powerCableMeters;
    }
    if (signalCableType === 'SPEAKON_PASIVO' || signalCableType === 'XLR_AUDIO') {
      totalFloorCablesMeters += signalLengthMeters;
    }

    roster.push({
      id: item.id,
      tag: item.tag,
      name: item.name,
      category: item.category,
      systemType: item.systemType,
      rmsWatts: item.rmsWatts,
      peakWatts: unitPeakWatts,
      coneSizeInches: unitConeInches,
      impedanceOhms: unitImpedanceOhms,
      powerWatts220v,
      peakWatts220v,
      drawAmps,
      assignedOutletName: bestOutlet.name,
      powerLineAssignment,
      powerCableMeters: powerCableType !== 'NONE_PASSIVE' ? powerCableMeters : 0,
      powerCableType,
      signalCableType,
      signalLengthMeters,
      signalOrigin,
      colorHex,
      badgeBg,
      posX: item.posX,
      posY: item.posY,
      zone: item.zone || 'PA_FRONT_L',
      zoneLabel: item.zoneLabel || 'Frente Principal',
      delayMs: item.delayMs || 0,
      recommendedGainNote: item.recommendedGainNote || 'Unity 0 dB (12:00)',
      gainMatchingDb: item.gainMatchingDb || 0,
    });
  }

  let externalAmpsRequiredCount = 0;
  if (passiveTopsCount > 0) {
    externalAmpsRequiredCount += Math.ceil(passiveTopsCount / 2);
  }
  if (passiveSubsCount > 0) {
    externalAmpsRequiredCount += Math.ceil(passiveSubsCount / 2);
  }

  // Sumar consumo real de amplificadores pasivos (separados por Línea 1 Subs vs Línea 2 Tops)
  if (externalAmpsRequiredCount > 0) {
    const passiveTopsRmsSum = roster
      .filter(r => r.systemType === 'PASSIVE' && r.category === 'top_box')
      .reduce((acc, r) => acc + r.rmsWatts, 0);
    const passiveTopsPeakSum = roster
      .filter(r => r.systemType === 'PASSIVE' && r.category === 'top_box')
      .reduce((acc, r) => acc + r.peakWatts, 0);

    const passiveSubsRmsSum = roster
      .filter(r => r.systemType === 'PASSIVE' && r.category === 'sub_bass')
      .reduce((acc, r) => acc + r.rmsWatts, 0);
    const passiveSubsPeakSum = roster
      .filter(r => r.systemType === 'PASSIVE' && r.category === 'sub_bass')
      .reduce((acc, r) => acc + r.peakWatts, 0);

    const passiveTopsRealW = Math.round((passiveTopsRmsSum * 0.33) / 0.90);
    const passiveTopsPeakW = Math.round((passiveTopsPeakSum * 0.38) / 0.90);
    const passiveSubsRealW = Math.round((passiveSubsRmsSum * 0.33) / 0.90);
    const passiveSubsPeakW = Math.round((passiveSubsPeakSum * 0.42) / 0.90);

    line2TopsCtrlWatts += passiveTopsRealW;
    line2TopsCtrlPeakWatts += passiveTopsPeakW;
    line1SubsWatts += passiveSubsRealW;
    line1SubsPeakWatts += passiveSubsPeakW;

    totalPowerWatts220v += passiveTopsRealW + passiveSubsRealW;
    totalPeakWatts220v += passiveTopsPeakW + passiveSubsPeakW;
    powerCordsIecCount += externalAmpsRequiredCount;
  }

  // Sumar carga base de Cabina DJ + Iluminación LED (800W típicos en Línea 2)
  totalPowerWatts220v += 800;
  totalPeakWatts220v += 950;
  line2TopsCtrlWatts += 800;
  line2TopsCtrlPeakWatts += 950;

  const totalAmps220v = Number((totalPowerWatts220v / (220 * 0.92)).toFixed(2));
  const line1SubsAmps = Number((line1SubsWatts / (220 * 0.92)).toFixed(2));
  const line2TopsCtrlAmps = Number((line2TopsCtrlWatts / (220 * 0.92)).toFixed(2));

  const totalFloorTapeMeters = Math.ceil(totalFloorCablesMeters * 1.2);
  const floorTapeRolls50m = Math.max(1, Math.ceil(totalFloorTapeMeters / 50));

  let placementStrategySummary = '';
  if (delayTopsCount > 0) {
    placementStrategySummary = `Distribución Anti-Saturación Activa: Se ubicaron ${frontTopsCount} cajas en el Frente Principal (A, B) y ${delayTopsCount} caja(s) como Refuerzo Delay en la pista (${roster.filter(r => r.delayMs > 0).map(r => `${r.tag} a ${r.posY}m con ${r.delayMs}ms`).join(', ')}). Así toda la pista escucha entre 102 y 106 dBA fuertes y claros sin reventar a la primera fila ni saturar las cajas.`;
  } else {
    placementStrategySummary = `Frente Principal Estéreo (${frontTopsCount} cajas) elevadas a 2.2m en trípode + Subwoofers en Bloque Central Acoplado. Mantener mixer en 0 dB y potenciómetros a las 12:00 (Unity) para evitar recorte digital ("chicharreo").`;
  }

  const phaseBalanceDirective =
    line1SubsAmps > 0
      ? `Dividir obligatoriamente en 2 tiradas de cable independientes: LÍNEA 1 Exclusiva para Sub-Bajos (${line1SubsWatts}W continuos / ${line1SubsAmps}A, picos de ${line1SubsPeakWatts}W) y LÍNEA 2 para Cajas Superiores + Cabina DJ (${line2TopsCtrlWatts}W continuos / ${line2TopsCtrlAmps}A). Evita derretir zapatillas y aísla a la mixer DJ de las caídas de tensión del golpe de bombo.`
      : `Línea única de ${line2TopsCtrlWatts}W (${line2TopsCtrlAmps}A) para Cajas Superiores y Cabina DJ.`;

  const recommendations: string[] = [
    placementStrategySummary,
    `Subwoofers en Mono Cluster Central: Los ${activeSubsCount + passiveSubsCount} bajos se agruparon juntos al centro en el suelo (separación < 1.7m), ganando +6 dB acústicos gratis por acoplamiento y eliminando cancelaciones en la pista.`,
    phaseBalanceDirective,
    `Regla de Oro Anti-Chicharreo: Mantener el Master de la mixer DJM promediando en 0 dB y los potenciómetros de las cajas en posición 12:00 (0 dB Unity).`,
  ];

  return {
    roster,
    totalPowerWatts220v,
    totalPeakWatts220v,
    totalRmsAudioWatts,
    totalPeakAudioWatts,
    totalAmps220v,
    activeTopsCount,
    passiveTopsCount,
    activeSubsCount,
    passiveSubsCount,
    frontTopsCount,
    delayTopsCount,
    externalAmpsRequiredCount,
    powerCordsIecCount,
    powerCordsPowerconCount,
    speakonCablesCount,
    xlrCablesCount,
    totalFloorTapeMeters,
    floorTapeRolls50m,
    placementStrategySummary,
    recommendations,
    electricalLines: {
      line1SubsWatts,
      line1SubsPeakWatts,
      line1SubsAmps,
      line2TopsCtrlWatts,
      line2TopsCtrlPeakWatts,
      line2TopsCtrlAmps,
      phaseBalanceDirective,
    },
  };
}
