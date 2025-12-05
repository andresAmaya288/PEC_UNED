#!/usr/bin/env python3
"""
Normalize recall fields in CSVs under datos/.
- Uppercases recall tokens
- Replaces commas and other separators with a homogeneous separator `;`
- Keeps only words that are in the allowed list (exact match after normalization)
- Writes output CSVs as `normalized_<original>.csv` in the same folder

Run:
  python scripts\normalize_recalls.py

The script is idempotent and can be re-run when new files are added.
"""
import csv
import os
import re
import sys
import unicodedata
import difflib

BASE = os.path.dirname(__file__)
DATOS_DIR = os.path.join(BASE, 'datos')
SEPARATOR = ';'
OUT_DIR = os.path.join(DATOS_DIR, 'normalized')

# use single space as homogeneous separator for readability
SEPARATOR = ' '

# Allowed words (exact uppercase tokens expected)
ALLOWED_WORDS = [
  "HUESO","MIEL","RINOCERONTE","CAMA","TORNADO","SOL","TANQUE","VINO",
  "MOSCA","LENTEJAS","FRIO","ELEFANTE","CHOCOLATE","PAZ","PRECIPICIO",
  "BIKINI","MAR","COCODRILO","BUITRE","IGLESIA","VOLCAN","AVISPA","FLOR",
  "ZAPATO","DELFIN","ENSALADA","TERREMOTO","GUSANO","FRESA","DESIERTO"
]
ALLOWED_SET = set(ALLOWED_WORDS)

# helpers
_non_letter_re = re.compile(r'[^A-ZÑ]')


def remove_accents(s: str) -> str:
    # normalize and remove combining marks
    nk = unicodedata.normalize('NFD', s)
    return ''.join(ch for ch in nk if not unicodedata.category(ch).startswith('M'))


def normalize_token(tok: str) -> str:
    tok = tok.strip()
    if not tok:
        return ''
    tok = remove_accents(tok)
    tok = tok.upper()
    # remove anything that is not A-Z or Ñ
    tok = _non_letter_re.sub('', tok)
    return tok


def split_recall_field(text: str):
    if text is None:
        return []
    # Replace common separators (commas, pipes, slashes) with our SEPARATOR
    # Also convert newlines to separator
    # But preserve words containing punctuation by cleaning later
    # First, unify separators
    unified = re.sub(r'[\r\n]+', SEPARATOR, text)
    unified = re.sub(r'[;,|/\\]+', SEPARATOR, unified)
    # Also replace multiple spaces around separators
    unified = re.sub(r'\s*' + re.escape(SEPARATOR) + r'\s*', SEPARATOR, unified)
    # If the field contains commas within quotes they are already part of the string
    parts = [p for p in unified.split(SEPARATOR) if p.strip()!='']
    return parts


def process_file(path: str):
    filename = os.path.basename(path)
    out_path = os.path.join(os.path.dirname(path), f'normalized_{filename}')
    # write normalized files into dedicated folder so originals remain untouched
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, filename)

    print(f'Processing {filename} -> {os.path.relpath(out_path)}')

    with open(path, 'r', encoding='utf-8', newline='') as f_in:
        # try to detect delimiter as comma by default
        reader = csv.DictReader(f_in)
        if 'recall' not in reader.fieldnames:
            print(f'  Warning: file {filename} has no "recall" column. Skipping.')
            return
        rows = list(reader)
        fieldnames = reader.fieldnames

    total_rows = len(rows)
    total_accepted = 0
    total_removed = 0
    total_fuzzy = 0
    total_kept_unmatched = 0

    # Process rows
    for row in rows:
        raw = row.get('recall', '')
        tokens = split_recall_field(raw)
        normalized = []
        for tok in tokens:
            n = normalize_token(tok)
            if not n:
                continue
            if n in ALLOWED_SET:
                normalized.append(n)
            else:
                # try fuzzy matching against allowed words
                match = None
                try:
                    candidates = difflib.get_close_matches(n, ALLOWED_WORDS, n=1, cutoff=0.75)
                    if candidates:
                        match = candidates[0]
                except Exception:
                    match = None

                if match:
                    normalized.append(match)
                    total_fuzzy += 1
                else:
                    # keep the normalized token as-is (user requested to keep unmatched tokens)
                    normalized.append(n)
                    total_kept_unmatched += 1

        total_accepted += len([t for t in normalized if t])
        # join using homogeneous separator
        row['recall'] = SEPARATOR.join(normalized)

    # write output
    with open(out_path, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f'  Rows: {total_rows}, tokens kept: {total_accepted}, fuzzy-replaced: {total_fuzzy}, kept-unmatched: {total_kept_unmatched}, previously-removed: {total_removed}')


def main():
    if not os.path.isdir(DATOS_DIR):
        print(f'Datos directory not found: {DATOS_DIR}')
        sys.exit(1)

    files = [os.path.join(DATOS_DIR, n) for n in os.listdir(DATOS_DIR) if n.lower().endswith('.csv')]
    if not files:
        print('No CSV files found in datos/ folder.')
        return

    for p in files:
        try:
            process_file(p)
        except Exception as e:
            print(f'Error processing {p}: {e}')

    print('Done.')


if __name__ == '__main__':
    main()
