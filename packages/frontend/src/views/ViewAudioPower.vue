<template>
  <div class="h-full w-full p-2.5 sm:p-3 lg:p-4 grid grid-cols-1 lg:grid-cols-12 gap-3 lg:gap-4 overflow-hidden font-sans">
    <!-- PANEL IZQUIERDO: RACK MODULAR DE AUDIO (Cajas Tops & Sub-Bajos) -->
    <div class="lg:col-span-7 h-full flex flex-col space-y-2.5 overflow-y-auto pr-0.5">
      <!-- Sección Tops (Rack 19" Azul Audio) -->
      <div class="cockpit-card p-3 shadow-xl space-y-2 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
        <div class="flex items-center justify-between border-b border-zinc-800/80 pb-1.5">
          <div class="flex items-center gap-1.5">
            <span class="text-xs">🔊</span>
            <h3 class="text-[11px] font-black tracking-wider text-white uppercase font-mono">
              Cajas Acústicas Medios/Agudos (Tops)
            </h3>
          </div>
          <button
            type="button"
            @click="addTopBatch"
            class="px-2 py-0.5 rounded bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/40 text-blue-300 font-mono text-[10px] font-bold transition flex items-center gap-1 cursor-pointer"
          >
            <span>+</span> Agregar Lote
          </button>
        </div>

        <!-- Lista de Lotes de Tops -->
        <div class="space-y-1.5">
          <div
            v-for="(batch, idx) in topBatches"
            :key="batch.id"
            class="bg-[#10131d] border border-zinc-800/90 rounded-lg p-2 grid grid-cols-12 gap-2 items-center font-mono text-xs"
          >
            <!-- Cantidad & Tipo Activa/Pasiva -->
            <div class="col-span-12 sm:col-span-4 flex items-center gap-1.5">
              <div class="flex items-center border border-zinc-700/80 rounded-md overflow-hidden bg-zinc-900 h-7">
                <button
                  type="button"
                  @click="batch.quantity = Math.max(1, (batch.quantity || 1) - 1); onBatchRmsChange(batch)"
                  class="px-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold h-full text-xs"
                >
                  -
                </button>
                <span class="px-2 font-bold text-white min-w-[24px] text-center text-xs">
                  {{ batch.quantity }}
                </span>
                <button
                  type="button"
                  @click="batch.quantity = (batch.quantity || 1) + 1; onBatchRmsChange(batch)"
                  class="px-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold h-full text-xs"
                >
                  +
                </button>
              </div>
              <select
                v-model="batch.systemType"
                @change="resetValidation"
                class="bg-zinc-900 border border-zinc-700/80 rounded-md px-1.5 h-7 text-white font-bold text-[10px] cursor-pointer"
              >
                <option value="ACTIVE">⚡ Activa</option>
                <option value="PASSIVE">🔌 Pasiva</option>
              </select>
            </div>

            <!-- Modelo / Cono -->
            <div class="col-span-6 sm:col-span-4">
              <input
                v-model="batch.modelLabel"
                type="text"
                placeholder="Modelo / Cono"
                class="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-md px-2 h-7 text-white placeholder:text-zinc-600 text-xs focus:outline-none focus:border-blue-500"
              />
            </div>

            <!-- Watts RMS y Peak -->
            <div class="col-span-5 sm:col-span-3 flex items-center gap-1.5">
              <div class="flex-1">
                <span class="text-[8px] text-zinc-500 uppercase block font-bold">RMS (W)</span>
                <input
                  v-model.number="batch.rmsWatts"
                  @input="onBatchRmsChange(batch)"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-md px-1.5 h-6 text-white font-bold text-[11px] focus:outline-none focus:border-blue-500"
                />
              </div>
              <div class="flex-1">
                <span class="text-[8px] text-zinc-500 uppercase block font-bold">Peak (W)</span>
                <input
                  v-model.number="batch.peakWatts"
                  @input="resetValidation"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-md px-1.5 h-6 text-amber-400 font-bold text-[11px] focus:outline-none focus:border-amber-500"
                />
              </div>
            </div>

            <!-- Eliminar Lote -->
            <div class="col-span-1 text-right">
              <button
                v-if="topBatches.length > 1"
                type="button"
                @click="removeTopBatch(idx)"
                class="text-zinc-500 hover:text-red-400 font-bold px-1 text-xs cursor-pointer"
                title="Eliminar lote"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <!-- Telemetría Tops -->
        <div class="flex items-center justify-between text-[10px] font-mono text-zinc-400 pt-1 border-t border-zinc-800/60">
          <span>Total Tops: <strong class="text-white">{{ totalTopsCount }}</strong> cajas</span>
          <span>Potencia: <strong class="text-blue-400">{{ totalTopsRmsWatts }}W RMS</strong> / {{ totalTopsPeakWatts }}W Peak</span>
        </div>
      </div>

      <!-- Sección Subwoofers (Rack 19" Ámbar Graves) -->
      <div class="cockpit-card p-3 shadow-xl space-y-2 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-amber-500"></div>
        <div class="flex items-center justify-between border-b border-zinc-800/80 pb-1.5">
          <div class="flex items-center gap-1.5">
            <span class="text-xs">🎛️</span>
            <h3 class="text-[11px] font-black tracking-wider text-white uppercase font-mono">
              Subwoofers / Graves (Subs)
            </h3>
          </div>
          <button
            type="button"
            @click="addSubBatch"
            class="px-2 py-0.5 rounded bg-amber-600/20 hover:bg-amber-600/30 border border-amber-500/40 text-amber-300 font-mono text-[10px] font-bold transition flex items-center gap-1 cursor-pointer"
          >
            <span>+</span> Agregar Lote
          </button>
        </div>

        <!-- Lista de Lotes de Subs -->
        <div class="space-y-1.5">
          <div
            v-for="(batch, idx) in subBatches"
            :key="batch.id"
            class="bg-[#10131d] border border-zinc-800/90 rounded-lg p-2 grid grid-cols-12 gap-2 items-center font-mono text-xs"
          >
            <!-- Cantidad & Tipo -->
            <div class="col-span-12 sm:col-span-4 flex items-center gap-1.5">
              <div class="flex items-center border border-zinc-700/80 rounded-md overflow-hidden bg-zinc-900 h-7">
                <button
                  type="button"
                  @click="batch.quantity = Math.max(1, (batch.quantity || 1) - 1); onBatchRmsChange(batch)"
                  class="px-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold h-full text-xs"
                >
                  -
                </button>
                <span class="px-2 font-bold text-white min-w-[24px] text-center text-xs">
                  {{ batch.quantity }}
                </span>
                <button
                  type="button"
                  @click="batch.quantity = (batch.quantity || 1) + 1; onBatchRmsChange(batch)"
                  class="px-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold h-full text-xs"
                >
                  +
                </button>
              </div>
              <select
                v-model="batch.systemType"
                @change="resetValidation"
                class="bg-zinc-900 border border-zinc-700/80 rounded-md px-1.5 h-7 text-white font-bold text-[10px] cursor-pointer"
              >
                <option value="ACTIVE">⚡ Activo</option>
                <option value="PASSIVE">🔌 Pasivo</option>
              </select>
            </div>

            <!-- Modelo / Cono -->
            <div class="col-span-6 sm:col-span-4">
              <input
                v-model="batch.modelLabel"
                type="text"
                placeholder="Subwoofer / Cono"
                class="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-md px-2 h-7 text-white placeholder:text-zinc-600 text-xs focus:outline-none focus:border-amber-500"
              />
            </div>

            <!-- Watts RMS y Peak -->
            <div class="col-span-5 sm:col-span-3 flex items-center gap-1.5">
              <div class="flex-1">
                <span class="text-[8px] text-zinc-500 uppercase block font-bold">RMS (W)</span>
                <input
                  v-model.number="batch.rmsWatts"
                  @input="onBatchRmsChange(batch)"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-md px-1.5 h-6 text-white font-bold text-[11px] focus:outline-none focus:border-amber-500"
                />
              </div>
              <div class="flex-1">
                <span class="text-[8px] text-zinc-500 uppercase block font-bold">Peak (W)</span>
                <input
                  v-model.number="batch.peakWatts"
                  @input="resetValidation"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-md px-1.5 h-6 text-amber-400 font-bold text-[11px] focus:outline-none focus:border-amber-500"
                />
              </div>
            </div>

            <!-- Eliminar Lote -->
            <div class="col-span-1 text-right">
              <button
                v-if="subBatches.length > 1"
                type="button"
                @click="removeSubBatch(idx)"
                class="text-zinc-500 hover:text-red-400 font-bold px-1 text-xs cursor-pointer"
                title="Eliminar lote"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <!-- Telemetría Subs -->
        <div class="flex items-center justify-between text-[10px] font-mono text-zinc-400 pt-1 border-t border-zinc-800/60">
          <span>Total Subs: <strong class="text-white">{{ totalSubsCount }}</strong> bajos</span>
          <span>Potencia: <strong class="text-amber-400">{{ totalSubsRmsWatts }}W RMS</strong> / {{ totalSubsPeakWatts }}W Peak</span>
        </div>
      </div>
    </div>

    <!-- PANEL DERECHO: ENERGÍA, FUENTE Y TACÓMETRO DE CARGA (HUD) -->
    <div class="lg:col-span-5 h-full bg-[#08090e] border border-zinc-800/90 rounded-xl p-3.5 flex flex-col justify-between shadow-2xl relative overflow-hidden font-mono text-xs">
      <div>
        <div class="flex items-center justify-between pb-2 border-b border-zinc-800/80 mb-3">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <h3 class="font-bold text-white uppercase tracking-wider text-[11px]">
              Alimentación & Protección SEC
            </h3>
          </div>
          <span class="text-zinc-500 text-[9px] uppercase">Cálculo RIC 03 / RIC 10</span>
        </div>

        <!-- Tipo de Fuente -->
        <div class="space-y-2.5 mb-3">
          <div>
            <label class="cockpit-label">Tipo de Suministro Eléctrico</label>
            <select
              v-model="powerSource.type"
              @change="resetValidation"
              class="w-full cockpit-input cursor-pointer font-bold"
            >
              <option value="GRID_220V">🔌 Red Eléctrica 220V Fija (Enchufe Domiciliario / Comercial)</option>
              <option value="GENERATOR_WATTS">⚡ Generador a Gasolina (Potencia en Watts)</option>
              <option value="GENERATOR_KVA">🏭 Generador Diésel / Industrial (Potencia en kVA)</option>
            </select>
          </div>

          <!-- Parámetros de la Fuente (Grid) -->
          <div v-if="powerSource.type === 'GRID_220V'" class="grid grid-cols-2 gap-2.5">
            <div>
              <label class="cockpit-label">Disyuntor (Breaker)</label>
              <select
                v-model="powerSource.circuitBreakerAmps"
                @change="resetValidation"
                class="w-full cockpit-input font-bold cursor-pointer"
              >
                <option value="10">10A (Casa Estándar)</option>
                <option value="16">16A (Embutido Reforzado)</option>
                <option value="20">20A (Comercial)</option>
                <option value="25">25A (Industrial Ligero)</option>
                <option value="32">32A (Empalme CEE)</option>
              </select>
            </div>
            <div>
              <label class="cockpit-label">Régimen Volumen</label>
              <select
                v-model="powerSource.driveRegime"
                @change="resetValidation"
                class="w-full cockpit-input font-bold cursor-pointer"
              >
                <option value="MAX_TECHNO_1_3">🔥 Techno / Drop Máximo</option>
                <option value="STANDARD_CLUB_1_5">🎵 Club Estándar</option>
                <option value="MODERATE_1_8">🍸 Moderado / Cóctel</option>
              </select>
            </div>
          </div>

          <!-- Parámetros Generador Watts -->
          <div v-else-if="powerSource.type === 'GENERATOR_WATTS'" class="grid grid-cols-2 gap-2.5">
            <div>
              <label class="cockpit-label">Capacidad Surge (W)</label>
              <input
                v-model.number="powerSource.generatorSurgeWatts"
                @input="resetValidation"
                type="number"
                placeholder="3500"
                class="w-full cockpit-input font-bold text-amber-300"
              />
            </div>
            <div>
              <label class="cockpit-label">Régimen Volumen</label>
              <select
                v-model="powerSource.driveRegime"
                @change="resetValidation"
                class="w-full cockpit-input font-bold cursor-pointer"
              >
                <option value="MAX_TECHNO_1_3">🔥 Techno / Drop Máximo</option>
                <option value="STANDARD_CLUB_1_5">🎵 Club Estándar</option>
              </select>
            </div>
          </div>

          <!-- Parámetros Generador kVA -->
          <div v-else class="grid grid-cols-2 gap-2.5">
            <div>
              <label class="cockpit-label">Potencia Aparente (kVA)</label>
              <input
                v-model.number="powerSource.apparentPowerKva"
                @input="resetValidation"
                type="number"
                placeholder="15"
                class="w-full cockpit-input font-bold text-amber-300"
              />
            </div>
            <div>
              <label class="cockpit-label">Factor Potencia (FP)</label>
              <input
                v-model.number="powerSource.powerFactor"
                @input="resetValidation"
                type="number"
                step="0.05"
                placeholder="0.8"
                class="w-full cockpit-input font-bold"
              />
            </div>
          </div>
        </div>

        <!-- Tacómetro de Carga y Barra de Estado (HUD Iluminado) -->
        <div class="bg-[#10131d] border border-zinc-800/80 rounded-lg p-3 space-y-2.5">
          <div class="flex items-center justify-between text-xs">
            <span class="text-zinc-400 font-bold uppercase text-[10px]">Carga Eléctrica Estimada:</span>
            <span
              class="px-2 py-0.5 rounded font-black text-[9px] uppercase tracking-wider"
              :class="powerAlertLevel === 'CRITICAL' ? 'bg-red-950 text-red-300 border border-red-700' : 'bg-emerald-950 text-emerald-300 border border-emerald-700'"
            >
              {{ powerFeasibility.status }}
            </span>
          </div>

          <!-- Barra de Carga Porcentual con Gradiente LED -->
          <div>
            <div class="w-full h-2.5 bg-zinc-900 rounded-full overflow-hidden flex border border-zinc-800">
              <div
                class="h-full transition-all duration-300"
                :class="loadPercentage > 100 ? 'bg-red-500' : loadPercentage > 80 ? 'bg-amber-400' : 'bg-emerald-500'"
                :style="{ width: `${Math.min(100, loadPercentage)}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-[9px] text-zinc-500 mt-1 font-mono">
              <span>0%</span>
              <span class="text-zinc-300 font-bold">Demanda: {{ loadPercentage }}% de capacidad</span>
              <span>100%</span>
            </div>
          </div>

          <!-- Métricas de Demanda y Picos -->
          <div class="grid grid-cols-2 gap-2 pt-1 border-t border-zinc-800/80 text-[10px]">
            <div>
              <span class="text-zinc-500 block text-[8px] uppercase">Demanda Continua:</span>
              <strong class="text-white text-xs">{{ powerFeasibility.totalSystemDemandWatts }} W</strong>
            </div>
            <div>
              <span class="text-zinc-500 block text-[8px] uppercase">Picos Transitorios:</span>
              <strong class="text-amber-400 text-xs">{{ powerFeasibility.transientPeakWatts }} W</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumen Diagnóstico SEC -->
      <div class="p-2.5 rounded-lg bg-[#10131d] border border-zinc-800/80 space-y-1 text-[10px] mt-2">
        <div class="flex items-center gap-1.5 text-zinc-300 font-bold">
          <span>⚡</span>
          <span>Diagnóstico Eléctrico SEC:</span>
        </div>
        <p class="text-zinc-400 leading-snug">
          {{ powerFeasibility.technicalDiagnosis || 'Cargando análisis eléctrico...' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useStagePlanState } from '../composables/useStagePlanState';

const {
  topBatches,
  subBatches,
  totalTopsCount,
  totalTopsRmsWatts,
  totalTopsPeakWatts,
  totalSubsCount,
  totalSubsRmsWatts,
  totalSubsPeakWatts,
  addTopBatch,
  removeTopBatch,
  addSubBatch,
  removeSubBatch,
  onBatchRmsChange,
  powerSource,
  powerFeasibility,
  powerAlertLevel,
  resetValidation,
} = useStagePlanState();

const loadPercentage = computed(() => {
  const demand = powerFeasibility.value.totalSystemDemandWatts || 0;
  let capacity = 3520; // 16A * 220V
  if (powerSource.type === 'GRID_220V') {
    capacity = Number(powerSource.circuitBreakerAmps || 16) * 220;
  } else if (powerSource.type === 'GENERATOR_WATTS') {
    capacity = powerSource.generatorSurgeWatts || 3500;
  } else {
    capacity = Math.round((powerSource.apparentPowerKva || 5) * 1000 * (powerSource.powerFactor || 0.8));
  }
  return Math.round((demand / Math.max(1, capacity)) * 100);
});
</script>
