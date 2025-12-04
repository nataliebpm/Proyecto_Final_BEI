# Fase 3: Implementación modular

## Objetivo
Escribir código limpio, legible y reutilizable para procesar archivos GFF y generar estadísticas.

## Funciones sugeridas
- `parse_gff(file_path, filter_type=None)`  
  - Lee el archivo GFF y devuelve una lista de features filtradas según el tipo (si se aplica).
- `calculate_stats(features)`  
  - Calcula estadísticas: total de features, conteo por tipo, longitud promedio, distribución de strands.
- `save_json(stats, output_file)`  
  - Guarda el diccionario de estadísticas en un archivo JSON.

## Buenas prácticas
- Uso de `argparse` para manejar argumentos de línea de comandos:
  - `--gff` → ruta del archivo GFF.
  - `--out` → archivo JSON de salida.
  - `--filter-type` → tipo de feature opcional.
- Validación de entradas:
  - Archivo existente.
  - Columnas correctas en el GFF.
  - Tipo válido si se aplica filtrado.
- Docstrings claros para cada función.
- Código modular y comentado para facilitar mantenimiento.
- Manejo de errores:
  - Archivo no encontrado.
  - Formato de línea incorrecto.
  - Tipo no encontrado al aplicar filtrado.
