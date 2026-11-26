<template>
  <footer class="h-[52px] flex-none border-t border-zinc-800 bg-[#0c0c12] px-4 flex items-center justify-between select-none z-30">
    <!-- HUD de Telemetría en Vivo (Izquierda) -->
    <div class="flex items-center space-x-2 sm:space-x-4 overflow-x-auto text-xs font-mono py-1">
      <!-- Potencia Demandada -->
      <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-300">
        <span class="text-amber-400">⚡</span>
        <span class="font-bold text-white">{{ powerFeasibility.totalSystemDemandWatts || 0 }}W</span>
        <span class="text-[10px] text-zinc-500 hidden sm:inline">DEMANDA</span>
      </div>

      <!-- Fuente / Amperios -->
      <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-300">
        <span class="text-blue-400">🔌</span>
        <span class="font-bold text-white">
          {{ powerSource.type === 'GRID_220V' ? `Red ${powerSource.circuitBreakerAmps}A` : 'Generador' }}
        </span>
      </div>

      <!-- Presión Sonora SPL -->
      <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-300">
        <span class="text-emerald-400">🎯</span>
        <span class="font-bold text-white">{{ Math.round(stageAcousticResult.frontSystem.spl1mContinuous || 0) }} dBA</span>
        <span class="text-[10px] text-zinc-500 hidden md:inline">SPL 1M</span>
      </div>

      <!-- Carga Logística Total -->
      <div class="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-zinc-900 border border-zinc-800 text-zinc-300">
        <span class="text-purple-400">📦</span>
        <span class="font-bold text-white">{{ Math.round(loadLogistics.grandTotalWeightKg || 0) }} kg</span>
        <span class="text-[10px] text-zinc-500">CARGA</span>
      </div>

      <!-- Alerta Rápida -->
      <span
        v-if="powerAlertLevel === 'CRITICAL'"
        class="text-[10px] px-2 py-0.5 rounded bg-red-950 text-red-300 border border-red-700 font-bold animate-pulse"
      >
        ⚠️ SOBRECARGA
      </span>
    </div>

    <!-- Acciones de Navegación del Wizard (Derecha) -->
    <div class="flex items-center space-x-2">
      <button
        v-if="currentStep > 1"
        @click="prevStep"
        class="px-3 py-1.5 rounded-lg bg-zinc-800/80 hover:bg-zinc-700 text-zinc-200 text-xs font-mono font-bold transition flex items-center gap-1 cursor-pointer"
      >
        <span>←</span>
        <span class="hidden sm:inline">Anterior</span>
      </button>

      <button
        v-if="currentStep < 4"
        @click="nextStep"
        class="px-4 py-1.5 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-mono font-black uppercase tracking-wider transition shadow-md shadow-red-950/80 flex items-center gap-1.5 cursor-pointer"
      >
        <span>{{ currentStep === 2 ? '⚡ Confirmar y Ver 2D' : currentStep === 3 ? '📋 Ver Reporte Final' : 'Siguiente' }}</span>
        <span>→</span>
      </button>

      <button
        v-else-if="currentStep === 4"
        @click="downloadPdf"
        :disabled="!isValidated"
        class="px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white text-xs font-mono font-black uppercase tracking-wider transition shadow-md shadow-emerald-950/80 flex items-center gap-1.5 cursor-pointer"
      >
        <span>📄 Descargar Memoria PDF</span>
      </button>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { useStagePlanState } from '../../composables/useStagePlanState';

const {
  currentStep,
  nextStep,
  prevStep,
  powerFeasibility,
  powerSource,
  stageAcousticResult,
  loadLogistics,
  powerAlertLevel,
  isValidated,
  downloadPdf,
} = useStagePlanState();
</script>
