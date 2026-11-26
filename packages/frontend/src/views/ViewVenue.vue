<template>
  <div class="h-full w-full p-4 lg:p-6 grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 overflow-hidden">
    <!-- PANEL IZQUIERDO: FORMULARIO Y PRESETS (Scroll interno suave solo si la pantalla es baja) -->
    <div class="lg:col-span-5 h-full flex flex-col space-y-4 overflow-y-auto pr-1">
      <!-- Selector de Casos Cotidianos Rápido -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-4 shadow-xl">
        <div class="flex items-center justify-between mb-2.5">
          <span class="text-xs font-mono font-bold text-zinc-400 uppercase tracking-wider">
            ⚡ Presets de Prueba Rápida (8 Escalas)
          </span>
          <span v-if="storageFeedbackMsg" class="text-[11px] text-emerald-400 font-mono font-bold animate-pulse">
            {{ storageFeedbackMsg }}
          </span>
        </div>
        <select
          :value="activePresetId || ''"
          @change="onPresetChange"
          class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none focus:border-red-500 transition cursor-pointer"
        >
          <option value="" disabled>Selecciona un caso cotidiano para autocompletar...</option>
          <option v-for="p in demoPresets" :key="p.id" :value="p.id">
            {{ p.scaleTag }} · {{ p.title }}
          </option>
        </select>
      </div>

      <!-- Tarjeta de Medidas Principales -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-5 shadow-xl flex-1 flex flex-col justify-between space-y-4 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-red-600"></div>

        <div>
          <div class="flex items-center justify-between border-b border-zinc-800/80 pb-3 mb-4">
            <h2 class="text-sm font-black tracking-wider text-white uppercase font-mono flex items-center gap-2">
              <span class="text-red-500 font-mono">[ 1 ]</span> Geometría del Recinto
            </h2>
            <span class="text-[11px] font-mono text-zinc-400">Dimensiones de Sala / Terreno</span>
          </div>

          <div class="space-y-3.5">
            <!-- Nombre -->
            <div>
              <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1">
                Nombre del Recinto o Evento
              </label>
              <input
                v-model="venue.name"
                @input="resetValidation"
                type="text"
                placeholder="Ej: Parcela Los Aromos, Curacaví"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2.5 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
              />
            </div>

            <!-- Ancho y Largo -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1 flex items-center justify-between">
                  <span>Ancho (m)</span>
                  <span class="text-zinc-400 font-normal">{{ venue.widthMeters || '--' }}m</span>
                </label>
                <input
                  v-model.number="venue.widthMeters"
                  @input="resetValidation"
                  type="number"
                  min="3"
                  max="80"
                  step="0.5"
                  placeholder="12"
                  class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-red-500 transition"
                />
              </div>

              <div>
                <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1 flex items-center justify-between">
                  <span>Largo (m)</span>
                  <span class="text-zinc-400 font-normal">{{ venue.depthMeters || '--' }}m</span>
                </label>
                <input
                  v-model.number="venue.depthMeters"
                  @input="resetValidation"
                  type="number"
                  min="3"
                  max="100"
                  step="0.5"
                  placeholder="18"
                  class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-red-500 transition"
                />
              </div>
            </div>

            <!-- Distancia Eléctrica y Entorno -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1">
                  Dist. Eléctrica (m)
                </label>
                <input
                  v-model.number="venue.electricalDistanceMeters"
                  @input="resetValidation"
                  type="number"
                  min="1"
                  max="150"
                  placeholder="25"
                  class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-red-500 transition"
                />
              </div>

              <div>
                <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1">
                  Tipo de Entorno
                </label>
                <select
                  v-model="venue.environmentType"
                  @change="resetValidation"
                  class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-xs text-white font-mono focus:outline-none focus:border-red-500 transition cursor-pointer"
                >
                  <option value="INDOOR">🏛️ Salón Cerrado</option>
                  <option value="OUTDOOR_PARCELA">🌲 Parcela / Aire Libre</option>
                </select>
              </div>
            </div>

            <!-- Duración y Altura -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1">
                  Duración Música (hrs)
                </label>
                <input
                  v-model.number="venue.eventDurationHours"
                  @input="resetValidation"
                  type="number"
                  min="1"
                  max="24"
                  placeholder="7"
                  class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-red-500 transition"
                />
              </div>

              <div>
                <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1">
                  Alto Techo (m)
                </label>
                <input
                  v-model.number="venue.heightMeters"
                  @input="resetValidation"
                  type="number"
                  min="2"
                  max="15"
                  step="0.5"
                  placeholder="3.5"
                  class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-sm text-white font-mono focus:outline-none focus:border-red-500 transition"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Indicador de Superficie y Aforo -->
        <div class="bg-[#14141c] border border-zinc-800 rounded-xl p-3.5 flex items-center justify-between font-mono">
          <div>
            <span class="text-[10px] text-zinc-500 uppercase tracking-wider block">Superficie Total & Aforo Pista</span>
            <span class="text-sm font-black text-red-400">
              {{ calculatedArea }} m²
              <span class="text-zinc-400 font-normal text-xs ml-1">(~{{ estimatedCrowd }} personas)</span>
            </span>
          </div>
          <span class="text-xl">📐</span>
        </div>
      </div>
    </div>

    <!-- PANEL DERECHO: VISUALIZADOR PERIMÉTRICO 2D REACTIVO EN VIVO (Cero Scroll) -->
    <div class="lg:col-span-7 h-full bg-[#0a0a0f] border border-zinc-800 rounded-2xl p-4 flex flex-col justify-between shadow-2xl relative overflow-hidden">
      <!-- Barra Superior de Herramientas del Visualizador -->
      <div class="flex items-center justify-between pb-2 border-b border-zinc-800/80 font-mono text-xs">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="font-bold text-zinc-300 uppercase tracking-wider">Perímetro Espacial CAD</span>
        </div>
        <div class="text-zinc-500 text-[11px]">
          Escala Dinámica: {{ venue.widthMeters || 10 }}m × {{ venue.depthMeters || 15 }}m
        </div>
      </div>

      <!-- Lienzo SVG Perimétrico Auto-escalable -->
      <div class="flex-1 w-full min-h-0 flex items-center justify-center p-2 relative">
        <svg
          class="w-full h-full max-h-full transition-all duration-300"
          :viewBox="svgViewBox"
          preserveAspectRatio="xMidYMid meet"
        >
          <!-- Cuadrícula de Fondo -->
          <defs>
            <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#1f1f2e" stroke-width="0.5" />
            </pattern>
          </defs>
          <rect x="-100" y="-100" width="400" height="400" fill="url(#grid)" />

          <!-- Perímetro del Recinto -->
          <rect
            :x="rectX"
            :y="rectY"
            :width="rectW"
            :height="rectH"
            fill="#12121a"
            stroke="#ef4444"
            stroke-width="2"
            stroke-dasharray="4 2"
            rx="4"
          />

          <!-- Área del Escenario / Cabina DJ (Frente) -->
          <rect
            :x="rectX + (rectW - Math.min(rectW * 0.5, 30)) / 2"
            :y="rectY + 3"
            :width="Math.min(rectW * 0.5, 30)"
            :height="10"
            fill="#272738"
            stroke="#f59e0b"
            stroke-width="1.5"
            rx="2"
          />
          <text
            :x="rectX + rectW / 2"
            :y="rectY + 10"
            fill="#fbbf24"
            font-size="4"
            font-family="monospace"
            font-weight="bold"
            text-anchor="middle"
          >
            🎧 ESCENARIO & CABINA DJ
          </text>

          <!-- Pista de Baile / Audiencia -->
          <rect
            :x="rectX + 4"
            :y="rectY + 18"
            :width="rectW - 8"
            :height="rectH - 24"
            fill="#1a1a26"
            stroke="#3b82f6"
            stroke-width="1"
            stroke-dasharray="2 2"
            rx="2"
          />
          <text
            :x="rectX + rectW / 2"
            :y="rectY + rectH / 2"
            fill="#60a5fa"
            font-size="5"
            font-family="monospace"
            font-weight="bold"
            text-anchor="middle"
          >
            💃 PISTA DE BAILE (~{{ calculatedArea }} m²)
          </text>

          <!-- Cotas Métricas: Ancho Superior -->
          <line
            :x1="rectX"
            :y1="rectY - 6"
            :x2="rectX + rectW"
            :y2="rectY - 6"
            stroke="#a1a1aa"
            stroke-width="0.8"
          />
          <text
            :x="rectX + rectW / 2"
            :y="rectY - 8"
            fill="#e4e4e7"
            font-size="4.5"
            font-family="monospace"
            text-anchor="middle"
          >
            ↔ {{ venue.widthMeters || 10 }} metros (Ancho)
          </text>

          <!-- Cotas Métricas: Largo Lateral -->
          <line
            :x1="rectX + rectW + 6"
            :y1="rectY"
            :x2="rectX + rectW + 6"
            :y2="rectY + rectH"
            stroke="#a1a1aa"
            stroke-width="0.8"
          />
          <text
            :x="rectX + rectW + 12"
            :y="rectY + rectH / 2"
            fill="#e4e4e7"
            font-size="4.5"
            font-family="monospace"
            text-anchor="middle"
            :transform="`rotate(90, ${rectX + rectW + 12}, ${rectY + rectH / 2})`"
          >
            ↕ {{ venue.depthMeters || 15 }} metros (Fondo)
          </text>
        </svg>
      </div>

      <!-- Barra de Diagnóstico de Terreno Inferior -->
      <div class="pt-2 border-t border-zinc-800/80 grid grid-cols-3 gap-2 font-mono text-[11px]">
        <div class="p-2 rounded-lg bg-[#14141c] border border-zinc-800 text-zinc-300">
          <span class="text-zinc-500 block text-[9px] uppercase">Atenuación 6dB</span>
          <span class="font-bold text-amber-300">{{ venue.environmentType === 'INDOOR' ? 'Salón con Eco RT60' : 'Campo Libre (-6dB/2x)' }}</span>
        </div>
        <div class="p-2 rounded-lg bg-[#14141c] border border-zinc-800 text-zinc-300">
          <span class="text-zinc-500 block text-[9px] uppercase">Línea Eléctrica</span>
          <span class="font-bold" :class="(venue.electricalDistanceMeters || 10) > 30 ? 'text-red-400' : 'text-emerald-400'">
            {{ (venue.electricalDistanceMeters || 10) > 30 ? 'Requiere 4.0mm²' : 'Estándar 2.5mm²' }}
          </span>
        </div>
        <div class="p-2 rounded-lg bg-[#14141c] border border-zinc-800 text-zinc-300">
          <span class="text-zinc-500 block text-[9px] uppercase">Torre Delay</span>
          <span class="font-bold" :class="(venue.depthMeters || 15) > 18 ? 'text-amber-400' : 'text-zinc-400'">
            {{ (venue.depthMeters || 15) > 18 ? 'Recomendada (>18m)' : 'No requerida' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useStagePlanState } from '../composables/useStagePlanState';

const {
  venue,
  demoPresets,
  activePresetId,
  applyDemoPreset,
  resetValidation,
  storageFeedbackMsg,
} = useStagePlanState();

function onPresetChange(e: Event) {
  const target = e.target as HTMLSelectElement;
  const preset = demoPresets.find((p) => p.id === target.value);
  if (preset) applyDemoPreset(preset);
}

const calculatedArea = computed(() => {
  return (venue.widthMeters && venue.depthMeters) ? Math.round(venue.widthMeters * venue.depthMeters) : 0;
});

const estimatedCrowd = computed(() => {
  return Math.round(calculatedArea.value * 0.72 * 2.2);
});

// Coordenadas reactivas para el SVG
const widthM = computed(() => venue.widthMeters || 12);
const depthM = computed(() => venue.depthMeters || 18);

const rectW = computed(() => widthM.value * 5);
const rectH = computed(() => depthM.value * 5);
const rectX = computed(() => 20);
const rectY = computed(() => 20);

const svgViewBox = computed(() => {
  const totalW = rectW.value + 60;
  const totalH = rectH.value + 50;
  return `0 0 ${Math.max(120, totalW)} ${Math.max(120, totalH)}`;
});
</script>
