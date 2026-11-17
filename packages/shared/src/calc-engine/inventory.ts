// ======================================================================
// CALC-ENGINE: INVENTORY & DISPOSITION MODULE
// Inventario de soportes, zapatillas y secuencia de montaje
// ======================================================================

export interface SupportInventoryInput {
  subsCount: number;
  topsCount: number;
  topsMountedOnSubPole: number;
  totalOutletsRequired: number;
}

export interface SupportInventoryResult {
  subsAtFloorCount: number;
  poleMountsCount: number;
  tripodStandsCount: number;
  powerStripsCount: number;
  totalOutletsSupplied: number;
  spareOutletsCount: number;
  warningDiscrepancy?: string;
}

export function calculateSupportInventory(input: SupportInventoryInput): SupportInventoryResult {
  const { subsCount, topsCount, topsMountedOnSubPole, totalOutletsRequired } = input;

  // 1. Subwoofers obligatoriamente a piso (acoplamiento acústico de semiesfera y estabilidad mecánica)
  const subsAtFloorCount = subsCount;

  // 2. Pole mounts no pueden superar la cantidad de subs ni la de tops
  const effectivePoleMounts = Math.min(topsMountedOnSubPole, subsCount, topsCount);

  // 3. Atriles trípode = tops restantes que no van en pole mount
  const tripodStandsCount = Math.max(0, topsCount - effectivePoleMounts);

  // 4. Zapatillas eléctricas industriales (estándar 6 tomas por zapatilla con al menos 1 de reserva)
  // Cada zapatilla aporta 5 tomas útiles y 1 de reserva garantizada
  const outletsPerStrip = 6;
  const usefulOutletsPerStrip = 5;
  const powerStripsCount = Math.max(1, Math.ceil(totalOutletsRequired / usefulOutletsPerStrip));
  const totalOutletsSupplied = powerStripsCount * outletsPerStrip;
  const spareOutletsCount = totalOutletsSupplied - totalOutletsRequired;

  let warningDiscrepancy: string | undefined;
  if (topsMountedOnSubPole > subsCount) {
    warningDiscrepancy = `Se especificaron ${topsMountedOnSubPole} tops en pole mount, pero sólo hay ${subsCount} subwoofers disponibles de base. Se ajustó a ${effectivePoleMounts} pole mounts y ${tripodStandsCount} atriles trípode.`;
  }

  return {
    subsAtFloorCount,
    poleMountsCount: effectivePoleMounts,
    tripodStandsCount,
    powerStripsCount,
    totalOutletsSupplied,
    spareOutletsCount,
    warningDiscrepancy,
  };
}

export const MOUNTING_PROTOCOL_STEPS = [
  {
    step: 1,
    title: 'Subwoofers en Mono Cluster Central a Piso',
    instruction: 'Agrupar todos los sub bajos juntos al centro frente a la cabina DJ en el suelo (separación < 1.7m entre conos) sobre gomas antideslizantes. Esto suma +6 dB gratis por acoplamiento coherente y elimina el "pasillo de la muerte" (cancelación de fase).',
  },
  {
    step: 2,
    title: 'Elevación de Cajas Acústicas en Atriles Independientes y Torres Delay',
    instruction: 'Jamás montar cajas sobre los sub bajos. Elevar el par frontal (A, B) en trípodes a 2.0-2.2m sobre las cabezas del público, y ubicar las cajas adicionales (C, D, E, F) como Torres de Refuerzo Delay en los costados de la pista.',
  },
  {
    step: 3,
    title: 'Tendido Eléctrico y Desenrollado Completo',
    instruction: 'Tender los alargadores desde el punto de suministro (tablero o generador) y fijarlos al piso con cinta Gaffer gris. Desenrollar el 100% de los carretes antes de energizar para prevenir efecto bobina y sobrecalentamiento.',
  },
  {
    step: 4,
    title: 'Calibración de Ganancia en Mixer (Trim, Fader, Master y Mezcla de 2 Canales)',
    instruction: 'Fader de canal al tope (10 / 0 dB). Ajustar Trim en el drop para marcar +3 a +6 dB (LEDs ámbar, CERO rojo). Ajustar Master entre 0 y +3 dB (+4 a +7 dBu XLR limpios). Al mezclar 2 canales en +6 dB, cortar el LOW EQ (40-250 Hz) de 1 canal ("un solo bajo a la vez") para evitar barro y cancelación de fase. En cajas activas: perilla a las 12:00 (0 dB Unity) con corte HPF 80 Hz.',
  },
  {
    step: 5,
    title: 'Protocolo de Encendido y Apagado Seguro',
    instruction: 'Encendido: 1° Mixer DJ y procesadores DSP, 2° Iluminación, 3° Amplificadores y cajas activas (últimos). Apagado en orden inverso (cajas activas primero) para evitar estallidos ("pop") en los transductores.',
  },
] as const;

export const MIXER_GAIN_STAGING_TABLE = [
  {
    section: 'Canal Individual (Trim / Gain)',
    optimalRange: '+3 dB a +6 dB',
    ledColor: 'Verde sólido + 1 a 2 LEDs Ámbar',
    technicalFunction: 'Normaliza el nivel de entrada del track en el drop (kick + bajo) sin saturar el bus de suma interna.',
  },
  {
    section: 'Fader de Canal',
    optimalRange: 'Al 10 (Tope arriba / 0 dB)',
    ledColor: 'Recorrido completo',
    technicalFunction: 'Garantiza ganancia unitaria y máxima resolución física de mezcla.',
  },
  {
    section: 'Vúmetro Master (XLR Out)',
    optimalRange: '0 dB a +3 dB (Máx +6 dB)',
    ledColor: 'Verde completo + primer LED Ámbar',
    technicalFunction: 'Entrega +4 dBu (1.228V RMS) a +7 dBu balanceados con máxima relación señal/ruido y transientes intactos.',
  },
  {
    section: 'Transición con 2 Canales a +6 dB',
    optimalRange: 'Master estable en 0 a +3 dB',
    ledColor: 'Low EQ Kill en 1 canal',
    technicalFunction: 'Un solo bajo a la vez: evita barro (40-250 Hz), cancelación de fase entre bombos y sobrecarga (+9 a +12 dB) del bus Master.',
  },
  {
    section: 'Zona Roja (Canal o Master)',
    optimalRange: '+10 dB a +15 dB (OVER / CLIP)',
    ledColor: 'ROJO (PROHIBIDO)',
    technicalFunction: 'Activa el limitador D/A, aplasta el golpe del bombo, genera onda semicuadrada ("chicharreo") y recalienta bobinas.',
  },
] as const;

