<template>
  <div class="h-full w-full p-4 lg:p-6 grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 overflow-hidden">
    <!-- PANEL IZQUIERDO: RACK MODULAR DE AUDIO (Cajas Tops & Sub-Bajos) -->
    <div class="lg:col-span-7 h-full flex flex-col space-y-4 overflow-y-auto pr-1">
      <!-- Sección Tops -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-4 shadow-xl space-y-3 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
        <div class="flex items-center justify-between border-b border-zinc-800/80 pb-2">
          <div class="flex items-center gap-2">
            <span class="text-base">🔊</span>
            <h3 class="text-xs font-black tracking-wider text-white uppercase font-mono">
              Cajas Acústicas Medios/Agudos (Tops)
            </h3>
          </div>
          <button
            @click="addTopBatch"
            class="px-2.5 py-1 rounded-lg bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/40 text-blue-300 font-mono text-xs font-bold transition flex items-center gap-1 cursor-pointer"
          >
            <span>+</span> Agregar Lote
          </button>
        </div>

        <!-- Lista de Lotes de Tops -->
        <div class="space-y-2">
          <div
            v-for="(batch, idx) in topBatches"
            :key="batch.id"
            class="bg-[#14141c] border border-zinc-800 rounded-xl p-3 grid grid-cols-12 gap-2.5 items-center font-mono text-xs"
          >
            <!-- Cantidad & Tipo -->
            <div class="col-span-12 sm:col-span-4 flex items-center gap-2">
              <div class="flex items-center border border-zinc-700 rounded-lg overflow-hidden bg-zinc-900">
                <button
                  @click="batch.quantity = Math.max(1, (batch.quantity || 1) - 1); onBatchRmsChange(batch)"
                  class="px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold"
                >
                  -
                </button>
                <span class="px-2.5 py-1 font-bold text-white min-w-[28px] text-center">
                  {{ batch.quantity }}
                </span>
                <button
                  @click="batch.quantity = (batch.quantity || 1) + 1; onBatchRmsChange(batch)"
                  class="px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold"
                >
                  +
                </button>
              </div>
              <select
                v-model="batch.systemType"
                @change="resetValidation"
                class="bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-white font-bold text-[11px]"
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
                class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-2.5 py-1 text-white placeholder:text-zinc-600 text-xs"
              />
            </div>

            <!-- Watts RMS y Peak -->
            <div class="col-span-5 sm:col-span-3 flex items-center gap-1.5">
              <div class="flex-1">
                <span class="text-[9px] text-zinc-500 block">RMS (W)</span>
                <input
                  v-model.number="batch.rmsWatts"
                  @input="onBatchRmsChange(batch)"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-white font-bold text-xs"
                />
              </div>
              <div class="flex-1">
                <span class="text-[9px] text-zinc-500 block">Peak (W)</span>
                <input
                  v-model.number="batch.peakWatts"
                  @input="resetValidation"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-amber-400 font-bold text-xs"
                />
              </div>
            </div>

            <!-- Eliminar Lote -->
            <div class="col-span-1 text-right">
              <button
                v-if="topBatches.length > 1"
                @click="removeTopBatch(idx)"
                class="text-zinc-600 hover:text-red-400 font-bold px-1"
                title="Eliminar lote"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-[11px] font-mono text-zinc-400 pt-1">
          <span>Total Tops: <strong class="text-white">{{ totalTopsCount }}</strong> cajas</span>
          <span>Potencia: <strong class="text-blue-400">{{ totalTopsRmsWatts }}W RMS</strong> / {{ totalTopsPeakWatts }}W Peak</span>
        </div>
      </div>

      <!-- Sección Subwoofers -->
      <div class="bg-[#0f0f14] border border-zinc-800 rounded-2xl p-4 shadow-xl space-y-3 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-1 h-full bg-amber-500"></div>
        <div class="flex items-center justify-between border-b border-zinc-800/80 pb-2">
          <div class="flex items-center gap-2">
            <span class="text-base">🎛️</span>
            <h3 class="text-xs font-black tracking-wider text-white uppercase font-mono">
              Subwoofers / Graves (Subs)
            </h3>
          </div>
          <button
            @click="addSubBatch"
            class="px-2.5 py-1 rounded-lg bg-amber-600/20 hover:bg-amber-600/30 border border-amber-500/40 text-amber-300 font-mono text-xs font-bold transition flex items-center gap-1 cursor-pointer"
          >
            <span>+</span> Agregar Lote
          </button>
        </div>

        <!-- Lista de Lotes de Subs -->
        <div class="space-y-2">
          <div
            v-for="(batch, idx) in subBatches"
            :key="batch.id"
            class="bg-[#14141c] border border-zinc-800 rounded-xl p-3 grid grid-cols-12 gap-2.5 items-center font-mono text-xs"
          >
            <!-- Cantidad & Tipo -->
            <div class="col-span-12 sm:col-span-4 flex items-center gap-2">
              <div class="flex items-center border border-zinc-700 rounded-lg overflow-hidden bg-zinc-900">
                <button
                  @click="batch.quantity = Math.max(1, (batch.quantity || 1) - 1); onBatchRmsChange(batch)"
                  class="px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold"
                >
                  -
                </button>
                <span class="px-2.5 py-1 font-bold text-white min-w-[28px] text-center">
                  {{ batch.quantity }}
                </span>
                <button
                  @click="batch.quantity = (batch.quantity || 1) + 1; onBatchRmsChange(batch)"
                  class="px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 font-bold"
                >
                  +
                </button>
              </div>
              <select
                v-model="batch.systemType"
                @change="resetValidation"
                class="bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-white font-bold text-[11px]"
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
                class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-2.5 py-1 text-white placeholder:text-zinc-600 text-xs"
              />
            </div>

            <!-- Watts RMS y Peak -->
            <div class="col-span-5 sm:col-span-3 flex items-center gap-1.5">
              <div class="flex-1">
                <span class="text-[9px] text-zinc-500 block">RMS (W)</span>
                <input
                  v-model.number="batch.rmsWatts"
                  @input="onBatchRmsChange(batch)"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-white font-bold text-xs"
                />
              </div>
              <div class="flex-1">
                <span class="text-[9px] text-zinc-500 block">Peak (W)</span>
                <input
                  v-model.number="batch.peakWatts"
                  @input="resetValidation"
                  type="number"
                  step="50"
                  class="w-full bg-zinc-900 border border-zinc-700 rounded-lg px-2 py-1 text-amber-400 font-bold text-xs"
                />
              </div>
            </div>

            <!-- Eliminar Lote -->
            <div class="col-span-1 text-right">
              <button
                v-if="subBatches.length > 1"
                @click="removeSubBatch(idx)"
                class="text-zinc-600 hover:text-red-400 font-bold px-1"
                title="Eliminar lote"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between text-[11px] font-mono text-zinc-400 pt-1">
          <span>Total Subs: <strong class="text-white">{{ totalSubsCount }}</strong> bajos</span>
          <span>Potencia: <strong class="text-amber-400">{{ totalSubsRmsWatts }}W RMS</strong> / {{ totalSubsPeakWatts }}W Peak</span>
        </div>
      </div>
    </div>

    <!-- PANEL DERECHO: ENERGÍA, FUENTE Y TACÓMETRO DE CARGA (HUD) -->
    <div class="lg:col-span-5 h-full bg-[#0a0a0f] border border-zinc-800 rounded-2xl p-5 flex flex-col justify-between shadow-2xl relative overflow-hidden font-mono text-xs">
      <div>
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800/80 mb-4">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <h3 class="font-bold text-white uppercase tracking-wider text-xs">
              Alimentación & Protección SEC
            </h3>
          </div>
          <span class="text-zinc-500 text-[10px]">Cálculo RIC 03 / RIC 10</span>
        </div>

        <!-- Tipo de Fuente -->
        <div class="space-y-3 mb-5">
          <div>
            <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Tipo de Suministro</label>
            <select
              v-model="powerSource.type"
              @change="resetValidation"
              class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold transition"
            >
              <option value="GRID_220V">🔌 Red Eléctrica 220V Fija (Enchufe Domiciliario / Comercial)</option>
              <option value="GENERATOR_WATTS">⚡ Generador a Gasolina (Potencia en Watts)</option>
              <option value="GENERATOR_KVA">🏭 Generador Diésel / Industrial (Potencia en kVA)</option>
            </select>
          </div>

          <!-- Parámetros de la Fuente -->
          <div v-if="powerSource.type === 'GRID_220V'" class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Termomagnético (Breaker)</label>
              <select
                v-model="powerSource.circuitBreakerAmps"
                @change="resetValidation"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold"
              >
                <option value="10">10 Amperios (Enchufe Casa Típico)</option>
                <option value="16">16 Amperios (Enchufe Embutido)</option>
                <option value="20">20 Amperios (Comercial)</option>
                <option value="25">25 Amperios (Industrial Ligero)</option>
                <option value="32">32 Amperios (Empalme Trifásico / CEE)</option>
              </select>
            </div>
            <div>
              <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Régimen Volumen</label>
              <select
                v-model="powerSource.driveRegime"
                @change="resetValidation"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold"
              >
                <option value="MAX_TECHNO_1_3">🔥 Techno / Drop Máximo</option>
                <option value="STANDARD_CLUB_1_5">🎵 Club Estándar</option>
                <option value="MODERATE_1_8">🍸 Moderado / Cóctel</option>
              </select>
            </div>
          </div>

          <div v-else-if="powerSource.type === 'GENERATOR_WATTS'" class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Capacidad Generador (W)</label>
              <input
                v-model.number="powerSource.generatorSurgeWatts"
                @input="resetValidation"
                type="number"
                placeholder="Ej: 3500"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold"
              />
            </div>
            <div>
              <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Régimen Volumen</label>
              <select
                v-model="powerSource.driveRegime"
                @change="resetValidation"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold"
              >
                <option value="MAX_TECHNO_1_3">🔥 Techno / Drop Máximo</option>
                <option value="STANDARD_CLUB_1_5">🎵 Club Estándar</option>
              </select>
            </div>
          </div>

          <div v-else class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Potencia Aparente (kVA)</label>
              <input
                v-model.number="powerSource.apparentPowerKva"
                @input="resetValidation"
                type="number"
                placeholder="Ej: 15"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold"
              />
            </div>
            <div>
              <label class="block text-zinc-400 uppercase text-[10px] mb-1 font-bold">Factor Potencia (FP)</label>
              <input
                v-model.number="powerSource.powerFactor"
                @input="resetValidation"
                type="number"
                step="0.05"
                placeholder="0.8"
                class="w-full bg-[#18181f] border border-zinc-700 rounded-xl px-3 py-2 text-white font-bold"
              />
            </div>
          </div>
        </div>

        <!-- Tacómetro de Carga y Barra de Estado (HUD) -->
        <div class="bg-[#12121a] border border-zinc-800 rounded-xl p-4 space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="text-zinc-400 font-bold uppercase">Carga Eléctrica Estimada:</span>
            <span
              class="px-2 py-0.5 rounded font-black text-[10px]"
              :class="powerAlertLevel === 'CRITICAL' ? 'bg-red-950 text-red-300 border border-red-700' : 'bg-emerald-950 text-emerald-300 border border-emerald-700'"
            >
              {{ powerFeasibility.status }}
            </span>
          </div>

          <!-- Barra de Carga Porcentual -->
          <div>
            <div class="w-full h-3 bg-zinc-800 rounded-full overflow-hidden flex">
              <div
                class="h-full transition-all duration-300"
                :class="loadPercentage > 100 ? 'bg-red-500' : loadPercentage > 80 ? 'bg-amber-400' : 'bg-emerald-500'"
                :style="{ width: `${Math.min(100, loadPercentage)}%` }"
              ></div>
            </div>
            <div class="flex justify-between text-[10px] text-zinc-500 mt-1">
              <span>0%</span>
              <span>Demanda: {{ loadPercentage }}% de capacidad</span>
              <span>100%</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 pt-1 border-t border-zinc-800/80 text-[11px]">
            <div>
              <span class="text-zinc-500 block text-[9px]">Demanda Continua:</span>
              <strong class="text-white">{{ powerFeasibility.totalSystemDemandWatts }} W</strong>
            </div>
            <div>
              <span class="text-zinc-500 block text-[9px]">Picos Transitorios:</span>
              <strong class="text-amber-400">{{ powerFeasibility.transientPeakWatts }} W</strong>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumen Diagnóstico SEC -->
      <div class="p-3 rounded-xl bg-[#14141c] border border-zinc-800 space-y-1.5 text-[11px]">
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
