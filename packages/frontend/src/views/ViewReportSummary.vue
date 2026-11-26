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

      <!-- KPI 3: Inversión / Arriendo / Logística -->
      <div class="cockpit-card p-2.5 sm:p-3 shadow-lg relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-purple-500"></div>
        <span class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider block">
          {{ rentalConfig.isRentalMode ? 'Inversión Arriendo Diario' : 'Carga & Despacho Flota' }}
        </span>
        <div class="flex items-baseline gap-1 mt-0.5">
          <span v-if="rentalConfig.isRentalMode" class="text-base lg:text-lg font-black font-mono text-purple-300 truncate">
            {{ rentalCostSummary.formattedTotalClp }}
          </span>
          <template v-else>
            <span class="text-lg lg:text-xl font-black font-mono text-white">{{ Math.round(loadLogistics.grandTotalWeightKg || 0) }}</span>
            <span class="text-[10px] text-purple-400 font-bold font-mono">kg</span>
          </template>
        </div>
        <span class="text-[9px] text-zinc-400 font-mono block mt-0.5 truncate">
          {{ rentalConfig.isRentalMode ? 'Rider externo cotizado' : `Vehículo: ${loadLogistics.recommendedVehicle}` }}
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

    <!-- ÁREA CENTRAL DIVIDIDA EN 3 COLUMNAS: LOGÍSTICA/ARRIENDO, PLANO 2D CAD Y MEMORIA TÉCNICA -->
    <div class="flex-1 w-full min-h-0 grid grid-cols-1 lg:grid-cols-12 gap-2.5 sm:gap-3 overflow-hidden mb-1">
      
      <!-- Columna 1: Logística de Flota & Cotizador de Arriendo (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#08090e] border border-zinc-800/90 rounded-xl p-3 flex flex-col justify-between shadow-xl overflow-y-auto space-y-2.5">
        <div>
          <!-- Módulo de Arriendo vs Equipos Propios -->
          <div class="p-2.5 rounded-lg bg-[#10131d] border border-zinc-800/80 mb-2.5">
            <div class="flex items-center justify-between pb-1.5 border-b border-zinc-800 mb-2">
              <span class="text-[10px] font-mono font-bold text-white uppercase flex items-center gap-1">
                <span>💰</span> Modalidad de Producción
              </span>
              <div class="flex items-center gap-1 bg-black/50 p-0.5 rounded border border-zinc-800 text-[9px] font-mono">
                <button
                  type="button"
                  @click="rentalConfig.isRentalMode = false"
                  :class="!rentalConfig.isRentalMode ? 'bg-zinc-700 text-white font-bold' : 'text-zinc-400 hover:text-white'"
                  class="px-1.5 py-0.5 rounded transition cursor-pointer"
                >
                  Propios
                </button>
                <button
                  type="button"
                  @click="rentalConfig.isRentalMode = true"
                  :class="rentalConfig.isRentalMode ? 'bg-purple-600 text-white font-bold' : 'text-zinc-400 hover:text-white'"
                  class="px-1.5 py-0.5 rounded transition cursor-pointer"
                >
                  Arriendo
                </button>
              </div>
            </div>

            <!-- Desglose de Inversión Arriendo -->
            <div v-if="rentalConfig.isRentalMode" class="space-y-1 font-mono text-[9px]">
              <div class="flex justify-between text-zinc-300">
                <span>Tops ({{ totalTopsCount }}x):</span>
                <span class="font-bold text-white">${{ rentalCostSummary.topsCost.toLocaleString('es-CL') }}</span>
              </div>
              <div class="flex justify-between text-zinc-300">
                <span>Subs ({{ totalSubsCount }}x):</span>
                <span class="font-bold text-white">${{ rentalCostSummary.subsCost.toLocaleString('es-CL') }}</span>
              </div>
              <div class="flex justify-between text-zinc-300">
                <span>Potencias/Racks:</span>
                <span class="font-bold text-white">${{ rentalCostSummary.ampsCost.toLocaleString('es-CL') }}</span>
              </div>
              <div v-if="powerSource.type !== 'GRID_220V'" class="flex justify-between text-zinc-300">
                <span>Generador:</span>
                <span class="font-bold text-white">${{ rentalCostSummary.generatorCost.toLocaleString('es-CL') }}</span>
              </div>
              <div class="flex justify-between text-zinc-300">
                <span>Luminarias ({{ lightingDmxAnalysis?.totalFixtureUnits || 0 }}x):</span>
                <span class="font-bold text-white">${{ rentalCostSummary.lightingCost.toLocaleString('es-CL') }}</span>
              </div>
              <div class="flex justify-between items-center text-zinc-300 pt-1 border-t border-zinc-800">
                <span>Personal ({{ rentalConfig.techniciansCount }} téc.):</span>
                <div class="flex items-center gap-1">
                  <button
                    type="button"
                    @click="rentalConfig.techniciansCount = Math.max(1, rentalConfig.techniciansCount - 1)"
                    class="px-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded text-[9px]"
                  >-</button>
                  <span class="font-bold text-white">${{ rentalCostSummary.laborCost.toLocaleString('es-CL') }}</span>
                  <button
                    type="button"
                    @click="rentalConfig.techniciansCount++"
                    class="px-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded text-[9px]"
                  >+</button>
                </div>
              </div>
              <div class="flex justify-between text-[11px] font-bold text-purple-400 pt-1 border-t border-zinc-700">
                <span>Total Estimado:</span>
                <span>{{ rentalCostSummary.formattedTotalClp }}</span>
              </div>
            </div>
            <div v-else class="text-[9px] text-zinc-500 font-mono">
              Equipos de inventario propio. Sin costos diarios de arriendo externo cargados al presupuesto.
            </div>
          </div>

          <!-- Tarjeta del Vehículo & Ley del Saco -->
          <div class="p-2.5 rounded-lg bg-[#10131d] border border-zinc-800/80 space-y-1 mb-2">
            <span class="text-[8px] text-zinc-500 uppercase tracking-wider font-bold">Vehículo Recomendado:</span>
            <div class="text-xs font-black text-purple-400 font-mono">
              {{ loadLogistics.recommendedVehicle }}
            </div>
            <p class="text-zinc-400 text-[9px] leading-relaxed">
              Carga total: ~{{ Math.round(loadLogistics.grandTotalWeightKg) }} kg (audio, cables, atriles).
            </p>
          </div>

          <!-- Alerta Ley del Saco -->
          <div
            v-if="loadLogistics.heavyItemsRequiringTwoPeople.length > 0"
            class="p-2 rounded-lg bg-amber-950/40 border border-amber-700/60 text-amber-200 text-[9px]"
          >
            <div class="flex items-center gap-1 font-bold">
              <span>⚠️</span>
              <span>Ley N° 20.949 (Ley del Saco):</span>
            </div>
            <p class="text-amber-300 text-[8.5px] mt-0.5">
              {{ loadLogistics.heavyItemsRequiringTwoPeople.length }} bultos > 25 kg. Manipulación entre 2 personas.
            </p>
          </div>
          <div v-else class="p-2 rounded-lg bg-emerald-950/40 border border-emerald-700/60 text-emerald-200 text-[9px]">
            ✓ Bultos &lt; 25 kg ergonómicamente aptos para 1 persona.
          </div>
        </div>

        <!-- Indicador Rack Pasivo si aplica -->
        <div v-if="powerAmpSizing.hasPassiveUnits" class="p-2 rounded bg-indigo-950/40 border border-indigo-700/60 text-indigo-300 text-[9px] font-mono">
          <div class="font-bold flex items-center gap-1">
            <span>🎛️</span>
            <span>Rack Potencias: {{ powerAmpSizing.totalAmplifiersCount }}x Amp (+{{ powerAmpSizing.totalAdditionalAcPowerWatts }}W AC)</span>
          </div>
        </div>
      </div>

      <!-- Columna 2: Previsualización del Plano 2D CAD & Exportación PNG (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#08090e] border border-zinc-800/90 rounded-xl p-2.5 flex flex-col justify-between shadow-xl overflow-hidden">
        <div class="flex flex-col h-full justify-between">
          <div>
            <div class="flex items-center justify-between pb-1.5 border-b border-zinc-800 mb-1.5">
              <div class="flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                <h3 class="font-bold text-white uppercase tracking-wider text-[11px] font-mono">
                  Plano CAD 2D (Blueprint)
                </h3>
              </div>
              <button
                type="button"
                @click="goToStep(3)"
                class="text-[9px] font-mono text-blue-400 hover:text-blue-300 underline cursor-pointer"
              >
                Abrir Visor →
              </button>
            </div>

            <!-- Contenedor Miniatura del Plano SVG CAD -->
            <div class="w-full bg-[#050608] rounded-lg border border-zinc-800/90 overflow-hidden shadow-inner max-h-[260px] flex items-center justify-center p-1">
              <LayoutSvg2D
                :venue-width="venue.widthMeters || 10"
                :venue-depth="venue.depthMeters || 16"
                :subs-count="totalSubsCount"
                :tops-count="totalTopsCount"
                :roster-nodes="hybridAnalysis.roster"
                :power-plan="powerDistributionPlan"
                :lighting-analysis="lightingDmxAnalysis"
                class="scale-95 origin-center w-full"
              />
            </div>
          </div>

          <!-- Botón de Descarga PNG del Plano -->
          <div class="pt-2 border-t border-zinc-800/80">
            <button
              type="button"
              @click="downloadCadPng"
              class="w-full py-1.5 px-2 rounded-lg bg-blue-950/60 hover:bg-blue-900/70 border border-blue-600/60 text-blue-200 font-mono font-bold text-[10px] transition flex items-center justify-center gap-1.5 cursor-pointer shadow-md"
              title="Descargar plano en formato imagen PNG de alta resolución"
            >
              <span>🖼️</span>
              <span>Descargar Plano CAD (PNG 300 DPI)</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Columna 3: Checklist Operativo & Memoria Técnica PDF (4 cols) -->
      <div class="lg:col-span-4 h-full bg-[#0c0e15] border border-zinc-800/90 rounded-xl p-3 flex flex-col justify-between shadow-xl overflow-y-auto">
        <div class="space-y-2.5">
          <div class="flex items-center gap-1.5 pb-1.5 border-b border-zinc-800">
            <span class="text-base">📋</span>
            <h3 class="font-bold text-white uppercase tracking-wider text-[11px] font-mono">
              Checklist & Despacho Oficial
            </h3>
          </div>

          <!-- Mini Lista de Checklist -->
          <div class="space-y-1">
            <div
              v-for="task in loadLogistics.checklist.slice(0, 4)"
              :key="task.id"
              class="p-1.5 rounded bg-[#10131d] border border-zinc-800/80 flex items-start gap-1.5 text-[9px] font-mono"
            >
              <input
                type="checkbox"
                class="mt-0.5 rounded bg-zinc-900 border-zinc-700 text-red-600 focus:ring-0 cursor-pointer"
              />
              <span class="text-zinc-200 truncate flex-1">{{ task.label }}</span>
            </div>
          </div>

          <!-- Firma Operador -->
          <div class="p-2 bg-[#10131d] border border-zinc-800/80 rounded-lg space-y-0.5 text-[9px] font-mono">
            <span class="text-zinc-500 text-[8px] uppercase block font-bold">Responsable Técnico Firmante:</span>
            <div class="font-bold text-zinc-100">{{ operatorSignature }}</div>
            <div class="text-zinc-500 text-[8px]">
              Trazabilidad SEC RIC N° 10, atenuación acústica ISO 9613 y protocolo puesta a tierra.
            </div>
          </div>

          <!-- Botón WhatsApp -->
          <button
            type="button"
            @click="copyWhatsAppSummary"
            class="w-full py-1.5 px-3 rounded-lg bg-[#182030] hover:bg-[#202b40] border border-zinc-700 text-white font-mono font-bold text-[10px] transition flex items-center justify-center gap-1.5 cursor-pointer shadow-md"
          >
            <span>📱</span>
            <span>{{ whatsappCopied ? '✓ ¡Copiado al Portapapeles!' : 'Copiar Resumen WhatsApp' }}</span>
          </button>
        </div>

        <!-- Botón Principal Descargar PDF Dual-Page -->
        <div class="pt-2">
          <button
            type="button"
            @click="downloadPdf()"
            :disabled="!isValidated"
            class="w-full py-2.5 px-3 rounded-lg bg-gradient-to-r from-red-600 to-amber-600 hover:from-red-500 hover:to-amber-500 disabled:opacity-40 text-white font-mono font-black uppercase tracking-wider transition flex items-center justify-center gap-1.5 cursor-pointer shadow-lg shadow-red-950/70 text-[11px]"
          >
            <span>📄</span>
            <span>Descargar Memoria Técnica PDF (Dual-Page) →</span>
          </button>
          <span class="text-[8px] text-zinc-500 text-center block mt-1 font-mono">
            Pág 1: Memoria SEC & Costos · Pág 2: Lámina CAD 2D Horizontal
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import LayoutSvg2D from '../components/LayoutSvg2D.vue';
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
  downloadCadPng,
  isValidated,
  totalSubsCount,
  totalTopsCount,
  hybridAnalysis,
  powerDistributionPlan,
  lightingDmxAnalysis,
  powerAmpSizing,
  rentalConfig,
  rentalCostSummary,
  goToStep,
} = useStagePlanState();
</script>
