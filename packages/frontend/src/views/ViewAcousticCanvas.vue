<template>
  <div class="h-full w-full p-2.5 sm:p-3 lg:p-4 flex flex-col justify-between overflow-hidden relative font-mono text-xs">
    <!-- BARRA SUPERIOR FLOTANTE DEL LIENZO CAD (TOOLSET & ZOOM CONTROLS) -->
    <div class="flex-none bg-[#0e0e14] border border-zinc-800 rounded-xl px-3 sm:px-4 py-2 flex flex-wrap items-center justify-between gap-2.5 shadow-xl z-20">
      <!-- Identificador de la Vista y Dimensiones -->
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse"></span>
        <span class="font-black text-white uppercase tracking-wider text-xs">
          [ 3 ] Plano Espacial & Cobertura Acústica 2D
        </span>
        <span class="text-zinc-500 text-[11px] hidden md:inline">
          · Recinto: {{ venue.widthMeters || 10 }}m × {{ venue.depthMeters || 16 }}m ({{ (venue.widthMeters || 10) * (venue.depthMeters || 16) }} m²)
        </span>
      </div>

      <!-- CONTROLES DE ZOOM Y PANORÁMICA 2D -->
      <div class="flex items-center gap-1 bg-[#14141d] border border-zinc-700/80 rounded-lg p-1 shadow-inner">
        <!-- Disminuir Zoom (-) -->
        <button
          type="button"
          @click="decreaseZoom"
          :disabled="zoomPercent <= 50"
          class="w-7 h-7 rounded bg-zinc-900 hover:bg-zinc-800 disabled:opacity-40 disabled:cursor-not-allowed text-zinc-200 hover:text-white font-black text-sm flex items-center justify-center transition border border-zinc-800 cursor-pointer"
          title="Alejar Zoom (-25%)"
        >
          −
        </button>

        <!-- Nivel de Zoom Actual (Clic para menú / toggle 100%) -->
        <button
          type="button"
          @click="resetZoom100"
          class="px-2 h-7 rounded bg-zinc-900 hover:bg-zinc-800 text-amber-400 font-mono font-bold text-[11px] flex items-center gap-1 border border-zinc-800 transition cursor-pointer"
          title="Restablecer a 100% Escala Real"
        >
          <span>🔍</span>
          <span>{{ zoomMode === 'fit' ? 'Ajustado' : `${zoomPercent}%` }}</span>
        </button>

        <!-- Aumentar Zoom (+) -->
        <button
          type="button"
          @click="increaseZoom"
          :disabled="zoomPercent >= 200"
          class="w-7 h-7 rounded bg-zinc-900 hover:bg-zinc-800 disabled:opacity-40 disabled:cursor-not-allowed text-zinc-200 hover:text-white font-black text-sm flex items-center justify-center transition border border-zinc-800 cursor-pointer"
          title="Acercar Zoom (+25%)"
        >
          +
        </button>

        <!-- Presets de Zoom Rápido -->
        <div class="hidden sm:flex items-center gap-1 ml-1 pl-1 border-l border-zinc-800">
          <button
            type="button"
            @click="setZoomMode('fit')"
            :class="[
              'px-2 py-1 rounded text-[10px] font-bold uppercase transition cursor-pointer',
              zoomMode === 'fit'
                ? 'bg-blue-600 text-white border border-blue-400'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
            ]"
            title="Ajustar recinto completo a la ventana (Cero Scroll)"
          >
            Ajustar
          </button>
          <button
            type="button"
            @click="setZoomPercent(100)"
            :class="[
              'px-2 py-1 rounded text-[10px] font-bold uppercase transition cursor-pointer',
              zoomMode === 'custom' && zoomPercent === 100
                ? 'bg-blue-600 text-white border border-blue-400'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
            ]"
            title="Escala estándar 100%"
          >
            100%
          </button>
          <button
            type="button"
            @click="setZoomPercent(150)"
            :class="[
              'px-2 py-1 rounded text-[10px] font-bold uppercase transition cursor-pointer',
              zoomMode === 'custom' && zoomPercent === 150
                ? 'bg-blue-600 text-white border border-blue-400'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
            ]"
            title="Ampliación detallada 150%"
          >
            150%
          </button>
          <button
            type="button"
            @click="setZoomPercent(200)"
            :class="[
              'px-2 py-1 rounded text-[10px] font-bold uppercase transition cursor-pointer',
              zoomMode === 'custom' && zoomPercent === 200
                ? 'bg-blue-600 text-white border border-blue-400'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800'
            ]"
            title="Máxima inspección 200% (Scroll 2D libre)"
          >
            200%
          </button>
        </div>
      </div>

      <!-- Herramientas y Modales Flotantes -->
      <div class="flex items-center gap-1.5 sm:gap-2">
        <button
          type="button"
          @click="showMixerModal = true"
          class="px-2.5 sm:px-3 py-1 rounded-lg bg-red-600/20 hover:bg-red-600/30 border border-red-500/50 text-red-300 font-bold transition flex items-center gap-1 cursor-pointer text-[11px]"
        >
          <span>🎛️</span>
          <span class="hidden sm:inline">Mixer</span> DJM
        </button>

        <button
          type="button"
          @click="showPlanBModal = true"
          class="px-2.5 sm:px-3 py-1 rounded-lg bg-amber-600/20 hover:bg-amber-600/30 border border-amber-500/50 text-amber-300 font-bold transition flex items-center gap-1 cursor-pointer text-[11px]"
        >
          <span>🚨</span>
          <span>Plan B</span>
        </button>

        <button
          type="button"
          @click="showSecModal = true"
          class="px-2.5 py-1 rounded-lg bg-sky-950 hover:bg-sky-900 border border-sky-700 text-sky-300 font-bold transition cursor-pointer text-[11px]"
          title="Ver Guía de Postes y Curvatura SEC RIC 10"
        >
          📍 RIC 10
        </button>
      </div>
    </div>

    <!-- ÁREA CENTRAL DE TRABAJO CAD (VISOR 2D CON PANORÁMICA Y SCROLL BIDIRECCIONAL) -->
    <div
      ref="cadViewportRef"
      @wheel="handleViewportWheel"
      class="flex-1 w-full min-h-0 bg-[#060609] border border-zinc-800 rounded-2xl my-2 relative overflow-auto shadow-2xl cad-scroll-container"
    >
      <!-- Canvas Wrapper con escala reactiva -->
      <div
        class="min-h-full flex items-center justify-center p-2 sm:p-4 transition-all duration-150"
        :class="{
          'w-full h-full': zoomMode === 'fit',
          'w-max h-max mx-auto': zoomMode === 'custom'
        }"
      >
        <div
          class="transition-all duration-150"
          :style="canvasStyle"
        >
          <LayoutSvg2D
            :venue-width="venue.widthMeters || 10"
            :venue-depth="venue.depthMeters || 16"
            :subs-count="totalSubsCount"
            :tops-count="totalTopsCount"
            :roster-nodes="hybridAnalysis.roster"
            :power-plan="powerDistributionPlan"
            :lighting-analysis="lightingDmxAnalysis"
          />
        </div>
      </div>

      <!-- HUD Flotante en la esquina inferior del plano con ayuda de navegación -->
      <div class="absolute bottom-3 left-4 pointer-events-none hidden sm:flex items-center gap-2 bg-black/75 backdrop-blur-md border border-zinc-800/80 px-3 py-1 rounded-lg text-[10px] text-zinc-400 font-mono shadow-lg">
        <span class="text-zinc-500">TIP:</span>
        <span>Usa Ctrl + Rueda para hacer zoom · Desplaza el ratón o táctil para navegar en 2D</span>
        <span v-if="zoomMode === 'custom' && zoomPercent > 100" class="text-amber-400 font-bold">
          [Modo Detalle Activo]
        </span>
      </div>
    </div>

    <!-- MODAL 1: CONSOLA HARDWARE REPLICA PIONEER DJM -->
    <div
      v-if="showMixerModal"
      class="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in"
    >
      <div class="bg-[#0e0e14] border-2 border-red-600/80 rounded-3xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-zinc-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🎛️</span>
            <h3 class="text-sm font-black uppercase text-white font-mono tracking-wider">
              Simulador Hardware Pioneer DJM · Gain Staging & Vúmetros
            </h3>
          </div>
          <button
            @click="showMixerModal = false"
            class="text-zinc-400 hover:text-white font-mono font-bold text-sm px-2 py-1 bg-zinc-800 rounded-lg cursor-pointer"
          >
            ✕ Cerrar
          </button>
        </div>

        <PioneerMixerSimulator />
      </div>
    </div>

    <!-- MODAL 2: SIMULADOR PLAN B (CONTINGENCIA EN VIVO) -->
    <div
      v-if="showPlanBModal"
      class="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in"
    >
      <div class="bg-[#0e0e14] border-2 border-amber-600/80 rounded-3xl max-w-3xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-zinc-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="text-xl">🚨</span>
            <h3 class="text-sm font-black uppercase text-white font-mono tracking-wider">
              Simulador "Plan B" ante Falla en Plena Fiesta (HU08 / CU-07)
            </h3>
          </div>
          <button
            @click="showPlanBModal = false"
            class="text-zinc-400 hover:text-white font-mono font-bold text-sm px-2 py-1 bg-zinc-800 rounded-lg cursor-pointer"
          >
            ✕ Cerrar
          </button>
        </div>

        <!-- Opciones de Escenario -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 font-mono text-xs">
          <button
            v-for="(label, key) in contingencyScenarios"
            :key="key"
            @click="activeContingencyScenario = key"
            class="p-3 rounded-xl border text-left font-bold transition cursor-pointer"
            :class="activeContingencyScenario === key ? 'bg-amber-600 text-white border-amber-400' : 'bg-zinc-900 text-zinc-300 border-zinc-700 hover:border-amber-500'"
          >
            {{ label }}
          </button>
        </div>

        <!-- Resultado del Plan B -->
        <div class="p-4 rounded-xl bg-zinc-900/80 border border-zinc-800 space-y-2">
          <div class="flex items-center justify-between text-xs font-bold text-amber-400">
            <span>Directiva Operativa:</span>
            <span>Severidad: {{ contingencyPlan.severity }}</span>
          </div>
          <p class="text-zinc-200 text-xs leading-relaxed">
            {{ contingencyPlan.mixerDirective }}
          </p>
          <div class="space-y-1.5 pt-2 border-t border-zinc-800">
            <div
              v-for="(st, sIdx) in contingencyPlan.steps"
              :key="sIdx"
              class="text-[11px] text-zinc-300 flex items-start gap-2"
            >
              <span class="text-amber-400 font-bold">{{ sIdx + 1 }}.</span>
              <span><strong>{{ st.action }}:</strong> {{ st.reason }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL 3: GUÍA SEC RIC N° 10 -->
    <div
      v-if="showSecModal"
      class="fixed inset-0 bg-black/85 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in"
    >
      <div class="bg-[#0b111a] border-2 border-sky-600 rounded-3xl max-w-2xl w-full p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-sky-900 pb-3">
          <h3 class="text-sm font-black uppercase text-sky-400 font-mono tracking-wider flex items-center gap-2">
            <span>📍</span>
            <span>Soportes de Esquina y Radio de Curvatura (SEC RIC N° 10)</span>
          </h3>
          <button
            @click="showSecModal = false"
            class="text-zinc-400 hover:text-white font-mono font-bold text-sm px-2 py-1 bg-zinc-800 rounded-lg cursor-pointer"
          >
            ✕ Cerrar
          </button>
        </div>

        <div class="text-zinc-300 text-xs space-y-3 leading-relaxed">
          <p>
            En eventos profesionales, en las esquinas y aristas del trazado perimetral se instalan <strong>Postes Guía Pasacables (Tótems de amarre)</strong> si el tendido va perimetral elevado, o <strong>Pasacables Esquineros a 90° (Codos pasacables)</strong> si va por el suelo. Sirven para dar el radio de doblez suave al cable, evitando que quede tirante o expuesto a machacamiento.
          </p>
          <div class="p-3 bg-sky-950/60 border border-sky-800 rounded-xl text-sky-200">
            <strong>Exigencia SEC RIC N° 10 (Radio de Curvatura R ≥ 6d):</strong>
            El radio mínimo de curvatura no debe ser inferior a 6 veces el diámetro exterior del cable para evitar fracturas internas del cobre por tracción.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useStagePlanState } from '../composables/useStagePlanState';
import LayoutSvg2D from '../components/LayoutSvg2D.vue';
import PioneerMixerSimulator from '../components/PioneerMixerSimulator.vue';
import type { ContingencyScenario } from '@stageplan/shared';

const {
  venue,
  totalTopsCount,
  totalSubsCount,
  hybridAnalysis,
  powerDistributionPlan,
  lightingDmxAnalysis,
  stageAcousticResult,
  activeContingencyScenario,
  contingencyPlan,
} = useStagePlanState();

const showMixerModal = ref(false);
const showPlanBModal = ref(false);
const showSecModal = ref(false);

const contingencyScenarios: Record<ContingencyScenario, string> = {
  GENERATOR_FAIL_TO_10A: '⚡ Murió Generador → Respaldo 10A Domicilio',
  TOP_BOX_FAILURE: '🔊 Murió 1 Caja Top en Vivo',
  SUB_FAILURE: '🎛️ Falla de Subwoofer en Vivo',
  LIGHTING_BREAKER_TRIP: '🔥 Disparo Térmico Línea Iluminación',
};

// ----------------------------------------------------------------------------
// SISTEMA DE ZOOM Y PANORÁMICA 2D RESPONSIVO
// ----------------------------------------------------------------------------
const cadViewportRef = ref<HTMLElement | null>(null);
const zoomMode = ref<'fit' | 'custom'>('fit');
const zoomPercent = ref<number>(100);

function setZoomMode(mode: 'fit' | 'custom') {
  zoomMode.value = mode;
  if (mode === 'fit') {
    zoomPercent.value = 100;
  }
}

function setZoomPercent(percent: number) {
  zoomMode.value = 'custom';
  zoomPercent.value = Math.max(50, Math.min(250, percent));
}

function increaseZoom() {
  zoomMode.value = 'custom';
  zoomPercent.value = Math.min(250, zoomPercent.value + 25);
}

function decreaseZoom() {
  zoomMode.value = 'custom';
  zoomPercent.value = Math.max(50, zoomPercent.value - 25);
}

function resetZoom100() {
  if (zoomMode.value === 'fit') {
    setZoomPercent(100);
  } else {
    setZoomMode('fit');
  }
}

// Soporte para Zoom fluido con Ctrl + Rueda del ratón
function handleViewportWheel(e: WheelEvent) {
  if (e.ctrlKey) {
    e.preventDefault();
    if (e.deltaY < 0) {
      increaseZoom();
    } else {
      decreaseZoom();
    }
  }
}

// Cálculo del estilo dinámico para el contenedor del plano
const canvasStyle = computed(() => {
  if (zoomMode.value === 'fit') {
    return {
      width: '100%',
      maxWidth: '1200px',
    };
  }

  // Base en píxeles ajustada al ratio de aspecto del recinto
  const baseWidthPx = 1000;
  const scaledWidth = Math.round(baseWidthPx * (zoomPercent.value / 100));

  return {
    width: `${scaledWidth}px`,
    minWidth: `${scaledWidth}px`,
  };
});
</script>

<style scoped>
/* Barras de desplazamiento estilizadas tipo CAD Oscuro */
.cad-scroll-container {
  scrollbar-width: thin;
  scrollbar-color: #3f3f46 #09090d;
}

.cad-scroll-container::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.cad-scroll-container::-webkit-scrollbar-track {
  background: #09090d;
  border-radius: 8px;
}

.cad-scroll-container::-webkit-scrollbar-thumb {
  background-color: #27272a;
  border-radius: 8px;
  border: 2px solid #09090d;
}

.cad-scroll-container::-webkit-scrollbar-thumb:hover {
  background-color: #3f3f46;
}

.cad-scroll-container::-webkit-scrollbar-corner {
  background: #09090d;
}
</style>
