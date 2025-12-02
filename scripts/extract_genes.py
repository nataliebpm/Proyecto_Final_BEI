
# Script para extraer genes de un archivo de datos genómicos usando argparse y pandas

import argparse
import pandas as pd

# 1. Creamos el parser de argumentos
parser = argparse.ArgumentParser(description="Extract genes from a genomic data file.")

# 2. Definimos los tipos de argumentos. 
parser.add_argument("input_file", type=str, help="Path to the input genomic data file.") #Argumento obligatorio. 
parser.add_argument("output_file", type = str, help="Path to the output file where extracted genes will be saved.") #Argumento obligatorio

# 3. Procesar los argumentos dados por el usuario
args = parser.parse_args()

# 4. Usar el argumento


##########################################################################################################################

#Creación de funciones: 

# Función para cargar el archivo fasta

load_fasta()


# Función de parse para el archivo gff
load_parser()

# Función para extraer secuencias de genes
extract_genes_seqs()