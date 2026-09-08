# Laboratorio 1: La ganancia que se evapora
Análisis de cancelación y propagación de errores con el dólar observado del SII (2022–2025).

## Descripción
Este proyecto analiza el impacto del redondeo a pocas cifras significativas y la aritmética de punto flotante (IEEE 754) en transacciones de compra y venta de dólares con un capital de $1.000.000 CLP, evaluando cuándo una rentabilidad es confiable y cuándo se pierde por cancelación numérica.

## Ejecución
Para ejecutar los análisis y generar los gráficos y el archivo de resultados:

- python src/errores.py
- python src/anualidad.py
- python src/punto_flotante.py

## Síntesis de Resultados por Función
 **A1 - analizar_error_representacion (src/errores.py):**
   - **Descripción:** Esta función redondea todos los precios mensuales a 2 cifras significativas usando mantisa corta, calcula el error absoluto y relativo para cada mes y busca cuál registró el mayor desvío relativo respecto al valor oficial.
  1. **Resultado:** Ocurrió en **Abril de 2022** con un precio real de 815.12 CLP aproximado a 820.0 CLP (Ea = 4.88 CLP, Er = 0.5987%).
