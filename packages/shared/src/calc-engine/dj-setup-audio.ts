// ======================================================================
// CALC-ENGINE: DJ BOOTH SETUP, BOOTH MONITORS & PASSIVE POWER AMP ROUTING
// STAGE PLAN v4.1 — DISTORSIONCL SPA
// Modela conexiones reales de Mixer (Pioneer DJM MASTER1 XLR / BOOTH TRS / LINK),
// reproductores CDJ/XDJ (RCA/Coaxial + Ethernet RJ45 + Switch),
// cajas de retorno (Activas/Pasivas) y especificación de Power para pasivos.
// ======================================================================

import type { SpeakerBatchInput } from './hybrid-roster.js';

export type DjSetupMode = 'CDJ_XDJ_MODULAR' | 'ALL_IN_ONE_CONTROLLER';
export type PlayerAudioLinkType = 'RCA_ANALOG' | 'DIGITAL_COAXIAL';

export interface DjSetupAndMonitorsInput {
  setupMode: DjSetupMode;
  playerCount: 0 | 2 | 3 | 4;
  playerAudioLinkType: PlayerAudioLinkType;
  linkEthernetProDj: boolean;
  linkMixerToEthernet: boolean;
  mixerWatts?: number;
  playerWattsEach?: number;
  // Cajas de Retorno (Booth Monitor)
  boothMonitorsCount: 0 | 1 | 2;
  boothMonitorType: 'ACTIVE' | 'PASSIVE';
  boothMonitorRmsWatts: number;
  boothMonitorImpedanceOhms?: 4 | 8;
  // Lotes de PA (para determinar Power externo requerido para Tops/Subs pasivos)
  speakerBatches: SpeakerBatchInput[];
  passiveWiringMode?: 'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK';
}

export interface PowerAmpRecommendation {
  id: string;
  targetRole: 'PASSIVE_TOPS' | 'PASSIVE_SUBS' | 'PASSIVE_BOOTH';
  title: string;
  boxesCount: number;
  totalRmsWatts: number;
  loadImpedanceOhms: number;
  recommendedAmpWattsPerChannel: number;
  recommendedMinChannels: number;
  requiredInputs: string;
  requiredOutputs: string;
  mixerConnectionChain: string;
  estimated220vDrawWatts: number;
  isImpedanceDanger: boolean;
}

export interface AudioConnectionRoute {
  id: string;
  category: 'BOOTH_PLAYER' | 'PRO_DJ_LINK' | 'BOOTH_MONITOR' | 'PA_MAIN' | 'PASSIVE_SPEAKON';
  fromPort: string;
  toPort: string;
  cableType: string;
  quantity: number;
  lengthMeters: number;
  note: string;
}

export interface DjSetupAudioAnalysis {
  djBoothTotal220vWatts: number;
  djBoothDevicesForPowerStrip: string[];
  boothMonitorsTotal220vWatts: number;
  passiveAmpsTotal220vWatts: number;
  ethernetCablesCount: number;
  requiresEthernetSwitch: boolean;
  rcaStereoCablesCount: number;
  digitalCoaxCablesCount: number;
  trsToXlrBoothCablesCount: number;
  xlrMasterCablesCount: number;
  speakonNl4CablesCount: number;
  powerAmpsRequired: PowerAmpRecommendation[];
  audioRoutes: AudioConnectionRoute[];
  alerts: string[];
  recommendations: string[];
}

function calcParallelOhms(impedances: number[]): number {
  const sumInv = impedances.reduce((acc, z) => acc + 1 / Math.max(1, z), 0);
  return sumInv > 0 ? Number((1 / sumInv).toFixed(2)) : 8;
}

/**
 * Calcula todo el ruteo de señal de audio y red de Cabina DJ, Retorno (Booth Monitor)
 * y especificación exacta de Amplificadores (Power) para parlantes pasivos.
 */
export function analyzeDjSetupAndAudioRouting(input: DjSetupAndMonitorsInput): DjSetupAudioAnalysis {
  const alerts: string[] = [];
  const recommendations: string[] = [];
  const audioRoutes: AudioConnectionRoute[] = [];
  const powerAmpsRequired: PowerAmpRecommendation[] = [];
  const djBoothDevicesForPowerStrip: string[] = [];

  const mixerWatts = input.mixerWatts ?? 45;
  const playerWatts = input.playerWattsEach ?? 35;

  let djBoothTotal220vWatts = 0;
  let ethernetCablesCount = 0;
  let requiresEthernetSwitch = false;
  let rcaStereoCablesCount = 0;
  let digitalCoaxCablesCount = 0;
  let trsToXlrBoothCablesCount = 0;
  let xlrMasterCablesCount = 0;
  let speakonNl4CablesCount = 0;

  // ------------------------------------------------------------------
  // 1. CABINA DJ: MIXER + CDJ / XDJ (O CONTROLADORA ALL-IN-ONE)
  // ------------------------------------------------------------------
  if (input.setupMode === 'ALL_IN_ONE_CONTROLLER' || input.playerCount === 0) {
    djBoothDevicesForPowerStrip.push('Controladora DJ All-in-One', 'Notebook / Soporte');
    djBoothTotal220vWatts += 120;
  } else {
    djBoothDevicesForPowerStrip.push('Mixer DJ (ej. DJM-900/750)');
    djBoothTotal220vWatts += mixerWatts;

    for (let i = 1; i <= input.playerCount; i++) {
      djBoothDevicesForPowerStrip.push(`CDJ / XDJ #${i}`);
      djBoothTotal220vWatts += playerWatts;
    }
    djBoothDevicesForPowerStrip.push('Notebook / Rekordbox (Opcional)');
    djBoothTotal220vWatts += 65;

    // Conexión de audio CDJ/XDJ -> Mixer
    if (input.playerAudioLinkType === 'DIGITAL_COAXIAL') {
      digitalCoaxCablesCount = input.playerCount;
      audioRoutes.push({
        id: 'route-cdj-dig',
        category: 'BOOTH_PLAYER',
        fromPort: `${input.playerCount}× CDJ/XDJ [DIGITAL OUT Coaxial]`,
        toPort: `Mixer [DIGITAL IN CH1–CH${input.playerCount}]`,
        cableType: 'Cable Coaxial Digital 75Ω (RCA naranja)',
        quantity: input.playerCount,
        lengthMeters: 1.5,
        note: 'Audio 100% digital sin pérdida hasta el DSP del mixer.',
      });
    } else {
      rcaStereoCablesCount = input.playerCount;
      audioRoutes.push({
        id: 'route-cdj-rca',
        category: 'BOOTH_PLAYER',
        fromPort: `${input.playerCount}× CDJ/XDJ [AUDIO OUT L/R RCA]`,
        toPort: `Mixer [CH1–CH${input.playerCount} LINE/CD IN]`,
        cableType: 'Cable Estéreo 2×RCA a 2×RCA (Rojo/Blanco)',
        quantity: input.playerCount,
        lengthMeters: 1.5,
        note: 'Conectar siempre en LINE/CD (NUNCA en PHONO, excepto tornamesas).',
      });
    }

    // Red Pro DJ Link (Ethernet RJ45)
    if (input.linkEthernetProDj && input.playerCount >= 2) {
      if (input.playerCount === 2 && !input.linkMixerToEthernet) {
        ethernetCablesCount = 1;
        requiresEthernetSwitch = false;
        audioRoutes.push({
          id: 'route-eth-direct',
          category: 'PRO_DJ_LINK',
          fromPort: 'CDJ/XDJ #1 [LINK RJ45]',
          toPort: 'CDJ/XDJ #2 [LINK RJ45]',
          cableType: 'Cable de Red Ethernet RJ45 (Cat5e/Cat6)',
          quantity: 1,
          lengthMeters: 1.5,
          note: 'Link directo entre 2 reproductores para compartir pendrive y Sync.',
        });
      } else {
        requiresEthernetSwitch = true;
        ethernetCablesCount = input.playerCount + (input.linkMixerToEthernet ? 1 : 0);
        djBoothDevicesForPowerStrip.push('Switch Ethernet 5 Puertos (Pro DJ Link)');
        djBoothTotal220vWatts += 10;

        audioRoutes.push({
          id: 'route-eth-switch',
          category: 'PRO_DJ_LINK',
          fromPort: `${input.playerCount}× CDJ/XDJ${input.linkMixerToEthernet ? ' + Mixer' : ''} [LINK RJ45]`,
          toPort: 'Switch Ethernet 5 Puertos (en Cabina)',
          cableType: 'Cable de Red Ethernet RJ45 (Cat5e/Cat6)',
          quantity: ethernetCablesCount,
          lengthMeters: 1.5,
          note: `Con ${input.playerCount} reproductores (o linkeando el Mixer) es OBLIGATORIO usar Switch Ethernet.`,
        });
        recommendations.push(
          `🌐 PRO DJ LINK (${input.playerCount}× CDJ/XDJ): Llevar Switch Ethernet 5 puertos + ${ethernetCablesCount} cables RJ45 Cat5e/Cat6 (más 1 de repuesto).`
        );
      }
    }
  }

  // ------------------------------------------------------------------
  // 2. CAJAS DE RETORNO (BOOTH MONITOR) — SIEMPRE CONECTADAS A BOOTH OUT
  // ------------------------------------------------------------------
  let boothMonitorsTotal220vWatts = 0;

  if (input.boothMonitorsCount > 0) {
    const monRms = Math.max(100, input.boothMonitorRmsWatts || 300);

    if (input.boothMonitorType === 'ACTIVE') {
      boothMonitorsTotal220vWatts = input.boothMonitorsCount * Math.round(monRms * 0.45);
      for (let i = 1; i <= input.boothMonitorsCount; i++) {
        djBoothDevicesForPowerStrip.push(`Monitor Retorno Activo #${i}`);
      }
      trsToXlrBoothCablesCount = input.boothMonitorsCount;
      audioRoutes.push({
        id: 'route-booth-act',
        category: 'BOOTH_MONITOR',
        fromPort: `Mixer [BOOTH OUT TRS 6.3mm ${input.boothMonitorsCount === 2 ? 'L/R' : 'L(Mono)'}]`,
        toPort: `${input.boothMonitorsCount}× Monitor Retorno Activo [XLR/TRS IN]`,
        cableType: 'Cable Balanceado TRS 1/4" (6.3mm) a XLR Macho',
        quantity: input.boothMonitorsCount,
        lengthMeters: 5,
        note: 'Control independiente desde perilla BOOTH MONITOR del Mixer.',
      });
    } else {
      // Retorno PASIVO: requiere Power dedicado desde BOOTH OUT
      const zBox = input.boothMonitorImpedanceOhms ?? 8;
      const totalBoothRms = monRms * input.boothMonitorsCount;
      const effectiveOhms = input.boothMonitorsCount === 2 ? zBox : zBox;
      const recWattsPerCh = Math.round(monRms * 1.5);
      const ampDraw = Math.round(totalBoothRms * 0.6);
      boothMonitorsTotal220vWatts = ampDraw;

      djBoothDevicesForPowerStrip.push('Power Retorno DJ (Booth Amp)');
      trsToXlrBoothCablesCount = input.boothMonitorsCount;
      speakonNl4CablesCount += input.boothMonitorsCount;

      powerAmpsRequired.push({
        id: 'amp-booth',
        targetRole: 'PASSIVE_BOOTH',
        title: `Power para Retorno DJ Pasivo (${input.boothMonitorsCount}× ${monRms}W @ ${zBox}Ω)`,
        boxesCount: input.boothMonitorsCount,
        totalRmsWatts: totalBoothRms,
        loadImpedanceOhms: effectiveOhms,
        recommendedAmpWattsPerChannel: recWattsPerCh,
        recommendedMinChannels: input.boothMonitorsCount === 2 ? 2 : 1,
        requiredInputs: 'Entradas balanceadas XLR / TRS 1/4" (desde BOOTH OUT del Mixer)',
        requiredOutputs: 'Salidas Speakon NL4 (Pin 1+ / 1-) hacia cada monitor',
        mixerConnectionChain: `Mixer [BOOTH OUT TRS] → Cable TRS-XLR → Power Retorno [IN] → Speakon NL4 → Monitor Pasivo`,
        estimated220vDrawWatts: ampDraw,
        isImpedanceDanger: false,
      });

      audioRoutes.push({
        id: 'route-booth-pas-sig',
        category: 'BOOTH_MONITOR',
        fromPort: 'Mixer [BOOTH OUT TRS 6.3mm]',
        toPort: 'Power Retorno [XLR/TRS IN]',
        cableType: 'Cable Balanceado TRS 1/4" a XLR Macho',
        quantity: input.boothMonitorsCount,
        lengthMeters: 3,
        note: 'Señal balanceada hacia el amplificador del retorno.',
      });
      audioRoutes.push({
        id: 'route-booth-pas-spk',
        category: 'PASSIVE_SPEAKON',
        fromPort: 'Power Retorno [Speakon OUT]',
        toPort: `${input.boothMonitorsCount}× Monitor Retorno Pasivo [Speakon IN]`,
        cableType: 'Cable de Carga Speakon NL4 (2×2.5 mm²)',
        quantity: input.boothMonitorsCount,
        lengthMeters: 5,
        note: 'Los monitores pasivos no llevan enchufe de 220V.',
      });
    }
  }

  // ------------------------------------------------------------------
  // 3. PA PRINCIPAL Y SUBS: SEPARACIÓN ACTIVO VS PASIVO + POWER EXTERNO
  // ------------------------------------------------------------------
  const activeTops = input.speakerBatches.filter((b) => b.category === 'top_box' && b.systemType === 'ACTIVE' && b.quantity > 0);
  const passiveTops = input.speakerBatches.filter((b) => b.category === 'top_box' && b.systemType === 'PASSIVE' && b.quantity > 0);
  const activeSubs = input.speakerBatches.filter((b) => b.category === 'sub_bass' && b.systemType === 'ACTIVE' && b.quantity > 0);
  const passiveSubs = input.speakerBatches.filter((b) => b.category === 'sub_bass' && b.systemType === 'PASSIVE' && b.quantity > 0);

  const activeTopsQty = activeTops.reduce((s, b) => s + b.quantity, 0);
  const passiveTopsQty = passiveTops.reduce((s, b) => s + b.quantity, 0);
  const activeSubsQty = activeSubs.reduce((s, b) => s + b.quantity, 0);
  const passiveSubsQty = passiveSubs.reduce((s, b) => s + b.quantity, 0);

  const hasAnySubs = activeSubsQty + passiveSubsQty > 0;
  const hasAnyTops = activeTopsQty + passiveTopsQty > 0;

  // Conexión desde Mixer MASTER 1 OUT (XLR L/R)
  if (hasAnySubs && hasAnyTops) {
    xlrMasterCablesCount += 2;
    audioRoutes.push({
      id: 'route-master-sub-xover',
      category: 'PA_MAIN',
      fromPort: 'Mixer [MASTER 1 OUT XLR L/R]',
      toPort: activeSubsQty > 0 ? 'Sub Activos / Crossover [XLR IN L/R]' : 'Crossover / DSP Externo [XLR IN L/R]',
      cableType: 'Cable Balanceado XLR (Canon) Macho-Hembra',
      quantity: 2,
      lengthMeters: 10,
      note: 'Aplicar corte HPF a 80–90 Hz para enviar solo medios-agudos a los Tops y graves puros a los Subs.',
    });
  } else if (hasAnyTops || hasAnySubs) {
    xlrMasterCablesCount += 2;
    audioRoutes.push({
      id: 'route-master-direct',
      category: 'PA_MAIN',
      fromPort: 'Mixer [MASTER 1 OUT XLR L/R]',
      toPort: passiveTopsQty > 0 && activeTopsQty === 0 ? 'Power Tops Pasivos [XLR IN A/B]' : 'Cajas PA Activas [XLR IN]',
      cableType: 'Cable Balanceado XLR (Canon) Macho-Hembra',
      quantity: 2,
      lengthMeters: 10,
      note: 'Señal estéreo principal balanceada desde MASTER 1 (nunca usar RCA Master2 para tiradas largas).',
    });
  }

  let passiveAmpsTotal220vWatts = 0;

  // Power para TOPS PASIVOS
  if (passiveTopsQty > 0) {
    const totalTopsRms = passiveTops.reduce((s, b) => s + b.rmsWatts * b.quantity, 0);
    const maxBoxRms = Math.max(...passiveTops.map((b) => b.rmsWatts));
    const ohmsList: number[] = [];
    passiveTops.forEach((b) => {
      for (let i = 0; i < b.quantity; i++) ohmsList.push(b.impedanceOhms || 8);
    });

    const wiring = input.passiveWiringMode ?? 'INDEPENDENT_CHANNELS';
    const perChannelLoad =
      wiring === 'PARALLEL_SPEAKON_LINK'
        ? calcParallelOhms(ohmsList.slice(0, Math.ceil(ohmsList.length / 2)))
        : ohmsList[0];

    const isDanger = perChannelLoad < 3.2;
    const recPerCh = Math.round(maxBoxRms * (perChannelLoad === 4 ? 2.2 : 1.5));
    const channelsNeeded = wiring === 'PARALLEL_SPEAKON_LINK' ? Math.max(2, Math.ceil(passiveTopsQty / 2)) : passiveTopsQty;
    const ampDraw = Math.round(totalTopsRms * 0.6);
    passiveAmpsTotal220vWatts += ampDraw;
    speakonNl4CablesCount += passiveTopsQty;

    if (hasAnySubs) {
      xlrMasterCablesCount += 2;
    }

    const mixerChain = hasAnySubs
      ? `Mixer [MASTER 1 XLR] → Crossover/Sub [HIGH-PASS OUT XLR] → Power Tops [XLR IN A/B] → Speakon NL4 → ${passiveTopsQty}× Top Pasivo`
      : `Mixer [MASTER 1 XLR] → Power Tops [XLR IN A/B] → Speakon NL4 → ${passiveTopsQty}× Top Pasivo`;

    const customAmpName = passiveTops.find((b) => b.powerAmpModel)?.powerAmpModel;
    const topsAmpTitle = customAmpName
      ? `${customAmpName} (${passiveTopsQty} caja${passiveTopsQty > 1 ? 's' : ''} · ${totalTopsRms}W RMS)`
      : `Power para Tops Pasivos (${passiveTopsQty} caja${passiveTopsQty > 1 ? 's' : ''} · ${totalTopsRms}W RMS)`;

    powerAmpsRequired.push({
      id: 'amp-tops',
      targetRole: 'PASSIVE_TOPS',
      title: topsAmpTitle,
      boxesCount: passiveTopsQty,
      totalRmsWatts: totalTopsRms,
      loadImpedanceOhms: perChannelLoad,
      recommendedAmpWattsPerChannel: recPerCh,
      recommendedMinChannels: channelsNeeded,
      requiredInputs: '2× Entradas XLR Balanceadas (o TRS) + selector Stereo / Parallel',
      requiredOutputs: `Salidas Speakon NL4 (Pin 1+/1-) estables hasta ${perChannelLoad <= 4 ? '2Ω–4Ω' : '4Ω–8Ω'}`,
      mixerConnectionChain: mixerChain,
      estimated220vDrawWatts: ampDraw,
      isImpedanceDanger: isDanger,
    });

    audioRoutes.push({
      id: 'route-spk-tops',
      category: 'PASSIVE_SPEAKON',
      fromPort: 'Power Tops [Speakon NL4 OUT]',
      toPort: `${passiveTopsQty}× Top Pasivo [Speakon IN]`,
      cableType: 'Cable Speakon NL4 (2×2.5 mm² cobre)',
      quantity: passiveTopsQty,
      lengthMeters: 15,
      note:
        wiring === 'PARALLEL_SPEAKON_LINK'
          ? `Puente paralelo (${perChannelLoad}Ω por canal). Verificar mínimo del Power.`
          : '1 canal independiente por caja (carga estable 8Ω).',
    });

    if (isDanger) {
      alerts.push(
        `🔴 IMPEDANCIA CRÍTICA EN POWER DE TOPS (${perChannelLoad}Ω < 3.2Ω): El amplificador entrará en modo PROTECT. Usa canales independientes.`
      );
    }
  }

  // Power para SUBS PASIVOS
  if (passiveSubsQty > 0) {
    const totalSubsRms = passiveSubs.reduce((s, b) => s + b.rmsWatts * b.quantity, 0);
    const maxSubRms = Math.max(...passiveSubs.map((b) => b.rmsWatts));
    const ohmsList: number[] = [];
    passiveSubs.forEach((b) => {
      for (let i = 0; i < b.quantity; i++) ohmsList.push(b.impedanceOhms || 8);
    });

    const wiring = input.passiveWiringMode ?? 'INDEPENDENT_CHANNELS';
    const perChannelLoad =
      wiring === 'PARALLEL_SPEAKON_LINK'
        ? calcParallelOhms(ohmsList.slice(0, Math.ceil(ohmsList.length / 2)))
        : ohmsList[0];

    const isDanger = perChannelLoad < 3.2;
    const recPerCh = Math.round(maxSubRms * (perChannelLoad === 4 ? 2.2 : 1.5));
    const channelsNeeded = wiring === 'PARALLEL_SPEAKON_LINK' ? Math.max(1, Math.ceil(passiveSubsQty / 2)) : passiveSubsQty;
    const ampDraw = Math.round(totalSubsRms * 0.65);
    passiveAmpsTotal220vWatts += ampDraw;
    speakonNl4CablesCount += passiveSubsQty;
    xlrMasterCablesCount += 2;

    const mixerChain = `Mixer [MASTER 1 XLR] → Crossover/DSP [LOW OUT < 90Hz XLR] → Power Subs [XLR IN] → Speakon NL4 (2×4mm²) → ${passiveSubsQty}× Sub Pasivo`;

    const customSubAmpName = passiveSubs.find((b) => b.powerAmpModel)?.powerAmpModel;
    const subsAmpTitle = customSubAmpName
      ? `${customSubAmpName} (${passiveSubsQty} sub${passiveSubsQty > 1 ? 's' : ''} · ${totalSubsRms}W RMS)`
      : `Power de Fuerza para Sub-Bajos Pasivos (${passiveSubsQty} sub${passiveSubsQty > 1 ? 's' : ''} · ${totalSubsRms}W RMS)`;

    powerAmpsRequired.push({
      id: 'amp-subs',
      targetRole: 'PASSIVE_SUBS',
      title: subsAmpTitle,
      boxesCount: passiveSubsQty,
      totalRmsWatts: totalSubsRms,
      loadImpedanceOhms: perChannelLoad,
      recommendedAmpWattsPerChannel: recPerCh,
      recommendedMinChannels: channelsNeeded,
      requiredInputs: '2× Entradas XLR Balanceadas + Filtro Low-Pass 80–100 Hz (en Power o Crossover)',
      requiredOutputs: 'Salidas Speakon NL4 de alta corriente (Pin 1+/1-, soporta 4Ω Bridge / Stereo)',
      mixerConnectionChain: mixerChain,
      estimated220vDrawWatts: ampDraw,
      isImpedanceDanger: isDanger,
    });

    audioRoutes.push({
      id: 'route-spk-subs',
      category: 'PASSIVE_SPEAKON',
      fromPort: 'Power Subs [Speakon NL4 OUT]',
      toPort: `${passiveSubsQty}× Sub Pasivo [Speakon IN]`,
      cableType: 'Cable Speakon NL4 Grueso (2×4.0 mm² baja pérdida)',
      quantity: passiveSubsQty,
      lengthMeters: 10,
      note: 'Para subgraves usar cable Speakon de 2×4.0 mm² (evita pérdida de damping factor).',
    });

    if (isDanger) {
      alerts.push(
        `🔴 IMPEDANCIA CRÍTICA EN POWER DE SUBS (${perChannelLoad}Ω < 3.2Ω): Riesgo de apagado térmico PROTECT en pleno drop.`
      );
    }
  }

  if (input.boothMonitorsCount > 0) {
    recommendations.push(
      `🎧 RETORNO DJ (BOOTH OUT): En Pioneer DJM la salida BOOTH es Jack TRS 6.3mm (1/4") balanceado, NO XLR. Lleva ${trsToXlrBoothCablesCount} cable(s) TRS a XLR Macho.`
    );
  }
  if (powerAmpsRequired.length > 0) {
    recommendations.push(
      `🔌 POWER EXTERNOS: Conecta siempre el Power a su toma eléctrica dedicada y enciéndelo AL FINAL (después del Mixer).`
    );
  }

  return {
    djBoothTotal220vWatts,
    djBoothDevicesForPowerStrip,
    boothMonitorsTotal220vWatts,
    passiveAmpsTotal220vWatts,
    ethernetCablesCount,
    requiresEthernetSwitch,
    rcaStereoCablesCount,
    digitalCoaxCablesCount,
    trsToXlrBoothCablesCount,
    xlrMasterCablesCount,
    speakonNl4CablesCount,
    powerAmpsRequired,
    audioRoutes,
    alerts,
    recommendations,
  };
}
