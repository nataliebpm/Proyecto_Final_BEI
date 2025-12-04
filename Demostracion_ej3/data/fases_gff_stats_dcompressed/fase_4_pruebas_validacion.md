# Fase 4: Pruebas y validación

## Objetivo
Verificar que las estadísticas generadas por `gff_stats.py` sean correctas y reproducibles.

## Acciones
1. Crear un archivo GFF de prueba pequeño con:
   - Varias líneas de diferentes tipos (`gene`, `CDS`, `mRNA`).
   - Diferentes strands (`+` y `-`).
   - Líneas comentadas (`#`) para verificar que se ignoren.
   
2. Escribir `asserts` para validar:
   - Total de features procesadas.
   - Conteo de features por tipo.
   - Longitud promedio por tipo.
   - Distribución de strands (`+` y `-`).
   
3. Probar filtrado por tipo (`--filter-type`) y validar resultados específicos.

## Documentación de pruebas
- Crear un archivo `tests.md` describiendo:
  - Cada prueba.
  - Datos de entrada.
  - Resultado esperado.
  
## Buenas prácticas
- Pruebas reproducibles y automáticas.
- Validar casos límite:
  - Archivo vacío.
  - Solo líneas comentadas.
  - Tipos no presentes.
- Mantener separación entre datos de prueba y datos reales.
