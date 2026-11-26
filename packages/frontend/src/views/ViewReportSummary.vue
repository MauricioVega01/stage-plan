<template>
  <div class="h-full w-full p-4 lg:p-6 flex flex-col justify-between overflow-hidden font-mono text-xs">
    <!-- FILA SUPERIOR: 4 CARDS DE KPIS EJECUTIVOS (Cero Scroll) -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4 flex-none mb-3">
      <!-- KPI 1: Demanda Eléctrica -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-3.5 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-amber-500"></div>
        <span class="text-[10px] text-zinc-500 uppercase tracking-wider block">Demanda de Energía</span>
        <div class="flex items-baseline gap-1 mt-1">
          <span class="text-xl lg:text-2xl font-black text-white">{{ powerFeasibility.totalSystemDemandWatts || 0 }}</span>
          <span class="text-xs text-amber-400 font-bold">W RMS</span>
        </div>
        <span class="text-[10px] text-zinc-400 block mt-1 truncate">
          Picos: {{ powerFeasibility.transientPeakWatts || 0 }}W · {{ powerSource.type === 'GRID_220V' ? `Red ${powerSource.circuitBreakerAmps}A` : 'Generador' }}
        </span>
      </div>

      <!-- KPI 2: Presión Sonora SPL -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-3.5 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
        <span class="text-[10px] text-zinc-500 uppercase tracking-wider block">Presión SPL Frente</span>
        <div class="flex items-baseline gap-1 mt-1">
          <span class="text-xl lg:text-2xl font-black text-white">{{ Math.round(stageAcousticResult.frontSystem.spl1mContinuous || 0) }}</span>
          <span class="text-xs text-emerald-400 font-bold">dBA a 1m</span>
        </div>
        <span class="text-[10px] text-zinc-400 block mt-1 truncate">
          {{ stageAcousticResult.delayLineRecommendation.required ? `Delay ${stageAcousticResult.delayLineRecommendation.totalDelayMs}ms requerido` : 'Cobertura directa óptima' }}
        </span>
      </div>

      <!-- KPI 3: Logística de Carga -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-3.5 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-purple-500"></div>
        <span class="text-[10px] text-zinc-500 uppercase tracking-wider block">Peso Total Equipamiento</span>
        <div class="flex items-baseline gap-1 mt-1">
          <span class="text-xl lg:text-2xl font-black text-white">{{ Math.round(loadLogistics.grandTotalWeightKg || 0) }}</span>
          <span class="text-xs text-purple-400 font-bold">kg</span>
        </div>
        <span class="text-[10px] text-zinc-400 block mt-1 truncate">
          Vehículo: {{ loadLogistics.recommendedVehicle }}
        </span>
      </div>

      <!-- KPI 4: Ruido Vecinal y SEC -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-3.5 shadow-xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
        <span class="text-[10px] text-zinc-500 uppercase tracking-wider block">Normativa Vecinal & SEC</span>
        <div class="flex items-baseline gap-1 mt-1">
          <span class="text-base lg:text-lg font-black" :class="neighborhoodNoiseAudit.status === 'COMPLIANT_SAFE' ? 'text-emerald-400' : 'text-amber-400'">
            {{ neighborhoodNoiseAudit.status === 'COMPLIANT_SAFE' ? '✓ CUMPLE D.S.38' : 'PRECAUCIÓN' }}
          </span>
        </div>
        <span class="text-[10px] text-zinc-400 block mt-1 truncate">
          Dist. Vecino: {{ venue.neighborDistanceMeters }}m (Límite {{ neighborhoodNoiseAudit.legalLimitDba }} dBA)
        </span>
      </div>
    </div>

    <!-- ÁREA CENTRAL DIVIDIDA: VEHÍCULO, CHECKLIST Y EXPORTACIÓN (Cero Scroll) -->
    <div class="flex-1 w-full min-h-0 grid grid-cols-1 lg:grid-cols-12 gap-4 overflow-hidden mb-3">
      <!-- Columna Izquierda: Vehículo Asignado y Ergonomía (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#0a0a0f] border border-zinc-800 rounded-2xl p-4 flex flex-col justify-between shadow-xl overflow-y-auto">
        <div>
          <div class="flex items-center gap-2 pb-2 border-b border-zinc-800 mb-3">
            <span class="text-lg">🚚</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-xs">
              Logística de Despacho & Movilización
            </h3>
          </div>

          <!-- Tarjeta del Vehículo -->
          <div class="p-4 rounded-xl bg-[#12121a] border border-zinc-800 space-y-2 mb-3">
            <span class="text-[10px] text-zinc-500 uppercase tracking-wider">Vehículo Recomendado:</span>
            <div class="text-base font-black text-purple-400">
              {{ loadLogistics.recommendedVehicle }}
            </div>
            <p class="text-zinc-400 text-[11px] leading-relaxed">
              Carga total estimada en {{ Math.round(loadLogistics.grandTotalWeightKg) }} kg (incluyendo cableado, atriles y ferretería de montaje).
            </p>
          </div>

          <!-- Alerta Ley del Saco -->
          <div
            v-if="loadLogistics.heavyItemsRequiringTwoPeople.length > 0"
            class="p-3.5 rounded-xl bg-amber-950/40 border border-amber-700/60 text-amber-200 space-y-1.5"
          >
            <div class="flex items-center gap-1.5 font-bold text-xs">
              <span>⚠️</span>
              <span>Ley N° 20.949 (Ley del Saco - Máx 25 kg):</span>
            </div>
            <p class="text-[11px] leading-snug text-amber-300">
              Se detectaron <strong>{{ loadLogistics.heavyItemsRequiringTwoPeople.length }} bultos pesados</strong> que superan los 25 kg. Se exige manipulación obligatoria entre 2 personas.
            </p>
          </div>
          <div v-else class="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-700/60 text-emerald-200 text-[11px]">
            ✓ Todos los bultos cumplen el límite ergonómico de 25 kg para manipulación individual.
          </div>
        </div>

        <div class="pt-3 border-t border-zinc-800/80 text-[10px] text-zinc-500">
          Operadores mínimos recomendados para montaje: <strong class="text-zinc-300">{{ loadLogistics.recommendedOperatorsCount }} técnicos</strong>
        </div>
      </div>

      <!-- Columna Central: Checklist Operativo de Terreno (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#0a0a0f] border border-zinc-800 rounded-2xl p-4 flex flex-col justify-between shadow-xl overflow-y-auto">
        <div>
          <div class="flex items-center gap-2 pb-2 border-b border-zinc-800 mb-3">
            <span class="text-lg">📋</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-xs">
              Checklist de Retiro y Montaje
            </h3>
          </div>

          <div class="space-y-2">
            <div
              v-for="task in loadLogistics.checklist"
              :key="task.id"
              class="p-2.5 rounded-xl bg-[#12121a] border border-zinc-800 flex items-start gap-2.5 text-[11px]"
            >
              <input
                type="checkbox"
                class="mt-0.5 rounded bg-zinc-800 border-zinc-700 text-red-600 focus:ring-0 cursor-pointer"
              />
              <div class="flex-1">
                <span class="font-bold text-zinc-200 block">{{ task.label }}</span>
                <span class="text-[9px] text-zinc-500 uppercase">{{ task.stage }}</span>
              </div>
              <span v-if="task.critical" class="text-[9px] text-red-400 font-bold bg-red-950 px-1.5 py-0.5 rounded">
                CRÍTICO
              </span>
            </div>
          </div>
        </div>

        <div class="pt-2 text-[10px] text-zinc-500">
          Revisar antes de salir de bodega y al desmontar a las 5:00 AM.
        </div>
      </div>

      <!-- Columna Derecha: Acciones de Exportación & Firma (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#0f0f14] border border-zinc-800 rounded-2xl p-4 flex flex-col justify-between shadow-xl">
        <div class="space-y-4">
          <div class="flex items-center gap-2 pb-2 border-b border-zinc-800">
            <span class="text-lg">📄</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-xs">
              Memoria Técnica & Entrega
            </h3>
          </div>

          <div class="p-3.5 bg-[#14141c] border border-zinc-800 rounded-xl space-y-2 text-[11px]">
            <span class="text-zinc-500 text-[10px] uppercase block">Responsable Técnico Firmante:</span>
            <div class="font-bold text-white">{{ operatorSignature }}</div>
            <div class="text-zinc-400 text-[10px]">
              Documento con trazabilidad normativa SEC, atenuación ISO 9613 y protocolo de puesta a tierra.
            </div>
          </div>

          <!-- Botón WhatsApp -->
          <button
            @click="copyWhatsAppSummary"
            class="w-full py-3 px-4 rounded-xl bg-[#1e293b] hover:bg-[#334155] border border-zinc-700 text-white font-bold transition flex items-center justify-center gap-2 cursor-pointer shadow-lg"
          >
            <span>📱</span>
            <span>{{ whatsappCopied ? '✓ ¡Copiado al Portapapeles!' : 'Copiar Resumen para WhatsApp' }}</span>
          </button>
        </div>

        <!-- Botón Principal Descargar PDF -->
        <button
          @click="downloadPdf"
          :disabled="!isValidated"
          class="w-full py-4 px-4 rounded-xl bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 disabled:opacity-50 text-white font-black uppercase tracking-wider transition flex items-center justify-center gap-2 cursor-pointer shadow-xl shadow-red-950/80 text-sm"
        >
          <span>📄</span>
          <span>Descargar Memoria Técnica en PDF →</span>
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
