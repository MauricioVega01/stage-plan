<template>
  <div class="bg-[#0f0f13] border border-zinc-800 rounded-2xl p-4 sm:p-6 shadow-2xl space-y-4">
    <!-- Header de Controles y Filtros del Plano -->
    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
      <div class="flex items-center space-x-2.5">
        <span class="inline-block w-3 h-3 bg-red-600 rounded-full animate-ping"></span>
        <h3 class="text-sm font-black tracking-wider text-white uppercase font-mono">
          Plano 2D Escala Proporcional (Audio + Fuerza Eléctrica SEC + Postes Guía)
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
          <span>Audio (XLR/Speakon)</span>
        </button>
        <button
          type="button"
          @click="showCornerGuides = !showCornerGuides"
          class="px-2.5 py-1 rounded-lg text-[11px] font-black uppercase font-mono border transition flex items-center gap-1 cursor-pointer"
          :class="showCornerGuides
            ? 'bg-sky-600 text-white border-sky-400 shadow-lg shadow-sky-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:border-sky-500'"
          title="Guías esquineras y postes de radio de curvatura para cables de fuerza y señal (SEC RIC 10)"
        >
          <span>📍</span>
          <span>Postes Guía ({{ cornerGuidePosts.length }})</span>
        </button>
        <div class="text-[11px] text-zinc-200 font-mono bg-zinc-900 px-2.5 py-1 rounded border border-zinc-700 font-bold">
          📏 {{ venueWidth }}m × {{ venueDepth }}m (Escala 1:{{ Math.round((venueWidth * 10) / viewBoxWidth) || 1 }})
        </div>
      </div>
    </div>

    <!-- Contenedor SVG reactivo con Aspect Ratio Dinámico -->
    <div
      class="relative w-full bg-[#050505] rounded-xl overflow-hidden border-2 border-zinc-800 flex items-center justify-center p-2 sm:p-3 shadow-inner"
      :style="{ aspectRatio: `${viewBoxWidth} / ${viewBoxHeight}` }"
    >
      <svg
        :viewBox="`0 0 ${viewBoxWidth} ${viewBoxHeight}`"
        class="w-full h-full select-none"
        preserveAspectRatio="xMidYMid meet"
      >
        <!-- Grilla y Gradientes para Mapa de Calor SPL -->
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#181820" stroke-width="0.7" />
          </pattern>
          <radialGradient id="splHeatFront" cx="50%" cy="25%" r="70%">
            <stop offset="0%" stop-color="#ef4444" stop-opacity="0.45" />
            <stop offset="28%" stop-color="#f59e0b" stop-opacity="0.30" />
            <stop offset="65%" stop-color="#10b981" stop-opacity="0.22" />
            <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.10" />
          </radialGradient>
          <radialGradient id="splHeatDelay" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.35" />
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
            v-for="(top, idx) in topPositions.filter((t) => t.isDelay)"
            :key="`heat-delay-${idx}`"
            :cx="top.x"
            :cy="top.y + 28"
            r="68"
            fill="url(#splHeatDelay)"
          />
          <!-- Zona Roja Acústica (>105 dB) -->
          <rect
            :x="contentWidth / 2 + margin - 90"
            :y="firstRowY - 22"
            width="180"
            height="15"
            fill="#450a0a"
            fill-opacity="0.88"
            stroke="#ef4444"
            stroke-width="0.9"
            rx="3"
          />
          <text
            :x="contentWidth / 2 + margin"
            :y="firstRowY - 12"
            fill="#fca5a5"
            font-size="6.8"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            ZONA ROJA (&gt;105 dB): PELIGRO AUDITIVO (&lt;2.5m)
          </text>

          <!-- Sweet Spot Pista (96-102 dBA) -->
          <rect
            :x="contentWidth / 2 + margin - 100"
            :y="margin + contentHeight * 0.62"
            width="200"
            height="16"
            fill="#022c22"
            fill-opacity="0.88"
            stroke="#10b981"
            stroke-width="1.0"
            rx="3"
          />
          <text
            :x="contentWidth / 2 + margin"
            :y="margin + contentHeight * 0.62 + 11"
            fill="#6ee7b7"
            font-size="7.2"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
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
              opacity="0.95"
            />
            <rect
              :x="cable.labelX - 32"
              :y="cable.labelY - 6"
              width="64"
              height="12"
              fill="#09090b"
              fill-opacity="0.94"
              :stroke="cable.stroke"
              stroke-width="0.8"
              rx="2"
            />
            <text
              :x="cable.labelX"
              :y="cable.labelY + 2.5"
              :fill="cable.stroke"
              font-size="5.8"
              font-weight="900"
              font-family="monospace"
              text-anchor="middle"
            >
              {{ cable.shortLabel }}
            </text>
          </g>
        </g>

        <!-- CAPA 3: SEÑAL DE AUDIO (XLR CIAN PARA ACTIVOS / SPEAKON ÁMBAR PARA PASIVOS) -->
        <g v-if="showAudioSignal">
          <g v-for="sig in audioSignalPaths" :key="sig.id">
            <polyline
              :points="sig.points"
              fill="none"
              :stroke="sig.stroke"
              :stroke-width="sig.width"
              :stroke-dasharray="sig.dash"
              stroke-linecap="round"
              stroke-linejoin="round"
              opacity="0.90"
            />
          </g>
        </g>

        <!-- BANDA 1: TABLERO ELÉCTRICO SEC (ESQUINA SUPERIOR IZQUIERDA DESPEJADA) -->
        <g :transform="`translate(${boardPoint.x - 32}, ${boardPoint.y - 14})`">
          <rect width="64" height="28" fill="#450a0a" stroke="#dc2626" stroke-width="2" rx="4" />
          <text x="32" y="11" fill="#fca5a5" font-size="7.5" font-weight="900" font-family="monospace" text-anchor="middle">⚡ 220V SEC</text>
          <text x="32" y="21" fill="#fde047" font-size="6" font-weight="900" font-family="monospace" text-anchor="middle">
            L1 SUB / L2 TOP
          </text>
        </g>

        <!-- BANDA 2: CABINA DJ (CENTRADA, ESPACIO AMPLIO) -->
        <rect
          :x="boothPoint.x - 62"
          :y="boothPoint.y - 14"
          width="124"
          height="28"
          fill="#1c1917"
          stroke="#dc2626"
          stroke-width="2.2"
          rx="5"
        />
        <text
          :x="boothPoint.x"
          :y="boothPoint.y + 2"
          fill="#ffffff"
          font-size="9"
          font-weight="900"
          font-family="monospace"
          text-anchor="middle"
        >
          CABINA DJ (0 dB)
        </text>
        <g v-if="hasLighting">
          <rect
            :x="boothPoint.x + 32"
            :y="boothPoint.y + 7"
            width="38"
            height="11"
            fill="#581c87"
            stroke="#e879f9"
            stroke-width="1.0"
            rx="2"
          />
          <text :x="boothPoint.x + 51" :y="boothPoint.y + 15" fill="#fae8ff" font-size="5.4" font-weight="900" font-family="monospace" text-anchor="middle">
            DMX OUT
          </text>
        </g>

        <!-- SUBWOOFERS A PISO EN MONO CLUSTER CENTRAL (BAJO LA CABINA CON SEPARACIÓN) -->
        <g v-if="subPositions.length > 0">
          <rect
            :x="contentWidth / 2 + margin - (subPositions.length * 18 + 14)"
            :y="subsBaseY - 17"
            :width="subPositions.length * 36 + 28"
            height="34"
            fill="#1e1b4b"
            fill-opacity="0.40"
            stroke="#8b5cf6"
            stroke-width="1.2"
            stroke-dasharray="3 3"
            rx="5"
          />
          <text
            :x="contentWidth / 2 + margin"
            :y="subsBaseY + 23"
            fill="#c4b5fd"
            font-size="6.5"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            CLUSTER CENTRAL DE SUB-BAJOS (+6 dB ACOPLADOS · PISO)
          </text>
        </g>

        <!-- Cajas Individuales de Sub-Bajos -->
        <g v-for="(sub, idx) in subPositions" :key="`sub-${idx}`">
          <rect
            :x="sub.x - 14"
            :y="sub.y - 12"
            width="28"
            height="24"
            :fill="sub.systemType === 'ACTIVE' ? '#3b0764' : '#083344'"
            :stroke="sub.systemType === 'ACTIVE' ? '#a855f7' : '#06b6d4'"
            stroke-width="2"
            rx="3"
          />
          <text :x="sub.x" :y="sub.y - 1" fill="#ffffff" font-size="8.2" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ sub.tag }}
          </text>
          <text :x="sub.x" :y="sub.y + 8" :fill="sub.systemType === 'ACTIVE' ? '#e9d5ff' : '#a5f3fc'" font-size="5.8" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ sub.rmsWatts }}W
          </text>
        </g>

        <!-- CAJAS ACÚSTICAS EN ATRILES (PA FRONTAL A Y B + TORRES DE DELAY) -->
        <g v-for="(top, idx) in topPositions" :key="`top-${idx}`">
          <!-- Cono de Dispersión Acústica -->
          <polygon
            :points="`${top.x},${top.y} ${top.x - 22},${Math.min(margin + contentHeight - 4, top.y + 50)} ${top.x + 22},${Math.min(margin + contentHeight - 4, top.y + 50)}`"
            :fill="top.isDelay ? '#10b981' : '#ef4444'"
            fill-opacity="0.16"
          />
          <!-- Círculo de la Caja -->
          <circle
            :cx="top.x"
            :cy="top.y"
            r="15"
            :fill="top.systemType === 'PASSIVE' ? '#78350f' : (top.isDelay ? '#064e3b' : '#7f1d1d')"
            :stroke="top.systemType === 'PASSIVE' ? '#f59e0b' : (top.isDelay ? '#10b981' : '#ef4444')"
            stroke-width="2.4"
          />
          <text :x="top.x" :y="top.y + 1.5" fill="#ffffff" font-size="9.5" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ top.tag }}
          </text>
          <text :x="top.x" :y="top.y + 10" fill="#fde047" font-size="5.8" font-weight="900" font-family="monospace" text-anchor="middle">
            {{ top.systemType === 'ACTIVE' ? 'ACT' : 'PAS' }}
          </text>
          <text
            :x="top.x"
            :y="top.y + 24"
            :fill="top.systemType === 'PASSIVE' ? '#fcd34d' : (top.isDelay ? '#6ee7b7' : '#fca5a5')"
            font-size="6.6"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ top.shortRole }}
          </text>
        </g>

        <!-- CAPA 5: ZAPATILLAS MULTICONTACTO (DESACOPLADAS, SIN SOLAPAMIENTO) -->
        <g v-if="showPowerStrips">
          <g v-for="zNode in powerStripNodes" :key="zNode.id">
            <!-- Rectángulo de la Zapatilla -->
            <rect
              :x="zNode.x - 29"
              :y="zNode.y - 11"
              width="58"
              height="22"
              :fill="zNode.status === 'OVERLOAD' ? '#7f1d1d' : zNode.status === 'WARNING' ? '#78350f' : '#064e3b'"
              :stroke="zNode.status === 'OVERLOAD' ? '#f87171' : zNode.status === 'WARNING' ? '#fbbf24' : '#34d399'"
              stroke-width="1.6"
              rx="4"
            />
            <text :x="zNode.x" :y="zNode.y - 1" fill="#ffffff" font-size="6.3" font-weight="900" font-family="monospace" text-anchor="middle">
              🔌 {{ zNode.id }} ({{ zNode.ratingAmps }}A)
            </text>
            <text :x="zNode.x" :y="zNode.y + 7.5" fill="#d1fae5" font-size="5.4" font-weight="800" font-family="monospace" text-anchor="middle">
              {{ zNode.usedSockets }}/{{ zNode.totalSockets }} bocas · {{ zNode.loadWatts }}W
            </text>
          </g>
        </g>

        <!-- Primera Fila de Audiencia (Distancia en Metros Real) -->
        <line
          :x1="margin + 6"
          :y1="firstRowY"
          :x2="contentWidth + margin - 6"
          :y2="firstRowY"
          stroke="#f59e0b"
          stroke-width="1.3"
          stroke-opacity="0.65"
          stroke-dasharray="4 3"
        />
        <text
          :x="contentWidth + margin - 10"
          :y="firstRowY - 5"
          fill="#fbbf24"
          font-size="7.2"
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
            :x="contentWidth / 2 + margin - 75"
            :y="ring.svgY - 9"
            width="150"
            height="16"
            fill="#022c22"
            stroke="#10b981"
            stroke-width="1"
            rx="3"
          />
          <text
            :x="contentWidth / 2 + margin"
            :y="ring.svgY + 2"
            fill="#6ee7b7"
            font-size="7"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ ring.label }}
          </text>
        </g>

        <!-- CAPA 6: POSTES GUÍA ESQUINEROS / TÓTEMS DE RADIO DE CURVATURA (SEC RIC N° 10) -->
        <g v-if="showCornerGuides">
          <g v-for="post in cornerGuidePosts" :key="post.id">
            <!-- Ancla de Esquina / Base de Poste -->
            <circle
              :cx="post.x"
              :cy="post.y"
              r="9.5"
              fill="#090d16"
              stroke="#38bdf8"
              stroke-width="2.2"
            />
            <!-- Cruz central del poste -->
            <line :x1="post.x - 5" :y1="post.y" :x2="post.x + 5" :y2="post.y" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" />
            <line :x1="post.x" :y1="post.y - 5" :x2="post.x" :y2="post.y + 5" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" />

            <!-- Curvatura guiada suave (Radio de Curvatura R >= 6d) -->
            <circle
              :cx="post.x"
              :cy="post.y"
              r="17"
              fill="none"
              stroke="#38bdf8"
              stroke-width="1.2"
              stroke-dasharray="3 2"
              opacity="0.9"
            />

            <!-- Etiqueta del Poste Guía -->
            <rect
              :x="post.labelX - 28"
              :y="post.labelY - 5.5"
              width="56"
              height="12"
              fill="#030712"
              fill-opacity="0.95"
              stroke="#38bdf8"
              stroke-width="0.8"
              rx="2.5"
            />
            <text
              :x="post.labelX"
              :y="post.labelY + 2.5"
              fill="#bae6fd"
              font-size="5.6"
              font-weight="900"
              font-family="monospace"
              text-anchor="middle"
            >
              {{ post.label }}
            </text>
          </g>
        </g>

        <!-- Etiqueta de Escala y Fondo de Pista -->
        <text
          :x="contentWidth / 2 + margin"
          :y="margin + contentHeight - 8"
          fill="#a1a1aa"
          font-size="7.5"
          font-weight="700"
          font-family="monospace"
          text-anchor="middle"
        >
          FONDO DE PISTA ({{ venueDepth }}m) — CABLEADO PERIMETRAL SIN CRUCES CENTRALES
        </text>
      </svg>
    </div>

    <!-- Leyenda de Capas de Cableado y Equipos -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-2 pt-1 text-[11px] font-mono">
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
      <div class="flex items-center space-x-2 bg-[#141418] p-2 rounded-lg border border-zinc-800">
        <span class="w-3.5 h-3.5 rounded-full border border-sky-400 bg-sky-950 flex items-center justify-center text-[9px] text-sky-300 font-bold">📍</span>
        <span class="text-zinc-200 font-bold truncate">Postes Guía (SEC)</span>
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
const showCornerGuides = ref(true);

// -------------------------------------------------------------
// RELACIÓN DE ASPECTO Y ESCALA PROPORCIONAL AL RECINTO REAL
// -------------------------------------------------------------
const viewBoxWidth = 560;
const margin = 20;

const viewBoxHeight = computed(() => {
  const w = Math.max(6, props.venueWidth || 10);
  const d = Math.max(6, props.venueDepth || 14);
  const ratio = d / w;
  // Limitar aspect ratio entre 0.65 y 1.25 para visualización ergonómica
  const clampedRatio = Math.max(0.68, Math.min(1.22, ratio));
  return Math.round(viewBoxWidth * clampedRatio);
});

const contentWidth = computed(() => viewBoxWidth - margin * 2);
const contentHeight = computed(() => viewBoxHeight.value - margin * 2);

// Puntos clave de referencia en el escenario
const boardPoint = computed(() => ({ x: margin + 40, y: margin + 46 }));
const boothPoint = computed(() => ({ x: contentWidth.value / 2 + margin, y: margin + 46 }));
const subsBaseY = computed(() => margin + 112);

const powerStrips = computed(() => props.powerPlan?.powerStrips ?? []);
const hasLighting = computed(() => (props.lightingAnalysis?.totalFixtureUnits ?? 0) > 0);
const dmxCablesCount = computed(() => props.lightingAnalysis?.totalDmxCablesCount ?? 0);

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];

// -------------------------------------------------------------
// POSICIONES DE SUBWOOFERS (CLUSTER CENTRAL A PISO)
// -------------------------------------------------------------
const subPositions = computed(() => {
  const customSubs = (props.rosterNodes || []).filter((n) => n.category === 'sub_bass');
  const count = customSubs.length > 0 ? customSubs.length : props.subsCount || 0;
  if (count <= 0) return [];

  const positions = [];
  const y = subsBaseY.value;
  const centerX = contentWidth.value / 2 + margin;
  const stepX = 36;
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

// -------------------------------------------------------------
// POSICIONES DE CAJAS TOPS (PA FRONTAL A Y B + TORRES DE DELAY)
// -------------------------------------------------------------
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
      // PA Frontal: alineado a los extremos laterales
      const x = isLeft ? margin + 55 : contentWidth.value + margin - 55;
      const y = margin + 105;
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
      // Torres de Delay: distribuidas en profundidad
      const ringRatio = pairIndex === 1 ? 0.58 : pairIndex === 2 ? 0.78 : 0.88;
      const realDistMeters = Number((depth * ringRatio).toFixed(1));
      const acousticDist = Math.max(4, realDistMeters - 2.0);
      const delayMs = node?.delayMs ?? Number(((acousticDist / soundSpeed) * 1000 + 3.0).toFixed(1));

      const x = isLeft ? margin + 40 : contentWidth.value + margin - 40;
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

// Anillos de retraso para torres de delay
const delayRings = computed(() => {
  const customTops = (props.rosterNodes || []).filter((n) => n.category === 'top_box');
  const count = customTops.length > 0 ? customTops.length : props.topsCount || 0;
  if (count <= 2) return [];

  const depth = Math.max(8, props.venueDepth || 16);
  const soundSpeed = 331.3 + 0.606 * (props.temperatureCelsius || 20);
  const rings = [];

  const maxPairs = Math.ceil(count / 2);
  for (let p = 1; p < maxPairs; p++) {
    const ringRatio = p === 1 ? 0.58 : p === 2 ? 0.78 : 0.88;
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

// Primera fila de audiencia calculada con proporción real
const firstRowY = computed(() => {
  const depth = Math.max(8, props.venueDepth || 16);
  const ratio = Math.min(Math.max(4 / depth, 0.36), 0.44);
  return margin + contentHeight.value * ratio;
});

// -------------------------------------------------------------
// POSICIONES DE ZAPATILLAS ELÉCTRICAS DESACOPLADAS (SIN SOLAPAR)
// -------------------------------------------------------------
const powerStripNodes = computed(() => {
  const list = powerStrips.value;
  const cx = boothPoint.value.x;
  let lightIdx = 0;
  let subIdx = 0;
  let boothIdx = 0;

  return list.map((z) => {
    let x = cx;
    let y = margin + 160;

    if (z.zone === 'DJ_BOOTH') {
      // Z1: Desplazada a la derecha de la Cabina DJ (despejada)
      x = cx + 110 + boothIdx * 45;
      y = margin + 46;
      boothIdx++;
    } else if (z.zone === 'SUB_CLUSTER') {
      // Z2: Debajo del cluster de sub-bajos, centrada con holgura
      x = cx + (subIdx === 0 ? -60 : 60);
      y = subsBaseY.value + 42;
      subIdx++;
    } else if (z.zone === 'DELAY_ZONE') {
      x = margin + 45;
      y = margin + contentHeight.value * 0.70;
    } else if (z.zone === 'LIGHTING_FX') {
      x = contentWidth.value + margin - 50;
      y = margin + 46 + lightIdx * 28;
      lightIdx++;
    }

    return { ...z, x, y };
  });
});

// -------------------------------------------------------------
// ZONAS DE ILUMINACIÓN Y EFECTOS
// -------------------------------------------------------------
const lightingZoneNodes = computed(() => {
  const zones = props.lightingAnalysis?.zones ?? [];
  const cx = boothPoint.value.x;
  return zones.map((z) => {
    let x = cx;
    let y = margin + 175;
    let icon = '💡';
    let shortTitle = 'LUCES';

    if (z.zone === 'TRUSS_LEFT') {
      x = margin + 55;
      y = margin + 175;
      icon = '💡';
      shortTitle = 'TRUSS IZQ';
    } else if (z.zone === 'TRUSS_RIGHT') {
      x = contentWidth.value + margin - 55;
      y = margin + 175;
      icon = '💡';
      shortTitle = 'TRUSS DER';
    } else if (z.zone === 'CENTER_BOOTH') {
      x = cx - 110;
      y = margin + 46;
      icon = '✨';
      shortTitle = 'FRENTE DJ';
    } else if (z.zone === 'FLOOR') {
      x = cx - 85;
      y = subsBaseY.value + 42;
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

// -------------------------------------------------------------
// POSTES GUÍA ESQUINEROS Y SOPORTES DE RADIO DE CURVATURA (SEC RIC 10)
// -------------------------------------------------------------
export interface CornerGuidePost {
  id: string;
  x: number;
  y: number;
  labelX: number;
  labelY: number;
  label: string;
  type: 'POSTE_ESQUINA' | 'PASACABLES_CODO';
  description: string;
}

const cornerGuidePosts = computed<CornerGuidePost[]>(() => {
  const list: CornerGuidePost[] = [];
  const W = contentWidth.value;
  const H = contentHeight.value;
  const topRailY = margin + 8;

  // 1. Esquina Superior Izquierda (Giro desde Tablero 220V hacia carril perimetral)
  list.push({
    id: 'post-tl',
    x: margin + 40,
    y: topRailY,
    labelX: margin + 40,
    labelY: topRailY + 16,
    label: '📍 POSTE GUÍA 1',
    type: 'POSTE_ESQUINA',
    description: 'Poste Guía Pasacables Esquinero Izquierdo (Radio Curvatura SEC RIC 10)',
  });

  // 2. Esquina Superior Derecha (Giro de carril de fondo hacia Top B PA Derecho)
  list.push({
    id: 'post-tr',
    x: W + margin - 55,
    y: topRailY,
    labelX: W + margin - 55,
    labelY: topRailY + 16,
    label: '📍 POSTE GUÍA 2',
    type: 'POSTE_ESQUINA',
    description: 'Poste Guía Pasacables Esquinero Derecho (Radio Curvatura SEC RIC 10)',
  });

  // 3. Esquinas Laterales para Torres de Delay (si aplican) o retorno de fondo
  const hasDelay = topPositions.value.some((t) => t.isDelay);
  if (hasDelay) {
    list.push({
      id: 'post-lat-l',
      x: margin + 6,
      y: margin + H * 0.46,
      labelX: margin + 35,
      labelY: margin + H * 0.46 - 8,
      label: '📍 GUÍA DELAY IZQ',
      type: 'PASACABLES_CODO',
      description: 'Pasacables Codo Esquinero 90° Lateral Izquierdo',
    });
    list.push({
      id: 'post-lat-r',
      x: W + margin - 6,
      y: margin + H * 0.46,
      labelX: W + margin - 35,
      labelY: margin + H * 0.46 - 8,
      label: '📍 GUÍA DELAY DER',
      type: 'PASACABLES_CODO',
      description: 'Pasacables Codo Esquinero 90° Lateral Derecho',
    });
  }

  return list;
});

// -------------------------------------------------------------
// CANALES DE CABLEADO PERIMETRAL ORTOGONALES (ANTI-COLISIÓN)
// -------------------------------------------------------------
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

  // Carril perimetral superior exclusivo para cables de fuerza
  const topPowerRailY = margin + 8;

  // 1. Troncal L2 hacia Cabina DJ (Z1)
  const boothExt = exts.find((e) => e.zone === 'DJ_BOOTH');
  const zBooth = powerStripNodes.value.find((z) => z.zone === 'DJ_BOOTH');
  if (boothExt && zBooth) {
    paths.push({
      id: 'pwr-booth',
      points: `${bx + 32},${by} ${bx + 32},${topPowerRailY} ${zBooth.x},${topPowerRailY} ${zBooth.x},${zBooth.y - 11}`,
      stroke: '#facc15',
      width: 2.2,
      dash: 'none',
      labelX: (bx + zBooth.x) / 2 + 10,
      labelY: topPowerRailY + 9,
      shortLabel: `L2 ${boothExt.crossSectionMm2}mm²·${boothExt.lengthMeters}m`,
    });
  }

  // 2. Troncal L1 hacia Cluster de Subs (Z2)
  const subExt = exts.find((e) => e.zone === 'SUB_CLUSTER');
  const zSub = powerStripNodes.value.find((z) => z.zone === 'SUB_CLUSTER');
  if (subExt && zSub) {
    paths.push({
      id: 'pwr-sub',
      points: `${bx},${by + 14} ${bx},${zSub.y} ${zSub.x - 29},${zSub.y}`,
      stroke: '#ef4444',
      width: 2.6,
      dash: 'none',
      labelX: bx + 55,
      labelY: zSub.y - 8,
      shortLabel: `L1 ${subExt.crossSectionMm2}mm²·${subExt.lengthMeters}m`,
    });
  }

  // 3. Alimentación Tops Activos
  for (const top of topPositions.value) {
    if (top.systemType !== 'ACTIVE') continue;
    const ext = exts.find((e) => e.to.includes(top.tag));
    if (!top.isDelay) {
      if (top.isLeft) {
        paths.push({
          id: `pwr-top-${top.tag}`,
          points: `${bx - 12},${by + 14} ${bx - 12},${top.y} ${top.x - 15},${top.y}`,
          stroke: '#facc15',
          width: 1.8,
          dash: 'none',
          labelX: margin + 35,
          labelY: (by + top.y) / 2 + 6,
          shortLabel: ext ? `${ext.crossSectionMm2}mm²·${ext.lengthMeters}m` : 'L2 220V',
        });
      } else {
        paths.push({
          id: `pwr-top-${top.tag}`,
          points: `${bx + 32},${topPowerRailY + 4} ${top.x},${topPowerRailY + 4} ${top.x},${top.y - 15}`,
          stroke: '#facc15',
          width: 1.8,
          dash: 'none',
          labelX: top.x - 42,
          labelY: topPowerRailY + 12,
          shortLabel: ext ? `${ext.crossSectionMm2}mm²·${ext.lengthMeters}m` : 'L2 220V',
        });
      }
    } else {
      const wallX = top.isLeft ? margin + 6 : contentWidth.value + margin - 6;
      const routePts = top.isLeft
        ? `${bx - 18},${by + 14} ${wallX},${by + 14} ${wallX},${top.y} ${top.x - 15},${top.y}`
        : `${bx + 32},${topPowerRailY} ${wallX},${topPowerRailY} ${wallX},${top.y} ${top.x + 15},${top.y}`;
      paths.push({
        id: `pwr-delay-${top.tag}`,
        points: routePts,
        stroke: '#eab308',
        width: 1.7,
        dash: '5 2',
        labelX: top.isLeft ? margin + 40 : contentWidth.value + margin - 40,
        labelY: top.y - 16,
        shortLabel: ext ? `${ext.crossSectionMm2}mm²·${ext.lengthMeters}m` : 'L2 Delay',
      });
    }
  }

  // 4. Troncales Línea 3 hacia Iluminación
  const l3Exts = exts.filter((e) => e.line === 'LINE_3_LIGHTING_FX');
  const zLights = powerStripNodes.value.filter((z) => z.line === 'LINE_3_LIGHTING_FX');
  l3Exts.forEach((ext, idx) => {
    const zTarget = zLights[idx] || zLights[0];
    if (!zTarget) return;
    const railY = topPowerRailY + 14 + idx * 5;
    paths.push({
      id: `pwr-l3-${idx}`,
      points: `${bx + 32},${railY} ${zTarget.x},${railY} ${zTarget.x},${zTarget.y - 11}`,
      stroke: '#f97316',
      width: 2.2,
      dash: 'none',
      labelX: (bx + zTarget.x) / 2 + 35,
      labelY: railY + 8,
      shortLabel: `L3 ${ext.crossSectionMm2}mm²·${ext.lengthMeters}m`,
    });
  });

  return paths;
});

// -------------------------------------------------------------
// TRAZADOS DE SEÑAL DE AUDIO (XLR CIAN / SPEAKON ÁMBAR)
// -------------------------------------------------------------
const audioSignalPaths = computed(() => {
  const cx = boothPoint.value.x;
  const cy = boothPoint.value.y + 14;
  const list: Array<{ id: string; points: string; stroke: string; width: number; dash: string }> = [];

  for (const top of topPositions.value) {
    const isPassive = top.systemType === 'PASSIVE';
    list.push({
      id: `sig-top-${top.tag}`,
      points: `${cx},${cy} ${top.x},${cy + 18} ${top.x},${top.y - 15}`,
      stroke: isPassive ? '#f59e0b' : '#22d3ee',
      width: isPassive ? 2.2 : 1.5,
      dash: isPassive ? 'none' : '4 3',
    });
  }

  for (const sub of subPositions.value) {
    const isPassive = sub.systemType === 'PASSIVE';
    list.push({
      id: `sig-sub-${sub.tag}`,
      points: `${cx},${cy} ${sub.x},${sub.y - 14}`,
      stroke: isPassive ? '#f59e0b' : '#22d3ee',
      width: isPassive ? 2.0 : 1.4,
      dash: isPassive ? 'none' : '3 3',
    });
  }

  return list;
});

// -------------------------------------------------------------
// TRAZADOS DMX DESDE DMX OUT EN CABINA
// -------------------------------------------------------------
const dmxPaths = computed(() => {
  const analysis = props.lightingAnalysis;
  if (!analysis || analysis.dmxControlledUnits === 0) return [];

  const startX = boothPoint.value.x + 51;
  const startY = boothPoint.value.y + 18;
  const dmxZones = lightingZoneNodes.value.filter((z) => z.dmxCount > 0);
  const paths: Array<{ id: string; points: string; labelX: number; labelY: number; label: string }> = [];

  if (analysis.needsDmxSplitter) {
    for (const lz of dmxZones) {
      const trunkRun = analysis.dmxRuns.find((r) => r.zone === lz.zone && r.kind === 'TRUNK');
      const len = trunkRun?.lengthMeters ?? 5;
      paths.push({
        id: `dmx-split-${lz.zone}`,
        points: `${startX},${startY} ${startX},${lz.y - 18} ${lz.x},${lz.y - 18} ${lz.x},${lz.y - 11}`,
        labelX: (startX + lz.x) / 2,
        labelY: lz.y - 18,
        label: `DMX ${len}m`,
      });
    }
  } else {
    let prevX = startX;
    let prevY = startY;
    for (const lz of dmxZones) {
      const trunkRun = analysis.dmxRuns.find((r) => r.zone === lz.zone && r.kind === 'TRUNK');
      const len = trunkRun?.lengthMeters ?? 5;
      paths.push({
        id: `dmx-chain-${lz.zone}`,
        points: `${prevX},${prevY} ${lz.x},${prevY} ${lz.x},${lz.y - 11}`,
        labelX: (prevX + lz.x) / 2,
        labelY: prevY - 6,
        label: `DMX ${len}m`,
      });
      prevX = lz.x;
      prevY = lz.y + 11;
    }
  }

  return paths;
});
</script>
