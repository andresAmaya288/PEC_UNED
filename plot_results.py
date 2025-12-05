#!/usr/bin/env python3
"""
plot_results.py

Genera gráficos estadísticos relevantes para el análisis del experimento de
niveles de procesamiento (ANOVA 2×2: Grupo × Procesamiento).

Salida:
- `results/plot_means_by_condition.png` — Gráfico de medias con IC 95%
- `results/plot_interaction.png` — Gráfico de interacción (líneas)
- `results/plot_distributions.png` — Distribuciones por grupo
- `results/plot_boxplot.png` — Diagramas de caja por condición

Dependencias: pandas, numpy, matplotlib, seaborn, scipy
Instalación: `pip install pandas numpy scipy matplotlib seaborn`
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# Configure style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['legend.fontsize'] = 10


def load_data(table1_path='results/table1.csv'):
    """Load and prepare data from table1.csv (skips comment lines starting with #)"""
    try:
        df = pd.read_csv(table1_path, comment='#')
    except FileNotFoundError:
        print(f"Error: {table1_path} no encontrado. Ejecuta analyze_recall.py primero.")
        return None
    
    # Remove empty rows
    df = df.dropna(how='all')
    
    if df.empty:
        print("Error: table1.csv no contiene datos válidos.")
        return None
    
    # Melt to long format for easier plotting
    long = pd.DataFrame({
        'Participant': np.repeat(df['Participant'].to_numpy(), 2),
        'Group': np.repeat(df['Group'].to_numpy(), 2),
        'Processing': ['S', 'A'] * len(df),
        'Score': np.concatenate([df['Perc_S'].to_numpy(), df['Perc_A'].to_numpy()])
    })
    
    return df, long


def plot_means_by_condition(long, results_path='results'):
    """
    Plot means and 95% CI by condition (Group × Processing)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate means and CI
    groups = long['Group'].unique()
    procs = ['S', 'A']
    
    means = []
    cis_low = []
    cis_high = []
    labels = []
    x_pos = []
    colors_list = []
    
    colors = {'Incidental': '#FF6B6B', 'Intencional': '#4ECDC4'}
    x = 0
    
    for g in sorted(groups):
        for p in procs:
            data = long.loc[(long['Group'] == g) & (long['Processing'] == p), 'Score']
            data = data.dropna()
            
            m = data.mean()
            se = stats.sem(data)
            df = len(data) - 1
            tcrit = stats.t.ppf(0.975, df) if df > 0 else 1.96
            ci_low = m - tcrit * se
            ci_high = m + tcrit * se
            
            means.append(m)
            cis_low.append(ci_low)
            cis_high.append(ci_high)
            labels.append(f'{g}\n({p})')
            x_pos.append(x)
            colors_list.append(colors[g])
            x += 1
    
    # Plot bars with error bars
    errors = [np.array(means) - np.array(cis_low), np.array(cis_high) - np.array(means)]
    ax.bar(x_pos, means, yerr=errors, capsize=10, color=colors_list, 
           alpha=0.7, edgecolor='black', linewidth=1.5, error_kw={'elinewidth': 2})
    
    ax.set_xlabel('Condición (Grupo × Procesamiento)', fontsize=12, fontweight='bold')
    ax.set_ylabel('% Recuerdo', fontsize=12, fontweight='bold')
    ax.set_title('Medias de Recuerdo por Condición\n(Barras: Media ± 95% IC)', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#FF6B6B', alpha=0.7, label='Incidental'),
                       Patch(facecolor='#4ECDC4', alpha=0.7, label='Intencional')]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    out_path = Path(results_path) / 'plot_means_by_condition.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado: {out_path}")
    plt.close()


def plot_interaction(long, results_path='results'):
    """
    Plot interaction effect (lines for each group, x-axis = Processing)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    groups = sorted(long['Group'].unique())
    procs = ['S', 'A']
    
    colors = {'Incidental': '#FF6B6B', 'Intencional': '#4ECDC4'}
    markers = {'Incidental': 'o', 'Intencional': 's'}
    
    for g in groups:
        means = []
        for p in procs:
            data = long.loc[(long['Group'] == g) & (long['Processing'] == p), 'Score']
            data = data.dropna()
            means.append(data.mean())
        
        ax.plot([0, 1], means, marker=markers[g], markersize=12, linewidth=2.5,
                label=g, color=colors[g], alpha=0.8)
    
    ax.set_xlabel('Nivel de Procesamiento', fontsize=12, fontweight='bold')
    ax.set_ylabel('% Recuerdo', fontsize=12, fontweight='bold')
    ax.set_title('Gráfico de Interacción\n(Grupo × Procesamiento)', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Superficial (S)', 'Profundo (A)'])
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='best')
    
    plt.tight_layout()
    out_path = Path(results_path) / 'plot_interaction.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado: {out_path}")
    plt.close()


def plot_distributions(long, results_path='results'):
    """
    Plot distributions (violin plots) by group and processing
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create violin plot
    sns.violinplot(data=long, x='Group', y='Score', hue='Processing',
                   ax=ax, palette={'S': '#FFB3BA', 'A': '#BAE1FF'},
                   inner='box', cut=0)
    
    ax.set_xlabel('Grupo', fontsize=12, fontweight='bold')
    ax.set_ylabel('% Recuerdo', fontsize=12, fontweight='bold')
    ax.set_title('Distribuciones de Recuerdo por Grupo y Procesamiento\n(Violin Plots)', 
                 fontsize=14, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.legend(title='Procesamiento', fontsize=10, title_fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    out_path = Path(results_path) / 'plot_distributions.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado: {out_path}")
    plt.close()


def plot_boxplots(long, results_path='results'):
    """
    Plot boxplots (caja y bigotes) for each condition
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    groups = sorted(long['Group'].unique())
    colors = {'S': '#FFB3BA', 'A': '#BAE1FF'}
    
    for idx, g in enumerate(groups):
        data = long.loc[long['Group'] == g]
        
        # Box plot by processing
        sns.boxplot(data=data, x='Processing', y='Score', hue='Processing', ax=axes[idx],
                   palette=colors, width=0.6, legend=False)
        sns.stripplot(data=data, x='Processing', y='Score', ax=axes[idx],
                     color='black', alpha=0.4, size=8, jitter=True)
        
        axes[idx].set_xlabel('Nivel de Procesamiento', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('% Recuerdo', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'Grupo: {g}', fontsize=12, fontweight='bold')
        # Set tick labels only after ensuring they match current tick positions
        proc_labels = sorted(data['Processing'].unique())
        if len(proc_labels) == 2:
            axes[idx].set_xticklabels(['Superficial (S)', 'Profundo (A)'])
        axes[idx].set_ylim(0, 100)
        axes[idx].grid(axis='y', alpha=0.3)
    
    plt.suptitle('Diagramas de Caja por Grupo\n(Mediana, cuartiles y datos individuales)',
                 fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    out_path = Path(results_path) / 'plot_boxplot.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado: {out_path}")
    plt.close()


def plot_paired_comparison(df, results_path='results'):
    """
    Plot paired comparison: S vs A for each participant
    """
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Sort by group for better visualization
    df = df.sort_values(['Group', 'Perc_S'])
    
    x = np.arange(len(df))
    width = 0.35
    
    colors = {'Incidental': '#FF6B6B', 'Intencional': '#4ECDC4'}
    group_colors = [colors[g] for g in df['Group']]
    
    # Plot S and A scores
    bars1 = ax.bar(x - width/2, df['Perc_S'], width, label='Superficial (S)',
                   alpha=0.7, edgecolor='black', linewidth=1)
    bars2 = ax.bar(x + width/2, df['Perc_A'], width, label='Profundo (A)',
                   alpha=0.7, edgecolor='black', linewidth=1)
    
    # Color bars by group
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        group_color = group_colors[i]
        bar1.set_facecolor(group_color)
        bar2.set_facecolor(group_color)
    
    ax.set_xlabel('Participante', fontsize=12, fontweight='bold')
    ax.set_ylabel('% Recuerdo', fontsize=12, fontweight='bold')
    ax.set_title('Comparación Pareada: Procesamiento Superficial vs Profundo\n(Por Participante)',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(df['Participant'].str.replace('datos_parcipiante_N ', 'P').str.replace('.csv', ''),
                       rotation=45, ha='right')
    ax.set_ylim(0, 100)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    # Add group legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#FF6B6B', alpha=0.7, label='Incidental'),
                       Patch(facecolor='#4ECDC4', alpha=0.7, label='Intencional')]
    ax.legend(handles=legend_elements + [Line2D([0], [0], label='Superficial (S)', 
                                                     color='black', linewidth=8, alpha=0.7),
                                         Line2D([0], [0], label='Profundo (A)',
                                                    color='black', linewidth=8, alpha=0.4)],
             fontsize=10, loc='upper left', ncol=2)
    
    plt.tight_layout()
    out_path = Path(results_path) / 'plot_paired_comparison.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado: {out_path}")
    plt.close()


def generate_all_plots(table1_path='results/table1.csv', results_path='results'):
    """Generate all plots"""
    data = load_data(table1_path)
    if data is None:
        return 1
    
    df, long = data
    
    print("\nGenerando gráficos...")
    plot_means_by_condition(long, results_path)
    plot_interaction(long, results_path)
    plot_distributions(long, results_path)
    plot_boxplots(long, results_path)
    plot_paired_comparison(df, results_path)
    
    print("\n[OK] Todos los gráficos han sido generados exitosamente.")
    return 0


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Genera gráficos estadísticos del análisis')
    parser.add_argument('--table', default='results/table1.csv', 
                       help='Ruta a table1.csv (default: results/table1.csv)')
    parser.add_argument('--out', default='results',
                       help='Carpeta de salida (default: results)')
    args = parser.parse_args()
    
    rc = generate_all_plots(table1_path=args.table, results_path=args.out)
    sys.exit(rc)
