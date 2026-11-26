<template>
  <div class="h-full w-full flex items-center justify-center p-3 sm:p-4 overflow-y-auto font-sans">
    <div class="cockpit-card p-5 sm:p-6 shadow-2xl relative overflow-hidden space-y-4 max-w-md w-full border border-zinc-800/90">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-600 via-amber-500 to-red-600"></div>

      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="text-[10px] font-mono font-black uppercase px-2 py-0.5 rounded-full bg-red-950/80 text-red-300 border border-red-700/60">
          🛡️ Acceso Operador · JWT / Bcrypt
        </span>
        <span class="text-[10px] font-mono text-zinc-500">CONSOLA TÉCNICA</span>
      </div>

      <div class="space-y-1">
        <h2 class="text-lg font-black text-white font-mono uppercase tracking-tight">
          Stage Plan Pro <span class="text-red-500">Studio</span>
        </h2>
        <p class="text-xs text-zinc-400 leading-relaxed font-sans">
          Inicia sesión para acceder al dimensionamiento de recintos, cálculo de carga eléctrica SEC y memoria técnica de eventos.
        </p>
      </div>

      <!-- Alerta de Error de Autenticación -->
      <div v-if="loginError" class="p-2.5 bg-red-950/80 border border-red-500 rounded-lg flex items-start gap-2 text-red-200 text-xs font-mono">
        <span class="text-sm">⚠️</span>
        <div class="flex-1">
          <p class="font-bold">{{ loginError }}</p>
        </div>
        <button type="button" @click="loginError = ''" class="text-zinc-400 hover:text-white font-mono text-xs cursor-pointer">✕</button>
      </div>

      <!-- Formulario de Login -->
      <form @submit.prevent="handleLogin" class="space-y-3 pt-1">
        <div>
          <label class="cockpit-label">Correo Electrónico</label>
          <div class="relative">
            <input
              v-model="operator.email"
              type="email"
              required
              placeholder="ejemplo@distorsioncl.cl"
              class="w-full cockpit-input pl-8 font-mono"
            />
            <span class="absolute left-2.5 top-2 text-zinc-500 text-xs">✉️</span>
          </div>
        </div>

        <div>
          <label class="cockpit-label">Contraseña</label>
          <div class="relative">
            <input
              v-model="operator.password"
              :type="showPassword ? 'text' : 'password'"
              required
              placeholder="••••••••••••"
              class="w-full cockpit-input pl-8 pr-14 font-mono"
            />
            <span class="absolute left-2.5 top-2 text-zinc-500 text-xs">🔒</span>
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-2.5 top-1.5 text-zinc-400 hover:text-zinc-200 text-[10px] font-mono cursor-pointer"
              tabindex="-1"
            >
              {{ showPassword ? 'Ocultar' : 'Ver' }}
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2.5 pt-0.5">
          <div>
            <label class="cockpit-label">Nombre Operador</label>
            <input
              v-model="operator.name"
              type="text"
              placeholder="Mauricio Vega Castillo"
              class="w-full cockpit-input font-mono"
            />
          </div>

          <div>
            <label class="cockpit-label">Rol Técnico</label>
            <select
              v-model="operator.role"
              class="w-full cockpit-input cursor-pointer font-mono"
            >
              <option value="Administrador / Ingeniero FOH">Ingeniero FOH</option>
              <option value="Jefe Técnico Eléctrico">Jefe Técnico Eléctrico</option>
              <option value="Operador de Audio">Operador de Audio</option>
            </select>
          </div>
        </div>

        <div class="flex items-center justify-between text-xs text-zinc-400 pt-0.5 font-mono">
          <label class="flex items-center gap-1.5 cursor-pointer select-none text-[11px]">
            <input
              v-model="operator.rememberMe"
              type="checkbox"
              class="rounded bg-zinc-800 border-zinc-700 text-red-600 focus:ring-0"
            />
            <span>Recordar sesión</span>
          </label>
          <span class="text-zinc-500 text-[9px] uppercase">Bcrypt / Session</span>
        </div>

        <!-- Botón de Envío -->
        <button
          type="submit"
          :disabled="loginLoading"
          class="w-full mt-1.5 py-2 px-3 rounded-lg bg-red-600 hover:bg-red-500 disabled:bg-zinc-800 disabled:text-zinc-500 text-white font-black text-xs uppercase tracking-wider font-mono transition-all shadow-lg shadow-red-950/70 cursor-pointer active:scale-[0.99] flex items-center justify-center gap-1.5"
        >
          <span v-if="loginLoading" class="inline-block w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          <span>{{ loginLoading ? 'Autenticando...' : 'Ingresar a Consola Técnica →' }}</span>
        </button>
      </form>

      <!-- Tarjeta Informativa de Credenciales para Evaluación Docente -->
      <div class="mt-2.5 p-2.5 bg-[#10131d] border border-zinc-800/80 rounded-lg text-xs font-mono space-y-1">
        <div class="flex items-center justify-between">
          <span class="text-zinc-400 font-bold uppercase text-[9px]">Credenciales Demo Docente:</span>
          <button
            type="button"
            @click="fillEvaluationCredentials"
            class="text-red-400 hover:text-red-300 underline cursor-pointer text-[9px] font-bold"
          >
            Autocompletar
          </button>
        </div>
        <div class="grid grid-cols-2 gap-1.5 text-zinc-300 bg-[#090a0f] p-1.5 rounded border border-zinc-800/60 text-[10px]">
          <div><span class="text-zinc-500">Correo:</span> mauricio.vega@distorsioncl.cl</div>
          <div><span class="text-zinc-500">Clave:</span> password123</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useStagePlanState } from '../composables/useStagePlanState';

const {
  operator,
  loginLoading,
  loginError,
  showPassword,
  fillEvaluationCredentials,
  handleLogin,
} = useStagePlanState();
</script>
