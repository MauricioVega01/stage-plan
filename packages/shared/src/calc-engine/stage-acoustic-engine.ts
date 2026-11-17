// ======================================================================
// CALC-ENGINE: ADVANCED ACOUSTIC & ELECTRICAL SPECIFICATION (STAGE PLAN v3.6)
// Soporte unificado y riguroso para ESPACIOS ABIERTOS (Campo Libre)
// y ESPACIOS CERRADOS (Campo Reverberante / Ecuación de Hopkins-Stryker)
// ======================================================================

export interface AudioBox {
  id: string;
  name: string;
  type: 'TOP' | 'SUB';
  powerRms: number;            // Watts RMS
  sensitivity: number;         // dB SPL @ 1W/1m
  potentiometerGainDb: number; // dB (0 dB = Unity/12:00, +4 dB = ~2:00)
  quantity: number;
}

export interface VenueEnvironment {
  areaM2: number;
  lengthM: number;
  widthM: number;
  heightM?: number;            // Altura de techo para cerrados
  temperatureCelsius: number;
  targetSplDba: number;
  environmentType: 'OUTDOOR_OPEN' | 'INDOOR_CLOSED';
  // En cerrados: coeficiente medio de absorción alfa (ej: 0.15 galpón / 0.25 salón con cortinas)
  absorptionCoefficient?: number;
}

export interface SystemCalculationOutput {
  frontSystem: {
    spl1mPeak: number;
    spl1mContinuous: number;
    splAtDistances: { distanceM: number; splPeak: number; splAeq: number }[];
    reverberationTimeRt60Seconds?: number;
    roomConstantR?: number;
  };
  delayLineRecommendation: {
    required: boolean;
    triggerDistanceM: number;
    delayTimeMs: number;
    haasCompensationMs: number;
    totalDelayMs: number;
    notes: string;
  };
  tonalBalance: {
    subToTopRatioDb: number;
    status: 'OPTIMAL' | 'SUB_DEFICIT' | 'SUB_EXCESS';
    boundaryGainAppliedDb: number;
  };
  electricalRequirements: {
    realAudioConsumptionWatts: number;
    totalActivePowerWatts: number;
    apparentPowerVa: number;
    minimumGeneratorKva: number;
    nominalCurrentAmperes220V: number;
  };
}

export class StageAcousticEngine {
  private static readonly CREST_FACTOR_MUSIC = 7.0; // dB para música electrónica
  private static readonly AMP_HEADROOM = 6.0;       // dB
  private static readonly DUTY_CYCLE = 0.33;        // 1/3 de potencia nominal
  private static readonly AMP_EFFICIENCY = 0.90;    // Clase D
  private static readonly POWER_FACTOR = 0.92;      // SMPS con PFC
  private static readonly GENERATOR_SAFETY = 1.45;  // Margen transitorio AVR

  public static calculate(
    boxes: AudioBox[],
    venue: VenueEnvironment,
    auxiliaryLoadsWatts = 800
  ): SystemCalculationOutput {
    const isIndoor = venue.environmentType === 'INDOOR_CLOSED';
    const height = venue.heightM || 3.5;
    const volumeM3 = venue.areaM2 * height;

    // 1. Velocidad del sonido con corrección de temperatura
    const c = 331.3 + 0.606 * venue.temperatureCelsius;

    // 2. Parámetros acústicos de sala (si es cerrado)
    // Coeficiente de absorción promedio (Sabine)
    const alpha = venue.absorptionCoefficient || (isIndoor ? 0.18 : 1.0);
    // Área total de superficies envolventes (piso, techo y 4 muros)
    const totalSurfaceArea = 2 * (venue.widthM * venue.lengthM + venue.widthM * height + venue.lengthM * height);
    // Constante de sala R = (S * alfa) / (1 - alfa)
    const roomConstantR = isIndoor ? (totalSurfaceArea * alpha) / (1 - alpha) : 999999;
    // Tiempo de reverberación Sabine RT60
    const rt60 = isIndoor ? 0.161 * (volumeM3 / (totalSurfaceArea * alpha)) : undefined;

    // Factor de directividad Q típico en cajas de frente (Q=2 en espacio abierto, Q=4 en esquina/muro cerrado)
    const directivityQ = isIndoor ? 4.0 : 2.0;

    // 3. Separar fuentes
    const tops = boxes.filter(b => b.type === 'TOP');
    const subs = boxes.filter(b => b.type === 'SUB');

    // 4. Cálculo acústico de Tops a 1m
    let totalTopPowerRms = 0;
    let splTopEnergySum = 0;

    tops.forEach(box => {
      totalTopPowerRms += box.powerRms * box.quantity;
      const unitSplCont = box.sensitivity + 10 * Math.log10(box.powerRms) + box.potentiometerGainDb;
      // Suma incoherente en medios/agudos
      const combinedSpl = unitSplCont + 10 * Math.log10(box.quantity);
      splTopEnergySum += Math.pow(10, combinedSpl / 10);
    });

    const frontTopsSpl1mCont = splTopEnergySum > 0 ? 10 * Math.log10(splTopEnergySum) : 0;
    const frontTopsSpl1mPeak = frontTopsSpl1mCont > 0 ? frontTopsSpl1mCont + this.AMP_HEADROOM : 0;

    // 5. Cálculo acústico de Subs a 1m (Mono cluster)
    // Acoplamiento de suelo (+6 dB half-space) + carga acústica de muros cerrados (+3 dB quarter-space si es cerrado)
    const boundaryGainDb = isIndoor ? 9.0 : 6.0;
    let totalSubPowerRms = 0;
    let splSubPressureSum = 0;

    subs.forEach(box => {
      totalSubPowerRms += box.powerRms * box.quantity;
      const unitSplCont = (box.sensitivity + boundaryGainDb) + 10 * Math.log10(box.powerRms) + box.potentiometerGainDb;
      // Suma coherente en graves (20*log10)
      const combinedSpl = unitSplCont + 20 * Math.log10(box.quantity);
      splSubPressureSum += Math.pow(10, combinedSpl / 20);
    });

    const frontSubsSpl1mCont = splSubPressureSum > 0 ? 20 * Math.log10(splSubPressureSum) : 0;

    // 6. Muestreo de distancias críticas en la pista
    // En abierto: Ley pura del inverso del cuadrado (-6 dB por duplicación)
    // En cerrado: Ecuación de Hopkins-Stryker (campo directo + campo reverberante reflejado)
    const testDistances = [2, 5, 10, 15, venue.lengthM];
    const splAtDistances = testDistances.map(d => {
      const dist = Math.max(1, d);
      let splPeak: number;

      if (!isIndoor) {
        // Campo Libre (Outdoor)
        const distanceLoss = 20 * Math.log10(dist);
        splPeak = frontTopsSpl1mPeak - distanceLoss;
      } else {
        // Campo Cerrado (Indoor - Hopkins-Stryker)
        // SPL(d) = SPL_1m + 10*log10( Q / (4*pi*d^2) + 4 / R )
        // Normalizado respecto a d=1m
        const directRatio = directivityQ / (4 * Math.PI * dist * dist);
        const reverbRatio = 4 / roomConstantR;
        const totalRatio = directRatio + reverbRatio;
        const normalizedAt1m = (directivityQ / (4 * Math.PI)) + reverbRatio;
        const indoorLoss = 10 * Math.log10(totalRatio / normalizedAt1m);
        splPeak = frontTopsSpl1mPeak + indoorLoss;
      }

      splPeak = Number(splPeak.toFixed(1));
      const splAeq = Number((splPeak - this.CREST_FACTOR_MUSIC).toFixed(1));
      return { distanceM: d, splPeak, splAeq };
    });

    // 7. Evaluación de Línea de Retardo (Delay Line)
    // En abierto: La caída rápida a -6 dB/octava exige delay más pronto para no forzar el frente.
    // En cerrado: El campo reverberante sostiene el nivel al fondo, pero reduce la inteligibilidad si RT60 es alto.
    const lastDistance = splAtDistances[splAtDistances.length - 1];
    let delayRequired = false;
    let triggerDistance = venue.lengthM * 0.55;
    let delayNotes = '';

    if (!isIndoor) {
      // Abierto: gatilla si al fondo cae bajo el target SPL
      delayRequired = venue.lengthM > 12 && lastDistance && lastDistance.splAeq < venue.targetSplDba;
      delayNotes = 'Línea de retardo por atenuación en campo libre al aire libre.';
    } else {
      // Cerrado: si el salón es largo (>16m) y el tiempo de reverberación supera 1.4s, el delay mejora la inteligibilidad directa
      const needsIntelligibilityBoost = Boolean(rt60 && rt60 > 1.3 && venue.lengthM > 16);
      delayRequired = (lastDistance && lastDistance.splAeq < venue.targetSplDba) || needsIntelligibilityBoost;
      delayNotes = needsIntelligibilityBoost
        ? 'Refuerzo de delay recomendado en recinto cerrado para aumentar el sonido directo sobre la reverberación del salón.'
        : 'Cobertura asistida en recinto cerrado.';
    }

    const baseDelayMs = (triggerDistance / c) * 1000;
    const haasCompensationMs = 3.0;
    const totalDelayMs = baseDelayMs + haasCompensationMs;

    // 8. Balance Tonal (Sub vs Top a 5 metros)
    // En cerrado, los subgraves se ven reforzados naturalmente por modos de sala y reflexiones (+3 dB)
    let subAt5m: number;
    let topAt5m: number;

    if (!isIndoor) {
      subAt5m = frontSubsSpl1mCont - 20 * Math.log10(5);
      topAt5m = frontTopsSpl1mCont - 20 * Math.log10(5);
    } else {
      // En cerrado a 5m
      subAt5m = frontSubsSpl1mCont - 10 * Math.log10(5) - 3;
      topAt5m = frontTopsSpl1mCont - 12;
    }

    const subToTopRatio = Number((subAt5m - topAt5m).toFixed(1));

    let tonalStatus: 'OPTIMAL' | 'SUB_DEFICIT' | 'SUB_EXCESS' = 'OPTIMAL';
    if (subToTopRatio < 6.0) tonalStatus = 'SUB_DEFICIT';
    else if (subToTopRatio > 14.0) tonalStatus = 'SUB_EXCESS';

    // 9. Dimensionamiento Eléctrico
    const totalAudioRms = totalTopPowerRms + totalSubPowerRms;
    const realAudioWatts = (totalAudioRms * this.DUTY_CYCLE) / this.AMP_EFFICIENCY;
    const totalActiveWatts = realAudioWatts + auxiliaryLoadsWatts;
    const apparentPowerVa = totalActiveWatts / this.POWER_FACTOR;
    const generatorKva = (apparentPowerVa / 1000) * this.GENERATOR_SAFETY;
    const nominalAmps220V = totalActiveWatts / (220 * this.POWER_FACTOR);

    return {
      frontSystem: {
        spl1mPeak: Number(frontTopsSpl1mPeak.toFixed(1)),
        spl1mContinuous: Number(frontTopsSpl1mCont.toFixed(1)),
        splAtDistances,
        reverberationTimeRt60Seconds: rt60 ? Number(rt60.toFixed(2)) : undefined,
        roomConstantR: isIndoor ? Number(roomConstantR.toFixed(1)) : undefined,
      },
      delayLineRecommendation: {
        required: delayRequired,
        triggerDistanceM: Number(triggerDistance.toFixed(2)),
        delayTimeMs: Number(baseDelayMs.toFixed(2)),
        haasCompensationMs,
        totalDelayMs: Number(totalDelayMs.toFixed(2)),
        notes: delayNotes,
      },
      tonalBalance: {
        subToTopRatioDb: subToTopRatio,
        status: tonalStatus,
        boundaryGainAppliedDb: boundaryGainDb,
      },
      electricalRequirements: {
        realAudioConsumptionWatts: Math.round(realAudioWatts),
        totalActivePowerWatts: Math.round(totalActiveWatts),
        apparentPowerVa: Math.round(apparentPowerVa),
        minimumGeneratorKva: Number(generatorKva.toFixed(2)),
        nominalCurrentAmperes220V: Number(nominalAmps220V.toFixed(2)),
      },
    };
  }
}

// ============================================================================
// VALIDADOR DE SUMINISTRO ELÉCTRICO REAL (ENCHUFE DOMICILIARIO VS GENERADOR)
// Y AUDITORÍA DE LOS 5 PILARES CRÍTICOS DE TERRENO (HPF, SPLAY, FASE, VDROP, TIERRA)
// ============================================================================

export type PowerSourceCategory = 'HOME_OUTLET' | 'GENERATOR';
export type VolumeDriveRegime = 'MODERATE_1_8' | 'STANDARD_CLUB_1_5' | 'MAX_TECHNO_1_3';

export interface PowerSourceInput {
  type: PowerSourceCategory;
  // Si es enchufe domiciliario:
  breakerAmps?: 10 | 16 | 20 | 25 | 32;
  voltage?: number;
  // Si es generador (el cliente puede ingresar "3500" Watts comerciales o kVA):
  generatorRunningWatts?: number;
  generatorSurgeWatts?: number;
}

export interface ElectricalFeasibilityOutput {
  status: 'SAFE' | 'WARNING_OVERLOAD_RISK' | 'CRITICAL_TRIP_GUARANTEED';
  nominalSourceWatts: number;
  availableContinuousWatts: number;
  totalSystemDemandWatts: number;
  transientPeakWatts: number;
  loadPercentage: number;
  headroomPercentage: number;
  maxRecommendedGainDb: number;
  technicalDiagnosis: string;
}

export class PowerSourceValidator {
  private static readonly CONTINUOUS_SAFETY_MARGIN_GRID = 0.80; // 80% norma térmica disyuntores
  private static readonly CONTINUOUS_SAFETY_MARGIN_GEN = 0.72;  // 72% margen dinámico AVR ante bombos

  public static evaluate(
    totalDemandWatts: number,
    source: PowerSourceInput,
    transientPeakWatts = Math.round(totalDemandWatts * 2.1)
  ): ElectricalFeasibilityOutput {
    let nominalWatts = 0;
    let continuousCapacity = 0;
    const voltage = source.voltage || 220;

    if (source.type === 'HOME_OUTLET') {
      const amps = source.breakerAmps || 10;
      nominalWatts = voltage * amps;
      continuousCapacity = nominalWatts * this.CONTINUOUS_SAFETY_MARGIN_GRID;
    } else {
      // Un generador comercial "3500W" suele indicar Starting/Surge Watts (~85% Running Watts = 2975W)
      const surgeW = source.generatorSurgeWatts || 3500;
      const runningWatts = source.generatorRunningWatts || Math.round(surgeW * 0.85);
      nominalWatts = runningWatts;
      continuousCapacity = runningWatts * this.CONTINUOUS_SAFETY_MARGIN_GEN;
    }

    const loadRatio = totalDemandWatts / Math.max(1, continuousCapacity);
    const loadPct = Number((loadRatio * 100).toFixed(1));
    const headroomPct = Number(((1 - loadRatio) * 100).toFixed(1));

    if (loadRatio <= 0.85) {
      return {
        status: 'SAFE',
        nominalSourceWatts: Math.round(nominalWatts),
        availableContinuousWatts: Math.round(continuousCapacity),
        totalSystemDemandWatts: Math.round(totalDemandWatts),
        transientPeakWatts,
        loadPercentage: loadPct,
        headroomPercentage: headroomPct,
        maxRecommendedGainDb: 0,
        technicalDiagnosis: `Suministro óptimo (${loadPct}% de la capacidad continua segura de ${Math.round(continuousCapacity)} W). Margen libre del ${headroomPct}% para absorber los golpes del bombo sin caídas de tensión ni disparo térmico.`,
      };
    } else if (loadRatio <= 1.05) {
      return {
        status: 'WARNING_OVERLOAD_RISK',
        nominalSourceWatts: Math.round(nominalWatts),
        availableContinuousWatts: Math.round(continuousCapacity),
        totalSystemDemandWatts: Math.round(totalDemandWatts),
        transientPeakWatts,
        loadPercentage: loadPct,
        headroomPercentage: headroomPct,
        maxRecommendedGainDb: -3,
        technicalDiagnosis:
          source.type === 'GENERATOR'
            ? `Generador al límite (${loadPct}% de los ${Math.round(continuousCapacity)} W seguros para audio). En los drops de Techno, el regulador AVR puede sufrir caídas bajo 195V y apagar las cajas. Mantén las cajas en 0 dB Unity (12:00) o escala a un generador de ≥ 5.000 W (5 kVA).`
            : `Enchufe al límite térmico (${loadPct}% de los ${Math.round(continuousCapacity)} W continuos seguros). Aunque el automático Curva C soporta los picos del bombo, tras 35–45 minutos al máximo puede calentarse y saltar. Se sugiere atenuar -3 dB o pasar a un circuito de 16A.`,
      };
    } else {
      return {
        status: 'CRITICAL_TRIP_GUARANTEED',
        nominalSourceWatts: Math.round(nominalWatts),
        availableContinuousWatts: Math.round(continuousCapacity),
        totalSystemDemandWatts: Math.round(totalDemandWatts),
        transientPeakWatts,
        loadPercentage: loadPct,
        headroomPercentage: headroomPct,
        maxRecommendedGainDb: -6,
        technicalDiagnosis:
          source.type === 'GENERATOR'
            ? `Suministro insuficiente: el sistema exige ${Math.round(totalDemandWatts)} W continuos (con picos de ${transientPeakWatts} W) y el generador solo entrega ${Math.round(continuousCapacity)} W estables para audio. El motor se frenará en el drop y las cajas se apagarán por bajo voltaje (undervoltage).`
            : `Sobrecarga garantizada: el sistema exige ${Math.round(totalDemandWatts)} W y supera el límite seguro de ${Math.round(continuousCapacity)} W del automático. El disyuntor saltará dejando el evento a oscuras. Separa líneas o usa un empalme de mayor amperaje.`,
      };
    }
  }
}

export interface FieldEngineeringAudit {
  // 1. Crossover / Filtro Pasa-Altos (HPF)
  hpfCutoffHz: number;
  hpfPowerSavedPct: number;
  hpfDirective: string;
  // 2. Dispersión Horizontal y Ángulo de Apertura (Splay Angle)
  recommendedSplayAngleDeg: number;
  splayDirective: string;
  // 3. Alineación Temporal Sub vs. Top en Escenario (Phase Alignment)
  frontTopsMicroDelayMs: number;
  phaseAlignmentDirective: string;
  // 4. Caída de Tensión en Cable (Continua y en Pico del Drop)
  recommendedCableMm2: 1.5 | 2.5 | 4.0 | 6.0;
  voltageDropContinuousV: number;
  voltageDropTransientPeakV: number;
  voltageAtBoxDuringDropV: number;
  voltageDropIf15Mm2V: number;
  cableVoltageDirective: string;
  // 5. Puesta a Tierra y Compresión Térmica (Power Compression)
  requiresCopperweldGroundRod: boolean;
  groundingDirective: string;
  estimatedPowerCompressionDb: number;
  powerCompressionDirective: string;
  // 6. Autonomía de Combustible del Generador (Litros de Bencina / Bidones 20L)
  fuelLogistics: {
    applies: boolean;
    eventHoursWithSoundcheck: number;
    litersPerHour: number;
    totalLitersRequired: number;
    jerrycans20LCount: number;
    fuelDirective: string;
  };
  // 7. Comparador Acústico: Prueba de Sonido (Vacío) vs. Pista Llena (Aforo Humano)
  crowdAcousticShift: {
    estimatedCrowdCapacity: number;
    rt60ReductionPct: number;
    temperatureRiseCelsius: number;
    soundSpeedShiftMs: number;
    crowdDirective: string;
  };
}

export function evaluateFieldEngineering(params: {
  venueWidthM: number;
  venueDepthM: number;
  electricalDistanceM: number;
  continuousCurrentAmps: number;
  isGenerator: boolean;
  isOutdoor: boolean;
  subsCount: number;
  driveRegime?: VolumeDriveRegime;
  eventDurationHours?: number;
}): FieldEngineeringAudit {
  const {
    venueWidthM,
    venueDepthM,
    electricalDistanceM,
    continuousCurrentAmps,
    isGenerator,
    isOutdoor,
    subsCount,
    driveRegime = 'MAX_TECHNO_1_3',
    eventDurationHours = 7,
  } = params;

  // 1. Crossover HPF en Tops
  const hpfCutoffHz = subsCount > 0 ? 85 : 55;
  const hpfPowerSavedPct = subsCount > 0 ? 40 : 15;
  const hpfDirective =
    subsCount > 0
      ? `Activar filtro HPF a 80–90 Hz en todas las cajas acústicas (Tops). Ahorra ~40% de potencia eléctrica en los tops y evita que sus conos cancelen el golpe de los subwoofers.`
      : `Sin subwoofers dedicados: activar filtro HPF de seguridad a 50–55 Hz en las cajas para evitar excursión mecánica excesiva de la bobina.`;

  // 2. Ángulo de Apertura (Splay Angle) para difusores de 90°x60° sin filtro de peine central
  const targetDist = Math.max(4, venueDepthM * 0.55);
  const rawAngleDeg = Math.round((Math.atan((venueWidthM * 0.35) / targetDist) * 180) / Math.PI);
  const recommendedSplayAngleDeg = Math.min(25, Math.max(10, rawAngleDeg));
  const splayDirective = `No apuntar las cajas A y B rectas en paralelo (provoca filtro de peine al centro). Girar cada caja ${recommendedSplayAngleDeg}° respecto al eje para cruzar los bordes de -6 dB limpiamente.`;

  // 3. Alineación Temporal Sub vs. Top en Escenario (Group Delay del Subwoofer)
  const frontTopsMicroDelayMs = subsCount > 0 ? 3.5 : 0;
  const phaseAlignmentDirective =
    subsCount > 0
      ? `Aplicar micro-retardo de +3.5 ms (2 a 5 ms) a las cajas frontales A y B en el DSP para alinearlas con el retardo interno del filtro de los subwoofers y lograr golpe físico en el pecho.`
      : `Sistema sin subwoofers: cajas frontales A y B operan en 0.0 ms.`;

  // 4. Caída de Tensión en Cable (Fórmula física: dV = 2 * I * rho * L / S, con rho = 0.0178)
  const rho = 0.0178;
  let recommendedCableMm2: 1.5 | 2.5 | 4.0 | 6.0 = 2.5;
  if (electricalDistanceM > 35 || continuousCurrentAmps > 16) {
    recommendedCableMm2 = 4.0;
  }
  if (electricalDistanceM > 55 || continuousCurrentAmps > 24) {
    recommendedCableMm2 = 6.0;
  }

  const voltageDropContinuousV = Number(
    ((2 * continuousCurrentAmps * rho * electricalDistanceM) / recommendedCableMm2).toFixed(1)
  );
  // En el pico del drop (bombo + bajo), la corriente transitoria duplica el promedio continuo
  const transientPeakAmps = continuousCurrentAmps * 2.0;
  const voltageDropTransientPeakV = Number(
    ((2 * transientPeakAmps * rho * electricalDistanceM) / recommendedCableMm2).toFixed(1)
  );
  const voltageAtBoxDuringDropV = Number((220 - voltageDropTransientPeakV).toFixed(1));

  // Comparación si el usuario cometiera el error de usar un alargador doméstico de 1.5 mm²
  const voltageDropIf15Mm2V = Number(
    ((2 * transientPeakAmps * rho * electricalDistanceM) / 1.5).toFixed(1)
  );

  const cableVoltageDirective = `A ${electricalDistanceM}m de distancia, exigir alargador industrial de mínimo ${recommendedCableMm2} mm² (caída en pico de drop: -${voltageDropTransientPeakV}V -> llegan ${voltageAtBoxDuringDropV}V reales). PROHIBIDO usar cable doméstico de 1.5 mm² (caería -${voltageDropIf15Mm2V}V en los drops, dejando las cajas en ${Number((220 - voltageDropIf15Mm2V).toFixed(0))}V y provocando apagados por bajo voltaje).`;

  // 5. Puesta a Tierra (Copperweld) y Compresión Térmica (Power Compression)
  const requiresCopperweldGroundRod = isGenerator || isOutdoor;
  const groundingDirective = requiresCopperweldGroundRod
    ? `OBLIGATORIO en parcela/generador: Clavar barra de cobre (jabalina Copperweld) a tierra conectada al chasis del generador. Evita tierra flotante, descargas eléctricas por rocío nocturno en trípodes/cabina y elimina el zumbido de 50 Hz (Ground Hum) en los cables XLR.`
    : `Recinto interior: Conectar toda la cadena de audio e iluminación a la misma fase y tierra física del tablero para evitar bucles de masa (zumbido de 50 Hz en XLR).`;

  const estimatedPowerCompressionDb =
    driveRegime === 'MAX_TECHNO_1_3' ? 3.2 : driveRegime === 'STANDARD_CLUB_1_5' ? 1.4 : 0.4;
  const powerCompressionDirective =
    driveRegime === 'MAX_TECHNO_1_3'
      ? `Alerta de Compresión Térmica (-${estimatedPowerCompressionDb} dB): El 97% de la energía eléctrica se disipa como calor en la bobina (150–220 °C). Exigir las cajas al tope triplica el consumo en Watts pero pierde ~3 dB por calentamiento del cobre. Mejor sumar cajas de Delay que forzar ganancias.`
      : `Régimen térmico saludable (-${estimatedPowerCompressionDb} dB de compresión): las bobinas operan frescas con máxima eficiencia electroacústica.`;

  // 6. Logística de Combustible para Generador (Horas de Fiesta + 1.5h Prueba de Sonido)
  const eventHoursWithSoundcheck = Number((eventDurationHours + 1.5).toFixed(1));
  const activeKw = (continuousCurrentAmps * 220 * 0.92) / 1000;
  // Un generador a gasolina consume ~0.65 L/h en vacío + ~0.48 L por cada kW activo
  const litersPerHour = isGenerator ? Number((0.65 + activeKw * 0.48).toFixed(2)) : 0;
  const totalLitersRequired = isGenerator ? Math.ceil(litersPerHour * eventHoursWithSoundcheck * 1.15) : 0; // +15% reserva
  const jerrycans20LCount = isGenerator ? Math.max(1, Math.ceil(totalLitersRequired / 20)) : 0;
  const fuelDirective = isGenerator
    ? `Para ${eventDurationHours}h de fiesta (+1.5h de prueba de sonido = ${eventHoursWithSoundcheck}h), el generador consumirá ~${litersPerHour} L/hora -> Total: ${totalLitersRequired} Litros (con 15% reserva). Llevar ${jerrycans20LCount} bidón(es) certificado(s) de 20L. REGLA DE SEGURIDAD: Jamás recargar combustible con el generador encendido.`
    : `Conectado a red eléctrica fija 220V (no requiere bidones de combustible).`;

  // 7. Comparador Prueba de Sonido (Salón Vacío) vs. Pista Llena (Absorción y Calor Humano)
  const usableDancefloorM2 = venueWidthM * venueDepthM * 0.72;
  const estimatedCrowdCapacity = Math.round(usableDancefloorM2 * 2.2); // ~2.2 personas/m² en pista
  const rt60ReductionPct = isOutdoor ? 12 : 36;
  const temperatureRiseCelsius = isOutdoor ? 3 : 7;
  const soundSpeedShiftMs = Number((0.606 * temperatureRiseCelsius).toFixed(1));
  const crowdDirective = isOutdoor
    ? `Aforo estimado en pista: ~${estimatedCrowdCapacity} personas. En exterior los cuerpos absorben agudos a nivel de piso (-${rt60ReductionPct}% reflejos); mantener las cajas elevadas a 2.2m en trípode sobre las cabezas.`
    : `Aforo estimado en pista: ~${estimatedCrowdCapacity} personas. Al llenarse el salón, los cuerpos absorben el ~${rt60ReductionPct}% del eco RT60 (el sonido pasa de retumbante en la prueba de sonido a seco y definido) y el calor humano sube +${temperatureRiseCelsius} °C la sala (+${soundSpeedShiftMs} m/s en velocidad del sonido).`;

  return {
    hpfCutoffHz,
    hpfPowerSavedPct,
    hpfDirective,
    recommendedSplayAngleDeg,
    splayDirective,
    frontTopsMicroDelayMs,
    phaseAlignmentDirective,
    recommendedCableMm2,
    voltageDropContinuousV,
    voltageDropTransientPeakV,
    voltageAtBoxDuringDropV,
    voltageDropIf15Mm2V,
    cableVoltageDirective,
    requiresCopperweldGroundRod,
    groundingDirective,
    estimatedPowerCompressionDb,
    powerCompressionDirective,
    fuelLogistics: {
      applies: isGenerator,
      eventHoursWithSoundcheck,
      litersPerHour,
      totalLitersRequired,
      jerrycans20LCount,
      fuelDirective,
    },
    crowdAcousticShift: {
      estimatedCrowdCapacity,
      rt60ReductionPct,
      temperatureRiseCelsius,
      soundSpeedShiftMs,
      crowdDirective,
    },
  };
}

// ============================================================================
// INNOVACIÓN 4: DETECTOR DE CUELLO DE BOTELLA ACÚSTICO (TOP VS SUB RMS BALANCE)
// ============================================================================

export interface TopSubBottleneckAnalysis {
  totalTopRmsWatts: number;
  totalSubRmsWatts: number;
  subEnergySharePct: number;
  topEnergySharePct: number;
  status: 'OPTIMAL_CLUB_BALANCE' | 'SUB_BASS_DEFICIT' | 'NO_SUBWOOFERS' | 'TOP_HEADROOM_BOTTLENECK';
  topTrimAdjustmentDb: number;
  bottleneckDiagnosis: string;
}

export function evaluateTopToSubBalance(params: {
  totalTopRmsWatts: number;
  totalSubRmsWatts: number;
  topsCount: number;
  subsCount: number;
}): TopSubBottleneckAnalysis {
  const { totalTopRmsWatts, totalSubRmsWatts, topsCount, subsCount } = params;
  const totalRms = Math.max(1, totalTopRmsWatts + totalSubRmsWatts);
  const subEnergySharePct = Math.round((totalSubRmsWatts / totalRms) * 100);
  const topEnergySharePct = 100 - subEnergySharePct;

  if (subsCount === 0 || totalSubRmsWatts === 0) {
    return {
      totalTopRmsWatts,
      totalSubRmsWatts: 0,
      subEnergySharePct: 0,
      topEnergySharePct: 100,
      status: 'NO_SUBWOOFERS',
      topTrimAdjustmentDb: -3,
      bottleneckDiagnosis: `Sin Subwoofers Dedicados (${totalTopRmsWatts}W RMS solo en cajas superiores): Para evitar romper los conos intentando reproducir sub-graves, activa el filtro HPF en 55 Hz y no fuerces el EQ Low en la mixer.`,
    };
  }

  // En música electrónica / eventos de baile, los graves exigen entre 50% y 72% de la potencia RMS total
  if (subEnergySharePct < 45) {
    // Cuántos dB atenuar las cajas superiores para que no tapen al subwoofer ni lo obliguen a clipear
    const idealTopRms = totalSubRmsWatts * 0.85;
    const trimDb = Number(Math.max(-9, Math.min(-1.5, 10 * Math.log10(idealTopRms / Math.max(1, totalTopRmsWatts)))).toFixed(1));
    return {
      totalTopRmsWatts,
      totalSubRmsWatts,
      subEnergySharePct,
      topEnergySharePct,
      status: 'SUB_BASS_DEFICIT',
      topTrimAdjustmentDb: trimDb,
      bottleneckDiagnosis: `Cuello de Botella en Sub-Graves (${subEnergySharePct}% Sub vs ${topEnergySharePct}% Tops): Tienes mucha potencia en cajas agudas (${totalTopRmsWatts}W RMS) para pocos subwoofers (${totalSubRmsWatts}W RMS). Atenúa las perillas traseras de las cajas superiores en ${trimDb} dB para emparejar el cuerpo del bajo sin quemar el subwoofer.`,
    };
  }

  if (subEnergySharePct > 75 && topsCount <= 2) {
    return {
      totalTopRmsWatts,
      totalSubRmsWatts,
      subEnergySharePct,
      topEnergySharePct,
      status: 'TOP_HEADROOM_BOTTLENECK',
      topTrimAdjustmentDb: 0,
      bottleneckDiagnosis: `Exceso de Sub-Graves frente a Cajas Superiores (${subEnergySharePct}% Sub vs ${topEnergySharePct}% Tops): Los ${totalSubRmsWatts}W RMS de bajos pueden enterrar las voces y sintetizadores de tus cajas (${totalTopRmsWatts}W RMS). Mantén el corte HPF de las cajas en 90 Hz y modera el envío de Sub en -2 dB.`,
    };
  }

  return {
    totalTopRmsWatts,
    totalSubRmsWatts,
    subEnergySharePct,
    topEnergySharePct,
    status: 'OPTIMAL_CLUB_BALANCE',
    topTrimAdjustmentDb: 0,
    bottleneckDiagnosis: `Equilibrio Electroacústico Ideal (${subEnergySharePct}% Sub-Bajos / ${topEnergySharePct}% Tops): La proporción entre tus ${totalSubRmsWatts}W RMS de subgraves y ${totalTopRmsWatts}W RMS de medios-agudos entrega pegada física en el pecho y definición cristalina con todas las ganancias en 0 dB Unity.`,
  };
}

// ============================================================================
// INNOVACIÓN 5: SIMULADOR DE RUIDO EXTERIOR Y ORDENANZA MUNICIPAL (D.S. N° 38 MMA CHILE)
// ============================================================================

export type VenueEnclosureWallType = 'OPEN_AIR' | 'TENT_CANVAS' | 'METAL_WAREHOUSE' | 'BRICK_CONCRETE_CLOSED';
export type EventScheduleShift = 'DAYTIME_07_21' | 'NIGHTTIME_21_07';

export interface NeighborhoodNoiseAudit {
  neighborDistanceM: number;
  enclosureType: VenueEnclosureWallType;
  scheduleShift: EventScheduleShift;
  wallIsolationDb: number;
  distanceAttenuationDb: number;
  estimatedNeighborDba: number;
  legalLimitDba: number;
  excessDba: number;
  status: 'COMPLIANT_SAFE' | 'BORDERLINE_CAUTION' | 'HIGH_RISK_MUNICIPAL_FINE';
  mitigationDirective: string;
}

export function evaluateNeighborhoodNoise(params: {
  spl1mContinuousDba: number;
  neighborDistanceM: number;
  enclosureType: VenueEnclosureWallType;
  scheduleShift: EventScheduleShift;
}): NeighborhoodNoiseAudit {
  const { spl1mContinuousDba, neighborDistanceM, enclosureType, scheduleShift } = params;
  const safeDist = Math.max(5, neighborDistanceM);

  const wallIsolationMap: Record<VenueEnclosureWallType, number> = {
    OPEN_AIR: 0,
    TENT_CANVAS: 4,
    METAL_WAREHOUSE: 13,
    BRICK_CONCRETE_CLOSED: 25,
  };

  const wallIsolationDb = wallIsolationMap[enclosureType] ?? 0;
  // Atenuación por divergencia geométrica (20*log10(d)) + absorción atmosférica (~0.008 dB/m)
  const distanceAttenuationDb = Number((20 * Math.log10(safeDist) + safeDist * 0.008).toFixed(1));

  // Nivel continuo equivalente proyectado hacia el receptor exterior
  const rawExteriorDba = spl1mContinuousDba - 6 - distanceAttenuationDb - wallIsolationDb;
  const estimatedNeighborDba = Math.max(32, Number(rawExteriorDba.toFixed(1)));

  // Límites referenciales D.S. N° 38 MMA (Zona II / III Residencial-Mixta en Chile)
  const legalLimitDba = scheduleShift === 'DAYTIME_07_21' ? 60 : 48;
  const excessDba = Number((estimatedNeighborDba - legalLimitDba).toFixed(1));

  if (excessDba <= 0) {
    return {
      neighborDistanceM: safeDist,
      enclosureType,
      scheduleShift,
      wallIsolationDb,
      distanceAttenuationDb,
      estimatedNeighborDba,
      legalLimitDba,
      excessDba: 0,
      status: 'COMPLIANT_SAFE',
      mitigationDirective: `Cumple Norma D.S. N° 38 MMA: A ${safeDist}m de distancia llegan ~${estimatedNeighborDba} dB(A) (bajo el límite legal de ${legalLimitDba} dB(A) en horario ${scheduleShift === 'DAYTIME_07_21' ? 'diurno' : 'nocturno'}). Operación segura sin riesgo de parte por ruidos molestos.`,
    };
  }

  if (excessDba <= 7) {
    return {
      neighborDistanceM: safeDist,
      enclosureType,
      scheduleShift,
      wallIsolationDb,
      distanceAttenuationDb,
      estimatedNeighborDba,
      legalLimitDba,
      excessDba,
      status: 'BORDERLINE_CAUTION',
      mitigationDirective: `Precaución Vecinal (+${excessDba} dB sobre norma de ${legalLimitDba} dBA a ${safeDist}m): Llegan ~${estimatedNeighborDba} dB(A) a la vivienda más cercana. Inclina las cajas en trípode -5° hacia el piso de la pista y evita apuntar los subwoofers hacia la calle o casas colindantes.`,
    };
  }

  return {
    neighborDistanceM: safeDist,
    enclosureType,
    scheduleShift,
    wallIsolationDb,
    distanceAttenuationDb,
    estimatedNeighborDba,
    legalLimitDba,
    excessDba,
    status: 'HIGH_RISK_MUNICIPAL_FINE',
    mitigationDirective: `¡RIESGO ALTO DE PARTE MUNICIPAL (+${excessDba} dB sobre límite de ${legalLimitDba} dBA)! A ${safeDist}m llegan ~${estimatedNeighborDba} dB(A). La onda sub-grave atraviesa cierres livianos. Recomendación: rotar el escenario 90°–180° de espaldas a los vecinos, usar más cajas de Delay a menor volumen y atenuar sub-bajos -4 dB después de las 01:00 AM.`,
  };
}
