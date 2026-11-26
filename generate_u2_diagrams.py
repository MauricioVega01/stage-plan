import os
import subprocess
from html import escape

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entrega_sumativa_02", "diagrams")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

os.makedirs(OUT_DIR, exist_ok=True)

COMMON_DEFS = """
<defs>
  <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#475569"/>
  </marker>
  <marker id="arr-navy" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#1F497D"/>
  </marker>
  <marker id="arr-red" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#c81e1e"/>
  </marker>
  <marker id="arr-green" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#059669"/>
  </marker>
  <marker id="hollow-tri" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#ffffff" stroke="#1F497D" stroke-width="1.2"/>
  </marker>
</defs>
"""

def box(x, y, w, h, title, lines=None, fill="#ffffff", stroke="#1F497D", badge=None, title_color="#1e293b", stroke_w=1.4, dashed=False):
    lines = lines or []
    dash = 'stroke-dasharray="5,4"' if dashed else ''
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}" {dash}/>']
    cy = y + 22
    if badge:
        bw = max(56, len(badge) * 6.5 + 14)
        parts.append(f'<rect x="{x+10}" y="{y+8}" width="{bw}" height="15" rx="3" fill="{stroke}" fill-opacity="0.12" stroke="{stroke}" stroke-width="0.8"/>')
        parts.append(f'<text x="{x+10+bw/2}" y="{y+18.5}" fill="{stroke}" font-size="8.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(badge)}</text>')
        cy = y + 38
    parts.append(f'<text x="{x+w/2}" y="{cy}" fill="{title_color}" font-size="12" font-weight="700" font-family="Segoe UI, system-ui, sans-serif" text-anchor="middle">{escape(title)}</text>')
    for idx, ln in enumerate(lines):
        ly = cy + 16 + idx * 14
        parts.append(f'<text x="{x+w/2}" y="{ly}" fill="#475569" font-size="9.5" font-family="Consolas, monospace" text-anchor="middle">{escape(ln)}</text>')
    return "\n".join(parts)

def zone(x, y, w, h, label, stroke="#94a3b8", fill="rgba(31,73,125,0.03)"):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1.1" stroke-dasharray="6,4"/>\n'
        f'<text x="{x+14}" y="{y+18}" fill="#475569" font-size="9.5" font-weight="700" font-family="Consolas, monospace" letter-spacing="0.06em">{escape(label)}</text>'
    )

def arrow(x1, y1, x2, y2, label="", color="#475569", marker="arr", dashed=False, lx=None, ly=None):
    dash = 'stroke-dasharray="5,4"' if dashed else ''
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" {dash} marker-end="url(#{marker})"/>'
    if label:
        mx = lx if lx is not None else (x1 + x2) / 2
        my = ly if ly is not None else (y1 + y2) / 2 - 6
        lw = len(label) * 5.8 + 10
        s += f'\n<rect x="{mx-lw/2}" y="{my-9}" width="{lw}" height="13" rx="2" fill="#f8fafc"/>'
        s += f'\n<text x="{mx}" y="{my+1}" fill="{color}" font-size="8.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(label)}</text>'
    return s

def path_arrow(d, label="", color="#475569", marker="arr", dashed=False, lx=0, ly=0):
    dash = 'stroke-dasharray="5,4"' if dashed else ''
    s = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" {dash} marker-end="url(#{marker})"/>'
    if label:
        lw = len(label) * 5.8 + 10
        s += f'\n<rect x="{lx-lw/2}" y="{ly-9}" width="{lw}" height="13" rx="2" fill="#f8fafc"/>'
        s += f'\n<text x="{lx}" y="{ly+1}" fill="{color}" font-size="8.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(label)}</text>'
    return s

def write_diagram(slug, eyebrow, title, svg_body, width=1160, height=660):
    svg = f'''<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
{COMMON_DEFS}
<rect width="100%" height="100%" fill="#f8fafc"/>
{svg_body}
</svg>'''
    svg_path = os.path.join(OUT_DIR, f"{slug}.svg")
    html_path = os.path.join(OUT_DIR, f"{slug}.html")
    png_path = os.path.join(OUT_DIR, f"{slug}.png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg)
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{escape(title)}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #f8fafc; font-family: 'Segoe UI', system-ui, sans-serif; padding: 22px 26px; color: #1e293b; }}
  .eyebrow {{ font-family: Consolas, monospace; font-size: 11px; font-weight: 700; letter-spacing: 0.14em; color: #1F497D; text-transform: uppercase; margin-bottom: 4px; }}
  h1 {{ font-size: 20px; font-weight: 800; color: #0f172a; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
  svg {{ width: 100%; height: auto; display: block; border: 1px solid #cbd5e1; border-radius: 8px; background: #f8fafc; }}
</style>
</head>
<body>
  <div class="eyebrow">{escape(eyebrow)}</div>
  <h1>{escape(title)}</h1>
  {svg}
</body>
</html>'''
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        f"--window-size={width+60},{height+110}",
        f"--screenshot={png_path}",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Chrome screenshot failed for {slug}: {res.stderr}")
    size_kb = os.path.getsize(png_path) / 1024
    print(f"OK {slug}: {size_kb:.1f} KB")


# 1. SCRUMBAN CRONOGRAMA & KANBAN
d1 = []
d1.append(zone(20, 18, 1120, 290, "CRONOGRAMA SCRUMBAN + PSP (4 SPRINTS FIJOS DE 14 DÍAS · RUTA CRÍTICA EN ROJO)"))
weeks = ["S1 (Sem 1-2)", "S2 (Sem 3-4)", "S3 (Sem 5-6)", "S4 (Sem 7-8)", "Cierre U2"]
for i, w in enumerate(weeks):
    gx = 240 + i * 176
    d1.append(f'<rect x="{gx}" y="42" width="170" height="22" rx="4" fill="#1F497D"/>')
    d1.append(f'<text x="{gx+85}" y="57" fill="#ffffff" font-size="10" font-weight="700" font-family="Segoe UI, sans-serif" text-anchor="middle">{w}</text>')
gantt_rows = [
    ("T01-T04 Diagnostico & Zod", 240, 170, "#1F497D", "CRITICA"),
    ("T05-T08 Motor SEC + Haas + 81 Tests", 416, 220, "#c81e1e", "CRITICA"),
    ("T09-T12 Backend Express + Prisma + JWT", 560, 180, "#1F497D", "CRITICA"),
    ("T13-T16 Cockpit 100% + Blueprint + DJM", 720, 220, "#c81e1e", "CRITICA"),
    ("T17-T20 OWASP + Benchmark + Entrega U2", 910, 200, "#059669", "HITO FINAL"),
]
for idx, (lbl, bx, bw, col, st) in enumerate(gantt_rows):
    ry = 76 + idx * 42
    d1.append(f'<text x="34" y="{ry+18}" fill="#1e293b" font-size="10.5" font-weight="700" font-family="Segoe UI, sans-serif">{lbl}</text>')
    d1.append(f'<rect x="{bx}" y="{ry+2}" width="{bw}" height="26" rx="5" fill="{col}" fill-opacity="0.9"/>')
    d1.append(f'<text x="{bx+bw/2}" y="{ry+19}" fill="#ffffff" font-size="9.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{st}</text>')
d1.append(f'<text x="34" y="294" fill="#c81e1e" font-size="9.5" font-weight="700" font-family="Consolas, monospace">Ruta Crítica: T01 → T02 → T04 → T05 → T06 → T08 → T09 → T10 → T12 → T13 → T15 → T18 → T20 (holgura 0 días)</text>')

d1.append(zone(20, 326, 1120, 316, "TABLERO KANBAN Y POLÍTICA WIP (SOLO-DEVELOPER MAURICIO VEGA · SECCIÓN C1 · GRUPO G10)"))
cols = [
    ("BACKLOG (U3)", "Sin límite", "#64748b", ["Despliegue VPS PostgreSQL 16", "Migración audit_logs & PG GIN"]),
    ("SELECTED FOR DEV", "WIP Max: 3", "#1F497D", ["Pruebas carga k6 (U3)", "Escaneo OWASP ZAP VPS (U3)"]),
    ("IN PROGRESS", "WIP Max: 1", "#c81e1e", ["T20 Cierre Informe U2", "(Foco exclusivo WIP=1)"]),
    ("TESTING / TDD", "WIP Max: 2", "#d97706", ["11 suites Vitest (81/81 OK)", "vue-tsc + vite build OK"]),
    ("DONE (DoD 100%)", "Completado", "#059669", ["Motor SEC + Rack Pasivos", "Cockpit 100% + Blueprint 2D", "Cotizador + PDF Dual-Page"]),
]
for i, (ctitle, wip, col, cards) in enumerate(cols):
    cx = 36 + i * 218
    d1.append(f'<rect x="{cx}" y="354" width="206" height="272" rx="7" fill="#ffffff" stroke="{col}" stroke-width="1.3"/>')
    d1.append(f'<rect x="{cx}" y="354" width="206" height="36" rx="7" fill="{col}"/>')
    d1.append(f'<text x="{cx+103}" y="370" fill="#ffffff" font-size="10" font-weight="700" font-family="Segoe UI, sans-serif" text-anchor="middle">{ctitle}</text>')
    d1.append(f'<text x="{cx+103}" y="384" fill="#f1f5f9" font-size="8.5" font-family="Consolas, monospace" text-anchor="middle">{wip}</text>')
    for j, card in enumerate(cards):
        ky = 402 + j * 64
        d1.append(f'<rect x="{cx+10}" y="{ky}" width="186" height="52" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>')
        d1.append(f'<text x="{cx+103}" y="{ky+30}" fill="#1e293b" font-size="9.5" font-weight="600" font-family="Segoe UI, sans-serif" text-anchor="middle">{escape(card)}</text>')
write_diagram("diag-01-scrumban-cronograma-kanban", "CRITERIO 2.1.1.1 & 2.1.1.2 · METODOLOGÍA ÁGIL", "Cronograma Scrumban + PSP (4 Sprints) y Tablero Kanban con Límites WIP", "\n".join(d1))


# 2. ARQUITECTURA 4+1 VISTA FÍSICA / DESPLIEGUE
d2 = []
d2.append(zone(20, 20, 260, 610, "NODO CLIENTE TERRENO (AUTÓNOMO)"))
d2.append(box(38, 65, 224, 115, "Smartphone / Laptop FOH", ["Chrome / Edge (Zoom 100%)", "Vue Router 4 (5 Vistas)", "Composable + localStorage"], "#ffffff", "#1F497D", "CLIENT"))
d2.append(box(38, 225, 224, 125, "Motor Reactivo en Memoria", ["Núcleo @stageplan/shared", "Cálculo < 1 ms sin red", "Blueprint 2D + Pioneer DJM"], "#ffffff", "#059669", "EDGE"))
d2.append(box(38, 395, 224, 115, "Salida Operacional Terreno", ["PDF Dual-Page (Memoria + CAD)", "Exportación PNG 300 DPI", "Resumen WhatsApp 1-Clic"], "#ffffff", "#d97706", "OFFLINE PDF"))

d2.append(zone(310, 20, 830, 610, "ENTORNO SERVIDOR: MVP LOCAL U2 (SQLite) Y PROYECCIÓN PRODUCCIÓN U3 (VPS TLS 1.3)"))
d2.append(box(335, 110, 195, 110, "Reverse Proxy Nginx", ["Proyección U3: TLS 1.3 + HSTS", "Único Puerto Expuesto :443", "En PoC U2: Vite :5173 local"], "#ffffff", "#c81e1e", "PROXY :443"))
d2.append(box(585, 65, 250, 130, "Frontend SPA (@stageplan/frontend)", ["Vue 3.5 + Vite 6.4 + Tailwind 3.4", "Vue Router 4 + useStagePlanState", "Bundle estático modular"], "#ffffff", "#1F497D", "FRONTEND"))
d2.append(box(585, 240, 250, 190, "API REST (@stageplan/backend)", ["Node.js v24 + Express 4.21 :3000", "Helmet + CORS + RateLimit (10/15m)", "Bcrypt(12) + Bloqueo 423 (5 fallos)", "JWT (12h) + Anti-IDOR (HTTP 404)"], "#ffffff", "#c81e1e", "BACKEND :3000"))
d2.append(box(875, 195, 245, 115, "PoC Local U2: SQLite 3 (dev.db)", ["Prisma ORM 6.4 (ACID)", "4 Tablas 3FN en Español", "Documentos JSON auditables"], "#ecfdf5", "#059669", "SQLITE POC U2"))
d2.append(box(875, 330, 245, 115, "Proy. U3: PostgreSQL 16 (:5432)", ["12 Tablas 3FN + JSONB (GIN)", "audit_logs + pgcrypto + Triggers", "Migración transparente Prisma"], "#eff6ff", "#1F497D", "TARGET PG16 U3", dashed=True))
d2.append(box(585, 485, 535, 110, "Núcleo Isomórfico (@stageplan/shared · 11 Módulos TS + 81 Tests Vitest)", ["electrical.ts · cabling.ts · acoustics.ts · hybrid-roster.ts (PowerAmp + Speakon)", "lighting-dmx.ts · power-distribution.ts · dj-setup-audio.ts · schemas.ts (Zod)"], "#eff6ff", "#1F497D", "SHARED KERNEL"))

d2.append(arrow(262, 125, 335, 150, "HTTPS / HTTP", "#c81e1e", "arr-red", lx=298, ly=115))
d2.append(arrow(530, 140, 585, 130, "Static", "#1F497D", "arr-navy"))
d2.append(path_arrow("M 530 185 L 558 185 L 558 320 L 585 320", "REST /api/*", "#c81e1e", "arr-red", lx=558, ly=248))
d2.append(arrow(835, 280, 875, 250, "Prisma", "#059669", "arr-green"))
d2.append(arrow(835, 360, 875, 385, "U3 :5432", "#1F497D", "arr-navy", dashed=True))
d2.append(arrow(150, 180, 150, 225, "Local", "#059669", "arr-green"))
d2.append(arrow(150, 350, 150, 395, "Blob PDF", "#d97706", "arr"))
d2.append(arrow(710, 430, 710, 485, "Import", "#1F497D", "arr-navy"))
write_diagram("diag-02-arquitectura-4plus1-despliegue", "CRITERIO 2.1.2.3 & 2.1.2.4 · VISTA FÍSICA Y DESPLIEGUE 4+1", "Arquitectura Tecnológica, Despliegue PoC Local / VPS U3 y Operación Terreno", "\n".join(d2))


# 3. ESCENARIOS - CASO DE USO CERO (CU-00)
d3 = []
d3.append(zone(260, 25, 650, 610, "LÍMITE DEL SISTEMA: STAGE PLAN (CASO DE USO CERO: CU-00)"))
def actor(ax, ay, name, role):
    return (
        f'<circle cx="{ax}" cy="{ay}" r="14" fill="#ffffff" stroke="#1F497D" stroke-width="1.8"/>'
        f'<line x1="{ax}" y1="{ay+14}" x2="{ax}" y2="{ay+48}" stroke="#1F497D" stroke-width="1.8"/>'
        f'<line x1="{ax-18}" y1="{ay+26}" x2="{ax+18}" y2="{ay+26}" stroke="#1F497D" stroke-width="1.8"/>'
        f'<line x1="{ax}" y1="{ay+48}" x2="{ax-14}" y2="{ay+72}" stroke="#1F497D" stroke-width="1.8"/>'
        f'<line x1="{ax}" y1="{ay+48}" x2="{ax+14}" y2="{ay+72}" stroke="#1F497D" stroke-width="1.8"/>'
        f'<text x="{ax}" y="{ay+90}" fill="#0f172a" font-size="11" font-weight="700" font-family="Segoe UI, sans-serif" text-anchor="middle">{escape(name)}</text>'
        f'<text x="{ax}" y="{ay+104}" fill="#64748b" font-size="9" font-family="Consolas, monospace" text-anchor="middle">{escape(role)}</text>'
    )
def usecase(ux, uy, rx, ry, code, title, fill="#ffffff", stroke="#1F497D"):
    return (
        f'<ellipse cx="{ux}" cy="{uy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{ux}" y="{uy-4}" fill="{stroke}" font-size="9" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(code)}</text>'
        f'<text x="{ux}" y="{uy+10}" fill="#0f172a" font-size="10.5" font-weight="700" font-family="Segoe UI, sans-serif" text-anchor="middle">{escape(title)}</text>'
    )

d3.append(actor(110, 140, "Operador FOH / DJ", "DISTORSIONCL SPA"))
d3.append(actor(110, 420, "Chofer / Bodeguero", "Reporte y Carga"))
d3.append(actor(1030, 260, "Administrador", "Auditoría Técnica"))

d3.append(usecase(430, 320, 130, 44, "CU-00", "Planificación Logística Integral", "#eff6ff", "#1F497D"))
ucs = [
    (740, 85, "CU-01", "Autenticación JWT & Anti-IDOR", "#ffffff", "#1F497D"),
    (740, 165, "CU-02", "Recinto & Ruido D.S. N° 38", "#ffffff", "#1F497D"),
    (740, 245, "CU-03", "Ruteo SEC RIC 10 + Postes Guía", "#fef2f2", "#c81e1e"),
    (740, 325, "CU-04", "Pasivos + Rack Powers + Speakon", "#ffffff", "#1F497D"),
    (740, 405, "CU-05", "Iluminación DMX x1 + Cables", "#ffffff", "#1F497D"),
    (740, 485, "CU-06", "Plano Blueprint + Pioneer DJM", "#ffffff", "#059669"),
    (740, 565, "CU-08", "PDF Dual-Page, Arriendo y Carga", "#ffffff", "#d97706"),
]
for ux, uy, code, ttl, fl, st in ucs:
    d3.append(usecase(ux, uy, 145, 28, code, ttl, fl, st))
    rel = "<<extend>>" if code in ("CU-04", "CU-06") else "<<include>>"
    d3.append(arrow(556, 320, 595, uy, rel, st, "arr", dashed=True, lx=575, ly=(320+uy)/2 - 4))

d3.append(arrow(140, 185, 300, 310, "Opera", "#1F497D", "arr-navy"))
d3.append(arrow(140, 460, 595, 565, "Descarga", "#d97706", "arr"))
d3.append(arrow(995, 290, 885, 90, "Consulta", "#1F497D", "arr-navy"))
write_diagram("diag-03-escenarios-caso-uso-cero", "CRITERIO 2.1.2.3 · VISTA DE ESCENARIOS (4+1)", "Diagrama de Casos de Uso — Caso de Uso Cero (CU-00) e Integración", "\n".join(d3))


# 4. VISTA LÓGICA - CLASES UML
d4 = []
def uml_class(x, y, w, name, attrs, methods, stroke="#1F497D"):
    ah = len(attrs) * 14 + 10
    mh = len(methods) * 14 + 10
    h = 28 + ah + mh
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#ffffff" stroke="{stroke}" stroke-width="1.4"/>']
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="{stroke}"/>')
    out.append(f'<text x="{x+w/2}" y="{y+17}" fill="#ffffff" font-size="11" font-weight="700" font-family="Segoe UI, sans-serif" text-anchor="middle">{escape(name)}</text>')
    for i, a in enumerate(attrs):
        out.append(f'<text x="{x+8}" y="{y+42+i*14}" fill="#334155" font-size="8.8" font-family="Consolas, monospace">{escape(a)}</text>')
    y2 = y + 28 + ah
    out.append(f'<line x1="{x}" y1="{y2}" x2="{x+w}" y2="{y2}" stroke="#cbd5e1" stroke-width="1"/>')
    for j, m in enumerate(methods):
        out.append(f'<text x="{x+8}" y="{y2+15+j*14}" fill="#1F497D" font-size="8.8" font-family="Consolas, monospace">{escape(m)}</text>')
    return "\n".join(out)

d4.append(uml_class(30, 30, 235, "Usuario (Auth / Prisma)", ["- id: UUID", "- correo: String", "- rol: String", "- claveHash: String"], ["+ login(): JWT (12h)", "+ checkLock423(): Bool"]))
d4.append(uml_class(30, 225, 235, "Recinto (Venue)", ["- id: UUID", "- anchoMetros: Float", "- largoMetros: Float", "- distElectricaMetros: Float", "- tipoEntorno: EnvEnum"], ["+ getAreaM2(): Float", "+ estimateNoiseDS38(): Db"]))
d4.append(uml_class(30, 440, 235, "SpeakerBatchInput", ["- category: TOP | SUB", "- systemType: ACTIVE|PASSIVE", "- rmsWatts / peakWatts: Int", "- impedanceOhms: 4|8|16"], ["+ isSpeakOnSafe(): Bool", "+ getTotalWatts(): Int"]))

d4.append(uml_class(345, 30, 305, "CalculationEngine (Shared Kernel)", ["- engineVersion: String = '4.0.0'", "- MAX_VOLTAGE_DROP: Float = 3.0"], ["+ runFullAudit(venue, lots): Result", "+ calcPowerAmpSizing(batches): AmpRack", "+ validateWithZod(input): Boolean"], "#c81e1e"))
d4.append(uml_class(345, 200, 305, "ElectricalSECValidator", ["- COPPER_RHO: Float = 0.0175", "- SAFETY_MARGIN: Float = 1.20"], ["+ calculateCableSizing(params): Cable", "+ splitLinesL1L2L3(loads): Circuits", "+ validateCircuitCapacity(): Alert"]))
d4.append(uml_class(345, 380, 305, "StageAcousticEngine", ["- SOUND_SPEED_20C: Float = 343.4"], ["+ calcClusterGainDb(subs): Float", "+ calcDelayHaasMs(distM): Float", "+ computeSplHeatMap(): ZoneMap"]))
d4.append(uml_class(345, 530, 305, "LightingDmxCalculator", ["- DMX_MAX_CH: Int = 512"], ["+ calcSingleUnitsX1(fixtures): Int", "+ calcDmxCableMeters(cabina, z): Float"], "#059669"))

d4.append(uml_class(735, 30, 385, "CalculoRider (Persist. Híbrida)", ["- id: UUID", "- recintoId: UUID", "- entradaRider: JSON", "- resultadosCalculados: JSON", "- alertasSnapshot: JSON"], ["+ persistAtomically(): CalculoRider", "+ toDualPagePdfPayload(): PdfReport"]))
d4.append(uml_class(735, 240, 385, "DjSetupAndGainSimulator", ["- ch1LowActive: Boolean", "- ch2LowActive: Boolean", "- masterPos: 12_OCLOCK|2_OCLOCK|MAX"], ["+ calcMasterOutputDb(): Float", "+ getLedMeterSegments(): LedState[]", "+ buildCableChecklist(): AudioRoute[]"], "#d97706"))
d4.append(uml_class(735, 435, 385, "LogisticsAndRentalService", ["- maxSackWeightKg: Int = 25", "- isRentalMode: Boolean"], ["+ checkLeyDelSaco20949(kg): Alert", "+ calcRentalSummaryClp(): CostClp", "+ exportCadPng300Dpi(): DataURL"]))

d4.append(arrow(265, 95, 345, 80, "1..*", "#1F497D", "arr-navy"))
d4.append(arrow(265, 285, 345, 110, "input", "#1F497D", "arr-navy"))
d4.append(arrow(265, 500, 345, 260, "loads", "#1F497D", "arr-navy"))
d4.append(arrow(650, 95, 735, 95, "persiste", "#c81e1e", "arr-red"))
d4.append(arrow(495, 155, 495, 200, "usa SEC", "#c81e1e", "arr-red"))
d4.append(arrow(495, 345, 495, 380, "usa Haas", "#1F497D", "arr-navy"))
d4.append(arrow(495, 500, 495, 530, "usa DMX", "#059669", "arr-green"))
d4.append(arrow(650, 430, 735, 310, "simula", "#d97706", "arr"))
d4.append(arrow(650, 120, 735, 485, "exporta", "#1F497D", "arr-navy"))
write_diagram("diag-04-vista-logica-clases", "CRITERIO 2.1.2.3 · VISTA LÓGICA (4+1)", "Diagrama de Clases del Dominio (STAGE PLAN v4.0)", "\n".join(d4))


# 5. VISTA DE DESARROLLO - COMPONENTES MONOREPO
d5 = []
d5.append(zone(20, 20, 1120, 620, "MONOREPO STAGE PLAN (NPM WORKSPACES · TYPESCRIPT STRICT)"))
d5.append(zone(45, 60, 325, 550, "@stageplan/frontend (Vue 3.5 + Vite 6.4)"))
d5.append(box(65, 105, 285, 95, "Router (5 Vistas) + Estado", ["ViewAuth, ViewVenue, ViewAudioPower", "ViewAcousticCanvas, ViewReportSummary", "useStagePlanState.ts + localStorage"], "#ffffff", "#1F497D", "UI SHELL"))
d5.append(box(65, 215, 285, 95, "LayoutSvg2D.vue (Blueprint CAD)", ["5 Capas Exclusivas + Vista Completa", "Postes Guía SEC RIC 10 + SPL", "Captura PNG 300 DPI (Canvas)"], "#ffffff", "#c81e1e", "SVG ENGINE"))
d5.append(box(65, 325, 285, 95, "PioneerMixerSimulator.vue", ["Réplica Hardware DJM", "Vúmetros 17 LEDs + Low Kill", "Perilla Master 12:00/2:00"], "#ffffff", "#d97706", "SIMULATOR"))
d5.append(box(65, 435, 285, 90, "services/pdfReport.ts", ["jsPDF + jspdf-autotable", "PDF Dual-Page (Memoria + CAD 2D)", "Ejecución 100% Offline en cliente"], "#ffffff", "#059669", "PDF DUAL-PAGE"))

d5.append(zone(415, 60, 320, 550, "@stageplan/shared (Núcleo Isomórfico)"))
d5.append(box(435, 105, 280, 90, "schemas.ts (Zod Contracts)", ["Validación Isomórfica", "Venue, Equipment, Lighting"], "#eff6ff", "#1F497D", "ZOD"))
d5.append(box(435, 215, 280, 175, "calc-engine/ (11 Módulos TS)", ["electrical.ts · cabling.ts", "acoustics.ts · hybrid-roster.ts", "lighting-dmx.ts · routing.ts", "dj-setup-audio.ts · inventory.ts", "power-distribution.ts", "stage-acoustic-engine.ts", "contingency-and-logistics.ts"], "#ffffff", "#1F497D", "PURE LOGIC"))
d5.append(box(435, 415, 280, 110, "tests/ (Vitest v3.2.7)", ["11 archivos .spec.ts", "81 Pruebas Unitarias TDD", "100% PASS Quality Gate"], "#ecfdf5", "#059669", "TDD VITEST"))

d5.append(zone(780, 60, 335, 550, "@stageplan/backend (Express + Prisma)"))
d5.append(box(800, 105, 295, 110, "server.ts & Middlewares", ["Helmet + CORS + RateLimit (10/15m)", "authMiddleware (JWT 12h) + errorHandler", "Anti-IDOR ownerId (HTTP 404)"], "#ffffff", "#c81e1e", "SECURITY"))
d5.append(box(800, 235, 295, 130, "REST Controllers", ["AuthController (Bloqueo 423 / 5x)", "VenueController (/api/venues/*)", "CalculationController (v4.0.0)"], "#ffffff", "#1F497D", "API REST"))
d5.append(box(800, 390, 295, 135, "Prisma ORM + SQLite / PG16", ["prisma/schema.prisma (SQLite dev.db)", "4 Tablas 3FN en español + JSON", "Proy. U3: PostgreSQL 16 (12 tablas)"], "#ffffff", "#1F497D", "DATA LAYER"))

d5.append(arrow(350, 150, 435, 150, "import", "#1F497D", "arr-navy"))
d5.append(arrow(350, 260, 435, 260, "calcula", "#c81e1e", "arr-red"))
d5.append(arrow(800, 280, 715, 160, "valida Zod", "#1F497D", "arr-navy"))
d5.append(arrow(800, 320, 715, 300, "ejecuta", "#1F497D", "arr-navy"))
d5.append(arrow(945, 215, 945, 235, "filtra", "#c81e1e", "arr-red"))
d5.append(arrow(945, 365, 945, 390, "ACID", "#1F497D", "arr-navy"))
write_diagram("diag-05-vista-desarrollo-componentes", "CRITERIO 2.1.2.3 · VISTA DE DESARROLLO (4+1)", "Diagrama de Componentes del Monorepo TypeScript (3 Paquetes)", "\n".join(d5))


# 6. VISTA DE PROCESOS - BPMN 2.0
d6 = []
d6.append(zone(20, 20, 1120, 195, "CARRIL 1: OPERADOR TÉCNICO FOH (TERRENO / PRE-PRODUCCIÓN)"))
d6.append(zone(20, 225, 1120, 215, "CARRIL 2: MOTOR DETERMINISTA STAGE PLAN (VALIDACIÓN Y CÁLCULO)"))
d6.append(zone(20, 450, 1120, 190, "CARRIL 3: SALIDA OPERACIONAL & PERSISTENCIA (SQLITE PoC / PDF DUAL-PAGE)"))

d6.append('<circle cx="70" cy="120" r="18" fill="#ecfdf5" stroke="#059669" stroke-width="2.2"/>')
d6.append('<text x="70" y="152" fill="#059669" font-size="9" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">INICIO</text>')
d6.append(box(120, 80, 165, 80, "1. Ingresar Recinto", ["Ancho, Largo, Vecinos", "Acometida 220V SEC"], "#ffffff", "#1F497D"))
d6.append(box(320, 80, 185, 80, "2. Configurar Equipos", ["Tops/Subs Activa o Pasiva", "Powers + Arriendo CLP"], "#ffffff", "#1F497D"))

d6.append(box(320, 285, 185, 85, "3. Validación Zod", ["Rango 1..500m, Watts > 0", "Saneamiento Inputs"], "#eff6ff", "#1F497D"))
def gateway(gx, gy, label):
    pts = f"{gx},{gy-28} {gx+28},{gy} {gx},{gy+28} {gx-28},{gy}"
    return (
        f'<polygon points="{pts}" fill="#fffbeb" stroke="#d97706" stroke-width="2"/>'
        f'<text x="{gx}" y="{gy+5}" fill="#d97706" font-size="16" font-weight="900" text-anchor="middle">X</text>'
        f'<text x="{gx}" y="{gy+42}" fill="#475569" font-size="8.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(label)}</text>'
    )
d6.append(gateway(585, 327, "SEC ΔV<=3% y Z>=3.2?"))
d6.append(box(685, 255, 200, 70, "Alerta / Rebalanceo", ["Dividir L1/L2/L3 + Calibre", "Sugerir Rack Powers y RIC 10"], "#fef2f2", "#c81e1e"))
d6.append(box(685, 345, 200, 75, "Cálculo Aprobado OK", ["Delays Haas + Cluster +6dB", "Rack Pasivo + Cotización CLP"], "#ecfdf5", "#059669"))

d6.append(box(320, 505, 230, 85, "4. Persistir en SQLite 3 (dev.db)", ["4 Tablas 3FN + JSON Snapshot", "Proy. U3: PostgreSQL 16"], "#ffffff", "#1F497D"))
d6.append(box(685, 505, 240, 85, "5. Plano CAD + PDF Dual-Page", ["Vista Completa todas capas", "PDF (2 Págs) + PNG 300 DPI"], "#ffffff", "#059669"))
d6.append('<circle cx="1030" cy="547" r="18" fill="#fef2f2" stroke="#c81e1e" stroke-width="3.5"/>')
d6.append('<text x="1030" y="582" fill="#c81e1e" font-size="9" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">FIN MONTAJE</text>')

d6.append(arrow(88, 120, 120, 120, "", "#059669", "arr-green"))
d6.append(arrow(285, 120, 320, 120, "", "#1F497D", "arr-navy"))
d6.append(arrow(412, 160, 412, 285, "Payload", "#1F497D", "arr-navy"))
d6.append(arrow(505, 327, 557, 327, "Evalúa", "#1F497D", "arr-navy"))
d6.append(arrow(613, 315, 685, 290, "NO", "#c81e1e", "arr-red"))
d6.append(path_arrow("M 785 255 L 785 120 L 505 120", "Reajusta Equipos / Líneas", "#c81e1e", "arr-red", dashed=True, lx=655, ly=108))
d6.append(arrow(613, 340, 685, 380, "SÍ", "#059669", "arr-green"))
d6.append(path_arrow("M 785 420 L 785 462 L 435 462 L 435 505", "Guarda 201 OK", "#1F497D", "arr-navy", lx=610, ly=456))
d6.append(arrow(550, 547, 685, 547, "Render", "#059669", "arr-green"))
d6.append(arrow(925, 547, 1012, 547, "Listo", "#059669", "arr-green"))
write_diagram("diag-06-vista-procesos-bpmn", "CRITERIO 2.1.2.3 · VISTA DE PROCESOS (4+1)", "Diagrama de Procesos de Negocio (BPMN 2.0) — Pre-Producción y Validación SEC", "\n".join(d6))


# 7. MODELO DE DATOS DER (PoC SQLite 4 Tablas en Español + Proyección U3 PostgreSQL 16)
d7 = []
def der_table(x, y, w, name, cols, stroke="#1F497D"):
    h = 26 + len(cols) * 14 + 8
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#ffffff" stroke="{stroke}" stroke-width="1.5"/>']
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="4" fill="{stroke}"/>')
    out.append(f'<text x="{x+w/2}" y="{y+16}" fill="#ffffff" font-size="10.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(name)}</text>')
    for i, c in enumerate(cols):
        col = "#c81e1e" if "PK" in c else ("#059669" if "JSON" in c else ("#1F497D" if "FK" in c else "#334155"))
        out.append(f'<text x="{x+10}" y="{y+40+i*14}" fill="{col}" font-size="8.8" font-family="Consolas, monospace">{escape(c)}</text>')
    return "\n".join(out)

d7.append(zone(20, 20, 725, 620, "MODELO HÍBRIDO IMPLEMENTADO EN PoC (SQLITE 3 dev.db + PRISMA ORM · 4 TABLAS 3FN EN ESPAÑOL)"))
d7.append(der_table(40, 55, 290, "usuarios", [
    "PK id: TEXT (UUID)",
    "   correo: TEXT (UNIQUE)",
    "   clave_hash: TEXT (bcrypt 12)",
    "   nombre: TEXT",
    "   rol: TEXT ('ADMIN')",
    "   intentos_fallidos: INTEGER (0..5)",
    "   bloqueado_hasta: DATETIME?",
    "   fecha_creacion / actualizacion"
]))
d7.append(der_table(40, 275, 290, "recintos", [
    "PK id: TEXT (UUID)",
    "FK usuario_id -> usuarios.id (CASCADE)",
    "   nombre: TEXT",
    "   ancho_metros / largo_metros: REAL",
    "   alto_metros: REAL",
    "   tipo_entorno: TEXT",
    "   distancia_electrica_metros: REAL",
    "   fecha_creacion / actualizacion"
]))
d7.append(der_table(385, 55, 335, "calculos_rider (NÚCLEO HÍBRIDO)", [
    "PK id: TEXT (UUID)",
    "FK usuario_id -> usuarios.id (CASCADE)",
    "FK recinto_id -> recintos.id (CASCADE)",
    "   version_motor: TEXT ('4.0.0')",
    "   entrada_rider: JSON (Tops/Subs/Power)",
    "   parametros_usados: JSON (RIC 03/10)",
    "   resultados_calculados: JSON (Watts/SPL)",
    "   alertas_snapshot: JSON (SEC/Speakon)",
    "   fecha_creacion: DATETIME"
], "#059669"))
d7.append(der_table(385, 295, 335, "enlaces_compartidos", [
    "PK id: TEXT (UUID)",
    "FK usuario_id -> usuarios.id (CASCADE)",
    "FK calculo_rider_id -> calculos_rider.id",
    "   token: TEXT (UNIQUE)",
    "   fecha_expiracion: DATETIME",
    "   esta_revocado: INTEGER (0/1)",
    "   fecha_creacion: DATETIME"
]))

d7.append(box(40, 480, 680, 135, "Consulta Híbrida Auditable en DB Browser for SQLite (3FN + json_extract)", [
    "SELECT u.nombre, r.nombre, json_extract(c.resultados_calculados, '$.totalWatts') AS watts,",
    "       json_extract(c.resultados_calculados, '$.electricalSummary.recommendedSectionMm2') AS mm2",
    "FROM usuarios u JOIN recintos r ON u.id = r.usuario_id",
    "JOIN calculos_rider c ON r.id = c.recinto_id",
    "WHERE json_extract(c.resultados_calculados, '$.electricalSummary.secCompliant') = 1;"
], "#ffffff", "#1F497D", "SQL + JSON_EXTRACT"))

d7.append(zone(770, 20, 370, 620, "PROYECCIÓN PRODUCCIÓN U3 (POSTGRESQL 16)", stroke="#1F497D", fill="rgba(31,73,125,0.05)"))
d7.append(box(790, 60, 330, 135, "Esquema Extendido (12 Tablas)", [
    "Definido en sql/schema_stageplan_pg16.sql",
    "• roles (RBAC 3 perfiles)",
    "• equipment_catalog (JSONB + GIN)",
    "• equipment_lots / lighting_fixtures",
    "• electrical_circuits / audio_routes"
], "#eff6ff", "#1F497D", "DDL U3 LISTO", dashed=True))
d7.append(box(790, 225, 330, 145, "Trazabilidad & Auditoría U3", [
    "• audit_logs (IDOR_BLOCKED, LOGIN_FAIL)",
    "• user_feedback (iteraciones terreno)",
    "• Índices GIN (jsonb_path_ops)",
    "• Triggers PL/pgSQL CHECK ΔV <= 3%",
    "• Extensión pgcrypto AES-256"
], "#ffffff", "#c81e1e", "SEGURIDAD U3", dashed=True))
d7.append(box(790, 400, 330, 135, "Ruta de Migración Prisma ORM", [
    "1. Cambiar provider = 'postgresql'",
    "2. Configurar DATABASE_URL en .env",
    "3. npx prisma migrate deploy",
    "Cero cambios en controladores REST"
], "#ecfdf5", "#059669", "MIGRACIÓN"))

d7.append(arrow(185, 220, 185, 275, "1:N CASCADE", "#1F497D", "arr-navy"))
d7.append(arrow(330, 120, 385, 120, "1:N", "#059669", "arr-green"))
d7.append(arrow(330, 330, 385, 185, "1:N", "#059669", "arr-green"))
d7.append(arrow(552, 232, 552, 295, "1:N CASCADE", "#1F497D", "arr-navy"))
d7.append(arrow(720, 150, 790, 125, "Escala a U3", "#1F497D", "arr-navy", dashed=True))
write_diagram("diag-07-modelo-datos-der", "CRITERIO 2.1.4.8 & 2.1.4.9 · MODELO HÍBRIDO DE DATOS", "Diagrama Entidad-Relación (PoC SQLite 4 Tablas 3FN + Proyección PostgreSQL 16 U3)", "\n".join(d7))


# 8. MAPA DE NAVEGACIÓN UX/UI (5 RUTAS VUE ROUTER · COCKPIT 100% ZOOM)
d8 = []
d8.append(zone(20, 20, 1120, 620, "ARQUITECTURA DE INFORMACIÓN Y FLUJO FULLSCREEN STUDIO COCKPIT (ZOOM 100% · VUE ROUTER)"))
steps = [
    (45, 75, "VISTA 0: /auth", ["Acceso Operador / Demo", "Credenciales 1-Clic", "Persistencia Sesión JWT"], "#1F497D", "P01"),
    (265, 75, "VISTA 1: /recinto", ["8 Presets + Geometría", "Entorno (Indoor / Parcela)", "Ruido D.S. N° 38 + Grilla"], "#1F497D", "P02"),
    (485, 75, "VISTA 2: /equipos", ["Tops & Subs Activo/Pasivo", "Rack de Potencias Pasivas", "Fuente 220V / Generador"], "#c81e1e", "P03"),
    (705, 75, "VISTA 3: /plano-2d", ["Blueprint 5 Capas Exclusivas", "Postes Guía RIC 10 + Haas", "Pioneer DJM + Plan B"], "#059669", "P04 / P05"),
    (925, 75, "VISTA 4: /reporte", ["Plano Vista Completa (ALL)", "Cotizador Arriendo CLP", "PDF Dual-Page + PNG 300 DPI"], "#d97706", "P06"),
]
for i, (sx, sy, sttl, slines, col, bdg) in enumerate(steps):
    d8.append(box(sx, sy, 195, 145, sttl, slines, "#ffffff", col, bdg))
    if i < len(steps) - 1:
        d8.append(arrow(sx+195, sy+72, sx+220, sy+72, "", col, "arr"))

d8.append(box(45, 270, 330, 155, "Navegación URL y Persistencia", ["• Cada paso posee ruta URL propia", "• Auto-guardado continuo en localStorage", "• Validación reactiva Zod en tiempo real", "• Telemetría fija en Header y Footer"], "#eff6ff", "#1F497D", "UX SHELL"))
d8.append(box(410, 270, 345, 155, "Interacciones Clave (Vistas 2, 3 y 4)", ["• Conmutador Activa/Pasiva -> Rack Powers", "• Tabs CAD exclusivas (cero ruido visual)", "• Vista Completa (ALL) consolidada en Reporte", "• Cotizador Propios vs Rider Arrendado CLP"], "#fef2f2", "#c81e1e", "CORE INTERACTION"))
d8.append(box(790, 270, 325, 155, "Ergonomía 100% Zoom y Móvil", ["• Desktop 100% zoom sin scroll global", "• Tablet 768px y Móvil 412px responsivos", "• Dark Mode técnico (#080a10) FOH", "• Botones táctiles y contraste WCAG AA"], "#ecfdf5", "#059669", "RESPONSIVE"))
d8.append(box(45, 465, 1070, 135, "Ciclo Cerrado de Retroalimentación (DISTORSIONCL SPA — Amaro Artiaga)", [
    "Iteración 1: Presets en 1-clic y botón WhatsApp  |  Iteración 2: Lotes Activa/Pasiva, cables XLR/Speakon sin sobrantes",
    "Iteración 3: Postes guía esquineros SEC RIC N° 10 (R >= 6d) + Réplica visual exacta Pioneer DJM (17 LEDs + Low Kill)",
    "Iteración 4: Cockpit 100% zoom, Plano Blueprint 5 capas (ALL en reporte), Rack de Potencias Pasivas, Arriendo CLP y PDF Dual-Page"
], "#ffffff", "#1F497D", "FEEDBACK LOOP"))

d8.append(arrow(582, 220, 582, 270, "Detalle", "#c81e1e", "arr-red"))
d8.append(arrow(802, 220, 952, 270, "Responsive", "#059669", "arr-green"))
d8.append(arrow(142, 220, 210, 270, "Rutas", "#1F497D", "arr-navy"))
write_diagram("diag-08-mapa-navegacion-ux", "CRITERIO 2.1.3.5 & 2.1.3.6 · ARQUITECTURA DE INFORMACIÓN UX/UI", "Mapa de Navegación Cockpit (5 Rutas URL), Interacciones Clave y Diseño Responsivo", "\n".join(d8))

print("ALL 8 DIAGRAMS GENERATED SUCCESSFULLY")
