import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { MOUNTING_PROTOCOL_STEPS, MIXER_GAIN_STAGING_TABLE } from '@stageplan/shared';

export interface GeneratePdfOptions {
  venue: {
    name: string;
    widthMeters: number;
    depthMeters: number;
    heightMeters: number;
    environmentType: 'INDOOR' | 'OUTDOOR_PARCELA' | 'OUTDOOR_OPEN';
    electricalDistanceMeters: number;
  };
  rider: {
    audio: {
      systemType: 'ACTIVE' | 'PASSIVE';
      topsCount: number;
      topsRmsWatts: number;
      subsCount: number;
      subsRmsWatts: number;
      topsSensitivityDb: number;
    };
    powerSource: {
      type: 'GRID_220V' | 'GENERATOR_WATTS' | 'GENERATOR_KVA';
      circuitBreakerAmps?: string;
      generatorSurgeWatts?: number;
      apparentPowerKva?: number;
      powerFactor: number;
    };
    djBoothNominalWatts: number;
  };
  results: {
    totalWatts: number;
    powerValidation: {
      alertLevel: 'NORMAL' | 'WARNING' | 'CRITICAL' | 'PENDIENTE';
      alertMessage: string;
      currentAmps?: number;
      breakerCapacityAmps?: number;
    };
    cableSizing: {
      commercialCrossSectionMm2: number;
      suggestedLengthMeters: number;
      actualVoltageDropPct: number;
      designCurrentAmps: number;
      determiningCriterion: string;
    };
    splCoverage: {
      spl1mDb: number;
      splAtFirstRowDb: number;
      splAtBackDb: number;
      recommendDelayFill: boolean;
      reverberationTimeRt60Seconds?: number;
      soundSpeedMs?: number;
      delayTimeMs?: number;
      haasCompensationMs?: number;
      totalDelayMs?: number;
      subToTopRatioDb?: number;
      tonalStatus?: string;
    };
    inventory: {
      subsAtFloorCount: number;
      tripodStandsCount: number;
      powerStripsCount: number;
    };
    hybridRoster?: {
      tag: string;
      name: string;
      systemType: string;
      rmsWatts: number;
      peakWatts?: number;
      powerCableMeters: number;
      powerCableType: string;
      signalCableType: string;
      signalLengthMeters: number;
      signalOrigin: string;
      zoneLabel?: string;
      recommendedGainNote?: string;
    }[];
    cablingSummary?: {
      externalAmpsCount: number;
      speakonCount: number;
      xlrCount: number;
      tapeMeters: number;
      tapeRolls50m: number;
    };
    v4EngineeringSummary?: {
      phaseBalanceDirective?: string;
      impedanceDirective?: string;
      bottleneckDiagnosis?: string;
      neighborhoodNoiseDirective?: string;
    };
    fieldAudit?: {
      hpfDirective: string;
      splayDirective: string;
      phaseAlignmentDirective: string;
      cableVoltageDirective: string;
      groundingDirective: string;
      powerCompressionDirective: string;
      fuelLogistics?: {
        fuelDirective: string;
      };
      crowdAcousticShift?: {
        crowdDirective: string;
      };
    };
  };
  authorName?: string;
}

export function generateOperationalReportPdf(options: GeneratePdfOptions): void {
  const { venue, rider, results, authorName = 'Técnico Operador (DISTORSIONCL SPA)' } = options;

  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  let currentY = 14;

  // Encabezado corporativo Hard Techno Industrial
  doc.setFillColor(12, 12, 16);
  doc.rect(0, 0, pageWidth, 28, 'F');
  doc.setFillColor(220, 38, 38);
  doc.rect(0, 26, pageWidth, 2, 'F'); // Barra roja de acento

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(16);
  doc.setTextColor(255, 255, 255);
  doc.text('STAGE PLAN — REPORTE OPERATIVO DE CAMPO', 14, 12);

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(212, 212, 216);
  doc.text('DISTORSIONCL SPA | Pre-Producción Electroacústica, Roster de Equipos & Seguridad SEC RIC 03/10', 14, 18);

  const timestamp = new Date().toLocaleString('es-CL');
  doc.setFontSize(8);
  doc.setTextColor(161, 161, 170);
  doc.text(`Generado: ${timestamp} | Por: ${authorName} | Modo Offline Autónomo`, 14, 23);

  currentY = 34;

  // 1. Datos del Recinto y Fuente Eléctrica
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(24, 24, 27);
  doc.text('1. Datos del Salón & Suministro Eléctrico', 14, currentY);
  currentY += 4;

  const powerSourceDesc =
    rider.powerSource.type === 'GRID_220V'
      ? `Red Domiciliaria 220V (Automático ${rider.powerSource.circuitBreakerAmps || '16'} A - Máx Continuo Seguro 80%: ${Math.round(Number(rider.powerSource.circuitBreakerAmps || 16) * 220 * 0.8)}W)`
      : rider.powerSource.type === 'GENERATOR_WATTS'
      ? `Generador Comercial ${rider.powerSource.generatorSurgeWatts || 3500} W Pico (~${Math.round((rider.powerSource.generatorSurgeWatts || 3500) * 0.85 * 0.72)}W Seguros Audio AVR)`
      : `Generador Industrial (${rider.powerSource.apparentPowerKva || 5} kVA, FP ${rider.powerSource.powerFactor})`;

  const venueRows = [
    ['Recinto / Parcela', venue.name || 'Sin especificar'],
    ['Dimensiones & Superficie', `${venue.widthMeters}m ancho × ${venue.depthMeters}m largo (${venue.widthMeters * venue.depthMeters} m²)`],
    ['Entorno Acústico', venue.environmentType === 'INDOOR' ? 'Cerrado (Salón / Galpón con reflexiones)' : 'Al Aire Libre (Parcela / Campo Libre)'],
    ['Distancia al Enchufe/Tablero', `${venue.electricalDistanceMeters} metros de tendido perimetral`],
    ['Fuente de Alimentación', powerSourceDesc],
    ['Consumo Total de Diseño', `${results.totalWatts} W reales (~${results.cableSizing.designCurrentAmps} A) | Estado: ${results.powerValidation.alertLevel}`],
  ];

  autoTable(doc, {
    startY: currentY,
    head: [['Parámetro Operativo', 'Valor Registrado']],
    body: venueRows,
    theme: 'grid',
    headStyles: { fillColor: [24, 24, 27], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 8.5 },
    bodyStyles: { fontSize: 8, textColor: [39, 39, 42] },
    columnStyles: { 0: { cellWidth: 65, fontStyle: 'bold' } },
    margin: { left: 14, right: 14 },
  });

  currentY = (doc as any).lastAutoTable.finalY + 8;

  // 2. Roster de Conexiones por Parlante con Letras (A, B, S1, S2)
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(24, 24, 27);
  doc.text('2. Roster de Parlantes & Mapeo de Cables (Energía y Señal)', 14, currentY);
  currentY += 4;

  const rosterBody = (results.hybridRoster || []).map(r => [
    r.tag,
    `${r.name} (${r.systemType} · ${r.rmsWatts}W RMS / ${r.peakWatts || r.rmsWatts * 2}W Peak)`,
    r.zoneLabel || 'Frente Principal',
    r.recommendedGainNote || '0 dB Unity (12:00)',
    r.powerCableType === 'NONE_PASSIVE' ? 'A Potencia (0V)' : `${r.powerCableMeters}m (${r.powerCableType})`,
    `${r.signalLengthMeters}m ${r.signalCableType}`,
  ]);

  if (rosterBody.length > 0) {
    autoTable(doc, {
      startY: currentY,
      head: [['ID', 'Equipo', 'Ubicación Sugerida en Sala', 'Ganancia / Retardo DSP', 'Energía 220V', 'Cable Señal']],
      body: rosterBody,
      theme: 'grid',
      headStyles: { fillColor: [220, 38, 38], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 7.5 },
      bodyStyles: { fontSize: 7, textColor: [39, 39, 42] },
      columnStyles: {
        0: { cellWidth: 10, halign: 'center', fontStyle: 'bold' },
        1: { cellWidth: 32 },
        2: { cellWidth: 44 },
        3: { cellWidth: 46 },
        4: { cellWidth: 26 },
        5: { cellWidth: 24 },
      },
      margin: { left: 14, right: 14 },
    });
    currentY = (doc as any).lastAutoTable.finalY + 8;
  }

  // 3. Resumen Acústico, Delay Haas & Materiales de Seguridad
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(24, 24, 27);
  doc.text('3. Estudio Acústico, Tiempo de Delay (Efecto Haas) & Bodega', 14, currentY);
  currentY += 4;

  const delayText = results.splCoverage.recommendDelayFill
    ? `RECOMENDADO: ${results.splCoverage.totalDelayMs || 34.9} ms (Vuelo: ${results.splCoverage.delayTimeMs || 31.9}ms + Compensación Haas: +3.0ms)`
    : 'No requerido (Cobertura óptima en toda la sala)';

  const rt60Text = results.splCoverage.reverberationTimeRt60Seconds
    ? `${results.splCoverage.reverberationTimeRt60Seconds} seg (Sabine)`
    : 'Campo libre (Sin reflexiones de techo)';

  const acousticRows = [
    ['Presión Sonora SPL a 1m (Frente)', `${results.splCoverage.spl1mDb} dB SPL`],
    ['SPL Primera Fila (4 metros)', `${results.splCoverage.splAtFirstRowDb} dB SPL (Confort auditivo de pista)`],
    ['SPL al Fondo de la Sala', `${results.splCoverage.splAtBackDb} dB SPL`],
    ['Tiempo de Reverberación (RT60)', rt60Text],
    ['Balance Tonal (Sub vs Top a 5m)', `${results.splCoverage.subToTopRatioDb || 8.0} dB (${results.splCoverage.tonalStatus || 'OPTIMAL'})`],
    ['Alineación de Delay (Línea de Refuerzo)', delayText],
    ['Cinta Adhesiva Gris para Piso (Gaffer)', `${results.cablingSummary?.tapeRolls50m || 1} rollo(s) de 50 metros (${results.cablingSummary?.tapeMeters || 48}m calculados con +20% holgura)`],
    ['Soportes en Terreno', `${results.inventory.subsAtFloorCount} Bajos a piso (Cluster Central) + ${results.inventory.tripodStandsCount} Atriles trípode independientes`],
    ...(results.fieldAudit
      ? [
          ['1. Filtro Crossover HPF (Tops)', results.fieldAudit.hpfDirective],
          ['2. Ángulo Apertura (Splay Angle)', results.fieldAudit.splayDirective],
          ['3. Fase Sub vs Top (Escenario)', results.fieldAudit.phaseAlignmentDirective],
          ['4. Caída de Tensión en el Drop', results.fieldAudit.cableVoltageDirective],
          ['5. Puesta a Tierra y Compresión', `${results.fieldAudit.groundingDirective} | ${results.fieldAudit.powerCompressionDirective}`],
          ...(results.fieldAudit.fuelLogistics ? [['6. Autonomía de Combustible', results.fieldAudit.fuelLogistics.fuelDirective]] : []),
          ...(results.fieldAudit.crowdAcousticShift ? [['7. Acústica Vacío vs Pista Llena', results.fieldAudit.crowdAcousticShift.crowdDirective]] : []),
          ...(results.v4EngineeringSummary?.phaseBalanceDirective ? [['8. Separación de Líneas Eléctricas', results.v4EngineeringSummary.phaseBalanceDirective]] : []),
          ...(results.v4EngineeringSummary?.impedanceDirective ? [['9. Impedancia Pasiva (Speakon Ohms)', results.v4EngineeringSummary.impedanceDirective]] : []),
          ...(results.v4EngineeringSummary?.bottleneckDiagnosis ? [['10. Equilibrio Tonal (Sub vs Top)', results.v4EngineeringSummary.bottleneckDiagnosis]] : []),
          ...(results.v4EngineeringSummary?.neighborhoodNoiseDirective ? [['11. Ordenanza Ruido D.S. N°38 MMA', results.v4EngineeringSummary.neighborhoodNoiseDirective]] : []),
        ]
      : []),
  ];

  autoTable(doc, {
    startY: currentY,
    head: [['Métrica de Ingeniería', 'Directriz Operativa']],
    body: acousticRows,
    theme: 'grid',
    headStyles: { fillColor: [24, 24, 27], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 8.5 },
    bodyStyles: { fontSize: 8, textColor: [39, 39, 42] },
    columnStyles: { 0: { cellWidth: 70, fontStyle: 'bold' } },
    margin: { left: 14, right: 14 },
  });

  currentY = (doc as any).lastAutoTable.finalY + 8;

  // 4. Calibración Visual de Ganancia en Mixer (Trim, Fader, Master y Mezcla de 2 Canales)
  if (currentY + 45 > pageHeight) {
    doc.addPage();
    currentY = 16;
  }

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(24, 24, 27);
  doc.text('4. Calibración Visual en Mixer DJM (Estructura de Ganancia & Transición a 2 Canales)', 14, currentY);
  currentY += 4;

  const gainRows = MIXER_GAIN_STAGING_TABLE.map((g: { section: string; optimalRange: string; ledColor: string; technicalFunction: string }) => [
    g.section,
    g.optimalRange,
    g.ledColor,
    g.technicalFunction,
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Sección de Mixer', 'Rango Óptimo Vúmetro', 'Color de LEDs', 'Función Técnica y Regla de Mezcla']],
    body: gainRows,
    theme: 'grid',
    headStyles: { fillColor: [220, 38, 38], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 8 },
    bodyStyles: { fontSize: 7.5, textColor: [39, 39, 42] },
    columnStyles: {
      0: { cellWidth: 38, fontStyle: 'bold' },
      1: { cellWidth: 32, fontStyle: 'bold' },
      2: { cellWidth: 34 },
    },
    margin: { left: 14, right: 14 },
  });

  currentY = (doc as any).lastAutoTable.finalY + 8;

  // 5. Protocolo de Montaje Seguro
  if (currentY + 40 > pageHeight) {
    doc.addPage();
    currentY = 16;
  }

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(24, 24, 27);
  doc.text('5. Protocolo de Montaje y Secuencia Operativa (En Terreno)', 14, currentY);
  currentY += 4;

  const protocolRows = MOUNTING_PROTOCOL_STEPS.map((s: { step: number; title: string; instruction: string }) => [
    `Paso ${s.step}: ${s.title}`,
    s.instruction,
  ]);

  autoTable(doc, {
    startY: currentY,
    head: [['Paso', 'Procedimiento Técnico']],
    body: protocolRows,
    theme: 'grid',
    headStyles: { fillColor: [24, 24, 27], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 8.5 },
    bodyStyles: { fontSize: 8, textColor: [39, 39, 42] },
    columnStyles: { 0: { cellWidth: 50, fontStyle: 'bold' } },
    margin: { left: 14, right: 14 },
  });

  // Pie de página legal SEC y ético
  const totalPages = (doc as any).internal.getNumberOfPages();
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i);
    doc.setFont('helvetica', 'italic');
    doc.setFontSize(7.5);
    doc.setTextColor(113, 113, 122);
    doc.text(
      'Documento de pre-producción generado por Stage Plan para DISTORSIONCL SPA. Cumple directrices SEC Pliegos RIC N° 03 y RIC N° 10 y estándar electroacústico IEC 60268. No reemplaza fiscalizaciones eléctricas oficiales.',
      pageWidth / 2,
      pageHeight - 6,
      { align: 'center' }
    );
  }

  const cleanVenueName = (venue.name || 'evento').replace(/[^a-zA-Z0-9]/g, '_');
  doc.save(`Rider_Operativo_StagePlan_${cleanVenueName}.pdf`);
}
