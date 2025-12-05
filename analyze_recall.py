#!/usr/bin/env python3
"""
analyze_recall.py

Lee los CSV exportados por la versión web del experimento (carpeta `datos/`),
calcula para cada participante el porcentaje (%) de palabras recordadas
correctamente por tipo de procesamiento (cue 'S' y 'A'), guarda la Tabla 1 en
`results/table1.csv` y realiza el ANOVA 2x2 (Grupo x Procesamiento). El script
intenta usar `pingouin` para el ANOVA mixto; si no está disponible usará
`statsmodels` como alternativa y reportará un ajuste de efectos mixtos.

Salida:
- `results/table1.csv` : tabla resumen por participante
- `results/analysis_results.txt` : resumen de los análisis estadísticos

Dependencias recomendadas: pandas, numpy, scipy, statsmodels, pingouin (opcional).
Instalación rápida: `pip install pandas numpy scipy statsmodels pingouin`
"""

from pathlib import Path
import re
import unicodedata
import sys
import warnings

import numpy as np
import pandas as pd

from scipy import stats

try:
    import pingouin as pg
    HAS_PINGOUIN = True
except Exception:
    pg = None  # type: ignore
    HAS_PINGOUIN = False

try:
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
except Exception:
    sm = None
    smf = None

# suppress a known scipy runtime warning about catastrophic cancellation when
# datasets are nearly identical (this happened with very small n in some runs)
warnings.filterwarnings("ignore", category=RuntimeWarning, message=r"Precision loss occurred in moment calculation due to catastrophic cancellation.*")


def normalize_text(s):
    """Lowercase, remove diacritics, remove punctuation except spaces, collapse spaces."""
    if s is None:
        return ""
    s = str(s)
    s = s.lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    # keep letters, numbers and spaces
    s = re.sub(r"[^0-9a-z\s]", ' ', s)
    s = re.sub(r"\s+", ' ', s).strip()
    return s


def tokenize(s):
    s2 = normalize_text(s)
    if s2 == '':
        return []
    return s2.split(' ')


def analyze_folder(datos_path='datos/normalized', results_path='results'):
    datos = Path(datos_path)
    results = Path(results_path)
    results.mkdir(parents=True, exist_ok=True)

    files = sorted(datos.glob('*.csv'))
    if not files:
        print(f"No se encontraron CSVs en {datos.resolve()}")
        return 1

    rows = []

    for f in files:
        try:
            df = pd.read_csv(f, encoding='utf-8', dtype=str)
        except Exception:
            df = pd.read_csv(f, encoding='latin-1', dtype=str)

        if df.empty:
            print(f"Archivo vacío: {f}")
            continue

        # extract participant id from filename
        pid = f.stem

        # expected columns: group,list,edad,sexo,estudios,word,cue,response,recall
        # metadata usually repeated in every row; take first occurrence
        first = df.iloc[0].to_dict()
        group = first.get('group') or first.get('Group') or 'Unknown'
        list_version = first.get('list') or first.get('List') or ''
        edad = first.get('edad') or first.get('edad') or ''
        sexo = first.get('sexo') or ''

        # presented words and cues
        if 'word' not in df.columns or 'cue' not in df.columns:
            print(f"Archivo {f} no contiene las columnas esperadas 'word'/'cue'. Skipping.")
            continue

        # get unique presented words for each cue
        s_words = df.loc[df['cue'] == 'S', 'word'].dropna().unique().tolist()
        a_words = df.loc[df['cue'] == 'A', 'word'].dropna().unique().tolist()

        recall_text = first.get('recall', '')

        tokens = set(tokenize(recall_text))

        # match words: normalize each presented word and check if appears among tokens
        def count_recalled(word_list):
            if not word_list:
                return 0, 0
            total = len(word_list)
            matched = 0
            for w in word_list:
                wnorm = normalize_text(w)
                # Some presented words can be multi-word; check any token equals or token sequence present
                # We'll check exact token match first; also check if full normalized word is substring of recall_text
                if wnorm in tokens:
                    matched += 1
                else:
                    # fallback: check substring in normalized recall text
                    if wnorm and wnorm in normalize_text(recall_text):
                        matched += 1
            return matched, total

        s_matched, s_total = count_recalled(s_words)
        a_matched, a_total = count_recalled(a_words)

        perc_s = (s_matched / s_total * 100) if s_total > 0 else float('nan')
        perc_a = (a_matched / a_total * 100) if a_total > 0 else float('nan')

        rows.append({
            'Participant': pid,
            'Group': group,
            'List': list_version,
            'Edad': edad,
            'Sexo': sexo,
            'S_matched': s_matched,
            'S_total': s_total,
            'A_matched': a_matched,
            'A_total': a_total,
            'Perc_S': perc_s,
            'Perc_A': perc_a,
        })

    dfp = pd.DataFrame(rows)

    if dfp.empty:
        print("No se pudieron procesar participantes.")
        return 1

    # Sort by Group so Intencional and Incidental are grouped together
    dfp = dfp.sort_values('Group').reset_index(drop=True)
    
    # Save Table 1 with group separation (comments for readability)
    table1_path = results / 'table1.csv'
    with open(table1_path, 'w', encoding='utf-8', newline='') as fh:
        # Write header
        fh.write(','.join(dfp.columns) + '\n')
        # Write rows grouped by condition with section markers
        for group in sorted(dfp['Group'].unique()):
            fh.write(f'\n# --- Grupo: {group} ---\n')
            group_data = dfp[dfp['Group'] == group]
            for _, row in group_data.iterrows():
                fh.write(','.join(str(v) for v in row.values) + '\n')
            # Add summary row: mean Perc_S and Perc_A for this group
            try:
                mean_s = float(group_data['Perc_S'].astype(float).mean())
            except Exception:
                mean_s = ''
            try:
                mean_a = float(group_data['Perc_A'].astype(float).mean())
            except Exception:
                mean_a = ''
            summary_values = [f'Group_Mean_{group}', group, '', '', '', '', '', '', '', f'{mean_s}', f'{mean_a}']
            fh.write(','.join(str(v) for v in summary_values) + '\n')
    
    print(f"Tabla 1 guardada en: {table1_path}")
    print(f"  - Total participantes procesados: {len(dfp)}")
    for group in sorted(dfp['Group'].unique()):
        count = len(dfp[dfp['Group'] == group])
        print(f"    {group}: {count} participantes")

    # build long format for ANOVA: one row per participant x processing
    # Ensure scores are interleaved per participant: [Perc_S_p1, Perc_A_p1, Perc_S_p2, Perc_A_p2, ...]
    participants_rep = np.repeat(dfp['Participant'].to_numpy(), 2)
    groups_rep = np.repeat(dfp['Group'].to_numpy(), 2)
    processing_seq = ['S', 'A'] * len(dfp)
    # interleave Perc_S and Perc_A so each participant has S then A
    scores_interleaved = np.column_stack((dfp['Perc_S'].to_numpy(), dfp['Perc_A'].to_numpy())).ravel()
    long = pd.DataFrame({
        'Participant': participants_rep,
        'Group': groups_rep,
        'Processing': processing_seq,
        'Score': scores_interleaved
    })

    # remove rows with nan scores (if some participants missing a condition)
    long = long.dropna(subset=['Score'])

    # convert types
    long['Score'] = long['Score'].astype(float)

    out_lines = []
    out_lines.append('ANALYSIS SUMMARY')
    out_lines.append('================')
    out_lines.append(f'N participants: {dfp.shape[0]}')
    out_lines.append('')

    # descriptive stats and 95% CI for each condition
    def mean_ci(x, alpha=0.05):
        x = np.asarray(x)
        x = x[~np.isnan(x)]
        n = len(x)
        if n == 0:
            return (np.nan, np.nan, np.nan)
        m = x.mean()
        se = stats.sem(x, nan_policy='omit')
        df = n - 1
        tcrit = stats.t.ppf(1 - alpha/2, df) if df > 0 else np.nan
        ci_low = m - tcrit * se
        ci_high = m + tcrit * se
        return (m, ci_low, ci_high)

    group_levels = long['Group'].unique().tolist()
    proc_levels = ['S', 'A']

    out_lines.append('Descriptive stats (means and 95% CI)')
    for g in group_levels:
        for p in proc_levels:
            vals = long.loc[(long['Group'] == g) & (long['Processing'] == p), 'Score']
            m, lo, hi = mean_ci(vals)
            out_lines.append(f'{g} - {p}: mean={m:.2f}, 95% CI=[{lo:.2f}, {hi:.2f}], n={len(vals)}')
    out_lines.append('')

    # attempt mixed ANOVA with pingouin
    if HAS_PINGOUIN and pg is not None:
        out_lines.append('Mixed ANOVA using pingouin (Group between, Processing within)')
        try:
            aov = pg.mixed_anova(data=long, dv='Score', within='Processing', between='Group', subject='Participant')
            out_lines.append(aov.to_string())
        except Exception as e:
            out_lines.append('pingouin mixed_anova failed: ' + str(e))
    else:
        out_lines.append('pingouin not available; attempting statsmodels fallback (mixed effects)')
        if sm is None or smf is None:
            out_lines.append('statsmodels no disponible; no se puede realizar ANOVA. Instale pingouin o statsmodels.')
        else:
            # Fit mixed effects model with random intercept for Participant
            try:
                # encode categorical factors
                long['Group_c'] = long['Group'].astype('category')
                long['Processing_c'] = long['Processing'].astype('category')
                model = smf.mixedlm('Score ~ Group_c * Processing_c', data=long, groups=long['Participant'])
                res = model.fit(reml=False)
                out_lines.append('MixedLM fit summary:')
                out_lines.append(res.summary().as_text())
                # also provide ANOVA-like table from OLS for fixed effects (note: ignores within-subject correlation)
                ols = smf.ols('Score ~ C(Group) * C(Processing)', data=long).fit()
                anova_table = sm.stats.anova_lm(ols, typ=2)
                out_lines.append('\nOLS ANOVA (Type II, treats observations as independent):')
                out_lines.append(anova_table.to_string())
            except Exception as e:
                out_lines.append('statsmodels mixed/fallback failed: ' + str(e))

    out_lines.append('')
    # Paired t-test (within-subject S vs A) overall and per group, with CI for paired difference
    out_lines.append('Paired comparisons (S vs A) and 95% CI of the mean difference')

    def paired_diff_ci(x, y, alpha=0.05):
        x = np.asarray(x); y = np.asarray(y)
        mask = ~np.isnan(x) & ~np.isnan(y)
        x = x[mask]; y = y[mask]
        n = len(x)
        if n == 0:
            return (np.nan, np.nan, np.nan, np.nan)
        dif = x - y
        md = dif.mean()
        se = stats.sem(dif)
        df = n - 1
        tcrit = stats.t.ppf(1 - alpha/2, df)
        ci_low = md - tcrit * se
        ci_high = md + tcrit * se
        tstat, pval = stats.ttest_rel(x, y, nan_policy='omit')
        return (md, ci_low, ci_high, pval)

    # overall
    wide = dfp.set_index('Participant')
    x = wide['Perc_S'].astype(float)
    y = wide['Perc_A'].astype(float)
    md, lo, hi, pval = paired_diff_ci(x, y)
    out_lines.append(f'Overall S - A: mean_diff={md:.3f}, 95% CI=[{lo:.3f}, {hi:.3f}], p_paired={pval:.4f}')

    # per group
    for g in group_levels:
        sub = dfp.loc[dfp['Group'] == g]
        md, lo, hi, pval = paired_diff_ci(sub['Perc_S'].astype(float), sub['Perc_A'].astype(float))
        out_lines.append(f'{g} S - A: mean_diff={md:.3f}, 95% CI=[{lo:.3f}, {hi:.3f}], p_paired={pval:.4f}, n={len(sub)}')

    # save analysis results
    out_path = results / 'analysis_results.txt'
    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out_lines))

    print(f'Análisis guardado en: {out_path}')
    print('Resumen breve:')
    for l in out_lines[:20]:
        print(l)

    return 0


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(description='Analisis de recuerdo: genera tabla y ANOVA 2x2')
    p.add_argument('--datos', default='datos', help='Carpeta donde están los CSV (default: datos)')
    p.add_argument('--out', default='results', help='Carpeta para resultados (default: results)')
    args = p.parse_args()

    rc = analyze_folder(datos_path=args.datos, results_path=args.out)
    sys.exit(rc)
