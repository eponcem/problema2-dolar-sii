# Informe Laboratorio 1: La ganancia que se evapora
**Computación Numérica Universidad Católica del Maule**
- **Integrante : Ernesto Ponce Muñoz**
## 1. Análisis de Error (Preguntas A1 a A5)

### A1. Error de representación mes a mes
Se redondearon los precios mensuales a 2 cifras significativas. El mes con mayor error relativo al redondear fue **Abril de 2022**:
1. Precio real: $815.12 CLP
2. Precio aproximado: $820.0 CLP
3. Error absoluto: Ea = |815.12 - 820.0| = 4.88 CLP
4. Error relativo: Er = (4.88 / 815.12) * 100 = 0.5987%

### A2. Evaluación entre dos puntos (Compra y venta de ejemplo)
Se seleccionó como prueba comprar en Junio de 2023 y vender en Enero de 2025 con un capital de M = $1.000.000 CLP:
1. Compra (Junio 2023): Real = 799.87 CLP, Aprox = 800.0 CLP (Er = 0.0163%)
   - Dólares obtenidos = 1.000.000 / 800.0 = 1.250 USD
2. Venta (Enero 2025): Real = 1000.76 CLP, Aprox = 1000.0 CLP (Er = 0.0759%)
   - Pesos finales = 1.250 * 1000.0 = $1.250.000 CLP
3. Propagación del error:
   - Er(pesos_final) = 0.0163% + 0.0759% = 0.0922%
   - Ea(Ganancia) = (0.0922 / 100) * 1.250.000 = 1.152,44 CLP
4. Ganancia calculada: $250.000 ± 1.152,44 CLP (Error relativo: 0.46%).

### A3. Cancelación entre Diciembre 2022 y Diciembre 2023
Calculando la variación del dólar con 3 cifras significativas:
1. Diciembre 2022: Real = 875.66 CLP, Aprox = 876.0 CLP (Ea = 0.34 CLP)
2. Diciembre 2023: Real = 874.67 CLP, Aprox = 875.0 CLP (Ea = 0.33 CLP)
3. Variación estimada: Delta P = 875.0 - 876.0 = -1.00 CLP
4. Error propagado en la resta: Ea = 0.34 + 0.33 = 0.67 CLP
5. Error relativo: Er = (0.67 / 1.00) * 100 = 67.00%
6. Resultado: Delta P = -1.00 ± 0.67 CLP (intervalo [-1.67, -0.33] CLP).

**¿Se puede afirmar con seguridad si el dólar subió o bajó?**  
Al ser todo el intervalo negativo (no cruza el cero), matemáticamente se puede afirmar que el dólar bajó. Sin embargo, la incertidumbre representa un 67% de la magnitud, lo que demuestra una cancelación catastrófica fuerte por la cercanía de ambos precios.

### A4. Variación anual (Enero a Diciembre)
Calculando la variación anual (Precio_diciembre - Precio_enero) a 2 cifras significativas:
1. **2025:** Delta P = -80.0 ± 4.60 CLP (Error relativo: 5.75%) -> Más confiable
2. **2024:** Delta P = +70.0 ± 4.31 CLP (Error relativo: 6.16%)
3. **2022:** Delta P = +60.0 ± 6.39 CLP (Error relativo: 10.65%)
4. **2023:** Delta P = +40.0 ± 8.33 CLP (Error relativo: 20.82%) -> Menos confiable

**¿Qué tienen en común los años poco confiables?**  
Tienen en común que la variación neta en el año fue muy pequeña. Al restar valores cercanos se pierden cifras significativas y el error acumulado se divide por un número chico, disparando el error relativo. En cambio, años con cambios grandes (como 2025 con 80 CLP de diferencia) absorben mejor el error.

### A5. Mejor compra y mejor venta
1. Mes más barato: Febrero de 2023 con $798.26 CLP (Aprox: $800.0 CLP)
2. Mes más caro: Enero de 2025 con $1000.76 CLP (Aprox: $1000.0 CLP)
3. Rentabilidad obtenida: 25.00% ± 0.37% (Ganancia de $250.000 CLP frente a un error de ± $3.673,95 CLP).

**¿La conclusión sobrevive al error o queda en duda?**  
Sobrevive con total seguridad. La ganancia estimada es 68 veces mayor que la incertidumbre, y el rango de rentabilidad queda entre 24.63% y 25.37%, por lo que la recomendación es completamente sólida.

---

## 2. Preguntas de Punto Flotante (B1, B2, B4)

### B1. Cifras significativas y mantisa corta
Trabajar en base decimal con solo 2 cifras significativas equivale a truncar la mantisa en binario a muy pocos bits (aproximadamente 6.6 bits), lo que produce que los valores queden muy separados entre sí.
Con el precio 1000.76 a 3 cifras significativas:
1. Valor real: 1000.76 CLP
2. Valor aproximado: 1000.0 CLP
3. Error absoluto: Ea = 0.76 CLP
4. Error relativo: Er = 0.0759%

### B2. La ida y vuelta que no vuelve
Al convertir $1.000.000 CLP a dólares con float32 y volver inmediatamente a pesos:
1. Se produce una diferencia (deriva) que se mueve entre -0.0625 y +0.0625 CLP.
2. Esto ocurre porque 1 ULP para un millón en float32 vale exactamente 0.0625 CLP (2^-4).
3. Esta deriva no sigue el patrón del precio del dólar (correlación r = -0.37); es simplemente ruido numérico por el redondeo en los últimos bits de la mantisa.
