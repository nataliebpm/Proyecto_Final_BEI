"title:  Borrador de script para extraer genes de un archivo de datos genómicos usando argparse y pandas"
"author: Natalie B. Pineda Morán"
"date: 03 diciembre 2025"

import pandas as pd
import argparse 
##############################################################################################################
# ------------------------------ Funciones ------------------------------

# Cargar GFF y convertirlo a DataFrame
def load_gff(ruta_gff):
    try:
        df_gff = pd.read_csv(
            ruta_gff,
            sep="\t",
            comment="#",
            header=None,
            names=[
                "seqid", "source", "feature_type", "coord_start", "coord_end",
                "score", "strand", "phase", "attributes"
            ]
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró archivo GFF: {ruta_gff}")

    return df_gff

#Configurar argparse
def load_parser():
    parser = argparse.ArgumentParser(description="Cálculo de estadísticas básicas de un archivo GFF.")
    parser.add_argument("gff", type = str, help="Ruta del archivo GFF.")
    parser.add_argument("output", type = str, help="Ruta del archivo de salida.")
    parser.add_argument("--filter_type", type = str, help="Indica para cuáles Features quieres calcular estadísticas.")
    return parser

#Función para contar las features según tipo de Feature
def count_features_by_type(df_gff):
    for feature_type in df_gff["feature_type"].unique():
        dict_feature_type = df_gff[df_gff["feature_type"] == feature_type].value_counts().to_dict()
    return dict_feature_type

#Función para obtener el promedio de longitud de las features según tipo de Feature
def average_length_by_type(df_gff, dict_feature_type):
    for feature_type in df_gff["feature_type"].unique():
        dict_feature_type["lengths"] = df_gff["coord_end"] - df_gff["coord_start"] + 1
        df_filtered = df_gff[df_gff["feature_type"] == feature_type]
        coords_length = df_filtered["coord_end"] - df_filtered["coord_start"] + 1
        average_length = df_gff.lengths.mean()
    return average_length



##############################################################################################################
# ------------------------------------------------ Main ------------------------------------------------

if __name__ == "__main__":
    args = load_parser().parse_args()

    df_gff = load_gff(args.gff)

    gene_seqs = count_features_by_type(df_gff, args.filter_type)

    with open(args.output, "w") as out:
        for attr, info in gene_seqs.items():
            out.write(f">{attr} coords={info['coords']} strand={info['strand']} length={info['length']}\n")
            out.write(info["seq"] + "\n")

    print("Extracción completada.")
