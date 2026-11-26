<template>
  <header class="h-[50px] flex-none border-b border-zinc-800/80 bg-[#090b11]/95 backdrop-blur-md px-3 sm:px-4 flex items-center justify-between select-none z-30 font-sans">
    <!-- Logo & Titular de Ingeniería -->
    <div class="flex items-center space-x-2.5 cursor-pointer" @click="goToStep(0)">
      <div class="w-7 h-7 bg-gradient-to-br from-red-500 to-red-700 border border-red-400/80 rounded-md flex items-center justify-center font-black text-white text-[11px] font-mono shadow-md shadow-red-950/70">
        SP
      </div>
      <div class="flex items-center gap-1.5">
        <h1 class="text-xs font-black tracking-wider text-white font-mono uppercase">
          Stage Plan <span class="text-red-500">Pro</span>
        </h1>
        <span class="text-[9px] px-1.5 py-0.2 bg-red-950/70 text-red-300 border border-red-700/50 rounded font-mono font-bold tracking-widest hidden sm:inline-block">
          STUDIO
        </span>
      </div>
    </div>

    <!-- Stepper Horizontal No-Scroll (Cockpit Central) -->
    <nav class="hidden md:flex items-center space-x-1">
      <button
        v-for="step in wizardSteps"
        :key="step.id"
        type="button"
        @click="goToStep(step.id)"
        :disabled="!isStepUnlocked(step.id)"
        :class="[
          'px-2.5 py-1 rounded-md text-[11px] font-mono font-bold transition-all duration-150 flex items-center gap-1.5 cursor-pointer relative',
          currentStep === step.id
            ? 'bg-red-600 text-white shadow-md shadow-red-950/90 ring-1 ring-red-400/80 font-black'
            : isStepCompleted(step.id)
            ? 'bg-[#121520] text-zinc-300 hover:bg-[#181d2c] hover:text-white border border-zinc-800/70'
            : isStepUnlocked(step.id)
            ? 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
            : 'text-zinc-600 cursor-not-allowed opacity-40'
        ]"
      >
        <span class="text-xs">{{ step.icon }}</span>
        <span>{{ step.shortLabel }}</span>
        <span
          v-if="isStepCompleted(step.id) && currentStep !== step.id"
          class="text-emerald-400 text-[10px] font-bold"
        >
          ✓
        </span>
      </button>
    </nav>

    <!-- Credencial de Operador y Control de Sesión -->
    <div class="flex items-center gap-2">
      <div
        v-if="operator.isLogged"
        class="flex items-center gap-2 bg-[#10131d] border border-zinc-700/60 px-2.5 py-1 rounded-md text-[11px] font-mono"
      >
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-zinc-200 font-bold truncate max-w-[110px] lg:max-w-[160px]">
          {{ operator.name || 'Mauricio Vega' }}
        </span>
        <button
          type="button"
          @click="handleLogout"
          class="ml-1 text-zinc-500 hover:text-red-400 text-[10px] uppercase font-bold transition cursor-pointer"
          title="Cerrar Sesión"
        >
          Salir
        </button>
      </div>
      <button
        v-else
        type="button"
        @click="goToStep(0)"
        class="flex items-center gap-1.5 bg-red-600/20 hover:bg-red-600/30 border border-red-500/60 px-2.5 py-1 rounded-md text-[11px] font-mono transition text-red-300 font-bold cursor-pointer"
      >
        <span class="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping"></span>
        <span>Login</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useStagePlanState } from '../../composables/useStagePlanState';

const {
  wizardSteps,
  currentStep,
  goToStep,
  isStepUnlocked,
  isStepCompleted,
  operator,
  handleLogout,
} = useStagePlanState();
</script>
