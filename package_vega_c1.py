import os
import zipfile

def package_vega_c1():
    zip_filename = "Vega_C1.zip"
    print(f"Creating {zip_filename} with v4.0 deliverables and source code...")
    
    files_to_include = [
        "Proyecto Integrado 1.docx",
        "TIHV43_GUÍA_ABPRO_U1.docx",
        "Formato_propuesto_sumativa 01_2026.docx",
        "Presentacion_Proyecto_STAGE_PLAN_Profesor.pdf",
        "GUION_PRESENTACION_PROFESOR.md",
        "INFORME_PRUEBAS_TDD_CALC_ENGINE.md",
        "MANUAL_DE_USUARIO_STAGEPLANNER.md",
        "MATRIZ_TRAZABILIDAD_STAGEPLANNER.md",
        "package.json"
    ]
    
    dirs_to_include = [
        "packages/backend",
        "packages/frontend",
        "packages/shared"
    ]
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_include:
            if os.path.exists(f):
                zf.write(f, arcname=f)
                print(f"  + Added file: {f}")
            else:
                print(f"  ! Warning: {f} not found")
                
        for d in dirs_to_include:
            for root, dirs, files in os.walk(d):
                # Ignore node_modules, dist, .turbo, .cache
                dirs[:] = [sub for sub in dirs if sub not in ('node_modules', 'dist', '.turbo', '.cache', 'coverage')]
                for file in files:
                    filepath = os.path.join(root, file)
                    relpath = os.path.relpath(filepath, '.')
                    zf.write(filepath, arcname=relpath)
                    
    print(f"✓ {zip_filename} packaged successfully.")

if __name__ == '__main__':
    package_vega_c1()

