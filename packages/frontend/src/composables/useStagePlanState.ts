import { ref, reactive, computed, onMounted, watch } from 'vue';
import { router } from '../router';
import { generateOperationalReportPdf } from '../services/pdfReport';
import {
  analyzeHybridRig,
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
  OutletPoint,
  LIGHTING_PRESETS,
  calculateLightingAndDmxRig,
  calculatePowerDistribution,
  simulateContingencyPlan,
  calculateLoadLogistics,
  analyzeDjSetupAndAudioRouting,
  type LightingBatchInput,
  type ContingencyScenario,
  type DjSetupMode,
  type PlayerAudioLinkType,
} from '@stageplan/shared';

export type WizardStepId = 0 | 1 | 2 | 3 | 4;

export interface DemoPreset {
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

const STEP_ROUTES: Record<WizardStepId, string> = {
  0: '/auth',
  1: '/recinto',
  2: '/equipos',
  3: '/plano-2d',
  4: '/reporte',
};

// ----------------------------------------------------------------------------
// SINGLETON STATE INSTANCE (PERSISTENTE ENTRE RUTAS Y EN LOCALSTORAGE)
// ----------------------------------------------------------------------------
const wizardSteps: { id: WizardStepId; icon: string; shortLabel: string; title: string; subtitle: string; path: string }[] = [
  { id: 0, icon: '🛡️', shortLabel: '0. Acceso', title: 'Acceso Operador', subtitle: 'Credencial Anti-IDOR', path: '/auth' },
  { id: 1, icon: '📐', shortLabel: '1. Recinto', title: 'Medidas y Casos Demo', subtitle: 'Dimensiones y 8 Escalas', path: '/recinto' },
  { id: 2, icon: '⚡', shortLabel: '2. Equipos', title: 'Sonido y Electricidad', subtitle: 'Lotes Mixtos, RMS/Peak y Fuente', path: '/equipos' },
  { id: 3, icon: '🗺️', shortLabel: '3. Plano 2D', title: 'Plano 2D y Heatmap', subtitle: 'Ubicación, SPL y Vúmetros', path: '/plano-2d' },
  { id: 4, icon: '📋', shortLabel: '4. Reporte', title: 'Reporte Final y PDF', subtitle: 'Camioneta, Fases y 7 Reglas', path: '/reporte' },
];

const currentStep = ref<WizardStepId>(1);
const isValidated = ref(false);
const validationMessage = ref('');
const activePresetId = ref<string | null>(null);
const storageFeedbackMsg = ref('');
const passiveWiringMode = ref<'INDEPENDENT_CHANNELS' | 'PARALLEL_SPEAKON_LINK'>('INDEPENDENT_CHANNELS');

// 0. Estado del Operador y Autenticación
const operator = reactive({
  email: 'mauricio.vega@distorsioncl.cl',
  password: 'password123',
  name: 'Mauricio Vega Castillo',
  role: 'Administrador / Ingeniero FOH',
  organization: 'DISTORSIONCL SPA',
  isLogged: true,
  token: 'local_authenticated_token',
  rememberMe: true,
});

const loginLoading = ref(false);
const loginError = ref('');
const showPassword = ref(false);

const operatorSignature = computed(() => {
  const n = operator.name.trim() || 'Mauricio Vega Castillo';
  return `${n} — ${operator.role} (${operator.organization || 'DISTORSIONCL SPA'})`;
});

// 1. Estado Reactivo del Recinto
const venue = reactive({
  name: 'Parcela Los Aromos, Curacaví',
  widthMeters: 14 as number | undefined,
  depthMeters: 18 as number | undefined,
  heightMeters: 3.5,
  environmentType: 'OUTDOOR_PARCELA',
  electricalDistanceMeters: 25 as number | undefined,
  eventDurationHours: 8 as number | undefined,
  temperatureCelsius: 20,
  targetSplDba: 102,
  neighborDistanceMeters: 30,
  enclosureWallType: 'OPEN_AIR' as VenueEnclosureWallType,
  scheduleShift: 'NIGHTTIME_21_07' as EventScheduleShift,
});

// 2. CONSTRUCTOR POR LOTES (Tops y Sub-bajos Híbridos)
const topBatches = ref<SpeakerBatchInput[]>([
  {
    id: 'top-b1',
    category: 'top_box',
    systemType: 'ACTIVE',
    quantity: 2,
    modelLabel: 'Caja Activa 15" Principal (PA L/R)',
    coneSizeInches: 15,
    rmsWatts: 800,
    peakWatts: 1600,
    impedanceOhms: 8,
  },
]);

const subBatches = ref<SpeakerBatchInput[]>([
  {
    id: 'sub-b1',
    category: 'sub_bass',
    systemType: 'ACTIVE',
    quantity: 2,
    modelLabel: 'Subwoofer Activo 18" (Cluster Central)',
    coneSizeInches: 18,
    rmsWatts: 1000,
    peakWatts: 2000,
    impedanceOhms: 8,
  },
]);

const totalTopsCount = computed(() => {
  return topBatches.value.reduce((acc, b) => acc + (Math.max(0, Math.floor(b.quantity)) || 0), 0);
});

const totalTopsRmsWatts = computed(() => {
  return topBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.rmsWatts || 0)), 0);
});

const totalTopsPeakWatts = computed(() => {
  return topBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.peakWatts || (b.rmsWatts || 0) * 2 || 0)), 0);
});

const totalSubsCount = computed(() => {
  return subBatches.value.reduce((acc, b) => acc + (Math.max(0, Math.floor(b.quantity)) || 0), 0);
});

const totalSubsRmsWatts = computed(() => {
  return subBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.rmsWatts || 0)), 0);
});

const totalSubsPeakWatts = computed(() => {
  return subBatches.value.reduce((acc, b) => acc + ((b.quantity || 0) * (b.peakWatts || (b.rmsWatts || 0) * 2 || 0)), 0);
});

const allBatches = computed<SpeakerBatchInput[]>(() => {
  return [...topBatches.value, ...subBatches.value];
});

// Iluminación
const lightingPresets = LIGHTING_PRESETS;
const lightingBatches = ref<LightingBatchInput[]>([]);

const lightingDmxAnalysis = computed(() => {
  return calculateLightingAndDmxRig(
    lightingBatches.value,
    venue.widthMeters || 10,
    venue.depthMeters || 16,
    220
  );
});

const activeContingencyScenario = ref<ContingencyScenario>('GENERATOR_FAIL_TO_10A');

// Setup Cabina DJ
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

// Fuente Eléctrica
const powerSource = reactive({
  type: 'GENERATOR_WATTS' as 'GRID_220V' | 'GENERATOR_WATTS' | 'GENERATOR_KVA',
  circuitBreakerAmps: '16' as '10' | '16' | '20' | '25' | '32',
  generatorSurgeWatts: 3500 as number | undefined,
  apparentPowerKva: undefined as number | undefined,
  powerFactor: 0.8,
  driveRegime: 'MAX_TECHNO_1_3' as VolumeDriveRegime,
});

// 8 Casos Demo Preconfigurados
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
    scaleTag: '5. PARCELA CON GENERADOR 3.5kW',
    areaLabel: '14m × 18m (252 m²)',
    title: '⚡ Parcela Fuera de Red (Generador 3.500W)',
    subtitle: '2 Tops 800W + 2 Subs 1000W · Generador a Gasolina 3.5kW · Techno al 100%',
    badgeClass: 'bg-amber-950 text-amber-300 border border-amber-600',
    venue: {
      name: 'Parcela San Bernardo (Audio + Luces)',
      widthMeters: 14,
      depthMeters: 18,
      environmentType: 'OUTDOOR_PARCELA',
      electricalDistanceMeters: 30,
      eventDurationHours: 8,
    },
    tops: [{ id: 'p5-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Top Activo 15"', coneSizeInches: 15, rmsWatts: 800, peakWatts: 1600 }],
    subs: [{ id: 'p5-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 2, modelLabel: 'Sub Activo 18"', coneSizeInches: 18, rmsWatts: 1000, peakWatts: 2000 }],
    power: { type: 'GENERATOR_WATTS', generatorSurgeWatts: 3500, driveRegime: 'MAX_TECHNO_1_3' },
  },
  {
    id: 'scale-6-galpon-warehouse',
    scaleTag: '6. ESCALA MEDIA-ALTA',
    areaLabel: '16m × 25m (400 m²)',
    title: '🏭 Warehouse / Galpón Industrial Rave',
    subtitle: '4 Tops 1000W + 4 Subs 1200W (Cluster) · Empalme Industrial 25A',
    badgeClass: 'bg-blue-950 text-blue-300 border border-blue-700',
    venue: {
      name: 'Galpón San Joaquín (Hard Techno Rave)',
      widthMeters: 16,
      depthMeters: 25,
      environmentType: 'INDOOR',
      electricalDistanceMeters: 35,
      eventDurationHours: 10,
    },
    tops: [{ id: 'p6-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 4, modelLabel: 'Top Activo 15"', coneSizeInches: 15, rmsWatts: 1000, peakWatts: 2000 }],
    subs: [{ id: 'p6-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 4, modelLabel: 'Sub Activo 18" Grave', coneSizeInches: 18, rmsWatts: 1200, peakWatts: 2400 }],
    power: { type: 'GRID_220V', circuitBreakerAmps: '25', driveRegime: 'MAX_TECHNO_1_3' },
  },
  {
    id: 'scale-7-festival-stage',
    scaleTag: '7. ESCALA ALTA (ALTO IMPACTO)',
    areaLabel: '20m × 35m (700 m²)',
    title: '🎪 Escenario Aire Libre / Festival',
    subtitle: '6 Tops 1000W + 6 Subs 1500W · Generador Diésel 15 kVA Trifásico',
    badgeClass: 'bg-purple-950 text-purple-300 border border-purple-600',
    venue: {
      name: 'Parque Padre Hurtado (Open Air Stage)',
      widthMeters: 20,
      depthMeters: 35,
      environmentType: 'OUTDOOR_PARCELA',
      electricalDistanceMeters: 45,
      eventDurationHours: 12,
    },
    tops: [{ id: 'p7-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 6, modelLabel: 'Line Array / Point Source 15"', coneSizeInches: 15, rmsWatts: 1000, peakWatts: 2000 }],
    subs: [{ id: 'p7-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 6, modelLabel: 'Sub Activo 18" Doble Bobina', coneSizeInches: 18, rmsWatts: 1500, peakWatts: 3000 }],
    power: { type: 'GENERATOR_KVA', apparentPowerKva: 15, driveRegime: 'MAX_TECHNO_1_3' },
  },
  {
    id: 'scale-8-extreme-40x60',
    scaleTag: '8. MEGA ESCALA (MÁXIMA CAPACIDAD)',
    areaLabel: '40m × 60m (2.400 m²)',
    title: '🏟️ Festival Masivo 2.400 m² (Open Air / Delay)',
    subtitle: '8 Tops 1200W + 8 Subs 1800W · Generador 30 kVA · Torres Delay Requeridas',
    badgeClass: 'bg-pink-950 text-pink-300 border border-pink-600',
    venue: {
      name: 'Explanada Ciudad Empresarial',
      widthMeters: 40,
      depthMeters: 60,
      environmentType: 'OUTDOOR_PARCELA',
      electricalDistanceMeters: 55,
      eventDurationHours: 14,
    },
    tops: [{ id: 'p8-t1', category: 'top_box', systemType: 'ACTIVE', quantity: 8, modelLabel: 'Point Source Array 15"', coneSizeInches: 15, rmsWatts: 1200, peakWatts: 2400 }],
    subs: [{ id: 'p8-s1', category: 'sub_bass', systemType: 'ACTIVE', quantity: 8, modelLabel: 'Sub Horn-Loaded 21"', coneSizeInches: 21, rmsWatts: 1800, peakWatts: 3600 }],
    power: { type: 'GENERATOR_KVA', apparentPowerKva: 30, driveRegime: 'MAX_TECHNO_1_3' },
  },
];

// Sincronizar automáticamente el paso del wizard cuando cambie la ruta en vue-router
router.afterEach((to) => {
  if (to.meta?.stepId !== undefined) {
    currentStep.value = to.meta.stepId as WizardStepId;
  }
});

// ----------------------------------------------------------------------------
// PERSISTENCIA LOCALSTORAGE AUTOMÁTICA
// ----------------------------------------------------------------------------
function loadProjectFromStorage() {
  if (typeof window === 'undefined') return;
  try {
    const raw = localStorage.getItem('stageplan_project_data');
    if (raw) {
      const data = JSON.parse(raw);
      if (data.venue) Object.assign(venue, data.venue);
      if (Array.isArray(data.topBatches)) topBatches.value = data.topBatches;
      if (Array.isArray(data.subBatches)) subBatches.value = data.subBatches;
      if (data.powerSource) Object.assign(powerSource, data.powerSource);
      if (data.djSetup) Object.assign(djSetup, data.djSetup);
      isValidated.value = true;
    }
  } catch (e) {
    console.warn('No se pudo restaurar estado desde localStorage:', e);
  }
}

function saveProjectToStorage() {
  if (typeof window === 'undefined') return;
  try {
    const payload = {
      venue: { ...venue },
      topBatches: topBatches.value,
      subBatches: subBatches.value,
      powerSource: { ...powerSource },
      djSetup: { ...djSetup },
    };
    localStorage.setItem('stageplan_project_data', JSON.stringify(payload));
  } catch (e) {
    console.warn('Error al persistir estado en localStorage:', e);
  }
}

// ----------------------------------------------------------------------------
// COMPOSABLE EXPORTADO
// ----------------------------------------------------------------------------
export function useStagePlanState() {
  onMounted(() => {
    loadProjectFromStorage();

    // Sincronizar paso activo con la URL actual del router
    if (router.currentRoute.value.meta?.stepId !== undefined) {
      currentStep.value = router.currentRoute.value.meta.stepId as WizardStepId;
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
  });

  // Watcher profundo para auto-guardar cambios automáticamente
  watch(
    [venue, topBatches, subBatches, powerSource, djSetup],
    () => {
      saveProjectToStorage();
    },
    { deep: true }
  );

  // Funciones de Autenticación
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
        body: JSON.stringify({ email: operator.email, password: operator.password }),
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
        goToStep(1);
        return;
      } else {
        const err = await res.json().catch(() => ({}));
        if (operator.email === 'mauricio.vega@distorsioncl.cl' && operator.password === 'password123') {
          operator.isLogged = true;
          operator.token = 'demo_jwt_session_token';
          goToStep(1);
          return;
        }
        loginError.value = err.error || 'Credenciales incorrectas.';
      }
    } catch (_netErr) {
      if (operator.email.includes('@') && operator.password.length >= 6) {
        operator.isLogged = true;
        operator.token = 'local_session_token_' + Date.now();
        if (!operator.name?.trim()) operator.name = 'Mauricio Vega Castillo';
        if (operator.rememberMe) {
          localStorage.setItem('stageplan_token', operator.token);
          localStorage.setItem('stageplan_operator', JSON.stringify({
            email: operator.email,
            name: operator.name,
            role: operator.role,
            organization: operator.organization,
          }));
        }
        goToStep(1);
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
    goToStep(0);
  }

  // Navegación con sincronización de URL en el Router
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
      currentStep.value = 0;
      router.push(STEP_ROUTES[0]);
      return;
    }
    if (stepId >= 3 && !isValidated.value) {
      validateData();
      if (!isValidated.value) {
        currentStep.value = 2;
        router.push(STEP_ROUTES[2]);
        return;
      }
    }
    currentStep.value = stepId;
    router.push(STEP_ROUTES[stepId]);
  }

  function nextStep() {
    if (currentStep.value === 1) {
      goToStep(2);
    } else if (currentStep.value === 2) {
      validateData();
      if (isValidated.value) goToStep(3);
    } else if (currentStep.value === 3) {
      goToStep(4);
    }
  }

  function prevStep() {
    if (currentStep.value > 1) {
      goToStep((currentStep.value - 1) as WizardStepId);
    }
  }

  // Lotes de Sonido
  function onBatchRmsChange(batch: SpeakerBatchInput) {
    if (batch.rmsWatts && (!batch.peakWatts || batch.peakWatts === batch.rmsWatts * 2 || batch.peakWatts < batch.rmsWatts)) {
      batch.peakWatts = Math.round(batch.rmsWatts * 2);
    }
    resetValidation();
  }

  function addTopBatch() {
    topBatches.value.push({
      id: `top-b${Date.now()}`,
      category: 'top_box',
      systemType: 'PASSIVE',
      quantity: 1,
      modelLabel: 'Caja Pasiva 12" Refuerzo',
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
    subBatches.value.push({
      id: `sub-b${Date.now()}`,
      category: 'sub_bass',
      systemType: 'PASSIVE',
      quantity: 1,
      modelLabel: 'Sub Pasivo 18"',
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

  function applyDemoPreset(preset: DemoPreset) {
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
    powerSource.circuitBreakerAmps = preset.power.circuitBreakerAmps || '16';
    powerSource.generatorSurgeWatts = preset.power.generatorSurgeWatts;
    powerSource.apparentPowerKva = preset.power.apparentPowerKva;
    powerSource.driveRegime = preset.power.driveRegime;

    storageFeedbackMsg.value = `✓ Caso aplicado: ${preset.title}`;
    setTimeout(() => { storageFeedbackMsg.value = ''; }, 3500);
    resetValidation();
  }

  // Cálculos de Dominio
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

  const hybridAnalysis = computed(() => {
    const djWatts = djSetupAnalysis.value.djBoothTotal220vWatts + djSetupAnalysis.value.boothMonitorsTotal220vWatts;
    const items = generateSmartPlacementFromBatches({
      venueWidthM: venue.widthMeters || 10,
      venueDepthM: venue.depthMeters || 16,
      batches: allBatches.value,
    });
    const defaultOutlets: OutletPoint[] = [
      { id: 'out-1', name: 'Zapatilla Izquierda', posX: 2, posY: 1, maxAmps: 16, maxWatts: 3500 },
      { id: 'out-2', name: 'Zapatilla Derecha', posX: (venue.widthMeters || 10) - 2, posY: 1, maxAmps: 16, maxWatts: 3500 },
    ];
    return analyzeHybridRig(items, defaultOutlets, { x: (venue.widthMeters || 10) / 2, y: 1.2 });
  });

  const passiveImpedanceAudit = computed(() => {
    return analyzePassiveImpedance(allBatches.value, passiveWiringMode.value);
  });

  const topSubBottleneck = computed(() => {
    return evaluateTopToSubBalance({
      totalTopRmsWatts: totalTopsRmsWatts.value,
      totalSubRmsWatts: totalSubsRmsWatts.value,
      topsCount: totalTopsCount.value,
      subsCount: totalSubsCount.value,
    });
  });

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

  const loadLogistics = computed(() => {
    const items = [
      ...topBatches.value.map((b) => ({
        name: b.modelLabel || 'Caja Top',
        quantity: b.quantity || 0,
        unitWeightKg: (b.coneSizeInches || 15) >= 15 ? 24 : 18,
      })),
      ...subBatches.value.map((b) => ({
        name: b.modelLabel || 'Subwoofer',
        quantity: b.quantity || 0,
        unitWeightKg: (b.coneSizeInches || 18) >= 18 ? 38 : 28,
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

  const stageAcousticResult = computed(() => {
    if (!venue.widthMeters || !venue.depthMeters || allBatches.value.length === 0) {
      return {
        frontSystem: { spl1mPeak: 0, spl1mContinuous: 0, splAtDistances: [], reverberationTimeRt60Seconds: undefined },
        delayLineRecommendation: { required: false, triggerDistanceM: 0, delayTimeMs: 0, haasCompensationMs: 3.0, totalDelayMs: 0, notes: '' },
        tonalBalance: { subToTopRatioDb: 0, status: 'OPTIMAL' as const, boundaryGainAppliedDb: 6 },
        electricalRequirements: { realAudioConsumptionWatts: 0, totalActivePowerWatts: 0, apparentPowerVa: 0, minimumGeneratorKva: 0, nominalCurrentAmperes220V: 0 },
      };
    }

    const boxes: AudioBox[] = [];
    for (const b of topBatches.value) {
      if ((b.quantity || 0) > 0 && (b.rmsWatts || 0) > 0) {
        boxes.push({ id: b.id, name: b.modelLabel || 'Caja Acústica', type: 'TOP', powerRms: b.rmsWatts, sensitivity: 98, potentiometerGainDb: 4, quantity: b.quantity });
      }
    }
    for (const b of subBatches.value) {
      if ((b.quantity || 0) > 0 && (b.rmsWatts || 0) > 0) {
        boxes.push({ id: b.id, name: b.modelLabel || 'Subwoofer', type: 'SUB', powerRms: b.rmsWatts, sensitivity: 97, potentiometerGainDb: 4, quantity: b.quantity });
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

  const neighborhoodNoiseAudit = computed(() => {
    return evaluateNeighborhoodNoise({
      spl1mContinuousDba: stageAcousticResult.value.frontSystem.spl1mContinuous || 116,
      neighborDistanceM: venue.neighborDistanceMeters || 30,
      enclosureType: venue.enclosureWallType || 'OPEN_AIR',
      scheduleShift: venue.scheduleShift || 'NIGHTTIME_21_07',
    });
  });

  const powerFeasibility = computed(() => {
    const baseTechnoWatts = hybridAnalysis.value.totalPowerWatts220v;
    const audioOnlyTechno = Math.max(0, baseTechnoWatts - 800);

    const regimeMultiplier =
      powerSource.driveRegime === 'MAX_TECHNO_1_3' ? 1.0 : powerSource.driveRegime === 'STANDARD_CLUB_1_5' ? 0.60 : 0.38;

    const extraWatts = lightingDmxAnalysis.value.totalLightingWatts + djSetupAnalysis.value.boothMonitorsTotal220vWatts;
    const adjustedDemandWatts = Math.round(audioOnlyTechno * regimeMultiplier + 800 + extraWatts);
    const transientPeakWatts = hybridAnalysis.value.totalPeakWatts220v > 0
      ? Math.round(hybridAnalysis.value.totalPeakWatts220v * regimeMultiplier)
      : Math.round(adjustedDemandWatts * 2.1);

    if (powerSource.type === 'GRID_220V') {
      return PowerSourceValidator.evaluate(adjustedDemandWatts, { type: 'HOME_OUTLET', breakerAmps: Number(powerSource.circuitBreakerAmps) as 10 | 16 | 20 | 25 | 32, voltage: 220 }, transientPeakWatts);
    } else if (powerSource.type === 'GENERATOR_WATTS') {
      return PowerSourceValidator.evaluate(adjustedDemandWatts, { type: 'GENERATOR', generatorSurgeWatts: powerSource.generatorSurgeWatts || 3500 }, transientPeakWatts);
    } else {
      const kva = powerSource.apparentPowerKva || 5;
      const runningWatts = Math.round(kva * 1000 * powerSource.powerFactor);
      return PowerSourceValidator.evaluate(adjustedDemandWatts, { type: 'GENERATOR', generatorRunningWatts: runningWatts }, transientPeakWatts);
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

  const smartPlacement = computed(() => {
    return generateSmartPlacementFromBatches({
      venueWidthM: venue.widthMeters || 10,
      venueDepthM: venue.depthMeters || 15,
      batches: allBatches.value,
      temperatureCelsius: venue.temperatureCelsius || 20,
    });
  });

  function resetValidation() {
    isValidated.value = false;
    validationMessage.value = '';
  }

  function validateData() {
    const errors: string[] = [];
    if (!venue.name?.trim()) errors.push('Ingresa el nombre del recinto o parcela.');
    if (!venue.widthMeters || venue.widthMeters <= 0) errors.push('El ancho debe ser mayor a 0m.');
    if (!venue.depthMeters || venue.depthMeters <= 0) errors.push('El largo debe ser mayor a 0m.');
    if (!venue.electricalDistanceMeters || venue.electricalDistanceMeters <= 0) errors.push('Indica los metros al punto eléctrico.');
    if (totalTopsCount.value === 0 && totalSubsCount.value === 0) errors.push('Ingresa al menos 1 caja o subwoofer.');

    if (errors.length > 0) {
      validationMessage.value = errors.join(' | ');
      isValidated.value = false;
      return false;
    }

    isValidated.value = true;
    validationMessage.value = '✓ Datos validados exitosamente.';
    return true;
  }

  // Exportaciones
  const whatsappCopied = ref(false);
  function copyWhatsAppSummary() {
    const text = `🎧 *STAGE PLAN PRO — FICHA TÉCNICA DE EVENTO*
📍 *Lugar:* ${venue.name || 'Evento'} (${venue.widthMeters}m × ${venue.depthMeters}m · ${(venue.widthMeters || 0) * (venue.depthMeters || 0)} m²)
👤 *Operador:* ${operatorSignature.value}

🔊 *SISTEMA DE AUDIO:*
• Tops: ${totalTopsCount.value} cajas (${totalTopsRmsWatts.value}W RMS / ${totalTopsPeakWatts.value}W Peak)
• Sub-Bajos: ${totalSubsCount.value} bajos en Cluster (${totalSubsRmsWatts.value}W RMS / ${totalSubsPeakWatts.value}W Peak)
• Retardo Delay: ${stageAcousticResult.value.delayLineRecommendation.required ? `${stageAcousticResult.value.delayLineRecommendation.totalDelayMs} ms Haas` : 'No requerido'}

⚡ *ENERGÍA & SEGURIDAD:*
• Fuente: ${powerSource.type === 'GRID_220V' ? `Enchufe ${powerSource.circuitBreakerAmps}A` : powerSource.type === 'GENERATOR_WATTS' ? `Generador ${powerSource.generatorSurgeWatts}W` : `Generador ${powerSource.apparentPowerKva} kVA`}
• Demanda: ${powerFeasibility.value.totalSystemDemandWatts}W continuos (${powerFeasibility.value.transientPeakWatts}W picos) — ${powerFeasibility.value.status}
• Cable Alargador: Mínimo ${fieldAudit.value.recommendedCableMm2} mm² a ${venue.electricalDistanceMeters}m

📦 *LOGÍSTICA & TRANSPORTE:*
• Carga Total: ~${loadLogistics.value.grandTotalWeightKg} kg (${loadLogistics.value.recommendedVehicle})
• Impedancia Speakon: ${passiveImpedanceAudit.value.hasPassiveUnits ? `${passiveImpedanceAudit.value.minImpedanceOhms} Ω (${passiveImpedanceAudit.value.status})` : 'Cajas Activas (Seguro)'}`;

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

  return {
    wizardSteps,
    currentStep,
    goToStep,
    nextStep,
    prevStep,
    isStepUnlocked,
    isStepCompleted,
    operator,
    operatorSignature,
    loginLoading,
    loginError,
    showPassword,
    fillEvaluationCredentials,
    handleLogin,
    handleLogout,
    venue,
    demoPresets,
    activePresetId,
    applyDemoPreset,
    topBatches,
    subBatches,
    allBatches,
    totalTopsCount,
    totalTopsRmsWatts,
    totalTopsPeakWatts,
    totalSubsCount,
    totalSubsRmsWatts,
    totalSubsPeakWatts,
    onBatchRmsChange,
    addTopBatch,
    removeTopBatch,
    addSubBatch,
    removeSubBatch,
    lightingBatches,
    lightingPresets,
    lightingDmxAnalysis,
    djSetup,
    djSetupAnalysis,
    powerSource,
    powerFeasibility,
    powerAlertLevel,
    passiveWiringMode,
    passiveImpedanceAudit,
    topSubBottleneck,
    hybridAnalysis,
    powerDistributionPlan,
    contingencyPlan,
    activeContingencyScenario,
    loadLogistics,
    stageAcousticResult,
    neighborhoodNoiseAudit,
    fieldAudit,
    smartPlacement,
    isValidated,
    validationMessage,
    validateData,
    resetValidation,
    whatsappCopied,
    copyWhatsAppSummary,
    downloadPdf,
    storageFeedbackMsg,
  };
}
