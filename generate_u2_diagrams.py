import os
import subprocess
from html import escape

OUT_DIR = r"D:\Dev\INACAP\stage-plan-main\stage-plan-main\entrega_sumativa_02\diagrams"
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
# Gantt header weeks
weeks = ["S1 (Sem 1-2)", "S2 (Sem 3-4)", "S3 (Sem 5-6)", "S4 (Sem 7-8)", "Cierre U2"]
for i, w in enumerate(weeks):
    gx = 240 + i * 176
    d1.append(f'<rect x="{gx}" y="42" width="170" height="22" rx="4" fill="#1F497D"/>')
    d1.append(f'<text x="{gx+85}" y="57" fill="#ffffff" font-size="10" font-weight="700" font-family="Segoe UI, sans-serif" text-anchor="middle">{w}</text>')
gantt_rows = [
    ("T01-T04 Diagnostico & Zod", 240, 170, "#1F497D", "CRITICA"),
    ("T05-T08 Motor SEC + Haas + 70 Tests", 416, 220, "#c81e1e", "CRITICA"),
    ("T09-T12 Backend Express + Prisma + JWT", 560, 180, "#1F497D", "CRITICA"),
    ("T13-T16 Vue 3 + Layout 2D + Pioneer DJM", 720, 220, "#c81e1e", "CRITICA"),
    ("T17-T20 OWASP + Benchmark + Entrega U2", 910, 200, "#059669", "HITO FINAL"),
]
for idx, (lbl, bx, bw, col, st) in enumerate(gantt_rows):
    ry = 76 + idx * 42
    d1.append(f'<text x="34" y="{ry+18}" fill="#1e293b" font-size="10.5" font-weight="700" font-family="Segoe UI, sans-serif">{lbl}</text>')
    d1.append(f'<rect x="{bx}" y="{ry+2}" width="{bw}" height="26" rx="5" fill="{col}" fill-opacity="0.9"/>')
    d1.append(f'<text x="{bx+bw/2}" y="{ry+19}" fill="#ffffff" font-size="9.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{st}</text>')
d1.append(f'<text x="34" y="294" fill="#c81e1e" font-size="9.5" font-weight="700" font-family="Consolas, monospace">Ruta Crítica: T01 → T02 → T05 → T08 → T12 → T15 → T18 → T20 (Dependencias Finish-to-Start sin holgura)</text>')

d1.append(zone(20, 326, 1120, 316, "TABLERO KANBAN Y POLÍTICA WIP (SOLO-DEVELOPER MAURICIO VEGA)"))
cols = [
    ("BACKLOG (MoSCoW)", "Sin límite", "#64748b", ["HU09 Exportación CSV", "HU10 Histórico Multi-Sede"]),
    ("SELECTED FOR DEV", "WIP Max: 3", "#1F497D", ["T18 Auditoría OWASP ZAP", "T19 Validación k6 5 VUs"]),
    ("IN PROGRESS", "WIP Max: 1", "#c81e1e", ["T20 Compilación DOCX Final", "(Foco exclusivo sin multitarea)"]),
    ("TESTING / TDD", "WIP Max: 2", "#d97706", ["10 suites Vitest (70/70 OK)", "vue-tsc + vite build OK"]),
    ("DONE (DoD 100%)", "Completado", "#059669", ["Motor SEC RIC 03/10 & Haas", "Layout 2D + Postes Guía", "Réplica Pioneer DJM + PDF"]),
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
d2.append(zone(20, 20, 250, 610, "NODO CLIENTE TERRENO (OFFLINE-FIRST)"))
d2.append(box(40, 70, 210, 110, "Smartphone / Laptop FOH", ["Chrome Mobile / Safari", "PWA + jsPDF Client-Side", "Modo Avión en Parcelas"], "#ffffff", "#1F497D", "CLIENT"))
d2.append(box(40, 230, 210, 120, "Renderizado Reactivo Local", ["Motor @stageplan/shared", "Cálculo < 2 ms en Memoria", "LayoutSvg2D + Pioneer DJM"], "#ffffff", "#059669", "EDGE"))
d2.append(box(40, 400, 210, 100, "Salida Operacional Terreno", ["Ficha PDF Vectorial SEC", "Resumen Texto WhatsApp"], "#ffffff", "#d97706", "OFFLINE"))

d2.append(zone(305, 20, 835, 610, "INFRAESTRUCTURA SERVIDOR CLOUD / VPS LINUX UBUNTU 22.04 LTS"))
d2.append(box(335, 110, 190, 105, "Reverse Proxy Nginx", ["TLS 1.3 + HSTS Forzado", "Único Puerto Expuesto :443", "Terminación SSL"], "#ffffff", "#c81e1e", "PROXY :443"))
d2.append(box(590, 70, 240, 125, "Frontend SPA (@stageplan/frontend)", ["Vue 3.5 + Vite 6.1 + Tailwind", "Pinia Store + Zod Validation", "Sirve Bundle Estático"], "#ffffff", "#1F497D", "FRONTEND"))
d2.append(box(590, 260, 240, 175, "API REST (@stageplan/backend)", ["Node.js v24 + Express 4.21 :3000", "Helmet + CORS + RateLimit (200/15m)", "JWT + Bcrypt(12) + Anti-IDOR", "Prisma ORM Client"], "#ffffff", "#c81e1e", "BACKEND :3000"))
d2.append(box(885, 260, 230, 175, "PostgreSQL 16 (:5432)", ["12 Tablas Relacionales 3FN", "Documentos JSONB + Índices GIN", "Triggers SEC RIC N° 10", "Audit Logs Forenses"], "#ffffff", "#1F497D", "PERSISTENCE"))
d2.append(box(590, 485, 525, 110, "Motor Compartido Isomórfico (@stageplan/shared · 11 Módulos)", ["electrical.ts · cabling.ts · acoustics.ts · hybrid-roster.ts · lighting-dmx.ts", "power-distribution.ts · dj-setup-audio.ts · stage-acoustic-engine.ts · schemas.ts (Zod)"], "#eff6ff", "#1F497D", "SHARED KERNEL"))

d2.append(arrow(250, 125, 335, 150, "HTTPS TLS 1.3", "#c81e1e", "arr-red", lx=292, ly=115))
d2.append(arrow(525, 140, 590, 130, "Static", "#1F497D", "arr-navy"))
d2.append(path_arrow("M 525 180 L 555 180 L 555 320 L 590 320", "REST /api/*", "#c81e1e", "arr-red", lx=555, ly=248))
d2.append(arrow(830, 345, 885, 345, "TCP :5432", "#1F497D", "arr-navy"))
d2.append(arrow(145, 180, 145, 230, "Local", "#059669", "arr-green"))
d2.append(arrow(145, 350, 145, 400, "Blob PDF", "#d97706", "arr"))
d2.append(arrow(710, 435, 710, 485, "Import", "#1F497D", "arr-navy"))
write_diagram("diag-02-arquitectura-4plus1-despliegue", "CRITERIO 2.1.2.3 & 2.1.2.4 · VISTA FÍSICA Y DESPLIEGUE 4+1", "Arquitectura Tecnológica, Despliegue Seguro y Capacidad Offline-First", "\n".join(d2))


# 3. ESCENARIOS - CASO DE USO CERO (CU-00)
d3 = []
d3.append(zone(260, 25, 650, 610, "LÍMITE DEL SISTEMA: STAGE PLAN (CASO DE USO CERO: CU-00)"))
# Actors on left & right
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
d3.append(actor(110, 420, "Chofer / Bodeguero", "Enlace Compartido"))
d3.append(actor(1030, 260, "Administrador", "Auditoría RBAC"))

d3.append(usecase(430, 320, 130, 44, "CU-00", "Planificación Logística Integral", "#eff6ff", "#1F497D"))
ucs = [
    (740, 85, "CU-01", "Autenticación JWT & RBAC", "#ffffff", "#1F497D"),
    (740, 165, "CU-02", "Recinto & Ruido D.S. N° 38", "#ffffff", "#1F497D"),
    (740, 245, "CU-03", "Ruteo SEC RIC 10 + Postes Guía", "#fef2f2", "#c81e1e"),
    (740, 325, "CU-04", "Cajas Activa/Pasiva + Powers", "#ffffff", "#1F497D"),
    (740, 405, "CU-05", "Iluminación DMX x1 + Cables", "#ffffff", "#1F497D"),
    (740, 485, "CU-06", "Simulador Pioneer DJM & Haas", "#ffffff", "#059669"),
    (740, 565, "CU-08", "Exportar PDF & Ley del Saco", "#ffffff", "#d97706"),
]
for ux, uy, code, ttl, fl, st in ucs:
    d3.append(usecase(ux, uy, 145, 28, code, ttl, fl, st))
    rel = "<<extend>>" if code in ("CU-04", "CU-06") else "<<include>>"
    d3.append(arrow(556, 320, 595, uy, rel, st, "arr", dashed=True, lx=575, ly=(320+uy)/2 - 4))

d3.append(arrow(140, 185, 300, 310, "Opera", "#1F497D", "arr-navy"))
d3.append(arrow(140, 460, 595, 565, "Descarga", "#d97706", "arr"))
d3.append(arrow(995, 290, 885, 90, "Audita", "#1F497D", "arr-navy"))
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

d4.append(uml_class(30, 30, 235, "User (RBAC)", ["- id: UUID", "- email: String", "- rol: RoleEnum", "- passwordHash: String"], ["+ authenticate(): JWT", "+ verifyOwnership(id): Bool"]))
d4.append(uml_class(30, 225, 235, "Venue", ["- id: UUID", "- widthMeters: Float", "- depthMeters: Float", "- electricalDistMeters: Float", "- wallType: WallEnum"], ["+ getAreaM2(): Float", "+ estimateNoiseDS38(): Db"]))
d4.append(uml_class(30, 440, 235, "EquipmentLot", ["- lotRole: TOP_PA | SUB", "- technology: ACTIVE|PASSIVE", "- rmsWatts: Int", "- powerAmpWatts: Int?", "- impedanceOhms: Float"], ["+ isSpeakOnSafe(): Bool", "+ getTotalWatts(): Int"]))

d4.append(uml_class(350, 30, 295, "CalculationEngine (Orchestrator)", ["- engineVersion: String = '1.0.0'", "- MAX_VOLTAGE_DROP: Float = 3.0"], ["+ runFullAudit(venue, lots): Result", "+ validateWithZod(input): Boolean"], "#c81e1e"))
d4.append(uml_class(350, 190, 295, "ElectricalSECValidator", ["- COPPER_RHO: Float = 0.0175", "- SAFETY_MARGIN: Float = 1.25"], ["+ calcVoltageDropPct(L, I, S): Float", "+ calcGuidePostsBendRadius(d): Float", "+ splitLinesL1L2L3(loads): Circuits"]))
d4.append(uml_class(350, 375, 295, "AcousticHaasEngine", ["- SOUND_SPEED_20C: Float = 343.2"], ["+ calcClusterGainDb(subs): Float", "+ calcDelayHaasMs(distM): Float", "+ computeSplHeatMap(): ZoneMap"]))
d4.append(uml_class(350, 530, 295, "LightingDmxCalculator", ["- DMX_MAX_CH: Int = 512"], ["+ calcSingleUnitsX1(fixtures): Int", "+ calcDmxCableMeters(cabina, z): Float"], "#059669"))

d4.append(uml_class(740, 30, 380, "RiderCalculation (Hybrid Persist)", ["- id: UUID", "- venueId: UUID", "- riderInput: JSONB", "- calculatedResults: JSONB", "- alertsSnapshot: JSONB"], ["+ persistAtomically(): RiderCalc", "+ toPdfPayload(): PdfReport"]))
d4.append(uml_class(740, 240, 380, "DjSetupAndGainSimulator", ["- ch1LowActive: Boolean", "- ch2LowActive: Boolean", "- masterPos: 12_OCLOCK|2_OCLOCK|MAX"], ["+ calcMasterOutputDb(): Float", "+ getLedMeterSegments(): LedState[]", "+ buildCableChecklist(): AudioRoute[]"], "#d97706"))
d4.append(uml_class(740, 435, 380, "SharedLink & Logistics", ["- token: String (Unique)", "- expiresAt: DateTime", "- maxSackWeightKg: Int = 25"], ["+ checkLeyDelSaco20949(kg): Alert", "+ generateVanCubicLoad(): VanPlan"]))

d4.append(arrow(265, 95, 350, 80, "1..*", "#1F497D", "arr-navy"))
d4.append(arrow(265, 285, 350, 110, "input", "#1F497D", "arr-navy"))
d4.append(arrow(265, 500, 350, 250, "loads", "#1F497D", "arr-navy"))
d4.append(arrow(645, 95, 740, 95, "persiste", "#c81e1e", "arr-red"))
d4.append(arrow(495, 145, 495, 190, "usa SEC", "#c81e1e", "arr-red"))
d4.append(arrow(495, 336, 495, 375, "usa Haas", "#1F497D", "arr-navy"))
d4.append(arrow(495, 496, 495, 530, "usa DMX", "#059669", "arr-green"))
d4.append(arrow(645, 430, 740, 310, "simula", "#d97706", "arr"))
d4.append(arrow(645, 120, 740, 485, "genera", "#1F497D", "arr-navy"))
write_diagram("diag-04-vista-logica-clases", "CRITERIO 2.1.2.3 · VISTA LÓGICA (4+1)", "Diagrama de Clases del Dominio (STAGE PLAN)", "\n".join(d4))


# 5. VISTA DE DESARROLLO - COMPONENTES MONOREPO
d5 = []
d5.append(zone(20, 20, 1120, 620, "MONOREPO STAGE PLAN (NPM WORKSPACES · TYPESCRIPT STRICT)"))
d5.append(zone(45, 60, 325, 550, "@stageplan/frontend (Vue 3.5 + Vite 6.1)"))
d5.append(box(65, 105, 285, 85, "App.vue & Pinia Store", ["Wizard 5 Pasos (0..4)", "Estado Reactivo Local"], "#ffffff", "#1F497D", "UI SHELL"))
d5.append(box(65, 210, 285, 95, "LayoutSvg2D.vue", ["Plano Escala Dinámica", "Postes Guía SEC RIC 10", "Cluster + Delays Haas"], "#ffffff", "#c81e1e", "SVG ENGINE"))
d5.append(box(65, 325, 285, 95, "PioneerMixerSimulator.vue", ["Réplica Hardware DJM", "Vúmetros 17 LEDs + Low Kill", "Perilla Master 12:00/2:00"], "#ffffff", "#d97706", "SIMULATOR"))
d5.append(box(65, 440, 285, 85, "services/pdfReport.ts", ["jsPDF + jspdf-autotable", "Generación 100% Offline"], "#ffffff", "#059669", "PDF OFFLINE"))

d5.append(zone(415, 60, 320, 550, "@stageplan/shared (Núcleo Isomórfico)"))
d5.append(box(435, 105, 280, 90, "schemas.ts (Zod Contracts)", ["Validación Isomórfica", "Venue, Equipment, Lighting"], "#eff6ff", "#1F497D", "ZOD"))
d5.append(box(435, 215, 280, 175, "calc-engine/ (11 Módulos TS)", ["electrical.ts · cabling.ts", "acoustics.ts · hybrid-roster.ts", "lighting-dmx.ts · routing.ts", "dj-setup-audio.ts · inventory.ts", "power-distribution.ts", "stage-acoustic-engine.ts", "contingency-and-logistics.ts"], "#ffffff", "#1F497D", "PURE LOGIC"))
d5.append(box(435, 415, 280, 110, "tests/ (Vitest v3.2.7)", ["10 archivos .spec.ts", "70 Pruebas Unitarias TDD", "100% PASS Quality Gate"], "#ecfdf5", "#059669", "TDD VITEST"))

d5.append(zone(780, 60, 335, 550, "@stageplan/backend (Express + Prisma)"))
d5.append(box(800, 105, 295, 105, "server.ts & Middlewares", ["Helmet + CORS + RateLimit", "authMiddleware (JWT Verify)", "Protección Anti-IDOR"], "#ffffff", "#c81e1e", "SECURITY"))
d5.append(box(800, 235, 295, 130, "REST Controllers", ["AuthController (/api/auth/*)", "VenueController (/api/venues/*)", "CalculationController"], "#ffffff", "#1F497D", "API REST"))
d5.append(box(800, 390, 295, 135, "Prisma ORM + PostgreSQL 16", ["prisma/schema.prisma", "Consultas Parametrizadas", "Relacional 3FN + JSONB"], "#ffffff", "#1F497D", "DATA LAYER"))

d5.append(arrow(350, 150, 435, 150, "import", "#1F497D", "arr-navy"))
d5.append(arrow(350, 260, 435, 260, "calcula", "#c81e1e", "arr-red"))
d5.append(arrow(800, 280, 715, 160, "valida Zod", "#1F497D", "arr-navy"))
d5.append(arrow(800, 320, 715, 300, "ejecuta", "#1F497D", "arr-navy"))
d5.append(arrow(945, 210, 945, 235, "filtra", "#c81e1e", "arr-red"))
d5.append(arrow(945, 365, 945, 390, "ACID", "#1F497D", "arr-navy"))
write_diagram("diag-05-vista-desarrollo-componentes", "CRITERIO 2.1.2.3 · VISTA DE DESARROLLO (4+1)", "Diagrama de Componentes del Monorepo TypeScript (3 Paquetes)", "\n".join(d5))


# 6. VISTA DE PROCESOS - BPMN 2.0
d6 = []
d6.append(zone(20, 20, 1120, 195, "CARRIL 1: OPERADOR TÉCNICO FOH (TERRENO / PRE-PRODUCCIÓN)"))
d6.append(zone(20, 225, 1120, 215, "CARRIL 2: MOTOR DETERMINISTA STAGE PLAN (VALIDACIÓN Y CÁLCULO)"))
d6.append(zone(20, 450, 1120, 190, "CARRIL 3: SALIDA OPERACIONAL & PERSISTENCIA (POSTGRESQL / PDF OFFLINE)"))

# Start circle
d6.append('<circle cx="70" cy="120" r="18" fill="#ecfdf5" stroke="#059669" stroke-width="2.2"/>')
d6.append('<text x="70" y="152" fill="#059669" font-size="9" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">INICIO</text>')
d6.append(box(120, 80, 165, 80, "1. Ingresar Recinto", ["Ancho, Largo, Vecinos", "Acometida 220V SEC"], "#ffffff", "#1F497D"))
d6.append(box(320, 80, 185, 80, "2. Configurar Equipos", ["Tops/Subs Activa o Pasiva", "Powers + Luces DMX x1"], "#ffffff", "#1F497D"))

d6.append(box(320, 285, 185, 85, "3. Validación Zod", ["Rango 1..500m, Watts > 0", "Saneamiento Inputs"], "#eff6ff", "#1F497D"))
# Gateway XOR
def gateway(gx, gy, label):
    pts = f"{gx},{gy-28} {gx+28},{gy} {gx},{gy+28} {gx-28},{gy}"
    return (
        f'<polygon points="{pts}" fill="#fffbeb" stroke="#d97706" stroke-width="2"/>'
        f'<text x="{gx}" y="{gy+5}" fill="#d97706" font-size="16" font-weight="900" text-anchor="middle">X</text>'
        f'<text x="{gx}" y="{gy+42}" fill="#475569" font-size="8.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(label)}</text>'
    )
d6.append(gateway(585, 327, "SEC ΔV<=3% y Z>=3.2?"))
d6.append(box(685, 255, 200, 70, "Alerta / Rebalanceo", ["Dividir L1/L2/L3 + Calibre", "Sugerir Postes Guía RIC 10"], "#fef2f2", "#c81e1e"))
d6.append(box(685, 345, 200, 75, "Cálculo Aprobado OK", ["Delays Haas + Cluster +6dB", "Metraje DMX y Pioneer DJM"], "#ecfdf5", "#059669"))

d6.append(box(320, 505, 230, 85, "4. Persistir en PostgreSQL 16", ["Tablas 3FN + JSONB Snapshot", "Trigger SEC Validado"], "#ffffff", "#1F497D"))
d6.append(box(685, 505, 230, 85, "5. Render Layout 2D + PDF", ["Mapa SVG con Postes Guía", "PDF Offline Modo Avión"], "#ffffff", "#059669"))
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
d6.append(arrow(915, 547, 1012, 547, "Listo", "#059669", "arr-green"))
write_diagram("diag-06-vista-procesos-bpmn", "CRITERIO 2.1.2.3 · VISTA DE PROCESOS (4+1)", "Diagrama de Procesos de Negocio (BPMN 2.0) — Pre-Producción y Validación SEC", "\n".join(d6))


# 7. MODELO DE DATOS DER (3FN + JSONB)
d7 = []
def der_table(x, y, w, name, cols, stroke="#1F497D"):
    h = 26 + len(cols) * 14 + 6
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="#ffffff" stroke="{stroke}" stroke-width="1.3"/>']
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="3" fill="{stroke}"/>')
    out.append(f'<text x="{x+w/2}" y="{y+16}" fill="#ffffff" font-size="10.5" font-weight="700" font-family="Consolas, monospace" text-anchor="middle">{escape(name)}</text>')
    for i, c in enumerate(cols):
        col = "#c81e1e" if "PK" in c else ("#059669" if "JSONB" in c else "#334155")
        out.append(f'<text x="{x+8}" y="{y+39+i*14}" fill="{col}" font-size="8.6" font-family="Consolas, monospace">{escape(c)}</text>')
    return "\n".join(out)

d7.append(der_table(25, 25, 200, "roles", ["PK id: smallint", "   nombre: text (UNIQUE)", "   descripcion: text"]))
d7.append(der_table(25, 145, 225, "users", ["PK id: uuid", "FK rol_id -> roles.id", "   email: text (UNIQUE)", "   password_hash: text", "   intentos_fallidos: int"]))
d7.append(der_table(25, 315, 225, "audit_logs", ["PK id: bigint", "FK user_id -> users.id", "   event_type: text", "   detail_json: JSONB (GIN)"]))
d7.append(der_table(25, 470, 225, "user_feedback", ["PK id: uuid", "FK user_id -> users.id", "   app_version: text", "   finding / status: text"]))

d7.append(der_table(320, 25, 250, "venues", ["PK id: uuid", "FK owner_id -> users.id", "   width_meters / depth_meters", "   electrical_distance_meters", "   neighbor_distance / wall_type"]))
d7.append(der_table(320, 195, 260, "rider_calculations (HÍBRIDA)", ["PK id: uuid", "FK owner_id -> users.id", "FK venue_id -> venues.id", "   rider_input: JSONB (GIN)", "   calculated_results: JSONB (GIN)", "   alerts_snapshot: JSONB"], "#059669"))
d7.append(der_table(320, 390, 250, "shared_links", ["PK id: uuid", "FK rider_calculation_id", "   token: text (UNIQUE)", "   expires_at / is_revoked"]))
d7.append(der_table(320, 520, 250, "equipment_catalog", ["PK id: uuid", "   category / brand / model", "   specs_json: JSONB (GIN)"], "#059669"))

d7.append(der_table(675, 25, 455, "equipment_lots (Activa / Pasiva / Power)", ["PK id: uuid | FK calculation_id -> rider_calculations.id", "FK catalog_id -> equipment_catalog.id", "   technology: ACTIVE|PASSIVE | power_amp_watts: int", "   impedance_ohms CHECK >= 2.0 | is_protect_alert: bool"]))
d7.append(der_table(675, 175, 455, "lighting_fixtures (Conteo x1 + DMX)", ["PK id: uuid | FK calculation_id -> rider_calculations.id", "   fixture_type: PAR_LED_X1 | watts_per_unit: int", "   dmx_channels: smallint | dmx_cable_meters: numeric"]))
d7.append(der_table(675, 315, 455, "electrical_circuits (SEC RIC 03/10 + Postes Guía)", ["PK id: uuid | FK calculation_id -> rider_calculations.id", "   line_code: L1|L2|L3 | power_strip_code: text", "   cable_section_mm2 | voltage_drop_pct CHECK <= 3.0", "   guide_posts_count | min_bend_radius_mm CHECK >= 48"], "#c81e1e"))
d7.append(der_table(675, 470, 455, "audio_routes (XLR / TRS-Booth / RJ45 / Speakon)", ["PK id: uuid | FK calculation_id -> rider_calculations.id", "   source_device -> target_device", "   signal_type | length_meters | haas_delay_ms"]))

d7.append(arrow(125, 100, 125, 145, "1:N", "#1F497D", "arr-navy"))
d7.append(arrow(250, 195, 320, 85, "1:N", "#1F497D", "arr-navy"))
d7.append(arrow(445, 145, 445, 195, "1:N", "#059669", "arr-green"))
d7.append(arrow(445, 340, 445, 390, "1:N", "#1F497D", "arr-navy"))
d7.append(arrow(580, 225, 675, 80, "1:N", "#1F497D", "arr-navy"))
d7.append(arrow(580, 245, 675, 225, "1:N", "#1F497D", "arr-navy"))
d7.append(arrow(580, 265, 675, 370, "1:N", "#c81e1e", "arr-red"))
d7.append(arrow(580, 285, 675, 515, "1:N", "#1F497D", "arr-navy"))
write_diagram("diag-07-modelo-datos-der", "CRITERIO 2.1.4.8 & 2.1.4.9 · MODELO HÍBRIDO POSTGRESQL 16", "Diagrama Entidad-Relación (12 Tablas 3FN + Documentos JSONB GIN)", "\n".join(d7))


# 8. MAPA DE NAVEGACIÓN UX/UI (WIZARD 5 PASOS)
d8 = []
d8.append(zone(20, 20, 1120, 620, "ARQUITECTURA DE INFORMACIÓN Y FLUJO DEL WIZARD RESPONSIVO (STAGE PLAN)"))
steps = [
    (45, 75, "PASO 0: OPERADOR", ["Autenticación / Perfil", "Acceso Rápido Demo 1-Clic", "Guardado Local / Carga"], "#1F497D", "P01"),
    (265, 75, "PASO 1: RECINTO", ["8 Escenarios + Ancho/Largo", "Entorno (Indoor / Parcela)", "Simulador Ruido D.S. N° 38"], "#1F497D", "P02"),
    (485, 75, "PASO 2: AUDIO Y ENERGÍA", ["Tops & Subs Activo/Pasivo+Power", "Iluminación DMX x1 + Metraje", "Fuente 220V / Generador"], "#c81e1e", "P03"),
    (705, 75, "PASO 3: PLANO 2D Y MIXER", ["Plano Escala + Postes Guía RIC 10", "Cluster Mono + Delays Haas", "Réplica Pioneer DJM + Plan B"], "#059669", "P04 / P05"),
    (925, 75, "PASO 4: REPORTE PDF", ["Plan de Carga (Ley del Saco)", "Protocolo de Encendido 5 Fases", "PDF Offline + Botón WhatsApp"], "#d97706", "P06"),
]
for i, (sx, sy, sttl, slines, col, bdg) in enumerate(steps):
    d8.append(box(sx, sy, 195, 145, sttl, slines, "#ffffff", col, bdg))
    if i < len(steps) - 1:
        d8.append(arrow(sx+195, sy+72, sx+220, sy+72, "", col, "arr"))

# Subflows detail below
d8.append(box(45, 280, 330, 155, "Navegación Secundaria y Asistencia", ["• InfoBadge (?) en cada parámetro físico", "• Validación reactiva Zod en tiempo real", "• Guardado automático en localStorage", "• Enlace compartido solo-lectura para chofer"], "#eff6ff", "#1F497D", "UX ASSIST"))
d8.append(box(410, 280, 345, 155, "Interacciones Críticas (Paso 2 y Paso 3)", ["• Cambio de tecnología Activa <-> Pasiva", "• Selector Power + Alerta Speakon < 3.2Ω", "• Perilla LOW Kill (12:00 <-> -∞ 7:00)", "• Master Rotary (12:00 / 2:00 / Clip)"], "#fef2f2", "#c81e1e", "CORE INTERACTION"))
d8.append(box(790, 280, 325, 155, "Adaptabilidad Multi-Dispositivo (WCAG AA)", ["• Desktop 1280px+: Vista multipanel FOH", "• Tablet 768px: Grilla fluida 2 columnas", "• Móvil 412px (Terreno): Botones >= 44px", "• Dark Mode técnico (#09090d) anti-encandilamiento"], "#ecfdf5", "#059669", "RESPONSIVE"))
d8.append(box(45, 475, 1070, 120, "Ciclo Cerrado de Retroalimentación (DISTORSIONCL SPA — Amaro Artiaga)", ["Iteración Iteración 1: Catálogo preajustes 1-clic y botón WhatsApp  |  Iteración 2: Activa/Pasiva con Power, luces x1 y mapa a escala", "Iteración 3: Postes guía esquineros (radio curvatura SEC RIC N° 10) + Réplica visual exacta Pioneer DJM con vúmetros verticales"], "#ffffff", "#1F497D", "FEEDBACK LOOP"))

d8.append(arrow(582, 220, 582, 280, "Detalle", "#c81e1e", "arr-red"))
d8.append(arrow(802, 220, 952, 280, "Responsive", "#059669", "arr-green"))
d8.append(arrow(142, 220, 210, 280, "Ayuda", "#1F497D", "arr-navy"))
write_diagram("diag-08-mapa-navegacion-ux", "CRITERIO 2.1.3.5 & 2.1.3.6 · ARQUITECTURA DE INFORMACIÓN UX/UI", "Mapa de Navegación del Wizard, Interacciones Clave y Diseño Responsivo", "\n".join(d8))

print("ALL 8 DIAGRAMS GENERATED SUCCESSFULLY")
