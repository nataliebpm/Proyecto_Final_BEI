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
        dict_feature_type = len(df_gff[df_gff["feature_type"] == feature_type].value_counts())
    return dict_feature_type

#Función para obtener el promedio de longitud de las features según tipo de Feature
def average_length_by_type(df_gff, dict_feature_type):
    df_gff = df_gff.copy()
    df_gff.copy["length"] = df_gff["coord_end"] - df_gff["coord_start"] + 1
    avg_lengths = df_gff.groupby("feature_type")["length"].mean().to_dict()
    return avg_lengths

#Función para obtener la clasificación de las Features según el strand
def strand_classification(df_gff, dict_feature_type):
    # Agrupar por feature_type y strand
    strand_counts = df_gff.groupby(["feature_type", "strand"]).size().unstack(fill_value=0)

    # Crear diccionario final
    strand_classification = {}
    for feature_type in dict_feature_type.keys():
        if feature_type in strand_counts.index:
            strand_classification[feature_type] = strand_counts.loc[feature_type].to_dict()
        else:
            strand_classification[feature_type] = {"+": 0, "-": 0} 
    return strand_classification




##############################################################################################################
# ------------------------------------------------ Main ------------------------------------------------

if __name__ == "__main__":
    parser = load_parser()
    args = parser.parse_args()

    df_gff = load_gff(args.gff)

    counts = count_features_by_type(df_gff)

    avg_lengths = average_length_by_type(df_gff)

    strand_stats = strand_classification(df_gff, counts)

    stats = {}
    for feature_type in counts:
        stats[feature_type] = {
            "count": counts[feature_type],
            "average_length": avg_lengths.get(feature_type, 0),
            "strand": strand_stats.get(feature_type, {})
        }

    with open(args.output, "w") as out:
        out.write("Feature_type\tCount\tAverage_length\tStrand+\tStrand-\n")
        for feature, info in stats.items():
            strand_plus = info["strand"].get("+", 0)
            strand_minus = info["strand"].get("-", 0)
            out.write(f"{feature}\t{info['count']}\t{info['average_length']:.2f}\t{strand_plus}\t{strand_minus}\n")

    print("Cálculo completado. Resultados guardados en", args.output)

