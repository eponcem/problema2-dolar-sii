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

 **A4 - analizar_variacion_anual_a4 (src/anualidad.py):**
   - **Descripción:** Calcula la variación del precio entre enero y diciembre para cada año (2022 a 2025) junto con sus errores propagados, y luego ordena los años de menor a mayor error relativo para identificar cuáles períodos ofrecen estimaciones más confiables.
   - **Resultado:** El año más confiable fue **2025** (Delta P = -80.0 +- 4.60 CLP, Er = 5.75%) y el menos confiable fue **2023** (Delta P = 40.0 +- 8.33 CLP, Er = 20.82%), ya que en 2023 la variación neta fue muy pequeña y cercana a cero.

**A5 - analizar_compra_venta (src/errores.py):**
   - **Descripción:** Recorre toda la serie para encontrar de forma automatizada el mes más barato (mínimo) y el más caro (máximo), calcula la rentabilidad porcentual de operar entre ambos extremos y propaga el error para verificar si la ganancia sobrevive a la incertidumbre.
   - **Resultado:** Comprar en **Febrero 2023** (798.26 CLP) y vender en **Enero 2025** (1000.76 CLP) entrega una rentabilidad de **25.00% +- 0.37%**. Como la rentabilidad supera ampliamente al error, la conclusión es totalmente sólida.

**B1 - analizar_b1_cifras_significativas (src/punto_flotante.py):**
   - **Descripción:** Evalúa el efecto de limitar la precisión a 3 cifras significativas sobre el valor más alto del período (1000.76 CLP) para ilustrar conceptualmente cómo una mantisa de pocos bits introduce un error de representación en punto flotante.
   - **Resultado:** El valor 1000.76 queda guardado como 1000.0 (1.00 x 10^3), produciendo un error absoluto de **0.76 CLP** y un error relativo de **0.0759%**.

**B2 - analizar_deriva (src/punto_flotante.py):**
   - **Descripción:** Ejecuta una operación de ida y vuelta (convertir 1.000.000 CLP a USD y luego de vuelta a CLP usando el mismo precio mensual) en precisión simple float32, midiendo la deriva monetaria acumulada frente al millón exacto a lo largo de los 37 meses.
   - **Resultado:** La deriva oscila estrictamente entre **-0.0625 y +0.0625 CLP** (exactamente 1 ULP de 1.000.000 en float32), actuando como ruido de redondeo sin seguir la tendencia del dólar.

**B4 - analizar_cancelacion_b4 (src/punto_flotante.py):**
   - **Descripción:** Realiza la resta directa 874.67 - 875.66 en precisión doble (float64) y precisión simple (float32) a nivel de hardware, comparando cuántas cifras significativas útiles conserva cada estándar al enfrentar cancelación catastrófica.
   - **Resultado:** En float64 el resultado es **-0.9900000000000091** (retiene aproximadamente 15 cifras válidas), mientras que en float32 es **-0.9899902344** (se degrada a solo 5 cifras válidas por la pérdida de bits significativos en la mantisa).
