# Fase 5: Documentación y reproducibilidad

## Objetivo
Facilitar que cualquier usuario pueda ejecutar, entender y reproducir los resultados del script `gff_stats.py`.

## Acciones
- Documentar el uso del script:
  ```bash
  python gff_stats.py --gff genes.gff --out report.json [--filter-type TYPE]
  ```
- Explicar la estructura del JSON de salida:
  ```json
  {
    "total_features": 512,
    "by_type": {"gene": 210, "CDS": 290},
    "avg_length": {"gene": 890.3, "CDS": 320.7},
    "strand_distribution": {"+": 61, "-": 39}
  }
  ```
- Agregar ejemplos de ejecución con y sin filtrado por tipo.
- Explicar supuestos sobre los datos:
  - Ignorar líneas comentadas.
  - Columna 3 = tipo, columna 4 = start, columna 5 = end, columna 7 = strand.
- Instrucciones para instalar dependencias:
  - Python >= 3.8.
  - Módulos estándar (`argparse`, `json`).

## Buenas prácticas
- README completo y claro.
- Explicación detallada de cada función y su propósito.
- Ejemplo de ejecución y salida esperada.
- Separación de documentación del código y de los datos de prueba.
- Mantener trazabilidad entre datos de entrada y resultados.
