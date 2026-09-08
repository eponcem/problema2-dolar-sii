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
  - **Resultado:** Ocurrió en **Abril de 2022** con un precio real de 815.12 CLP aproximado a 820.0 CLP (Ea = 4.88 CLP, Er = 0.5987%).

 **A2 - analizar_ejemplo_a2 (src/errores.py):**
   - **Descripción:** Simula una transacción completa de compra y venta con un capital de 1.000.000 CLP entre dos meses fijados (Junio 2023 y Enero 2025), propagando los errores en la división (compra), multiplicación (venta) y resta (ganancia) para determinar el margen de incertidumbre.
   - **Resultado:** Compra en Junio 2023 y venta en Enero 2025 genera una ganancia estimada de **250.000 +- 1.152,44 CLP** (Er = 0.46%).

 **A3 - analizar_cancelacion_a3 (src/anualidad.py):**
   - **Descripción:** Calcula la diferencia del dólar entre dos meses casi idénticos (Diciembre 2022 y Diciembre 2023) redondeados a 3 cifras significativas, sumando los errores absolutos para evaluar si la cercanía de los valores provoca el fenómeno de cancelación numérica.
   - **Resultado:** Variación de **-1.00 +- 0.67 CLP** con un error relativo muy alto de **67.00%**, demostrando cómo la resta de números parecidos amplifica drásticamente la incertidumbre relativa.