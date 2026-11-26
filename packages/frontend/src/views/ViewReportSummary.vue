<template>
  <div class="h-full w-full p-2.5 sm:p-3 lg:p-4 flex flex-col justify-between overflow-hidden font-sans text-xs">
    <!-- FILA SUPERIOR: 4 CARDS DE KPIS EJECUTIVOS (Cockpit Titanium) -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-3 flex-none mb-2">
      <!-- KPI 1: Demanda Eléctrica -->
      <div class="cockpit-card p-2.5 sm:p-3 shadow-lg relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-amber-500"></div>
        <span class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider block">Demanda de Energía</span>
        <div class="flex items-baseline gap-1 mt-0.5">
          <span class="text-lg lg:text-xl font-black font-mono text-white">{{ powerFeasibility.totalSystemDemandWatts || 0 }}</span>
          <span class="text-[10px] text-amber-400 font-bold font-mono">W RMS</span>
        </div>
        <span class="text-[9px] text-zinc-400 font-mono block mt-0.5 truncate">
          Picos: {{ powerFeasibility.transientPeakWatts || 0 }}W · {{ powerSource.type === 'GRID_220V' ? `Red ${powerSource.circuitBreakerAmps}A` : 'Generador' }}
        </span>
      </div>

      <!-- KPI 2: Presión Sonora SPL -->
      <div class="cockpit-card p-2.5 sm:p-3 shadow-lg relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
        <span class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider block">Presión SPL Frente</span>
        <div class="flex items-baseline gap-1 mt-0.5">
          <span class="text-lg lg:text-xl font-black font-mono text-white">{{ Math.round(stageAcousticResult.frontSystem.spl1mContinuous || 0) }}</span>
          <span class="text-[10px] text-emerald-400 font-bold font-mono">dBA a 1m</span>
        </div>
        <span class="text-[9px] text-zinc-400 font-mono block mt-0.5 truncate">
          {{ stageAcousticResult.delayLineRecommendation.required ? `Delay ${stageAcousticResult.delayLineRecommendation.totalDelayMs}ms` : 'Cobertura directa' }}
        </span>
      </div>

      <!-- KPI 3: Logística de Carga -->
      <div class="cockpit-card p-2.5 sm:p-3 shadow-lg relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-purple-500"></div>
        <span class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider block">Peso Total Equipamiento</span>
        <div class="flex items-baseline gap-1 mt-0.5">
          <span class="text-lg lg:text-xl font-black font-mono text-white">{{ Math.round(loadLogistics.grandTotalWeightKg || 0) }}</span>
          <span class="text-[10px] text-purple-400 font-bold font-mono">kg</span>
        </div>
        <span class="text-[9px] text-zinc-400 font-mono block mt-0.5 truncate">
          Vehículo: {{ loadLogistics.recommendedVehicle }}
        </span>
      </div>

      <!-- KPI 4: Ruido Vecinal y SEC -->
      <div class="cockpit-card p-2.5 sm:p-3 shadow-lg relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
        <span class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider block">Normativa Vecinal & SEC</span>
        <div class="flex items-baseline gap-1 mt-0.5">
          <span class="text-sm lg:text-base font-black font-mono" :class="neighborhoodNoiseAudit.status === 'COMPLIANT_SAFE' ? 'text-emerald-400' : 'text-amber-400'">
            {{ neighborhoodNoiseAudit.status === 'COMPLIANT_SAFE' ? '✓ CUMPLE D.S.38' : 'PRECAUCIÓN' }}
          </span>
        </div>
        <span class="text-[9px] text-zinc-400 font-mono block mt-0.5 truncate">
          Dist. Vecino: {{ venue.neighborDistanceMeters }}m (Límite {{ neighborhoodNoiseAudit.legalLimitDba }} dBA)
        </span>
      </div>
    </div>

    <!-- ÁREA CENTRAL DIVIDIDA: VEHÍCULO, CHECKLIST Y EXPORTACIÓN (Cero Scroll a 100% Zoom) -->
    <div class="flex-1 w-full min-h-0 grid grid-cols-1 lg:grid-cols-12 gap-2.5 sm:gap-3 overflow-hidden mb-1">
      <!-- Columna Izquierda: Vehículo Asignado y Ergonomía (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#08090e] border border-zinc-800/90 rounded-xl p-3 flex flex-col justify-between shadow-xl overflow-y-auto">
        <div>
          <div class="flex items-center gap-1.5 pb-2 border-b border-zinc-800 mb-2.5">
            <span class="text-base">🚚</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-[11px] font-mono">
              Logística de Despacho & Flota
            </h3>
          </div>

          <!-- Tarjeta del Vehículo -->
          <div class="p-3 rounded-lg bg-[#10131d] border border-zinc-800/80 space-y-1 mb-2.5">
            <span class="text-[9px] text-zinc-500 uppercase tracking-wider font-bold">Vehículo Recomendado:</span>
            <div class="text-sm font-black text-purple-400 font-mono">
              {{ loadLogistics.recommendedVehicle }}
            </div>
            <p class="text-zinc-400 text-[10px] leading-relaxed">
              Carga total: ~{{ Math.round(loadLogistics.grandTotalWeightKg) }} kg (incluye cableado, atriles y ferretería).
            </p>
          </div>

          <!-- Alerta Ley del Saco -->
          <div
            v-if="loadLogistics.heavyItemsRequiringTwoPeople.length > 0"
            class="p-2.5 rounded-lg bg-amber-950/40 border border-amber-700/60 text-amber-200 space-y-1"
          >
            <div class="flex items-center gap-1.5 font-bold text-[10px]">
              <span>⚠️</span>
              <span>Ley N° 20.949 (Ley del Saco - Máx 25 kg):</span>
            </div>
            <p class="text-[10px] leading-snug text-amber-300">
              Se detectaron <strong>{{ loadLogistics.heavyItemsRequiringTwoPeople.length }} bultos pesados</strong> que superan los 25 kg. Manipulación obligatoria entre 2 personas.
            </p>
          </div>
          <div v-else class="p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-700/60 text-emerald-200 text-[10px]">
            ✓ Todos los bultos cumplen el límite ergonómico de 25 kg para manipulación individual.
          </div>
        </div>

        <div class="pt-2 border-t border-zinc-800/80 text-[9px] text-zinc-500 font-mono">
          Operadores mínimos recomendados: <strong class="text-zinc-300">{{ loadLogistics.recommendedOperatorsCount }} técnicos</strong>
        </div>
      </div>

      <!-- Columna Central: Checklist Operativo de Terreno (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#08090e] border border-zinc-800/90 rounded-xl p-3 flex flex-col justify-between shadow-xl overflow-y-auto">
        <div>
          <div class="flex items-center gap-1.5 pb-2 border-b border-zinc-800 mb-2.5">
            <span class="text-base">📋</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-[11px] font-mono">
              Checklist de Retiro y Montaje
            </h3>
          </div>

          <div class="space-y-1.5">
            <div
              v-for="task in loadLogistics.checklist"
              :key="task.id"
              class="p-2 rounded-lg bg-[#10131d] border border-zinc-800/80 flex items-start gap-2 text-[10px] font-mono"
            >
              <input
                type="checkbox"
                class="mt-0.5 rounded bg-zinc-900 border-zinc-700 text-red-600 focus:ring-0 cursor-pointer"
              />
              <div class="flex-1">
                <span class="font-bold text-zinc-200 block">{{ task.label }}</span>
                <span class="text-[8px] text-zinc-500 uppercase">{{ task.stage }}</span>
              </div>
              <span v-if="task.critical" class="text-[8px] text-red-400 font-bold bg-red-950 px-1 py-0.2 rounded border border-red-800/60">
                CRÍTICO
              </span>
            </div>
          </div>
        </div>

        <div class="pt-2 text-[9px] text-zinc-500 font-mono">
          Revisar antes de salir de bodega y al desmontar a las 5:00 AM.
        </div>
      </div>

      <!-- Columna Derecha: Acciones de Exportación & Firma (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#0c0e15] border border-zinc-800/90 rounded-xl p-3 flex flex-col justify-between shadow-xl">
        <div class="space-y-2.5">
          <div class="flex items-center gap-1.5 pb-1.5 border-b border-zinc-800">
            <span class="text-base">📄</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-[11px] font-mono">
              Memoria Técnica & Despacho
            </h3>
          </div>

          <div class="p-2.5 bg-[#10131d] border border-zinc-800/80 rounded-lg space-y-1 text-[10px] font-mono">
            <span class="text-zinc-500 text-[9px] uppercase block font-bold">Responsable Técnico Firmante:</span>
            <div class="font-bold text-zinc-100">{{ operatorSignature }}</div>
            <div class="text-zinc-500 text-[9px]">
              Trazabilidad SEC RIC N° 10, atenuación acústica ISO 9613 y protocolo puesta a tierra.
            </div>
          </div>

          <!-- Botón WhatsApp -->
          <button
            type="button"
            @click="copyWhatsAppSummary"
            class="w-full py-2 px-3 rounded-lg bg-[#182030] hover:bg-[#202b40] border border-zinc-700 text-white font-mono font-bold text-xs transition flex items-center justify-center gap-1.5 cursor-pointer shadow-md"
          >
            <span>📱</span>
            <span>{{ whatsappCopied ? '✓ ¡Copiado al Portapapeles!' : 'Copiar Resumen WhatsApp' }}</span>
          </button>
        </div>

        <!-- Botón Principal Descargar PDF -->
        <button
          type="button"
          @click="downloadPdf"
          :disabled="!isValidated"
          class="w-full py-2.5 px-3 rounded-lg bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 disabled:opacity-40 text-white font-mono font-black uppercase tracking-wider transition flex items-center justify-center gap-1.5 cursor-pointer shadow-lg shadow-red-950/70 text-xs"
        >
          <span>📄</span>
          <span>Descargar Memoria Técnica PDF →</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStagePlanState } from '../composables/useStagePlanState';

const {
  venue,
  powerFeasibility,
  powerSource,
  stageAcousticResult,
  loadLogistics,
  neighborhoodNoiseAudit,
  operatorSignature,
  whatsappCopied,
  copyWhatsAppSummary,
  downloadPdf,
  isValidated,
} = useStagePlanState();
</script>
