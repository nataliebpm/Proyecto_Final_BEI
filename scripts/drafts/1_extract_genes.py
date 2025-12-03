"title:  Borrador de script para extraer genes de un archivo de datos genómicos usando argparse y pandas"
"author: Natalie B. Pineda Morán"
"date: 1 diciembre 2025"


#!/usr/bin/env python3
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


# Cargar GFF
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
            ],
            dtype={"seqid": str, "coord_start": int, "coord_end": int, "strand": str}
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró archivo GFF: {ruta_gff}")

    return df_gff


# Reverse complement (asegúrate de que esta función esté definida antes de usarse)
def reverse_complement(seq):
    comp = str.maketrans("ACGTacgt", "TGCAtgca")
    return seq.translate(comp)[::-1]


# Argparse con min-length añadido
def load_parser():
    parser = argparse.ArgumentParser(description="Extractor de genes desde archivo GFF + FASTA.")
    parser.add_argument("--gff", type=str, required=True, help="Ruta del archivo GFF.")
    parser.add_argument("--fasta", type=str, required=True, help="Ruta del archivo FASTA.")
    parser.add_argument("--output", type=str, required=True, help="Ruta del archivo de salida.")
    parser.add_argument("--min-length", type=int, default=0,
                        help="Longitud mínima del gen para ser exportado (bases).")
    return parser.parse_args()


# Extraer genes con filtro de longitud
def extract_genes_seqs(df_fasta, df_gff, min_length=0):
    gene_seqs = {}

    # filtrar solo features tipo 'gene' (ajusta si en tu GFF usa otra palabra)
    genes_df = df_gff[df_gff["feature_type"] == "gene"]

    for gene in genes_df.itertuples(index=False):
        seq_id = gene.seqid
        coord_start = int(gene.coord_start)
        coord_end = int(gene.coord_end)
        strand = gene.strand

        # longitud correcta: coord_end - coord_start + 1
        gene_length = coord_end - coord_start + 1

        if gene_length < min_length:
            continue  # descartar gen corto

        # Python slicing: start index = coord_start - 1, end index = coord_end (exclusivo)
        start_idx = coord_start - 1
        end_idx = coord_end

        if seq_id in df_fasta:
            sequence = df_fasta[seq_id][start_idx:end_idx]

            if strand == "-":
                sequence = reverse_complement(sequence)

            # usar un header seguro: puedes cambiar attributes por ID extraído si quieres
            header = gene.attributes if gene.attributes and isinstance(gene.attributes, str) else seq_id
            gene_seqs[header] = {
                "coords": f"{coord_start}-{coord_end}",
                "strand": strand,
                "length": gene_length,
                "seq": sequence
            }
        else:
            # opcional: advertencia si seqid no está en FASTA (no levanta excepción)
            # print(f"Warning: seqid {seq_id} not found in FASTA, skipping.", file=sys.stderr)
            continue

    return gene_seqs


##############################################################################################################
# Main

if __name__ == "__main__":
    args = load_parser()

    # Cargar archivos
    df_gff = load_gff(args.gff)
    df_fasta = fasta_conversion(args.fasta)

    # Asegurarse de pasar args.min_length al llamar
    gene_seqs = extract_genes_seqs(df_fasta, df_gff, args.min_length)

    # Escribir salida
    with open(args.output, "w") as out:
        for attr, info in gene_seqs.items():
            out.write(f">{attr} coords={info['coords']} strand={info['strand']} length={info['length']}\n")
            out.write(info["seq"] + "\n")

    print("Extracción completada.")
