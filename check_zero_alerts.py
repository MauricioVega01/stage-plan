import re

files = {
    'informe': r'stage-plan-main/INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md',
    'guion': r'stage-plan-main/GUION_PRESENTACION_PROFESOR.md',
    'docx_gen': r'stage-plan-main/generate_sumativa_02_docx.py'
}

patterns = [
    (r'\b(dmx|par led|luminaria|foco)\b', 'DMX / Iluminación'),
    (r'\b(d\.s\.\s*(?:n[°o]\s*)?38|ruido vecinal)\b', 'D.S. 38 / Ruido'),
    (r'\b(modo avi[oó]n|offline-first)\b', 'Modo Avión / Offline inflado'),
    (r'\b(44\s*tests|44\s*pruebas)\b', 'Tests desactualizados (44 vs 70)'),
    (r'\b(hopkins|sabine|rt60|splay angle)\b', 'Física teórica riesgosa')
]

total_alertas = 0
for name, path in files.items():
    print(f'=== AUDITORIA: {name} ===')
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for pat, label in patterns:
        matches = []
        for i, l in enumerate(lines):
            # Excepcion legitima: seccion 'Won't Have / Fuera de alcance' donde se aclara que NO se hace DMX
            if 'fuera de alcance' in l.lower() or "won't have" in l.lower():
                continue
            if re.search(pat, l, re.IGNORECASE):
                matches.append((i+1, l.strip()[:90]))
        if matches:
            total_alertas += len(matches)
            print(f'  [ALERTA] {label}: {len(matches)} coincidencias')
            for line_no, sample in matches:
                print(f'    L{line_no}: {sample}')
        else:
            print(f'  [OK] {label}: 0 alertas')

print('-----------------------------------------')
print('TOTAL ALERTAS DETECTADAS:', total_alertas)
if total_alertas == 0:
    print('ESTADO: 100% COHERENTE Y LIMPIO.')
