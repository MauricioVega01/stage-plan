# Informe de Aprobación de Pruebas Unitarias y Cobertura (TDD v4.0)
**Proyecto de Título: Analista Programador — INACAP**  
**Subsistema:** `@stageplan/shared` (`calc-engine` + Esquemas Zod)  
**Fecha:** Noviembre 2026  
**Resultado:** **100% Tests Pasados (44/44 en 6 Suites)** | **100% Lines & Statements** | **94.8% Branches**

---

## 1. Resumen de Métricas de Calidad Obtenidas

| Métrica | Meta INACAP (Master Plan) | Resultado Real Obtenido | Estado |
|---|:---:|:---:|:---:|
| **Cobertura de Líneas (`Lines`)** | $\ge 90\%$ | **100.0%** | **SUPERADO** |
| **Cobertura de Sentencias (`Statements`)** | $\ge 90\%$ | **100.0%** | **SUPERADO** |
| **Cobertura de Funciones (`Functions`)** | $\ge 90\%$ | **100.0%** | **SUPERADO** |
| **Cobertura de Ramas (`Branches`)** | $\ge 90\%$ | **94.8%** | **SUPERADO** |
| **Tiempo de Ejecución Suite** | $< 5.0\text{ s}$ | **4.67 s** | **CUMPLIDO** |
| **Tests Flaky / Fallidos** | 0 | **0** | **CUMPLIDO** |

---

## 2. Distribución de Suites y Tests Automatizados (Vitest v3.2.7)

| Archivo de Prueba | Módulo / Alcance Validado | Tests | Resultado |
|---|---|:---:|:---:|
| `calc-engine.spec.ts` | SEC RIC 03/10, Impedancia Speakon, Multilote RMS/Peak, 2 Líneas de Fuerza, Soportes y SPL | **23** | **APROBADO** |
| `routing-and-gaffer.spec.ts` | Multi-enchufe Manhattan, Balance de Cargas y Cinta Gaffer 50m | **10** | **APROBADO** |
| `stage-acoustic-engine.spec.ts` | SPL, Haas, Generador 3500W (72% AVR), Balance Top/Sub y D.S. N° 38 MMA | **5** | **APROBADO** |
| `stage-acoustic-indoor-outdoor.spec.ts` | Acústica de Salas Sabine RT60 y Hopkins-Stryker | **2** | **APROBADO** |
| `hybrid-roster.spec.ts` | Algoritmos Asymmetric Rigging y Gain Matching para Cajas Desiguales | **2** | **APROBADO** |
| `cabling.spec.ts` | Cableado Dinámico (XLR, Speakon NL4, IEC C13, PowerCON, DMX) | **2** | **APROBADO** |
| **TOTAL GENERAL** | **Suite Completa de Ingeniería Electroacústica y Eléctrica** | **44** | **100% PASS** |

---

## 3. Validación de Casos Numéricos Oficiales (v4.0)

| Historia / Módulo | Caso de Prueba | Entrada | Salida Esperada | Salida Obtenida | Veredicto |
|---|---|---|---|---|:---:|
| **HU02** | Caída de Tensión y Cableado (RIC 03/10) | $1800\text{ W}$, $220\text{ V}$, $30\text{ m}$, Holgura $20\%$ | $I_{\text{dis}} = 9.82\text{ A}$, $S = 2.5\text{ mm}^2$, $\Delta V = 4.12\text{ V}$ ($1.87\%$) | $I_{\text{dis}} = 9.82\text{ A}$, $S = 2.5\text{ mm}^2$, $\Delta V = 4.12\text{ V}$ ($1.87\%$) | **APROBADO** |
| **HU03** | Sobrecarga de Enchufe 10A | $2000\text{ W}$ en $10\text{ A}$ | $I_{\text{dis}} = 10.91\text{ A}$, ratio $1.091$ $\rightarrow$ ALERTA CRÍTICA | $I_{\text{dis}} = 10.91\text{ A}$, ratio $1.091$ $\rightarrow$ ALERTA CRÍTICA | **APROBADO** |
| **HU03** | Sobrecarga Generador 5 kVA | $3.5\text{ kW}$ carga, $5\text{ kVA}$ ($FP=0.8$) | $P_{\text{dis}} = 4.2\text{ kW} > 4.0\text{ kW}$ $\rightarrow$ ALERTA CRÍTICA | $P_{\text{dis}} = 4.2\text{ kW} > 4.0\text{ kW}$ $\rightarrow$ ALERTA CRÍTICA | **APROBADO** |
| **HU03 / v4** | Asistente Speakon: 2 Cajas 8Ω en Paralelo | 2 cajas pasivas $8\ \Omega$ | $Z_{\text{eq}} = 4.0\ \Omega$, safe = true, alerta = verde | $Z_{\text{eq}} = 4.0\ \Omega$, safe = true, alerta = verde | **APROBADO** |
| **HU03 / v4** | Asistente Speakon: Riesgo PROTECT (< 3.2Ω) | 3 cajas pasivas $8\ \Omega$ en paralelo | $Z_{\text{eq}} = 2.67\ \Omega < 3.2\ \Omega$, safe = false, alerta = ROJO PROTECT | $Z_{\text{eq}} = 2.67\ \Omega$, safe = false, alerta = ROJO PROTECT | **APROBADO** |
| **HU03 / v4** | Separación 2 Líneas Eléctricas | 2 Subs (1400W RMS / 2800W Peak) + 3 Tops (1300W RMS / 2600W Peak) | Línea 1 (Subs): 1400W RMS, 6.36A. Línea 2 (Tops): 1300W RMS, 5.91A | Línea 1: 1400W / 6.36A. Línea 2: 1300W / 5.91A | **APROBADO** |
| **HU04 / v4** | Asymmetric Rigging & Gain Matching | 2 Activas 500W RMS + 1 Pasiva 300W RMS | 2 Activas a PA Frontal (A, B @ 0dB), 1 Pasiva a Delay C con -2.2 dB | PA Frontal A, B @ 0dB, Delay C @ -2.2 dB | **APROBADO** |
| **HU05** | Atenuación SPL y Refuerzo Delay | Sensibilidad $98\text{ dB}$, $500\text{ W}$, fondo $16\text{ m}$ | $125.0\text{ dB}$ (1m), $113.0\text{ dB}$ (4m), $100.9\text{ dB}$ (16m), Delay = true | $125.0\text{ dB}$ (1m), $113.0\text{ dB}$ (4m), $100.9\text{ dB}$ (16m), Delay = true | **APROBADO** |
| **HU05 / v4** | Ratio de Balance Top-to-Sub | 2000W RMS Tops vs 1000W RMS Subs | Ratio 0.50 $\rightarrow$ Cuello de botella detectado (Deficit graves) | Ratio 0.50 $\rightarrow$ Alerta Cuello de Botella Subgraves | **APROBADO** |
| **HU05 / v4** | Impacto Vecinal D.S. N° 38 MMA | Evento 102 dBA en pista, vecino a 45m, muro ladrillo, noche | Nivel vecino = 54.9 dBA vs Límite 45 dBA $\rightarrow$ Excede norma nocturna | Nivel vecino = 54.9 dBA vs Límite 45 dBA $\rightarrow$ Excede | **APROBADO** |
