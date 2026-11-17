// ======================================================================
// CALC-ENGINE: ELECTRICAL MODULE
// Fórmulas de ingeniería eléctrica basadas en RIC N° 03 y RIC N° 10 (SEC Chile)
// ======================================================================

export interface CableCalculationInput {
  powerWatts: number;
  voltage?: number;
  distanceMeters: number;
  safetyMarginPct?: number;
  maxVoltageDropPct?: number;
  copperResistivity?: number;
  powerFactorLoad?: number;
}

export interface CableCalculationResult {
  nominalCurrentAmps: number;
  designCurrentAmps: number;
  theoreticalCrossSectionMm2: number;
  ampacityCrossSectionMm2: number;
  commercialCrossSectionMm2: number;
  determiningCriterion: 'VOLTAGE_DROP' | 'AMPACITY';
  suggestedLengthMeters: number;
  actualVoltageDropVolts: number;
  actualVoltageDropPct: number;
  warningRolledCable: string;
}

// Tabla de ampacidad de referencia para cordones flexibles de servicio móvil (RIC N° 04 / RIC N° 10)
export const COMMERCIAL_SECTIONS = [1.5, 2.5, 4.0, 6.0, 10.0, 16.0] as const;

export const AMPACITY_TABLE = [
  { sectionMm2: 1.5, maxAmps: 15.0 },
  { sectionMm2: 2.5, maxAmps: 21.0 },
  { sectionMm2: 4.0, maxAmps: 28.0 },
  { sectionMm2: 6.0, maxAmps: 36.0 },
  { sectionMm2: 10.0, maxAmps: 50.0 },
  { sectionMm2: 16.0, maxAmps: 66.0 },
];

export function getSectionByAmpacity(amps: number): number {
  for (const row of AMPACITY_TABLE) {
    if (amps <= row.maxAmps) {
      return row.sectionMm2;
    }
  }
  return 16.0; // Sección máxima comercial en el rango contemplado
}

export function roundToNextCommercialSection(sectionMm2: number): number {
  for (const s of COMMERCIAL_SECTIONS) {
    if (sectionMm2 <= s) {
      return s;
    }
  }
  return 16.0;
}

export function calculateCableSizing(input: CableCalculationInput): CableCalculationResult {
  const voltage = input.voltage ?? 220;
  const safetyMargin = (input.safetyMarginPct ?? 20) / 100;
  const maxDropPct = input.maxVoltageDropPct ?? 3.0;
  const rho = input.copperResistivity ?? 0.0175;
  const fp = input.powerFactorLoad ?? 1.0;

  // 1. Corriente nominal y de diseño
  const nominalCurrentAmps = input.powerWatts / (voltage * fp);
  const designCurrentAmps = nominalCurrentAmps * (1 + safetyMargin);

  // 2. Criterio 1: Caída de tensión admisible (dV_max en Volts)
  const dV_max = (maxDropPct / 100) * voltage;
  // S = (2 * rho * L * I_diseño) / dV_max
  const theoreticalCrossSectionMm2 = (2 * rho * input.distanceMeters * designCurrentAmps) / dV_max;

  // 3. Criterio 2: Ampacidad
  const ampacityCrossSectionMm2 = getSectionByAmpacity(designCurrentAmps);

  // 4. Doble criterio: se adopta el más exigente y se lleva a sección comercial
  const requiredSection = Math.max(theoreticalCrossSectionMm2, ampacityCrossSectionMm2);
  const commercialCrossSectionMm2 = roundToNextCommercialSection(requiredSection);

  const determiningCriterion: 'VOLTAGE_DROP' | 'AMPACITY' =
    theoreticalCrossSectionMm2 > ampacityCrossSectionMm2 ? 'VOLTAGE_DROP' : 'AMPACITY';

  // 5. Metraje sugerido (+10% de holgura de tendido)
  const suggestedLengthMeters = Math.round(input.distanceMeters * 1.10);

  // 6. Caída de tensión real con la sección comercial adoptada
  // dV_real = (2 * rho * L * I_diseño) / S_comercial
  const actualVoltageDropVolts = (2 * rho * input.distanceMeters * designCurrentAmps) / commercialCrossSectionMm2;
  const actualVoltageDropPct = (actualVoltageDropVolts / voltage) * 100;

  return {
    nominalCurrentAmps: Number(nominalCurrentAmps.toFixed(2)),
    designCurrentAmps: Number(designCurrentAmps.toFixed(2)),
    theoreticalCrossSectionMm2: Number(theoreticalCrossSectionMm2.toFixed(2)),
    ampacityCrossSectionMm2,
    commercialCrossSectionMm2,
    determiningCriterion,
    suggestedLengthMeters,
    actualVoltageDropVolts: Number(actualVoltageDropVolts.toFixed(2)),
    actualVoltageDropPct: Number(actualVoltageDropPct.toFixed(2)),
    warningRolledCable: 'Desenrolle completamente los alargadores en carrete; un cable enrollado bajo carga genera un efecto bobina que sobrecalienta el conductor y reduce drásticamente su capacidad de corriente.',
  };
}

export interface PowerValidationResult {
  totalEstimatedWatts: number;
  designPowerWatts: number;
  nominalCurrentAmps: number;
  designCurrentAmps: number;
  maxAllowedCurrentOrPower: number;
  usageRatio: number; // e.g. 1.09 = 109%
  alertLevel: 'INFO' | 'WARNING' | 'CRITICAL';
  alertMessage: string;
}

export function validateCircuitCapacity(
  powerWatts: number,
  breakerAmps: number,
  safetyMarginPct = 20,
  voltage = 220,
  powerFactor = 1.0
): PowerValidationResult {
  const nominalCurrentAmps = powerWatts / (voltage * powerFactor);
  const designCurrentAmps = nominalCurrentAmps * (1 + safetyMarginPct / 100);
  const usageRatio = designCurrentAmps / breakerAmps;

  let alertLevel: 'INFO' | 'WARNING' | 'CRITICAL' = 'INFO';
  let alertMessage = 'Carga eléctrica dentro de límites seguros.';

  if (usageRatio > 1.0) {
    alertLevel = 'CRITICAL';
    alertMessage = `ALERTA CRÍTICA: Corriente de diseño (${designCurrentAmps.toFixed(2)} A) supera la capacidad del disyuntor (${breakerAmps} A). Riesgo inminente de disparo térmico.`;
  } else if (usageRatio > 0.9) {
    alertLevel = 'WARNING';
    alertMessage = `ADVERTENCIA: Uso elevado de circuito (${(usageRatio * 100).toFixed(1)}%). Próximo al límite del disyuntor de ${breakerAmps} A.`;
  }

  return {
    totalEstimatedWatts: powerWatts,
    designPowerWatts: powerWatts * (1 + safetyMarginPct / 100),
    nominalCurrentAmps: Number(nominalCurrentAmps.toFixed(2)),
    designCurrentAmps: Number(designCurrentAmps.toFixed(2)),
    maxAllowedCurrentOrPower: breakerAmps,
    usageRatio: Number(usageRatio.toFixed(3)),
    alertLevel,
    alertMessage,
  };
}

export function validateGeneratorCapacity(
  powerWatts: number,
  generatorKva: number,
  fpGen = 0.8,
  safetyMarginPct = 20
): PowerValidationResult {
  const realKw = generatorKva * fpGen;
  const designKw = (powerWatts / 1000) * (1 + safetyMarginPct / 100);
  const usageRatio = designKw / realKw;

  let alertLevel: 'INFO' | 'WARNING' | 'CRITICAL' = 'INFO';
  let alertMessage = 'Capacidad del generador adecuada para la carga.';

  if (usageRatio > 1.0) {
    alertLevel = 'CRITICAL';
    alertMessage = `ALERTA CRÍTICA: Potencia de diseño (${designKw.toFixed(2)} kW) supera la capacidad real del generador (${realKw.toFixed(2)} kW @ FP ${fpGen}). Riesgo de apagón o daño al alternador.`;
  } else if (usageRatio > 0.9) {
    alertLevel = 'WARNING';
    alertMessage = `ADVERTENCIA: Generador al ${(usageRatio * 100).toFixed(1)}% de su capacidad. Evite conectar cargas no planificadas.`;
  }

  return {
    totalEstimatedWatts: powerWatts,
    designPowerWatts: Number((designKw * 1000).toFixed(1)),
    nominalCurrentAmps: Number((powerWatts / (220 * 0.85)).toFixed(2)),
    designCurrentAmps: Number(((designKw * 1000) / (220 * 0.85)).toFixed(2)),
    maxAllowedCurrentOrPower: realKw * 1000,
    usageRatio: Number(usageRatio.toFixed(3)),
    alertLevel,
    alertMessage,
  };
}

