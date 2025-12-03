
"title:  Borrador de script para extraer genes de un archivo de datos genómicos usando argparse y pandas"
"author: Natalie B. Pineda Morán"
"date: 1 diciembre 2025"

import pandas as pd
import argparse

##############################################################################################################
# ------------------------------ Funciones ------------------------------

# Cargar el archivo fasta
def fasta_conversion(ruta_fasta):
    sequences = {}
    seq_id = None
    seq_chunks = []

    try:
        with open(ruta_fasta, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.startswith(">"):
                    if seq_id is not None:
                        sequences[seq_id] = "".join(seq_chunks)

                    seq_id = line[1:].split()[0]
                    seq_chunks = []
                else:
                    if seq_id is None:
                        raise ValueError("Se encontró secuencia antes de encabezado.")
                    seq_chunks.append(line)

        # guardar última secuencia
        if seq_id is not None:
            sequences[seq_id] = "".join(seq_chunks)

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró archivo FASTA: {ruta_fasta}")

    return sequences


# Función para cargar archivo GFF como DataFrame
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


# Función reverse complement (no estaba en tu código)
def reverse_complement(seq):
    comp = str.maketrans("ACGTacgt", "TGCAtgca")
    return seq.translate(comp)[::-1]


# Función de argparse corregida
def load_parser():
    parser = argparse.ArgumentParser(description="Extractor de genes desde archivo GFF + FASTA.")
    parser.add_argument("--gff", type=str, required=True, help="Ruta del archivo GFF.")
    parser.add_argument("--fasta", type=str, required=True, help="Ruta del archivo FASTA.")
    parser.add_argument("--output", type=str, required=True, help="Ruta del archivo de salida.")
    return parser.parse_args()


# Función para extraer secuencias de genes
def extract_genes_seqs(df_fasta, df_gff):
    gene_seqs = {}

    for gene in df_gff[df_gff["feature_type"] == "gene"].itertuples():
        seq_id = gene.seqid
        start = gene.coord_start - 1
        end = gene.coord_end
        strand = gene.strand

        if seq_id in df_fasta:
            sequence = df_fasta[seq_id][start:end]

            if strand == "-":
                sequence = reverse_complement(sequence)

            gene_seqs[gene.attributes] = {
                "coords": f"{start+1}-{end}",
                "strand": strand,
                "seq": sequence
            }

    return gene_seqs


##############################################################################################################
# Main (estructura respetada)

if __name__ == "__main__":
    args = load_parser()

    # cargar archivos usando tus funciones
    df_gff = load_gff(args.gff, args.fasta)
    df_fasta = fasta_conversion(args.fasta)

    # extraer genes
    gene_seqs = extract_genes_seqs(df_fasta, df_gff)

    # escribir archivo de salida
    with open(args.output, "w") as out:
        for attr, info in gene_seqs.items():
            out.write(f">{attr} gene_coords={info['coords']} strand={info['strand']}\n")
            out.write(info["seq"] + "\n")

    print("Extracción completada.")
