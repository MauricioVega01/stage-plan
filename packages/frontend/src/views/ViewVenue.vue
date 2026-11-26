<template>
  <div class="h-full w-full p-2.5 sm:p-3 lg:p-4 grid grid-cols-1 lg:grid-cols-12 gap-3 lg:gap-4 overflow-hidden font-sans">
    <!-- PANEL IZQUIERDO: FORMULARIO Y PRESETS (Cockpit Ergonómico a Zoom 100%) -->
    <div class="lg:col-span-5 h-full flex flex-col space-y-2.5 overflow-y-auto pr-0.5">
      <!-- Selector de Casos Cotidianos Rápido (Preset Rack) -->
      <div class="cockpit-card p-3 shadow-lg">
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[10px] font-sans font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
            <span class="text-amber-400">⚡</span>
            <span>Presets Rápidos (8 Escalas de Evento)</span>
          </span>
          <span v-if="storageFeedbackMsg" class="text-[10px] text-emerald-400 font-mono font-bold animate-pulse">
            {{ storageFeedbackMsg }}
          </span>
        </div>
        <select
          :value="activePresetId || ''"
          @change="onPresetChange"
          class="w-full h-8 bg-[#131622] border border-zinc-700/80 rounded-lg px-2.5 text-xs text-zinc-200 font-mono focus:outline-none focus:border-red-500/80 transition cursor-pointer"
        >
          <option value="" disabled>Selecciona un caso cotidiano para autocompletar...</option>
          <option v-for="p in demoPresets" :key="p.id" :value="p.id">
            {{ p.scaleTag }} · {{ p.title }}
          </option>
        </select>
      </div>

      <!-- Tarjeta de Medidas Principales (Cockpit Sizing) -->
      <div class="cockpit-card p-3.5 shadow-xl flex-1 flex flex-col justify-between relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-red-600"></div>

        <div class="space-y-3">
          <!-- Cabecera de la Tarjeta -->
          <div class="flex items-center justify-between border-b border-zinc-800/80 pb-2">
            <h2 class="text-xs font-black tracking-wider text-white uppercase font-mono flex items-center gap-1.5">
              <span class="text-red-500 font-mono">[ 1 ]</span>
              <span>Geometría del Recinto</span>
            </h2>
            <span class="text-[10px] font-mono text-zinc-500">Superficie & Acústica</span>
          </div>

          <!-- Campos del Formulario con Densidad Óptima -->
          <div class="space-y-2.5">
            <!-- Nombre del Evento / Recinto -->
            <div>
              <label class="cockpit-label">Nombre del Recinto o Parcela</label>
              <input
                v-model="venue.name"
                @input="resetValidation"
                type="text"
                placeholder="Ej: Parcela Los Aromos, Curacaví"
                class="w-full cockpit-input"
              />
            </div>

            <!-- Ancho y Largo (Grid 2 Cols) -->
            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="cockpit-label flex items-center justify-between">
                  <span>Ancho (m)</span>
                  <span class="text-zinc-500 font-mono font-normal">{{ venue.widthMeters || '--' }}m</span>
                </label>
                <input
                  v-model.number="venue.widthMeters"
                  @input="resetValidation"
                  type="number"
                  min="3"
                  max="80"
                  step="0.5"
                  placeholder="12"
                  class="w-full cockpit-input text-amber-300 font-bold"
                />
              </div>

              <div>
                <label class="cockpit-label flex items-center justify-between">
                  <span>Largo (m)</span>
                  <span class="text-zinc-500 font-mono font-normal">{{ venue.depthMeters || '--' }}m</span>
                </label>
                <input
                  v-model.number="venue.depthMeters"
                  @input="resetValidation"
                  type="number"
                  min="3"
                  max="100"
                  step="0.5"
                  placeholder="18"
                  class="w-full cockpit-input text-amber-300 font-bold"
                />
              </div>
            </div>

            <!-- Distancia Eléctrica y Tipo de Entorno -->
            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="cockpit-label">Dist. Eléctrica (m)</label>
                <input
                  v-model.number="venue.electricalDistanceMeters"
                  @input="resetValidation"
                  type="number"
                  min="1"
                  max="150"
                  placeholder="25"
                  class="w-full cockpit-input font-bold"
                />
              </div>

              <div>
                <label class="cockpit-label">Tipo de Entorno</label>
                <select
                  v-model="venue.environmentType"
                  @change="resetValidation"
                  class="w-full cockpit-input cursor-pointer"
                >
                  <option value="INDOOR">🏛️ Salón Cerrado</option>
                  <option value="OUTDOOR_PARCELA">🌲 Parcela / Aire Libre</option>
                </select>
              </div>
            </div>

            <!-- Duración Música y Altura de Techo -->
            <div class="grid grid-cols-2 gap-2.5">
              <div>
                <label class="cockpit-label">Duración Música (hrs)</label>
                <input
                  v-model.number="venue.eventDurationHours"
                  @input="resetValidation"
                  type="number"
                  min="1"
                  max="24"
                  placeholder="7"
                  class="w-full cockpit-input"
                />
              </div>

              <div>
                <label class="cockpit-label">Alto Techo (m)</label>
                <input
                  v-model.number="venue.heightMeters"
                  @input="resetValidation"
                  type="number"
                  min="2"
                  max="15"
                  step="0.5"
                  placeholder="3.5"
                  class="w-full cockpit-input"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Indicador de Superficie y Aforo Compacto -->
        <div class="bg-[#10131d] border border-zinc-800/80 rounded-lg p-2.5 flex items-center justify-between font-mono mt-2">
          <div>
            <span class="text-[9px] text-zinc-500 uppercase tracking-wider block">Superficie Total & Aforo Recomendado</span>
            <span class="text-xs font-black text-red-400">
              {{ calculatedArea }} m²
              <span class="text-zinc-400 font-normal text-[11px] ml-1">(~{{ estimatedCrowd }} personas)</span>
            </span>
          </div>
          <span class="text-base text-zinc-400">📐</span>
        </div>
      </div>
    </div>

    <!-- PANEL DERECHO: VISUALIZADOR PERIMÉTRICO 2D REACTIVO EN VIVO -->
    <div class="lg:col-span-7 h-full bg-[#08090e] border border-zinc-800/90 rounded-xl p-3 sm:p-3.5 flex flex-col justify-between shadow-2xl relative overflow-hidden">
      <!-- Barra Superior de Herramientas del Visualizador -->
      <div class="flex items-center justify-between pb-2 border-b border-zinc-800/80 font-mono text-[11px]">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="font-bold text-zinc-300 uppercase tracking-wider">Perímetro Espacial CAD</span>
        </div>
        <div class="text-zinc-400 font-bold bg-[#10131d] px-2 py-0.5 rounded border border-zinc-800">
          📐 {{ venue.widthMeters || 10 }}m × {{ venue.depthMeters || 15 }}m
        </div>
      </div>

      <!-- Lienzo SVG Perimétrico Auto-escalable con Grilla Oscura de Precisión -->
      <div class="flex-1 w-full min-h-0 flex items-center justify-center p-1 relative select-none">
        <svg
          class="w-full h-full max-h-full transition-all duration-200"
          :viewBox="svgViewBox"
          preserveAspectRatio="xMidYMid meet"
        >
          <!-- Grilla de Radar Técnico -->
          <defs>
            <pattern id="venueGrid" width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#161926" stroke-width="0.5" />
            </pattern>
          </defs>
          <rect x="-100" y="-100" width="500" height="500" fill="url(#venueGrid)" />

          <!-- Perímetro Exterior del Recinto -->
          <rect
            :x="rectX"
            :y="rectY"
            :width="rectW"
            :height="rectH"
            fill="#0c0e17"
            stroke="#ef4444"
            stroke-width="1.8"
            stroke-dasharray="5 2.5"
            rx="4"
          />

          <!-- Área del Escenario / Cabina DJ (Frente) -->
          <rect
            :x="rectX + (rectW - Math.min(rectW * 0.5, 30)) / 2"
            :y="rectY + 3"
            :width="Math.min(rectW * 0.5, 30)"
            :height="10"
            fill="#1e2233"
            stroke="#f59e0b"
            stroke-width="1.2"
            rx="2"
          />
          <text
            :x="rectX + rectW / 2"
            :y="rectY + 9.5"
            fill="#fbbf24"
            font-size="4"
            font-family="monospace"
            font-weight="bold"
            text-anchor="middle"
          >
            🎧 ESCENARIO & CABINA DJ
          </text>

          <!-- Pista de Baile / Zona de Audiencia -->
          <rect
            :x="rectX + 4"
            :y="rectY + 18"
            :width="rectW - 8"
            :height="rectH - 24"
            fill="#101420"
            stroke="#06b6d4"
            stroke-width="0.8"
            stroke-dasharray="2.5 2"
            rx="2"
          />
          <text
            :x="rectX + rectW / 2"
            :y="rectY + rectH / 2"
            fill="#38bdf8"
            font-size="4.5"
            font-family="monospace"
            font-weight="bold"
            text-anchor="middle"
          >
            💃 PISTA DE BAILE (~{{ calculatedArea }} m²)
          </text>

          <!-- Cota Superior: Ancho -->
          <line
            :x1="rectX"
            :y1="rectY - 6"
            :x2="rectX + rectW"
            :y2="rectY - 6"
            stroke="#71717a"
            stroke-width="0.7"
          />
          <text
            :x="rectX + rectW / 2"
            :y="rectY - 8.5"
            fill="#e4e4e7"
            font-size="4"
            font-family="monospace"
            font-weight="bold"
            text-anchor="middle"
          >
            ↔ {{ venue.widthMeters || 10 }}m (Ancho)
          </text>

          <!-- Cota Lateral: Fondo -->
          <line
            :x1="rectX + rectW + 6"
            :y1="rectY"
            :x2="rectX + rectW + 6"
            :y2="rectY + rectH"
            stroke="#71717a"
            stroke-width="0.7"
          />
          <text
            :x="rectX + rectW + 11"
            :y="rectY + rectH / 2"
            fill="#e4e4e7"
            font-size="4"
            font-family="monospace"
            font-weight="bold"
            text-anchor="middle"
            :transform="`rotate(90, ${rectX + rectW + 11}, ${rectY + rectH / 2})`"
          >
            ↕ {{ venue.depthMeters || 15 }}m (Fondo)
          </text>
        </svg>
      </div>

      <!-- Barra de Diagnóstico de Terreno Inferior -->
      <div class="pt-2 border-t border-zinc-800/80 grid grid-cols-3 gap-2 font-mono text-[10px]">
        <div class="p-1.5 rounded bg-[#10131d] border border-zinc-800/80 text-zinc-300">
          <span class="text-zinc-500 block text-[8px] uppercase">Atenuación SPL</span>
          <span class="font-bold text-amber-300 truncate block">{{ venue.environmentType === 'INDOOR' ? 'Salón RT60' : 'Campo Libre (-6dB)' }}</span>
        </div>
        <div class="p-1.5 rounded bg-[#10131d] border border-zinc-800/80 text-zinc-300">
          <span class="text-zinc-500 block text-[8px] uppercase">Alargador SEC</span>
          <span class="font-bold truncate block" :class="(venue.electricalDistanceMeters || 10) > 30 ? 'text-red-400' : 'text-emerald-400'">
            {{ (venue.electricalDistanceMeters || 10) > 30 ? 'Requiere 4.0mm²' : 'Estándar 2.5mm²' }}
          </span>
        </div>
        <div class="p-1.5 rounded bg-[#10131d] border border-zinc-800/80 text-zinc-300">
          <span class="text-zinc-500 block text-[8px] uppercase">Línea Delay</span>
          <span class="font-bold truncate block" :class="(venue.depthMeters || 15) > 18 ? 'text-amber-400' : 'text-zinc-400'">
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
