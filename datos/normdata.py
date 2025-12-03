import pandas as pd
import unicodedata
import os
import re

# Palabras válidas
VALID_WORDS = [
    "HUESO","MIEL","RINOCERONTE","CAMA","TORNADO","SOL","TANQUE","VINO",
    "MOSCA","LENTEJAS","FRIO","ELEFANTE","CHOCOLATE","PAZ","PRECIPICIO",
    "BIKINI","MAR","COCODRILO","BUITRE","IGLESIA","VOLCAN","AVISPA","FLOR",
    "ZAPATO","DELFIN","ENSALADA","TERREMOTO","GUSANO","FRESA","DESIERTO"
]

# Archivos concretos (mismo directorio donde ejecutes el script)
INPUT_FILES = [
    "datos/datos_participante_N (1).csv",
    "datos/datos_participante_N (2).csv",
    "datos/datos_participante_N (3).csv",
    "datos/datos_participante_N (4).csv",
    "datos/datos_participante_N (5).csv",
    "datos/datos_participante_N (6).csv",
]

def normalize_text(text: str) -> str:
    """Quita tildes y pasa a mayúsculas."""
    if not isinstance(text, str):
        text = str(text)
    text = text.strip().upper()
    # Eliminar acentos y otros diacríticos
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text

def match_word(word: str) -> str:
    """
    Dada una palabra (posiblemente corrupta), devuelve
    la palabra canónica más cercana de VALID_WORDS.
    """
    from difflib import get_close_matches

    w = normalize_text(word)

    # Si está vacía, devolvemos vacío
    if w == "":
        return ""

    # Si ya es una palabra válida, devolver tal cual
    if w in VALID_WORDS:
        return w

    # A veces aparece como subcadena o con caracteres raros alrededor
    for valid in VALID_WORDS:
        if valid in w or w in valid:
            return valid

    # Si no, usar coincidencia aproximada
    match = get_close_matches(w, VALID_WORDS, n=1, cutoff=0.6)
    return match[0] if match else w  # no se añaden palabras, solo se transforma esa

def normalize_recall_string(s: str, sep: str = " ") -> str:
    """
    Toma el contenido de una celda de 'recall' que puede tener
    varias palabras separadas por espacios, saltos de línea, comas, etc.,
    normaliza cada palabra y las une de nuevo con un separador homogéneo.

    Muy importante: no se añaden ni se borran palabras, solo se transforman.
    """
    if not isinstance(s, str):
        s = str(s)

    # Normalizamos saltos de línea a espacios para empezar
    s = s.replace("\r", " ").replace("\n", " ")

    # Separar por espacios, comas, punto y coma, tabuladores, etc.
    # (cualquier secuencia de espacios o , ; \t)
    raw_tokens = re.split(r"[\s,;]+", s)

    tokens = [t for t in raw_tokens if t != ""]  # quitamos tokens vacíos

    normalized_tokens = [match_word(tok) for tok in tokens]

    # Unificar separador: por defecto, un espacio
    return sep.join(normalized_tokens)

def find_recall_column(columns):
    """Busca la columna 'recall' aunque la escritura no sea exacta."""
    for c in columns:
        if "recall" in c.lower():
            return c
    return None

def process_file(file_path: str, output_dir: str, sep_recall: str = " "):
    print(f"Procesando: {file_path}")
    # Intentar inferir el separador automáticamente
    try:
        df = pd.read_csv(file_path, sep=None, engine="python")
    except Exception:
        # fallback: separar por cualquier espacio
        df = pd.read_csv(file_path, delimiter=r"\s+", engine="python")

    recall_col = find_recall_column(df.columns)
    if recall_col is None:
        print(f"  ⚠ No se encontró columna tipo 'recall' en {file_path}. Se omite.")
        return None

    # Renombramos la columna encontrada a 'recall' para ser consistentes
    if recall_col != "recall":
        df.rename(columns={recall_col: "recall"}, inplace=True)

    # Normalizar SOLO la columna recall, celda completa (todas las palabras)
    df["recall"] = df["recall"].apply(lambda x: normalize_recall_string(x, sep=sep_recall))

    # Guardar versión normalizada de este archivo
    base_name = os.path.basename(file_path)
    out_path = os.path.join(output_dir, base_name.replace(".csv", "_normalizado.csv"))
    df.to_csv(out_path, index=False)
    print(f"  ✅ Guardado: {out_path}")

    return df

def main():
    output_dir = "normalizados"
    os.makedirs(output_dir, exist_ok=True)

    all_dfs = []

    # separador homogéneo dentro de la columna recall (puedes cambiarlo por "," si prefieres)
    sep_recall = " "

    for f in INPUT_FILES:
        if not os.path.exists(f):
            print(f"⚠ Archivo no encontrado: {f} (se omite)")
            continue
        df = process_file(f, output_dir, sep_recall=sep_recall)
        if df is not None:
            all_dfs.append(df)

    if all_dfs:
        combinado = pd.concat(all_dfs, ignore_index=True)
        combinado.to_csv("recall_unificado.csv", index=False)
        print("✅ Archivo unificado guardado como 'recall_unificado.csv'")
    else:
        print("⚠ No se procesó ningún archivo.")

if __name__ == "__main__":
    main()
