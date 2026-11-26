# CASO DE SIMULACIÓN ACÚSTICA: CÁLCULO DE SPL Y REFUERZOS (DELAY)
**Proyecto Integrado (`TIHV43`) — Analista Programador — INACAP Sede Maipú (Sección C1 · Grupo G10)**  
**Sistema:** STAGE PLAN (v4.0) — Módulo `calc-engine/stage-acoustic-engine`  
**Objetivo:** Demostración paso a paso de la pérdida de presión sonora y activación técnica de cajas de refuerzo (*delay line*).

---

## 1. ESCENARIO DE SIMULACIÓN (EL CASO REAL FICTICIO)

- **Evento:** *"Sunset Electronic Festival 2026"*
- **Cliente:** Productora y Arriendo de Audio DISTORSIONCL SPA.
- **Recinto:** Parcela al aire libre en **Curacaví, Región Metropolitana**.
- **Dimensiones del espacio de audiencia:**
  - Ancho de pista: $12\text{ metros}$.
  - Profundidad total: $28\text{ metros}$.
  - Entorno: Exterior / Parcela (`OUTDOOR_PARCELA`).
- **Sistema de Audio Principal (FOH) propuesto inicialmente:**
  - 2 Cajas Top activas de 2 vías ($12''$).
  - Potencia RMS: $500\text{ W}$ por caja.
  - Sensibilidad nominal del fabricante: $98\text{ dB @ 1W/1m}$.
- **Requerimiento Operativo (Estándar DJ):**
  - Mantener un nivel mínimo de **$98\text{ dB SPL}$** en toda la zona de baile.
  - Diferencia máxima de volumen admisible entre la primera fila y el fondo: **$\le 10\text{ dB}$**.

---

## 2. FORMULACIÓN MATEMÁTICA (LEY DEL INVERSO DEL CUADRADO)

En un entorno al aire libre (campo libre sin paredes reflectantes), la presión sonora decae según la **Ley del Inverso del Cuadrado**:

$$\text{SPL}(d) = \text{Sensibilidad} + 10 \cdot \log_{10}(P_{\text{RMS}}) - 20 \cdot \log_{10}(d)$$

Donde:
- $\text{Sensibilidad}$: $98\text{ dB @ 1W/1m}$
- $P_{\text{RMS}}$: Potencia en Watts continuos ($500\text{ W}$)
- $d$: Distancia en metros desde la fuente sonora hasta el oyente.

---

## 3. PASO A PASO: EJECUCIÓN DEL MOTOR `calc-engine`

```
 [ESCENARIO] ──────────────────────────────────────────────────────────┐
 │  CABINA DJ                                                          │
 │  [TOP L]                           [TOP R]                          │
 └─────┬─────────────────────────────────┬─────────────────────────────┘
       │ d = 1m: 125.0 dB                │
       ▼                                 ▼
   ══════════════════════════════════════════════════════ Primera Fila (d = 4m)
       SPL = 113.0 dB  (Nivel Óptimo / Confortable)
       │
       │  Atenuación: -6 dB por cada duplicación de distancia
       ▼
   ------------------------------------------------------ Mitad de Pista (d = 14m)
       SPL = 102.1 dB
       │
       ▼
   ══════════════════════════════════════════════════════ Fondo de Audiencia (d = 28m)
       SPL = 96.1 dB   ❌ [BAJO EL OBJETIVO DE 98 dB]
       Caída Fila - Fondo = 16.9 dB ❌ [SUPERA EL UMBRAL DE 10 dB]
```

### Paso A: Nivel SPL a 1 metro de la fuente
$$\text{Ganancia de Potencia} = 10 \cdot \log_{10}(500) \approx 10 \cdot 2.69897 = +26.99\text{ dB}$$
$$\text{SPL a 1m} = 98 + 26.99 = \mathbf{125.0\text{ dB SPL}}$$

### Paso B: Nivel SPL en la Primera Fila ($d = 4\text{ metros}$)
$$\text{Pérdida por distancia} = 20 \cdot \log_{10}(4) \approx 20 \cdot 0.60206 = -12.04\text{ dB}$$
$$\text{SPL}_{\text{1° fila}} = 125.0 - 12.04 = \mathbf{113.0\text{ dB SPL}}$$
*(Nivel potente y seguro para una pista de música electrónica).*

### Paso C: Nivel SPL en el Fondo del Salón ($d = 28\text{ metros}$)
$$\text{Pérdida por distancia} = 20 \cdot \log_{10}(28) \approx 20 \cdot 1.44716 = -28.94\text{ dB}$$
$$\text{SPL}_{\text{fondo}} = 125.0 - 28.94 = \mathbf{96.1\text{ dB SPL}}$$

---

## 4. DIAGNÓSTICO ALGORÍTMICO Y EVALUACIÓN DE CRITERIOS

El motor compara los resultados obtenidos contra los 3 criterios normativos de STAGE PLAN:

| Criterio Evaluado | Umbral de Seguridad | Valor Calculado | ¿Aprueba o Falla? |
|---|:---:|:---:|:---:|
| **1. Caída entre 1° fila y fondo** | Máximo $10.0\text{ dB}$ | $\mathbf{16.9\text{ dB}}$ ($113.0 - 96.1$) | ❌ **FALLA (Brecha excesiva)** |
| **2. Presión sonora mínima en fondo** | Mínimo $98.0\text{ dB}$ | $\mathbf{96.1\text{ dB}}$ | ❌ **FALLA (Volumen insuficiente)** |
| **3. Distancia máxima sin absorción de agudos** | Máximo $20.0\text{ m}$ (Exterior) | $\mathbf{28.0\text{ m}}$ | ❌ **FALLA (Aire absorbe agudos)** |

### Salida del Sistema STAGE PLAN:
```json
{
  "splAt1mDb": 125.0,
  "splAtFirstRowDb": 113.0,
  "splAtBackDb": 96.1,
  "splDropFirstRowToBackDb": 16.9,
  "recommendDelayFill": true,
  "recommendationReason": [
    "La caída sonora entre la primera fila y el fondo (16.9 dB) supera el umbral confortable de 10.0 dB.",
    "El nivel de presión sonora en el fondo (96.1 dB) está por debajo de los 98.0 dB requeridos para una experiencia DJ envolvente.",
    "La distancia de fondo (28 m) excede el alcance óptimo de agudos (20 m) por absorción de aire. Se requiere línea de retardo (delay)."
  ]
}
```

---

## 5. SOLUCIÓN TÉCNICA PROPUESTA POR STAGE PLAN: LÍNEA DE RETARDO (DELAY)

Para resolver la falla sin tener que subir el volumen en la cabina (lo que dejaría sorda a la primera fila con más de $120\text{ dB}$), el sistema recomienda implementar una **Línea de Refuerzo / Delay**:

### 5.1 Ubicación Física del Refuerzo
- Se instalan **2 cajas top secundarias** sobre atriles trípode a los **$14\text{ metros}$** de distancia (mitad de pista).
- En este punto ($14\text{ m}$), el sistema principal ya había caído a $102.1\text{ dB}$. La nueva caja de refuerzo suma presión acústica y restituye la cobertura en la segunda mitad del recinto, llevando el fondo nuevamente a **$103\text{ dB}$**.

### 5.2 Ajuste Temporal en Milisegundos (Cálculo del Retardo)
El sonido viaja por el aire a una velocidad aproximada de:
$$v_{\text{sonido}} \approx 343\text{ m/s} \quad (\text{a } 20^\circ\text{C})$$

El tiempo que tarda el sonido del escenario principal en llegar a la torre de refuerzo ($14\text{ metros}$) es:
$$t_{\text{delay}} = \frac{\text{Distancia}}{v_{\text{sonido}}} = \frac{14\text{ m}}{343\text{ m/s}} \approx 0.0408\text{ s} = \mathbf{40.8\text{ milisegundos}}$$

> **Regla de Oro en Terreno:** En el procesador de audio (DSP o consola), se aplica un retardo de **$41\text{ ms}$** (+ $2\text{ ms}$ de efecto Haas para fijar la imagen sonora en el escenario principal). De esta manera, el sonido de los parlantes de refuerzo y el del escenario llegan al oído del público **exactamente al mismo tiempo**, evitando ecos molestos (*flanging* o desfase).

---

## 6. IMPACTO LOGÍSTICO Y ELÉCTRICO REPORTADO EN EL PDF

Al activar el refuerzo de 2 cajas top adicionales en la línea de delay, STAGE PLAN actualiza automáticamente las otras secciones del reporte:

1. **Checklist de Soportes:**
   - De 2 atriles trípode pasa a **4 atriles trípode** reglamentarios con pasador de seguridad.
2. **Distribución Eléctrica:**
   - Suma 2 tomas de corriente adicionales en la zona media de la pista.
   - Si se alimentan desde el escenario, advierte que se requiere una tirada de alargador de **$15\text{ metros}$** con sección comercial de **$2.5\text{ mm}^2$** para evitar caídas de tensión acumuladas.
3. **Protocolo en el PDF:**
   - Añade el recordatorio: *"Alinear fase y retardo en milisegundos de la línea de delay antes de iniciar la prueba de sonido."*

