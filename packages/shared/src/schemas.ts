import { z } from 'zod';

// ==========================================
// 1. ESQUEMAS DE PARÁMETROS CONFIGURABLES
// ==========================================

export const EngineeringParamsSchema = z.object({
  powerFactorGenerator: z.number().min(0.5).max(1.0).default(0.8), // FP_gen
  powerFactorLoad: z.number().min(0.5).max(1.0).default(1.0),      // FP_carga
  nominalVoltage: z.number().min(110).max(250).default(220),       // V
  safetyMarginPct: z.number().min(0).max(100).default(20),         // Holgura continua % (20%)
  maxVoltageDropPct: z.number().min(0.5).max(10).default(3.0),     // dV_max % (3% según RIC 03 SEC)
  copperResistivity: z.number().min(0.015).max(0.03).default(0.0175), // rho cobre (0.0175 ohm.mm2/m a 20C)
  circuitBreakerCapacity: z.enum(['10', '16', '20', '25', '32']).default('10'), // A
  ampEfficiencyClassD: z.number().min(0.5).max(1.0).default(0.8),  // Eficiencia amplificador
  ampUsageFactorConservative: z.number().min(0.1).max(1.0).default(1.0), // Factor uso conservador
  ampUsageFactorMusical: z.number().min(0.1).max(1.0).default(0.5),      // Factor uso promedio musical
  headroomFactor: z.number().min(1.0).max(3.0).default(1.5),             // Headroom amplificador
  minAmpImpedance: z.number().min(1).max(8).default(4),                   // Impedancia mín amplificador (ohms)
  referenceAudienceDistance: z.number().min(1).max(20).default(4),       // Primera fila (m)
  splTargetFloor: z.number().min(70).max(130).default(98),               // SPL objetivo pista (dB)
  splMaxDropThreshold: z.number().min(3).max(20).default(10),            // Umbral caída SPL (dB)
});

export type EngineeringParams = z.infer<typeof EngineeringParamsSchema>;

// ==========================================
// 2. ESQUEMA DE RECINTO (VENUE)
// ==========================================

export const VenueSchema = z.object({
  name: z.string().min(2, 'El nombre debe tener al menos 2 caracteres'),
  widthMeters: z.number().positive('El ancho debe ser mayor a 0').max(500),
  depthMeters: z.number().positive('La profundidad debe ser mayor a 0').max(500),
  heightMeters: z.number().positive('La altura debe ser mayor a 0').max(50),
  environmentType: z.enum(['INDOOR', 'OUTDOOR_PARCELA', 'OUTDOOR_OPEN']),
  electricalDistanceMeters: z.number().positive('La distancia debe ser mayor a 0').max(500),
});

export type Venue = z.infer<typeof VenueSchema>;

// ==========================================
// 3. ESQUEMA DE EQUIPOS Y RIDER TÉCNICO
// ==========================================

export const PassiveSpeakerConfigSchema = z.object({
  rmsWattsPerBox: z.number().positive().max(10000),
  nominalImpedanceOhms: z.enum(['4', '8', '16']).default('8'),
  wiring: z.enum(['PARALLEL', 'SERIES']).default('PARALLEL'),
  quantity: z.number().int().min(1).max(32),
});

export const AudioSystemSchema = z.object({
  systemType: z.enum(['ACTIVE', 'PASSIVE']),
  // Cajas Top / Medios-Agudos
  topsCount: z.number().int().min(0).max(32).default(2),
  topsRmsWatts: z.number().positive().max(5000).default(400),
  topsSensitivityDb: z.number().min(70).max(120).default(98), // dB @ 1W/1m
  topsMountedOnSubPole: z.number().int().min(0).max(32).default(0),
  // Cajas Subwoofer
  subsCount: z.number().int().min(0).max(32).default(2),
  subsRmsWatts: z.number().positive().max(10000).default(800),
  // Configuración Pasiva (si aplica)
  passiveConfig: z.object({
    topsWiring: z.enum(['PARALLEL', 'SERIES']).default('PARALLEL'),
    topsBoxImpedance: z.number().default(8),
    boxesPerChannel: z.number().int().min(1).max(8).default(2),
  }).optional(),
});

export const LightingFixtureTypeEnum = z.enum([
  'PAR_LED',
  'LED_BAR',
  'MOVING_HEAD',
  'LASER',
  'STROBE',
  'FOG_MACHINE',
  'HAZER',
]);

export const LightingZoneEnum = z.enum([
  'TRUSS_LEFT',
  'CENTER_BOOTH',
  'TRUSS_RIGHT',
  'FLOOR',
]);

export const DmxConnectorEnum = z.enum([
  'DMX_3PIN',
  'DMX_5PIN',
  'NONE',
]);

export const LightingFixtureSchema = z.object({
  id: z.string().optional(),
  name: z.string().min(1),
  fixtureType: LightingFixtureTypeEnum.default('PAR_LED'),
  nominalWatts: z.number().positive().max(10000),
  quantity: z.number().int().positive().max(64),
  zone: LightingZoneEnum.default('CENTER_BOOTH'),
  dmxConnector: DmxConnectorEnum.default('DMX_3PIN'),
  unitWeightKg: z.number().nonnegative().max(150).default(4),
  isThermalLoad: z.boolean().default(false),
});

export type LightingFixtureInput = z.infer<typeof LightingFixtureSchema>;

export const PowerSourceSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('GRID_220V'),
    circuitBreakerAmps: z.enum(['10', '16', '20', '25', '32']).default('10'),
  }),
  z.object({
    type: z.literal('GENERATOR_KVA'),
    apparentPowerKva: z.number().positive().max(500),
    powerFactor: z.number().min(0.5).max(1.0).default(0.8),
  }),
]);

export const RiderSchema = z.object({
  audio: AudioSystemSchema,
  lighting: z.array(LightingFixtureSchema).default([]),
  powerSource: PowerSourceSchema,
  djBoothNominalWatts: z.number().nonnegative().default(300), // Consumo cabina DJ
  hasHighInrushEquipment: z.boolean().default(false),         // Máquina de humo, motores, etc.
});

export type Rider = z.infer<typeof RiderSchema>;

