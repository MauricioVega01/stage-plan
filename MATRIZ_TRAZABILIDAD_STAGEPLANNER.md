# Matriz de Trazabilidad y Casos de Prueba Oficiales: STAGE PLAN (v4.0)
**Proyecto de Título / Integrado: Analista Programador — INACAP**

Esta matriz vincula los Requerimientos Funcionales (RF), Historias de Usuario (HU), Casos de Prueba de Aceptación (con valores numéricos exactos de ingeniería) y Casos de Uso según el Master Plan Oficial v4.0 de STAGE PLAN.

---

## 1. Mapeo de Trazabilidad Principal (70 Tests Unitarios Automatizados en Vitest)

| Requisito Funcional | Historia de Usuario | Módulo / Engine | Caso de Uso | Criterio de Aceptación y Caso Numérico Exacto (Master Plan v4.0) |
|---|---|---|---|---|
| **RF01** | **HU01** | `auth` / JWT | CU01 | Validación de credenciales cifradas (Argon2/bcrypt), emisión de JWT en memoria + cookie HttpOnly, bloqueo tras 5 fallos, mitigación IDOR en rutas privadas. |
| **RF02 & RF04** | **HU02** | `calc-engine/electrical` | CU02, CU04 | **Caso Cableado y Caída de Tensión (SEC RIC 03/10):** Carga $1.800\text{ W}$, $220\text{ V}$, $L = 30\text{ m}$, holgura $20\%$, $\Delta V_{\max} = 3\%$ ($6.6\text{ V}$):<br>• $I_{\text{nominal}} = 8.18\text{ A}$<br>• $I_{\text{diseño}} = 9.82\text{ A}$<br>• Sección comercial adoptada: **$2.5\text{ mm}^2$**<br>• Metraje sugerido ($+10\%$): **$33\text{ m}$**<br>• Caída real con $2.5\text{ mm}^2$: **$4.12\text{ V}$ ($1.87\%$)** |
| **RF03 & RF04** | **HU03** | `calc-engine/electrical` | CU03, CU04 | **Caso Eléctrico y Suministro:**<br>**(a) Circuito:** $2.000\text{ W}$ en disyuntor de $10\text{ A}$ ($220\text{ V}$) $\rightarrow I_{\text{nom}} = 9.09\text{ A}$, $I_{\text{dis}} = 10.91\text{ A} \rightarrow$ **ALERTA CRÍTICA** ($> 100\%$).<br>**(b) Generador:** $5\text{ kVA}$ ($FP=0.8 \rightarrow 4.0\text{ kW}$) con carga de $3.5\text{ kW} \rightarrow P_{\text{dis}} = 4.2\text{ kW} \rightarrow$ **ALERTA CRÍTICA** sobrecarga.<br>**(c) Generador Comercial 3500W:** Aplica 72% de factor de seguridad AVR ($2.142\text{ W}$ útiles). |
| **RF03 & v4** | **HU03b** | `calc-engine/hybrid-roster` | CU03, CU04 | **Caso Impedancia Speakon en Paralelo:**<br>**(a)** 2 cajas $8\ \Omega \rightarrow Z_{\text{eq}} = 4.0\ \Omega \rightarrow$ Seguro (Verde).<br>**(b)** 3 cajas $8\ \Omega \rightarrow Z_{\text{eq}} = 2.67\ \Omega < 3.2\ \Omega \rightarrow$ **ALERTA ROJA PROTECT** por riesgo de cortocircuito en transistores. |
| **RF03 & v4** | **HU03c** | `calc-engine/hybrid-roster` | CU03, CU04 | **Caso División en 2 Líneas de Fuerza:**<br>Separa automáticamente la instalación en **Línea 1 (Fuerza Subs)** y **Línea 2 (Tops + DJ)** con cálculo independiente de Watts y Amperes para prevenir caídas de tensión en cabina. |
| **RF03 & v4** | **HU04** | `calc-engine/hybrid-roster` | CU03, CU04 | **Caso Constructor Multilote Asymmetric Rigging & Gain Matching:**<br>2 cajas Activas de 500W RMS + 1 Pasiva de 300W RMS:<br>• Ubica Activas en Frente Principal ($A, B$ a 0 dB Unity).<br>• Ubica Pasiva en Torre Delay Lateral $C$ con retardo Haas y **Gain Matching (-2.2 dB)** para proteger cono. |
| **RF04 & RF05** | **HU05** | `calc-engine/stage-acoustic` | CU04, CU05 | **Caso Acústico SPL, Cobertura y Mapa de Calor 2D:**<br>Sensibilidad $98\text{ dB @ 1W/1m}$, $500\text{ W}$, fondo a $16\text{ m}$:<br>• SPL a $1\text{ m} = 125.0\text{ dB}$, a $4\text{ m} = 113.0\text{ dB}$, al fondo = $100.9\text{ dB}$.<br>• Mapa de calor interactivo con gradientes radiales SVG (Rojo $>105\text{ dBA}$, Verde $96-102\text{ dBA}$, Azul $<90\text{ dBA}$). |
| **RF05 & v4** | **HU05b** | `calc-engine/stage-acoustic` | CU04, CU05 | **Caso Diagnósticos Avanzados (Top/Sub & dimensionamiento acústico y eléctrico):**<br>**(a) Ratio Top/Sub:** Detecta cuellos de botella por déficit de subgraves si la relación RMS Sub/Top $< 1.0$.<br>**(b) Balance de Cobertura Frontal/Delay:** Proyecta la atenuación de SPL hacia el fondo del recinto para calibrar torres de refuerzo.
| **RF06** | **HU06** | `reports` (jsPDF) & Clipboard | CU05 | **Caso Exportación y Movilidad:**<br>• Reporte Operativo PDF Offline con 5 secciones completas y advertencia SEC.<br>• Botón rápido de copia a WhatsApp para compartir resumen técnico en terreno. |
| **RF07** | **HU07** | `history` (Prisma/PostgreSQL) | CU06 | Historial centralizado versionado por recinto y cálculo. Clonación rápida de riders anteriores. Control de acceso estricto anti-IDOR. |

---

## 2. Aprobado para Implementación
Tanto el diseño arquitectónico como la formulación de ingeniería cumplen al 100% los requerimientos de la rúbrica de titulación de INACAP y están respaldados por **70 pruebas unitarias aprobadas**.
