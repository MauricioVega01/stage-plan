with open(r'stage-plan-main/generate_sumativa_02_docx.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('DMX x1 y PDF Offline', 'Ruteo Cables Audio y Reporte PDF')
text = text.replace('y modo Offline-First.', 'y ejecución local.')
text = text.replace('Olvido de cables DMX/Speakon', 'Olvido de cables de poder o Speakon')
text = text.replace('Should Have: Conteo DMX unitario x1, réplica', 'Should Have: Réplica')
text = text.replace('control hardware USB-DMX directo.', 'control de luminarias por protocolo DMX.')
text = text.replace('el esquema PostgreSQL 16 (4 tablas 3FN + JSONB GIN) equilibran integridad ACID, flexibilidad de inventario y operación Offline-First.',
                    'la base de datos SQLite 3 dev.db (4 tablas 3FN + JSON) equilibran integridad ACID, portabilidad total y agilidad operativa en terreno.')

with open(r'stage-plan-main/generate_sumativa_02_docx.py', 'w', encoding='utf-8') as f:
    f.write(text)

with open(r'stage-plan-main/INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md', 'r', encoding='utf-8') as f:
    inf = f.read()

inf = inf.replace('en Modo Avión', 'de forma local')
inf = inf.replace('Modo Avión', 'modo local')

with open(r'stage-plan-main/INFORME_SUMATIVA_02_TIHV43_MAURICIO_VEGA.md', 'w', encoding='utf-8') as f:
    f.write(inf)

print('Ajustes finales aplicados.')
