// ======================================================================
// CALC-ENGINE: SPATIAL ROUTING & GAFFER TAPE MODULE (v3.2)
// Cálculo de distancias individuales, ruteo inteligente y cinta gris
// ======================================================================

export interface Point2D {
  x: number;
  y: number;
}

export interface ElectricalOutlet {
  id: string;
  name: string;
  position: Point2D;
  maxPowerWatts: number;
  currentAssignedWatts?: number;
}

export interface EquipmentLoad {
  id: string;
  name: string;
  position: Point2D;
  powerWatts: number;
  requiresFloorTransit?: boolean;
}

export interface DistanceOptions {
  heightMeters?: number; // Elevación sobre trípode (1.5m estándar)
  marginPct?: number;    // Holgura de tendido (+10% por defecto)
}

export interface DistanceResult {
  euclidean: number;
  perimeter: number;
  suggestedCableMeters: number;
}

export function calculateDistances(
  equipmentPos: Point2D,
  outletPos: Point2D,
  options?: DistanceOptions
): DistanceResult {
  const height = options?.heightMeters ?? 0;
  const margin = (options?.marginPct ?? 10) / 100;

  // 1. Distancia euclidiana recta en línea de aire: sqrt(dx^2 + dy^2)
  const dx = equipmentPos.x - outletPos.x;
  const dy = equipmentPos.y - outletPos.y;
  const euclidean = Number(Math.sqrt(dx * dx + dy * dy).toFixed(2));

  // 2. Distancia perimetral / Manhattan (por la orilla o pared): |dx| + |dy|
  const perimeter = Number((Math.abs(dx) + Math.abs(dy)).toFixed(2));

  // 3. Metraje sugerido de cable: (tendido perimetral + bajada del trípode) * (1 + holgura)
  const rawCableMeters = perimeter + height;
  const suggestedCableMeters = Math.ceil(rawCableMeters * (1 + margin));

  return {
    euclidean,
    perimeter,
    suggestedCableMeters,
  };
}

export interface GafferTapeInput {
  floorTransitMeters: number;
}

export interface GafferTapeResult {
  transitDistanceMeters: number;
  requiredTapeMetersWithMargin: number; // +20% para fijaciones y solapamientos
  standardRolls50m: number;
  spareMeters: number;
  friendlySummary: string;
}

export function calculateGafferTape(input: GafferTapeInput): GafferTapeResult {
  const transitMeters = Math.max(0, input.floorTransitMeters);

  if (transitMeters === 0) {
    return {
      transitDistanceMeters: 0,
      requiredTapeMetersWithMargin: 0,
      standardRolls50m: 0,
      spareMeters: 0,
      friendlySummary: 'No hay cables que crucen zonas de paso de gente; no se necesita cinta para piso.',
    };
  }

  // Se añade un 20% de cinta extra para parches transversales y esquinas
  const requiredTapeMetersWithMargin = Math.round(transitMeters * 1.20);
  const standardRolls50m = Math.ceil(requiredTapeMetersWithMargin / 50);
  const totalTapeSupplied = standardRolls50m * 50;
  const spareMeters = totalTapeSupplied - requiredTapeMetersWithMargin;

  const rollsText = standardRolls50m === 1 ? '1 rollo' : `${standardRolls50m} rollos`;
  const friendlySummary = `Tienes ${transitMeters} metros de cable cruzando el piso donde pasa la gente. Para evitar tropiezos, necesitas ${requiredTapeMetersWithMargin} metros de cinta gris para piso (${rollsText} de 50m). Te sobrarán ${spareMeters} metros de cinta para detalles y fijaciones.`;

  return {
    transitDistanceMeters: transitMeters,
    requiredTapeMetersWithMargin,
    standardRolls50m,
    spareMeters,
    friendlySummary,
  };
}

export interface RouteAssignment {
  equipmentId: string;
  outletId: string;
  euclideanDistanceMeters: number;
  perimeterDistanceMeters: number;
  cableTensionMeters: number;
}

export interface RecommendationItem {
  type: 'ADD_OUTLET_CAPACITY' | 'ADD_OUTLET_DISTANCE' | 'INFO';
  friendlyMessage: string;
}

export interface RoutingEngineResult {
  assignments: RouteAssignment[];
  outletsStatus: Array<{
    outletId: string;
    totalAssignedWatts: number;
    usagePercentage: number;
    isOverloaded: boolean;
  }>;
  needsAdditionalOutlet: boolean;
  recommendations: RecommendationItem[];
  gafferTape: GafferTapeResult;
}

export function routeEquipmentToOutlets(
  equipments: EquipmentLoad[],
  outlets: ElectricalOutlet[]
): RoutingEngineResult {
  if (outlets.length === 0) {
    throw new Error('Debe existir al menos un enchufe o punto de suministro eléctrico disponible.');
  }

  const assignments: RouteAssignment[] = [];
  const assignedWattsPerOutlet: Record<string, number> = {};
  outlets.forEach((o) => {
    assignedWattsPerOutlet[o.id] = 0;
  });

  let totalFloorTransitMeters = 0;
  const recommendations: RecommendationItem[] = [];
  let needsAdditionalOutlet = false;

  // 1. Ruteo inteligente: ordenar equipos de mayor a menor potencia para optimizar carga
  const sortedEquipments = [...equipments].sort((a, b) => b.powerWatts - a.powerWatts);

  for (const eq of sortedEquipments) {
    // Buscar enchufes que tengan capacidad remanente
    const candidateOutlets = outlets.filter((o) => {
      const currentLoad = assignedWattsPerOutlet[o.id];
      return currentLoad + eq.powerWatts <= o.maxPowerWatts;
    });

    // Si hay enchufes con capacidad libre, elegimos el más cercano
    // Si ninguno tiene capacidad, elegimos el más cercano de todos los existentes
    const pool = candidateOutlets.length > 0 ? candidateOutlets : outlets;

    let chosenOutlet = pool[0];
    let minDistance = Infinity;
    let chosenPerimeter = 0;
    let chosenEuclidean = 0;

    for (const o of pool) {
      const dist = calculateDistances(eq.position, o.position, { heightMeters: 1.5 });
      if (dist.perimeter < minDistance) {
        minDistance = dist.perimeter;
        chosenOutlet = o;
        chosenPerimeter = dist.perimeter;
        chosenEuclidean = dist.euclidean;
      }
    }

    assignedWattsPerOutlet[chosenOutlet.id] += eq.powerWatts;

    assignments.push({
      equipmentId: eq.id,
      outletId: chosenOutlet.id,
      euclideanDistanceMeters: chosenEuclidean,
      perimeterDistanceMeters: chosenPerimeter,
      cableTensionMeters: Math.ceil((chosenPerimeter + 1.5) * 1.1),
    });

    // Sumar cables por suelo si corresponde
    if (eq.requiresFloorTransit !== false) {
      // Metraje de piso aproximado por tendido
      totalFloorTransitMeters += chosenPerimeter;
    }

    // Regla de distancia excesiva (> 25 metros)
    if (chosenPerimeter > 25) {
      needsAdditionalOutlet = true;
      recommendations.push({
        type: 'ADD_OUTLET_DISTANCE',
        friendlyMessage: `El equipo '${eq.name}' está a ${chosenPerimeter} metros del enchufe '${chosenOutlet.name}'. Supera los 25 metros recomendados. Si el local lo permite, conviene habilitar un enchufe más cercano para no perder fuerza eléctrica en un cable tan largo.`,
      });
    }
  }

  // 2. Evaluar estado de los enchufes
  const outletsStatus = outlets.map((o) => {
    const totalAssignedWatts = assignedWattsPerOutlet[o.id];
    const usagePercentage = Number(((totalAssignedWatts / o.maxPowerWatts) * 100).toFixed(1));
    const isOverloaded = totalAssignedWatts > o.maxPowerWatts;

    if (usagePercentage > 90) {
      needsAdditionalOutlet = true;
      const statusText = isOverloaded ? 'está sobrecargado' : 'está al límite';
      recommendations.push({
        type: 'ADD_OUTLET_CAPACITY',
        friendlyMessage: `El enchufe '${o.name}' ${statusText} con ${totalAssignedWatts}W de ${o.maxPowerWatts}W permitidos (${usagePercentage}%). Si el salón lo permite, sugerimos conectar parte de los equipos a otro enchufe o circuito adicional para evitar que se corte la luz.`,
      });
    }

    return {
      outletId: o.id,
      totalAssignedWatts,
      usagePercentage,
      isOverloaded,
    };
  });

  // 3. Cálculo de cinta industrial gris
  const gafferTape = calculateGafferTape({ floorTransitMeters: totalFloorTransitMeters });

  return {
    assignments,
    outletsStatus,
    needsAdditionalOutlet,
    recommendations,
    gafferTape,
  };
}

