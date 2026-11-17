// ======================================================================
// CALC-ENGINE: ACOUSTICS MODULE
// Fórmulas de impedancia, amplificación pasiva y atenuación acústica SPL
// ======================================================================

export interface PassiveChannelInput {
  boxesCount: number;
  boxRmsWatts: number;
  boxImpedanceOhms: number;
  wiring: 'PARALLEL' | 'SERIES';
  headroomFactor?: number;
  minAmpImpedance?: number;
  ampEfficiency?: number;
}

export interface PassiveChannelResult {
  equivalentImpedanceOhms: number;
  totalChannelRmsWatts: number;
  recommendedAmpWattsPerChannel: number;
  networkPowerConservativeWatts: number; // Factor de uso 1.0
  networkPowerMusicalWatts: number;      // Factor de uso 0.5
  isBelowMinImpedance: boolean;
  alertLevel: 'INFO' | 'WARNING' | 'CRITICAL';
  alertMessage: string;
}

export function calculatePassiveAmplification(input: PassiveChannelInput): PassiveChannelResult {
  const {
    boxesCount,
    boxRmsWatts,
    boxImpedanceOhms,
    wiring,
    headroomFactor = 1.5,
    minAmpImpedance = 4,
    ampEfficiency = 0.8,
  } = input;

  // 1. Impedancia equivalente
  let equivalentImpedanceOhms: number;
  if (wiring === 'PARALLEL') {
    equivalentImpedanceOhms = boxImpedanceOhms / boxesCount;
  } else {
    equivalentImpedanceOhms = boxImpedanceOhms * boxesCount;
  }

  // 2. Potencia RMS total en el canal
  const totalChannelRmsWatts = boxRmsWatts * boxesCount;

  // 3. Potencia recomendada del amplificador (con headroom)
  const recommendedAmpWattsPerChannel = Math.round(totalChannelRmsWatts * headroomFactor);

  // 4. Consumo de red eléctrica (sobre la demanda RMS real de las cajas, no sobre el pico del amp)
  // P_red = (P_RMS / Eficiencia) * Factor_de_uso
  const networkPowerConservativeWatts = Math.round((totalChannelRmsWatts / ampEfficiency) * 1.0);
  const networkPowerMusicalWatts = Math.round((totalChannelRmsWatts / ampEfficiency) * 0.5);

  // 5. Alerta de impedancia mínima del amplificador
  const isBelowMinImpedance = equivalentImpedanceOhms < minAmpImpedance;
  let alertLevel: 'INFO' | 'WARNING' | 'CRITICAL' = 'INFO';
  let alertMessage = `Impedancia resultante (${equivalentImpedanceOhms} ohms) compatible con el amplificador (mínimo ${minAmpImpedance} ohms).`;

  if (isBelowMinImpedance) {
    alertLevel = 'CRITICAL';
    alertMessage = `ALERTA CRÍTICA: Impedancia equivalente (${equivalentImpedanceOhms} ohms) es inferior a la admitida por el amplificador (${minAmpImpedance} ohms). Riesgo de disparo de protección o daño permanente a la etapa de potencia.`;
  }

  return {
    equivalentImpedanceOhms: Number(equivalentImpedanceOhms.toFixed(2)),
    totalChannelRmsWatts,
    recommendedAmpWattsPerChannel,
    networkPowerConservativeWatts,
    networkPowerMusicalWatts,
    isBelowMinImpedance,
    alertLevel,
    alertMessage,
  };
}

export interface SplCoverageInput {
  sensitivityDb: number; // dB @ 1W/1m
  powerRmsWatts: number;
  distanceFirstRowMeters?: number; // Por defecto 4m
  distanceBackMeters: number;      // Fondo del salón
  splTargetDb?: number;            // Por defecto 98 dB
  maxSplDropThresholdDb?: number;  // Por defecto 10 dB
  isIndoor?: boolean;
}

export interface SplCoverageResult {
  splAt1mDb: number;
  splAtFirstRowDb: number;
  splAtBackDb: number;
  splDropFrom1mDb: number;
  splDropFirstRowToBackDb: number;
  recommendDelayFill: boolean;
  recommendationReason: string[];
  indoorAcousticNote: string;
}

export function calculateSplCoverage(input: SplCoverageInput): SplCoverageResult {
  const {
    sensitivityDb,
    powerRmsWatts,
    distanceFirstRowMeters = 4,
    distanceBackMeters,
    splTargetDb = 98,
    maxSplDropThresholdDb = 10,
    isIndoor = false,
  } = input;

  // Ley de inverso del cuadrado: SPL(d) = Sensibilidad + 10*log10(P_RMS) - 20*log10(d)
  // El cálculo estándar de pre-producción redondea el SPL a 1m (125.0 dB) y a partir de él proyecta las distancias
  const powerGain = 10 * Math.log10(powerRmsWatts);
  const splAt1mDb = Number((sensitivityDb + powerGain).toFixed(1));

  const splAtFirstRowDb = Number((splAt1mDb - 20 * Math.log10(distanceFirstRowMeters)).toFixed(1));
  const splAtBackDb = Number((splAt1mDb - 20 * Math.log10(distanceBackMeters)).toFixed(1));

  const splDropFrom1mDb = Number((splAt1mDb - splAtBackDb).toFixed(1));
  const splDropFirstRowToBackDb = Number((splAtFirstRowDb - splAtBackDb).toFixed(1));

  const reasons: string[] = [];
  let recommendDelayFill = false;

  // Criterio a: Caída entre primera fila y fondo supera el umbral (10 dB por defecto)
  if (splDropFirstRowToBackDb > maxSplDropThresholdDb) {
    recommendDelayFill = true;
    reasons.push(
      `La caída sonora entre la primera fila y el fondo (${splDropFirstRowToBackDb.toFixed(1)} dB) supera el umbral confortable de ${maxSplDropThresholdDb} dB.`
    );
  }

  // Criterio b: SPL en el fondo cae bajo el objetivo para formato DJ (98 dB)
  if (splAtBackDb < splTargetDb) {
    recommendDelayFill = true;
    reasons.push(
      `El nivel de presión sonora en el fondo (${splAtBackDb.toFixed(1)} dB) está por debajo de los ${splTargetDb} dB requeridos para una experiencia DJ envolvente.`
    );
  }

  // Criterio c: Profundidad superior a distancias críticas de absorción atmosférica
  const maxDistanceNoDelay = isIndoor ? 30 : 20;
  if (distanceBackMeters > maxDistanceNoDelay) {
    recommendDelayFill = true;
    reasons.push(
      `La distancia de fondo (${distanceBackMeters} m) excede el alcance óptimo de agudos (${maxDistanceNoDelay} m) por absorción de aire. Se requiere línea de retardo (delay).`
    );
  }

  return {
    splAt1mDb: Number(splAt1mDb.toFixed(1)),
    splAtFirstRowDb: Number(splAtFirstRowDb.toFixed(1)),
    splAtBackDb: Number(splAtBackDb.toFixed(1)),
    splDropFrom1mDb: Number(splDropFrom1mDb.toFixed(1)),
    splDropFirstRowToBackDb: Number(splDropFirstRowToBackDb.toFixed(1)),
    recommendDelayFill,
    recommendationReason: reasons,
    indoorAcousticNote: isIndoor
      ? 'Aviso acústico: en recintos cerrados, las reflexiones y el campo reverberante atenúan menos que la ley teórica de campo libre (-6 dB por duplicación de distancia).'
      : 'Cálculo de campo libre en exterior.',
  };
}

