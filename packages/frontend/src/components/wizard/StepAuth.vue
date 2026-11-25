<template>
  <section class="max-w-xl mx-auto space-y-6">
    <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden space-y-6">
      <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-red-600 via-amber-500 to-red-600"></div>

      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-xs font-mono font-black uppercase px-3 py-1 rounded-full bg-red-950/80 text-red-300 border border-red-700">
          🛡️ Sesión Segura Anti-IDOR · JWT / Bcrypt
        </span>
        <span class="text-xs font-mono text-zinc-400">VISTA 0 · AUTENTICACIÓN</span>
      </div>

      <div class="space-y-2">
        <h2 class="text-2xl sm:text-3xl font-black text-white font-mono uppercase tracking-tight">
          Consola Técnica Stage Plan
        </h2>
        <p class="text-sm text-zinc-300 leading-relaxed">
          Inicia sesión con tus credenciales de operador para acceder al dimensionamiento de recintos, cálculo de impedancia y generación de reportes normativos SEC.
        </p>
      </div>

      <!-- Alerta de Error de Autenticación -->
      <div v-if="loginError" class="p-3.5 bg-red-950/80 border-2 border-red-500 rounded-xl flex items-start gap-3 text-red-200 text-sm">
        <span class="text-lg">⚠️</span>
        <div class="flex-1">
          <p class="font-bold font-mono">{{ loginError }}</p>
        </div>
        <button @click="$emit('clear-error')" class="text-zinc-400 hover:text-white font-mono text-xs cursor-pointer">✕</button>
      </div>

      <!-- Formulario de Login -->
      <form @submit.prevent="$emit('login')" class="space-y-4 pt-1">
        <div>
          <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1.5">
            Correo Electrónico
          </label>
          <div class="relative">
            <input
              :value="operator.email"
              @input="updateField('email', ($event.target as HTMLInputElement).value)"
              type="email"
              required
              placeholder="ejemplo@distorsioncl.cl"
              class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl pl-11 pr-4 py-3 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
            />
            <span class="absolute left-3.5 top-3.5 text-zinc-400 text-sm">✉️</span>
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1.5">
            Contraseña
          </label>
          <div class="relative">
            <input
              :value="operator.password"
              @input="updateField('password', ($event.target as HTMLInputElement).value)"
              :type="showPassword ? 'text' : 'password'"
              required
              placeholder="••••••••••••"
              class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl pl-11 pr-16 py-3 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
            />
            <span class="absolute left-3.5 top-3.5 text-zinc-400 text-sm">🔒</span>
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3.5 top-3.5 text-zinc-400 hover:text-zinc-200 text-xs font-mono cursor-pointer"
              tabindex="-1"
            >
              {{ showPassword ? 'Ocultar' : 'Ver' }}
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
          <div>
            <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1.5">
              Nombre Operador
            </label>
            <input
              :value="operator.name"
              @input="updateField('name', ($event.target as HTMLInputElement).value)"
              type="text"
              placeholder="Mauricio Vega Castillo"
              class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-3.5 py-2.5 text-xs text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
            />
          </div>

          <div>
            <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1.5">
              Rol Técnico
            </label>
            <select
              :value="operator.role"
              @change="updateField('role', ($event.target as HTMLSelectElement).value)"
              class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-red-500 transition cursor-pointer"
            >
              <option value="Administrador / Ingeniero FOH">Administrador / Ingeniero FOH</option>
              <option value="Jefe Técnico Eléctrico">Jefe Técnico Eléctrico</option>
              <option value="Operador de Audio">Operador de Audio</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-zinc-400 pt-2 font-mono">
          <label class="flex items-center gap-2 cursor-pointer select-none">
            <input
              :checked="operator.rememberMe"
              @change="updateField('rememberMe', ($event.target as HTMLInputElement).checked)"
              type="checkbox"
              class="rounded bg-zinc-800 border-zinc-700 text-red-600 focus:ring-0"
            />
            <span>Recordar sesión</span>
          </label>
          <span class="text-zinc-500">Cifrado Bcrypt / Argon2id</span>
        </div>

        <!-- Botón de Envío -->
        <button
          type="submit"
          :disabled="loginLoading"
          class="w-full mt-3 py-3.5 px-6 rounded-xl bg-red-600 hover:bg-red-500 disabled:bg-zinc-800 disabled:text-zinc-500 text-white font-black text-sm uppercase tracking-wider font-mono transition-all shadow-xl shadow-red-950/60 cursor-pointer active:scale-[0.99] flex items-center justify-center gap-2"
        >
          <span v-if="loginLoading" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ loginLoading ? 'Autenticando...' : 'Ingresar a Consola Técnica →' }}</span>
        </button>
      </form>

      <!-- Tarjeta Informativa de Credenciales para Evaluación Docente -->
      <div class="mt-4 p-4 bg-[#14141a] border border-zinc-700/80 rounded-2xl text-xs font-mono space-y-2">
        <div class="flex items-center justify-between">
          <span class="text-zinc-400 font-bold uppercase tracking-wider">Credenciales para Evaluación Docente:</span>
          <button
            type="button"
            @click="$emit('fill-credentials')"
            class="text-red-400 hover:text-red-300 underline cursor-pointer"
          >
            Autocompletar
          </button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-zinc-300 bg-[#0b0b0f] p-2.5 rounded-lg border border-zinc-800">
          <div><span class="text-zinc-500">Correo:</span> mauricio.vega@distorsioncl.cl</div>
          <div><span class="text-zinc-500">Clave:</span> password123</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps<{
  operator: {
    email: string;
    password: string;
    name: string;
    role: string;
    rememberMe: boolean;
  };
  loginError: string;
  loginLoading: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:operator', value: typeof props.operator): void;
  (e: 'login'): void;
  (e: 'clear-error'): void;
  (e: 'fill-credentials'): void;
}>();

const showPassword = ref(false);

function updateField(key: string, value: any) {
  emit('update:operator', {
    ...props.operator,
    [key]: value,
  });
}
</script>
