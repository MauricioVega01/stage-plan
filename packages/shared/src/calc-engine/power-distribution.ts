// ======================================================================
// CALC-ENGINE: POWER DISTRIBUTION, EXTENSION CORDS & POWER STRIPS (ZAPATILLAS)
// STAGE PLAN v4.1 — HU07 / CU-06 (DISTORSIONCL SPA)
// Calcula bocas exactas por zona, zapatillas 10A/16A (límite 80% SEC RIC 10),
// prohíbe daisy-chain (zapatilla sobre zapatilla) y cubica alargadores reales.
// ======================================================================

import { calculateCableSizing } from './electrical.js';
import type { EquipmentRosterConnection } from './hybrid-roster.js';
import type { LightingAndDmxAnalysis } from './lighting-dmx.js';

export type PowerLineId = 'LINE_1_SUBS' | 'LINE_2_TOPS_CTRL' | 'LINE_3_LIGHTING_FX';

export type PowerStripZone =
  | 'DJ_BOOTH'
  | 'SUB_CLUSTER'
  | 'PA_FRONT_L'
  | 'PA_FRONT_R'
  | 'DELAY_ZONE'
  | 'LIGHTING_FX';

export interface PowerStripSpec {
  id: string; // Z1, Z2, Z3...
  label: string;
  zone: PowerStripZone;
  line: PowerLineId;
  ratingAmps: 10 | 16;
  totalSockets: 4 | 6;
  usedSockets: number;
  freeSockets: number;
  connectedDevices: string[];
  loadWatts: number;
  safeMaxWatts: number; // 80% continuo SEC: 1760W (10A) o 2816W (16A)
  usagePct: number;
  status: 'OK' | 'WARNING' | 'OVERLOAD';
  plugStandard: 'CHILENO_10A' | 'SCHUKO_16A';
  surgeProtectedRecommended: boolean;
}

export interface ExtensionCordItem {
  id: string;
  from: string;
  to: string;
  zone: PowerStripZone;
  line: PowerLineId;
  lengthMeters: number;
  crossSectionMm2: number;
  ratingAmps: 10 | 16;
  loadWatts: number;
  isFloorTransit: boolean;
  label: string;
}

export interface ExtensionCordInventoryRow {
  crossSectionMm2: number;
  lengthMeters: number;
  ratingAmps: 10 | 16;
  quantity: number;
  description: string;
}

export interface PowerDistributionInput {
  venueWidthMeters: number;
  venueDepthMeters: number;
  electricalDistanceMeters: number;
  voltage?: number;
  djBoothWatts: number;
  djBoothDevices?: string[]; // Por defecto: Mixer DJ, Controladora/CDJs, Notebook, Retorno/Router
  roster: EquipmentRosterConnection[];
  externalAmpsCount: number;
  lightingAnalysis?: LightingAndDmxAnalysis;
}

export interface PowerDistributionPlan {
  powerStrips: PowerStripSpec[];
  extensionCords: ExtensionCordItem[];
  extensionCordSummary: ExtensionCordInventoryRow[];
  totalSocketsRequired: number;
  totalPowerStrips10A: number;
  totalPowerStrips16A: number;
  totalPowerStripsCount: number;
  passiveBoxesWithout220vCount: number;
  daisyChainPreventionTriggered: boolean;
  lineTotalsWatts: {
    line1Subs: number;
    line2TopsAndBooth: number;
    line3LightingAndFx: number;
    grandTotal: number;
  };
  alerts: string[];
  recommendations: string[];
}

const SAFE_WATTS_10A = 1760; // 220V * 10A * 0.80 (SEC RIC 10 continuo)
const SAFE_WATTS_16A = 2816; // 220V * 16A * 0.80 (SEC RIC 10 continuo)

/**
 * Redondea el metraje de alargador a largos comerciales reales de bodega/ferretería:
 * 5m, 10m, 15m, 20m, 25m, 30m, 40m, 50m.
 */
export function roundToCommercialExtensionLength(meters: number): number {
  const safe = Math.max(3, meters);
  if (safe <= 5) return 5;
  if (safe <= 10) return 10;
  if (safe <= 15) return 15;
  if (safe <= 20) return 20;
  if (safe <= 25) return 25;
  if (safe <= 30) return 30;
  return Math.ceil(safe / 10) * 10;
}

function makePowerStrip(
  seq: number,
  params: {
    label: string;
    zone: PowerStripZone;
    line: PowerLineId;
    devices: string[];
    loadWatts: number;
    force16A?: boolean;
    surgeProtected?: boolean;
  }
): PowerStripSpec {
  const usedSockets = params.devices.length;
  const totalSockets: 4 | 6 = usedSockets <= 3 ? 4 : 6;
  const needs16A = params.force16A === true || params.loadWatts > SAFE_WATTS_10A;
  const ratingAmps: 10 | 16 = needs16A ? 16 : 10;
  const safeMaxWatts = ratingAmps === 16 ? SAFE_WATTS_16A : SAFE_WATTS_10A;
  const usagePct = safeMaxWatts > 0 ? Math.round((params.loadWatts / safeMaxWatts) * 100) : 0;

  let status: 'OK' | 'WARNING' | 'OVERLOAD' = 'OK';
  if (params.loadWatts > safeMaxWatts || usedSockets > totalSockets) {
    status = 'OVERLOAD';
  } else if (usagePct >= 85) {
    status = 'WARNING';
  }

  return {
    id: `Z${seq}`,
    label: params.label,
    zone: params.zone,
    line: params.line,
    ratingAmps,
    totalSockets,
    usedSockets,
    freeSockets: Math.max(0, totalSockets - usedSockets),
    connectedDevices: params.devices,
    loadWatts: Math.round(params.loadWatts),
    safeMaxWatts,
    usagePct,
    status,
    plugStandard: ratingAmps === 16 ? 'SCHUKO_16A' : 'CHILENO_10A',
    surgeProtectedRecommended: params.surgeProtected ?? params.zone === 'DJ_BOOTH',
  };
}

/**
 * Planifica todas las zapatillas (bocas, amperaje, límite 80% SEC), alargadores comerciales
 * (largo y sección mm²) y evita encadenamiento inseguro (daisy-chain).
 */
export function calculatePowerDistribution(input: PowerDistributionInput): PowerDistributionPlan {
  const voltage = input.voltage ?? 220;
  const width = Math.max(4, input.venueWidthMeters || 10);
  const depth = Math.max(6, input.venueDepthMeters || 14);
  const boardDist = Math.max(2, input.electricalDistanceMeters || 10);

  const powerStrips: PowerStripSpec[] = [];
  const extensionCords: ExtensionCordItem[] = [];
  const alerts: string[] = [];
  const recommendations: string[] = [];

  let zSeq = 1;
  let extSeq = 1;
  let daisyChainPreventionTriggered = false;

  const pickSection = (watts: number, lengthMeters: number): number => {
    if (watts <= 0) return 1.5;
    const sizing = calculateCableSizing({
      powerWatts: watts,
      voltage,
      distanceMeters: lengthMeters,
      safetyMarginPct: 20,
      maxVoltageDropPct: 3.0,
    });
    return sizing.commercialCrossSectionMm2;
  };

  // Separar equipos de audio por rol físico y tipo activo/pasivo
  const passiveBoxes = input.roster.filter((r) => r.systemType === 'PASSIVE');
  const passiveBoxesWithout220vCount = passiveBoxes.length;

  const activeSubs = input.roster.filter((r) => r.category === 'sub_bass' && r.systemType === 'ACTIVE');
  const passiveSubs = input.roster.filter((r) => r.category === 'sub_bass' && r.systemType === 'PASSIVE');
  const activeFrontTops = input.roster.filter(
    (r) =>
      r.category === 'top_box' &&
      r.systemType === 'ACTIVE' &&
      (r.zone === 'PA_FRONT_L' || r.zone === 'PA_FRONT_R')
  );
  const activeDelayTops = input.roster.filter(
    (r) =>
      r.category === 'top_box' &&
      r.systemType === 'ACTIVE' &&
      (r.zone === 'DELAY_RING_1' || r.zone === 'DELAY_RING_2')
  );
  const passiveTops = input.roster.filter((r) => r.category === 'top_box' && r.systemType === 'PASSIVE');

  // ------------------------------------------------------------------
  // 1. Z1 — CABINA DJ (Línea 2: electrónica sensible con supresor de picos)
  // ------------------------------------------------------------------
  const boothDevices =
    input.djBoothDevices && input.djBoothDevices.length > 0
      ? [...input.djBoothDevices]
      : ['Mixer DJ', 'Controladora / CDJs', 'Notebook / Interfaz', 'Monitor Retorno / Router'];

  // Si hay etapas de potencia para Tops pasivos, se conectan en Rack junto a cabina (Línea 2)
  const passiveTopsWatts = passiveTops.reduce((s, r) => s + r.powerWatts220v, 0);
  const passiveTopsAmpsCount = passiveTops.length > 0 ? Math.max(1, Math.ceil(passiveTops.length / 2)) : 0;
  for (let i = 1; i <= passiveTopsAmpsCount; i++) {
    boothDevices.push(`Amplificador Tops Pasivos #${i}`);
  }

  const boothTotalWatts = Math.max(150, input.djBoothWatts || 300) + passiveTopsWatts;

  // Regla anti-daisy-chain: si excede 6 bocas en Cabina, dividir en 2 zapatillas con alimentación independiente
  if (boothDevices.length > 6) {
    daisyChainPreventionTriggered = true;
    const mid = Math.ceil(boothDevices.length / 2);
    const z1a = makePowerStrip(zSeq++, {
      label: 'Zapatilla Cabina DJ A (Electrónica)',
      zone: 'DJ_BOOTH',
      line: 'LINE_2_TOPS_CTRL',
      devices: boothDevices.slice(0, mid),
      loadWatts: boothTotalWatts * 0.5,
      surgeProtected: true,
    });
    const z1b = makePowerStrip(zSeq++, {
      label: 'Zapatilla Cabina DJ B (Rack / Aux)',
      zone: 'DJ_BOOTH',
      line: 'LINE_2_TOPS_CTRL',
      devices: boothDevices.slice(mid),
      loadWatts: boothTotalWatts * 0.5,
      surgeProtected: true,
    });
    powerStrips.push(z1a, z1b);
    alerts.push(
      `🚫 ANTI DAISY-CHAIN (SEC RIC N° 10): Cabina DJ requiere ${boothDevices.length} bocas (>6). Se dividió en ${z1a.id} y ${z1b.id} con tomas independientes; PROHIBIDO enchufar una zapatilla dentro de otra.`
    );
  } else {
    powerStrips.push(
      makePowerStrip(zSeq++, {
        label: 'Zapatilla Cabina DJ (Con Supresor)',
        zone: 'DJ_BOOTH',
        line: 'LINE_2_TOPS_CTRL',
        devices: boothDevices,
        loadWatts: boothTotalWatts,
        surgeProtected: true,
      })
    );
  }

  const boothExtLen = roundToCommercialExtensionLength((boardDist + width * 0.25) * 1.1);
  const boothExtSection = pickSection(boothTotalWatts, boothExtLen);
  extensionCords.push({
    id: `EXT-${extSeq++}`,
    from: 'Tablero 220V (L2)',
    to: 'Z1 Cabina DJ',
    zone: 'DJ_BOOTH',
    line: 'LINE_2_TOPS_CTRL',
    lengthMeters: boothExtLen,
    crossSectionMm2: boothExtSection,
    ratingAmps: boothTotalWatts > SAFE_WATTS_10A ? 16 : 10,
    loadWatts: Math.round(boothTotalWatts),
    isFloorTransit: true,
    label: `Troncal L2 Cabina (${boothExtSection}mm² · ${boothExtLen}m)`,
  });

  // ------------------------------------------------------------------
  // 2. Z2 — SUB CLUSTER CENTRAL (Línea 1 Fuerza exclusiva para Sub-bajos)
  // ------------------------------------------------------------------
  const subDevices: string[] = [];
  activeSubs.forEach((s) => subDevices.push(`${s.tag} ${s.name} (Activo)`));
  const passiveSubAmps = passiveSubs.length > 0 ? Math.max(1, Math.ceil(passiveSubs.length / 2)) : 0;
  for (let i = 1; i <= passiveSubAmps; i++) {
    subDevices.push(`Amplificador Sub-Bajos #${i}`);
  }

  const line1SubsWatts =
    activeSubs.reduce((s, r) => s + r.powerWatts220v, 0) +
    passiveSubs.reduce((s, r) => s + r.powerWatts220v, 0);

  if (subDevices.length > 0) {
    // Si supera 2816W (16A seguro), repartir en 2 zapatillas industriales en paralelo al tablero (anti daisy-chain)
    if (line1SubsWatts > SAFE_WATTS_16A || subDevices.length > 6) {
      daisyChainPreventionTriggered = true;
      const mid = Math.ceil(subDevices.length / 2);
      const zSub1 = makePowerStrip(zSeq++, {
        label: 'Zapatilla Industrial Subs L1-A',
        zone: 'SUB_CLUSTER',
        line: 'LINE_1_SUBS',
        devices: subDevices.slice(0, mid),
        loadWatts: line1SubsWatts / 2,
        force16A: true,
      });
      const zSub2 = makePowerStrip(zSeq++, {
        label: 'Zapatilla Industrial Subs L1-B',
        zone: 'SUB_CLUSTER',
        line: 'LINE_1_SUBS',
        devices: subDevices.slice(mid),
        loadWatts: line1SubsWatts / 2,
        force16A: true,
      });
      powerStrips.push(zSub1, zSub2);
      alerts.push(
        `⚡ ALTA POTENCIA EN SUBS (${Math.round(line1SubsWatts)}W): Excede 1 sola zapatilla de 16A (${SAFE_WATTS_16A}W seguros). Se asignaron 2 zapatillas industriales (${zSub1.id} y ${zSub2.id}) con alargadores separados desde tablero.`
      );
    } else {
      powerStrips.push(
        makePowerStrip(zSeq++, {
          label: 'Zapatilla Industrial Sub Cluster (L1)',
          zone: 'SUB_CLUSTER',
          line: 'LINE_1_SUBS',
          devices: subDevices,
          loadWatts: line1SubsWatts,
          force16A: true,
        })
      );
    }

    const subExtLen = roundToCommercialExtensionLength((boardDist + width * 0.35 + 1.5) * 1.1);
    const subExtSection = Math.max(2.5, pickSection(line1SubsWatts, subExtLen));
    extensionCords.push({
      id: `EXT-${extSeq++}`,
      from: 'Tablero 220V (L1 Fuerza)',
      to: 'Z2 Sub Cluster Central',
      zone: 'SUB_CLUSTER',
      line: 'LINE_1_SUBS',
      lengthMeters: subExtLen,
      crossSectionMm2: subExtSection,
      ratingAmps: 16,
      loadWatts: Math.round(line1SubsWatts),
      isFloorTransit: true,
      label: `Troncal L1 Subs (${subExtSection}mm² · ${subExtLen}m)`,
    });
  }

  // ------------------------------------------------------------------
  // 3. TOPS ACTIVOS (Frente L/R + Torres Delay — Línea 2)
  // ------------------------------------------------------------------
  let activeTopsWatts = 0;

  for (const top of activeFrontTops) {
    activeTopsWatts += top.powerWatts220v;
    const isLeft = top.zone === 'PA_FRONT_L';
    const distFromBoard = isLeft ? boardDist + 2.5 : boardDist + width + 2.5;
    const len = roundToCommercialExtensionLength(distFromBoard * 1.1);
    const sec = pickSection(top.powerWatts220v, len);
    extensionCords.push({
      id: `EXT-${extSeq++}`,
      from: 'Tablero / Z1 (L2)',
      to: `Caja Activa ${top.tag} (${isLeft ? 'Izq' : 'Der'})`,
      zone: isLeft ? 'PA_FRONT_L' : 'PA_FRONT_R',
      line: 'LINE_2_TOPS_CTRL',
      lengthMeters: len,
      crossSectionMm2: sec,
      ratingAmps: 10,
      loadWatts: Math.round(top.powerWatts220v),
      isFloorTransit: !isLeft,
      label: `Alargador Top ${top.tag} (${sec}mm² · ${len}m)`,
    });
  }

  if (activeDelayTops.length > 0) {
    const delayDevices = activeDelayTops.map((t) => `${t.tag} ${t.name} (Delay)`);
    const delayWatts = activeDelayTops.reduce((s, r) => s + r.powerWatts220v, 0);
    activeTopsWatts += delayWatts;

    powerStrips.push(
      makePowerStrip(zSeq++, {
        label: 'Zapatilla Zona Delays (Perimetral L2)',
        zone: 'DELAY_ZONE',
        line: 'LINE_2_TOPS_CTRL',
        devices: delayDevices,
        loadWatts: delayWatts,
      })
    );

    // Cada torre delay recibe alargador perimetral bordeando las paredes (nunca cruzando centro pista)
    for (const dTop of activeDelayTops) {
      const perimDist = boardDist + (dTop.posY || depth * 0.55) + 2.2;
      const len = roundToCommercialExtensionLength(perimDist * 1.1);
      const sec = pickSection(dTop.powerWatts220v, len);
      extensionCords.push({
        id: `EXT-${extSeq++}`,
        from: 'Tablero 220V (L2 Perimetral)',
        to: `Torre Delay ${dTop.tag}`,
        zone: 'DELAY_ZONE',
        line: 'LINE_2_TOPS_CTRL',
        lengthMeters: len,
        crossSectionMm2: sec,
        ratingAmps: 10,
        loadWatts: Math.round(dTop.powerWatts220v),
        isFloorTransit: true,
        label: `Perimetral Delay ${dTop.tag} (${sec}mm² · ${len}m)`,
      });
    }
  }

  // ------------------------------------------------------------------
  // 4. LÍNEA 3 — ILUMINACIÓN Y EFECTOS TÉRMICOS (HUMO / LÁSER / CABEZAS)
  // ------------------------------------------------------------------
  const lighting = input.lightingAnalysis;
  const line3LightingWatts = lighting?.totalLightingWatts ?? 0;

  if (lighting && lighting.totalFixtureUnits > 0) {
    // Separar dispositivos térmicos (Humo/Hazer) de luminarias LED/DMX si ambos coexisten
    const fxDevices: string[] = [];
    const lightDevices: string[] = [];

    for (const z of lighting.zones) {
      if (z.hasThermalLoad) {
        z.fixtureNames.forEach((n) => fxDevices.push(n));
      } else {
        z.fixtureNames.forEach((n) => lightDevices.push(n));
      }
    }

    if (lightDevices.length > 0) {
      const zLight = makePowerStrip(zSeq++, {
        label: 'Zapatilla Iluminación Truss/Luces (L3)',
        zone: 'LIGHTING_FX',
        line: 'LINE_3_LIGHTING_FX',
        devices: lightDevices.slice(0, 6),
        loadWatts: lighting.nonThermalLightingWatts,
      });
      powerStrips.push(zLight);

      const lightExtLen = roundToCommercialExtensionLength((boardDist + width * 0.4 + 2.2) * 1.1);
      const lightExtSec = pickSection(lighting.nonThermalLightingWatts, lightExtLen);
      extensionCords.push({
        id: `EXT-${extSeq++}`,
        from: 'Tablero 220V (L3 Luces)',
        to: `${zLight.id} Iluminación`,
        zone: 'LIGHTING_FX',
        line: 'LINE_3_LIGHTING_FX',
        lengthMeters: lightExtLen,
        crossSectionMm2: lightExtSec,
        ratingAmps: lighting.nonThermalLightingWatts > SAFE_WATTS_10A ? 16 : 10,
        loadWatts: lighting.nonThermalLightingWatts,
        isFloorTransit: true,
        label: `Troncal L3 Luces (${lightExtSec}mm² · ${lightExtLen}m)`,
      });
    }

    if (lighting.hasThermalLoad && fxDevices.length > 0) {
      const zSmoke = makePowerStrip(zSeq++, {
        label: 'Toma Dedicada Humo / Hazer (L3 Térmica)',
        zone: 'LIGHTING_FX',
        line: 'LINE_3_LIGHTING_FX',
        devices: fxDevices.slice(0, 4),
        loadWatts: lighting.thermalEffectsWatts,
        force16A: lighting.thermalEffectsWatts >= 1400,
      });
      powerStrips.push(zSmoke);

      const smokeExtLen = roundToCommercialExtensionLength((boardDist + 4.0) * 1.1);
      const smokeExtSec = Math.max(2.5, pickSection(lighting.thermalEffectsWatts, smokeExtLen));
      extensionCords.push({
        id: `EXT-${extSeq++}`,
        from: 'Tablero 220V (L3 Térmica)',
        to: `${zSmoke.id} Humo / Hazer`,
        zone: 'LIGHTING_FX',
        line: 'LINE_3_LIGHTING_FX',
        lengthMeters: smokeExtLen,
        crossSectionMm2: smokeExtSec,
        ratingAmps: 16,
        loadWatts: lighting.thermalEffectsWatts,
        isFloorTransit: true,
        label: `Alargador Dedicado Humo (${smokeExtSec}mm² · ${smokeExtLen}m)`,
      });
    }
  }

  // ------------------------------------------------------------------
  // 5. CONSOLIDACIÓN DE INVENTARIO DE ALARGADORES Y ZAPATILLAS
  // ------------------------------------------------------------------
  const extSummaryMap = new Map<string, ExtensionCordInventoryRow>();
  for (const ext of extensionCords) {
    const key = `${ext.crossSectionMm2}_${ext.lengthMeters}_${ext.ratingAmps}`;
    if (!extSummaryMap.has(key)) {
      extSummaryMap.set(key, {
        crossSectionMm2: ext.crossSectionMm2,
        lengthMeters: ext.lengthMeters,
        ratingAmps: ext.ratingAmps,
        quantity: 0,
        description: `Alargador ${ext.crossSectionMm2} mm² (${ext.ratingAmps}A) de ${ext.lengthMeters} metros`,
      });
    }
    extSummaryMap.get(key)!.quantity += 1;
  }

  const extensionCordSummary = Array.from(extSummaryMap.values()).sort(
    (a, b) => b.crossSectionMm2 - a.crossSectionMm2 || b.lengthMeters - a.lengthMeters
  );

  // Sumar bocas: todas las zapatillas + 1 boca directa por cada Top activo frontal con alargador propio
  const socketsInStrips = powerStrips.reduce((s, z) => s + z.usedSockets, 0);
  const totalSocketsRequired = socketsInStrips + activeFrontTops.length;
  const totalPowerStrips10A = powerStrips.filter((z) => z.ratingAmps === 10).length;
  const totalPowerStrips16A = powerStrips.filter((z) => z.ratingAmps === 16).length;

  const line2TopsAndBoothWatts = Math.round(boothTotalWatts + activeTopsWatts);

  // Alertas normativas y recomendaciones prácticas en Chile
  for (const z of powerStrips) {
    if (z.status === 'OVERLOAD') {
      alerts.push(
        `🔴 SOBRECARGA EN ${z.id} (${z.label}): ${z.loadWatts}W excede el límite seguro continuo (${z.safeMaxWatts}W al 80% SEC). Dividir carga en dos tomas independientes.`
      );
    }
  }

  if (passiveBoxesWithout220vCount > 0) {
    recommendations.push(
      `🔊 CAJAS PASIVAS SIN 220V EN TRÍPODE: Tienes ${passiveBoxesWithout220vCount} caja(s) pasiva(s); NO lleves alargador eléctrico hacia sus atriles, solo cable Speakon NL4 desde el amplificador.`
    );
  }
  if (totalPowerStrips16A > 0) {
    recommendations.push(
      `🇨🇱 ADAPTADORES ENCHUFE CHILENO (10A vs 16A): Tu montaje requiere ${totalPowerStrips16A} zapatilla(s) industrial(es) de 16A (clavija gruesa Schuko). Lleva al menos 2 adaptadores certificados 16A↔10A por si el recinto solo tiene tomas domiciliarias de 10A.`
    );
  }
  recommendations.push(
    `🚫 REGLA DE ORO SEC RIC N° 10: Nunca encadenes zapatilla sobre zapatilla (daisy-chain) ni operes alargadores enrollados en carrete (riesgo de sobrecalentamiento por efecto bobina).`
  );

  return {
    powerStrips,
    extensionCords,
    extensionCordSummary,
    totalSocketsRequired,
    totalPowerStrips10A,
    totalPowerStrips16A,
    totalPowerStripsCount: powerStrips.length,
    passiveBoxesWithout220vCount,
    daisyChainPreventionTriggered,
    lineTotalsWatts: {
      line1Subs: Math.round(line1SubsWatts),
      line2TopsAndBooth: line2TopsAndBoothWatts,
      line3LightingAndFx: Math.round(line3LightingWatts),
      grandTotal: Math.round(line1SubsWatts + line2TopsAndBoothWatts + line3LightingWatts),
    },
    alerts,
    recommendations,
  };
}
