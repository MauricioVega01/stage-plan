<template>
  <div class="bg-[#0f0f13] border border-zinc-800 rounded-2xl p-6 shadow-2xl space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
      <div class="flex items-center space-x-2.5">
        <span class="inline-block w-3 h-3 bg-red-600 rounded-full animate-ping"></span>
        <h3 class="text-sm font-black tracking-wider text-white uppercase font-mono">
          Plano 2D Inteligente (Montaje Mixto + Mapa de Calor SPL)
        </h3>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button
          type="button"
          @click="showHeatmap = !showHeatmap"
          class="px-3 py-1 rounded-lg text-xs font-black uppercase font-mono border transition flex items-center gap-1.5"
          :class="showHeatmap
            ? 'bg-red-600 text-white border-red-400 shadow-lg shadow-red-950/50'
            : 'bg-zinc-900 text-zinc-300 border-zinc-700 hover:border-red-500'"
        >
          <span>🔥</span>
          <span>{{ showHeatmap ? 'Mapa de Calor SPL: ACTIVO' : 'Activar Mapa de Calor SPL' }}</span>
        </button>
        <div class="text-xs text-zinc-300 font-mono bg-zinc-900 px-3 py-1 rounded border border-zinc-700">
          {{ venueWidth }}m (Ancho) × {{ venueDepth }}m (Largo)
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
            <stop offset="0%" stop-color="#ef4444" stop-opacity="0.48" />
            <stop offset="26%" stop-color="#f59e0b" stop-opacity="0.34" />
            <stop offset="62%" stop-color="#10b981" stop-opacity="0.28" />
            <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.16" />
          </radialGradient>
          <radialGradient id="splHeatDelay" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.38" />
            <stop offset="70%" stop-color="#10b981" stop-opacity="0.15" />
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

        <!-- CAPA DE MAPA DE CALOR SPL (Innovación 3) -->
        <g v-if="showHeatmap">
          <rect
            :x="margin + 2"
            :y="margin + 2"
            :width="contentWidth - 4"
            :height="contentHeight - 4"
            fill="url(#splHeatFront)"
            rx="5"
          />
          <!-- Refuerzo de calor en zonas de Delay si existen -->
          <circle
            v-for="(top, idx) in topPositions.filter(t => t.isDelay)"
            :key="`heat-delay-${idx}`"
            :cx="top.x"
            :cy="top.y + 28"
            r="68"
            fill="url(#splHeatDelay)"
          />
          <!-- Etiquetas de Zonas Térmicas SPL -->
          <rect :x="contentWidth / 2 + margin - 78" :y="margin + 90" width="156" height="15" fill="#450a0a" fill-opacity="0.85" stroke="#ef4444" stroke-width="0.8" rx="3" />
          <text :x="contentWidth / 2 + margin" :y="margin + 100" fill="#fca5a5" font-size="6.8" font-weight="900" font-family="monospace" text-anchor="middle">
            ZONA ROJA (&gt;105 dB): PELIGRO AUDITIVO (&lt;2.5m)
          </text>

          <rect :x="contentWidth / 2 + margin - 88" :y="margin + contentHeight * 0.48" width="176" height="16" fill="#022c22" fill-opacity="0.88" stroke="#10b981" stroke-width="0.9" rx="3" />
          <text :x="contentWidth / 2 + margin" :y="margin + contentHeight * 0.48 + 10.5" fill="#6ee7b7" font-size="7" font-weight="900" font-family="monospace" text-anchor="middle">
            SWEET SPOT PISTA (96–102 dBA): IMPACTO LIMPIO
          </text>
        </g>

        <!-- Enchufe / Tablero Eléctrico Dual (Línea 1 Subs + Línea 2 Tops) -->
        <g :transform="`translate(${margin + 8}, ${margin + 8})`">
          <rect width="58" height="28" fill="#450a0a" stroke="#dc2626" stroke-width="1.8" rx="4" />
          <text x="29" y="12" fill="#fca5a5" font-size="7.5" font-weight="900" font-family="monospace" text-anchor="middle">⚡ 220V SEC</text>
          <text x="29" y="22" fill="#fde047" font-size="6.5" font-weight="900" font-family="monospace" text-anchor="middle">L1 SUB / L2 TOP</text>
        </g>

        <!-- Zona Escenario / Cabina DJ -->
        <rect
          :x="contentWidth / 2 + margin - 52"
          :y="margin + 8"
          width="104"
          height="26"
          fill="#1c1917"
          stroke="#dc2626"
          stroke-width="2"
          rx="4"
        />
        <text
          :x="contentWidth / 2 + margin"
          :y="margin + 24"
          fill="#ffffff"
          font-size="9.5"
          font-weight="900"
          font-family="monospace"
          text-anchor="middle"
        >
          CABINA DJ (0 dB)
        </text>

        <!-- Primera Fila de Audiencia (4 metros) -->
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
          :y="firstRowY - 4"
          fill="#fbbf24"
          font-size="7.5"
          font-weight="700"
          font-family="monospace"
          text-anchor="end"
        >
          PRIMERA FILA (4m · ~106 dBA)
        </text>

        <!-- Líneas Guía de Torres de Delay (si hay más de 2 cajas) -->
        <g v-for="ring in delayRings" :key="ring.id">
          <line
            :x1="margin + 8"
            :y1="ring.svgY"
            :x2="contentWidth + margin - 8"
            :y2="ring.svgY"
            stroke="#10b981"
            stroke-width="1.4"
            stroke-opacity="0.7"
            stroke-dasharray="5 3"
          />
          <rect
            :x="contentWidth / 2 + margin - 72"
            :y="ring.svgY - 9"
            width="144"
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
            font-size="7.5"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ ring.label }}
          </text>
        </g>

        <!-- Sub Bajos a Piso en MONO CLUSTER CENTRAL (Juntos al centro para ganar +6 dB y evitar cancelación) -->
        <g v-if="subPositions.length > 0">
          <!-- Marco indicador de Cluster Central -->
          <rect
            :x="contentWidth / 2 + margin - (subPositions.length * 16 + 12)"
            :y="margin + 36"
            :width="subPositions.length * 32 + 24"
            height="36"
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
            font-size="7"
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
          <text
            :x="sub.x"
            :y="sub.y - 1"
            fill="#ffffff"
            font-size="8"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ sub.tag }}
          </text>
          <text
            :x="sub.x"
            :y="sub.y + 8"
            :fill="sub.systemType === 'ACTIVE' ? '#e9d5ff' : '#a5f3fc'"
            font-size="5.8"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ sub.rmsWatts }}W
          </text>
        </g>

        <!-- Cajas Acústicas en Atriles (PA Frontal A/B + Torres de Delay C/D/E/F...) -->
        <g v-for="(top, idx) in topPositions" :key="`top-${idx}`">
          <!-- Cono de cobertura visual hacia la pista -->
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
          <text
            :x="top.x"
            :y="top.y + 1"
            fill="#ffffff"
            font-size="9"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ top.tag }}
          </text>
          <text
            :x="top.x"
            :y="top.y + 9"
            fill="#fde047"
            font-size="5.5"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ top.systemType === 'ACTIVE' ? 'ACT' : 'PAS' }}
          </text>
          <!-- Etiqueta de rol y Watts debajo de cada caja -->
          <text
            :x="top.x"
            :y="top.y + 23"
            :fill="top.systemType === 'PASSIVE' ? '#fcd34d' : (top.isDelay ? '#6ee7b7' : '#fca5a5')"
            font-size="6.8"
            font-weight="900"
            font-family="monospace"
            text-anchor="middle"
          >
            {{ top.shortRole }}
          </text>
        </g>

        <!-- Etiqueta Fondo de Pista -->
        <text
          :x="contentWidth / 2 + margin"
          :y="margin + contentHeight - 6"
          fill="#a1a1aa"
          font-size="7.5"
          font-weight="700"
          font-family="monospace"
          text-anchor="middle"
        >
          FONDO DE PISTA ({{ venueDepth }}m) — SONIDO UNIFORME SIN SATURAR EL FRENTE
        </text>
      </svg>
    </div>

    <!-- Leyenda Informativa de Colores, Zonas y Ganancias -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5 pt-2 text-xs font-mono">
      <div class="flex items-center space-x-2.5 bg-[#141418] p-2.5 rounded-lg border border-zinc-800">
        <span class="w-4 h-4 rounded-full bg-red-600 border-2 border-white shrink-0"></span>
        <div>
          <div class="text-white font-bold">PA Frontal Activo (A, B)</div>
          <div class="text-[11px] text-zinc-400">Mayor RMS · Trípode 2.2m</div>
        </div>
      </div>
      <div class="flex items-center space-x-2.5 bg-[#141418] p-2.5 rounded-lg border border-zinc-800">
        <span class="w-4 h-4 rounded-full bg-emerald-500 border-2 border-white shrink-0"></span>
        <div>
          <div class="text-white font-bold">Torres Delay (C, D...)</div>
          <div class="text-[11px] text-zinc-400">Refuerzo Pista · Con Retardo</div>
        </div>
      </div>
      <div class="flex items-center space-x-2.5 bg-[#141418] p-2.5 rounded-lg border border-zinc-800">
        <span class="w-4 h-4 rounded-sm bg-purple-600 border-2 border-white shrink-0"></span>
        <div>
          <div class="text-white font-bold">Sub Cluster (S1, S2)</div>
          <div class="text-[11px] text-zinc-400">Centro en Piso (+6 dB)</div>
        </div>
      </div>
      <div class="flex items-center space-x-2.5 bg-[#141418] p-2.5 rounded-lg border border-zinc-800">
        <span class="w-4 h-4 rounded-full bg-amber-500 border-2 border-white shrink-0"></span>
        <div>
          <div class="text-white font-bold">Unidades Pasivas (PAS)</div>
          <div class="text-[11px] text-zinc-400">Vía Speakon a Amplificador</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

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
  }
);

const showHeatmap = ref(true);

const viewBoxWidth = 420;
const viewBoxHeight = 320;
const margin = 18;

const contentWidth = computed(() => viewBoxWidth - margin * 2);
const contentHeight = computed(() => viewBoxHeight - margin * 2);

const LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'];

// Sub Bajos SIEMPRE agrupados en un MONO CLUSTER CENTRAL frente a la cabina DJ
const subPositions = computed(() => {
  const customSubs = (props.rosterNodes || []).filter(n => n.category === 'sub_bass');
  const count = customSubs.length > 0 ? customSubs.length : (props.subsCount || 0);
  if (count <= 0) return [];

  const positions = [];
  const y = margin + 54;
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

// Distribución inteligente de Cajas Acústicas (soportando lotes mixtos Activos + Pasivos):
const topPositions = computed(() => {
  const customTops = (props.rosterNodes || []).filter(n => n.category === 'top_box');
  const count = customTops.length > 0 ? customTops.length : (props.topsCount || 0);
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
      const x = isLeft ? margin + 42 : contentWidth.value + margin - 42;
      const y = margin + 48;
      positions.push({
        x,
        y,
        tag,
        systemType: sysType,
        rmsWatts: rmsW,
        isDelay: false,
        shortRole: `${rmsW}W · 0dB`,
      });
    } else {
      const ringRatio = pairIndex === 1 ? 0.52 : pairIndex === 2 ? 0.74 : 0.88;
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
        shortRole: `${rmsW}W (+${delayMs}ms)`,
      });
    }
  }
  return positions;
});

const delayRings = computed(() => {
  const customTops = (props.rosterNodes || []).filter(n => n.category === 'top_box');
  const count = customTops.length > 0 ? customTops.length : (props.topsCount || 0);
  if (count <= 2) return [];

  const depth = Math.max(8, props.venueDepth || 16);
  const soundSpeed = 331.3 + 0.606 * (props.temperatureCelsius || 20);
  const rings = [];

  const maxPairs = Math.ceil(count / 2);
  for (let p = 1; p < maxPairs; p++) {
    const ringRatio = p === 1 ? 0.52 : p === 2 ? 0.74 : 0.88;
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
  const ratio = Math.min(Math.max(4 / depth, 0.28), 0.42);
  return margin + contentHeight.value * ratio;
});
</script>
