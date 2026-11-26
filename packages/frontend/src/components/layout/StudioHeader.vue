<template>
  <header class="h-14 flex-none border-b border-zinc-800 bg-[#0c0c12] px-4 flex items-center justify-between select-none z-30">
    <!-- Logo & Titular de Ingeniería -->
    <div class="flex items-center space-x-3 cursor-pointer" @click="goToStep(0)">
      <div class="w-8 h-8 bg-red-600 border border-red-400 rounded-lg flex items-center justify-center font-black text-white text-xs font-mono shadow-md shadow-red-950/60">
        SP
      </div>
      <div class="flex items-center gap-2">
        <h1 class="text-sm font-black tracking-tight text-white font-mono uppercase">
          Stage Plan <span class="text-red-500">Pro</span>
        </h1>
        <span class="text-[9px] px-1.5 py-0.5 bg-red-950/80 text-red-300 border border-red-700/60 rounded font-mono font-bold tracking-wider hidden sm:inline-block">
          STUDIO OS
        </span>
      </div>
    </div>

    <!-- Stepper Horizontal No-Scroll (Cockpit Central) -->
    <nav class="hidden md:flex items-center space-x-1 lg:space-x-2">
      <button
        v-for="step in wizardSteps"
        :key="step.id"
        @click="goToStep(step.id)"
        :disabled="!isStepUnlocked(step.id)"
        :class="[
          'px-2.5 py-1.5 rounded-lg text-xs font-mono font-bold transition flex items-center gap-1.5',
          currentStep === step.id
            ? 'bg-red-600 text-white shadow-md shadow-red-950/80 ring-1 ring-red-400'
            : isStepCompleted(step.id)
            ? 'bg-zinc-800/80 text-zinc-300 hover:bg-zinc-700 hover:text-white'
            : isStepUnlocked(step.id)
            ? 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
            : 'text-zinc-600 cursor-not-allowed opacity-50'
        ]"
      >
        <span class="text-xs">{{ step.icon }}</span>
        <span>{{ step.shortLabel }}</span>
        <span
          v-if="isStepCompleted(step.id) && currentStep !== step.id"
          class="text-emerald-400 text-[10px]"
        >
          ✓
        </span>
      </button>
    </nav>

    <!-- Credencial de Operador y Control de Sesión -->
    <div class="flex items-center gap-2">
      <div
        v-if="operator.isLogged"
        class="flex items-center gap-2 bg-[#14141c] border border-zinc-700/80 px-2.5 py-1 rounded-lg text-xs font-mono"
      >
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-zinc-200 font-bold truncate max-w-[120px] lg:max-w-[180px]">
          {{ operator.name || 'Mauricio Vega' }}
        </span>
        <button
          @click="handleLogout"
          class="ml-1 text-zinc-400 hover:text-red-400 text-[11px] underline cursor-pointer"
          title="Cerrar Sesión"
        >
          Salir
        </button>
      </div>
      <button
        v-else
        @click="goToStep(0)"
        class="flex items-center gap-1.5 bg-red-600/20 hover:bg-red-600/30 border border-red-500/60 px-2.5 py-1 rounded-lg text-xs font-mono transition text-red-300 font-bold cursor-pointer"
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
