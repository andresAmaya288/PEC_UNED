#!/usr/bin/env python3
"""
run_analysis.py

Script wrapper que ejecuta el pipeline completo de análisis:
1. normalize_recalls.py   — Normaliza los fields de recall en datos/
2. analyze_recall.py      — Procesa datos normalizados y genera table1.csv (separado por grupo) + análisis estadístico
3. plot_results.py        — Genera gráficos basados en table1.csv

Uso:
    python run_analysis.py

Asume:
- datos/                  — CSV originales del experimento
- datos/normalized/       — (creado por normalize_recalls) CSV normalizados
- results/                — (creado) CSV table1, análisis y gráficos

Procesará automáticamente N participantes.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_pipeline():
    root = Path(__file__).parent
    
    print("="*70)
    print("PIPELINE DE ANÁLISIS - PEC PSICOLOGÍA DE LA MEMORIA")
    print("="*70)
    print()
    
    # Step 1: Normalize recalls
    print("[1/3] Normalizando archivos de recall...")
    print("-"*70)
    try:
        result = subprocess.run(
            [sys.executable, str(root / 'normalize_recalls.py')],
            cwd=str(root),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        if result.returncode != 0:
            print(f"Error en normalize_recalls.py (código {result.returncode})")
            return 1
    except Exception as e:
        print(f"Error ejecutando normalize_recalls.py: {e}")
        return 1
    
    print()
    
    # Step 2: Analyze recall
    print("[2/3] Analizando datos de recall (table1 y ANOVA)...")
    print("-"*70)
    try:
        result = subprocess.run(
            [sys.executable, str(root / 'analyze_recall.py'), '--datos', 'datos/normalized'],
            cwd=str(root),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        if result.returncode != 0:
            print(f"Error en analyze_recall.py (código {result.returncode})")
            return 1
    except Exception as e:
        print(f"Error ejecutando analyze_recall.py: {e}")
        return 1
    
    print()
    
    # Step 3: Plot results
    print("[3/3] Generando gráficos...")
    print("-"*70)
    try:
        result = subprocess.run(
            [sys.executable, str(root / 'plot_results.py')],
            cwd=str(root),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        if result.returncode != 0:
            print(f"Error en plot_results.py (código {result.returncode})")
            return 1
    except Exception as e:
        print(f"Error ejecutando plot_results.py: {e}")
        return 1
    
    print()
    print("="*70)
    print("✓ PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*70)
    print()
    print("Archivos generados:")
    print(f"  - results/table1.csv              (Tabla resumen, separada por grupo)")
    print(f"  - results/analysis_results.txt    (Análisis estadístico: ANOVA, paired t-tests)")
    print(f"  - results/plot_*.png              (Gráficos: medias, interacción, distribuciones, boxplot, paired)")
    print()
    
    return 0


if __name__ == '__main__':
    rc = run_pipeline()
    sys.exit(rc)
