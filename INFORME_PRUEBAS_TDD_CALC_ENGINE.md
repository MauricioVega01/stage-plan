# Informe de Pruebas Unitarias y Aseguramiento TDD (v4.0)
**Asignatura:** Proyecto Integrado (`TIHV43`) — Analista Programador — INACAP Sede Maipú (Sección C1 · Grupo G10)  
**Subsistema:** `@stageplan/shared` (`calc-engine` + Esquemas Zod)  
**Resultado Verificado:** **81/81 Tests Pasados en 11 Suites (100% PASS)** | **0 errores de compilación TypeScript (`vue-tsc` + `tsc`)**

---

## 1. Resumen de Métricas de Calidad Obtenidas

| Métrica | Meta del Proyecto | Resultado Real Medido | Estado |
|---|:---:|:---:|:---:|
| **Pruebas Unitarias Aprobadas** | 100% | **81 / 81 (11 archivos)** | **CUMPLIDO** |
| **Tiempo de Ejecución de Tests** | < 5.0 s (tests) | **186 ms tests (7.65 s total)** | **CUMPLIDO** |
| **Benchmark Motor Completo (1.000 iters)** | < 50 ms SLA | **0,0286 ms promedio (p95: 0,0479 ms)** | **CUMPLIDO** |
| **Compilación Estática (`tsc` + `vue-tsc`)** | 0 errores | **0 errores en 3 workspaces** | **CUMPLIDO** |
| **Tests Flaky / Fallidos** | 0 | **0** | **CUMPLIDO** |

---

## 2. Distribución Actual de las 11 Suites Automatizadas (Vitest v3.2.7)

| Archivo de Prueba (`.spec.ts`) | Módulo / Alcance Validado | Tests | Tiempo | Estado |
|---|---|:---:|:---:|:---:|
| `calc-engine.spec.ts` | SEC RIC 03/10, caída de tensión, capacidad red/generador, soportes y SPL | **23** | 25 ms | **PASS** |
| `routing-and-gaffer.spec.ts` | Enrutamiento perimetral Manhattan, zapatillas Z1..Z y cinta Gaffer 50 m | **10** | 14 ms | **PASS** |
| `hybrid-roster.spec.ts` | Mezclas Activa/Pasiva, Asymmetric Rigging y **Rack de Potencias Pasivas (PA-01..PA-06)** | **8** | 30 ms | **PASS** |
| `power-distribution.spec.ts` | Distribución trifásica/monofásica L1/L2/L3 y protecciones 80% | **8** | 27 ms | **PASS** |
| `lighting-dmx.spec.ts` | Conteo unitario x1 de luminarias, carga térmica (hazer/blinders) y bus DMX512 | **8** | 21 ms | **PASS** |
| `contingency-logistics.spec.ts` | Plan de contingencia ante fallos, peso total y Ley del Saco N° 20.949 (> 25 kg) | **6** | 12 ms | **PASS** |
| `stage-acoustic-engine.spec.ts` | Clúster mono (+6 dB), retardos Haas, balance Top/Sub y cobertura SPL | **5** | 15 ms | **PASS** |
| `qa-gap-branches.spec.ts` | Cobertura de ramas borde en cálculos eléctricos, ruido D.S. N° 38 y validaciones | **5** | 14 ms | **PASS** |
| `dj-setup-audio.spec.ts` | Ruteo de cabina DJ (CDJ/XDJ, Pro DJ Link RJ45, Mixer DJM y Booth) | **4** | 12 ms | **PASS** |
| `stage-acoustic-indoor-outdoor.spec.ts` | Acústica de salas Sabine RT60 vs. campo libre en parcela | **2** | 8 ms | **PASS** |
| `cabling.spec.ts` | Selección automática de cables XLR, Speakon NL4, IEC C13 y PowerCON | **2** | 7 ms | **PASS** |
| **TOTAL GENERAL** | **Suite Completa `@stageplan/shared`** | **81** | **186 ms** | **100% PASS** |

---

## 3. Evidencia de Ejecución Real (`npm test`)

```text
RUN  v3.2.7 packages/shared

 ✓ tests/routing-and-gaffer.spec.ts (10 tests) 14ms
 ✓ tests/power-distribution.spec.ts (8 tests) 27ms
 ✓ tests/calc-engine.spec.ts (23 tests) 25ms
 ✓ tests/lighting-dmx.spec.ts (8 tests) 21ms
 ✓ tests/qa-gap-branches.spec.ts (5 tests) 14ms
 ✓ tests/hybrid-roster.spec.ts (8 tests) 30ms
 ✓ tests/stage-acoustic-engine.spec.ts (5 tests) 15ms
 ✓ tests/contingency-logistics.spec.ts (6 tests) 12ms
 ✓ tests/dj-setup-audio.spec.ts (4 tests) 12ms
 ✓ tests/stage-acoustic-indoor-outdoor.spec.ts (2 tests) 8ms
 ✓ tests/cabling.spec.ts (2 tests) 7ms

 Test Files  11 passed (11)
      Tests  81 passed (81)
   Duration  7.65s (tests 186ms)
```

---

## 4. Casos Numéricos Verificados de Referencia

1. **Caída de Tensión SEC RIC 03/10 (`HU02`):** Carga 1.800 W, 220 V, 30 m, holgura 20% → corriente de diseño 9,82 A, sección comercial 2,5 mm², caída real 4,12 V (1,87% ≤ 3%).
2. **Impedancia Speakon en Paralelo (`HU04`):** 2 cajas de 8 Ω → 4,0 Ω (seguro); 3 cajas de 8 Ω → 2,67 Ω (< 3,2 Ω) → alerta `DANGER_PROTECT_SHORT`.
3. **Rack de Potencias Pasivas (`PA-02`..`PA-06`):** 2 tops pasivos de 400 W RMS @ 8 Ω exigen 640 W RMS/canal (headroom 1,6×); 4 tops de 350 W RMS en paralelo @ 4 Ω exigen 1.120 W RMS/canal (*Crown XTi 4002 / Powersoft T604*) sumando consumo AC 220V al balance eléctrico.
4. **Ley del Saco N° 20.949 (`contingency-and-logistics`):** Equipos sobre 25 kg activan advertencia obligatoria de manipulación asistida entre 2 operarios.
