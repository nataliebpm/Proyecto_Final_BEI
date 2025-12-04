# ---------------------------------- Metadatos ------------------------------------------

"title:  Script para extraer genes de un archivo de datos genómicos usando argparse y pandas"
"author: Natalie B. Pineda Morán"
"date: 03 diciembre 2025"

# -------------------------------------Librerías-----------------------------------------
import pandas as pd
import argparse
import json  # agregado para generar JSON


# -------------------------------------- Funciones --------------------------------------

# Cargar archivo GFF en un DataFrame de pandas
def load_gff(ruta_gff):
    try:
        # Cambié sep="\s+" con engine="python" para manejar espacios o tabs
        df_gff = pd.read_csv(
            ruta_gff,
            sep="\s+",
            engine="python",
            comment="#",
            header=None,
            names=[
                "seqid", "source", "feature_type", "coord_start", "coord_end",
                "score", "strand", "phase", "attributes"
            ]
        )
        # Convertir coordenadas a numéricas
        df_gff["coord_start"] = pd.to_numeric(df_gff["coord_start"], errors="coerce")
        df_gff["coord_end"] = pd.to_numeric(df_gff["coord_end"], errors="coerce")
        df_gff = df_gff.dropna(subset=["coord_start", "coord_end"])
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró archivo GFF: {ruta_gff}")
    return df_gff

# Configuración del parser de argumentos
def load_parser():
    parser = argparse.ArgumentParser(description="Cálculo de estadísticas básicas de un archivo GFF.")
    parser.add_argument("gff", type=str, help="Ruta del archivo GFF.")
    parser.add_argument("output", type=str, help="Ruta del archivo de salida.")
    parser.add_argument("--filter_type", type=str, help="Indica para cuáles Features quieres calcular estadísticas.")
    return parser

# Funciones para calcular estadísticas
def count_features_by_type(df_gff):
    dict_feature_type = {}
    for feature_type in df_gff["feature_type"].unique():
        dict_feature_type[feature_type] = len(df_gff[df_gff["feature_type"] == feature_type])
    return dict_feature_type

# Calcular la longitud promedio por tipo de feature
def average_length_by_type(df_gff):
    df_gff = df_gff.copy()
    df_gff["length"] = df_gff["coord_end"] - df_gff["coord_start"] + 1
    avg_lengths = df_gff.groupby("feature_type")["length"].mean().to_dict()
    return avg_lengths

# Clasificación por hebra
def strand_classification(df_gff):
    df_gff = df_gff[df_gff["strand"].isin(["+", "-"])]
    strand_counts = df_gff["strand"].value_counts().to_dict()
    return strand_counts


# -------------------------------------- Main ------------------------------------------------

if __name__ == "__main__":
    parser = load_parser()
    args = parser.parse_args()

    df_gff = load_gff(args.gff)

    if args.filter_type:
        df_gff = df_gff[df_gff["feature_type"] == args.filter_type]

    counts = count_features_by_type(df_gff)
    avg_lengths = average_length_by_type(df_gff)
    strand_stats = strand_classification(df_gff)

    # Crear diccionario final en formato JSON
    stats = {
        "total_features": len(df_gff),
        "by_type": counts,
        "avg_length": {k: round(v, 2) for k, v in avg_lengths.items()},
        "strand_distribution": strand_stats
    }

    # Guardar JSON
    with open(args.output, "w") as out_file:
        json.dump(stats, out_file, indent=4)

    print("Cálculo completado. Resultados guardados en", args.output)
