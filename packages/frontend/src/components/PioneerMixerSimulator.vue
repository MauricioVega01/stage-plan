<template>
  <div class="pioneer-mixer-container select-none font-mono text-white">
    <!-- BARRA SUPERIOR DE PRESETS RÁPIDOS PARA LA DEFENSA -->
    <div class="flex flex-wrap items-center justify-between gap-2 mb-4 bg-[#111116] p-3 rounded-xl border border-zinc-800">
      <div class="flex items-center gap-2">
        <span class="text-xs font-black uppercase text-red-400 tracking-wider">
          🎛️ SIMULADOR HARDWARE PIONEER DJM
        </span>
        <span class="text-[11px] text-zinc-400 hidden sm:inline">
          · Estructura de Ganancia, Low EQ Kill y Salida Master FOH
        </span>
      </div>

      <div class="flex flex-wrap items-center gap-1.5">
        <button
          type="button"
          @click="setPreset('CLEAN')"
          class="px-2.5 py-1.5 rounded-lg text-xs font-bold transition border cursor-pointer"
          :class="ch1Low && !ch2Low && masterPos === '12_OCLOCK'
            ? 'bg-emerald-950 text-emerald-300 border-emerald-500 shadow-md shadow-emerald-950/50'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:text-white'"
        >
          🎧 1 Bajo Activo (12:00)
        </button>
        <button
          type="button"
          @click="setPreset('DOUBLE_BASS')"
          class="px-2.5 py-1.5 rounded-lg text-xs font-bold transition border cursor-pointer"
          :class="ch1Low && ch2Low
            ? 'bg-red-950 text-red-300 border-red-500 shadow-md shadow-red-950 animate-pulse'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:text-white'"
        >
          🚨 Error: 2 Bajos Arriba
        </button>
        <button
          type="button"
          @click="setPreset('MASTER_CLIP')"
          class="px-2.5 py-1.5 rounded-lg text-xs font-bold transition border cursor-pointer"
          :class="masterPos === 'MAX'
            ? 'bg-orange-950 text-orange-300 border-orange-500 shadow-md shadow-orange-950'
            : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:text-white'"
        >
          ⚠️ Master forzado (&gt; 2:00)
        </button>
      </div>
    </div>

    <!-- CHASSIS PRINCIPAL PIONEER DJM CON TEXTURA METÁLICA NEGRA -->
    <div class="djm-chassis p-4 sm:p-6 rounded-2xl border-2 border-zinc-700/80 shadow-2xl relative overflow-hidden">
      <!-- Marca de Agua / Logo Pioneer DJ -->
      <div class="flex items-center justify-between pb-4 border-b border-zinc-700/60 mb-4">
        <div class="flex items-center gap-2">
          <div class="w-3 h-3 rounded-full bg-red-600 shadow-[0_0_8px_#ef4444]"></div>
          <span class="text-xs uppercase font-black text-zinc-400 tracking-widest font-sans">
            STAGE PLAN · VIRTUAL HARDWARE
          </span>
        </div>
        <div class="text-right">
          <span class="text-lg font-black tracking-tight text-white font-sans italic">Pioneer DJ</span>
          <span class="text-[9px] block text-zinc-500 font-mono -mt-1 tracking-widest">DJM-SERIES REPLICA</span>
        </div>
      </div>

      <!-- SECCIÓN PRINCIPAL: CANAL 1 | CANAL 2 | SECCIÓN MASTER -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6">
        
        <!-- ==================== CANAL 1 (DECK A) ==================== -->
        <div class="channel-strip p-3 sm:p-4 rounded-xl border border-zinc-700/70 bg-[#121217] relative flex flex-col justify-between">
          <!-- Header Canal 1 -->
          <div>
            <!-- Selector de Entrada Giratorio -->
            <div class="flex flex-col items-center mb-3">
              <div class="text-[8px] text-zinc-400 font-bold tracking-tighter uppercase mb-0.5 flex gap-2">
                <span>DIGITAL</span>
                <span class="text-white font-black">LINE</span>
                <span>PHONO</span>
              </div>
              <div class="w-8 h-8 rounded-full bg-gradient-to-b from-[#3a3a46] to-[#16161c] border border-zinc-500 shadow-inner flex items-center justify-center relative">
                <div class="w-0.5 h-3.5 bg-white rounded-full absolute top-0.5"></div>
              </div>
              <div class="text-2xl font-black text-white font-sans mt-0.5">1</div>
            </div>

            <!-- Clip Led y TRIM -->
            <div class="flex items-center justify-between mb-3 px-1">
              <span
                class="px-1.5 py-0.5 rounded text-[9px] font-black tracking-widest uppercase border"
                :class="ch1IsClipping
                  ? 'bg-red-600 text-white border-red-400 shadow-[0_0_10px_#ef4444] animate-pulse'
                  : 'bg-zinc-900 text-zinc-600 border-zinc-800'"
              >
                CLIP
              </span>
              <div class="text-right">
                <span class="text-[10px] font-black text-zinc-200 block uppercase tracking-wider">TRIM</span>
                <span class="text-[8px] text-zinc-500 block">DECK 3/C</span>
              </div>
            </div>

            <!-- Fila TRIM Knob + VU Meter Lateral -->
            <div class="flex items-center justify-center gap-3 mb-4">
              <!-- Perilla TRIM -->
              <div class="relative flex flex-col items-center">
                <div class="knob-potentiometer w-12 h-12 rounded-full border border-zinc-500 shadow-lg flex items-center justify-center relative">
                  <div class="w-0.5 h-5 bg-white rounded-full absolute top-1 origin-bottom"></div>
                </div>
                <div class="flex justify-between w-14 text-[8px] text-zinc-400 font-bold mt-1">
                  <span>-∞</span>
                  <span class="text-zinc-200">12:00</span>
                  <span>+9</span>
                </div>
              </div>
            </div>
          </div>

          <!-- CUERPO PRINCIPAL DEL CANAL: VÚMETRO VERTICAL + PERILLAS EQ (HI, MID, LOW) -->
          <div class="flex items-start justify-center gap-4 py-2 border-y border-zinc-800/80 my-2">
            <!-- VÚMETRO PIONEER VERTICAL CH 1 -->
            <div class="flex items-center gap-1 bg-[#0a0a0d] p-1.5 rounded-lg border border-zinc-800">
              <div class="flex flex-col gap-[3px]">
                <div
                  v-for="(seg, idx) in pioneerLeds"
                  :key="'ch1-' + idx"
                  class="w-4 h-2 rounded-[1.5px] transition-all duration-150"
                  :class="getLedClass(ch1Db, seg)"
                ></div>
              </div>
              <div class="flex flex-col justify-between h-[180px] text-[8px] font-bold text-zinc-500 py-0.5">
                <span class="text-red-500">CLIP</span>
                <span class="text-red-400">+12</span>
                <span class="text-amber-400">+9</span>
                <span class="text-amber-400 font-black">+6</span>
                <span class="text-amber-300">+3</span>
                <span class="text-emerald-400 font-black">0</span>
                <span>-6</span>
                <span>-12</span>
                <span>-18</span>
                <span>-∞</span>
              </div>
            </div>

            <!-- COLUMNA DE POTENCIÓMETROS DE EQ (HI, MID, LOW) -->
            <div class="flex flex-col items-center gap-3">
              <!-- HI Knob -->
              <div class="flex flex-col items-center">
                <span class="text-[10px] font-black text-zinc-300 uppercase">HI</span>
                <div class="knob-potentiometer w-11 h-11 rounded-full border border-zinc-500 flex items-center justify-center relative shadow-md">
                  <div class="w-0.5 h-4.5 bg-white rounded-full absolute top-1"></div>
                </div>
                <div class="flex justify-between w-14 text-[7px] text-zinc-500">
                  <span>-26</span>
                  <span class="text-zinc-300">0</span>
                  <span>+6</span>
                </div>
              </div>

              <!-- MID Knob -->
              <div class="flex flex-col items-center">
                <span class="text-[10px] font-black text-zinc-300 uppercase">MID</span>
                <div class="knob-potentiometer w-11 h-11 rounded-full border border-zinc-500 flex items-center justify-center relative shadow-md">
                  <div class="w-0.5 h-4.5 bg-white rounded-full absolute top-1"></div>
                </div>
                <div class="flex justify-between w-14 text-[7px] text-zinc-500">
                  <span>-26</span>
                  <span class="text-zinc-300">0</span>
                  <span>+6</span>
                </div>
              </div>

              <!-- LOW Knob (INTERACTIVO / GIRA AL CORTAR EL BAJO) -->
              <div class="flex flex-col items-center">
                <div class="flex items-center gap-1">
                  <span class="text-[10px] font-black text-zinc-200 uppercase">LOW</span>
                  <span
                    class="text-[8px] font-bold px-1 rounded"
                    :class="ch1Low ? 'bg-emerald-950 text-emerald-300' : 'bg-red-950 text-red-300'"
                  >
                    {{ ch1Low ? '0 dB' : '-∞' }}
                  </span>
                </div>
                <div
                  @click="ch1Low = !ch1Low"
                  title="Haz clic para activar o cortar el bajo de este canal"
                  class="knob-potentiometer w-11 h-11 rounded-full border-2 cursor-pointer transition-transform duration-300 flex items-center justify-center relative shadow-lg"
                  :class="ch1Low ? 'border-emerald-500 shadow-emerald-950/50' : 'border-zinc-600'"
                >
                  <!-- Indicador blanco que rota a -135deg si está en Low Kill (-∞) -->
                  <div
                    class="w-0.5 h-4.5 bg-white rounded-full absolute top-1 transition-transform duration-300 origin-bottom"
                    :style="{ transform: ch1Low ? 'rotate(0deg)' : 'rotate(-135deg)' }"
                  ></div>
                </div>
                <div class="flex justify-between w-14 text-[7px] text-zinc-500">
                  <span :class="!ch1Low ? 'text-red-400 font-bold' : ''">-∞</span>
                  <span :class="ch1Low ? 'text-emerald-400 font-bold' : ''">0</span>
                  <span>+6</span>
                </div>
              </div>
            </div>

            <!-- Indicador Lateral EQ / ISOLATOR -->
            <div class="flex flex-col items-center justify-center self-center h-full text-[8px] text-zinc-500 font-bold border-l border-zinc-700 pl-1.5">
              <span>E</span>
              <span>Q</span>
              <span class="my-1">/</span>
              <span>I</span>
              <span>S</span>
              <span>O</span>
            </div>
          </div>

          <!-- BOTÓN INTERACTIVO DE CONMUTACIÓN RÁPIDA -->
          <button
            type="button"
            @click="ch1Low = !ch1Low"
            class="w-full mt-3 py-2 px-3 rounded-lg text-xs font-black uppercase tracking-wider transition border cursor-pointer"
            :class="ch1Low
              ? 'bg-emerald-700 hover:bg-emerald-600 text-white border-emerald-400 shadow-md shadow-emerald-950'
              : 'bg-zinc-800 hover:bg-zinc-700 text-zinc-400 border-zinc-600'"
          >
            {{ ch1Low ? '🔊 Bajo Activo (12:00)' : '🔇 Low EQ Kill (-∞)' }}
          </button>
        </div>


        <!-- ==================== SECCIÓN MASTER PIONEER FOH ==================== -->
        <div
          class="master-strip p-4 sm:p-5 rounded-xl border-2 bg-[#141219] flex flex-col justify-between shadow-xl"
          :class="isMasterClipping ? 'border-red-600 bg-red-950/20 shadow-red-950/50' : 'border-zinc-700'"
        >
          <!-- Header Master -->
          <div>
            <div class="flex items-center justify-between border-b border-zinc-700/80 pb-2 mb-3">
              <span class="text-xs font-black text-white uppercase tracking-wider">MASTER OUT (XLR)</span>
              <span
                class="px-2 py-0.5 rounded text-[10px] font-black uppercase border tracking-wider"
                :class="isMasterClipping
                  ? 'bg-red-600 text-white border-red-400 shadow-[0_0_12px_#ef4444] animate-pulse'
                  : 'bg-emerald-950 text-emerald-300 border-emerald-600'"
              >
                {{ isMasterClipping ? '🔴 CLIP / DISTORSIÓN' : '🟢 LIMPIO (+4 dBu)' }}
              </span>
            </div>

            <!-- Gran Perilla Giratoria Master Rotary -->
            <div class="flex flex-col items-center justify-center my-3">
              <div class="text-[11px] font-bold text-zinc-300 uppercase mb-2">
                NIVEL MASTER ROTARY (FOH)
              </div>
              <div
                class="w-20 h-20 rounded-full border-4 flex items-center justify-center relative shadow-2xl transition-all duration-300 bg-gradient-to-b from-[#2e2e3a] to-[#121217]"
                :class="isMasterClipping ? 'border-red-500 shadow-red-900/50' : 'border-zinc-500'"
              >
                <!-- Indicador Blanco de la Posición Horaria -->
                <div
                  class="w-1 h-8 bg-white rounded-full absolute top-1.5 transition-transform duration-300 origin-bottom shadow"
                  :style="{
                    transform: masterPos === '12_OCLOCK'
                      ? 'rotate(0deg)'
                      : masterPos === '2_OCLOCK'
                      ? 'rotate(45deg)'
                      : 'rotate(110deg)'
                  }"
                ></div>
                <span class="text-[10px] font-black text-zinc-400 uppercase tracking-widest mt-6">MASTER</span>
              </div>

              <!-- Escala Alrededor del Master -->
              <div class="flex justify-between w-28 text-[9px] text-zinc-400 font-bold mt-2">
                <span>-∞</span>
                <span :class="masterPos === '12_OCLOCK' ? 'text-emerald-400 font-black' : ''">12:00 (0dB)</span>
                <span :class="masterPos === '2_OCLOCK' ? 'text-amber-400 font-black' : ''">2:00</span>
                <span :class="masterPos === 'MAX' ? 'text-red-400 font-black' : ''">+10</span>
              </div>
            </div>

            <!-- Botones de Selección Rápida del Master -->
            <div class="grid grid-cols-3 gap-1.5 my-3">
              <button
                type="button"
                @click="masterPos = '12_OCLOCK'"
                class="py-1.5 px-1 rounded text-[10px] font-bold border transition cursor-pointer"
                :class="masterPos === '12_OCLOCK'
                  ? 'bg-emerald-600 text-white border-emerald-400 shadow-md shadow-emerald-950'
                  : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:text-white'"
              >
                12:00 (0 dB)
              </button>
              <button
                type="button"
                @click="masterPos = '2_OCLOCK'"
                class="py-1.5 px-1 rounded text-[10px] font-bold border transition cursor-pointer"
                :class="masterPos === '2_OCLOCK'
                  ? 'bg-amber-600 text-white border-amber-400 shadow-md shadow-amber-950'
                  : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:text-white'"
              >
                2:00 (+3.5dB)
              </button>
              <button
                type="button"
                @click="masterPos = 'MAX'"
                class="py-1.5 px-1 rounded text-[10px] font-bold border transition cursor-pointer"
                :class="masterPos === 'MAX'
                  ? 'bg-red-600 text-white border-red-400 shadow-md shadow-red-950'
                  : 'bg-zinc-900 text-zinc-400 border-zinc-700 hover:text-white'"
              >
                &gt; 2:00 (Clip)
              </button>
            </div>
          </div>

          <!-- VÚMETRO DUAL MASTER ESTÉREO (L y R) -->
          <div class="bg-[#0b0a0e] p-3 rounded-xl border border-zinc-800 space-y-2 mt-2">
            <div class="flex items-center justify-between text-[11px] font-bold">
              <span class="text-zinc-400 uppercase">Salida Master L / R:</span>
              <span
                class="px-2 py-0.5 rounded font-black font-mono text-xs"
                :class="isMasterClipping ? 'bg-red-950 text-red-300 border border-red-500' : 'bg-emerald-950 text-emerald-300 border border-emerald-600'"
              >
                {{ masterDb > 0 ? `+${masterDb.toFixed(1)}` : masterDb.toFixed(1) }} dB
              </span>
            </div>

            <div class="flex items-center justify-center gap-3 py-1">
              <!-- Canal L -->
              <div class="flex items-center gap-1">
                <span class="text-[9px] font-bold text-zinc-400">L</span>
                <div class="flex flex-col gap-[3px]">
                  <div
                    v-for="(seg, idx) in pioneerLeds"
                    :key="'mst-l-' + idx"
                    class="w-4 h-2 rounded-[1.5px] transition-all duration-150"
                    :class="getLedClass(masterDb, seg)"
                  ></div>
                </div>
              </div>

              <!-- Escala Central de Decibeles -->
              <div class="flex flex-col justify-between h-[180px] text-[8px] font-bold text-zinc-500 py-0.5">
                <span class="text-red-500">CLIP</span>
                <span class="text-red-400">+12</span>
                <span class="text-amber-400">+9</span>
                <span class="text-amber-400 font-black">+6</span>
                <span class="text-amber-300">+3</span>
                <span class="text-emerald-400 font-black">0</span>
                <span>-6</span>
                <span>-12</span>
                <span>-18</span>
                <span>-∞</span>
              </div>

              <!-- Canal R -->
              <div class="flex items-center gap-1">
                <div class="flex flex-col gap-[3px]">
                  <div
                    v-for="(seg, idx) in pioneerLeds"
                    :key="'mst-r-' + idx"
                    class="w-4 h-2 rounded-[1.5px] transition-all duration-150"
                    :class="getLedClass(masterDb, seg)"
                  ></div>
                </div>
                <span class="text-[9px] font-bold text-zinc-400">R</span>
              </div>
            </div>
          </div>
        </div>


        <!-- ==================== CANAL 2 (DECK B) ==================== -->
        <div class="channel-strip p-3 sm:p-4 rounded-xl border border-zinc-700/70 bg-[#121217] relative flex flex-col justify-between">
          <!-- Header Canal 2 -->
          <div>
            <!-- Selector de Entrada Giratorio -->
            <div class="flex flex-col items-center mb-3">
              <div class="text-[8px] text-zinc-400 font-bold tracking-tighter uppercase mb-0.5 flex gap-2">
                <span>DIGITAL</span>
                <span class="text-white font-black">LINE</span>
                <span>PHONO</span>
              </div>
              <div class="w-8 h-8 rounded-full bg-gradient-to-b from-[#3a3a46] to-[#16161c] border border-zinc-500 shadow-inner flex items-center justify-center relative">
                <div class="w-0.5 h-3.5 bg-white rounded-full absolute top-0.5"></div>
              </div>
              <div class="text-2xl font-black text-white font-sans mt-0.5">2</div>
            </div>

            <!-- Clip Led y TRIM -->
            <div class="flex items-center justify-between mb-3 px-1">
              <span
                class="px-1.5 py-0.5 rounded text-[9px] font-black tracking-widest uppercase border"
                :class="ch2IsClipping
                  ? 'bg-red-600 text-white border-red-400 shadow-[0_0_10px_#ef4444] animate-pulse'
                  : 'bg-zinc-900 text-zinc-600 border-zinc-800'"
              >
                CLIP
              </span>
              <div class="text-right">
                <span class="text-[10px] font-black text-zinc-200 block uppercase tracking-wider">TRIM</span>
                <span class="text-[8px] text-zinc-500 block">DECK 1/A</span>
              </div>
            </div>

            <!-- Fila TRIM Knob + VU Meter Lateral -->
            <div class="flex items-center justify-center gap-3 mb-4">
              <!-- Perilla TRIM -->
              <div class="relative flex flex-col items-center">
                <div class="knob-potentiometer w-12 h-12 rounded-full border border-zinc-500 shadow-lg flex items-center justify-center relative">
                  <div class="w-0.5 h-5 bg-white rounded-full absolute top-1 origin-bottom"></div>
                </div>
                <div class="flex justify-between w-14 text-[8px] text-zinc-400 font-bold mt-1">
                  <span>-∞</span>
                  <span class="text-zinc-200">12:00</span>
                  <span>+9</span>
                </div>
              </div>
            </div>
          </div>

          <!-- CUERPO PRINCIPAL DEL CANAL: VÚMETRO VERTICAL + PERILLAS EQ (HI, MID, LOW) -->
          <div class="flex items-start justify-center gap-4 py-2 border-y border-zinc-800/80 my-2">
            <!-- VÚMETRO PIONEER VERTICAL CH 2 -->
            <div class="flex items-center gap-1 bg-[#0a0a0d] p-1.5 rounded-lg border border-zinc-800">
              <div class="flex flex-col gap-[3px]">
                <div
                  v-for="(seg, idx) in pioneerLeds"
                  :key="'ch2-' + idx"
                  class="w-4 h-2 rounded-[1.5px] transition-all duration-150"
                  :class="getLedClass(ch2Db, seg)"
                ></div>
              </div>
              <div class="flex flex-col justify-between h-[180px] text-[8px] font-bold text-zinc-500 py-0.5">
                <span class="text-red-500">CLIP</span>
                <span class="text-red-400">+12</span>
                <span class="text-amber-400">+9</span>
                <span class="text-amber-400 font-black">+6</span>
                <span class="text-amber-300">+3</span>
                <span class="text-emerald-400 font-black">0</span>
                <span>-6</span>
                <span>-12</span>
                <span>-18</span>
                <span>-∞</span>
              </div>
            </div>

            <!-- COLUMNA DE POTENCIÓMETROS DE EQ (HI, MID, LOW) -->
            <div class="flex flex-col items-center gap-3">
              <!-- HI Knob -->
              <div class="flex flex-col items-center">
                <span class="text-[10px] font-black text-zinc-300 uppercase">HI</span>
                <div class="knob-potentiometer w-11 h-11 rounded-full border border-zinc-500 flex items-center justify-center relative shadow-md">
                  <div class="w-0.5 h-4.5 bg-white rounded-full absolute top-1"></div>
                </div>
                <div class="flex justify-between w-14 text-[7px] text-zinc-500">
                  <span>-26</span>
                  <span class="text-zinc-300">0</span>
                  <span>+6</span>
                </div>
              </div>

              <!-- MID Knob -->
              <div class="flex flex-col items-center">
                <span class="text-[10px] font-black text-zinc-300 uppercase">MID</span>
                <div class="knob-potentiometer w-11 h-11 rounded-full border border-zinc-500 flex items-center justify-center relative shadow-md">
                  <div class="w-0.5 h-4.5 bg-white rounded-full absolute top-1"></div>
                </div>
                <div class="flex justify-between w-14 text-[7px] text-zinc-500">
                  <span>-26</span>
                  <span class="text-zinc-300">0</span>
                  <span>+6</span>
                </div>
              </div>

              <!-- LOW Knob (INTERACTIVO / GIRA AL CORTAR EL BAJO) -->
              <div class="flex flex-col items-center">
                <div class="flex items-center gap-1">
                  <span class="text-[10px] font-black text-zinc-200 uppercase">LOW</span>
                  <span
                    class="text-[8px] font-bold px-1 rounded"
                    :class="ch2Low ? 'bg-red-950 text-red-300' : 'bg-cyan-950 text-cyan-300'"
                  >
                    {{ ch2Low ? '0 dB (ERROR)' : '-∞ (KILL)' }}
                  </span>
                </div>
                <div
                  @click="ch2Low = !ch2Low"
                  title="Haz clic para activar o cortar el bajo de este canal"
                  class="knob-potentiometer w-11 h-11 rounded-full border-2 cursor-pointer transition-transform duration-300 flex items-center justify-center relative shadow-lg"
                  :class="ch2Low ? 'border-red-500 shadow-red-950/50 animate-pulse' : 'border-cyan-600'"
                >
                  <!-- Indicador blanco que rota a -135deg si está en Low Kill (-∞) -->
                  <div
                    class="w-0.5 h-4.5 bg-white rounded-full absolute top-1 transition-transform duration-300 origin-bottom"
                    :style="{ transform: ch2Low ? 'rotate(0deg)' : 'rotate(-135deg)' }"
                  ></div>
                </div>
                <div class="flex justify-between w-14 text-[7px] text-zinc-500">
                  <span :class="!ch2Low ? 'text-cyan-400 font-bold' : ''">-∞</span>
                  <span :class="ch2Low ? 'text-red-400 font-bold' : ''">0</span>
                  <span>+6</span>
                </div>
              </div>
            </div>

            <!-- Indicador Lateral EQ / ISOLATOR -->
            <div class="flex flex-col items-center justify-center self-center h-full text-[8px] text-zinc-500 font-bold border-l border-zinc-700 pl-1.5">
              <span>E</span>
              <span>Q</span>
              <span class="my-1">/</span>
              <span>I</span>
              <span>S</span>
              <span>O</span>
            </div>
          </div>

          <!-- BOTÓN INTERACTIVO DE CONMUTACIÓN RÁPIDA -->
          <button
            type="button"
            @click="ch2Low = !ch2Low"
            class="w-full mt-3 py-2 px-3 rounded-lg text-xs font-black uppercase tracking-wider transition border cursor-pointer"
            :class="!ch2Low
              ? 'bg-cyan-700 hover:bg-cyan-600 text-white border-cyan-400 shadow-md shadow-cyan-950'
              : 'bg-red-700 hover:bg-red-600 text-white border-red-400 shadow-md shadow-red-950 animate-pulse'"
          >
            {{ !ch2Low ? '🔇 Mantener Low Kill (-∞)' : '🚨 Activar 2do Bajo (Simular Error)' }}
          </button>
        </div>

      </div>

      <!-- INFORME DE DIAGNÓSTICO TÉCNICO EN VIVO (PARA DEFENSA EN INACAP) -->
      <div
        class="mt-5 p-4 rounded-xl border-2 space-y-2 text-xs leading-relaxed"
        :class="isMasterClipping
          ? 'bg-red-950/40 border-red-600 text-red-200'
          : 'bg-emerald-950/40 border-emerald-600 text-emerald-200'"
      >
        <div class="font-black text-sm uppercase flex items-center gap-2">
          <span>{{ isMasterClipping ? '🚨 ALERTA ROJA EN FOH: DISTORSIÓN ARMÓNICA POR SATURACIÓN' : '✅ ESTRUCTURA DE GANANCIA PROFESIONAL CERTIFICADA' }}</span>
        </div>
        <p v-if="!isMasterClipping" class="text-zinc-200">
          <strong>Transición Limpia (Bass Swap Activo):</strong> Con solo 1 bajo activo en 12:00 (0 dB) y el segundo canal en Low Kill (-∞), los medios y agudos se suman sinérgicamente (+1.5 a +2.5 dB) mientras el rango de sub-graves (30–120 Hz) permanece bajo control absoluto. Con la perilla Master entre las <strong>12:00 (Unity)</strong> y las <strong>2:00 (+3.5 dB)</strong>, el Master se mantiene en <strong>+{{ masterDb.toFixed(1) }} dB</strong> (zona ámbar segura), entregando pegada contundente y protegiendo bobinas de subwoofers y etapas de potencia.
        </p>
        <p v-else-if="ch1Low && ch2Low" class="text-zinc-200">
          <strong>Error Crítico (2 Bajos Arriba Simultáneos):</strong> Al sonar dos bombos/bajos a la vez, se produce una suma incontrolada de hasta <strong>+6 dB en bajas frecuencias</strong>. Esto <strong>cuadruplica la demanda de potencia de pico</strong> en los amplificadores ($P = V^2 / R$), satura el bus Master a <strong>+{{ masterDb.toFixed(1) }} dB CLIP ROJO</strong>, y activa los limitadores del procesador, recalentando bobinas por compresión dinámica destructiva.
        </p>
        <p v-else class="text-zinc-200">
          <strong>Error en FOH (Perilla Master Forzada &gt; 2:00):</strong> Aunque los canales individuales estén bien calibrados, girar la perilla Master más allá de las 2:00 sobreexcita los preamplificadores de salida del mixer, enviando señal recortada (onda cuadrada) a los amplificadores y quemando drivers de agudos.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Definición de los 15 segmentos LED del vúmetro vertical Pioneer DJM
// Valores ordenados de arriba hacia abajo (+CLIP hasta -∞)
const pioneerLeds = [
  { label: 'CLIP', db: 15, colorType: 'red' },
  { label: '+12', db: 12, colorType: 'red' },
  { label: '+9', db: 9, colorType: 'orange' },
  { label: '+6', db: 6, colorType: 'amber' },
  { label: '+3', db: 3, colorType: 'amber' },
  { label: '0', db: 0, colorType: 'amber' },
  { label: '-3', db: -3, colorType: 'yellow-green' },
  { label: '-6', db: -6, colorType: 'green' },
  { label: '-9', db: -9, colorType: 'green' },
  { label: '-12', db: -12, colorType: 'green' },
  { label: '-15', db: -15, colorType: 'green' },
  { label: '-18', db: -18, colorType: 'green' },
  { label: '-21', db: -21, colorType: 'green' },
  { label: '-24', db: -24, colorType: 'green' },
  { label: '-inf', db: -30, colorType: 'green' },
];

// Estado de simulación
const ch1Low = ref(true); // Canal 1 con bajo activo por defecto
const ch2Low = ref(false); // Canal 2 con bajo cortado (-∞ kill) por defecto
const masterPos = ref<'12_OCLOCK' | '2_OCLOCK' | 'MAX'>('12_OCLOCK');

// Nivel medido en CH 1 (Deck A)
const ch1Db = computed(() => {
  if (ch1Low.value && ch2Low.value) return 9.0; // Interferencia si ambos están activos
  return ch1Low.value ? 6.0 : 2.0; // +6 dB ámbar máximo recomendado según la imagen Pioneer
});

// Nivel medido en CH 2 (Deck B)
const ch2Db = computed(() => {
  if (ch1Low.value && ch2Low.value) return 9.0;
  return ch2Low.value ? 6.0 : 2.5; // +2.5 dB si solo suenan medios y agudos (bajo cortado)
});

// Nivel medido en Master Out XLR L/R
const masterDb = computed(() => {
  let base = 2.0; // Nivel base de suma estéreo
  if (ch1Low.value && ch2Low.value) {
    base += 6.5; // Choque destructivo de dos bombos (+6.5 dB)
  } else if (ch1Low.value || ch2Low.value) {
    base += 1.0; // Transición limpia
  }

  // Aporte según posición de perilla Master
  if (masterPos.value === '12_OCLOCK') {
    return base; // Unity 0 dB
  } else if (masterPos.value === '2_OCLOCK') {
    return base + 2.5; // Empuje limpio a cabina (+2.5 dB)
  } else {
    return base + 8.0; // Overdrive forzado (> 2:00)
  }
});

// Condiciones de Clip
const ch1IsClipping = computed(() => ch1Db.value >= 12.0);
const ch2IsClipping = computed(() => ch2Db.value >= 12.0);
const isMasterClipping = computed(() => masterDb.value >= 7.5);

// Función para obtener las clases CSS de cada segmento LED según su estado
function getLedClass(currentDb: number, seg: { label: string; db: number; colorType: string }) {
  const isLit = currentDb >= seg.db;

  if (!isLit) {
    return 'bg-[#18181f] border border-zinc-900/60 opacity-40';
  }

  // Segmento encendido según su color genuino Pioneer
  switch (seg.colorType) {
    case 'red':
      return 'bg-red-600 shadow-[0_0_6px_#ef4444] border-t border-red-300';
    case 'orange':
      return 'bg-orange-500 shadow-[0_0_5px_#f97316] border-t border-orange-300';
    case 'amber':
      return 'bg-amber-400 shadow-[0_0_5px_#fbbf24] border-t border-amber-200';
    case 'yellow-green':
      return 'bg-lime-400 shadow-[0_0_4px_#a3e635] border-t border-lime-200';
    case 'green':
    default:
      return 'bg-emerald-500 shadow-[0_0_4px_#10b981] border-t border-emerald-300';
  }
}

// Presets de demostración
function setPreset(type: 'CLEAN' | 'DOUBLE_BASS' | 'MASTER_CLIP') {
  if (type === 'CLEAN') {
    ch1Low.value = true;
    ch2Low.value = false;
    masterPos.value = '12_OCLOCK';
  } else if (type === 'DOUBLE_BASS') {
    ch1Low.value = true;
    ch2Low.value = true;
    masterPos.value = '12_OCLOCK';
  } else if (type === 'MASTER_CLIP') {
    ch1Low.value = true;
    ch2Low.value = false;
    masterPos.value = 'MAX';
  }
}
</script>

<style scoped>
.djm-chassis {
  background: radial-gradient(circle at 50% 0%, #1c1c24 0%, #0e0e13 70%, #08080a 100%);
}

.channel-strip {
  background: linear-gradient(180deg, #16161d 0%, #101015 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05), 0 4px 12px rgba(0, 0, 0, 0.4);
}

.knob-potentiometer {
  background: radial-gradient(circle at 40% 40%, #3a3a46 0%, #1e1e24 60%, #111116 100%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.2);
}
</style>

