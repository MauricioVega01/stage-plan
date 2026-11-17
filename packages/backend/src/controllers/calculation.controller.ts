import { Request, Response } from 'express';
import {
  RiderSchema,
  EngineeringParamsSchema,
  calculateCableSizing,
  validateCircuitCapacity,
  validateGeneratorCapacity,
  calculatePassiveAmplification,
  calculateSplCoverage,
  calculateSupportInventory,
  MOUNTING_PROTOCOL_STEPS,
} from '@stageplan/shared';
import { prisma } from '../prisma.js';

export class CalculationController {
  // POST /api/venues/:venueId/calculate
  // Ejecuta el motor oficial calc-engine, valida con Zod y persiste en PostgreSQL
  static async calculateAndSave(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const venueId = req.params.venueId as string;

    // 1. Validar propiedad del recinto (Anti-IDOR)
    const venue = await prisma.venue.findFirst({
      where: { id: venueId, ownerId },
    });

    if (!venue) {
      res.status(404).json({ error: 'Recinto no encontrado o no tiene permisos sobre él.' });
      return;
    }

    // 2. Validar Rider y Parámetros
    const riderParse = RiderSchema.safeParse(req.body.rider);
    if (!riderParse.success) {
      res.status(400).json({ error: 'Rider inválido', details: riderParse.error.format() });
      return;
    }

    const paramsParse = EngineeringParamsSchema.safeParse(req.body.params ?? {});
    if (!paramsParse.success) {
      res.status(400).json({ error: 'Parámetros inválidos', details: paramsParse.error.format() });
      return;
    }

    const rider = riderParse.data;
    const params = paramsParse.data;

    // 3. Ejecutar Lógica de Ingeniería (calc-engine)
    // A. Potencias y Consumo
    let totalAudioWatts = 0;
    let passiveChannelResult = null;

    if (rider.audio.systemType === 'PASSIVE') {
      const pConfig = rider.audio.passiveConfig || {
        topsWiring: 'PARALLEL' as const,
        topsBoxImpedance: 8,
        boxesPerChannel: 2,
      };

      passiveChannelResult = calculatePassiveAmplification({
        boxesCount: pConfig.boxesPerChannel,
        boxRmsWatts: rider.audio.topsRmsWatts,
        boxImpedanceOhms: pConfig.topsBoxImpedance,
        wiring: pConfig.topsWiring,
        headroomFactor: params.headroomFactor,
        minAmpImpedance: params.minAmpImpedance,
        ampEfficiency: params.ampEfficiencyClassD,
      });

      // El consumo continuo en modo conservador
      totalAudioWatts = passiveChannelResult.networkPowerConservativeWatts * (rider.audio.topsCount / pConfig.boxesPerChannel);
      // Sumar subwoofers
      totalAudioWatts += (rider.audio.subsCount * rider.audio.subsRmsWatts) / params.ampEfficiencyClassD;
    } else {
      // Audio Activo: consumo nominal declarado de las cajas
      totalAudioWatts = (rider.audio.topsCount * rider.audio.topsRmsWatts) + (rider.audio.subsCount * rider.audio.subsRmsWatts);
    }

    const lightingWatts = rider.lighting.reduce((sum, f) => sum + (f.nominalWatts * f.quantity), 0);
    const totalWatts = totalAudioWatts + lightingWatts + rider.djBoothNominalWatts;

    // B. Validación Eléctrica (Red vs Generador)
    let powerValidation;
    if (rider.powerSource.type === 'GRID_220V') {
      powerValidation = validateCircuitCapacity(
        totalWatts,
        Number(rider.powerSource.circuitBreakerAmps),
        params.safetyMarginPct,
        params.nominalVoltage,
        params.powerFactorLoad
      );
    } else {
      powerValidation = validateGeneratorCapacity(
        totalWatts,
        rider.powerSource.apparentPowerKva,
        rider.powerSource.powerFactor,
        params.safetyMarginPct
      );
    }

    // C. Cableado y Caída de Tensión (RIC 03 / RIC 10)
    const cableSizing = calculateCableSizing({
      powerWatts: totalWatts,
      voltage: params.nominalVoltage,
      distanceMeters: venue.electricalDistanceMeters,
      safetyMarginPct: params.safetyMarginPct,
      maxVoltageDropPct: params.maxVoltageDropPct,
      copperResistivity: params.copperResistivity,
      powerFactorLoad: params.powerFactorLoad,
    });

    // D. Cobertura Acústica SPL
    const splCoverage = calculateSplCoverage({
      sensitivityDb: rider.audio.topsSensitivityDb,
      powerRmsWatts: rider.audio.topsRmsWatts,
      distanceFirstRowMeters: params.referenceAudienceDistance,
      distanceBackMeters: venue.depthMeters,
      splTargetDb: params.splTargetFloor,
      maxSplDropThresholdDb: params.splMaxDropThreshold,
      isIndoor: venue.environmentType === 'INDOOR',
    });

    // E. Inventario de Soportes
    const totalOutletsRequired = (rider.audio.topsCount) + (rider.audio.subsCount) + (rider.lighting.length > 0 ? 2 : 0) + 2; // +2 DJ booth
    const inventory = calculateSupportInventory({
      subsCount: rider.audio.subsCount,
      topsCount: rider.audio.topsCount,
      topsMountedOnSubPole: rider.audio.topsMountedOnSubPole,
      totalOutletsRequired,
    });

    // F. Compilar resultados
    const calculatedResults = {
      totalWatts,
      powerValidation,
      cableSizing,
      passiveChannelResult,
      splCoverage,
      inventory,
      mountingProtocol: MOUNTING_PROTOCOL_STEPS,
      secDisclaimer: 'El sistema es una herramienta de estimación de pre-producción y no reemplaza la verificación ni la certificación de una instalación eléctrica realizada por un instalador eléctrico autorizado por la SEC.',
    };

    const alertsSnapshot = {
      electricalAlert: powerValidation.alertLevel,
      electricalMessage: powerValidation.alertMessage,
      acousticsDelayRequired: splCoverage.recommendDelayFill,
      acousticsReasons: splCoverage.recommendationReason,
      hasHighInrush: rider.hasHighInrushEquipment,
    };

    // 4. Persistir en la base de datos
    const savedCalculation = await prisma.riderCalculation.create({
      data: {
        ownerId,
        venueId: venue.id,
        engineVersion: '3.1.0',
        riderInput: rider as any,
        paramsUsed: params as any,
        calculatedResults: calculatedResults as any,
        alertsSnapshot: alertsSnapshot as any,
      },
    });

    res.status(201).json(savedCalculation);
  }

  // GET /api/calculations/history
  static async listHistory(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const history = await prisma.riderCalculation.findMany({
      where: { ownerId },
      include: {
        venue: {
          select: { name: true, widthMeters: true, depthMeters: true, environmentType: true },
        },
      },
      orderBy: { createdAt: 'desc' },
    });
    res.json(history);
  }

  // GET /api/calculations/:id
  static async getById(req: Request, res: Response): Promise<void> {
    const ownerId = req.user!.id;
    const id = req.params.id as string;

    const calculation = await prisma.riderCalculation.findFirst({
      where: { id, ownerId },
      include: { venue: true },
    });

    if (!calculation) {
      res.status(404).json({ error: 'Cálculo no encontrado o no tiene permisos para verlo.' });
      return;
    }

    res.json(calculation);
  }
}

