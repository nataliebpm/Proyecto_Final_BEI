# Fase 2: Diseño del flujo de trabajo

## Objetivo
Crear un plan modular para procesar datos de un archivo GFF, asegurando reproducibilidad y trazabilidad.

## Flujo de trabajo
1. **Lectura del archivo GFF**
   - Abrir el archivo de forma segura.
   - Ignorar líneas comentadas (`#`).

2. **Filtrado opcional**
   - Si se proporciona `--filter-type`, descartar líneas cuyo tipo no coincida.

3. **Extracción de información relevante**
   - Columna `type` → tipo de feature.
   - Columnas `start` y `end` → longitud del feature.
   - Columna `strand` → `+` o `-`.

4. **Cálculo de estadísticas**
   - `total_features`: contar todas las líneas procesadas.
   - `by_type`: conteo de features por tipo.
   - `avg_length`: longitud promedio por tipo.
   - `strand_distribution`: conteo de `+` y `-`.

5. **Salida**
   - Guardar resultados en un archivo JSON con la estructura requerida.

## Consideraciones bioinformáticas
- Evitar procesar líneas innecesarias.
- Mantener trazabilidad de datos originales a estadísticas.
- Documentar supuestos sobre los datos y formato del archivo.
- Preparar para posibles extensiones (varios archivos, soporte GTF, visualización).
