<template>
  <div class="h-screen w-screen overflow-hidden flex flex-col bg-[#08080c] text-white selection:bg-red-600 selection:text-white font-sans select-none">
    <!-- BARRA SUPERIOR FIJA (STUDIO HEADER · 56px) -->
    <StudioHeader />

    <!-- ÁREA DE TRABAJO DINÁMICA (100% ALTURA DISPONIBLE · CERO SCROLL GLOBAL) -->
    <main class="flex-1 min-h-0 overflow-hidden relative">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- BARRA INFERIOR DE TELEMETRÍA Y NAVEGACIÓN (52px) -->
    <StudioFooter v-if="currentStep > 0" />
  </div>
</template>

<script setup lang="ts">
import { useStagePlanState } from './composables/useStagePlanState';
import StudioHeader from './components/layout/StudioHeader.vue';
import StudioFooter from './components/layout/StudioFooter.vue';

const { currentStep } = useStagePlanState();
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
