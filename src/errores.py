import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from cargar_datos import cargar_csv

def redondear_cifras(x, cifras=2):
    if x == 0:
        return 0.0
    return float(f"{x:.{cifras}g}")

def escribir_seccion_csv(ruta, modo, titulo, cabecera, filas):
    with open(ruta, modo, newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow([titulo])
        escritor.writerow(cabecera)
        for fila in filas:
            escritor.writerow(fila)
        escritor.writerow([])

def analizar_error_representacion(valores, etiquetas, directorio):
    val_aprox_lista = []
    for v in valores:
        val_aprox_lista.append(redondear_cifras(v, 2))
    val_aprox = np.array(val_aprox_lista)

    ea = np.abs(valores - val_aprox)
    er = (ea / valores) * 100

    filas = []
    for i in range(len(valores)):
        fila = [
            etiquetas[i],
            valores[i],
            val_aprox[i],
            round(float(ea[i]), 4),
            round(float(er[i]), 4)
        ]
        filas.append(fila)

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv,
        'w',
        ' A1: error de representacion por mes (2 cifras significativas) ',
        ['mes', 'precio_real', 'precio_aprox', 'error_absoluto', 'error_relativo_pct'],
        filas
    )

    idx_max_er = int(np.argmax(er))
    print(f"[A1] Mes con mayor error relativo al redondear: {etiquetas[idx_max_er]}")
    print(f"     Precio real: {valores[idx_max_er]}, Aprox: {val_aprox[idx_max_er]}")
    print(f"     Error absoluto: {ea[idx_max_er]:.4f} CLP, Error relativo: {er[idx_max_er]:.4f}%")

    # Grafico 1: Serie mensual
    plt.figure(figsize=(12, 5))
    plt.plot(etiquetas, valores, marker='o', markersize=3, color='steelblue', label='Precio Real (SII)')
    plt.plot(etiquetas, val_aprox, linestyle='--', color='orange', label='Aproximación (2 cifras)')
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel('Precio (CLP)')
    plt.title('Gráfico 1: Serie Mensual del Dólar Observado 2022–2025 (Real vs 2 Cifras)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/1_serie_mensual.png'))
    plt.close()

    # Grafico 3: Error de representacion absoluto
    plt.figure(figsize=(12, 5))
    plt.bar(etiquetas, ea, color='forestgreen', edgecolor='black', linewidth=0.5)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel('Error Absoluto (CLP)')
    plt.title('Gráfico 3: Error de Representación Absoluto por Mes al Usar 2 Cifras Significativas')
    plt.grid(True, axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/3_error_representacion.png'))
    plt.close()

def evaluar_compra_venta(precio_compra_real, precio_venta_real, monto=1000000):
    p_compra_aprox = redondear_cifras(precio_compra_real, 2)
    p_venta_aprox = redondear_cifras(precio_venta_real, 2)

    er_compra = (abs(precio_compra_real - p_compra_aprox) / precio_compra_real) * 100
    er_venta = (abs(precio_venta_real - p_venta_aprox) / precio_venta_real) * 100

    usd = monto / p_compra_aprox
    pesos_final = usd * p_venta_aprox
    ganancia = pesos_final - monto

    er_pesos_final = er_compra + er_venta
    ea_ganancia = (er_pesos_final / 100.0) * pesos_final

    rentabilidad = (ganancia / monto) * 100
    error_rentabilidad = (ea_ganancia / monto) * 100

    resultado = {
        'p_compra_aprox': p_compra_aprox,
        'p_venta_aprox': p_venta_aprox,
        'usd': usd,
        'pesos_final': pesos_final,
        'ganancia': ganancia,
        'ea_ganancia': ea_ganancia,
        'rentabilidad': rentabilidad,
        'error_rentabilidad': error_rentabilidad
    }
    return resultado

def analizar_ejemplo_a2(valores, etiquetas, directorio, idx_compra=17, idx_venta=36):
    p_compra_real = valores[idx_compra]
    p_venta_real = valores[idx_venta]
    r = evaluar_compra_venta(p_compra_real, p_venta_real)
    er_ganancia_pct = (abs(r['ea_ganancia'] / r['ganancia']) * 100) if r['ganancia'] != 0 else 0.0

    print(f"[A2] Ejemplo compra-venta:")
    print(f"     Compra: {etiquetas[idx_compra]} ({r['p_compra_aprox']} CLP)")
    print(f"     Venta: {etiquetas[idx_venta]} ({r['p_venta_aprox']} CLP)")
    print(f"     Ganancia: {r['ganancia']:.2f} +- {r['ea_ganancia']:.2f} CLP (Error: {er_ganancia_pct:.2f}%)")

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' A2: compra-venta de ejemplo ',
        ['mes_compra', 'mes_venta', 'ganancia_clp', 'error_absoluto_clp', 'error_relativo_pct'],
        [[
            etiquetas[idx_compra],
            etiquetas[idx_venta],
            round(float(r['ganancia']), 2),
            round(float(r['ea_ganancia']), 2),
            round(float(er_ganancia_pct), 2)
        ]]
    )

def analizar_compra_venta(valores, etiquetas, directorio):
    monto = 1000000
    idx_min = int(np.argmin(valores))
    idx_max = int(np.argmax(valores))
    p_compra_real = valores[idx_min]

    p_compra_aprox = redondear_cifras(p_compra_real, 2)
    er_compra = (abs(p_compra_real - p_compra_aprox) / p_compra_real) * 100

    meses_venta = valores[idx_min + 1:]
    etiq_venta = etiquetas[idx_min + 1:]

    aprox_venta_lista = []
    for v in meses_venta:
        aprox_venta_lista.append(redondear_cifras(v, 2))
    p_venta_aprox = np.array(aprox_venta_lista)

    er_venta = (np.abs(meses_venta - p_venta_aprox) / meses_venta) * 100

    usd = monto / p_compra_aprox
    pesos_final = usd * p_venta_aprox
    ganancia = pesos_final - monto

    er_pesos_final = er_compra + er_venta 
    ea_ganancia = (er_pesos_final / 100.0) * pesos_final 
    
    rentabilidad = (ganancia / monto) * 100
    error_rentabilidad = (ea_ganancia / monto) * 100
    
    # Grafico 4
    plt.figure(figsize=(12, 5))
    plt.errorbar(
        etiq_venta,
        rentabilidad,
        yerr=error_rentabilidad,
        fmt='o-',
        color='steelblue',
        ecolor='red',
        capsize=3,
        label='Rentabilidad (%) +- Error'
    )
    plt.axhline(0, color='black', linestyle='--', linewidth=1)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel('Rentabilidad (%)')
    plt.title('Gráfico 4: Rentabilidad de Comprar en el Mínimo y Vender en Cada Mes Posterior')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/4_rentabilidad.png'))
    plt.close()

    r_optimo = evaluar_compra_venta(valores[idx_min], valores[idx_max])
    conclusion_solida = bool(r_optimo['ganancia'] > r_optimo['ea_ganancia'])

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')

    filas_tabla = []
    for i in range(len(etiq_venta)):
        fila = [
            etiq_venta[i],
            round(float(meses_venta[i]), 2),
            round(float(ganancia[i]), 2),
            round(float(ea_ganancia[i]), 2),
            round(float(er_pesos_final[i]), 2)
        ]
        filas_tabla.append(fila)

    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' A5: comprar en el minimo, vender en cada mes posterior ',
        ['mes_venta', 'precio_venta_real', 'ganancia_clp', 'error_absoluto_clp', 'error_relativo_pct'],
        filas_tabla
    )

    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' A5: comprar en el minimo, vender en el maximo del periodo ',
        ['mes_compra', 'mes_venta', 'rentabilidad_pct', 'error_pct', 'conclusion_solida'],
        [[
            etiquetas[idx_min],
            etiquetas[idx_max],
            round(float(r_optimo['rentabilidad']), 2),
            round(float(r_optimo['error_rentabilidad']), 2),
            conclusion_solida
        ]]
    )

    print(f"[A5] Minimo = {etiquetas[idx_min]} ({valores[idx_min]} CLP), Maximo = {etiquetas[idx_max]} ({valores[idx_max]} CLP)")
    print(f"     Rentabilidad = {r_optimo['rentabilidad']:.2f}% +- {r_optimo['error_rentabilidad']:.2f}%")
    print(f"     ¿Conclusion solida?: {'Si' if conclusion_solida else 'No'}")

if __name__ == '__main__':
    directorio_script = os.path.dirname(__file__)
    ruta_csv_datos = os.path.join(directorio_script, '../data/dolar_observado_sii_2022_2025.csv')
    valores, etiquetas = cargar_csv(ruta_csv_datos)
    
    analizar_error_representacion(valores, etiquetas, directorio_script)
    analizar_ejemplo_a2(valores, etiquetas, directorio_script)
    analizar_compra_venta(valores, etiquetas, directorio_script)
