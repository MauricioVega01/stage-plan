<template>
  <div class="min-h-screen bg-[#050505] text-zinc-100 pb-28 md:pb-16 font-sans selection:bg-red-600 selection:text-white">
    <!-- HEADER PRINCIPAL HARD TECHNO INDUSTRIAL -->
    <header class="bg-[#0b0b0f] border-b-2 border-red-600/80 sticky top-0 z-40 px-4 sm:px-6 py-3.5 shadow-2xl shadow-black/90">
      <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-3">
        <!-- Logo e Identidad -->
        <div class="flex items-center space-x-3 cursor-pointer" @click="goToStep(0)">
          <div class="w-11 h-11 bg-red-600 border-2 border-red-400 rounded-xl flex items-center justify-center font-black text-white text-lg shadow-lg shadow-red-600/40 font-mono tracking-tighter">
            SP
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="text-xl font-black tracking-tight text-white font-mono uppercase">
                Stage Plan
              </h1>
              <span class="text-[10px] px-2 py-0.5 bg-red-950 text-red-300 border border-red-700 rounded font-mono font-bold tracking-wider">
                PRO OS
              </span>
            </div>
            <p class="text-xs text-zinc-400 font-medium">
              Ingeniería Electroacústica & Seguridad Eléctrica — DISTORSIONCL SPA
            </p>
          </div>
        </div>

        <!-- Credencial de Operador Activo + Descarga Rápida PDF -->
        <div class="flex items-center gap-2.5">
          <div
            v-if="operator.isLogged"
            class="flex items-center gap-2 bg-[#14141a] border border-emerald-700/60 px-3 py-1.5 rounded-xl text-xs font-mono"
          >
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span class="text-emerald-300 font-bold truncate max-w-[150px] sm:max-w-[220px]">
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
            class="flex items-center gap-2 bg-[#14141a] hover:bg-[#1c1c24] border border-amber-600/60 px-3 py-1.5 rounded-xl text-xs font-mono transition cursor-pointer text-amber-300 font-bold"
          >
            <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
            <span>Iniciar Sesión</span>
          </button>

          <button
            @click="downloadPdf"
            :disabled="!isValidated"
            :class="[
              'flex items-center space-x-2 text-xs sm:text-sm font-black px-4 py-2.5 rounded-xl transition-all shadow-lg tracking-wide uppercase font-mono',
              isValidated
                ? 'bg-red-600 hover:bg-red-500 text-white cursor-pointer active:scale-95 shadow-red-600/30'
                : 'bg-zinc-900 border border-zinc-800 text-zinc-500 cursor-not-allowed opacity-50'
            ]"
            title="Valida los datos en el Paso 2 para habilitar la descarga del PDF"
          >
            <span>📄 PDF Offline</span>
            <span v-if="isValidated" class="w-2 h-2 rounded-full bg-white animate-pulse"></span>
          </button>
        </div>
      </div>

      <!-- STEPPER DE NAVEGACIÓN EN PC (DESKTOP >= 768px) -->
      <div class="max-w-6xl mx-auto mt-3.5 hidden md:grid md:grid-cols-5 gap-2 pt-3 border-t border-zinc-800/80">
        <button
          v-for="step in wizardSteps"
          :key="step.id"
          @click="goToStep(step.id)"
          :class="[
            'flex items-center gap-2.5 p-2.5 rounded-xl border-2 text-left transition-all cursor-pointer',
            currentStep === step.id
              ? 'bg-red-950/60 border-red-500 text-white shadow-lg shadow-red-950/50'
              : isStepUnlocked(step.id)
              ? 'bg-[#121217] hover:bg-[#191920] border-zinc-800 text-zinc-300'
              : 'bg-[#0c0c10] border-zinc-900 text-zinc-500 opacity-70'
          ]"
        >
          <div
            :class="[
              'w-8 h-8 rounded-lg flex items-center justify-center font-mono font-black text-sm shrink-0 border',
              currentStep === step.id
                ? 'bg-red-600 border-white text-white'
                : isStepCompleted(step.id)
                ? 'bg-emerald-950 border-emerald-500 text-emerald-300'
                : 'bg-zinc-900 border-zinc-700 text-zinc-400'
            ]"
          >
            {{ isStepCompleted(step.id) && currentStep !== step.id ? '✓' : step.id }}
          </div>
          <div class="overflow-hidden">
            <div class="text-xs font-black uppercase font-mono truncate">{{ step.shortLabel }}</div>
            <div class="text-[11px] text-zinc-400 truncate">{{ step.subtitle }}</div>
          </div>
        </button>
      </div>

      <!-- BARRA COMPACTA DE PROGRESO EN CELULAR (MOBILE < 768px) -->
      <div class="md:hidden mt-3 pt-2.5 border-t border-zinc-800 flex items-center justify-between text-xs font-mono">
        <span class="text-red-400 font-black uppercase">
          ETAPA {{ currentStep }} DE 4: {{ wizardSteps[currentStep].title }}
        </span>
        <span class="text-zinc-400 font-bold">
          {{ isValidated ? '✅ Validado' : '⏳ En configuración' }}
        </span>
      </div>
    </header>

    <!-- CONTENEDOR PRINCIPAL DE VISTAS SECUENCIALES (CENTRADO, AMPLIO Y LEGIBLE PARA BAJA VISIÓN) -->
    <main class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <!-- ===================================================================== -->
      <!-- VISTA 0: AUTENTICACIÓN Y LOGIN DE OPERADOR (DISTORSIONCL SPA)         -->
      <!-- ===================================================================== -->
      <section v-if="currentStep === 0" class="max-w-xl mx-auto space-y-6">
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden space-y-6">
          <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-red-600 via-amber-500 to-red-600"></div>

          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="text-xs font-mono font-black uppercase px-3 py-1 rounded-full bg-red-950/80 text-red-300 border border-red-700">
              🛡️ Sesión Segura Anti-IDOR · JWT / Argon2
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
            <button @click="loginError = ''" class="text-zinc-400 hover:text-white font-mono text-xs cursor-pointer">✕</button>
          </div>

          <!-- Formulario de Login -->
          <form @submit.prevent="handleLogin" class="space-y-4 pt-1">
            <div>
              <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono mb-1.5">
                Correo Electrónico
              </label>
              <div class="relative">
                <input
                  v-model="operator.email"
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
                  v-model="operator.password"
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
                  v-model="operator.name"
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
                  v-model="operator.role"
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
                  v-model="operator.rememberMe"
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
                @click="fillEvaluationCredentials"
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

      <!-- ===================================================================== -->
      <!-- VISTA 1: ESCENARIO, MEDIDAS DEL RECINTO Y 8 CASOS COTIDIANOS          -->
      <!-- ===================================================================== -->
      <section v-else-if="currentStep === 1" class="space-y-8">
        <!-- Galería de 8 Casos Reales de Menor a Mayor Escala -->
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-6 shadow-2xl space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 pb-4">
            <div>
              <span class="text-xs font-mono font-bold text-red-400 uppercase block">
                Opción A · Cargar Caso de Estudio Real en 1 Clic
              </span>
              <h2 class="text-lg sm:text-xl font-black text-white font-mono uppercase">
                8 Escenarios Cotidianos (De Menor a Mayor Escala)
              </h2>
            </div>
            <button
              @click="clearForm"
              class="text-xs sm:text-sm font-mono font-bold px-4 py-2 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-200 border border-zinc-700 cursor-pointer transition"
            >
              🧹 Dejar Campos Vacíos
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            <button
              v-for="preset in demoPresets"
              :key="preset.id"
              @click="loadPreset(preset)"
              :class="[
                'text-left p-3.5 rounded-xl border-2 transition-all cursor-pointer flex flex-col justify-between gap-2',
                activePresetId === preset.id
                  ? 'bg-red-950/50 border-red-500 shadow-lg shadow-red-950/40'
                  : 'bg-[#15151c] hover:bg-[#1c1c26] border-zinc-800 hover:border-zinc-600'
              ]"
            >
              <div class="flex items-center justify-between gap-1">
                <span class="text-[10px] font-mono font-black uppercase px-2 py-0.5 rounded" :class="preset.badgeClass">
                  {{ preset.scaleTag }}
                </span>
                <span class="text-xs font-mono text-zinc-300 font-bold">{{ preset.areaLabel }}</span>
              </div>
              <div class="text-sm font-bold text-white leading-snug">
                {{ preset.title }}
              </div>
              <div class="text-xs font-mono text-zinc-400 leading-tight">
                {{ preset.subtitle }}
              </div>
            </button>
          </div>

          <!-- Atajo inmediato cuando se elige un Preset Demo -->
          <div
            v-if="activePresetId && isValidated"
            class="p-4 rounded-xl bg-emerald-950/40 border-2 border-emerald-600 flex flex-wrap items-center justify-between gap-3"
          >
            <div class="text-sm text-emerald-200">
              <strong>✔️ Escenario cargado y validado:</strong> Puedes revisar las medidas abajo o saltar directo al Plano 2D o al Reporte Final.
            </div>
            <div class="flex flex-wrap gap-2">
              <button
                @click="goToStep(3)"
                class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs uppercase font-mono cursor-pointer transition"
              >
                🗺️ Ver Plano 2D y Mixer (Paso 3) →
              </button>
              <button
                @click="goToStep(4)"
                class="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 text-white font-black text-xs uppercase font-mono cursor-pointer transition"
              >
                📋 Ir al Reporte Final (Paso 4) →
              </button>
            </div>
          </div>
        </div>

        <!-- Formulario Espacioso de Medidas del Salón o Parcela -->
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-2xl relative overflow-hidden space-y-6">
          <div class="absolute top-0 left-0 w-1.5 h-full bg-red-600"></div>

          <div class="flex items-center justify-between border-b border-zinc-800 pb-4">
            <h2 class="text-lg sm:text-xl font-black tracking-wider text-white uppercase font-mono">
              <span class="text-red-500">[ PASO 1 ]</span> Medidas del Recinto o Parcela
            </h2>
            <span class="text-xs font-mono text-zinc-400">Letras grandes para lectura cómoda</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div class="sm:col-span-2">
              <label class="block text-base font-bold text-white mb-2">
                Nombre del Recinto, Club o Parcela
              </label>
              <input
                v-model="venue.name"
                @input="resetValidation"
                type="text"
                placeholder="Ej: Parcela Los Aromos, Curacaví"
                class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 transition"
              />
            </div>

            <div>
              <label class="block text-base font-bold text-white mb-2">
                Ancho del Lugar (metros)
              </label>
              <input
                v-model.number="venue.widthMeters"
                @input="resetValidation"
                type="number"
                inputmode="numeric"
                min="1"
                placeholder="Ej: 12"
                class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
              />
            </div>

            <div>
              <label class="block text-base font-bold text-white mb-2">
                Largo / Fondo de la Pista (metros)
              </label>
              <input
                v-model.number="venue.depthMeters"
                @input="resetValidation"
                type="number"
                inputmode="numeric"
                min="1"
                placeholder="Ej: 18"
                class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
              />
            </div>

            <div>
              <label class="block text-base font-bold text-white mb-2 flex items-center justify-between">
                <span>Distancia al Enchufe o Generador (m)</span>
                <InfoBadge
                  title="Distancia al Punto Eléctrico"
                  simple-explanation="Cuántos metros hay caminando por la orilla desde la cabina DJ hasta el enchufe de pared o hasta el generador."
                  practical-example="A más de 30 metros un cable delgado de casa pierde voltaje y apaga las cajas en el golpe del bajo."
                  golden-rule="Más de 20m exige cable de 2.5 mm²; más de 35m exige 4.0 mm²."
                />
              </label>
              <input
                v-model.number="venue.electricalDistanceMeters"
                @input="resetValidation"
                type="number"
                inputmode="numeric"
                min="1"
                placeholder="Ej: 30"
                class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
              />
            </div>

            <div>
              <label class="block text-base font-bold text-white mb-2 flex items-center justify-between">
                <span>Tipo de Recinto (Acústica)</span>
                <InfoBadge
                  title="Cerrado (Indoor) vs. Aire Libre (Outdoor)"
                  simple-explanation="En un salón cerrado el sonido rebota en paredes y techo generando eco (RT60 Sabine). Al aire libre no hay eco, pero el sonido pierde 6 dB cada vez que duplicas la distancia."
                />
              </label>
              <select
                v-model="venue.environmentType"
                @change="resetValidation"
                class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white focus:outline-none focus:border-red-500 transition cursor-pointer"
              >
                <option value="INDOOR">🏛️ Cerrado (Salón / Galpón / Casa)</option>
                <option value="OUTDOOR_PARCELA">🌲 Al Aire Libre (Parcela / Patio / Predio)</option>
              </select>
            </div>

            <div>
              <label class="block text-base font-bold text-white mb-2">
                Duración del Evento (horas de música)
              </label>
              <input
                v-model.number="venue.eventDurationHours"
                @input="resetValidation"
                type="number"
                inputmode="numeric"
                min="1"
                max="24"
                placeholder="Ej: 7"
                class="w-full bg-[#18181f] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white placeholder:text-zinc-500 focus:outline-none focus:border-red-500 font-mono transition"
              />
            </div>

            <div class="bg-[#14141c] border-2 border-zinc-800 rounded-xl p-4 flex items-center justify-between">
              <div>
                <span class="text-xs font-mono uppercase text-zinc-400 block">Superficie y Aforo Estimado</span>
                <span class="text-lg font-black font-mono text-red-400">
                  {{ (venue.widthMeters && venue.depthMeters) ? (venue.widthMeters * venue.depthMeters) : 0 }} m²
                  <span class="text-zinc-300 text-sm">
                    (~{{ (venue.widthMeters && venue.depthMeters) ? Math.round(venue.widthMeters * venue.depthMeters * 0.72 * 2.2) : 0 }} personas)
                  </span>
                </span>
              </div>
              <span class="text-2xl">📐</span>
            </div>
          </div>

          <!-- Innovación 5: Parámetros de Entorno Vecinal (D.S. N° 38 MMA Chile) -->
          <div class="bg-[#15151d] border-2 border-zinc-800 rounded-2xl p-5 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <h3 class="text-sm sm:text-base font-black text-white uppercase font-mono flex items-center gap-2">
                <span>🏘️ Simulador de Ruido a Vecinos y Ordenanza Municipal (D.S. N° 38 MMA)</span>
                <InfoBadge
                  title="Prevención de Partes por Ruidos Molestos"
                  simple-explanation="Estima cuántos decibeles llegarán a la vivienda más cercana según la distancia, el tipo de muro del recinto y si la fiesta es de día o de noche."
                />
              </h3>
              <span class="text-xs font-mono text-amber-400 font-bold">Norma Chilena D.S. N° 38</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-bold text-zinc-200 mb-2">Distancia al Vecino más cercano (m)</label>
                <input
                  v-model.number="venue.neighborDistanceMeters"
                  type="number"
                  min="5"
                  max="2000"
                  placeholder="Ej: 35"
                  class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3 text-base text-white font-mono focus:outline-none focus:border-red-500"
                />
              </div>

              <div>
                <label class="block text-sm font-bold text-zinc-200 mb-2">Tipo de Cierre / Aislamiento</label>
                <select
                  v-model="venue.enclosureWallType"
                  class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3 text-base text-white focus:outline-none focus:border-red-500 cursor-pointer"
                >
                  <option value="OPEN_AIR">🌲 Aire Libre / Patio Abierto (0 dB aislamiento)</option>
                  <option value="TENT_CANVAS">🎪 Carpa / Toldo de Lona (-4 dB aislamiento)</option>
                  <option value="METAL_WAREHOUSE">🏭 Galpón Industrial Techo Lata (-13 dB)</option>
                  <option value="BRICK_CONCRETE_CLOSED">🧱 Salón Ladrillo / Hormigón Cerrado (-25 dB)</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-bold text-zinc-200 mb-2">Horario del Evento</label>
                <select
                  v-model="venue.scheduleShift"
                  class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3 text-base text-white focus:outline-none focus:border-red-500 cursor-pointer"
                >
                  <option value="NIGHTTIME_21_07">🌙 Nocturno 21:00 a 07:00 (Límite 48 dBA)</option>
                  <option value="DAYTIME_07_21">☀️ Diurno 07:00 a 21:00 (Límite 60 dBA)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Botones de Avance Paso 1 -> Paso 2 -->
          <div class="flex flex-wrap items-center justify-between gap-4 pt-6 border-t border-zinc-800">
            <button
              @click="goToStep(0)"
              class="px-5 py-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 font-mono font-bold text-sm cursor-pointer transition"
            >
              ← Volver a Operador
            </button>
            <button
              @click="goToStep(2)"
              class="px-6 py-4 rounded-xl bg-red-600 hover:bg-red-500 text-white font-black text-base uppercase tracking-wider font-mono shadow-xl shadow-red-950/50 cursor-pointer transition"
            >
              Siguiente: Sonido Mixto y Energía (Paso 2) →
            </button>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VISTA 2: CONSTRUCTOR DE INVENTARIO MIXTO POR LOTES (RMS + PEAK)       -->
      <!-- ===================================================================== -->
      <section v-else-if="currentStep === 2" class="space-y-8">
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-6 sm:p-8 shadow-2xl relative overflow-hidden space-y-6">
          <div class="absolute top-0 left-0 w-1.5 h-full bg-red-600"></div>

          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 pb-4">
            <div>
              <h2 class="text-lg sm:text-xl font-black tracking-wider text-white uppercase font-mono">
                <span class="text-red-500">[ PASO 2 ]</span> Constructor de Equipos Mixto (Activos + Pasivos · RMS y Peak)
              </h2>
              <p class="text-xs sm:text-sm text-zinc-300 font-mono mt-1">
                Combina distintas cajas (ej. <strong>2 Cajas Activas + 1 Pasiva</strong>) y distintos Sub-Bajos indicando sus <strong>Watts RMS</strong> y <strong>Watts Peak</strong>.
              </p>
            </div>

            <!-- Barra de Acciones Rápidas: Ejemplo Mixto + Guardado LocalStorage -->
            <div class="flex flex-wrap items-center gap-2">
              <button
                type="button"
                @click="loadMixedActivePassiveExample"
                class="px-3.5 py-2 rounded-xl bg-red-950 hover:bg-red-900 text-red-200 border border-red-600 text-xs font-mono font-black uppercase cursor-pointer transition"
              >
                ⚡ Ejemplo: 2 Activas + 1 Pasiva + Subs Mixtos
              </button>
              <button
                type="button"
                @click="saveCustomRigToStorage"
                class="px-3 py-2 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-200 border border-zinc-700 text-xs font-mono font-bold cursor-pointer transition"
              >
                💾 Guardar Mi Set
              </button>
              <button
                v-if="hasSavedCustomRig"
                type="button"
                @click="loadCustomRigFromStorage"
                class="px-3 py-2 rounded-xl bg-emerald-950 hover:bg-emerald-900 text-emerald-300 border border-emerald-600 text-xs font-mono font-bold cursor-pointer transition"
              >
                📂 Cargar Mi Set
              </button>
            </div>
          </div>

          <div v-if="storageFeedbackMsg" class="p-3 rounded-xl bg-emerald-950/60 border border-emerald-500 text-emerald-200 text-xs font-mono font-bold">
            {{ storageFeedbackMsg }}
          </div>

          <!-- Bloque A: Constructor por Lotes de Cajas Acústicas en Atril (Letras A, B, C...) -->
          <div class="bg-[#15151c] border-2 border-zinc-800 rounded-2xl p-5 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-full bg-red-500"></span>
                <h3 class="text-base font-black text-white uppercase font-mono">
                  A. Lotes de Cajas Acústicas en Atriles (Voz, Medios y Agudos)
                </h3>
                <InfoBadge
                  title="Mezcla de Cajas Activas y Pasivas (Asymmetric Rigging)"
                  simple-explanation="Puedes agregar varios lotes (por ejemplo 2 Cajas Activas de 500W RMS y 1 Caja Pasiva de 350W RMS). El motor pondrá automáticamente las 2 más potentes en el Frente Principal (A y B) y usará la 3ª como Torre de Refuerzo Delay (C) calculando cómo emparejar su ganancia."
                />
              </div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-mono bg-red-950/70 text-red-300 px-2.5 py-1 rounded border border-red-800 font-bold">
                  Total Tops: {{ totalTopsCount }} cajas ({{ totalTopsRmsWatts }}W RMS / {{ totalTopsPeakWatts }}W Peak)
                </span>
                <button
                  type="button"
                  @click="addTopBatch"
                  class="px-3.5 py-1.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-mono font-black text-xs uppercase cursor-pointer transition shadow-md"
                >
                  + Agregar Lote de Cajas
                </button>
              </div>
            </div>

            <!-- Lista de Lotes de Cajas -->
            <div class="space-y-3">
              <div
                v-for="(batch, idx) in topBatches"
                :key="batch.id"
                class="p-4 rounded-xl bg-[#1c1c25] border-2 transition space-y-3"
                :class="batch.systemType === 'ACTIVE' ? 'border-red-900/70' : 'border-amber-700/70'"
              >
                <div class="flex flex-wrap items-center justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="text-[11px] font-mono font-black px-2.5 py-0.5 rounded uppercase"
                      :class="batch.systemType === 'ACTIVE' ? 'bg-red-600 text-white' : 'bg-amber-500 text-black'"
                    >
                      Lote Caja #{{ idx + 1 }} · {{ batch.systemType === 'ACTIVE' ? 'ACTIVA (220V + XLR)' : 'PASIVA (Power + Speakon)' }}
                    </span>
                    <input
                      v-model="batch.modelLabel"
                      type="text"
                      placeholder="Nombre opcional (Ej: RCF ART / JBL Pasiva)"
                      class="bg-[#121218] border border-zinc-700 rounded-lg px-3 py-1 text-xs text-white font-mono focus:outline-none focus:border-red-500"
                    />
                  </div>
                  <button
                    v-if="topBatches.length > 1"
                    type="button"
                    @click="removeTopBatch(idx)"
                    class="text-xs font-mono text-red-400 hover:text-red-300 bg-red-950/50 px-2.5 py-1 rounded border border-red-800 cursor-pointer"
                  >
                    🗑️ Quitar Lote
                  </button>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-6 gap-3">
                  <div>
                    <label class="block text-xs font-bold text-zinc-300 mb-1">Tecnología</label>
                    <select
                      v-model="batch.systemType"
                      @change="resetValidation"
                      class="w-full bg-[#121218] border border-zinc-700 rounded-lg px-2.5 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-red-500 cursor-pointer"
                    >
                      <option value="ACTIVE">⚡ Activa</option>
                      <option value="PASSIVE">🔌 Pasiva</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-zinc-300 mb-1">Cantidad</label>
                    <input
                      v-model.number="batch.quantity"
                      @input="resetValidation"
                      type="number"
                      min="0"
                      max="12"
                      class="w-full bg-[#121218] border border-zinc-700 rounded-lg px-3 py-2.5 text-base text-white font-mono font-bold focus:outline-none focus:border-red-500"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-zinc-300 mb-1">Cono (Pulgadas)</label>
                    <select
                      v-model.number="batch.coneSizeInches"
                      @change="resetValidation"
                      class="w-full bg-[#121218] border border-zinc-700 rounded-lg px-2.5 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-red-500 cursor-pointer"
                    >
                      <option :value="10">10" Pulgadas</option>
                      <option :value="12">12" Pulgadas</option>
                      <option :value="15">15" Pulgadas</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-emerald-300 mb-1">Watts RMS (c/u)</label>
                    <input
                      v-model.number="batch.rmsWatts"
                      @input="onBatchRmsChange(batch)"
                      type="number"
                      min="50"
                      max="5000"
                      placeholder="Ej: 500"
                      class="w-full bg-[#121218] border border-emerald-700 rounded-lg px-3 py-2.5 text-base text-emerald-300 font-mono font-bold focus:outline-none focus:border-emerald-400"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-amber-300 mb-1">Watts Peak (c/u)</label>
                    <input
                      v-model.number="batch.peakWatts"
                      @input="resetValidation"
                      type="number"
                      min="100"
                      max="10000"
                      placeholder="Ej: 1000"
                      class="w-full bg-[#121218] border border-amber-700 rounded-lg px-3 py-2.5 text-base text-amber-300 font-mono font-bold focus:outline-none focus:border-amber-400"
                    />
                  </div>

                  <div v-if="batch.systemType === 'PASSIVE'">
                    <label class="block text-xs font-bold text-cyan-300 mb-1">Impedancia (Ω)</label>
                    <select
                      v-model.number="batch.impedanceOhms"
                      @change="resetValidation"
                      class="w-full bg-[#121218] border border-cyan-600 rounded-lg px-2.5 py-2.5 text-sm text-cyan-300 font-mono font-bold focus:outline-none focus:border-cyan-400 cursor-pointer"
                    >
                      <option :value="8">8 Ω (Estándar)</option>
                      <option :value="4">4 Ω (Alta Carga)</option>
                    </select>
                  </div>
                  <div v-else class="flex flex-col justify-end">
                    <span class="text-[11px] font-mono text-zinc-400 bg-[#121218] border border-zinc-800 rounded-lg px-2.5 py-2.5 text-center">
                      Amp Interno Clase D
                    </span>
                  </div>
                </div>

                <!-- Configuración de Power (Etapa de Potencia) para Tops Pasivos -->
                <div
                  v-if="batch.systemType === 'PASSIVE'"
                  class="mt-2.5 p-3 rounded-lg bg-[#111622] border border-cyan-800/80 grid grid-cols-1 sm:grid-cols-3 gap-2.5 font-mono text-xs"
                >
                  <div>
                    <label class="block text-[11px] font-bold text-cyan-300 mb-1">⚡ Power Tops (Etapa de Potencia)</label>
                    <input
                      v-model="batch.powerAmpModel"
                      @input="resetValidation"
                      type="text"
                      placeholder="Ej: Crown XLi 2500 / QSC RMX 2450"
                      class="w-full bg-[#0c1018] border border-cyan-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold text-cyan-300 mb-1">Watts RMS por Canal (del Power)</label>
                    <input
                      v-model.number="batch.powerAmpWatts"
                      @input="resetValidation"
                      type="number"
                      placeholder="Ej: 750"
                      class="w-full bg-[#0c1018] border border-cyan-700 rounded-lg px-2.5 py-1.5 text-xs text-cyan-200 focus:outline-none focus:border-cyan-400 font-bold"
                    />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold text-cyan-300 mb-1">Ubicación del Power</label>
                    <select
                      v-model="batch.powerAmpLocation"
                      @change="resetValidation"
                      class="w-full bg-[#0c1018] border border-cyan-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400 cursor-pointer"
                    >
                      <option value="DJ_BOOTH">Cabina DJ / Rack Técnico</option>
                      <option value="STAGE_RACK">Escenario (Cerca de cajas)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bloque B: Constructor por Lotes de Sub Bajos a Piso en Mono Cluster Central (S1, S2...) -->
          <div class="bg-[#15151c] border-2 border-zinc-800 rounded-2xl p-5 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="w-3.5 h-3.5 rounded-sm bg-purple-500"></span>
                <h3 class="text-base font-black text-white uppercase font-mono">
                  B. Lotes de Sub-Bajos a Piso (Mono Cluster Central)
                </h3>
                <InfoBadge
                  title="Sub Bajos Mixtos en Bloque Central"
                  simple-explanation="Combina subwoofers activos y pasivos indicando sus Watts RMS y Watts Peak. Todos se agrupan al centro en el suelo (< 1.7m entre sí, cero tubos extensores) para ganar +6 dB gratis."
                />
              </div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-mono bg-purple-950/70 text-purple-300 px-2.5 py-1 rounded border border-purple-800 font-bold">
                  Total Subs: {{ totalSubsCount }} bajos ({{ totalSubsRmsWatts }}W RMS / {{ totalSubsPeakWatts }}W Peak)
                </span>
                <button
                  type="button"
                  @click="addSubBatch"
                  class="px-3.5 py-1.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-mono font-black text-xs uppercase cursor-pointer transition shadow-md"
                >
                  + Agregar Lote de Sub-Bajos
                </button>
              </div>
            </div>

            <!-- Lista de Lotes de Sub-Bajos -->
            <div class="space-y-3">
              <div
                v-for="(batch, idx) in subBatches"
                :key="batch.id"
                class="p-4 rounded-xl bg-[#1c1c25] border-2 transition space-y-3"
                :class="batch.systemType === 'ACTIVE' ? 'border-purple-900/70' : 'border-cyan-700/70'"
              >
                <div class="flex flex-wrap items-center justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <span
                      class="text-[11px] font-mono font-black px-2.5 py-0.5 rounded uppercase"
                      :class="batch.systemType === 'ACTIVE' ? 'bg-purple-600 text-white' : 'bg-cyan-500 text-black'"
                    >
                      Lote Sub #{{ idx + 1 }} · {{ batch.systemType === 'ACTIVE' ? 'ACTIVO (PowerCon/IEC + XLR)' : 'PASIVO (Power + Speakon)' }}
                    </span>
                    <input
                      v-model="batch.modelLabel"
                      type="text"
                      placeholder="Nombre opcional (Ej: Sub 18 Activo / Sub Pasivo)"
                      class="bg-[#121218] border border-zinc-700 rounded-lg px-3 py-1 text-xs text-white font-mono focus:outline-none focus:border-purple-500"
                    />
                  </div>
                  <button
                    v-if="subBatches.length > 1"
                    type="button"
                    @click="removeSubBatch(idx)"
                    class="text-xs font-mono text-red-400 hover:text-red-300 bg-red-950/50 px-2.5 py-1 rounded border border-red-800 cursor-pointer"
                  >
                    🗑️ Quitar Lote
                  </button>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-6 gap-3">
                  <div>
                    <label class="block text-xs font-bold text-zinc-300 mb-1">Tecnología</label>
                    <select
                      v-model="batch.systemType"
                      @change="resetValidation"
                      class="w-full bg-[#121218] border border-zinc-700 rounded-lg px-2.5 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-purple-500 cursor-pointer"
                    >
                      <option value="ACTIVE">⚡ Activo</option>
                      <option value="PASSIVE">🔌 Pasivo</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-zinc-300 mb-1">Cantidad</label>
                    <input
                      v-model.number="batch.quantity"
                      @input="resetValidation"
                      type="number"
                      min="0"
                      max="12"
                      class="w-full bg-[#121218] border border-zinc-700 rounded-lg px-3 py-2.5 text-base text-white font-mono font-bold focus:outline-none focus:border-purple-500"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-zinc-300 mb-1">Cono (Pulgadas)</label>
                    <select
                      v-model.number="batch.coneSizeInches"
                      @change="resetValidation"
                      class="w-full bg-[#121218] border border-zinc-700 rounded-lg px-2.5 py-2.5 text-sm text-white font-mono focus:outline-none focus:border-purple-500 cursor-pointer"
                    >
                      <option :value="15">15" Pulgadas</option>
                      <option :value="18">18" Pulgadas</option>
                      <option :value="21">21" Pulgadas</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-emerald-300 mb-1">Watts RMS (c/u)</label>
                    <input
                      v-model.number="batch.rmsWatts"
                      @input="onBatchRmsChange(batch)"
                      type="number"
                      min="0"
                      max="6000"
                      placeholder="Ej: 800"
                      class="w-full bg-[#121218] border border-emerald-700 rounded-lg px-3 py-2.5 text-base text-emerald-300 font-mono font-bold focus:outline-none focus:border-emerald-400"
                    />
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-amber-300 mb-1">Watts Peak (c/u)</label>
                    <input
                      v-model.number="batch.peakWatts"
                      @input="resetValidation"
                      type="number"
                      min="0"
                      max="12000"
                      placeholder="Ej: 1600"
                      class="w-full bg-[#121218] border border-amber-700 rounded-lg px-3 py-2.5 text-base text-amber-300 font-mono font-bold focus:outline-none focus:border-amber-400"
                    />
                  </div>

                  <div v-if="batch.systemType === 'PASSIVE'">
                    <label class="block text-xs font-bold text-cyan-300 mb-1">Impedancia (Ω)</label>
                    <select
                      v-model.number="batch.impedanceOhms"
                      @change="resetValidation"
                      class="w-full bg-[#121218] border border-cyan-600 rounded-lg px-2.5 py-2.5 text-sm text-cyan-300 font-mono font-bold focus:outline-none focus:border-cyan-400 cursor-pointer"
                    >
                      <option :value="8">8 Ω (Estándar)</option>
                      <option :value="4">4 Ω (Alta Carga)</option>
                    </select>
                  </div>
                  <div v-else class="flex flex-col justify-end">
                    <span class="text-[11px] font-mono text-zinc-400 bg-[#121218] border border-zinc-800 rounded-lg px-2.5 py-2.5 text-center">
                      Amp Interno Clase D
                    </span>
                  </div>
                </div>

                <!-- Configuración de Power Subwoofer (Etapa de Graves) para Subs Pasivos -->
                <div
                  v-if="batch.systemType === 'PASSIVE'"
                  class="mt-2.5 p-3 rounded-lg bg-[#111622] border border-cyan-800/80 grid grid-cols-1 sm:grid-cols-3 gap-2.5 font-mono text-xs"
                >
                  <div>
                    <label class="block text-[11px] font-bold text-cyan-300 mb-1">⚡ Power Subwoofer (Etapa Graves)</label>
                    <input
                      v-model="batch.powerAmpModel"
                      @input="resetValidation"
                      type="text"
                      placeholder="Ej: Powersoft K10 / Crest Pro 9200"
                      class="w-full bg-[#0c1018] border border-cyan-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400"
                    />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold text-cyan-300 mb-1">Watts RMS por Canal (del Power Sub)</label>
                    <input
                      v-model.number="batch.powerAmpWatts"
                      @input="resetValidation"
                      type="number"
                      placeholder="Ej: 1500"
                      class="w-full bg-[#0c1018] border border-cyan-700 rounded-lg px-2.5 py-1.5 text-xs text-cyan-200 focus:outline-none focus:border-cyan-400 font-bold"
                    />
                  </div>
                  <div>
                    <label class="block text-[11px] font-bold text-cyan-300 mb-1">Ubicación & Conexión</label>
                    <select
                      v-model="batch.powerAmpLocation"
                      @change="resetValidation"
                      class="w-full bg-[#0c1018] border border-cyan-700 rounded-lg px-2.5 py-1.5 text-xs text-white focus:outline-none focus:border-cyan-400 cursor-pointer"
                    >
                      <option value="DJ_BOOTH">Cabina DJ (L1 Fuerza + Speakon NL4)</option>
                      <option value="STAGE_RACK">Rack Escenario (L1 Fuerza)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- HU06 / CU-05: CONSTRUCTOR DE ILUMINACIÓN, EFECTOS (HUMO/LÁSER) Y DMX -->
          <!-- ===================================================================== -->
          <div class="bg-[#0b0b10] border-2 border-fuchsia-800/70 rounded-2xl p-5 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 pb-3">
              <div>
                <h3 class="text-base font-black text-fuchsia-300 font-mono uppercase">
                  💡 Iluminación, Efectos (Humo / Láser) y Cableado Físico DMX
                </h3>
                <p class="text-xs text-zinc-400">
                  Suma los Watts reales al consumo total (Línea 3) y calcula cables DMX físicos saliendo desde <span class="text-fuchsia-300 font-mono font-bold">DMX OUT</span> en cabina.
                </p>
              </div>
              <div class="text-xs font-mono bg-fuchsia-950/60 border border-fuchsia-700 text-fuchsia-200 px-3 py-1.5 rounded-lg font-bold">
                {{ lightingDmxAnalysis.totalFixtureUnits }} eq. · {{ lightingDmxAnalysis.totalLightingWatts }}W · {{ lightingDmxAnalysis.totalDmxCablesCount }} cables DMX
              </div>
            </div>

            <!-- Botones rápidos de Presets de Iluminación / Humo y Personalizado -->
            <div class="space-y-2">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-[11px] font-mono uppercase text-zinc-400 font-bold">Presets Rápidos (Foco PAR = x1 Unidad):</span>
                <button
                  type="button"
                  @click="addCustomLighting"
                  class="px-3 py-1.5 rounded-lg text-xs font-mono font-black bg-fuchsia-600 hover:bg-fuchsia-500 text-white uppercase shadow-md transition cursor-pointer flex items-center gap-1.5"
                >
                  <span>✨</span>
                  <span>+ Agregar Equipo de Luz Personalizado</span>
                </button>
              </div>
              <div class="flex flex-wrap gap-1.5">
                <button
                  v-for="preset in lightingPresets"
                  :key="preset.key"
                  type="button"
                  @click="addLightingPreset(preset)"
                  class="px-2.5 py-1.5 rounded-lg text-xs font-mono font-bold border transition cursor-pointer"
                  :class="preset.isThermalLoad
                    ? 'bg-orange-950/60 hover:bg-orange-900 border-orange-600 text-orange-200'
                    : 'bg-zinc-900 hover:bg-fuchsia-950/70 border-zinc-700 hover:border-fuchsia-500 text-zinc-200'"
                  :title="preset.shortNote"
                >
                  + {{ preset.name }} ({{ preset.nominalWatts }}W)
                </button>
              </div>
              <p class="text-[11px] font-mono text-zinc-400 italic">
                ℹ️ Nota técnica: Los focos <strong>PAR LED</strong> se cuentan por <strong>unidad individual (x1)</strong> (PAR significa <em>Parabolic Aluminized Reflector</em>, no es que vengan en pares de 2).
              </p>
            </div>

            <!-- Lista editable de lotes de iluminación / humo -->
            <div v-if="lightingBatches.length === 0" class="text-xs font-mono text-zinc-500 bg-zinc-950 border border-dashed border-zinc-800 rounded-xl p-4 text-center">
              Sin luces ni máquinas de humo agregadas. Pulsa cualquier botón de arriba para sumar focos PAR, cabezas móviles, láser o máquina de humo.
            </div>

            <div v-else class="space-y-2.5">
              <div
                v-for="(lb, idx) in lightingBatches"
                :key="lb.id"
                class="bg-[#14141d] border rounded-xl p-3.5 space-y-3"
                :class="lb.isThermalLoad ? 'border-orange-600/80' : 'border-zinc-800'"
              >
                <div class="flex flex-wrap items-center justify-between gap-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-mono font-black px-2 py-0.5 rounded" :class="lb.isThermalLoad ? 'bg-orange-950 text-orange-300 border border-orange-600' : 'bg-fuchsia-950 text-fuchsia-300 border border-fuchsia-700'">
                      {{ lb.isThermalLoad ? '🔥 L3 TÉRMICA' : '💡 L3 LUCES' }}
                    </span>
                    <input
                      v-model="lb.name"
                      type="text"
                      class="bg-[#0c0c12] border border-zinc-700 rounded-lg px-2.5 py-1 text-sm text-white font-bold focus:outline-none focus:border-fuchsia-500"
                    />
                  </div>
                  <button
                    type="button"
                    @click="removeLightingBatch(idx)"
                    class="text-xs font-mono text-red-400 hover:text-red-300 px-2 py-1 rounded bg-red-950/40 border border-red-900 cursor-pointer"
                  >
                    ✕ Quitar
                  </button>
                </div>

                <div class="grid grid-cols-2 sm:grid-cols-5 gap-2.5">
                  <div>
                    <label class="block text-[11px] text-zinc-400 mb-1">Cantidad</label>
                    <input
                      v-model.number="lb.quantity"
                      type="number"
                      min="1"
                      max="32"
                      class="w-full bg-[#0c0c12] border border-zinc-700 rounded-lg px-2.5 py-2 text-sm text-white font-mono font-bold"
                    />
                  </div>
                  <div>
                    <label class="block text-[11px] text-amber-300 mb-1">Watts (c/u)</label>
                    <input
                      v-model.number="lb.nominalWatts"
                      type="number"
                      min="10"
                      max="5000"
                      class="w-full bg-[#0c0c12] border border-amber-700 rounded-lg px-2.5 py-2 text-sm text-amber-300 font-mono font-bold"
                    />
                  </div>
                  <div>
                    <label class="block text-[11px] text-zinc-400 mb-1">Ubicación Física</label>
                    <select
                      v-model="lb.zone"
                      class="w-full bg-[#0c0c12] border border-zinc-700 rounded-lg px-2 py-2 text-xs text-white font-mono cursor-pointer"
                    >
                      <option value="TRUSS_LEFT">Trípode / Truss Izq</option>
                      <option value="CENTER_BOOTH">Frente / Cabina</option>
                      <option value="TRUSS_RIGHT">Trípode / Truss Der</option>
                      <option value="FLOOR">Piso (Humo / FX)</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-[11px] text-fuchsia-300 mb-1">Cable DMX</label>
                    <select
                      v-model="lb.dmxConnector"
                      class="w-full bg-[#0c0c12] border border-fuchsia-700 rounded-lg px-2 py-2 text-xs text-fuchsia-200 font-mono cursor-pointer"
                    >
                      <option value="DMX_3PIN">DMX 3-Pin (Estándar)</option>
                      <option value="DMX_5PIN">DMX 5-Pin (Pro)</option>
                      <option value="NONE">Sin DMX (Manual/Auto)</option>
                    </select>
                  </div>
                  <div>
                    <label class="block text-[11px] text-zinc-400 mb-1">Peso c/u (kg)</label>
                    <input
                      v-model.number="lb.unitWeightKg"
                      type="number"
                      step="0.5"
                      min="0"
                      max="100"
                      class="w-full bg-[#0c0c12] border border-zinc-700 rounded-lg px-2.5 py-2 text-sm text-zinc-200 font-mono"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Alertas instantáneas de Humo / Láser / Conectores DMX -->
            <div v-if="lightingDmxAnalysis.alerts.length > 0" class="space-y-1.5">
              <div
                v-for="(al, i) in lightingDmxAnalysis.alerts"
                :key="`la-${i}`"
                class="text-xs font-mono bg-orange-950/50 border border-orange-600 text-orange-200 rounded-lg px-3 py-2"
              >
                {{ al }}
              </div>
            </div>
          </div>

          <!-- Innovación 2: Calculadora de Impedancia en Paralelo para Equipos Pasivos (Speakon Ohms) + Power Externo -->
          <div
            v-if="passiveImpedanceAudit.hasPassiveUnits || djSetupAnalysis.powerAmpsRequired.length > 0"
            class="p-5 rounded-2xl border-2 space-y-4 font-mono transition"
            :class="
              passiveImpedanceAudit.status === 'DANGER_PROTECT_SHORT'
                ? 'bg-red-950/50 border-red-500 text-red-100'
                : passiveImpedanceAudit.status === 'HIGH_LOAD_4_OHM'
                ? 'bg-amber-950/40 border-amber-500 text-amber-100'
                : 'bg-cyan-950/35 border-cyan-600 text-cyan-100'
            "
          >
            <div class="flex flex-wrap items-center justify-between gap-3">
              <div>
                <span class="text-xs font-black uppercase tracking-wider block">
                  🔌 Power Externo Requerido, Salidas Speakon y Conexión al Mixer (Unidades Pasivas)
                </span>
                <h4 class="text-sm sm:text-base font-black text-white mt-0.5">
                  Carga Mínima por Canal de Amplificador: {{ passiveImpedanceAudit.minImpedanceOhms ?? 8 }} Ω
                </h4>
              </div>
              <select
                v-model="passiveWiringMode"
                class="bg-[#121218] border-2 border-zinc-600 rounded-xl px-3 py-2 text-xs text-white font-mono font-bold cursor-pointer"
              >
                <option value="INDEPENDENT_CHANNELS">Modo Estéreo Independiente (Ch A / Ch B separados)</option>
                <option value="PARALLEL_SPEAKON_LINK">Modo Puente Paralelo (Speakon Link encadenado en 1 canal)</option>
              </select>
            </div>
            <p v-if="passiveImpedanceAudit.hasPassiveUnits" class="text-xs sm:text-sm leading-relaxed">{{ passiveImpedanceAudit.technicalDirective }}</p>
            <p v-if="passiveImpedanceAudit.hasPassiveUnits" class="text-xs opacity-90 border-t border-white/15 pt-2">🔧 {{ passiveImpedanceAudit.speakonRoutingNote }}</p>

            <!-- Tarjetas desplegadas automáticamente por cada Power requerido (Tops Pasivos / Subs Pasivos / Retorno Pasivo) -->
            <div v-if="djSetupAnalysis.powerAmpsRequired.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 border-t border-white/15">
              <div
                v-for="amp in djSetupAnalysis.powerAmpsRequired"
                :key="amp.id"
                class="bg-[#0e1218] border border-cyan-700/70 rounded-xl p-3.5 space-y-1.5 text-xs"
              >
                <div class="flex items-center justify-between gap-2">
                  <span class="font-black text-cyan-300">{{ amp.title }}</span>
                  <span class="px-2 py-0.5 rounded bg-cyan-950 text-cyan-200 border border-cyan-700 font-black">
                    {{ amp.recommendedAmpWattsPerChannel }}W/ch @ {{ amp.loadImpedanceOhms }}Ω
                  </span>
                </div>
                <div class="text-zinc-300"><strong>Entradas Power:</strong> {{ amp.requiredInputs }}</div>
                <div class="text-zinc-300"><strong>Salidas Power:</strong> {{ amp.requiredOutputs }} ({{ amp.recommendedMinChannels }} canal/es)</div>
                <div class="text-amber-300 bg-black/40 border border-zinc-800 rounded p-2">
                  <strong>🔗 Conexión al Mixer:</strong> {{ amp.mixerConnectionChain }}
                </div>
              </div>
            </div>
          </div>

          <!-- ===================================================================== -->
          <!-- SETUP CABINA DJ (CDJ/XDJ + LINK ETHERNET) Y CAJAS DE RETORNO (BOOTH)  -->
          <!-- ===================================================================== -->
          <div class="bg-[#0e1116] border-2 border-cyan-800/70 rounded-2xl p-5 space-y-4 font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
              <div>
                <h3 class="text-base font-black text-cyan-300 uppercase">
                  🎛️ Cabina DJ (CDJ / XDJ + Link Ethernet) y Cajas de Retorno (Booth)
                </h3>
                <p class="text-xs text-zinc-400">
                  Calcula cables RCA/Coaxial, cables Ethernet RJ45 (y Switch si usas 3–4 CDJs), salidas BOOTH TRS y alimentación en Z1.
                </p>
              </div>
              <span class="text-xs bg-cyan-950 border border-cyan-700 text-cyan-200 px-3 py-1 rounded-lg font-bold">
                Cabina + Retorno: {{ djSetupAnalysis.djBoothTotal220vWatts + djSetupAnalysis.boothMonitorsTotal220vWatts }}W
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Panel Izquierdo: CDJs / XDJs / Mixer -->
              <div class="bg-[#141822] border border-zinc-800 rounded-xl p-4 space-y-3 text-xs">
                <div class="font-black text-white uppercase">1. Reproductores y Mixer DJ</div>
                <div class="grid grid-cols-2 gap-2.5">
                  <div>
                    <label class="block text-[11px] text-zinc-400 mb-1">Tipo de Setup</label>
                    <select
                      v-model="djSetup.setupMode"
                      @change="if (djSetup.setupMode === 'ALL_IN_ONE_CONTROLLER') djSetup.playerCount = 0; else if (djSetup.playerCount === 0) djSetup.playerCount = 2; resetValidation();"
                      class="w-full bg-[#0b0d12] border border-zinc-700 rounded-lg px-2 py-2 text-white font-bold cursor-pointer"
                    >
                      <option value="CDJ_XDJ_MODULAR">Mixer + CDJ / XDJ</option>
                      <option value="ALL_IN_ONE_CONTROLLER">Controladora All-in-One</option>
                    </select>
                  </div>
                  <div v-if="djSetup.setupMode === 'CDJ_XDJ_MODULAR'">
                    <label class="block text-[11px] text-cyan-300 mb-1">Cantidad CDJ / XDJ</label>
                    <select
                      v-model.number="djSetup.playerCount"
                      @change="resetValidation"
                      class="w-full bg-[#0b0d12] border border-cyan-700 rounded-lg px-2 py-2 text-cyan-200 font-bold cursor-pointer"
                    >
                      <option :value="2">2× CDJ / XDJ</option>
                      <option :value="3">3× CDJ / XDJ (Switch)</option>
                      <option :value="4">4× CDJ / XDJ (Switch)</option>
                    </select>
                  </div>
                </div>

                <div v-if="djSetup.setupMode === 'CDJ_XDJ_MODULAR'" class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  <div>
                    <label class="block text-[11px] text-zinc-400 mb-1">Audio CDJ → Mixer</label>
                    <select
                      v-model="djSetup.playerAudioLinkType"
                      class="w-full bg-[#0b0d12] border border-zinc-700 rounded-lg px-2 py-2 text-white cursor-pointer"
                    >
                      <option value="RCA_ANALOG">RCA Estéreo (CH LINE/CD)</option>
                      <option value="DIGITAL_COAXIAL">Digital Coaxial (S/PDIF)</option>
                    </select>
                  </div>
                  <div class="flex flex-col justify-center space-y-1.5 pt-1">
                    <label class="flex items-center gap-2 cursor-pointer text-zinc-200">
                      <input type="checkbox" v-model="djSetup.linkEthernetProDj" class="accent-cyan-500 cursor-pointer" />
                      <span>Linkear con Ethernet RJ45</span>
                    </label>
                    <label v-if="djSetup.linkEthernetProDj" class="flex items-center gap-2 cursor-pointer text-zinc-300">
                      <input type="checkbox" v-model="djSetup.linkMixerToEthernet" class="accent-cyan-500 cursor-pointer" />
                      <span>Incluir puerto LINK del Mixer</span>
                    </label>
                  </div>
                </div>

                <div v-if="djSetup.setupMode === 'CDJ_XDJ_MODULAR'" class="bg-black/40 border border-zinc-800 rounded-lg p-2.5 text-[11px] text-cyan-200">
                  🌐 Red Pro DJ Link: <strong>{{ djSetupAnalysis.ethernetCablesCount }} cable(s) Ethernet RJ45</strong>
                  <span v-if="djSetupAnalysis.requiresEthernetSwitch" class="text-amber-300 font-bold"> + Switch Ethernet 5 puertos OBLIGATORIO</span>
                  <span v-else-if="djSetupAnalysis.ethernetCablesCount > 0"> (conexión directa entre 2 equipos)</span>
                </div>
              </div>

              <!-- Panel Derecho: Cajas de Retorno (Booth Monitor) -->
              <div class="bg-[#141822] border border-zinc-800 rounded-xl p-4 space-y-3 text-xs">
                <div class="font-black text-white uppercase">2. Cajas de Retorno (Booth Monitor DJ)</div>
                <div class="grid grid-cols-3 gap-2">
                  <div>
                    <label class="block text-[11px] text-zinc-400 mb-1">Cantidad</label>
                    <select
                      v-model.number="djSetup.boothMonitorsCount"
                      @change="resetValidation"
                      class="w-full bg-[#0b0d12] border border-zinc-700 rounded-lg px-2 py-2 text-white font-bold cursor-pointer"
                    >
                      <option :value="0">0 (Sin retorno)</option>
                      <option :value="1">1× Retorno (Mono)</option>
                      <option :value="2">2× Retornos (L/R)</option>
                    </select>
                  </div>
                  <div v-if="djSetup.boothMonitorsCount > 0">
                    <label class="block text-[11px] text-zinc-400 mb-1">Tipo</label>
                    <select
                      v-model="djSetup.boothMonitorType"
                      @change="resetValidation"
                      class="w-full bg-[#0b0d12] border border-zinc-700 rounded-lg px-2 py-2 text-white font-bold cursor-pointer"
                    >
                      <option value="ACTIVE">⚡ Activo</option>
                      <option value="PASSIVE">🔌 Pasivo (Power)</option>
                    </select>
                  </div>
                  <div v-if="djSetup.boothMonitorsCount > 0">
                    <label class="block text-[11px] text-emerald-300 mb-1">Watts RMS c/u</label>
                    <input
                      v-model.number="djSetup.boothMonitorRmsWatts"
                      type="number"
                      min="100"
                      max="2000"
                      class="w-full bg-[#0b0d12] border border-emerald-700 rounded-lg px-2 py-2 text-emerald-300 font-bold"
                    />
                  </div>
                </div>
                <div v-if="djSetup.boothMonitorsCount > 0" class="bg-black/40 border border-zinc-800 rounded-lg p-2.5 text-[11px] text-zinc-300">
                  🎛️ Conexión desde Mixer: <strong class="text-amber-300">BOOTH OUT (Jack TRS 6.3mm)</strong> → {{ djSetup.boothMonitorsCount }}× cable TRS a XLR Macho
                  <span v-if="djSetup.boothMonitorType === 'PASSIVE'" class="text-cyan-300"> → Power Retorno → Speakon NL4</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Bloque C: Fuente de Energía y Régimen de Volumen -->
          <div class="bg-[#15151c] border-2 border-zinc-800 rounded-2xl p-5 space-y-5">
            <div>
              <label class="block text-base font-bold text-white mb-2 flex items-center gap-2">
                <span>⚡ ¿De dónde sacarás la electricidad?</span>
                <InfoBadge
                  title="Enchufe de Casa vs Generador (Derating Real)"
                  simple-explanation="Un enchufe común de 10A soporta 1.760W continuos seguros (80%). Un generador comercial rotulado como '3500 Watts' entrega solo ~2.140W seguros para audio (72% AVR) porque el golpe del bajo frena el motor."
                />
              </label>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <select
                  v-model="powerSource.type"
                  @change="resetValidation"
                  class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-base text-white focus:outline-none focus:border-red-500 cursor-pointer"
                >
                  <option value="GRID_220V">🔌 Enchufe de Casa / Salón (Red 220V)</option>
                  <option value="GENERATOR_WATTS">⛽ Generador en Watts (Ej: 3500 W)</option>
                  <option value="GENERATOR_KVA">🏭 Generador Industrial en kVA (Ej: 5 kVA)</option>
                </select>

                <div v-if="powerSource.type === 'GRID_220V'">
                  <select
                    v-model="powerSource.circuitBreakerAmps"
                    @change="resetValidation"
                    class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-base text-white focus:outline-none focus:border-red-500 cursor-pointer"
                  >
                    <option value="10">Enchufe Casa 10 A (2.200W máx · 1.760W seguros)</option>
                    <option value="16">Enchufe Fuerza 16 A (3.520W máx · 2.816W seguros)</option>
                    <option value="20">Automático Industrial 20 A (3.520W seguros)</option>
                    <option value="25">Automático Industrial 25 A (4.400W seguros)</option>
                  </select>
                </div>

                <div v-else-if="powerSource.type === 'GENERATOR_WATTS'">
                  <input
                    v-model.number="powerSource.generatorSurgeWatts"
                    @input="resetValidation"
                    type="number"
                    inputmode="numeric"
                    placeholder="Watts del generador (Ej: 3500)"
                    class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white font-mono focus:outline-none focus:border-red-500"
                  />
                </div>

                <div v-else>
                  <input
                    v-model.number="powerSource.apparentPowerKva"
                    @input="resetValidation"
                    type="number"
                    inputmode="numeric"
                    placeholder="Potencia en kVA (Ej: 5)"
                    class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-lg text-white font-mono focus:outline-none focus:border-red-500"
                  />
                </div>
              </div>
            </div>

            <div>
              <label class="block text-base font-bold text-white mb-2 flex items-center gap-2">
                <span>🔊 ¿A qué nivel de exigencia trabajará el sonido?</span>
                <InfoBadge
                  title="Consumo No Lineal y Compresión Térmica"
                  simple-explanation="Al máximo volumen en Techno, el consumo eléctrico se triplica y el 97% de la energía calienta la bobina (150–220 °C), perdiendo ~3.2 dB por compresión térmica."
                />
              </label>
              <select
                v-model="powerSource.driveRegime"
                @change="resetValidation"
                class="w-full bg-[#1c1c24] border-2 border-zinc-700 rounded-xl px-4 py-3.5 text-base text-white focus:outline-none focus:border-red-500 cursor-pointer"
              >
                <option value="MAX_TECHNO_1_3">🔥 Aprovechamiento Máximo Rave/Techno (1/3 RMS continuo · Picos x5)</option>
                <option value="STANDARD_CLUB_1_5">⚡ Volumen Pista Estándar Sin Clip (1/5 RMS continuo · Alta dinámica)</option>
                <option value="MODERATE_1_8">🟢 Volumen Moderado / Warm-Up (1/8 RMS continuo · Bajo consumo)</option>
              </select>
            </div>
          </div>

          <!-- Mensaje de Error si faltan campos -->
          <div
            v-if="validationMessage && !isValidated"
            class="p-4 rounded-xl bg-amber-950/50 border-2 border-amber-500 text-amber-200 text-base flex items-start gap-3"
          >
            <span class="text-xl">⚠️</span>
            <div>
              <p class="font-bold">Revisa estos datos antes de continuar:</p>
              <p class="text-sm mt-1">{{ validationMessage }}</p>
            </div>
          </div>

          <!-- Botones de Acción Paso 2 -> Paso 3 -->
          <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-zinc-800">
            <button
              @click="goToStep(1)"
              class="px-5 py-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 font-mono font-bold text-sm cursor-pointer transition"
            >
              ← Volver a Medidas (Paso 1)
            </button>

            <button
              @click="validateAndGoToSimulation"
              class="flex-1 sm:flex-initial px-8 py-4 rounded-xl bg-red-600 hover:bg-red-500 text-white font-black text-base uppercase tracking-wider font-mono shadow-2xl shadow-red-950/80 cursor-pointer transition active:scale-[0.99]"
            >
              ⚡ Confirmar Equipos y Abrir Plano 2D (Paso 3) →
            </button>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VISTA 3: PLANO 2D INTELIGENTE (PANTALLA ANCHA) & SIMULADOR MIXER DJM  -->
      <!-- ===================================================================== -->
      <section v-else-if="currentStep === 3" class="space-y-8">
        <!-- Encabezado de Vista 3 -->
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-5 flex flex-wrap items-center justify-between gap-3">
          <div>
            <span class="text-xs font-mono text-red-400 font-bold uppercase block">[ PASO 3 DE 4 · ESTUDIO ACÚSTICO Y ESPACIAL ]</span>
            <h2 class="text-xl font-black text-white font-mono uppercase">
              Plano 2D Mixto, Mapa de Calor SPL y Calibración DJM
            </h2>
          </div>
          <span
            class="text-xs font-mono font-bold px-3 py-1.5 rounded-xl border-2"
            :class="stageAcousticResult.tonalBalance.status === 'OPTIMAL' ? 'bg-emerald-950 border-emerald-600 text-emerald-300' : 'bg-amber-950 border-amber-600 text-amber-300'"
          >
            BALANCE TONAL SUB/TOP: {{ stageAcousticResult.tonalBalance.status }} (+{{ stageAcousticResult.tonalBalance.subToTopRatioDb }} dB)
          </span>
        </div>

        <!-- Plano 2D en Gran Formato con soporte para Nodos Mixtos, Cableado, Zapatillas y DMX -->
        <LayoutSvg2D
          :venue-width="venue.widthMeters || 10"
          :venue-depth="venue.depthMeters || 16"
          :subs-count="totalSubsCount"
          :tops-count="totalTopsCount"
          :roster-nodes="hybridAnalysis.roster"
          :power-plan="powerDistributionPlan"
          :lighting-analysis="lightingDmxAnalysis"
        />

        <!-- Tarjeta Informativa de Ingeniería: Postes Guía y Radio de Curvatura SEC -->
        <div class="bg-[#0b111a] border-2 border-sky-700/80 rounded-2xl p-4 sm:p-5 font-mono text-xs space-y-2.5">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-sky-900 pb-2">
            <span class="text-sky-400 font-black uppercase flex items-center gap-1.5">
              <span>📍</span>
              <span>Soportes de Esquina y Radio de Curvatura (SEC Pliego RIC N° 10)</span>
            </span>
            <span class="bg-sky-950 border border-sky-600 text-sky-200 px-2 py-0.5 rounded text-[11px] font-bold">
              Norma Chilena SEC / IEC 60364
            </span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-zinc-300 leading-relaxed text-[11px]">
            <div class="space-y-1">
              <strong class="text-sky-300 block text-xs">¿Cómo se llaman industrialmente y para qué sirven?</strong>
              <p>
                En eventos profesionales, en las esquinas y aristas del trazado perimetral se instalan <strong>Postes Guía Pasacables (Tótems de amarre / Drop Poles)</strong> si el tendido va perimetral elevado, o <strong>Pasacables Esquineros a 90° (Codos pasacables)</strong> si va por el suelo. Sirven para dar el radio de doblez suave al cable, evitando que quede tirante o expuesto a machacamiento.
              </p>
            </div>
            <div class="space-y-1">
              <strong class="text-amber-300 block text-xs">Exigencia SEC RIC N° 10 (Radio de Curvatura R ≥ 6d):</strong>
              <p>
                Los conductores flexibles de fuerza clase 5 exigen un radio de doblado mínimo de <strong>6 veces su diámetro exterior</strong>. Un quiebre en punta viva corta los microfilamentos de cobre internos, estrangula la chaqueta de aislación y provoca puntos calientes por resistencia de contacto.
              </p>
            </div>
          </div>
        </div>

        <!-- Diagnóstico Innovador: Cuello de Botella Acústico & Ordenanza de Ruido D.S. N°38 MMA -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Innovación 4: Detector de Balance Sub-to-Top -->
          <div
            class="p-5 rounded-2xl border-2 space-y-2 font-mono transition"
            :class="
              topSubBottleneck.status === 'OPTIMAL_CLUB_BALANCE'
                ? 'bg-emerald-950/40 border-emerald-600 text-emerald-100'
                : topSubBottleneck.status === 'SUB_BASS_DEFICIT'
                ? 'bg-amber-950/40 border-amber-500 text-amber-100'
                : 'bg-cyan-950/40 border-cyan-500 text-cyan-100'
            "
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-black uppercase text-amber-300">⚖️ Balance Tonal Sub vs Top</span>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-black/40 border border-white/20">
                {{ topSubBottleneck.subEnergySharePct }}% Graves / {{ topSubBottleneck.topEnergySharePct }}% Agudos
              </span>
            </div>
            <p class="text-xs sm:text-sm leading-relaxed">{{ topSubBottleneck.bottleneckDiagnosis }}</p>
          </div>

          <!-- Innovación 5: Diagnóstico Vecinal D.S. N°38 -->
          <div
            class="p-5 rounded-2xl border-2 space-y-2 font-mono transition"
            :class="
              neighborhoodNoiseAudit.status === 'COMPLIANT_SAFE'
                ? 'bg-emerald-950/40 border-emerald-600 text-emerald-100'
                : neighborhoodNoiseAudit.status === 'BORDERLINE_CAUTION'
                ? 'bg-amber-950/40 border-amber-500 text-amber-100'
                : 'bg-red-950/50 border-red-600 text-red-100'
            "
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-black uppercase text-red-300">🏘️ Ordenanza Ruido (D.S. N° 38 MMA)</span>
              <span class="text-[11px] font-bold px-2 py-0.5 rounded bg-black/40 border border-white/20">
                ~{{ neighborhoodNoiseAudit.estimatedNeighborDba }} dBA @ {{ neighborhoodNoiseAudit.neighborDistanceM }}m
              </span>
            </div>
            <p class="text-xs sm:text-sm leading-relaxed">{{ neighborhoodNoiseAudit.mitigationDirective }}</p>
          </div>
        </div>

        <!-- Métricas de Presión Sonora SPL y Tiempo de Delay Haas -->
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-6 shadow-2xl space-y-5">
          <div class="flex items-center justify-between border-b border-zinc-800 pb-3">
            <h3 class="text-base font-black text-white uppercase font-mono flex items-center gap-2">
              🔊 Presión Sonora (SPL) por Zona y Alineación Temporal (Efecto Haas)
            </h3>
            <InfoBadge
              title="Cómo leer los Decibeles (SPL)"
              simple-explanation="Muestra qué tan fuerte se escucha a 1 metro, en la primera fila (4m) y al fondo del salón. Gracias a las Torres de Delay, el fondo mantiene más de 100 dBA sin reventar los oídos de adelante."
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
            <div class="bg-[#16161e] p-5 rounded-2xl border-2 border-zinc-800">
              <span class="text-zinc-400 block text-sm font-bold mb-1">Frente Escenario (1m)</span>
              <span class="text-2xl sm:text-3xl font-black text-white font-mono">{{ stageAcousticResult.frontSystem.spl1mPeak }} dB Peak</span>
              <span class="text-xs text-zinc-400 block font-mono mt-1">Continuo: {{ stageAcousticResult.frontSystem.spl1mContinuous }} dB SPL</span>
            </div>

            <div class="bg-[#16161e] p-5 rounded-2xl border-2 border-emerald-800/70">
              <span class="text-emerald-300 block text-sm font-bold mb-1">Primera Fila (4 metros)</span>
              <span class="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">
                {{ stageAcousticResult.frontSystem.splAtDistances[1] ? stageAcousticResult.frontSystem.splAtDistances[1].splPeak : 0 }} dB Peak
              </span>
              <span class="text-xs text-emerald-300/80 block font-mono mt-1">Zona de Pegada Limpia</span>
            </div>

            <div class="bg-[#16161e] p-5 rounded-2xl border-2 border-red-800/70">
              <span class="text-red-300 block text-sm font-bold mb-1">Fondo de Pista ({{ venue.depthMeters }}m)</span>
              <span class="text-2xl sm:text-3xl font-black text-red-400 font-mono">
                {{ stageAcousticResult.frontSystem.splAtDistances.length > 0 ? stageAcousticResult.frontSystem.splAtDistances[stageAcousticResult.frontSystem.splAtDistances.length - 1].splPeak : 0 }} dB Peak
              </span>
              <span class="text-xs text-zinc-300 block font-mono mt-1">
                Sensación continua (LAeq): {{ stageAcousticResult.frontSystem.splAtDistances.length > 0 ? stageAcousticResult.frontSystem.splAtDistances[stageAcousticResult.frontSystem.splAtDistances.length - 1].splAeq : 0 }} dBA
              </span>
            </div>
          </div>

          <div class="p-4 bg-[#15151d] border border-zinc-700 rounded-xl space-y-2 text-sm font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="text-zinc-200 font-bold">⏱️ Retardo de Línea de Refuerzo (Delay + Efecto Haas):</span>
              <span
                class="font-black px-3 py-1 rounded text-xs"
                :class="stageAcousticResult.delayLineRecommendation.required ? 'bg-amber-950 text-amber-300 border border-amber-600' : 'bg-zinc-800 text-zinc-300'"
              >
                {{ stageAcousticResult.delayLineRecommendation.required ? `${stageAcousticResult.delayLineRecommendation.totalDelayMs} ms CALIBRADO` : 'NO REQUERIDO (PISTA CORTA)' }}
              </span>
            </div>
            <p v-if="stageAcousticResult.delayLineRecommendation.required" class="text-zinc-300 text-xs leading-relaxed">
              • Tiempo de vuelo físico: {{ stageAcousticResult.delayLineRecommendation.delayTimeMs }} ms a {{ stageAcousticResult.delayLineRecommendation.triggerDistanceM }}m + <strong>{{ stageAcousticResult.delayLineRecommendation.haasCompensationMs }} ms (Efecto Haas)</strong> para que el cerebro ubique el sonido en el DJ.
            </p>
            <div v-if="venue.environmentType === 'INDOOR' && stageAcousticResult.frontSystem.reverberationTimeRt60Seconds" class="pt-2 border-t border-zinc-800 flex items-center justify-between text-xs text-zinc-300">
              <span>Tiempo de Reverberación del Salón (Eco RT60 Sabine):</span>
              <span class="text-white font-bold">{{ stageAcousticResult.frontSystem.reverberationTimeRt60Seconds }} segundos</span>
            </div>
          </div>
        </div>

        <!-- Consola Interactiva de Ganancia y Simulador de Vúmetros DJM -->
        <div class="p-6 bg-gradient-to-r from-red-950/40 via-[#111116] to-[#111116] border-2 border-red-700/80 rounded-2xl space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <h3 class="text-base font-black uppercase tracking-wider text-red-400 font-mono">
              🎛️ Guía Anti-Saturación y Simulador de Vúmetros Mixer DJM
            </h3>
            <span class="text-xs font-mono bg-red-950 text-red-200 px-3 py-1 rounded border border-red-700">
              Cero Clip / Cero Chicharreo (+4 a +7 dBu)
            </span>
          </div>

          <p class="text-sm text-zinc-200 leading-relaxed">
            {{ hybridAnalysis.placementStrategySummary }}
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
            <div class="bg-[#14141b] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex items-center justify-between">
                <span class="text-amber-400 font-bold text-sm">1. Canal (Trim) + Fader</span>
                <span class="bg-amber-950 text-amber-300 px-2 py-0.5 rounded border border-amber-700">+3 a +6 dB (Ámbar)</span>
              </div>
              <p class="text-zinc-300 leading-relaxed">
                <strong>Fader al tope (10)</strong>. Ajusta el <strong>Trim</strong> en el drop hasta encender 1–2 LEDs ámbar (+3 a +6 dB). <strong>Jamás tocar rojo (+10 dB)</strong>.
              </p>
            </div>

            <div class="bg-[#14141b] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex items-center justify-between">
                <span class="text-emerald-400 font-bold text-sm">2. Master Mixer (XLR)</span>
                <span class="bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-700">0 a +3 dB (+4/+7 dBu)</span>
              </div>
              <p class="text-zinc-300 leading-relaxed">
                Promediar en <strong>0 dB</strong> con picos del kick en <strong>+3 dB</strong>. En rojo (+10 dB) el limitador aplasta el golpe y recalienta bobinas.
              </p>
            </div>
          </div>

          <!-- SIMULADOR PROFESIONAL HARDWARE REPLICA PIONEER DJM (GAIN STAGING, VÚMETROS VERTICALES Y LOW BASS SWAP) -->
          <PioneerMixerSimulator />

          <!-- HU08 / CU-07: SIMULADOR PLAN B (CONTINGENCIA EN VIVO) -->
          <div class="bg-[#0e0c10] border-2 border-red-700/80 rounded-2xl p-5 space-y-4 font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
              <div>
                <span class="text-[11px] text-red-400 font-black uppercase block">🚨 MODO CONTINGENCIA EN VIVO (HU08 / CU-07)</span>
                <h3 class="text-base font-black text-white uppercase">Simulador "Plan B" ante Falla en Plena Fiesta</h3>
              </div>
              <span class="text-xs text-zinc-400">Protocolo de recuperación en &lt; 2 minutos</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
              <button
                type="button"
                @click="activeContingencyScenario = 'GENERATOR_FAIL_TO_10A'"
                class="px-3 py-2.5 rounded-xl text-xs font-black border text-left transition cursor-pointer"
                :class="activeContingencyScenario === 'GENERATOR_FAIL_TO_10A' ? 'bg-red-600 text-white border-red-400' : 'bg-zinc-900 text-zinc-300 border-zinc-700 hover:border-red-500'"
              >
                ⚡ Murió Generador → 10A
              </button>
              <button
                type="button"
                @click="activeContingencyScenario = 'TOP_BOX_FAILURE'"
                class="px-3 py-2.5 rounded-xl text-xs font-black border text-left transition cursor-pointer"
                :class="activeContingencyScenario === 'TOP_BOX_FAILURE' ? 'bg-red-600 text-white border-red-400' : 'bg-zinc-900 text-zinc-300 border-zinc-700 hover:border-red-500'"
              >
                🔊 Falló 1 Caja Top Frontal
              </button>
              <button
                type="button"
                @click="activeContingencyScenario = 'SUB_FAILURE'"
                class="px-3 py-2.5 rounded-xl text-xs font-black border text-left transition cursor-pointer"
                :class="activeContingencyScenario === 'SUB_FAILURE' ? 'bg-red-600 text-white border-red-400' : 'bg-zinc-900 text-zinc-300 border-zinc-700 hover:border-red-500'"
              >
                🔈 Falló 1 Subwoofer
              </button>
              <button
                type="button"
                @click="activeContingencyScenario = 'LIGHTING_BREAKER_TRIP'"
                class="px-3 py-2.5 rounded-xl text-xs font-black border text-left transition cursor-pointer"
                :class="activeContingencyScenario === 'LIGHTING_BREAKER_TRIP' ? 'bg-red-600 text-white border-red-400' : 'bg-zinc-900 text-zinc-300 border-zinc-700 hover:border-red-500'"
              >
                🔥 Saltó Automático L3 Humo
              </button>
            </div>

            <div v-if="contingencyPlan" class="bg-[#161218] border border-red-900/70 rounded-xl p-4 space-y-3">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-sm font-black text-red-300">{{ contingencyPlan.title }}</span>
                <span
                  class="text-xs font-black px-2.5 py-1 rounded-lg border"
                  :class="contingencyPlan.isSystemSurvivable ? 'bg-emerald-950 border-emerald-500 text-emerald-300' : 'bg-red-950 border-red-500 text-red-200'"
                >
                  {{ contingencyPlan.initialWatts }}W → {{ contingencyPlan.resultingWatts }}W
                </span>
              </div>
              <ol class="space-y-2 text-xs">
                <li v-for="st in contingencyPlan.steps" :key="st.order" class="bg-black/40 border border-zinc-800 rounded-lg p-2.5">
                  <div class="flex items-center justify-between gap-2">
                    <span class="text-white font-bold">{{ st.order }}. {{ st.action }}</span>
                    <span v-if="st.wattsSaved" class="text-emerald-400 font-black shrink-0">-{{ st.wattsSaved }}W</span>
                  </div>
                  <div class="text-zinc-400 mt-0.5">{{ st.reason }}</div>
                </li>
              </ol>
              <div class="text-xs bg-amber-950/40 border border-amber-700/70 text-amber-200 rounded-lg p-2.5">
                <strong>🎛️ Directriz Mixer:</strong> {{ contingencyPlan.mixerDirective }}
              </div>
              <p class="text-xs text-emerald-300 font-bold">{{ contingencyPlan.recoverySummary }}</p>
            </div>
          </div>

          <!-- Navegación Paso 3 -> Paso 4 -->
          <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-zinc-800">
            <button
              @click="goToStep(2)"
              class="px-5 py-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 font-mono font-bold text-sm cursor-pointer transition"
            >
              ← Volver a Equipos (Paso 2)
            </button>
            <button
              @click="goToStep(4)"
              class="px-8 py-4 rounded-xl bg-red-600 hover:bg-red-500 text-white font-black text-base uppercase tracking-wider font-mono shadow-2xl shadow-red-950/80 cursor-pointer transition"
            >
              Ir al Reporte Final, Camioneta y PDF (Paso 4) →
            </button>
          </div>
        </div>
      </section>

      <!-- ===================================================================== -->
      <!-- VISTA 4: REPORTE EJECUTIVO FINAL, CAMIONETA, 7 REGLAS Y DESCARGA PDF  -->
      <!-- ===================================================================== -->
      <section v-else-if="currentStep === 4" class="space-y-8">
        <!-- Banner de Descarga Oficial PDF + Firma del Operador -->
        <div class="bg-gradient-to-r from-red-950/70 via-[#121218] to-[#121218] border-2 border-red-600 rounded-2xl p-6 shadow-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="space-y-1">
            <span class="text-xs font-mono font-black uppercase text-red-400">
              [ PASO 4 DE 4 · HOJA DE RUTA LISTA PARA TERRENO ]
            </span>
            <h2 class="text-xl sm:text-2xl font-black text-white font-mono uppercase">
              Reporte Operativo: {{ venue.name }}
            </h2>
            <p class="text-sm text-zinc-300 font-mono">
              Responsable: <strong>{{ operatorSignature }}</strong> | Superficie: {{ (venue.widthMeters || 0) * (venue.depthMeters || 0) }} m²
            </p>
          </div>

          <div class="flex flex-col sm:flex-row gap-2.5 w-full sm:w-auto">
            <button
              @click="copyWhatsAppSummary"
              class="w-full sm:w-auto px-5 py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-sm uppercase tracking-wider font-mono shadow-xl shadow-emerald-950/60 cursor-pointer transition active:scale-95 flex items-center justify-center gap-2"
            >
              <span>{{ whatsappCopied ? '✅ ¡Copiado para WhatsApp!' : '💬 Copiar Resumen WhatsApp' }}</span>
            </button>
            <button
              @click="downloadPdf"
              class="w-full sm:w-auto px-7 py-4 rounded-xl bg-red-600 hover:bg-red-500 text-white font-black text-base uppercase tracking-wider font-mono shadow-2xl shadow-red-600/40 cursor-pointer transition active:scale-95 flex items-center justify-center gap-2 shrink-0"
            >
              <span>📄 Descargar Reporte PDF (Modo Avión)</span>
            </button>
          </div>
        </div>

        <!-- Innovación 1: Separación Automática en 2 Líneas Eléctricas (Línea 1 Subs / Línea 2 Tops+Cabina) -->
        <div class="bg-[#121219] border-2 border-red-700/80 rounded-2xl p-5 space-y-3 font-mono shadow-xl">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-2.5">
            <h3 class="text-sm sm:text-base font-black uppercase text-red-400 flex items-center gap-2">
              <span>⚡ División por Líneas Eléctricas (Anti-Derretimiento de Enchufes)</span>
              <InfoBadge
                title="Separación de Fases y Cables de Fuerza"
                simple-explanation="Para que el golpe de los subwoofers no bote la consola ni sobrecaliente un solo alargador, la app separa el evento en 2 líneas eléctricas independientes."
              />
            </h3>
            <span class="text-xs text-zinc-300 bg-zinc-900 px-2.5 py-1 rounded border border-zinc-700">
              Total Sistema: {{ powerFeasibility.totalSystemDemandWatts }}W
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div class="p-3.5 rounded-xl bg-[#181822] border border-purple-800/80 space-y-1">
              <span class="text-purple-400 font-bold block text-sm">LÍNEA 1: Fuerza Sub-Graves (Piso)</span>
              <p class="text-white font-black text-base">
                {{ hybridAnalysis.electricalLines.line1SubsWatts }} W continuos · {{ hybridAnalysis.electricalLines.line1SubsAmps }} A
                <span class="text-xs text-zinc-400 block font-normal">(Picos transitorios de {{ hybridAnalysis.electricalLines.line1SubsPeakWatts }} W)</span>
              </p>
              <p class="text-zinc-300 text-[11px] leading-relaxed">
                Exclusiva para subwoofers activos y amplificadores de sub graves pasivos.
              </p>
            </div>

            <div class="p-3.5 rounded-xl bg-[#181822] border border-red-800/80 space-y-1">
              <span class="text-red-400 font-bold block text-sm">LÍNEA 2: Medios/Agudos + Cabina DJ</span>
              <p class="text-white font-black text-base">
                {{ hybridAnalysis.electricalLines.line2TopsCtrlWatts }} W continuos · {{ hybridAnalysis.electricalLines.line2TopsCtrlAmps }} A
                <span class="text-xs text-zinc-400 block font-normal">(Picos de {{ hybridAnalysis.electricalLines.line2TopsCtrlPeakWatts }} W con DJM y luces)</span>
              </p>
              <p class="text-zinc-300 text-[11px] leading-relaxed">
                Alimenta cajas acústicas en atril, torres de delay y equipamiento de DJ.
              </p>
            </div>
          </div>

          <p class="text-xs text-zinc-300 pt-1">
            📌 {{ hybridAnalysis.electricalLines.phaseBalanceDirective }}
          </p>
        </div>

        <!-- Semáforo de Estado de la Energía -->
        <div
          :class="[
            'p-6 rounded-2xl border-2 flex items-start space-x-4 shadow-2xl transition-all',
            powerAlertLevel === 'CRITICAL'
              ? 'bg-red-950/50 border-red-600 text-red-100'
              : powerAlertLevel === 'WARNING'
              ? 'bg-amber-950/50 border-amber-500 text-amber-100'
              : 'bg-emerald-950/50 border-emerald-600 text-emerald-100',
          ]"
        >
          <div
            :class="[
              'w-6 h-6 rounded-full shrink-0 border-2 mt-1',
              powerAlertLevel === 'CRITICAL'
                ? 'bg-red-500 border-white animate-ping'
                : powerAlertLevel === 'WARNING'
                ? 'bg-amber-400 border-white'
                : 'bg-emerald-400 border-white',
            ]"
          ></div>
          <div class="leading-relaxed w-full space-y-1">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <span class="font-black text-base uppercase tracking-wider font-mono">
                DIAGNÓSTICO ELÉCTRICO: {{ powerFeasibility.status === 'CRITICAL_TRIP_GUARANTEED' ? 'SOBRECARGA CRÍTICA (CORTE SEGURO)' : powerFeasibility.status === 'WARNING_OVERLOAD_RISK' ? 'ALERTA DE SOBRECARGA (> 80%)' : 'CARGA SEGURA CONFORME SEC' }}
              </span>
              <span class="text-xs font-mono px-3 py-1 rounded bg-black/50 border border-white/20 font-bold">
                Demanda: {{ powerFeasibility.totalSystemDemandWatts }}W continuos (Picos: {{ powerFeasibility.transientPeakWatts }}W) / Capacidad Segura: {{ powerFeasibility.availableContinuousWatts }}W ({{ powerFeasibility.loadPercentage }}%)
              </span>
            </div>
            <p class="text-sm sm:text-base">
              {{ powerFeasibility.technicalDiagnosis }}
            </p>
          </div>
        </div>

        <!-- Roster Individual de Parlantes + Checklist de Carga de Camioneta -->
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-6 shadow-2xl space-y-5">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 pb-4">
            <div>
              <h3 class="text-base sm:text-lg font-black tracking-wider text-white uppercase font-mono">
                📦 Roster de Conexiones y Checklist de Carga de Camioneta
              </h3>
              <p class="text-xs text-zinc-400 font-mono mt-0.5">
                Toca cada equipo para marcarlo como cargado en la camioneta antes de salir de bodega.
              </p>
            </div>
            <div class="flex items-center gap-3 font-mono text-xs">
              <span class="text-emerald-400 font-bold">
                Verificados: {{ checkedCount }} / {{ hybridAnalysis.roster.length }}
              </span>
              <button
                @click="toggleAllChecked"
                class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-600 cursor-pointer transition"
              >
                {{ checkedCount === hybridAnalysis.roster.length ? 'Desmarcar Todos' : '✔️ Marcar Todos' }}
              </button>
            </div>
          </div>

          <div class="space-y-3">
            <div
              v-for="item in hybridAnalysis.roster"
              :key="item.id"
              @click="toggleItemChecked(item.id)"
              :class="[
                'border-2 p-4 rounded-xl transition flex flex-col sm:flex-row sm:items-center justify-between gap-3 cursor-pointer select-none',
                checkedItems[item.id]
                  ? 'bg-emerald-950/25 border-emerald-600'
                  : 'bg-[#15151c] border-zinc-800 hover:border-zinc-700'
              ]"
            >
              <div class="flex items-start space-x-3.5">
                <div
                  :class="[
                    'w-11 h-11 rounded-xl flex items-center justify-center font-black font-mono text-base border-2 shrink-0 mt-0.5',
                    item.badgeBg
                  ]"
                >
                  {{ checkedItems[item.id] ? '✓' : item.tag }}
                </div>
                <div class="space-y-1">
                  <h4 class="text-base font-bold text-white flex flex-wrap items-center gap-2">
                    {{ item.name }}
                    <span class="text-[10px] px-2 py-0.5 rounded font-mono font-bold uppercase" :class="item.systemType === 'ACTIVE' ? 'bg-red-950 text-red-300 border border-red-700' : 'bg-cyan-950 text-cyan-300 border border-cyan-700'">
                      {{ item.systemType }}
                    </span>
                    <span v-if="item.delayMs > 0" class="text-[10px] px-2 py-0.5 rounded font-mono font-bold bg-emerald-950 text-emerald-300 border border-emerald-600">
                      ⏱️ DELAY +{{ item.delayMs }} ms
                    </span>
                  </h4>
                  <p class="text-xs sm:text-sm text-emerald-300 font-mono font-bold">
                    📍 Ubicación sugerida: {{ item.zoneLabel }} (X: {{ item.posX }}m, Y: {{ item.posY }}m)
                  </p>
                  <p class="text-xs text-amber-200 font-mono">
                    🎛️ Ajuste: {{ item.recommendedGainNote }}
                  </p>
                </div>
              </div>

              <div class="text-left sm:text-right border-t sm:border-t-0 pt-2 sm:pt-0 border-zinc-800 space-y-1 text-xs font-mono">
                <div>
                  <span class="text-zinc-400">Energía 220V: </span>
                  <span v-if="item.powerCableType === 'NONE_PASSIVE'" class="text-cyan-400 font-bold">
                    A Potencia (Speakon)
                  </span>
                  <span v-else class="text-amber-300 font-bold">
                    {{ item.powerCableMeters }}m a {{ item.assignedOutletName }} ({{ item.powerCableType }})
                  </span>
                </div>
                <div>
                  <span class="text-zinc-400">Señal: </span>
                  <span class="text-white font-bold">{{ item.signalLengthMeters }}m {{ item.signalCableType }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Resumen de Cables y Cinta Gaffer -->
          <div class="p-4 bg-[#181820] border border-zinc-700 rounded-xl grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs sm:text-sm font-mono">
            <div class="flex justify-between text-zinc-300">
              <span>Amplificadores Externos:</span>
              <span class="text-white font-bold">{{ hybridAnalysis.externalAmpsRequiredCount }} en cabina</span>
            </div>
            <div class="flex justify-between text-zinc-300">
              <span>Cables Speakon NL4 (Pasivos):</span>
              <span class="text-cyan-400 font-bold">{{ hybridAnalysis.speakonCablesCount }} unidades</span>
            </div>
            <div class="flex justify-between text-zinc-300">
              <span>Cables XLR Balanceados (Activos):</span>
              <span class="text-red-400 font-bold">{{ hybridAnalysis.xlrCablesCount }} unidades</span>
            </div>
            <div class="flex justify-between text-zinc-300">
              <span>Cinta Gaffer Gris (Rollos 50m):</span>
              <span class="text-amber-300 font-bold">{{ hybridAnalysis.floorTapeRolls50m }} rollo(s) ({{ hybridAnalysis.totalFloorTapeMeters }}m)</span>
            </div>
          </div>
        </div>

        <!-- Auditoría Completa de las 7 Reglas Críticas de Terreno -->
        <div class="bg-[#0f0f14] border-2 border-zinc-800 rounded-2xl p-6 shadow-2xl space-y-4">
          <div class="flex items-center justify-between border-b border-zinc-800 pb-3">
            <h3 class="text-base sm:text-lg font-black tracking-wider text-white uppercase font-mono">
              🛡️ 7 Reglas Críticas de Ingeniería en Terreno
            </h3>
            <span class="text-xs font-mono text-amber-400 font-bold">Prevención de Fallos en Vivo</span>
          </div>

          <div class="grid grid-cols-1 gap-3 text-xs sm:text-sm font-mono">
            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex justify-between">
                <span class="text-emerald-400 font-bold">1. Filtro Pasa-Altos (Crossover HPF en Cajas Top)</span>
                <span class="text-emerald-300 font-bold">{{ fieldAudit.hpfCutoffHz }} Hz (-{{ fieldAudit.hpfPowerSavedPct }}% derroche)</span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.hpfDirective }}</p>
            </div>

            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex justify-between">
                <span class="text-cyan-400 font-bold">2. Ángulo de Apertura Horizontal (Splay Angle Anti-Peine)</span>
                <span class="text-cyan-300 font-bold">Abrir {{ fieldAudit.recommendedSplayAngleDeg }}° por lado</span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.splayDirective }}</p>
            </div>

            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex justify-between">
                <span class="text-purple-400 font-bold">3. Alineación de Fase Sub vs. Top en Escenario</span>
                <span class="text-purple-300 font-bold">Tops A/B: +{{ fieldAudit.frontTopsMicroDelayMs }} ms</span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.phaseAlignmentDirective }}</p>
            </div>

            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex justify-between">
                <span class="text-amber-400 font-bold">4. Caída de Tensión en el Drop ({{ venue.electricalDistanceMeters }}m)</span>
                <span class="text-amber-300 font-bold">Mínimo {{ fieldAudit.recommendedCableMm2 }} mm² ({{ fieldAudit.voltageAtBoxDuringDropV }}V en el drop)</span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.cableVoltageDirective }}</p>
            </div>

            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1.5">
              <div class="flex justify-between">
                <span class="text-red-400 font-bold">5. Tierra Física (Anti-Hum 50Hz) y Compresión Térmica</span>
                <span class="text-red-300 font-bold">{{ fieldAudit.requiresCopperweldGroundRod ? 'Jabalina Cobre OBLIGATORIA' : 'Tierra Tablero' }}</span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.groundingDirective }}</p>
              <p class="text-amber-200/90 pt-1 border-t border-zinc-800">{{ fieldAudit.powerCompressionDirective }}</p>
            </div>

            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex justify-between">
                <span class="text-orange-400 font-bold">6. Autonomía de Combustible ({{ venue.eventDurationHours || 7 }}h evento + 1.5h prueba)</span>
                <span class="text-orange-300 font-bold">
                  {{ fieldAudit.fuelLogistics.applies ? `${fieldAudit.fuelLogistics.totalLitersRequired} L (${fieldAudit.fuelLogistics.jerrycans20LCount} bidón 20L)` : 'Red Fija 220V' }}
                </span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.fuelLogistics.fuelDirective }}</p>
            </div>

            <div class="bg-[#15151c] p-4 rounded-xl border border-zinc-800 space-y-1">
              <div class="flex justify-between">
                <span class="text-blue-400 font-bold">7. Prueba de Sonido (Vacío) vs. Pista Llena (~{{ fieldAudit.crowdAcousticShift.estimatedCrowdCapacity }} pers.)</span>
                <span class="text-blue-300 font-bold">-{{ fieldAudit.crowdAcousticShift.rt60ReductionPct }}% Eco RT60 · +{{ fieldAudit.crowdAcousticShift.temperatureRiseCelsius }}°C</span>
              </div>
              <p class="text-zinc-300">{{ fieldAudit.crowdAcousticShift.crowdDirective }}</p>
            </div>
          </div>

          <!-- HU07 / CU-06: PLANILLA ESTRICTA DE ALARGADORES Y ZAPATILLAS MULTICONTACTO -->
          <div class="bg-[#0e1014] border-2 border-emerald-700/70 rounded-2xl p-5 space-y-4 font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
              <div>
                <span class="text-[11px] text-emerald-400 font-black uppercase block">🔌 HU07 / CU-06 · MONTAJE RÁPIDO SEC RIC N° 10</span>
                <h3 class="text-base font-black text-white uppercase">Zapatillas Multicontacto, Bocas y Alargadores Exactos</h3>
              </div>
              <div class="flex flex-wrap gap-2 text-xs font-bold">
                <span class="bg-emerald-950 border border-emerald-600 text-emerald-200 px-2.5 py-1 rounded-lg">
                  {{ powerDistributionPlan.totalSocketsRequired }} Bocas totales
                </span>
                <span class="bg-amber-950 border border-amber-600 text-amber-200 px-2.5 py-1 rounded-lg">
                  {{ powerDistributionPlan.totalPowerStrips10A }}× 10A · {{ powerDistributionPlan.totalPowerStrips16A }}× 16A
                </span>
              </div>
            </div>

            <div v-if="powerDistributionPlan.alerts.length > 0" class="space-y-1.5">
              <div
                v-for="(al, i) in powerDistributionPlan.alerts"
                :key="`pa-${i}`"
                class="text-xs bg-red-950/60 border border-red-500 text-red-200 rounded-lg px-3 py-2"
              >
                {{ al }}
              </div>
            </div>

            <!-- Tabla de Zapatillas Z1..Zn -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div
                v-for="z in powerDistributionPlan.powerStrips"
                :key="z.id"
                class="bg-[#151820] border rounded-xl p-3.5 space-y-1.5 text-xs"
                :class="z.status === 'OVERLOAD' ? 'border-red-500' : z.status === 'WARNING' ? 'border-amber-500' : 'border-zinc-700'"
              >
                <div class="flex items-center justify-between">
                  <span class="font-black text-white text-sm">{{ z.id }} · {{ z.label }}</span>
                  <span class="px-2 py-0.5 rounded font-black text-[11px]" :class="z.ratingAmps === 16 ? 'bg-red-950 text-red-300 border border-red-700' : 'bg-emerald-950 text-emerald-300 border border-emerald-700'">
                    {{ z.ratingAmps }}A ({{ z.usedSockets }}/{{ z.totalSockets }} bocas)
                  </span>
                </div>
                <div class="text-zinc-300">
                  Carga: <strong class="text-amber-300">{{ z.loadWatts }}W</strong> / Límite seguro 80%: {{ z.safeMaxWatts }}W ({{ z.usagePct }}%)
                </div>
                <div class="text-[11px] text-zinc-400">
                  Conectar aquí: <span class="text-zinc-200">{{ z.connectedDevices.join(' · ') }}</span>
                </div>
              </div>
            </div>

            <!-- Lista consolidada de Alargadores a llevar -->
            <div class="bg-[#090b0f] border border-zinc-800 rounded-xl p-3.5 space-y-2">
              <div class="text-xs font-black text-amber-300 uppercase">📦 Lista Estricta de Alargadores para Bodega</div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                <div
                  v-for="(ext, idx) in powerDistributionPlan.extensionCordSummary"
                  :key="`extsum-${idx}`"
                  class="flex items-center justify-between bg-[#141720] border border-zinc-800 rounded-lg px-3 py-2"
                >
                  <span class="text-white font-bold">{{ ext.quantity }}× {{ ext.description }}</span>
                  <span class="text-[11px] text-amber-300 font-black">{{ ext.crossSectionMm2 }} mm²</span>
                </div>
              </div>
            </div>

            <div class="space-y-1 text-[11px] text-zinc-300">
              <p v-for="(rec, idx) in powerDistributionPlan.recommendations" :key="`prec-${idx}`">{{ rec }}</p>
            </div>
          </div>

          <!-- HU06 / CU-05: INVENTARIO FÍSICO DE CABLES DMX DESDE DMX OUT -->
          <div v-if="lightingDmxAnalysis.totalFixtureUnits > 0" class="bg-[#120d16] border-2 border-fuchsia-700/70 rounded-2xl p-5 space-y-4 font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
              <div>
                <span class="text-[11px] text-fuchsia-400 font-black uppercase block">🟣 HU06 / CU-05 · CABLEADO FÍSICO DESDE DMX OUT</span>
                <h3 class="text-base font-black text-white uppercase">Iluminación ({{ lightingDmxAnalysis.totalLightingWatts }}W) y Cables DMX de Montaje</h3>
              </div>
              <div class="flex flex-wrap gap-2 text-xs font-bold">
                <span class="bg-fuchsia-950 border border-fuchsia-600 text-fuchsia-200 px-2.5 py-1 rounded-lg">
                  {{ lightingDmxAnalysis.totalDmxCablesCount }} cables ({{ lightingDmxAnalysis.totalDmxMeters }}m)
                </span>
                <span v-if="lightingDmxAnalysis.terminators120OhmCount > 0" class="bg-purple-950 border border-purple-600 text-purple-200 px-2.5 py-1 rounded-lg">
                  {{ lightingDmxAnalysis.terminators120OhmCount }}× Terminador 120Ω
                </span>
                <span v-if="lightingDmxAnalysis.needsDmxSplitter" class="bg-amber-950 border border-amber-500 text-amber-200 px-2.5 py-1 rounded-lg">
                  🔀 Splitter DMX sugerido
                </span>
              </div>
            </div>

            <div v-if="lightingDmxAnalysis.dmxCableInventory.length > 0" class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div
                v-for="(item, idx) in lightingDmxAnalysis.dmxCableInventory"
                :key="`dmxinv-${idx}`"
                class="bg-[#1c1324] border border-fuchsia-900 rounded-lg px-3 py-2.5 space-y-0.5"
              >
                <div class="text-white font-black">{{ item.quantity }}× {{ item.description }}</div>
                <div class="text-[11px] text-fuchsia-300">{{ item.kindSummary }}</div>
              </div>
            </div>

            <div class="space-y-1 text-[11px] text-zinc-300">
              <p v-for="(al, idx) in lightingDmxAnalysis.alerts" :key="`dal-${idx}`" class="text-orange-300 font-bold">{{ al }}</p>
              <p v-for="(rec, idx) in lightingDmxAnalysis.recommendations" :key="`drec-${idx}`">{{ rec }}</p>
            </div>
          </div>

          <!-- CONEXIONES EXACTAS DE AUDIO Y RED EN CABINA DJ (MIXER / CDJ / RETORNO / POWER) -->
          <div v-if="djSetupAnalysis.audioRoutes.length > 0" class="bg-[#0e1217] border-2 border-cyan-700/70 rounded-2xl p-5 space-y-4 font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
              <div>
                <span class="text-[11px] text-cyan-400 font-black uppercase block">🎛️ FLUJO DE SEÑAL Y CONEXIONES DE AUDIO</span>
                <h3 class="text-base font-black text-white uppercase">Setup Cabina DJ, Ethernet Pro DJ Link, Retorno y Power</h3>
              </div>
              <div class="flex flex-wrap gap-2 text-xs font-bold">
                <span v-if="djSetupAnalysis.ethernetCablesCount > 0" class="bg-cyan-950 border border-cyan-600 text-cyan-200 px-2.5 py-1 rounded-lg">
                  🌐 {{ djSetupAnalysis.ethernetCablesCount }}× RJ45 {{ djSetupAnalysis.requiresEthernetSwitch ? '+ Switch' : '' }}
                </span>
                <span v-if="djSetupAnalysis.trsToXlrBoothCablesCount > 0" class="bg-amber-950 border border-amber-600 text-amber-200 px-2.5 py-1 rounded-lg">
                  🎧 {{ djSetupAnalysis.trsToXlrBoothCablesCount }}× TRS-XLR Booth
                </span>
              </div>
            </div>

            <div class="space-y-2 text-xs">
              <div
                v-for="rt in djSetupAnalysis.audioRoutes"
                :key="rt.id"
                class="bg-[#141922] border border-zinc-800 rounded-xl p-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
              >
                <div class="space-y-0.5">
                  <div class="text-white font-black">
                    {{ rt.quantity }}× {{ rt.cableType }} ({{ rt.lengthMeters }}m)
                  </div>
                  <div class="text-cyan-300 text-[11px]">
                    {{ rt.fromPort }} → {{ rt.toPort }}
                  </div>
                  <div class="text-zinc-400 text-[11px]">{{ rt.note }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- HU09 / CU-08: LOGÍSTICA DE VEHÍCULO, LEY DEL SACO N° 20.949 Y CHECKLIST 3 ETAPAS -->
          <div class="bg-[#0e1116] border-2 border-cyan-700/70 rounded-2xl p-5 space-y-4 font-mono">
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 pb-3">
              <div>
                <span class="text-[11px] text-cyan-400 font-black uppercase block">🚚 HU09 / CU-08 · LOGÍSTICA Y ERGONOMÍA CHILE</span>
                <h3 class="text-base font-black text-white uppercase">Peso Total, Vehículo, Ley del Saco y Checklist Operativo</h3>
              </div>
              <div class="flex flex-wrap gap-2 text-xs font-bold">
                <span class="bg-cyan-950 border border-cyan-600 text-cyan-200 px-2.5 py-1 rounded-lg">
                  ⚖️ {{ loadLogistics.grandTotalWeightKg }} kg totales
                </span>
                <span class="bg-zinc-900 border border-zinc-700 text-white px-2.5 py-1 rounded-lg">
                  🚐 {{ loadLogistics.recommendedVehicle }} ({{ loadLogistics.recommendedOperatorsCount }} op.)
                </span>
              </div>
            </div>

            <div v-if="loadLogistics.leyDelSacoAlert" class="text-xs bg-amber-950/60 border-2 border-amber-500 text-amber-200 rounded-xl p-3 font-bold">
              {{ loadLogistics.leyDelSacoAlert }}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div
                v-for="stage in (['PRE_DEPARTURE', 'ON_SITE_SETUP', 'TEARDOWN_5AM'] as const)"
                :key="stage"
                class="bg-[#141923] border border-zinc-800 rounded-xl p-3 space-y-2"
              >
                <div class="font-black uppercase text-[11px]" :class="stage === 'PRE_DEPARTURE' ? 'text-cyan-300' : stage === 'ON_SITE_SETUP' ? 'text-emerald-300' : 'text-amber-300'">
                  {{ stage === 'PRE_DEPARTURE' ? '1. Salida Bodega' : stage === 'ON_SITE_SETUP' ? '2. Montaje Terreno' : '3. Retiro 5:00 AM' }}
                </div>
                <label
                  v-for="task in loadLogistics.checklist.filter(c => c.stage === stage)"
                  :key="task.id"
                  class="flex items-start gap-2 cursor-pointer text-[11px] text-zinc-200 hover:text-white"
                >
                  <input
                    type="checkbox"
                    :checked="!!logisticsChecks[task.id]"
                    @change="logisticsChecks[task.id] = !logisticsChecks[task.id]"
                    class="mt-0.5 accent-emerald-500 cursor-pointer"
                  />
                  <span :class="logisticsChecks[task.id] ? 'line-through text-zinc-500' : ''">{{ task.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <div class="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-zinc-800">
            <button
              @click="goToStep(3)"
              class="px-5 py-3.5 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-700 font-mono font-bold text-sm cursor-pointer transition"
            >
              ← Volver al Plano 2D (Paso 3)
            </button>
            <button
              @click="downloadPdf"
              class="px-8 py-4 rounded-xl bg-red-600 hover:bg-red-500 text-white font-black text-base uppercase tracking-wider font-mono shadow-2xl shadow-red-600/40 cursor-pointer transition"
            >
              📄 Descargar Reporte Oficial PDF
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- DOCK DE NAVEGACIÓN INFERIOR FIJO PARA CELULAR (MOBILE FIRST < 768px) -->
    <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-[#09090d]/95 backdrop-blur-md border-t-2 border-red-600/80 px-2 py-1.5 grid grid-cols-5 gap-1">
      <button
        v-for="step in wizardSteps"
        :key="`mob-${step.id}`"
        @click="goToStep(step.id)"
        :class="[
          'flex flex-col items-center justify-center py-2 px-1 rounded-xl font-mono transition cursor-pointer',
          currentStep === step.id
            ? 'bg-red-600 text-white font-black'
            : isStepUnlocked(step.id)
            ? 'text-zinc-300 hover:bg-zinc-900'
            : 'text-zinc-600 opacity-60'
        ]"
      >
        <span class="text-base leading-none">{{ step.icon }}</span>
        <span class="text-[10px] mt-1 truncate max-w-full">{{ step.shortLabel }}</span>
      </button>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import LayoutSvg2D from './components/LayoutSvg2D.vue';
import InfoBadge from './components/InfoBadge.vue';
import PioneerMixerSimulator from './components/PioneerMixerSimulator.vue';
import { generateOperationalReportPdf } from './services/pdfReport';
import {
  analyzeHybridRig,
  generateSmartAcousticPlacement,
  generateSmartPlacementFromBatches,
  analyzePassiveImpedance,
  evaluateTopToSubBalance,
  evaluateNeighborhoodNoise,
  StageAcousticEngine,
  PowerSourceValidator,
  evaluateFieldEngineering,
  VolumeDriveRegime,
  SpeakerBatchInput,
  VenueEnclosureWallType,
  EventScheduleShift,
  AudioBox,
  VenueEnvironment,
  LIGHTING_PRESETS,
  calculateLightingAndDmxRig,
  calculatePowerDistribution,
  simulateContingencyPlan,
  calculateLoadLogistics,
  analyzeDjSetupAndAudioRouting,
  type LightingBatchInput,
  type LightingPreset,
  type ContingencyScenario,
  type DjSetupMode,
  type PlayerAudioLinkType,
} from '@stageplan/shared';

type WizardStepId = 0 | 1 | 2 | 3 | 4;

const wizardSteps: { id: WizardStepId; icon: string; shortLabel: string; title: string; subtitle: string }[] = [
  { id: 0, icon: '🛡️', shortLabel: '0. Acceso', title: 'Acceso Operador', subtitle: 'Credencial Anti-IDOR' },
  { id: 1, icon: '📐', shortLabel: '1. Recinto', title: 'Medidas y Casos Demo', subtitle: 'Dimensiones y 8 Escalas' },
  { id: 2, icon: '⚡', shortLabel: '2. Equipos', title: 'Sonido y Electricidad', subtitle: 'Lotes Mixtos, RMS/Peak y Fuente' },
  { id: 3, icon: '🗺️', shortLabel: '3. Plano 2D', title: 'Plano 2D y Heatmap', subtitle: 'Ubicación, SPL y Vúmetros' },
  { id: 4, icon: '📋', shortLabel: '4. Reporte', title: 'Reporte Final y PDF', subtitle: 'Camioneta, Fases y 7 Reglas' },
];

const currentStep = ref<WizardStepId>(0);
const isValidated = ref(false);
const validationMessage = ref('');
const activePresetId = ref<string | null>(null);
const checkedItems = reactive<Record<string, boolean>>({});
const storageFeedbackMsg = ref('');
const hasSavedCustomRig = ref(false);
const passiveWiringMode = ref<'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK'>('INDEPENDENT_CHANNELS');

// 0. Estado del Operador y Autenticación (Vista 0 - Login)
const operator = reactive({
  email: 'mauricio.vega@distorsioncl.cl',
  password: 'password123',
  name: 'Mauricio Vega Castillo',
  role: 'Administrador / Ingeniero FOH',
  organization: 'DISTORSIONCL SPA',
  isLogged: false,
  token: '',
  rememberMe: true,
});

const loginLoading = ref(false);
const loginError = ref('');
const showPassword = ref(false);

const operatorSignature = computed(() => {
  const n = operator.name.trim() || 'Mauricio Vega Castillo';
  return `${n} — ${operator.role} (${operator.organization || 'DISTORSIONCL SPA'})`;
});

function fillEvaluationCredentials() {
  operator.email = 'mauricio.vega@distorsioncl.cl';
  operator.password = 'password123';
  operator.name = 'Mauricio Vega Castillo';
  operator.role = 'Administrador / Ingeniero FOH';
  operator.organization = 'DISTORSIONCL SPA';
  loginError.value = '';
}

async function handleLogin() {
  if (!operator.email || !operator.password) {
    loginError.value = 'Por favor ingresa tu correo y contraseña.';
    return;
  }
  loginLoading.value = true;
  loginError.value = '';

  try {
    const res = await fetch('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: operator.email,
        password: operator.password,
      }),
    });

    if (res.ok) {
      const data = await res.json();
      operator.token = data.token || 'jwt_token_' + Date.now();
      if (data.user?.name) operator.name = data.user.name;
      operator.isLogged = true;
      if (operator.rememberMe) {
        localStorage.setItem('stageplan_token', operator.token);
        localStorage.setItem('stageplan_operator', JSON.stringify({
          email: operator.email,
          name: operator.name,
          role: operator.role,
          organization: operator.organization,
        }));
      }
      currentStep.value = 1;
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    } else {
      const err = await res.json().catch(() => ({}));
      // En evaluación offline o credenciales predeterminadas de demo:
      if (operator.email === 'mauricio.vega@distorsioncl.cl' && operator.password === 'password123') {
        operator.isLogged = true;
        operator.token = 'demo_jwt_session_token';
        currentStep.value = 1;
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }
      loginError.value = err.error || 'Credenciales incorrectas.';
      return;
    }
  } catch (_netErr) {
    // Si el servidor backend no está encendido, permitir inicio de contingencia local
    if (operator.email.includes('@') && operator.password.length >= 6) {
      operator.isLogged = true;
      operator.token = 'local_session_token_' + Date.now();
      if (!operator.name || !operator.name.trim()) {
        operator.name = 'Mauricio Vega Castillo';
      }
      if (operator.rememberMe) {
        localStorage.setItem('stageplan_token', operator.token);
        localStorage.setItem('stageplan_operator', JSON.stringify({
          email: operator.email,
          name: operator.name,
          role: operator.role,
          organization: operator.organization,
        }));
      }
      currentStep.value = 1;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      loginError.value = 'Ingrese un correo electrónico válido y una contraseña de al menos 6 caracteres.';
    }
  } finally {
    loginLoading.value = false;
  }
}

function handleLogout() {
  operator.isLogged = false;
  operator.token = '';
  localStorage.removeItem('stageplan_token');
  currentStep.value = 0;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function isStepUnlocked(stepId: WizardStepId): boolean {
  if (stepId === 0) return true;
  if (!operator.isLogged) return false;
  if (stepId <= 2) return true;
  return isValidated.value;
}

function isStepCompleted(stepId: WizardStepId): boolean {
  if (stepId === 0) return operator.isLogged;
  if (stepId === 1) return Boolean(venue.name && venue.widthMeters && venue.depthMeters && venue.electricalDistanceMeters);
  if (stepId >= 2) return isValidated.value;
  return false;
}

function goToStep(stepId: WizardStepId) {
  if (stepId > 0 && !operator.isLogged) {
    loginError.value = 'Debes autenticarte en la Consola Técnica para continuar.';
    currentStep.value = 0;
    return;
  }
  if (stepId >= 3 && !isValidated.value) {
    validateData();
    if (!isValidated.value) {
      currentStep.value = 2;
      return;
    }
  }
  currentStep.value = stepId;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function validateAndGoToSimulation() {
  validateData();
  if (isValidated.value) {
    currentStep.value = 3;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// 1. Estado Reactivo del Recinto
const venue = reactive({
  name: '',
  widthMeters: undefined as number | undefined,
  depthMeters: undefined as number | undefined,
  heightMeters: 3.5,
  environmentType: 'INDOOR',
  electricalDistanceMeters: undefined as number | undefined,
  eventDurationHours: undefined as number | undefined,
  temperatureCelsius: 20,
  targetSplDba: 102,
  neighborDistanceMeters: 30,
  enclosureWallType: 'OPEN_AIR' as VenueEnclosureWallType,
  scheduleShift: 'NIGHTTIME_21_07' as EventScheduleShift,
});

// 2. CONSTRUCTOR POR LOTES (Tops y Sub-bajos Híbridos con RMS y Peak)
const topBatches = ref<SpeakerBatchInput[]>([
  {
    id: 'top-b1',
    category: 'top_box',
    systemType: 'ACTIVE',
    quantity: 2,
    modelLabel: 'Caja Activa 15" Principal',
    coneSizeInches: 15,
    rmsWatts: 500,
    peakWatts: 1000,
    impedanceOhms: 8,
  },
]);

const subBatches = ref<SpeakerBatchInput[]>([
  {
    id: 'sub-b1',
    category: 'sub_bass',
    systemType: 'ACTIVE',
    quantity: 1,
    modelLabel: 'Sub Activo 18" Central',
    coneSizeInches: 18,
    rmsWatts: 800,
    peakWatts: 1600,
    impedanceOhms: 8,
  },
]);

function onBatchRmsChange(batch: SpeakerBatchInput) {
  if (batch.rmsWatts && (!batch.peakWatts || batch.peakWatts === batch.rmsWatts * 2 || batch.peakWatts < batch.rmsWatts)) {
    batch.peakWatts = Math.round(batch.rmsWatts * 2);
  }
  resetValidation();
}

function addTopBatch() {
  const newId = `top-b${Date.now()}`;
  topBatches.value.push({
    id: newId,
    category: 'top_box',
    systemType: 'PASSIVE',
    quantity: 1,
    modelLabel: `Caja Pasiva 12" Refuerzo`,
    coneSizeInches: 12,
    rmsWatts: 350,
    peakWatts: 700,
    impedanceOhms: 8,
  });
  resetValidation();
}

function removeTopBatch(index: number) {
  if (topBatches.value.length > 1) {
    topBatches.value.splice(index, 1);
    resetValidation();
  }
}

function addSubBatch() {
  const newId = `sub-b${Date.now()}`;
  subBatches.value.push({
    id: newId,
    category: 'sub_bass',
    systemType: 'PASSIVE',
    quantity: 1,
    modelLabel: `Sub Pasivo 18"`,
    coneSizeInches: 18,
    rmsWatts: 600,
    peakWatts: 1200,
    impedanceOhms: 8,
  });
  resetValidation();
}

function removeSubBatch(index: number) {
  if (subBatches.value.length > 1) {
    subBatches.value.splice(index, 1);
    resetValidation();
  }
}

const totalTopsCount = computed(() => {
  return topBatches.value.reduce((acc, b) => acc + (Math.max(0, Math.floor(b.quantity)) || 0), 0);
});

const totalTopsRmsWatts = computed(() => {
  return topBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.rmsWatts || 0)), 0);
});

const totalTopsPeakWatts = computed(() => {
  return topBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.peakWatts || b.rmsWatts * 2 || 0)), 0);
});

const totalSubsCount = computed(() => {
  return subBatches.value.reduce((acc, b) => acc + (Math.max(0, Math.floor(b.quantity)) || 0), 0);
});

const totalSubsRmsWatts = computed(() => {
  return subBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.rmsWatts || 0)), 0);
});

const totalSubsPeakWatts = computed(() => {
  return subBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.peakWatts || b.rmsWatts * 2 || 0)), 0);
});

const allBatches = computed<SpeakerBatchInput[]>(() => {
  return [...topBatches.value, ...subBatches.value];
});

// 2B. HU06 / CU-05: CONSTRUCTOR DE ILUMINACIÓN, EFECTOS (HUMO/LÁSER) Y DMX FÍSICO
const lightingPresets = LIGHTING_PRESETS;
const lightingBatches = ref<LightingBatchInput[]>([
  {
    id: 'light-init-1',
    name: 'Foco PAR LED (54x3W)',
    fixtureType: 'PAR_LED',
    quantity: 4,
    nominalWatts: 120,
    zone: 'TRUSS_LEFT',
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 2.5,
    isThermalLoad: false,
  },
]);

function addLightingPreset(preset: LightingPreset) {
  lightingBatches.value.push({
    id: `light-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    name: preset.name,
    fixtureType: preset.fixtureType,
    quantity: 1,
    nominalWatts: preset.nominalWatts,
    zone: preset.defaultZone,
    dmxConnector: preset.dmxConnector,
    unitWeightKg: preset.unitWeightKg,
    isThermalLoad: preset.isThermalLoad,
  });
  resetValidation();
}

function addCustomLighting() {
  lightingBatches.value.push({
    id: `light-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
    name: 'Foco PAR LED 54x3W RGBW',
    fixtureType: 'PAR_LED',
    quantity: 1,
    nominalWatts: 120,
    zone: 'TRUSS_LEFT',
    dmxConnector: 'DMX_3PIN',
    unitWeightKg: 2.5,
    isThermalLoad: false,
  });
  resetValidation();
}

function removeLightingBatch(index: number) {
  lightingBatches.value.splice(index, 1);
}

const lightingDmxAnalysis = computed(() => {
  return calculateLightingAndDmxRig(
    lightingBatches.value,
    venue.widthMeters || 10,
    venue.depthMeters || 16,
    220
  );
});

const activeContingencyScenario = ref<ContingencyScenario>('GENERATOR_FAIL_TO_10A');
const logisticsChecks = reactive<Record<string, boolean>>({});

// 2C. SETUP CABINA DJ (CDJ/XDJ + ETHERNET + RETORNO BOOTH + POWER PASIVOS)
const djSetup = reactive({
  setupMode: 'CDJ_XDJ_MODULAR' as DjSetupMode,
  playerCount: 2 as 0 | 2 | 3 | 4,
  playerAudioLinkType: 'RCA_ANALOG' as PlayerAudioLinkType,
  linkEthernetProDj: true,
  linkMixerToEthernet: false,
  boothMonitorsCount: 1 as 0 | 1 | 2,
  boothMonitorType: 'ACTIVE' as 'ACTIVE' | 'PASSIVE',
  boothMonitorRmsWatts: 300,
  boothMonitorImpedanceOhms: 8 as 4 | 8,
});

const djSetupAnalysis = computed(() => {
  return analyzeDjSetupAndAudioRouting({
    setupMode: djSetup.setupMode,
    playerCount: djSetup.playerCount,
    playerAudioLinkType: djSetup.playerAudioLinkType,
    linkEthernetProDj: djSetup.linkEthernetProDj,
    linkMixerToEthernet: djSetup.linkMixerToEthernet,
    boothMonitorsCount: djSetup.boothMonitorsCount,
    boothMonitorType: djSetup.boothMonitorType,
    boothMonitorRmsWatts: djSetup.boothMonitorRmsWatts,
    boothMonitorImpedanceOhms: djSetup.boothMonitorImpedanceOhms,
    speakerBatches: allBatches.value,
    passiveWiringMode: passiveWiringMode.value,
  });
});

// 2D. HU07 / CU-06: PLAN DE ALARGADORES Y ZAPATILLAS MULTICONTACTO
const powerDistributionPlan = computed(() => {
  return calculatePowerDistribution({
    venueWidthMeters: venue.widthMeters || 10,
    venueDepthMeters: venue.depthMeters || 16,
    electricalDistanceMeters: venue.electricalDistanceMeters || 12,
    djBoothWatts: djSetupAnalysis.value.djBoothTotal220vWatts + djSetupAnalysis.value.boothMonitorsTotal220vWatts,
    djBoothDevices: djSetupAnalysis.value.djBoothDevicesForPowerStrip,
    roster: hybridAnalysis.value.roster,
    externalAmpsCount: hybridAnalysis.value.externalAmpsRequiredCount,
    lightingAnalysis: lightingDmxAnalysis.value,
  });
});

// 2E. HU08 / CU-07: SIMULADOR PLAN B (CONTINGENCIA EN VIVO)
const contingencyPlan = computed(() => {
  return simulateContingencyPlan(activeContingencyScenario.value, {
    totalAudioSubsWatts: hybridAnalysis.value.electricalLines.line1SubsWatts,
    totalAudioTopsAndBoothWatts:
      hybridAnalysis.value.electricalLines.line2TopsCtrlWatts + djSetupAnalysis.value.boothMonitorsTotal220vWatts,
    thermalFxWatts: lightingDmxAnalysis.value.thermalEffectsWatts,
    lightingLedWatts: lightingDmxAnalysis.value.nonThermalLightingWatts,
    topsCount: totalTopsCount.value,
    subsCount: totalSubsCount.value,
    hasPassiveSpeakers: passiveImpedanceAudit.value.hasPassiveUnits,
  });
});

// 2F. HU09 / CU-08: LOGÍSTICA DE CARGA, VEHÍCULO Y LEY DEL SACO (25 KG)
const loadLogistics = computed(() => {
  const items = [
    ...topBatches.value.map((b) => ({
      name: b.modelLabel || 'Caja Top',
      quantity: b.quantity || 0,
      unitWeightKg: b.coneSizeInches >= 15 ? 24 : 18,
    })),
    ...subBatches.value.map((b) => ({
      name: b.modelLabel || 'Subwoofer',
      quantity: b.quantity || 0,
      unitWeightKg: b.coneSizeInches >= 18 ? 38 : 28,
    })),
    ...lightingBatches.value.map((l) => ({
      name: l.name,
      quantity: l.quantity || 0,
      unitWeightKg: l.unitWeightKg || 4,
    })),
  ];

  return calculateLoadLogistics({
    items,
    extensionCordsCount: powerDistributionPlan.value.extensionCords.length,
    powerStripsCount: powerDistributionPlan.value.totalPowerStripsCount,
    dmxCablesCount: lightingDmxAnalysis.value.totalDmxCablesCount,
    dmxTerminatorsCount: lightingDmxAnalysis.value.terminators120OhmCount,
    gafferRolls50m: Math.max(1, hybridAnalysis.value.floorTapeRolls50m),
    usesGenerator: powerSource.type !== 'GRID_220V',
    has16ASockets: powerDistributionPlan.value.totalPowerStrips16A > 0,
  });
});

// 3. Auditoría de Impedancia para Unidades Pasivas (Speakon Ohms)
const passiveImpedanceAudit = computed(() => {
  return analyzePassiveImpedance(allBatches.value, passiveWiringMode.value);
});

// 4. Fuente Eléctrica y Régimen de Exigencia de Volumen
const powerSource = reactive({
  type: 'GRID_220V' as 'GRID_220V' | 'GENERATOR_WATTS' | 'GENERATOR_KVA',
  circuitBreakerAmps: '16' as '10' | '16' | '20' | '25' | '32',
  generatorSurgeWatts: undefined as number | undefined,
  apparentPowerKva: undefined as number | undefined,
  powerFactor: 0.8,
  driveRegime: 'MAX_TECHNO_1_3' as VolumeDriveRegime,
});

// Guardado y Carga en LocalStorage de Sets de Equipos
function saveCustomRigToStorage() {
  try {
    const payload = {
      topBatches: topBatches.value,
      subBatches: subBatches.value,
      powerSource: { ...powerSource },
    };
    localStorage.setItem('stageplan_custom_rig', JSON.stringify(payload));
    hasSavedCustomRig.value = true;
    storageFeedbackMsg.value = '✓ Tu Set de Equipos (Lotes, Watts RMS y Peak) fue guardado exitosamente en el navegador.';
    setTimeout(() => { storageFeedbackMsg.value = ''; }, 4500);
  } catch (e) {
    storageFeedbackMsg.value = 'No se pudo guardar en almacenamiento local.';
  }
}

function loadCustomRigFromStorage() {
  try {
    const raw = localStorage.getItem('stageplan_custom_rig');
    if (!raw) return;
    const data = JSON.parse(raw);
    if (Array.isArray(data.topBatches)) topBatches.value = data.topBatches;
    if (Array.isArray(data.subBatches)) subBatches.value = data.subBatches;
    if (data.powerSource) Object.assign(powerSource, data.powerSource);
    storageFeedbackMsg.value = '✓ Tu Set Personalizado ha sido cargado con éxito.';
    setTimeout(() => { storageFeedbackMsg.value = ''; }, 4500);
    resetValidation();
  } catch (e) {
    storageFeedbackMsg.value = 'Error al leer el set guardado.';
  }
}

function loadMixedActivePassiveExample() {
  topBatches.value = [
    {
      id: 't-ex1',
      category: 'top_box',
      systemType: 'ACTIVE',
      quantity: 2,
      modelLabel: 'Caja Activa 15" Frente (PA Principal)',
      coneSizeInches: 15,
      rmsWatts: 500,
      peakWatts: 1000,
      impedanceOhms: 8,
    },
    {
      id: 't-ex2',
      category: 'top_box',
      systemType: 'PASSIVE',
      quantity: 1,
      modelLabel: 'Caja Pasiva 12" Refuerzo (Delay Lateral)',
      coneSizeInches: 12,
      rmsWatts: 350,
      peakWatts: 700,
      impedanceOhms: 8,
    },
  ];
  subBatches.value = [
    {
      id: 's-ex1',
      category: 'sub_bass',
      systemType: 'ACTIVE',
      quantity: 1,
      modelLabel: 'Sub Activo 18" (Cluster Piso)',
      coneSizeInches: 18,
      rmsWatts: 800,
      peakWatts: 1600,
      impedanceOhms: 8,
    },
    {
      id: 's-ex2',
      category: 'sub_bass',
      systemType: 'PASSIVE',
      quantity: 1,
      modelLabel: 'Sub Pasivo 18" (Power Externo)',
      coneSizeInches: 18,
      rmsWatts: 600,
      peakWatts: 1200,
      impedanceOhms: 8,
    },
  ];
  powerSource.type = 'GENERATOR_WATTS';
  powerSource.generatorSurgeWatts = 3500;
  powerSource.driveRegime = 'MAX_TECHNO_1_3';
  storageFeedbackMsg.value = '⚡ Ejemplo cargado: 2 Cajas Activas 500W + 1 Pasiva 350W + 1 Sub Activo 800W + 1 Sub Pasivo 600W.';
  setTimeout(() => { storageFeedbackMsg.value = ''; }, 4500);
  resetValidation();
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    if (localStorage.getItem('stageplan_custom_rig')) {
      hasSavedCustomRig.value = true;
    }
    const savedToken = localStorage.getItem('stageplan_token');
    const savedOp = localStorage.getItem('stageplan_operator');
    if (savedToken && savedOp) {
      try {
        const parsed = JSON.parse(savedOp);
        operator.email = parsed.email || operator.email;
        operator.name = parsed.name || operator.name;
        operator.role = parsed.role || operator.role;
        operator.organization = parsed.organization || operator.organization;
        operator.token = savedToken;
        operator.isLogged = true;
      } catch (_e) {}
    }
  }
});

interface DemoPreset {
  id: string;
  scaleTag: string;
  areaLabel: string;
  title: string;
  subtitle: string;
  badgeClass: string;
  venue: {
    name: string;
    widthMeters: number;
    depthMeters: number;
    environmentType: 'INDOOR' | 'OUTDOOR_PARCELA';
    electricalDistanceMeters: number;
    eventDurationHours: number;
  };
  tops: SpeakerBatchInput[];
  subs: SpeakerBatchInput[];
  power: {
    type: 'GRID_220V' | 'GENERATOR_WATTS' | 'GENERATOR_KVA';
    circuitBreakerAmps?: '10' | '16' | '20' | '25' | '32';
    generatorSurgeWatts?: number;
    apparentPowerKva?: number;
    driveRegime: VolumeDriveRegime;
  };
}

// 8 CASOS COTIDIANOS DE MENOR A MAYOR ESCALA (Actualizados con lotes y Peak)
const demoPresets: DemoPreset[] = [
  {
    id: 'scale-1-living',
    scaleTag: '1. MICRO ESCALA',
    areaLabel: '5m × 6m (30 m²)',
    title: '🏠 Junta / Previa en Depto o Terraza',
    subtitle: '2 Cajas Activas 400W (Sin Sub) · Enchufe 10A · Volumen Moderado',
    badgeClass: 'bg-emerald-950 text-emerald-300 border border-emerald-700',
    venue: {
      name: 'Terraza Departamento Providencia',
      widthMeters: 5,
      depthMeters: 6,
      environmentType: 'INDOOR',
      electricalDistanceMeters: 8,
      eventDurationHours: 5,
    },
    tops: [{ id: 'p1-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Caja Activa 10"', coneSizeInches: 10, rmsWatts: 400, peakWatts: 800 }],
    subs: [],
    power: { type: 'GRID_220V', circuitBreakerAmps: '10', driveRegime: 'MODERATE_1_8' },
  },
  {
    id: 'scale-2-quincho',
    scaleTag: '2. ESCALA BAJA',
    areaLabel: '8m × 10m (80 m²)',
    title: '🏡 Cumpleaños en Patio / Quincho Casa',
    subtitle: '2 Cajas 600W + 1 Sub 800W · Enchufe Casa 10A · Régimen Estándar',
    badgeClass: 'bg-emerald-950 text-emerald-300 border border-emerald-700',
    venue: {
      name: 'Quincho Familiar La Florida',
      widthMeters: 8,
      depthMeters: 10,
      environmentType: 'OUTDOOR_PARCELA',
      electricalDistanceMeters: 18,
      eventDurationHours: 6,
    },
    tops: [{ id: 'p2-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Caja Activa 12"', coneSizeInches: 12, rmsWatts: 600, peakWatts: 1200 }],
    subs: [{ id: 'p2-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 1, modelLabel: 'Sub Activo 15"', coneSizeInches: 15, rmsWatts: 800, peakWatts: 1600 }],
    power: { type: 'GRID_220V', circuitBreakerAmps: '10', driveRegime: 'STANDARD_CLUB_1_5' },
  },
  {
    id: 'scale-3-overload-10a',
    scaleTag: '3. FALLO COMÚN',
    areaLabel: '9m × 12m (108 m²)',
    title: '⚠️ Fiesta en Casa Botando Enchufe 10A',
    subtitle: '2 Tops 1000W + 2 Subs 1000W al Máximo en Enchufe 10A (Cortocircuito)',
    badgeClass: 'bg-red-950 text-red-300 border border-red-600',
    venue: {
      name: 'Casa Particular Ñuñoa (Sobrecarga 10A)',
      widthMeters: 9,
      depthMeters: 12,
      environmentType: 'INDOOR',
      electricalDistanceMeters: 25,
      eventDurationHours: 7,
    },
    tops: [{ id: 'p3-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Top Activo 15"', coneSizeInches: 15, rmsWatts: 1000, peakWatts: 2000 }],
    subs: [{ id: 'p3-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Sub Activo 18"', coneSizeInches: 18, rmsWatts: 1000, peakWatts: 2000 }],
    power: { type: 'GRID_220V', circuitBreakerAmps: '10', driveRegime: 'MAX_TECHNO_1_3' },
  },
  {
    id: 'scale-4-restobar',
    scaleTag: '4. ESCALA MEDIA-BAJA (MIXTO)',
    areaLabel: '10m × 16m (160 m²)',
    title: '🍹 Restobar / Club Pequeño (Híbrido)',
    subtitle: '4 Cajas Activas 500W (Con Delay) + 1 Sub Pasivo 1000W (8Ω) · Red 16A',
    badgeClass: 'bg-cyan-950 text-cyan-300 border border-cyan-700',
    venue: {
      name: 'Restobar Barrio Italia (Salón Largo)',
      widthMeters: 10,
      depthMeters: 16,
      environmentType: 'INDOOR',
      electricalDistanceMeters: 20,
      eventDurationHours: 6,
    },
    tops: [{ id: 'p4-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 4, modelLabel: 'Top Activo 12"', coneSizeInches: 12, rmsWatts: 500, peakWatts: 1000 }],
    subs: [{ id: 'p4-s1', category: 'sub_bass', systemType: 'PASSIVE', quantity: 1, modelLabel: 'Sub Pasivo 18"', coneSizeInches: 18, rmsWatts: 1000, peakWatts: 2000, impedanceOhms: 8 }],
    power: { type: 'GRID_220V', circuitBreakerAmps: '16', driveRegime: 'STANDARD_CLUB_1_5' },
  },
  {
    id: 'scale-5-parcela-gen3500',
    scaleTag: '5. ESCALA MEDIA (GENERADOR)',
    areaLabel: '12m × 18m (216 m²)',
    title: '🌲 Parcela con Generador de 3500 W',
    subtitle: '2 Tops 1000W + 2 Subs 1000W · Alerta AVR 72% + Bencina + Jabalina',
    badgeClass: 'bg-amber-950 text-amber-300 border border-amber-600',
    venue: {
      name: 'Parcela Los Aromos Curacaví',
      widthMeters: 12,
      depthMeters: 18,
      environmentType: 'OUTDOOR_PARCELA',
      electricalDistanceMeters: 35,
      eventDurationHours: 8,
    },
    tops: [{ id: 'p5-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Top Activo 15"', coneSizeInches: 15, rmsWatts: 1000, peakWatts: 2000 }],
    subs: [{ id: 'p5-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Sub Activo 18"', coneSizeInches: 18, rmsWatts: 1000, peakWatts: 2000 }],
    power: { type: 'GENERATOR_WATTS', generatorSurgeWatts: 3500, driveRegime: 'MAX_TECHNO_1_3' },
  },
  {
    id: 'scale-6-matrimonio',
    scaleTag: '6. ESCALA MEDIA-ALTA',
    areaLabel: '14m × 22m (308 m²)',
    title: '💍 Matrimonio / Evento en Carpa',
    subtitle: '4 Cajas 800W (PA + Torres Delay) + 2 Subs 1200W · Tablero 20A',
    badgeClass: 'bg-purple-950 text-purple-300 border border-purple-700',
    venue: {
      name: 'Centro de Eventos Pirque (Carpa)',
      widthMeters: 14,
      depthMeters: 22,
      environmentType: 'INDOOR',
      electricalDistanceMeters: 30,
      eventDurationHours: 8,
    },
    tops: [{ id: 'p6-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 4, modelLabel: 'Top Activo 15"', coneSizeInches: 15, rmsWatts: 800, peakWatts: 1600 }],
    subs: [{ id: 'p6-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Sub Activo 18"', coneSizeInches: 18, rmsWatts: 1200, peakWatts: 2400 }],
    power: { type: 'GRID_220V', circuitBreakerAmps: '20', driveRegime: 'STANDARD_CLUB_1_5' },
  },
  {
    id: 'scale-7-warehouse-rave',
    scaleTag: '7. ESCALA ALTA (RAVE)',
    areaLabel: '15m × 28m (420 m²)',
    title: '🏭 Galpón Industrial Hard Techno',
    subtitle: '6 Tops Activos 1000W (2 Anillos Delay) + 4 Subs Pasivos 1500W (8Ω) · 25A',
    badgeClass: 'bg-red-950 text-red-300 border border-red-600',
    venue: {
      name: 'Galpón Industrial Estación Central',
      widthMeters: 15,
      depthMeters: 28,
      environmentType: 'INDOOR',
      electricalDistanceMeters: 40,
      eventDurationHours: 9,
    },
    tops: [{ id: 'p7-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 6, modelLabel: 'Top Activo 15"', coneSizeInches: 15, rmsWatts: 1000, peakWatts: 2000 }],
    subs: [{ id: 'p7-s1', category: 'sub_bass', systemType: 'PASSIVE', quantity: 4, modelLabel: 'Sub Pasivo 18"', coneSizeInches: 18, rmsWatts: 1500, peakWatts: 3000, impedanceOhms: 8 }],
    power: { type: 'GRID_220V', circuitBreakerAmps: '25', driveRegime: 'MAX_TECHNO_1_3' },
  },
  {
    id: 'scale-8-festival',
    scaleTag: '8. ESCALA FESTIVAL',
    areaLabel: '20m × 36m (720 m²)',
    title: '🎪 Escenario Open-Air / Predio Masivo',
    subtitle: '8 Tops Pasivos 1200W (3 Anillos Delay) + 4 Subs Activos 1800W · Gen 12 kVA',
    badgeClass: 'bg-amber-950 text-amber-300 border border-amber-500',
    venue: {
      name: 'Predio Open Air Lampa (Escenario Principal)',
      widthMeters: 20,
      depthMeters: 36,
      environmentType: 'OUTDOOR_PARCELA',
      electricalDistanceMeters: 48,
      eventDurationHours: 10,
    },
    tops: [{ id: 'p8-t1', category: 'top_box', systemType: 'PASSIVE', quantity: 8, modelLabel: 'Top Pasivo 15"', coneSizeInches: 15, rmsWatts: 1200, peakWatts: 2400, impedanceOhms: 8 }],
    subs: [{ id: 'p8-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 4, modelLabel: 'Sub Activo 18"', coneSizeInches: 18, rmsWatts: 1800, peakWatts: 3600 }],
    power: { type: 'GENERATOR_KVA', apparentPowerKva: 12, driveRegime: 'MAX_TECHNO_1_3' },
  },
];

function loadPreset(preset: DemoPreset) {
  activePresetId.value = preset.id;
  venue.name = preset.venue.name;
  venue.widthMeters = preset.venue.widthMeters;
  venue.depthMeters = preset.venue.depthMeters;
  venue.environmentType = preset.venue.environmentType;
  venue.electricalDistanceMeters = preset.venue.electricalDistanceMeters;
  venue.eventDurationHours = preset.venue.eventDurationHours;

  topBatches.value = JSON.parse(JSON.stringify(preset.tops));
  subBatches.value = JSON.parse(JSON.stringify(preset.subs));

  powerSource.type = preset.power.type;
  if (preset.power.circuitBreakerAmps) powerSource.circuitBreakerAmps = preset.power.circuitBreakerAmps;
  if (preset.power.generatorSurgeWatts) powerSource.generatorSurgeWatts = preset.power.generatorSurgeWatts;
  if (preset.power.apparentPowerKva) powerSource.apparentPowerKva = preset.power.apparentPowerKva;
  powerSource.driveRegime = preset.power.driveRegime;

  Object.keys(checkedItems).forEach(k => delete checkedItems[k]);
  validateData();
}

function clearForm() {
  activePresetId.value = null;
  venue.name = '';
  venue.widthMeters = undefined;
  venue.depthMeters = undefined;
  venue.electricalDistanceMeters = undefined;
  venue.eventDurationHours = undefined;
  topBatches.value = [
    { id: 'top-b1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Caja Activa 15"', coneSizeInches: 15, rmsWatts: 500, peakWatts: 1000, impedanceOhms: 8 },
  ];
  subBatches.value = [
    { id: 'sub-b1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 1, modelLabel: 'Sub Activo 18"', coneSizeInches: 18, rmsWatts: 800, peakWatts: 1600, impedanceOhms: 8 },
  ];
  powerSource.generatorSurgeWatts = undefined;
  powerSource.apparentPowerKva = undefined;
  Object.keys(checkedItems).forEach(k => delete checkedItems[k]);
  isValidated.value = false;
  validationMessage.value = '';
}

function toggleItemChecked(id: string) {
  checkedItems[id] = !checkedItems[id];
}

const checkedCount = computed(() => {
  return hybridAnalysis.value.roster.filter(r => checkedItems[r.id]).length;
});

function toggleAllChecked() {
  const allSelected = checkedCount.value === hybridAnalysis.value.roster.length;
  for (const r of hybridAnalysis.value.roster) {
    checkedItems[r.id] = !allSelected;
  }
}

function resetValidation() {
  if (isValidated.value) {
    isValidated.value = false;
    validationMessage.value = 'Se detectaron cambios. Confirma los datos en el Paso 2 para actualizar los cálculos.';
  }
}

function validateData() {
  const errors: string[] = [];

  if (!venue.name || venue.name.trim().length === 0) {
    errors.push('Ingresa el nombre del recinto o parcela (Paso 1).');
  }
  if (!venue.widthMeters || venue.widthMeters <= 0) {
    errors.push('El ancho del lugar debe ser mayor a 0 metros (Paso 1).');
  }
  if (!venue.depthMeters || venue.depthMeters <= 0) {
    errors.push('El largo del lugar debe ser mayor a 0 metros (Paso 1).');
  }
  if (!venue.electricalDistanceMeters || venue.electricalDistanceMeters <= 0) {
    errors.push('Indica cuántos metros hay hasta el enchufe o generador (Paso 1).');
  }

  const hasTops = totalTopsCount.value > 0 && totalTopsRmsWatts.value > 0;
  const hasSubs = totalSubsCount.value > 0 && totalSubsRmsWatts.value > 0;

  if (!hasTops && !hasSubs) {
    errors.push('Debes ingresar al menos 1 caja acústica o sub bajo con sus Watts RMS (Paso 2).');
  }

  if (powerSource.type === 'GENERATOR_WATTS' && (!powerSource.generatorSurgeWatts || powerSource.generatorSurgeWatts <= 0)) {
    errors.push('Indica los Watts del generador, por ejemplo 3500 (Paso 2).');
  }

  if (powerSource.type === 'GENERATOR_KVA' && (!powerSource.apparentPowerKva || powerSource.apparentPowerKva <= 0)) {
    errors.push('Indica la potencia en kVA del generador (Paso 2).');
  }

  if (errors.length > 0) {
    isValidated.value = false;
    validationMessage.value = errors.join(' ');
  } else {
    isValidated.value = true;
    validationMessage.value = `¡Parámetros confirmados! Superficie de ${venue.widthMeters! * venue.depthMeters!} m².`;
  }
}

// Motor reactivo de análisis de hardware híbrido, ubicación acústica inteligente y división de 2 Líneas Eléctricas
const hybridAnalysis = computed(() => {
  if (!isValidated.value) {
    return {
      roster: [],
      totalPowerWatts220v: 0,
      totalPeakWatts220v: 0,
      totalRmsAudioWatts: 0,
      totalPeakAudioWatts: 0,
      totalAmps220v: 0,
      activeTopsCount: 0,
      passiveTopsCount: 0,
      activeSubsCount: 0,
      passiveSubsCount: 0,
      frontTopsCount: 0,
      delayTopsCount: 0,
      externalAmpsRequiredCount: 0,
      powerCordsIecCount: 0,
      powerCordsPowerconCount: 0,
      speakonCablesCount: 0,
      xlrCablesCount: 0,
      totalFloorTapeMeters: 0,
      floorTapeRolls50m: 0,
      placementStrategySummary: '',
      recommendations: [],
      electricalLines: {
        line1SubsWatts: 0,
        line1SubsPeakWatts: 0,
        line1SubsAmps: 0,
        line2TopsCtrlWatts: 0,
        line2TopsCtrlPeakWatts: 0,
        line2TopsCtrlAmps: 0,
        phaseBalanceDirective: '',
      },
    };
  }

  const venueW = venue.widthMeters || 10;
  const venueD = venue.depthMeters || 16;

  // Generación inteligente desde lotes heterogéneos
  const items = generateSmartPlacementFromBatches({
    venueWidthM: venueW,
    venueDepthM: venueD,
    batches: allBatches.value,
    temperatureCelsius: venue.temperatureCelsius || 20,
  });

  const outlets = [
    { id: 'out-1', name: 'Enchufe Pared Izquierda', maxAmps: 16, maxWatts: 3520, posX: 0, posY: 2 },
    { id: 'out-2', name: 'Enchufe Pared Derecha', maxAmps: 16, maxWatts: 3520, posX: venueW, posY: 2 },
  ];

  return analyzeHybridRig(items, outlets, { x: venueW / 2, y: 1.2 });
});

// Innovación 4: Detector de Cuello de Botella Acústico (Top vs Sub Balance)
const topSubBottleneck = computed(() => {
  return evaluateTopToSubBalance({
    totalTopRmsWatts: totalTopsRmsWatts.value,
    totalSubRmsWatts: totalSubsRmsWatts.value,
    topsCount: totalTopsCount.value,
    subsCount: totalSubsCount.value,
  });
});

// MOTOR ELECTROACÚSTICO DUAL (STAGE ACOUSTIC ENGINE)
const stageAcousticResult = computed(() => {
  if (!isValidated.value) {
    return {
      frontSystem: {
        spl1mPeak: 0,
        spl1mContinuous: 0,
        splAtDistances: [],
        reverberationTimeRt60Seconds: undefined,
      },
      delayLineRecommendation: {
        required: false,
        triggerDistanceM: 0,
        delayTimeMs: 0,
        haasCompensationMs: 3.0,
        totalDelayMs: 0,
        notes: '',
      },
      tonalBalance: {
        subToTopRatioDb: 0,
        status: 'OPTIMAL' as const,
        boundaryGainAppliedDb: 6,
      },
      electricalRequirements: {
        realAudioConsumptionWatts: 0,
        totalActivePowerWatts: 0,
        apparentPowerVa: 0,
        minimumGeneratorKva: 0,
        nominalCurrentAmperes220V: 0,
      },
    };
  }

  const boxes: AudioBox[] = [];
  for (const b of topBatches.value) {
    if (b.quantity > 0 && b.rmsWatts > 0) {
      boxes.push({
        id: b.id,
        name: b.modelLabel || 'Caja Acústica',
        type: 'TOP',
        powerRms: b.rmsWatts,
        sensitivity: 98,
        potentiometerGainDb: 4,
        quantity: b.quantity,
      });
    }
  }
  for (const b of subBatches.value) {
    if (b.quantity > 0 && b.rmsWatts > 0) {
      boxes.push({
        id: b.id,
        name: b.modelLabel || 'Subwoofer',
        type: 'SUB',
        powerRms: b.rmsWatts,
        sensitivity: 97,
        potentiometerGainDb: 4,
        quantity: b.quantity,
      });
    }
  }

  const venueEnv: VenueEnvironment = {
    areaM2: (venue.widthMeters || 10) * (venue.depthMeters || 15),
    lengthM: venue.depthMeters || 15,
    widthM: venue.widthMeters || 10,
    heightM: venue.heightMeters || 3.5,
    temperatureCelsius: venue.temperatureCelsius || 20,
    targetSplDba: venue.targetSplDba || 102,
    environmentType: venue.environmentType === 'INDOOR' ? 'INDOOR_CLOSED' : 'OUTDOOR_OPEN',
    absorptionCoefficient: 0.18,
  };

  return StageAcousticEngine.calculate(boxes, venueEnv, 800);
});

// Innovación 5: Simulador de Ruido Exterior y Ordenanza Municipal (D.S. N° 38 MMA)
const neighborhoodNoiseAudit = computed(() => {
  return evaluateNeighborhoodNoise({
    spl1mContinuousDba: stageAcousticResult.value.frontSystem.spl1mContinuous || 116,
    neighborDistanceM: venue.neighborDistanceMeters || 30,
    enclosureType: venue.enclosureWallType || 'OPEN_AIR',
    scheduleShift: venue.scheduleShift || 'NIGHTTIME_21_07',
  });
});

// Evaluación de Factibilidad Eléctrica Real (Enchufe Domiciliario vs Generador en Watts/kVA + Régimen de Exigencia)
const powerFeasibility = computed(() => {
  const baseTechnoWatts = hybridAnalysis.value.totalPowerWatts220v;
  const audioOnlyTechno = Math.max(0, baseTechnoWatts - 800);

  const regimeMultiplier =
    powerSource.driveRegime === 'MAX_TECHNO_1_3'
      ? 1.0
      : powerSource.driveRegime === 'STANDARD_CLUB_1_5'
      ? 0.60
      : 0.38;

  const extraBoothAndLightWatts =
    lightingDmxAnalysis.value.totalLightingWatts + djSetupAnalysis.value.boothMonitorsTotal220vWatts;
  const adjustedDemandWatts = Math.round(audioOnlyTechno * regimeMultiplier + 800 + extraBoothAndLightWatts);
  // Usa Watts Peak reales calculados por los lotes si están disponibles
  const transientPeakWatts = hybridAnalysis.value.totalPeakWatts220v > 0
    ? Math.round(hybridAnalysis.value.totalPeakWatts220v * regimeMultiplier)
    : Math.round(adjustedDemandWatts * 2.1);

  if (powerSource.type === 'GRID_220V') {
    return PowerSourceValidator.evaluate(
      adjustedDemandWatts,
      {
        type: 'HOME_OUTLET',
        breakerAmps: Number(powerSource.circuitBreakerAmps) as 10 | 16 | 20 | 25 | 32,
        voltage: 220,
      },
      transientPeakWatts
    );
  } else if (powerSource.type === 'GENERATOR_WATTS') {
    return PowerSourceValidator.evaluate(
      adjustedDemandWatts,
      {
        type: 'GENERATOR',
        generatorSurgeWatts: powerSource.generatorSurgeWatts || 3500,
      },
      transientPeakWatts
    );
  } else {
    const kva = powerSource.apparentPowerKva || 5;
    const runningWatts = Math.round(kva * 1000 * powerSource.powerFactor);
    return PowerSourceValidator.evaluate(
      adjustedDemandWatts,
      {
        type: 'GENERATOR',
        generatorRunningWatts: runningWatts,
      },
      transientPeakWatts
    );
  }
});

const powerAlertLevel = computed(() => {
  if (!isValidated.value) return 'PENDIENTE';
  const st = powerFeasibility.value.status;
  if (st === 'CRITICAL_TRIP_GUARANTEED') return 'CRITICAL';
  if (st === 'WARNING_OVERLOAD_RISK') return 'WARNING';
  return 'NORMAL';
});

const fieldAudit = computed(() => {
  const continuousAmps = Number((powerFeasibility.value.totalSystemDemandWatts / (220 * 0.92)).toFixed(2));
  return evaluateFieldEngineering({
    venueWidthM: venue.widthMeters || 10,
    venueDepthM: venue.depthMeters || 16,
    electricalDistanceM: venue.electricalDistanceMeters || 25,
    continuousCurrentAmps: continuousAmps,
    isGenerator: powerSource.type !== 'GRID_220V',
    isOutdoor: venue.environmentType !== 'INDOOR',
    subsCount: totalSubsCount.value,
    driveRegime: powerSource.driveRegime,
    eventDurationHours: venue.eventDurationHours || 7,
  });
});

// Innovación 6: Resumen Copiable para WhatsApp
const whatsappCopied = ref(false);
function copyWhatsAppSummary() {
  const text = `🎧 *STAGE PLAN — FICHA TÉCNICA DE EVENTO*
📍 *Lugar:* ${venue.name || 'Evento'} (${venue.widthMeters}m × ${venue.depthMeters}m · ${venue.widthMeters! * venue.depthMeters!} m²)
👤 *Operador:* ${operatorSignature.value}

🔊 *SISTEMA DE AUDIO:*
• Tops: ${totalTopsCount.value} cajas (${totalTopsRmsWatts.value}W RMS / ${totalTopsPeakWatts.value}W Peak)
• Sub-Bajos: ${totalSubsCount.value} bajos en Cluster Central (${totalSubsRmsWatts.value}W RMS / ${totalSubsPeakWatts.value}W Peak)
• Retardo Delay: ${stageAcousticResult.value.delayLineRecommendation.required ? `${stageAcousticResult.value.delayLineRecommendation.totalDelayMs} ms Haas` : 'No requerido'}

⚡ *ENERGÍA & SEGURIDAD:*
• Fuente: ${powerSource.type === 'GRID_220V' ? `Enchufe ${powerSource.circuitBreakerAmps}A` : powerSource.type === 'GENERATOR_WATTS' ? `Generador ${powerSource.generatorSurgeWatts}W` : `Generador ${powerSource.apparentPowerKva} kVA`}
• Demanda: ${powerFeasibility.value.totalSystemDemandWatts}W continuos (${powerFeasibility.value.transientPeakWatts}W picos) — ${powerFeasibility.value.status}
• Cable Alargador: Mínimo ${fieldAudit.value.recommendedCableMm2} mm² a ${venue.electricalDistanceMeters}m
• División de Fases: Línea 1 Subs (${hybridAnalysis.value.electricalLines.line1SubsWatts}W) / Línea 2 Tops+DJ (${hybridAnalysis.value.electricalLines.line2TopsCtrlWatts}W)

📋 *Norma Ruido Vecinos (D.S. 38):* ~${neighborhoodNoiseAudit.value.estimatedNeighborDba} dBA a ${neighborhoodNoiseAudit.value.neighborDistanceM}m (${neighborhoodNoiseAudit.value.status})`;

  navigator.clipboard.writeText(text);
  whatsappCopied.value = true;
  setTimeout(() => { whatsappCopied.value = false; }, 3500);
}

function downloadPdf() {
  if (!isValidated.value) return;
  generateOperationalReportPdf({
    venue: {
      name: venue.name || 'Sin Nombre',
      widthMeters: venue.widthMeters || 10,
      depthMeters: venue.depthMeters || 10,
      heightMeters: venue.heightMeters || 3.5,
      environmentType: venue.environmentType as any,
      electricalDistanceMeters: venue.electricalDistanceMeters || 10,
    },
    rider: {
      audio: {
        systemType: topBatches.value.some(b => b.systemType === 'PASSIVE') ? 'PASSIVE' : 'ACTIVE',
        topsCount: totalTopsCount.value,
        topsRmsWatts: totalTopsRmsWatts.value,
        subsCount: totalSubsCount.value,
        subsRmsWatts: totalSubsRmsWatts.value,
        topsSensitivityDb: 98,
      },
      powerSource: powerSource as any,
      djBoothNominalWatts: 350,
    },
    results: {
      totalWatts: powerFeasibility.value.totalSystemDemandWatts,
      powerValidation: {
        alertLevel: powerAlertLevel.value as any,
        alertMessage: powerFeasibility.value.technicalDiagnosis,
      },
      cableSizing: {
        commercialCrossSectionMm2: fieldAudit.value.recommendedCableMm2,
        suggestedLengthMeters: venue.electricalDistanceMeters || 20,
        actualVoltageDropPct: Number(((fieldAudit.value.voltageDropContinuousV / 220) * 100).toFixed(2)),
        designCurrentAmps: Number((powerFeasibility.value.totalSystemDemandWatts / (220 * 0.92)).toFixed(2)),
        determiningCriterion: 'VOLTAGE_DROP',
      } as any,
      splCoverage: {
        spl1mDb: stageAcousticResult.value.frontSystem.spl1mContinuous,
        splAtFirstRowDb: stageAcousticResult.value.frontSystem.splAtDistances[1]?.splPeak || 112,
        splAtBackDb: stageAcousticResult.value.frontSystem.splAtDistances[stageAcousticResult.value.frontSystem.splAtDistances.length - 1]?.splPeak || 98,
        recommendDelayFill: stageAcousticResult.value.delayLineRecommendation.required,
        reverberationTimeRt60Seconds: stageAcousticResult.value.frontSystem.reverberationTimeRt60Seconds,
        soundSpeedMs: 343.4,
        delayTimeMs: stageAcousticResult.value.delayLineRecommendation.delayTimeMs,
        haasCompensationMs: stageAcousticResult.value.delayLineRecommendation.haasCompensationMs,
        totalDelayMs: stageAcousticResult.value.delayLineRecommendation.totalDelayMs,
        subToTopRatioDb: stageAcousticResult.value.tonalBalance.subToTopRatioDb,
        tonalStatus: stageAcousticResult.value.tonalBalance.status,
      },
      inventory: {
        subsAtFloorCount: totalSubsCount.value,
        tripodStandsCount: totalTopsCount.value,
        powerStripsCount: Math.max(1, Math.ceil(totalTopsCount.value / 3)),
      },
      hybridRoster: hybridAnalysis.value.roster.map(r => ({
        tag: r.tag,
        name: r.name,
        systemType: r.systemType,
        rmsWatts: r.rmsWatts,
        peakWatts: r.peakWatts,
        powerCableMeters: r.powerCableMeters,
        powerCableType: r.powerCableType,
        signalCableType: r.signalCableType,
        signalLengthMeters: r.signalLengthMeters,
        signalOrigin: r.signalOrigin,
        zoneLabel: `${r.zoneLabel} (X:${r.posX}m, Y:${r.posY}m)`,
        recommendedGainNote: r.recommendedGainNote,
      })),
      cablingSummary: {
        externalAmpsCount: hybridAnalysis.value.externalAmpsRequiredCount,
        speakonCount: hybridAnalysis.value.speakonCablesCount,
        xlrCount: hybridAnalysis.value.xlrCablesCount,
        tapeMeters: hybridAnalysis.value.totalFloorTapeMeters,
        tapeRolls50m: hybridAnalysis.value.floorTapeRolls50m,
      },
      v4EngineeringSummary: {
        phaseBalanceDirective: hybridAnalysis.value.electricalLines.phaseBalanceDirective,
        impedanceDirective: passiveImpedanceAudit.value.hasPassiveUnits ? passiveImpedanceAudit.value.technicalDirective : undefined,
        bottleneckDiagnosis: topSubBottleneck.value.bottleneckDiagnosis,
        neighborhoodNoiseDirective: neighborhoodNoiseAudit.value.mitigationDirective,
      },
      fieldAudit: fieldAudit.value,
      powerDistribution: powerDistributionPlan.value,
      lightingDmx: lightingDmxAnalysis.value,
      logistics: loadLogistics.value,
      djSetupAudio: djSetupAnalysis.value,
    },
    authorName: operatorSignature.value,
  });
}
</script>
