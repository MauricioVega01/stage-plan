import { describe, it, expect } from 'vitest';
import { analyzeDjSetupAndAudioRouting } from '../src/calc-engine/dj-setup-audio.js';
import type { SpeakerBatchInput } from '../src/calc-engine/hybrid-roster.js';

describe('DJ Setup Audio Routing, CDJ/XDJ Ethernet Link, Booth Monitors & Passive Power Amp', () => {
  const mixedBatches: SpeakerBatchInput[] = [
    {
      id: 't-pas',
      category: 'top_box',
      systemType: 'PASSIVE',
      quantity: 2,
      modelLabel: 'Top Pasivo 15"',
      coneSizeInches: 15,
      rmsWatts: 400,
      peakWatts: 800,
      impedanceOhms: 8,
    },
    {
      id: 's-pas',
      category: 'sub_bass',
      systemType: 'PASSIVE',
      quantity: 2,
      modelLabel: 'Sub Pasivo 18"',
      coneSizeInches: 18,
      rmsWatts: 800,
      peakWatts: 1600,
      impedanceOhms: 8,
    },
  ];

  it('con 2 CDJ/XDJ y link directo calcula 2 cables RCA y 1 cable Ethernet RJ45 sin switch', () => {
    const res = analyzeDjSetupAndAudioRouting({
      setupMode: 'CDJ_XDJ_MODULAR',
      playerCount: 2,
      playerAudioLinkType: 'RCA_ANALOG',
      linkEthernetProDj: true,
      linkMixerToEthernet: false,
      boothMonitorsCount: 1,
      boothMonitorType: 'ACTIVE',
      boothMonitorRmsWatts: 300,
      speakerBatches: [],
    });

    expect(res.rcaStereoCablesCount).toBe(2);
    expect(res.ethernetCablesCount).toBe(1);
    expect(res.requiresEthernetSwitch).toBe(false);
    expect(res.trsToXlrBoothCablesCount).toBe(1);
    expect(res.djBoothDevicesForPowerStrip.some((d) => d.includes('CDJ / XDJ #2'))).toBe(true);
    expect(res.djBoothDevicesForPowerStrip.some((d) => d.includes('Monitor Retorno Activo #1'))).toBe(true);
  });

  it('con 3 o 4 CDJ/XDJ exige Switch Ethernet 5 puertos y (N + mixer) cables RJ45', () => {
    const res = analyzeDjSetupAndAudioRouting({
      setupMode: 'CDJ_XDJ_MODULAR',
      playerCount: 4,
      playerAudioLinkType: 'DIGITAL_COAXIAL',
      linkEthernetProDj: true,
      linkMixerToEthernet: true,
      boothMonitorsCount: 2,
      boothMonitorType: 'ACTIVE',
      boothMonitorRmsWatts: 350,
      speakerBatches: [],
    });

    expect(res.requiresEthernetSwitch).toBe(true);
    expect(res.ethernetCablesCount).toBe(5); // 4 CDJs + 1 Mixer
    expect(res.digitalCoaxCablesCount).toBe(4);
    expect(res.trsToXlrBoothCablesCount).toBe(2);
    expect(res.djBoothDevicesForPowerStrip.some((d) => d.includes('Switch Ethernet'))).toBe(true);
  });

  it('cuando hay Tops y Subs PASIVOS calcula Power externo, salidas Speakon NL4 y cadena desde MASTER 1 XLR', () => {
    const res = analyzeDjSetupAndAudioRouting({
      setupMode: 'CDJ_XDJ_MODULAR',
      playerCount: 2,
      playerAudioLinkType: 'RCA_ANALOG',
      linkEthernetProDj: true,
      linkMixerToEthernet: false,
      boothMonitorsCount: 1,
      boothMonitorType: 'ACTIVE',
      boothMonitorRmsWatts: 300,
      speakerBatches: mixedBatches,
      passiveWiringMode: 'INDEPENDENT_CHANNELS',
    });

    const ampTops = res.powerAmpsRequired.find((a) => a.targetRole === 'PASSIVE_TOPS');
    const ampSubs = res.powerAmpsRequired.find((a) => a.targetRole === 'PASSIVE_SUBS');

    expect(ampTops).toBeDefined();
    expect(ampTops!.recommendedAmpWattsPerChannel).toBe(600); // 400W * 1.5 headroom
    expect(ampTops!.requiredOutputs).toContain('Speakon NL4');
    expect(ampTops!.mixerConnectionChain).toContain('MASTER 1 XLR');

    expect(ampSubs).toBeDefined();
    expect(ampSubs!.recommendedAmpWattsPerChannel).toBe(1200); // 800W * 1.5 headroom
    expect(res.speakonNl4CablesCount).toBe(4);
  });

  it('soporta Monitor de Retorno PASIVO generando Power Booth dedicado desde BOOTH OUT TRS', () => {
    const res = analyzeDjSetupAndAudioRouting({
      setupMode: 'ALL_IN_ONE_CONTROLLER',
      playerCount: 0,
      playerAudioLinkType: 'RCA_ANALOG',
      linkEthernetProDj: false,
      linkMixerToEthernet: false,
      boothMonitorsCount: 2,
      boothMonitorType: 'PASSIVE',
      boothMonitorRmsWatts: 250,
      boothMonitorImpedanceOhms: 8,
      speakerBatches: [],
    });

    const boothAmp = res.powerAmpsRequired.find((a) => a.targetRole === 'PASSIVE_BOOTH');
    expect(boothAmp).toBeDefined();
    expect(boothAmp!.mixerConnectionChain).toContain('BOOTH OUT TRS');
    expect(res.speakonNl4CablesCount).toBe(2);
  });
});
