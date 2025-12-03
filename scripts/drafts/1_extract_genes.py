"title:  Borrador de script para extraer genes de un archivo de datos genómicos usando argparse y pandas"
"author: Natalie B. Pineda Morán"
"date: 1 diciembre 2025"



import pandas as pd
import argparse

############################################################################################################################################################
#Creación de funciones: 

#Función para cargar el archivo fasta y gff

ruta_fasta = str(input("Ruta del archivo FASTA: "))
ruta_gff = str(input("Ruta del archivo GFF: "))

# Función para cargar los archivos
def load_files(ruta_gff, ruta_fasta):
    df_gff = pd.read_csv(ruta_gff,
        sep="\t",                # Separador tabulado
        comment="#",             # Ignorar líneas que comienzan con #
        header=None,             # No hay cabecera en el archivo
        names=["seqid", "source", "feature_type", "coord_start", "coord_end", "score", "strand", "phase", "attributes"]
    )
    return(df_gff)

#Función para convertir archivo fasta a diccionario. 
def fasta_conversion(ruta_fasta):
    sequences = {}
    seq_id = None
    seq_chunks = []  # usar lista para eficiencia

    try:
        with open(ruta_fasta, 'r') as file:
            for line in file:
                line = line.strip()

                # Saltar líneas vacías
                if not line:
                    continue

                # Si es encabezado
                if line.startswith(">"):
                    # Guardar secuencia previa si existe
                    if seq_id is not None:
                        sequences[seq_id] = "".join(seq_chunks)

                    # Extraer solo el identificador hasta el primer espacio
                    seq_id = line[1:].split()[0]

                    seq_chunks = []  # reiniciar lista
                else:
                    # Validar que hay un encabezado antes de secuencias
                    if seq_id is None:
                        raise ValueError(
                            f"Se encontró una secuencia antes de cualquier encabezado")
    return sequences
df_fasta = pd.DataFrame{sequences}

# Función de parse para el archivo gff
def load_parser():
    # 1. Creamos el parser de argumentos
    parser = argparse.ArgumentParser(description="Extract genes from a genomic data file.")

    # 2. Definimos los tipos de argumentos. 
    parser.add_argument("path_input_file", type=str, help="Path to the input FASTA and GFF files.") #Argumento obligatorio. 
    parser.add_argument("path_output_file", type = str, help="Path to the output file where extracted genes will be saved.") #Argumento obligatorio

    # 3. Procesar los argumentos dados por el usuario
    args = parser.parse_args()

    # 4. Usar el argumento

# Función para extraer secuencias de genes

def extract_genes_seqs(df_fasta, df_gff): 
    gene_seqs = {}
    for gene in df_gff[df_gff['feature_type'] == 'gene'].itertuples():
        seq_id = gene.seqid
        start = gene.coord_start - 1  # Ajustar a índice 0
        end = gene.coord_end
        strand = gene.strand

        if seq_id in df_fasta:
            sequence = df_fasta[seq_id][start:end]
            if strand == '-':
                sequence = reverse_complement(sequence)
            gene_seqs[gene.attributes] = sequence
    return gene_seqs
df_gene_seqs = pd.DataFrame{gene_seqs}