<template>
  <div class="inline-flex items-center">
    <button
      type="button"
      @click="isOpen = true"
      class="w-6 h-6 rounded-full bg-zinc-800 hover:bg-red-600 text-zinc-300 hover:text-white border border-zinc-600 transition flex items-center justify-center text-xs font-bold font-mono shadow-sm cursor-pointer ml-1.5 focus:outline-none focus:ring-2 focus:ring-red-500"
      :title="title"
      aria-label="Más información"
    >
      i
    </button>

    <!-- Modal Accesible de Ayuda Rápida -->
    <div
      v-if="isOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm p-4 animate-in fade-in duration-200"
      @click.self="isOpen = false"
    >
      <div class="bg-zinc-950 border-2 border-red-600 rounded-2xl max-w-lg w-full p-6 shadow-2xl shadow-red-950/60 relative text-left">
        <!-- Botón Cerrar Superior -->
        <button
          @click="isOpen = false"
          class="absolute top-4 right-4 text-zinc-400 hover:text-white bg-zinc-900 border border-zinc-700 w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm cursor-pointer"
        >
          ✕
        </button>

        <!-- Cabecera -->
        <div class="flex items-center gap-2 mb-3">
          <span class="w-3 h-3 bg-red-600 rounded-sm"></span>
          <h3 class="text-lg font-black tracking-wide text-white uppercase font-mono">
            {{ title }}
          </h3>
        </div>

        <!-- Contenido explicativo con lenguaje sencillo -->
        <div class="space-y-4 text-sm text-zinc-200 leading-relaxed">
          <div class="p-3 bg-zinc-900/80 border-l-4 border-red-500 rounded-r-lg">
            <p class="font-bold text-white mb-1">¿Qué es en palabras simples?</p>
            <p>{{ simpleExplanation }}</p>
          </div>

          <div v-if="practicalExample" class="p-3 bg-zinc-900/80 border-l-4 border-amber-500 rounded-r-lg">
            <p class="font-bold text-amber-300 mb-1">Ejemplo en la vida real:</p>
            <p>{{ practicalExample }}</p>
          </div>

          <div v-if="goldenRule" class="p-3 bg-zinc-900/80 border-l-4 border-emerald-500 rounded-r-lg">
            <p class="font-bold text-emerald-300 mb-1">Regla de oro para el evento:</p>
            <p>{{ goldenRule }}</p>
          </div>
        </div>

        <button
          @click="isOpen = false"
          class="mt-5 w-full bg-red-600 hover:bg-red-500 text-white font-bold py-2.5 px-4 rounded-xl text-sm uppercase tracking-wider transition cursor-pointer"
        >
          Entendido, cerrar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  title: string;
  simpleExplanation: string;
  practicalExample?: string;
  goldenRule?: string;
}>();

const isOpen = ref(false);
</script>

