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

