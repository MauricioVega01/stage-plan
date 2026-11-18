// ======================================================================
// CALC-ENGINE: LIGHTING, FX (FOG/LASER) & PHYSICAL DMX CABLING MODULE
// STAGE PLAN v4.1 — HU06 / CU-05 (DISTORSIONCL SPA)
// Enfoque 100% montaje físico: Watts reales, Línea 3 térmica (humo),
// trazado de cables DMX desde DMX OUT (Cabina), largos y conectores.
// ======================================================================

export type LightingFixtureType =
  | 'PAR_LED'
  | 'LED_BAR'
  | 'MOVING_HEAD'
  | 'LASER'
  | 'STROBE'
  | 'FOG_MACHINE'
  | 'HAZER';

export type LightingMountZone =
  | 'TRUSS_LEFT'
  | 'CENTER_BOOTH'
  | 'TRUSS_RIGHT'
  | 'FLOOR';

export type DmxConnectorType = 'DMX_3PIN' | 'DMX_5PIN' | 'NONE';

export interface LightingBatchInput {
  id: string;
  name: string;
  fixtureType: LightingFixtureType;
  quantity: number;
  nominalWatts: number;
  zone: LightingMountZone;
  dmxConnector: DmxConnectorType;
  unitWeightKg: number;
  isThermalLoad?: boolean;
}

export interface LightingPreset {
  key: string;
  name: string;
  fixtureType: LightingFixtureType;
  nominalWatts: number;
  dmxConnector: DmxConnectorType;
  unitWeightKg: number;
  isThermalLoad: boolean;
  defaultZone: LightingMountZone;
  shortNote: string;
}

export const LIGHTING_PRESETS: LightingPreset[] = [
  {
    key: 'par_led',
    name: 'Foco PAR LED (54x3W / 18x12W)',
    fixtureType: 'PAR_LED',
    nominalWatts: 120,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 2.5,
    isThermalLoad: false,
    defaultZone: 'TRUSS_LEFT',
    shortNote: 'Baño de color pista · Bajo consumo',
  },
  {
    key: 'led_bar',
    name: 'Barra LED Wash / Pixel',
    fixtureType: 'LED_BAR',
    nominalWatts: 160,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 3.8,
    isThermalLoad: false,
    defaultZone: 'CENTER_BOOTH',
    shortNote: 'Alineación frontal en cabina o truss',
  },
  {
    key: 'moving_beam',
    name: 'Cabeza Móvil Beam 7R (230W)',
    fixtureType: 'MOVING_HEAD',
    nominalWatts: 320,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 16,
    isThermalLoad: false,
    defaultZone: 'TRUSS_RIGHT',
    shortNote: 'Haz concentrado · Requiere clamp y piola',
  },
  {
    key: 'moving_spot',
    name: 'Cabeza Móvil Spot LED 150W',
    fixtureType: 'MOVING_HEAD',
    nominalWatts: 200,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 11,
    isThermalLoad: false,
    defaultZone: 'TRUSS_LEFT',
    shortNote: 'Gobos y barridos dinámicos',
  },
  {
    key: 'laser_rgb',
    name: 'Láser RGB 2W (ILDA/DMX)',
    fixtureType: 'LASER',
    nominalWatts: 75,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 4.5,
    isThermalLoad: false,
    defaultZone: 'CENTER_BOOTH',
    shortNote: 'Seguridad ocular: montar >= 2.7m sobre pista',
  },
  {
    key: 'strobe_blinder',
    name: 'Estrobo LED / Blinder',
    fixtureType: 'STROBE',
    nominalWatts: 400,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 5.5,
    isThermalLoad: false,
    defaultZone: 'CENTER_BOOTH',
    shortNote: 'Picos rápidos de destello',
  },
  {
    key: 'fog_1500',
    name: 'Máquina de Humo 1500W',
    fixtureType: 'FOG_MACHINE',
    nominalWatts: 1500,
    dmxConnector: 'NONE',
    unitWeightKg: 7.5,
    isThermalLoad: true,
    defaultZone: 'FLOOR',
    shortNote: 'Carga térmica crítica: SIEMPRE en Línea 3 separada del audio',
  },
  {
    key: 'hazer_900',
    name: 'Hazer / Niebla Continua 900W',
    fixtureType: 'HAZER',
    nominalWatts: 900,
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 6.5,
    isThermalLoad: true,
    defaultZone: 'FLOOR',
    shortNote: 'Resistencia térmica: separar de la línea de audio',
  },
];

export interface DmxCableRun {
  id: string;
  from: string;
  to: string;
  zone: LightingMountZone;
  kind: 'TRUNK' | 'LINK';
  lengthMeters: number;
  connector: 'DMX_3PIN' | 'DMX_5PIN';
}

export interface DmxCableSummaryItem {
  connector: 'DMX_3PIN' | 'DMX_5PIN';
  lengthMeters: number;
  quantity: number;
  kindSummary: string;
  description: string;
}

export interface LightingZoneSummary {
  zone: LightingMountZone;
  zoneLabel: string;
  fixtureCount: number;
  dmxCount: number;
  totalWatts: number;
  hasThermalLoad: boolean;
  fixtureNames: string[];
}

export interface LightingAndDmxAnalysis {
  totalFixtureUnits: number;
  dmxControlledUnits: number;
  totalLightingWatts: number;
  thermalEffectsWatts: number;
  nonThermalLightingWatts: number;
  totalLightingAmps220v: number;
  totalWeightKg: number;
  requiresDedicatedLine3: boolean;
  hasLaserUnit: boolean;
  hasThermalLoad: boolean;
  zones: LightingZoneSummary[];
  dmxRuns: DmxCableRun[];
  dmxCableInventory: DmxCableSummaryItem[];
  totalDmxCablesCount: number;
  totalDmxMeters: number;
  recommendedSpareDmxCables: number;
  needs3To5PinAdapter: boolean;
  needsDmxSplitter: boolean;
  terminators120OhmCount: number;
  alerts: string[];
  recommendations: string[];
}

const ZONE_LABELS: Record<LightingMountZone, string> = {
  TRUSS_LEFT: 'Trípode / Truss Izquierdo',
  CENTER_BOOTH: 'Frente / Cabina DJ',
  TRUSS_RIGHT: 'Trípode / Truss Derecho',
  FLOOR: 'Piso (Humo / Efectos)',
};

/**
 * Redondea largos físicos DMX a medidas reales de bodega/arriendo:
 * 1.5m (puente truss), 3m, 5m, 10m, 15m, 20m, 30m.
 */
export function roundToStandardDmxLength(meters: number): number {
  if (meters <= 1.5) return 1.5;
  if (meters <= 3) return 3;
  if (meters <= 5) return 5;
  if (meters <= 10) return 10;
  if (meters <= 15) return 15;
  if (meters <= 20) return 20;
  return Math.ceil(meters / 10) * 10;
}

/**
 * Calcula consumo eléctrico real de iluminación/efectos (humo, láser, cabezas móviles, PAR),
 * separación de Línea 3 térmica y cubicación física exacta de cables DMX tomando DMX OUT
 * en la Cabina DJ como punto de partida.
 */
export function calculateLightingAndDmxRig(
  batches: LightingBatchInput[],
  venueWidthMeters: number,
  venueDepthMeters: number,
  voltage: number = 220
): LightingAndDmxAnalysis {
  const validBatches = (batches || []).filter((b) => b.quantity > 0 && b.nominalWatts > 0);

  if (validBatches.length === 0) {
    return {
      totalFixtureUnits: 0,
      dmxControlledUnits: 0,
      totalLightingWatts: 0,
      thermalEffectsWatts: 0,
      nonThermalLightingWatts: 0,
      totalLightingAmps220v: 0,
      totalWeightKg: 0,
      requiresDedicatedLine3: false,
      hasLaserUnit: false,
      hasThermalLoad: false,
      zones: [],
      dmxRuns: [],
      dmxCableInventory: [],
      totalDmxCablesCount: 0,
      totalDmxMeters: 0,
      recommendedSpareDmxCables: 0,
      needs3To5PinAdapter: false,
      needsDmxSplitter: false,
      terminators120OhmCount: 0,
      alerts: [],
      recommendations: [
        'Sin iluminación ni efectos activos: el consumo eléctrico se asigna 100% a Audio (L1 Subs + L2 Tops/Cabina).',
      ],
    };
  }

  const width = Math.max(4, venueWidthMeters || 10);
  const depth = Math.max(6, venueDepthMeters || 14);

  let totalFixtureUnits = 0;
  let dmxControlledUnits = 0;
  let totalLightingWatts = 0;
  let thermalEffectsWatts = 0;
  let totalWeightKg = 0;
  let hasLaserUnit = false;
  let hasThermalLoad = false;
  let has3Pin = false;
  let has5Pin = false;

  const zoneMap = new Map<
    LightingMountZone,
    {
      fixtureCount: number;
      dmxItems: Array<{ label: string; connector: 'DMX_3PIN' | 'DMX_5PIN' }>;
      totalWatts: number;
      hasThermalLoad: boolean;
      fixtureNames: string[];
    }
  >();

  for (const batch of validBatches) {
    const isThermal =
      batch.isThermalLoad === true ||
      batch.fixtureType === 'FOG_MACHINE' ||
      batch.fixtureType === 'HAZER';
    const batchWatts = batch.nominalWatts * batch.quantity;

    totalFixtureUnits += batch.quantity;
    totalLightingWatts += batchWatts;
    totalWeightKg += (batch.unitWeightKg || 0) * batch.quantity;

    if (isThermal) {
      thermalEffectsWatts += batchWatts;
      hasThermalLoad = true;
    }
    if (batch.fixtureType === 'LASER') {
      hasLaserUnit = true;
    }

    if (!zoneMap.has(batch.zone)) {
      zoneMap.set(batch.zone, {
        fixtureCount: 0,
        dmxItems: [],
        totalWatts: 0,
        hasThermalLoad: false,
        fixtureNames: [],
      });
    }
    const zEntry = zoneMap.get(batch.zone)!;
    zEntry.fixtureCount += batch.quantity;
    zEntry.totalWatts += batchWatts;
    if (isThermal) zEntry.hasThermalLoad = true;
    zEntry.fixtureNames.push(`${batch.quantity}x ${batch.name}`);

    if (batch.dmxConnector !== 'NONE') {
      dmxControlledUnits += batch.quantity;
      if (batch.dmxConnector === 'DMX_3PIN') has3Pin = true;
      if (batch.dmxConnector === 'DMX_5PIN') has5Pin = true;
      for (let i = 1; i <= batch.quantity; i++) {
        zEntry.dmxItems.push({
          label: `${batch.name} #${i}`,
          connector: batch.dmxConnector,
        });
      }
    }
  }

  const nonThermalLightingWatts = Math.max(0, totalLightingWatts - thermalEffectsWatts);
  const totalLightingAmps220v = Number((totalLightingWatts / voltage).toFixed(2));
  const requiresDedicatedLine3 = hasThermalLoad || totalLightingWatts > 800;

  // Zonas ordenadas en secuencia física natural desde DMX OUT en Cabina
  const zoneOrder: LightingMountZone[] = ['CENTER_BOOTH', 'TRUSS_LEFT', 'TRUSS_RIGHT', 'FLOOR'];
  const zones: LightingZoneSummary[] = [];

  for (const z of zoneOrder) {
    const entry = zoneMap.get(z);
    if (!entry) continue;
    zones.push({
      zone: z,
      zoneLabel: ZONE_LABELS[z],
      fixtureCount: entry.fixtureCount,
      dmxCount: entry.dmxItems.length,
      totalWatts: Math.round(entry.totalWatts),
      hasThermalLoad: entry.hasThermalLoad,
      fixtureNames: entry.fixtureNames,
    });
  }

  // Distancia física desde DMX OUT (Cabina DJ al centro-frente) hacia cada zona (incluye subida a trípode + 20% holgura)
  const trunkRawMeters = (zone: LightingMountZone): number => {
    const halfWidth = width / 2;
    switch (zone) {
      case 'CENTER_BOOTH':
        return (1.8 + 2.2) * 1.2; // subida a barra/truss sobre cabina
      case 'TRUSS_LEFT':
      case 'TRUSS_RIGHT':
        return (Math.max(2.5, halfWidth - 0.8) + 2.2) * 1.2; // recorrido lateral + subida trípode 2.2m
      case 'FLOOR':
        return (Math.min(3.5, depth * 0.2) + 1.5) * 1.2; // cabina a zona piso/humo
    }
  };

  const activeDmxZones = zoneOrder.filter((z) => (zoneMap.get(z)?.dmxItems.length || 0) > 0);
  const hasBothSides =
    (zoneMap.get('TRUSS_LEFT')?.dmxItems.length || 0) > 0 &&
    (zoneMap.get('TRUSS_RIGHT')?.dmxItems.length || 0) > 0;
  const needsDmxSplitter = dmxControlledUnits > 32 || (hasBothSides && width >= 8);
  const needs3To5PinAdapter = has3Pin && has5Pin;

  // Trazado físico de cables DMX tomando DMX OUT (Cabina) como punto de partida
  const dmxRuns: DmxCableRun[] = [];
  let runSeq = 1;

  if (needsDmxSplitter) {
    // Cada zona sale como rama limpia desde el Splitter DMX en Cabina (evita cruzar pista de vuelta)
    for (const z of activeDmxZones) {
      const items = zoneMap.get(z)!.dmxItems;
      const trunkLen = roundToStandardDmxLength(trunkRawMeters(z));
      dmxRuns.push({
        id: `dmx-${runSeq++}`,
        from: 'DMX OUT / Splitter (Cabina)',
        to: `${ZONE_LABELS[z]} · ${items[0].label}`,
        zone: z,
        kind: 'TRUNK',
        lengthMeters: trunkLen,
        connector: items[0].connector,
      });

      const linkLen = z === 'FLOOR' ? 3 : 1.5;
      for (let i = 1; i < items.length; i++) {
        dmxRuns.push({
          id: `dmx-${runSeq++}`,
          from: items[i - 1].label,
          to: items[i].label,
          zone: z,
          kind: 'LINK',
          lengthMeters: linkLen,
          connector: items[i].connector,
        });
      }
    }
  } else {
    // Cadena única (daisy-chain) desde DMX OUT recorriendo zonas activas
    let previousNode = 'DMX OUT (Cabina DJ)';
    let previousZone: LightingMountZone | null = null;

    for (const z of activeDmxZones) {
      const items = zoneMap.get(z)!.dmxItems;
      let hopMeters: number;
      if (previousZone === null) {
        hopMeters = trunkRawMeters(z);
      } else if (
        (previousZone === 'TRUSS_LEFT' && z === 'TRUSS_RIGHT') ||
        (previousZone === 'TRUSS_RIGHT' && z === 'TRUSS_LEFT')
      ) {
        // Cruce de torre a torre bajando por borde delantero (ancho completo + bajada/subida)
        hopMeters = (width + 4.4) * 1.15;
      } else {
        hopMeters = trunkRawMeters(z);
      }

      dmxRuns.push({
        id: `dmx-${runSeq++}`,
        from: previousNode,
        to: `${ZONE_LABELS[z]} · ${items[0].label}`,
        zone: z,
        kind: 'TRUNK',
        lengthMeters: roundToStandardDmxLength(hopMeters),
        connector: items[0].connector,
      });

      const linkLen = z === 'FLOOR' ? 3 : 1.5;
      for (let i = 1; i < items.length; i++) {
        dmxRuns.push({
          id: `dmx-${runSeq++}`,
          from: items[i - 1].label,
          to: items[i].label,
          zone: z,
          kind: 'LINK',
          lengthMeters: linkLen,
          connector: items[i].connector,
        });
      }

      previousNode = items[items.length - 1].label;
      previousZone = z;
    }
  }

  // Consolidar inventario de cables DMX por (conector + largo comercial)
  const invMap = new Map<
    string,
    { connector: 'DMX_3PIN' | 'DMX_5PIN'; lengthMeters: number; quantity: number; trunks: number; links: number }
  >();

  let totalDmxMeters = 0;
  for (const run of dmxRuns) {
    totalDmxMeters += run.lengthMeters;
    const key = `${run.connector}_${run.lengthMeters}`;
    if (!invMap.has(key)) {
      invMap.set(key, {
        connector: run.connector,
        lengthMeters: run.lengthMeters,
        quantity: 0,
        trunks: 0,
        links: 0,
      });
    }
    const row = invMap.get(key)!;
    row.quantity += 1;
    if (run.kind === 'TRUNK') row.trunks += 1;
    else row.links += 1;
  }

  const dmxCableInventory: DmxCableSummaryItem[] = Array.from(invMap.values())
    .sort((a, b) => b.lengthMeters - a.lengthMeters)
    .map((item) => {
      const pinText = item.connector === 'DMX_5PIN' ? '5 pines' : '3 pines';
      const kindSummary =
        item.trunks > 0 && item.links > 0
          ? `${item.trunks} troncal + ${item.links} puente`
          : item.trunks > 0
          ? 'Troncal desde cabina / cruce zona'
          : 'Puente corto entre focos (daisy-chain)';
      return {
        connector: item.connector,
        lengthMeters: item.lengthMeters,
        quantity: item.quantity,
        kindSummary,
        description: `Cable DMX 120Ω (${pinText}) de ${item.lengthMeters}m`,
      };
    });

  const totalDmxCablesCount = dmxRuns.length;
  const recommendedSpareDmxCables = totalDmxCablesCount > 0 ? Math.max(1, Math.ceil(totalDmxCablesCount * 0.15)) : 0;
  const terminators120OhmCount =
    dmxControlledUnits === 0 ? 0 : needsDmxSplitter ? activeDmxZones.length : 1;

  // Alertas y directrices operativas
  const alerts: string[] = [];
  const recommendations: string[] = [];

  if (hasThermalLoad) {
    alerts.push(
      `🔥 CARGA TÉRMICA DETECTADA (${Math.round(thermalEffectsWatts)}W en Humo/Hazer): PROHIBIDO enchufar en la zapatilla de Cabina DJ o audio. Asignar obligatoriamente a LÍNEA 3 (Iluminación/Efectos) para evitar cortes del disyuntor y zumbido (hum) en parlantes.`
    );
  }
  if (hasLaserUnit) {
    alerts.push(
      `⚠️ SEGURIDAD LÁSER: Montar el proyector láser a una altura mínima de 2.7m por encima del nivel de los ojos del público y bloquear haces directos hacia la pista.`
    );
  }
  if (needs3To5PinAdapter) {
    alerts.push(
      `🔌 CONECTORES DMX MIXTOS (3-pin y 5-pin): Debes llevar al menos 2 adaptadores DMX 3-pin ↔ 5-pin para unir la cadena sin trabas.`
    );
  }
  if (needsDmxSplitter) {
    recommendations.push(
      `🔀 SPLITTER DMX ÓPTICO RECOMENDADO: ${
        dmxControlledUnits > 32
          ? `Superas el límite físico RS-485 de 32 equipos por línea (${dmxControlledUnits} equipos).`
          : `Tienes torres Izquierda y Derecha separadas por ${width}m; un Splitter en cabina envía ramas independientes limpias sin cruzar el suelo.`
      }`
    );
  }
  if (terminators120OhmCount > 0) {
    recommendations.push(
      `🛡️ TERMINADOR DMX 120Ω: Conectar ${terminators120OhmCount} terminador(es) en la salida DMX OUT del último foco de cada rama para evitar rebotes de señal y parpadeos aleatorios.`
    );
  }
  if (totalDmxCablesCount > 0) {
    recommendations.push(
      `📦 REPUESTO DMX: Llevar ${recommendedSpareDmxCables} cable(s) DMX extra (120Ω) de 5m/10m. Evitar cables de micrófono comunes en tiradas mayores a 10m.`
    );
  }

  return {
    totalFixtureUnits,
    dmxControlledUnits,
    totalLightingWatts: Math.round(totalLightingWatts),
    thermalEffectsWatts: Math.round(thermalEffectsWatts),
    nonThermalLightingWatts: Math.round(nonThermalLightingWatts),
    totalLightingAmps220v,
    totalWeightKg: Number(totalWeightKg.toFixed(1)),
    requiresDedicatedLine3,
    hasLaserUnit,
    hasThermalLoad,
    zones,
    dmxRuns,
    dmxCableInventory,
    totalDmxCablesCount,
    totalDmxMeters: Number(totalDmxMeters.toFixed(1)),
    recommendedSpareDmxCables,
    needs3To5PinAdapter,
    needsDmxSplitter,
    terminators120OhmCount,
    alerts,
    recommendations,
  };
}
