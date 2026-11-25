import os
import glob
import re

base_dir = r'stage-plan-main'
md_files = glob.glob(os.path.join(base_dir, '*.md'))

patterns = [
    (r'\b(dmx|par led|luminaria|foco)\b', 'DMX / Iluminacion'),
    (r'\b(d\.s\.\s*(?:n[°o]\s*)?38|ruido vecinal)\b', 'D.S. 38 / Ruido'),
    (r'\b(modo avi[oó]n|offline-first)\b', 'Modo Avion / Offline inflado'),
    (r'\b(44\s*tests|44\s*pruebas)\b', 'Tests desactualizados (44 vs 70)'),
    (r'\b(12\s*tablas)\b', '12 tablas'),
]

print(f'Analizando {len(md_files)} archivos markdown en {base_dir}...')
audit_results = {}

for fpath in md_files:
    fname = os.path.basename(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.readlines()
    
    file_findings = []
    for pat, label in patterns:
        matches = []
        for i, l in enumerate(content):
            # Ignorar si es seccion de fuera de alcance o explicacion de escala futura
            if 'fuera de alcance' in l.lower() or "won't have" in l.lower() or 'schema_stageplan_pg16.sql' in l or 'diseño extendido' in l.lower():
                continue
            if re.search(pat, l, re.IGNORECASE):
                matches.append((i+1, l.strip()[:85]))
        if matches:
            file_findings.append((label, matches))
    
    audit_results[fname] = file_findings

for fname, findings in audit_results.items():
    print(f'=== {fname} ===')
    if not findings:
        print('  [IMPECABLE] Cero inconsistencias.')
    else:
        for label, matches in findings:
            print(f'  [ALERTA] {label}: {len(matches)} coincidencias')
            for lno, txt in matches[:4]:
                print(f'    L{lno}: {txt}')
