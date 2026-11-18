<template>
  <div class="bg-[#0f0f13] border border-zinc-800 rounded-2xl p-6 shadow-2xl space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
      <div class="flex items-center space-x-2.5">
        <span class="inline-block w-3 h-3 bg-red-600 rounded-full animate-ping"></span>
        <h3 class="text-sm font-black tracking-wider text-white uppercase font-mono">
          Plano 2D Inteligente (Audio + Cableado Fuerza + Zapatillas + DMX)
        </h3>
      </div>
      <div class="flex flex-wrap items-center gap-1.5">
        <button
          type="button"
          @click="showHeatmap = !showHeatmap"
          class="px-2.5 py-1 rounded-lg text-[11px] font-black uppercase font-mono border transition flex items-center gap-1 cursor-pointer"
          :class="showHeatmap
            ? 'bg-red-600 text-white border-red-400 shadow-lg shadow-red-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:border-red-500'"
        >
          <span>🔥</span>
          <span>SPL</span>
        </button>
        <button
          type="button"
          @click="showPowerCables = !showPowerCables"
          class="px-2.5 py-1 rounded-lg text-[11px] font-black uppercase font-mono border transition flex items-center gap-1 cursor-pointer"
          :class="showPowerCables
            ? 'bg-amber-600 text-white border-amber-400 shadow-lg shadow-amber-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:border-amber-500'"
        >
          <span>⚡</span>
          <span>Fuerza L1/L2/L3</span>
        </button>
        <button
          type="button"
          @click="showPowerStrips = !showPowerStrips"
          class="px-2.5 py-1 rounded-lg text-[11px] font-black uppercase font-mono border transition flex items-center gap-1 cursor-pointer"
          :class="showPowerStrips
            ? 'bg-emerald-600 text-white border-emerald-400 shadow-lg shadow-emerald-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:border-emerald-500'"
        >
          <span>🔌</span>
          <span>Zapatillas ({{ powerStrips.length }})</span>
        </button>
        <button
          type="button"
          @click="showAudioSignal = !showAudioSignal"
          class="px-2.5 py-1 rounded-lg text-[11px] font-black uppercase font-mono border transition flex items-center gap-1 cursor-pointer"
          :class="showAudioSignal
            ? 'bg-cyan-600 text-white border-cyan-400 shadow-lg shadow-cyan-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:border-cyan-500'"
        >
          <span>🎛️</span>
          <span>XLR/Speakon</span>
        </button>
        <button
          v-if="hasLighting"
          type="button"
          @click="showDmxCables = !showDmxCables"
          class="px-2.5 py-1 rounded-lg text-[11px] font-black uppercase font-mono border transition flex items-center gap-1 cursor-pointer"
          :class="showDmxCables
            ? 'bg-fuchsia-600 text-white border-fuchsia-400 shadow-lg shadow-fuchsia-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:border-fuchsia-500'"
        >
          <span>🟣</span>
          <span>DMX ({{ dmxCablesCount }})</span>
        </button>
        <div class="text-[11px] text-zinc-300 font-mono bg-zinc-900 px-2.5 py-1 rounded border border-zinc-700">
          {{ venueWidth }}m × {{ venueDepth }}m
        </div>
      </div>
    </div>

    <!-- Contenedor SVG reactivo -->
    <div class="relative w-full aspect-[4/3] bg-[#050505] rounded-xl overflow-hidden border-2 border-zinc-800 flex items-center justify-center p-3 shadow-inner">
      <svg
        :viewBox="`0 0 ${viewBoxWidth} ${viewBoxHeight}`"
        class="w-full h-full select-none"
        preserveAspectRatio="xMidYMid meet"
      >
        <!-- Grilla y Gradientes para Mapa de Calor SPL -->
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1c1c24" stroke-width="0.8" />
          </pattern>
          <radialGradient id="splHeatFront" cx="50%" cy="20%" r="65%">
            <stop offset="0%" stop-color="#ef4444" stop-opacity="0.42" />
            <stop offset="26%" stop-color="#f59e0b" stop-opacity="0.28" />
            <stop offset="62%" stop-color="#10b981" stop-opacity="0.22" />
            <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.12" />
          </radialGradient>
          <radialGradient id="splHeatDelay" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.34" />
            <stop offset="70%" stop-color="#10b981" stop-opacity="0.12" />
            <stop offset="100%" stop-color="#3b82f6" stop-opacity="0" />
          </radialGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        <!-- Perímetro del Recinto con borde acerado -->
        <rect
          :x="margin"
          :y="margin"
          :width="contentWidth"
          :height="contentHeight"
          fill="none"
          stroke="#3f3f46"
          stroke-width="2.5"
          stroke-dasharray="6 3"
          rx="6"
        />

        <!-- CAPA 1: MAPA DE CALOR SPL -->
        <g v-if="showHeatmap">
          <rect
            :x="margin + 2"
            :y="margin + 2"
            :width="contentWidth - 4"
            :height="contentHeight - 4"
            fill="url(#splHeatFront)"
            rx="5"
          />
          <circle
            v-for="(top, idx) in topPositions.filter(t => t.isDelay)"
            :key="`heat-delay-${idx}`"
            :cx="top.x"
            :cy="top.y + 28"
            r="68"
            fill="url(#splHeatDelay)"
          />
          <rect :x="contentWidth / 2 + margin - 78" :y="margin + 92" width="156" height="14" fill="#450a0a" fill-opacity="0.82" stroke="#ef4444" stroke-width="0.8" rx="3" />
          <text :x="contentWidth / 2 + margin" :y="margin + 101" fill="#fca5a5" font-size="6.4" font-weight="900" font-family="monospace" text-anchor="middle">
            ZONA ROJA (&gt;105 dB): PELIGRO AUDITIVO (&lt;2.5m)
          </text>

          <rect :x="contentWidth / 2 + margin - 88" :y="margin + contentHeight * 0.56" width="176" height="15" fill="#022c22" fill-opacity="0.85" stroke="#10b981" stroke-width="0.9" rx="3" />
          <text :x="contentWidth / 2 + margin" :y="margin + contentHeight * 0.56 + 10" fill="#6ee7b7" font-size="6.7" font-weight="900" font-family="monospace" text-anchor="middle">
            SWEET SPOT PISTA (96–102 dBA): IMPACTO LIMPIO
          </text>
        </g>

        <!-- CAPA 2: CABLEADO ELÉCTRICO ORTOGONAL (L1 SUBS / L2 TOPS+CABINA / L3 LUCES+HUMO) -->
        <g v-if="showPowerCables">
          <g v-for="cable in powerCablePaths" :key="cable.id">
            <polyline
              :points="cable.points"
              fill="none"
              :stroke="cable.stroke"
              :stroke-width="cable.width"
              stroke-linecap="round"
              stroke-linejoin="round"
              :stroke-dasharray="cable.dash"
              opacity="0.92"
            />
            <rect
              :x="cable.labelX - 30"
              :y="cable.labelY - 6"
              width="60"
              height="11"
              fill="#09090b"
              fill-opacity="0.9"
              :stroke="cable.stroke"
              stroke-width="0.7"
              rx="2"
            />
            <text
              :x="cable.labelX"
              :y="cable.labelY + 2"
              :fill="cable.stroke"
              font-size="5.5"
              font-weight="900"
              font-family="monospace"
              text-anchor="middle"
            >
              {{ cable.shortLabel }}
            </text>
          </g>
        </g>

        <!-- CAPA 3: SEÑAL DE AUDIO (XLR CIAN / SPEAKON ÁMBAR) -->
        <g v-if="showAudioSignal">
          <g v-for="sig in audioSignalPaths" :key="sig.id">
            <polyline
              :points="sig.points"
              fill="none"
              :stroke="sig.stroke"
              :stroke-width="sig.width"
              :stroke-dasharray="sig.dash"
              opacity="0.85"
            />
          </g>
        </g>

        <!-- CAPA 4: CADENA FÍSICA DMX DESDE DMX OUT (CABINA) -->
        <g v-if="showDmxCables && hasLighting">
          <g v-for="dmx in dmxPaths" :key="dmx.id">
            <polyline
              :points="dmx.points"
              fill="none"
              stroke="#e879f9"
              stroke-width="1.8"
              stroke-dasharray="4 2"
              opacity="0.92"
            />
            <rect
              :x="dmx.labelX - 20"
              :y="dmx.labelY - 5"
              width="40"
              height="10"
              fill="#2e1065"
              fill-opacity="0.92"
              stroke="#e879f9"
              stroke-width="0.7"
              rx="2"
            />
            <text
              :x="dmx.labelX"
              :y="dmx.labelY + 2"
              fill="#f5d0fe"
              font-size="5.3"
              font-weight="900"
              font-family="monospace"
              text-anchor="middle"
            >
              {{ dmx.label }}
            </text>
          </g>

          <!-- Nodos visuales de zonas de iluminación / humo -->
          <g v-for="lz in lightingZoneNodes" :key="lz.zone">
            <rect
              :x="lz.x - 28"
              :y="lz.y - 10"
              width="56"
              height="20"
              :fill="lz.hasThermal ? '#431407' : '#3b0764'"
              :stroke="lz.hasThermal ? '#fb923c' : '#e879f9'"
              stroke-width="1.5"
              rx="4"
            />
            <text :x="lz.x" :y="lz.y - 1" fill="#ffffff" font-size="6.2" font-weight="900" font-family="monospace" text-anchor="middle">
              {{ lz.icon }} {{ lz.shortTitle }}
            </text>
            <text :x="lz.x" :y="lz.y + 7" :fill="lz.hasThermal ? '#fed7aa' : '#f5d0fe'" font-size="5.3" font-weight="700" font-family="monospace" text-anchor="middle">
              {{ lz.fixtureCount }}u · {{ lz.totalWatts }}W
            </text>
          </g>
        </g>

        <!-- Enchufe / Tablero Eléctrico (L1 Subs / L2 Tops / L3 Luces) -->
        <g :transform="`translate(${boardPoint.x - 29}, ${boardPoint.y - 14})`">
          <rect width="58" height="28" fill="#450a0a" stroke="#dc2626" stroke-width="1.8" rx="4" />
          <text x="29" y="11" fill="#fca5a5" font-size="7.2" font-weight="900" font-family="monospace" text-anchor="middle">⚡ 220V SEC</text>
          <text x="29" y="21" fill="#fde047" font-size="5.8" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ hasLighting ? 'L1 / L2 / L3' : 'L1 SUB / L2 TOP' }}
          </text>
        </g>

        <!-- Zona Escenario / Cabina DJ + Salida DMX OUT -->
        <rect
          :x="boothPoint.x - 54"
          :y="boothPoint.y - 13"
          width="108"
          height="26"
          fill="#1c1917"
          stroke="#dc2626"
          stroke-width="2"
          rx="4"
        />
        <text
          :x="boothPoint.x"
          :y="boothPoint.y + 2"
          fill="#ffffff"
          font-size="8.8"
          font-weight="900"
          font-family="monospace"
          text-anchor="middle"
        >
          CABINA DJ (0 dB)
        </text>
        <g v-if="hasLighting">
          <rect
            :x="boothPoint.x + 28"
            :y="boothPoint.y + 9"
            width="38"
            height="10"
            fill="#581c87"
            stroke="#e879f9"
            stroke-width="0.9"
            rx="2"
          />
          <text :x="boothPoint.x + 47" :y="boothPoint.y + 16" fill="#fae8ff" font-size="5.2" font-weight="900" font-family="monospace" text-anchor="middle">
            DMX OUT
          </text>
        </g>

        <!-- Primera Fila de Audiencia (4 metros) -->
        <line
          :x1="margin + 6"
          :y1="firstRowY"
          :x2="contentWidth + margin - 6"
          :y2="firstRowY"
          stroke="#f59e0b"
          stroke-width="1.2"
          stroke-opacity="0.6"
          stroke-dasharray="4 3"
        />
        <text
          :x="contentWidth + margin - 10"
          :y="firstRowY - 4"
          fill="#fbbf24"
          font-size="7"
          font-weight="700"
          font-family="monospace"
          text-anchor="end"
        >
          PRIMERA FILA (4m · ~106 dBA)
        </text>

        <!-- Líneas Guía de Torres de Delay -->
        <g v-for="ring in delayRings" :key="ring.id">
          <line
            :x1="margin + 8"
            :y1="ring.svgY"
            :x2="contentWidth + margin - 8"
            :y2="ring.svgY"
            stroke="#10b981"
            stroke-width="1.3"
            stroke-opacity="0.65"
            stroke-dasharray="5 3"
          />
          <rect
            :x="contentWidth / 2 + margin - 72"
            :y="ring.svgY - 9"
            width="144"
            height="15"
            fill="#022c22"
            stroke="#10b981"
            stroke-width="1"
            rx="3"
          />
          <text
            :x="contentWidth / 2 + margin"
            :y="ring.svgY + 1.5"
            fill="#6ee7b7"
            font-size="7"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ ring.label }}
          </text>
        </g>

        <!-- Sub Bajos a Piso en MONO CLUSTER CENTRAL -->
        <g v-if="subPositions.length > 0">
          <rect
            :x="contentWidth / 2 + margin - (subPositions.length * 16 + 12)"
            :y="margin + 38"
            :width="subPositions.length * 32 + 24"
            height="34"
            fill="#1e1b4b"
            fill-opacity="0.35"
            stroke="#8b5cf6"
            stroke-width="1"
            stroke-dasharray="2 2"
            rx="4"
          />
          <text
            :x="contentWidth / 2 + margin"
            :y="margin + 82"
            fill="#c4b5fd"
            font-size="6.5"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            SUB CLUSTER CENTRAL (+6 dB ACOPLADOS · 0 TUBOS)
          </text>
        </g>

        <g v-for="(sub, idx) in subPositions" :key="`sub-${idx}`">
          <rect
            :x="sub.x - 13"
            :y="sub.y - 12"
            width="26"
            height="24"
            :fill="sub.systemType === 'ACTIVE' ? '#3b0764' : '#083344'"
            :stroke="sub.systemType === 'ACTIVE' ? '#a855f7' : '#06b6d4'"
            stroke-width="2"
            rx="3"
          />
          <text :x="sub.x" :y="sub.y - 1" fill="#ffffff" font-size="8" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ sub.tag }}
          </text>
          <text :x="sub.x" :y="sub.y + 8" :fill="sub.systemType === 'ACTIVE' ? '#e9d5ff' : '#a5f3fc'" font-size="5.6" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ sub.rmsWatts }}W
          </text>
        </g>

        <!-- Cajas Acústicas en Atriles (PA Frontal + Torres Delay) -->
        <g v-for="(top, idx) in topPositions" :key="`top-${idx}`">
          <polygon
            :points="`${top.x},${top.y} ${top.x - 18},${Math.min(margin + contentHeight - 4, top.y + 42)} ${top.x + 18},${Math.min(margin + contentHeight - 4, top.y + 42)}`"
            :fill="top.isDelay ? '#10b981' : '#ef4444'"
            fill-opacity="0.14"
          />
          <circle
            :cx="top.x"
            :cy="top.y"
            r="14"
            :fill="top.systemType === 'PASSIVE' ? '#78350f' : (top.isDelay ? '#064e3b' : '#7f1d1d')"
            :stroke="top.systemType === 'PASSIVE' ? '#f59e0b' : (top.isDelay ? '#10b981' : '#ef4444')"
            stroke-width="2.2"
          />
          <text :x="top.x" :y="top.y + 1" fill="#ffffff" font-size="9" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ top.tag }}
          </text>
          <text :x="top.x" :y="top.y + 9" fill="#fde047" font-size="5.4" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ top.systemType === 'ACTIVE' ? 'ACT' : 'PAS' }}
          </text>
          <text
            :x="top.x"
            :y="top.y + 23"
            :fill="top.systemType === 'PASSIVE' ? '#fcd34d' : (top.isDelay ? '#6ee7b7' : '#fca5a5')"
            font-size="6.4"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ top.shortRole }}
          </text>
        </g>

        <!-- CAPA 5: ZAPATILLAS MULTICONTACTO (Z1, Z2, Z3...) -->
        <g v-if="showPowerStrips">
          <g v-for="zNode in powerStripNodes" :key="zNode.id">
            <rect
              :x="zNode.x - 27"
              :y="zNode.y - 10"
              width="54"
              height="20"
              :fill="zNode.status === 'OVERLOAD' ? '#7f1d1d' : zNode.status === 'WARNING' ? '#78350f' : '#064e3b'"
              :stroke="zNode.status === 'OVERLOAD' ? '#f87171' : zNode.status === 'WARNING' ? '#fbbf24' : '#34d399'"
              stroke-width="1.5"
              rx="4"
            />
            <text :x="zNode.x" :y="zNode.y - 1" fill="#ffffff" font-size="6.1" font-weight="900" font-family="monospace" text-anchor="middle">
              🔌 {{ zNode.id }} ({{ zNode.ratingAmps }}A)
            </text>
            <text :x="zNode.x" :y="zNode.y + 7" fill="#d1fae5" font-size="5.2" font-weight="800" font-family="monospace" text-anchor="middle">
              {{ zNode.usedSockets }}/{{ zNode.totalSockets }} bocas · {{ zNode.loadWatts }}W
            </text>
          </g>
        </g>

        <!-- Etiqueta Fondo de Pista -->
        <text
          :x="contentWidth / 2 + margin"
          :y="margin + contentHeight - 6"
          fill="#a1a1aa"
          font-size="7.2"
          font-weight="700"
          font-family="monospace"
          text-anchor="middle"
        >
          FONDO DE PISTA ({{ venueDepth }}m) — CABLEADO PERIMETRAL SIN CRUCES CENTRALES
        </text>
      </svg>
    </div>

    <!-- Leyenda de Capas de Cableado y Equipos -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 pt-1 text-[11px] font-mono">
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-4 h-1.5 bg-red-500 rounded shrink-0"></span>
        <span class="text-zinc-200 font-bold">L1 Fuerza Subs</span>
      </div>
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-4 h-1.5 bg-amber-400 rounded shrink-0"></span>
        <span class="text-zinc-200 font-bold">L2 Tops/Cabina</span>
      </div>
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-4 h-1.5 bg-orange-500 rounded shrink-0"></span>
        <span class="text-zinc-200 font-bold">L3 Luces/Humo</span>
      </div>
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-4 h-1.5 bg-cyan-400 rounded shrink-0"></span>
        <span class="text-zinc-200 font-bold">Audio XLR</span>
      </div>
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-4 h-1.5 bg-fuchsia-400 rounded shrink-0"></span>
        <span class="text-zinc-200 font-bold">Cadena DMX</span>
      </div>
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-3.5 h-3.5 bg-emerald-700 border border-emerald-400 rounded-sm shrink-0"></span>
        <span class="text-zinc-200 font-bold">Zapatillas Z1..Z</span>
      </div>
    </div>

    <!-- Resumen rápido debajo del mapa: Zapatillas y Alargadores -->
    <div v-if="powerPlan && powerPlan.powerStrips.length > 0" class="bg-[#0a0a0e] border border-zinc-800 rounded-xl p-3.5 space-y-2.5 font-mono text-xs">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-emerald-400 font-black uppercase">
          🔌 Resumen Rápido en Mapa: {{ powerPlan.totalSocketsRequired }} bocas totales · {{ powerPlan.totalPowerStripsCount }} zapatilla(s) · {{ powerPlan.extensionCords.length }} alargador(es)
        </span>
        <span v-if="powerPlan.passiveBoxesWithout220vCount > 0" class="text-amber-300 text-[11px]">
          ({{ powerPlan.passiveBoxesWithout220vCount }} caja(s) pasiva(s) van sin 220V al trípode, solo Speakon)
        </span>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
        <div
          v-for="z in powerPlan.powerStrips"
          :key="`mini-${z.id}`"
          class="bg-[#14141c] border rounded-lg p-2.5 space-y-1"
          :class="z.status === 'OVERLOAD' ? 'border-red-500' : z.status === 'WARNING' ? 'border-amber-500' : 'border-zinc-800'"
        >
          <div class="flex items-center justify-between">
            <span class="font-black text-white">{{ z.id }} · {{ z.ratingAmps }}A ({{ z.usedSockets }}/{{ z.totalSockets }} bocas)</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded font-bold" :class="z.line === 'LINE_1_SUBS' ? 'bg-red-950 text-red-300' : z.line === 'LINE_3_LIGHTING_FX' ? 'bg-orange-950 text-orange-300' : 'bg-amber-950 text-amber-300'">
              {{ z.line === 'LINE_1_SUBS' ? 'L1' : z.line === 'LINE_3_LIGHTING_FX' ? 'L3' : 'L2' }} · {{ z.loadWatts }}W
            </span>
          </div>
          <div class="text-[11px] text-zinc-400 truncate">{{ z.label }}</div>
          <div class="text-[10px] text-zinc-500 truncate">{{ z.connectedDevices.join(' · ') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import type { PowerDistributionPlan, LightingAndDmxAnalysis } from '@stageplan/shared';

export interface MapRosterNode {
  tag: string;
  category: 'top_box' | 'sub_bass' | 'dj_booth' | 'lighting' | 'other';
  systemType: 'ACTIVE' | 'PASSIVE';
  rmsWatts: number;
  peakWatts?: number;
  delayMs?: number;
  posY?: number;
}

const props = withDefaults(
  defineProps<{
    venueWidth: number;
    venueDepth: number;
    subsCount: number;
    topsCount: number;
    topsSystemType?: 'ACTIVE' | 'PASSIVE';
    subsSystemType?: 'ACTIVE' | 'PASSIVE';
    temperatureCelsius?: number;
    rosterNodes?: MapRosterNode[];
    powerPlan?: PowerDistributionPlan | null;
    lightingAnalysis?: LightingAndDmxAnalysis | null;
  }>(),
  {
    venueWidth: 10,
    venueDepth: 16,
    subsCount: 0,
    topsCount: 0,
    topsSystemType: 'ACTIVE',
    subsSystemType: 'ACTIVE',
    temperatureCelsius: 20,
    rosterNodes: () => [],
    powerPlan: null,
    lightingAnalysis: null,
  }
);

const showHeatmap = ref(true);
const showPowerCables = ref(true);
const showPowerStrips = ref(true);
const showAudioSignal = ref(true);
const showDmxCables = ref(true);

const viewBoxWidth = 420;
const viewBoxHeight = 320;
const margin = 18;

const contentWidth = computed(() => viewBoxWidth - margin * 2);
const contentHeight = computed(() => viewBoxHeight - margin * 2);

const boardPoint = computed(() => ({ x: margin + 37, y: margin + 22 }));
const boothPoint = computed(() => ({ x: contentWidth.value / 2 + margin, y: margin + 21 }));

const powerStrips = computed(() => props.powerPlan?.powerStrips ?? []);
const hasLighting = computed(() => (props.lightingAnalysis?.totalFixtureUnits ?? 0) > 0);
const dmxCablesCount = computed(() => props.lightingAnalysis?.totalDmxCablesCount ?? 0);

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];

const subPositions = computed(() => {
  const customSubs = (props.rosterNodes || []).filter((n) => n.category === 'sub_bass');
  const count = customSubs.length > 0 ? customSubs.length : props.subsCount || 0;
  if (count <= 0) return [];

  const positions = [];
  const y = margin + 55;
  const centerX = contentWidth.value / 2 + margin;
  const stepX = 30;
  const startX = centerX - ((count - 1) * stepX) / 2;

  for (let i = 0; i < count; i++) {
    const node = customSubs[i];
    positions.push({
      x: startX + i * stepX,
      y,
      tag: node?.tag || `S${i + 1}`,
      systemType: node?.systemType || props.subsSystemType,
      rmsWatts: node?.rmsWatts || 800,
    });
  }
  return positions;
});

const topPositions = computed(() => {
  const customTops = (props.rosterNodes || []).filter((n) => n.category === 'top_box');
  const count = customTops.length > 0 ? customTops.length : props.topsCount || 0;
  if (count <= 0) return [];

  const depth = Math.max(8, props.venueDepth || 16);
  const soundSpeed = 331.3 + 0.606 * (props.temperatureCelsius || 20);
  const positions = [];

  for (let i = 0; i < count; i++) {
    const node = customTops[i];
    const tag = node?.tag || LETTERS[i] || `T${i + 1}`;
    const sysType = node?.systemType || props.topsSystemType;
    const rmsW = node?.rmsWatts || 500;
    const isLeft = i % 2 === 0;
    const pairIndex = Math.floor(i / 2);

    if (pairIndex === 0) {
      const x = isLeft ? margin + 46 : contentWidth.value + margin - 46;
      const y = margin + 62;
      positions.push({
        x,
        y,
        tag,
        systemType: sysType,
        rmsWatts: rmsW,
        isDelay: false,
        isLeft,
        shortRole: `${rmsW}W · 0dB`,
      });
    } else {
      const ringRatio = pairIndex === 1 ? 0.56 : pairIndex === 2 ? 0.76 : 0.88;
      const realDistMeters = Number((depth * ringRatio).toFixed(1));
      const acousticDist = Math.max(4, realDistMeters - 2.0);
      const delayMs = node?.delayMs ?? Number(((acousticDist / soundSpeed) * 1000 + 3.0).toFixed(1));

      const x = isLeft ? margin + 32 : contentWidth.value + margin - 32;
      const y = margin + contentHeight.value * ringRatio;

      positions.push({
        x,
        y,
        tag,
        systemType: sysType,
        rmsWatts: rmsW,
        isDelay: true,
        isLeft,
        shortRole: `${rmsW}W (+${delayMs}ms)`,
      });
    }
  }
  return positions;
});

const delayRings = computed(() => {
  const customTops = (props.rosterNodes || []).filter((n) => n.category === 'top_box');
  const count = customTops.length > 0 ? customTops.length : props.topsCount || 0;
  if (count <= 2) return [];

  const depth = Math.max(8, props.venueDepth || 16);
  const soundSpeed = 331.3 + 0.606 * (props.temperatureCelsius || 20);
  const rings = [];

  const maxPairs = Math.ceil(count / 2);
  for (let p = 1; p < maxPairs; p++) {
    const ringRatio = p === 1 ? 0.56 : p === 2 ? 0.76 : 0.88;
    const realDistMeters = Number((depth * ringRatio).toFixed(1));
    const acousticDist = Math.max(4, realDistMeters - 2.0);
    const delayMs = Number(((acousticDist / soundSpeed) * 1000 + 3.0).toFixed(1));
    rings.push({
      id: `ring-${p}`,
      svgY: margin + contentHeight.value * ringRatio,
      label: `ZONA DELAY ${p} (${realDistMeters}m · +${delayMs} ms)`,
    });
  }
  return rings;
});

const firstRowY = computed(() => {
  const depth = Math.max(8, props.venueDepth || 16);
  const ratio = Math.min(Math.max(4 / depth, 0.34), 0.44);
  return margin + contentHeight.value * ratio;
});

// Posiciones de Zapatillas Multicontacto en el Plano 2D
const powerStripNodes = computed(() => {
  const list = powerStrips.value;
  const cx = boothPoint.value.x;
  let lightIdx = 0;
  let subIdx = 0;
  let boothIdx = 0;

  return list.map((z) => {
    let x = cx;
    let y = margin + 122;

    if (z.zone === 'DJ_BOOTH') {
      x = cx - 82 + boothIdx * 164;
      y = margin + 30;
      boothIdx++;
    } else if (z.zone === 'SUB_CLUSTER') {
      x = cx + (subIdx === 0 ? -68 : 68);
      y = margin + 72;
      subIdx++;
    } else if (z.zone === 'DELAY_ZONE') {
      x = margin + 40;
      y = margin + contentHeight.value * 0.68;
    } else if (z.zone === 'LIGHTING_FX') {
      x = contentWidth.value + margin - 46;
      y = margin + 28 + lightIdx * 24;
      lightIdx++;
    }

    return { ...z, x, y };
  });
});

// Zonas de iluminación y efectos sobre el mapa
const lightingZoneNodes = computed(() => {
  const zones = props.lightingAnalysis?.zones ?? [];
  const cx = boothPoint.value.x;
  return zones.map((z) => {
    let x = cx;
    let y = margin + 118;
    let icon = '💡';
    let shortTitle = 'LUCES';

    if (z.zone === 'TRUSS_LEFT') {
      x = margin + 52;
      y = margin + 114;
      icon = '💡';
      shortTitle = 'TRUSS IZQ';
    } else if (z.zone === 'TRUSS_RIGHT') {
      x = contentWidth.value + margin - 52;
      y = margin + 114;
      icon = '💡';
      shortTitle = 'TRUSS DER';
    } else if (z.zone === 'CENTER_BOOTH') {
      x = cx + 96;
      y = margin + 52;
      icon = '✨';
      shortTitle = 'FRENTE';
    } else if (z.zone === 'FLOOR') {
      x = cx - 96;
      y = margin + 114;
      icon = '🌫️';
      shortTitle = z.hasThermalLoad ? 'HUMO/FX' : 'PISO FX';
    }

    return {
      zone: z.zone,
      x,
      y,
      icon,
      shortTitle,
      fixtureCount: z.fixtureCount,
      totalWatts: z.totalWatts,
      hasThermal: z.hasThermalLoad,
      dmxCount: z.dmxCount,
    };
  });
});

// Trazados ortogonales (Manhattan / perimetrales) de cableado de fuerza
const powerCablePaths = computed(() => {
  const paths: Array<{
    id: string;
    points: string;
    stroke: string;
    width: number;
    dash: string;
    labelX: number;
    labelY: number;
    shortLabel: string;
  }> = [];

  const bx = boardPoint.value.x;
  const by = boardPoint.value.y;
  const exts = props.powerPlan?.extensionCords ?? [];

  // 1. Troncales a zapatillas (Cabina, Subs, Luces/Humo)
  const boothExt = exts.find((e) => e.zone === 'DJ_BOOTH');
  const zBooth = powerStripNodes.value.find((z) => z.zone === 'DJ_BOOTH');
  if (boothExt && zBooth) {
    paths.push({
      id: 'pwr-booth',
      points: `${bx},${by + 14} ${bx},${zBooth.y} ${zBooth.x - 27},${zBooth.y}`,
      stroke: '#facc15',
      width: 2.2,
      dash: 'none',
      labelX: (bx + zBooth.x) / 2 - 4,
      labelY: zBooth.y - 10,
      shortLabel: `L2 ${boothExt.crossSectionMm2}mm²·${boothExt.lengthMeters}m`,
    });
  }

  const subExt = exts.find((e) => e.zone === 'SUB_CLUSTER');
  const zSub = powerStripNodes.value.find((z) => z.zone === 'SUB_CLUSTER');
  if (subExt && zSub) {
    paths.push({
      id: 'pwr-sub',
      points: `${bx + 10},${by + 14} ${bx + 10},${zSub.y} ${zSub.x - 27},${zSub.y}`,
      stroke: '#ef4444',
      width: 2.6,
      dash: 'none',
      labelX: bx + 48,
      labelY: zSub.y + 11,
      shortLabel: `L1 ${subExt.crossSectionMm2}mm²·${subExt.lengthMeters}m`,
    });
  }

  // 2. Alargadores hacia Tops Activos (cajas pasivas NO llevan 220V al trípode)
  for (const top of topPositions.value) {
    if (top.systemType !== 'ACTIVE') continue;
    const ext = exts.find((e) => e.to.includes(top.tag));
    if (!top.isDelay) {
      if (top.isLeft) {
        paths.push({
          id: `pwr-top-${top.tag}`,
          points: `${bx - 12},${by + 14} ${bx - 12},${top.y} ${top.x - 14},${top.y}`,
          stroke: '#facc15',
          width: 1.8,
          dash: 'none',
          labelX: margin + 32,
          labelY: (by + top.y) / 2 + 8,
          shortLabel: ext ? `${ext.crossSectionMm2}mm²·${ext.lengthMeters}m` : 'L2 220V',
        });
      } else {
        // Borde superior por detrás de cabina hasta Top derecho
        const topEdgeY = margin + 4;
        paths.push({
          id: `pwr-top-${top.tag}`,
          points: `${bx + 29},${topEdgeY} ${top.x},${topEdgeY} ${top.x},${top.y - 14}`,
          stroke: '#facc15',
          width: 1.8,
          dash: 'none',
          labelX: top.x - 36,
          labelY: topEdgeY + 8,
          shortLabel: ext ? `${ext.crossSectionMm2}mm²·${ext.lengthMeters}m` : 'L2 220V',
        });
      }
    } else {
      // Perimetral por muros laterales para Torres Delay (nunca cruzando centro pista)
      const wallX = top.isLeft ? margin + 5 : contentWidth.value + margin - 5;
      const routePts = top.isLeft
        ? `${bx - 18},${by + 14} ${wallX},${by + 14} ${wallX},${top.y} ${top.x - 14},${top.y}`
        : `${bx + 29},${margin + 4} ${wallX},${margin + 4} ${wallX},${top.y} ${top.x + 14},${top.y}`;
      paths.push({
        id: `pwr-delay-${top.tag}`,
        points: routePts,
        stroke: '#eab308',
        width: 1.7,
        dash: '5 2',
        labelX: top.isLeft ? margin + 34 : contentWidth.value + margin - 34,
        labelY: top.y - 18,
        shortLabel: ext ? `${ext.crossSectionMm2}mm²·${ext.lengthMeters}m` : 'L2 Delay',
      });
    }
  }

  // 3. Línea 3 hacia Iluminación / Humo (borde superior diferenciado en naranja)
  const l3Exts = exts.filter((e) => e.line === 'LINE_3_LIGHTING_FX');
  const zLights = powerStripNodes.value.filter((z) => z.line === 'LINE_3_LIGHTING_FX');
  l3Exts.forEach((ext, idx) => {
    const zTarget = zLights[idx] || zLights[0];
    if (!zTarget) return;
    const railY = margin + 8 + idx * 4;
    paths.push({
      id: `pwr-l3-${idx}`,
      points: `${bx + 29},${railY} ${zTarget.x - 27},${railY} ${zTarget.x - 27},${zTarget.y}`,
      stroke: '#f97316',
      width: 2.2,
      dash: 'none',
      labelX: (bx + zTarget.x) / 2 + 44,
      labelY: railY + 9 + idx * 11,
      shortLabel: `L3 ${ext.crossSectionMm2}mm²·${ext.lengthMeters}m`,
    });
  });

  return paths;
});

// Trazados de señal de audio (XLR cian para activos / Speakon ámbar para pasivos)
const audioSignalPaths = computed(() => {
  const cx = boothPoint.value.x;
  const cy = boothPoint.value.y + 13;
  const list: Array<{ id: string; points: string; stroke: string; width: number; dash: string }> = [];

  for (const top of topPositions.value) {
    const isPassive = top.systemType === 'PASSIVE';
    list.push({
      id: `sig-top-${top.tag}`,
      points: `${cx},${cy} ${top.x},${cy + 12} ${top.x},${top.y - 14}`,
      stroke: isPassive ? '#f59e0b' : '#22d3ee',
      width: isPassive ? 2.0 : 1.3,
      dash: isPassive ? 'none' : '3 3',
    });
  }

  for (const sub of subPositions.value) {
    const isPassive = sub.systemType === 'PASSIVE';
    list.push({
      id: `sig-sub-${sub.tag}`,
      points: `${cx},${cy} ${sub.x},${sub.y - 12}`,
      stroke: isPassive ? '#f59e0b' : '#22d3ee',
      width: isPassive ? 1.8 : 1.2,
      dash: isPassive ? 'none' : '2 2',
    });
  }

  return list;
});

// Trazados físicos DMX desde DMX OUT en Cabina hacia cada zona con equipos DMX
const dmxPaths = computed(() => {
  const analysis = props.lightingAnalysis;
  if (!analysis || analysis.dmxControlledUnits === 0) return [];

  const startX = boothPoint.value.x + 47;
  const startY = boothPoint.value.y + 19;
  const dmxZones = lightingZoneNodes.value.filter((z) => z.dmxCount > 0);
  const paths: Array<{ id: string; points: string; labelX: number; labelY: number; label: string }> = [];

  if (analysis.needsDmxSplitter) {
    // Ramas independientes desde DMX OUT / Splitter en cabina
    for (const lz of dmxZones) {
      const trunkRun = analysis.dmxRuns.find((r) => r.zone === lz.zone && r.kind === 'TRUNK');
      const len = trunkRun?.lengthMeters ?? 5;
      paths.push({
        id: `dmx-split-${lz.zone}`,
        points: `${startX},${startY} ${startX},${lz.y - 16} ${lz.x},${lz.y - 16} ${lz.x},${lz.y - 10}`,
        labelX: (startX + lz.x) / 2,
        labelY: lz.y - 16,
        label: `DMX ${len}m`,
      });
    }
  } else {
    // Cadena daisy-chain desde DMX OUT recorriendo zonas con DMX
    let prevX = startX;
    let prevY = startY;
    for (const lz of dmxZones) {
      const trunkRun = analysis.dmxRuns.find((r) => r.zone === lz.zone && r.kind === 'TRUNK');
      const len = trunkRun?.lengthMeters ?? 5;
      paths.push({
        id: `dmx-chain-${lz.zone}`,
        points: `${prevX},${prevY} ${lz.x},${prevY} ${lz.x},${lz.y - 10}`,
        labelX: (prevX + lz.x) / 2,
        labelY: prevY - 4,
        label: `DMX ${len}m`,
      });
      prevX = lz.x;
      prevY = lz.y + 10;
    }
  }

  return paths;
});
</script>
