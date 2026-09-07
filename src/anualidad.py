import numpy as np
import os
import matplotlib.pyplot as plt
from cargar_datos import cargar_csv
from errores import redondear_cifras, escribir_seccion_csv

def analizar_cancelacion_a3(valores, directorio):
    # Diciembre 2022 (indice 11) y Diciembre 2023 (indice 23)
    v22 = valores[11]
    v23 = valores[23]

    aprox22 = redondear_cifras(v22, 3)
    aprox23 = redondear_cifras(v23, 3)

    ea22 = abs(v22 - aprox22)
    ea23 = abs(v23 - aprox23)

    delta_a3 = aprox23 - aprox22
    ea_delta_a3 = ea22 + ea23
    er_delta_a3 = (ea_delta_a3 / abs(delta_a3)) * 100.0
    afirmacion_segura = bool(abs(delta_a3) > ea_delta_a3)

    print(f"[A3] Dic 2022 = {v22} (aprox {aprox22}), Dic 2023 = {v23} (aprox {aprox23})")
    print(f"     Delta P = {delta_a3:.2f} +- {ea_delta_a3:.2f} CLP (Error: {er_delta_a3:.2f}%)")
    print(f"     ¿Afirmacion segura?: {'Si' if afirmacion_segura else 'No'}")

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' A3: cancelacion diciembre 2022 vs diciembre 2023 (3 cifras) ',
        ['delta_p', 'error_absoluto', 'error_relativo_pct', 'afirmacion_segura'],
        [[round(delta_a3, 2), round(ea_delta_a3, 2), round(er_delta_a3, 2), afirmacion_segura]]
    )

def analizar_variacion_anual_a4(valores, directorio):
    anios = [2022, 2023, 2024, 2025]
    idx_eneros = [0, 12, 24, 36]
    idx_dic = [11, 23, 35, 47]

    filas_a4 = []
    for i in range(len(anios)):
        p_ene = valores[idx_eneros[i]]
        p_dic = valores[idx_dic[i]]
        
        ap_ene = redondear_cifras(p_ene, 2)
        ap_dic = redondear_cifras(p_dic, 2)
        
        ea_e = abs(p_ene - ap_ene)
        ea_d = abs(p_dic - ap_dic)
        
        delta_anio = ap_dic - ap_ene
        ea_delta = ea_e + ea_d
        er_delta = (ea_delta / abs(delta_anio)) * 100.0
        
        filas_a4.append([anios[i], round(delta_anio, 2), round(ea_delta, 2), round(er_delta, 2)])

    # Ordenar por menor error relativo (mas confiable primero)
    filas_a4.sort(key=lambda x: x[3])

    print("[A4] Variacion anual (Enero -> Diciembre) ordenada por confiabilidad:")
    for fila in filas_a4:
        print(f"     Año {fila[0]}: Delta = {fila[1]} +- {fila[2]} CLP, Error = {fila[3]}%")

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' A4: variacion enero-diciembre por año (mas confiable primero) ',
        ['año', 'variacion_clp', 'error_absoluto', 'error_relativo_pct'],
        filas_a4
    )

def graficar_cancelacion_mensual(valores, etiquetas, directorio):
    aprox_todos = []
    for v in valores:
        aprox_todos.append(redondear_cifras(v, 2))
    val_aprox = np.array(aprox_todos)

    deltas_mes = np.diff(val_aprox)
    ea_mes = np.abs(valores - val_aprox)
    ea_propagado_mes = ea_mes[1:] + ea_mes[:-1]

    colores = []
    for i in range(len(deltas_mes)):
        if abs(deltas_mes[i]) <= ea_propagado_mes[i]:
            colores.append('red')
        else:
            colores.append('steelblue')

    plt.figure(figsize=(12, 5))
    plt.bar(
        etiquetas[1:],
        deltas_mes,
        yerr=ea_propagado_mes,
        color=colores,
        capsize=2
    )
    plt.axhline(0, color='black', linewidth=1)
    plt.xticks(rotation=90, fontsize=7)
    plt.ylabel('Variacion Delta P (CLP)')
    plt.title('Grafico 2: Variacion Mes a Mes (Rojo: Cancelacion/Incierto | Azul: Confiable)')
    plt.grid(True, axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/2_cancelacion_mensual.png'))
    plt.close()

if __name__ == '__main__':
    directorio_script = os.path.dirname(__file__)
    ruta_csv = os.path.join(directorio_script, '../data/dolar_observado_sii_2022_2025.csv')
    valores, etiquetas = cargar_csv(ruta_csv)
    
    analizar_cancelacion_a3(valores, directorio_script)
    analizar_variacion_anual_a4(valores, directorio_script)
    graficar_cancelacion_mensual(valores, etiquetas, directorio_script)
