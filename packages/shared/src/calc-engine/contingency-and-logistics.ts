// ======================================================================
// CALC-ENGINE: CONTINGENCY PLAN ("PLAN B EN VIVO") & LOAD LOGISTICS
// STAGE PLAN v4.1 — HU08 / CU-07 y HU09 / CU-08 (DISTORSIONCL SPA)
// Incluye Ley N° 20.949 de Chile ("Ley del Saco": máx. 25 kg carga manual)
// ======================================================================

export type ContingencyScenario =
  | 'GENERATOR_FAIL_TO_10A'
  | 'TOP_BOX_FAILURE'
  | 'SUB_FAILURE'
  | 'LIGHTING_BREAKER_TRIP';

export interface ContingencyContext {
  totalAudioSubsWatts: number;
  totalAudioTopsAndBoothWatts: number;
  thermalFxWatts: number; // Humo / Hazer
  lightingLedWatts: number;
  topsCount: number;
  subsCount: number;
  hasPassiveSpeakers: boolean;
}

export interface ContingencyStep {
  order: number;
  action: string;
  wattsSaved?: number;
  reason: string;
}

export interface ContingencyPlanResult {
  scenario: ContingencyScenario;
  title: string;
  severity: 'WARNING' | 'CRITICAL';
  targetSafeWatts: number;
  initialWatts: number;
  resultingWatts: number;
  isSystemSurvivable: boolean;
  steps: ContingencyStep[];
  mixerDirective: string;
  recoverySummary: string;
}

const SAFE_10A_OUTLET_WATTS = 1760;

/**
 * Simula una falla crítica en pleno evento y entrega un protocolo determinista
 * paso a paso (< 2 minutos) para mantener la música viva sin quemar equipos.
 */
export function simulateContingencyPlan(
  scenario: ContingencyScenario,
  ctx: ContingencyContext
): ContingencyPlanResult {
  const initialWatts = Math.round(
    ctx.totalAudioSubsWatts + ctx.totalAudioTopsAndBoothWatts + ctx.thermalFxWatts + ctx.lightingLedWatts
  );

  if (scenario === 'GENERATOR_FAIL_TO_10A') {
    let remaining = initialWatts;
    const steps: ContingencyStep[] = [];
    let stepNum = 1;

    if (ctx.thermalFxWatts > 0) {
      remaining -= ctx.thermalFxWatts;
      steps.push({
        order: stepNum++,
        action: 'Desconectar inmediatamente Máquina de Humo / Hazer (Línea 3 Térmica).',
        wattsSaved: Math.round(ctx.thermalFxWatts),
        reason: 'Es la mayor carga resistiva prescindible y no afecta la música.',
      });
    }

    if (remaining > SAFE_10A_OUTLET_WATTS && ctx.lightingLedWatts > 0) {
      remaining -= ctx.lightingLedWatts;
      steps.push({
        order: stepNum++,
        action: 'Apagar cabezas móviles / estrobos y dejar solo 1–2 PAR LED ambientales (o 0W luces).',
        wattsSaved: Math.round(ctx.lightingLedWatts),
        reason: 'Libera corriente de inmediato para priorizar PA y Cabina DJ.',
      });
    }

    if (remaining > SAFE_10A_OUTLET_WATTS && ctx.totalAudioSubsWatts > 0) {
      const subReduction = Math.round(ctx.totalAudioSubsWatts * 0.5);
      remaining -= subReduction;
      steps.push({
        order: stepNum++,
        action: 'Dejar solo 1 subwoofer activo (o bajar ganancia de sub-bajos en -6 dB).',
        wattsSaved: subReduction,
        reason: 'Los golpes de sub-graves disparan el térmico de 10A en el drop.',
      });
    }

    steps.push({
      order: stepNum++,
      action: 'Reconectar Cabina DJ + PA esencial al enchufe domiciliario de 10A con alargador de 2.5 mm² desenrollado.',
      reason: 'Evita caída de tensión y permite operar continuo bajo 1.760W (80% SEC).',
    });

    const isSurvivable = remaining <= SAFE_10A_OUTLET_WATTS;

    return {
      scenario,
      title: 'PLAN B: Falla de Generador → Emergencia en Enchufe 10A (1.760W máx.)',
      severity: 'CRITICAL',
      targetSafeWatts: SAFE_10A_OUTLET_WATTS,
      initialWatts,
      resultingWatts: Math.max(0, Math.round(remaining)),
      isSystemSurvivable: isSurvivable,
      steps,
      mixerDirective:
        'Bajar Master del Mixer en -3 dB y aplicar HPF a 90 Hz en los Tops para minimizar picos de corriente.',
      recoverySummary: isSurvivable
        ? `Sistema estabilizado en ${Math.round(remaining)}W (bajo el límite seguro de ${SAFE_10A_OUTLET_WATTS}W en 10A). La fiesta continúa sin disparar el automático.`
        : `Incluso recortando luces y humo quedan ${Math.round(remaining)}W (>1.760W). Obligatorio conseguir un 2° enchufe de otro circuito de la casa para separar los sub-bajos.`,
    };
  }

  if (scenario === 'TOP_BOX_FAILURE') {
    const remainingTops = Math.max(0, ctx.topsCount - 1);
    const hasDelayToPromote = ctx.topsCount >= 3;
    const steps: ContingencyStep[] = [
      {
        order: 1,
        action: 'Silenciar Master del Mixer y desconectar el cable de poder/Speakon de la caja fallada.',
        reason: 'Evita cortocircuito en el amplificador o chasquidos en la pista.',
      },
      {
        order: 2,
        action: hasDelayToPromote
          ? 'Reubicar una torre Delay operativa hacia el Frente Principal (quitar retardo ms → 0 ms).'
          : 'Conmutar la salida del Mixer a modo MONO y centrar la única caja Top operativa a 2.2m.',
        reason: hasDelayToPromote
          ? 'Recupera el estéreo frontal completo en menos de 2 minutos.'
          : 'Evita que la mitad de la pista pierda un canal (L o R) de las canciones.',
      },
      {
        order: 3,
        action: 'Mantener el nivel de ganancia en 0 dB Unity (NO subir la perilla para compensar el volumen faltante).',
        reason: 'Forzar la caja sobreviviente a +6 dB la llevará a clip y la quemará también.',
      },
    ];

    return {
      scenario,
      title: 'PLAN B: Falla de 1 Caja Top Frontal en Vivo',
      severity: remainingTops === 0 ? 'CRITICAL' : 'WARNING',
      targetSafeWatts: initialWatts,
      initialWatts,
      resultingWatts: initialWatts,
      isSystemSurvivable: remainingTops >= 1,
      steps,
      mixerDirective: hasDelayToPromote
        ? 'Restablecer Delay en 0 ms para la caja promovida al frente y verificar Gain Matching en 0 dB.'
        : 'Activar salida MONO en el Mixer DJ y mantener LEDs máximo en ámbar (+3 dB).',
      recoverySummary:
        remainingTops >= 1
          ? `Quedan ${remainingTops} caja(s) Top operativa(s). ${
              hasDelayToPromote ? 'Se promueve 1 delay al frente.' : 'Operación segura en modo MONO centrado.'
            }`
          : 'Sin cajas Top operativas disponibles; usar monitor de cabina como respaldo temporal de emergencia.',
    };
  }

  if (scenario === 'SUB_FAILURE') {
    const remainingSubs = Math.max(0, ctx.subsCount - 1);
    const steps: ContingencyStep[] = [
      {
        order: 1,
        action: 'Apagar y desconectar el subwoofer fallado (si es pasivo, desconectar su cable Speakon inmediatamente).',
        reason: 'Un parlante con bobina quemada puede caer a cortocircuito y activar PROTECT en el amplificador.',
      },
      {
        order: 2,
        action:
          remainingSubs >= 1
            ? 'Dejar el(los) subwoofer(s) restante(s) en el centro a piso y verificar impedancia >= 4Ω.'
            : 'Desactivar el filtro HPF (o bajarlo a 50–60 Hz) en las cajas Top para recuperar algo de cuerpo grave.',
        reason:
          remainingSubs >= 1
            ? 'Se pierden ~3 a 6 dB en sub-graves, pero el cluster central sigue sin cancelaciones.'
            : 'Permite continuar con rango completo en los Tops a volumen moderado.',
      },
    ];

    return {
      scenario,
      title: 'PLAN B: Falla de 1 Subwoofer en Vivo',
      severity: 'WARNING',
      targetSafeWatts: initialWatts,
      initialWatts,
      resultingWatts: initialWatts,
      isSystemSurvivable: true,
      steps,
      mixerDirective:
        remainingSubs >= 1
          ? 'No sobre-ecualizar el Low EQ del Mixer para compensar el sub perdido; proteger el cono restante.'
          : 'Reducir Master en -2 dB si los Tops pasan a rango completo sin sub-bajo.',
      recoverySummary:
        remainingSubs >= 1
          ? `Operando con ${remainingSubs} subwoofer(s) restante(s) en bloque central.`
          : 'Operando en modo Full-Range con cajas Top mientras se aísla el sub dañado.',
    };
  }

  // LIGHTING_BREAKER_TRIP
  const afterThermal = Math.max(0, initialWatts - ctx.thermalFxWatts);
  return {
    scenario,
    title: 'PLAN B: Disparo de Automático en Línea 3 (Iluminación / Humo)',
    severity: 'WARNING',
    targetSafeWatts: SAFE_10A_OUTLET_WATTS,
    initialWatts,
    resultingWatts: afterThermal,
    isSystemSurvivable: true,
    steps: [
      {
        order: 1,
        action: 'Confirmar que Audio (L1 Subs y L2 Tops/Cabina) sigue intacto y con música continua.',
        reason: 'Gracias a la separación en 3 líneas, una falla en luces/humo nunca apaga el sonido.',
      },
      {
        order: 2,
        action: 'Desenchufar la Máquina de Humo / Hazer antes de volver a subir el automático.',
        wattsSaved: Math.round(ctx.thermalFxWatts),
        reason: 'La resistencia térmica del calentador es la causa N°1 de disparos térmicos.',
      },
      {
        order: 3,
        action: 'Subir el automático y reactivar únicamente luminarias LED de bajo consumo (< 600W).',
        reason: 'Mantiene ambientación visual sin volver a sobrecargar el circuito.',
      },
    ],
    mixerDirective: 'Sin cambios en el Mixer DJ: el sistema de audio opera aislado en Líneas 1 y 2.',
    recoverySummary: `Al aislar la carga térmica (${Math.round(ctx.thermalFxWatts)}W), la iluminación LED opera con margen seguro sin interrumpir el sonido.`,
  };
}

// ======================================================================
// HU09 / CU-08: LOGÍSTICA DE CARGA, VEHÍCULO Y ERGONOMÍA (LEY DEL SACO 20.949)
// ======================================================================

export interface LogisticsItemWeight {
  name: string;
  quantity: number;
  unitWeightKg: number;
}

export interface LogisticsInput {
  items: LogisticsItemWeight[];
  extensionCordsCount: number;
  powerStripsCount: number;
  dmxCablesCount: number;
  dmxTerminatorsCount: number;
  gafferRolls50m: number;
  usesGenerator: boolean;
  has16ASockets: boolean;
}

export interface ChecklistTaskItem {
  id: string;
  stage: 'PRE_DEPARTURE' | 'ON_SITE_SETUP' | 'TEARDOWN_5AM';
  label: string;
  critical: boolean;
}

export interface LoadLogisticsResult {
  totalEquipmentWeightKg: number;
  cablingAndHardwareWeightKg: number;
  grandTotalWeightKg: number;
  leyDelSacoMaxKg: number; // 25 kg Chile (Ley 20.949)
  heavyItemsRequiringTwoPeople: LogisticsItemWeight[];
  leyDelSacoAlert: string | null;
  recommendedVehicle: 'SUV / Hatchback' | 'Camioneta Pickup' | 'Furgón Utilitario (H1 / Sprinter)';
  recommendedOperatorsCount: number;
  checklist: ChecklistTaskItem[];
}

export const CHILE_LEY_DEL_SACO_MAX_KG = 25;

/**
 * Calcula peso total de carga, alerta de ergonomía bajo Ley N° 20.949 (Chile),
 * vehículo recomendado y checklist operativo de 3 momentos (Bodega / Montaje / Retiro).
 */
export function calculateLoadLogistics(input: LogisticsInput): LoadLogisticsResult {
  let totalEquipmentWeightKg = 0;
  const heavyItemsRequiringTwoPeople: LogisticsItemWeight[] = [];

  for (const item of input.items) {
    if (item.quantity <= 0) continue;
    totalEquipmentWeightKg += item.quantity * item.unitWeightKg;
    if (item.unitWeightKg > CHILE_LEY_DEL_SACO_MAX_KG) {
      heavyItemsRequiringTwoPeople.push(item);
    }
  }

  // Peso realista de cableado y ferretería: ~2.8kg por alargador, 0.7kg por zapatilla, 0.5kg por cable DMX, 0.6kg por rollo Gaffer
  const cablingAndHardwareWeightKg =
    input.extensionCordsCount * 2.8 +
    input.powerStripsCount * 0.7 +
    input.dmxCablesCount * 0.5 +
    input.gafferRolls50m * 0.6 +
    8; // bolso de cables XLR/IEC/adaptadores/herramientas

  const grandTotalWeightKg = Number((totalEquipmentWeightKg + cablingAndHardwareWeightKg).toFixed(1));

  let recommendedVehicle: LoadLogisticsResult['recommendedVehicle'] = 'SUV / Hatchback';
  if (grandTotalWeightKg > 450) {
    recommendedVehicle = 'Furgón Utilitario (H1 / Sprinter)';
  } else if (grandTotalWeightKg > 180) {
    recommendedVehicle = 'Camioneta Pickup';
  }

  const recommendedOperatorsCount =
    heavyItemsRequiringTwoPeople.length > 0 || grandTotalWeightKg > 220 ? 2 : 1;

  const leyDelSacoAlert =
    heavyItemsRequiringTwoPeople.length > 0
      ? `⚖️ LEY DEL SACO N° 20.949 (CHILE — MÁX. 25 kg): Tienes ${heavyItemsRequiringTwoPeople.length} tipo(s) de equipo sobre 25 kg (${heavyItemsRequiringTwoPeople
          .map((i) => `${i.name}: ${i.unitWeightKg} kg`)
          .join(', ')}). Manipulación obligatoria entre mínimo 2 operadores o carro de carga.`
      : null;

  const checklist: ChecklistTaskItem[] = [
    {
      id: 'chk-pre-1',
      stage: 'PRE_DEPARTURE',
      label: `Cargar ${input.extensionCordsCount} alargador(es) + ${input.powerStripsCount} zapatilla(s) certificadas (10A/16A).`,
      critical: true,
    },
    {
      id: 'chk-pre-2',
      stage: 'PRE_DEPARTURE',
      label: `Cargar ${Math.max(1, input.gafferRolls50m)} rollo(s) de Cinta Gaffer 50m + 2 cables IEC C13 de repuesto.`,
      critical: true,
    },
    ...(input.dmxCablesCount > 0
      ? [
          {
            id: 'chk-pre-dmx',
            stage: 'PRE_DEPARTURE' as const,
            label: `Cargar ${input.dmxCablesCount} cable(s) DMX 120Ω + ${Math.max(1, input.dmxTerminatorsCount)} terminador(es) DMX 120Ω.`,
            critical: true,
          },
        ]
      : []),
    ...(input.has16ASockets
      ? [
          {
            id: 'chk-pre-adapt',
            stage: 'PRE_DEPARTURE' as const,
            label: 'Llevar 2 adaptadores certificados 16A Schuko ↔ 10A chileno.',
            critical: true,
          },
        ]
      : []),
    ...(input.usesGenerator
      ? [
          {
            id: 'chk-pre-gen',
            stage: 'PRE_DEPARTURE' as const,
            label: 'Llevar barra Copperweld (tierra física), maza, combustible de reserva y multímetro.',
            critical: true,
          },
        ]
      : []),
    {
      id: 'chk-site-1',
      stage: 'ON_SITE_SETUP',
      label: 'Desenrollar al 100% todos los alargadores y encintar cruces peatonales con Cinta Gaffer.',
      critical: true,
    },
    {
      id: 'chk-site-2',
      stage: 'ON_SITE_SETUP',
      label: 'Verificar separación física de Líneas (L1 Subs / L2 Tops+Cabina / L3 Humo-Luces) sin daisy-chain.',
      critical: true,
    },
    {
      id: 'chk-site-3',
      stage: 'ON_SITE_SETUP',
      label: 'Probar sonido con HPF 80–90 Hz en Tops y Mixer sin picos rojos antes de abrir puertas.',
      critical: false,
    },
    {
      id: 'chk-tear-1',
      stage: 'TEARDOWN_5AM',
      label: 'Apagar amplificadores y cajas ANTES de apagar el Mixer DJ (evita golpe DC en conos).',
      critical: true,
    },
    {
      id: 'chk-tear-2',
      stage: 'TEARDOWN_5AM',
      label: `Contabilizar retiro completo: ${input.extensionCordsCount} alargadores, ${input.powerStripsCount} zapatillas${
        input.dmxCablesCount > 0 ? ` y ${input.dmxCablesCount} cables DMX` : ''
      } (cero olvidos de madrugada).`,
      critical: true,
    },
  ];

  return {
    totalEquipmentWeightKg: Number(totalEquipmentWeightKg.toFixed(1)),
    cablingAndHardwareWeightKg: Number(cablingAndHardwareWeightKg.toFixed(1)),
    grandTotalWeightKg,
    leyDelSacoMaxKg: CHILE_LEY_DEL_SACO_MAX_KG,
    heavyItemsRequiringTwoPeople,
    leyDelSacoAlert,
    recommendedVehicle,
    recommendedOperatorsCount,
    checklist,
  };
}
