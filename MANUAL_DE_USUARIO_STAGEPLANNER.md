# MANUAL DE USUARIO DEL SOFTWARE: STAGE PLAN (v4.0)
**Plataforma Web de Pre-Producción Logística, Plano CAD Blueprint, Rack de Potencias Pasivas y Seguridad SEC**  
**Proyecto Integrado (TIHV43) — Analista Programador — INACAP Sede Maipú (Sección C1 · Grupo G10)**

---

## 1. INTRODUCCIÓN Y PROPÓSITO DEL SISTEMA

**STAGE PLAN (v4.0)** es una herramienta de ingeniería preventiva y logística orientada a eventos en formato DJ. Su propósito es reemplazar las estimaciones empíricas sin cálculo normativo por dimensionamiento determinista basado en la **Normativa Eléctrica Chilena SEC (Pliegos RIC N° 03 y RIC N° 10)**, el **Decreto Supremo N° 38 MMA**, acústica espacial y la **Ley del Saco N° 20.949**.

### Flujo Operativo
1. **Planificación en Studio Cockpit (100% Zoom):** El usuario recorre 5 vistas con URL propia y guardado automático en `localStorage` (`/auth`, `/recinto`, `/equipos`, `/plano-2d`, `/reporte`).
2. **Visualización CAD sin Ruido Visual:** El plano 2D separa la ingeniería en 5 capas exclusivas al configurar y consolida todas las capas simultáneamente en el reporte final.
3. **Exportación Autónoma para Terreno:** Descarga un **Plano PNG (300 DPI)**, copia un resumen formateado para **WhatsApp** y genera un **PDF Dual-Page** directamente en el navegador (`jsPDF`), utilizable sin conexión a internet en parcelas rurales.

---

## 2. REQUISITOS Y PUESTA EN MARCHA LOCAL

- **Navegadores recomendados:** Google Chrome, Microsoft Edge, Firefox o Safari (diseñado para verse sin barras de desplazamiento globales al **100% de zoom**, y adaptable a smartphones de 412 px).

```powershell
# 1. Ubicarse en la raíz del proyecto
cd "c:\Users\WIT2026\Documents\stage-plan-main\stage-plan-main"

# 2. Ejecutar las pruebas unitarias automatizadas (81 tests Vitest en 11 archivos)
npm test

# 3. Iniciar el servidor Frontend
npm run dev
```

Abrir en el navegador: `http://localhost:5173`.

---

## 3. GUÍA PASO A PASO POR VISTAS

### Vista 0 (`/auth`): Acceso Operador
- Ingresa credenciales registradas o utiliza el botón de acceso rápido para evaluación (`mauricio.vega@distorsioncl.cl` / `password123`).

### Vista 1 (`/recinto`): Geometría del Recinto y Ruido D.S. N° 38
1. Selecciona uno de los **8 presets rápidos** por escala de evento o ingresa manualmente nombre, ancho, largo, altura, metros al tablero eléctrico, entorno (`Cerrado` o `Parcela/Exterior`), distancia a viviendas vecinas y horario.
2. Verifica el indicador en vivo de superficie ($\text{m}^2$) y cumplimiento acústico vecinal D.S. N° 38.

### Vista 2 (`/equipos`): Lotes Activo/Pasivo, Rack de Potencias y Fuente Eléctrica
1. **Cajas Tops y Subwoofers:** Ajusta cantidades con los controles táctiles `[-] [QTY] [+]`, cambia la tecnología (`Activa` o `Pasiva`), potencia RMS/Peak e impedancia (4 Ω / 8 Ω).
2. **Rack de Potencias Sugerido:** Al incorporar cajas o subs pasivos, aparece automáticamente la tarjeta de dimensionamiento indicando cantidad de etapas de rack 19", margen **Headroom 1,6× RMS**, modelos comerciales recomendados (*Crown / Powersoft / Lab Gruppen*) y la carga AC 220V adicional sumada al balance eléctrico.
3. **Fuente Eléctrica SEC:** Selecciona red domiciliaria (10A–32A) o generador (Watts o kVA) y revisa el tacómetro de demanda y calibre mínimo del alargador.

### Vista 3 (`/plano-2d`): Plano CAD 2D Blueprint, Simulador Pioneer DJM y Plan B
1. **Selector de 5 Capas Exclusivas:** Alterna entre `Arquitectura & Audio` (capa inicial limpia), `Cobertura SPL`, `Fuerza SEC L1/L2/L3`, `Audio & DMX` y `Vista Completa` para inspeccionar cada subsistema sin superposiciones.
2. **Controles de Zoom:** Usa `Ajustado`, `100%`, `150%`, `200%` o la rueda del mouse para inspeccionar postes guía SEC RIC N° 10 (radio $R \ge 6d$), clúster mono central (+6 dB) y torres de retardo Haas.
3. **Herramientas:** Abre el modal **Mixer DJM** (vúmetros de 17 LEDs, *Low EQ Kill* y Master) o **Plan B** ante contingencias.

### Vista 4 (`/reporte`): Previsualización Completa, Cotizador de Arriendo y Exportación
1. **Cotizador de Inversión Operativa:** Conmuta entre `Propios` y `Arriendo` para calcular el costo diario estimado en CLP de tops, subs, racks de potencia, generador, luminarias y personal técnico.
2. **Plano 2D Vista Completa y Descarga PNG:** Visualiza el plano consolidado con todas las capas activas y descárgalo en imagen **PNG (300 DPI)** para enviarlo por WhatsApp.
3. **Descargar Memoria Técnica PDF (Dual-Page):** Genera un PDF de 2 páginas en el navegador:
   - **Página 1 (Vertical):** Memoria técnica SEC RIC 03/10, roster de equipos, rack de potencias, logística Ley del Saco N° 20.949 y desglose de arriendo CLP.
   - **Página 2 (Horizontal):** Lámina técnica CAD 2D completa en alta resolución sobre fondo Blueprint.
