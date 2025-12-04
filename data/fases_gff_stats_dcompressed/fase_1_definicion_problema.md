# Fase 1: Definición del problema y requisitos

## Objetivo
Entender las estadísticas que se desean generar a partir de un archivo GFF.

## Entrada
- Archivo GFF (`.gff`).

## Salida esperada
Archivo JSON con:
- Total de features.
- Conteo por tipo de feature.
- Longitud promedio por tipo.
- Distribución de strand (`+` y `-`).

## Acciones
- Revisar formato GFF3.
- Identificar columnas de interés: `type`, `start`, `end`, `strand`.
- Definir métricas y estadísticas requeridas.
- Identificar argumentos opcionales (`--filter-type`).

## Consideraciones
- Ignorar líneas comentadas (`#`).
- Definir supuestos sobre los datos (p.ej., start < end, strands válidos).
- Planificar para extensibilidad futura (otros formatos GFF/GTF).
