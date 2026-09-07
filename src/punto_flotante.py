import numpy as np
import os
import matplotlib.pyplot as plt
from cargar_datos import cargar_csv
from errores import redondear_cifras, escribir_seccion_csv

def analizar_b1_cifras_significativas(directorio):
    val_real = 1000.76
    val_aprox_3 = redondear_cifras(val_real, 3)
    ea_1000 = abs(val_real - val_aprox_3)
    er_1000 = (ea_1000 / val_real) * 100.0

    print(f"[B1] 1000.76 a 3 cifras: real = {val_real}, aprox = {val_aprox_3}")
    print(f"     Ea = {ea_1000:.4f} CLP, Er = {er_1000:.4f}%")

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' B1: cifras significativas (1000.76 a 3 cifras) ',
        ['valor_real', 'valor_aprox_3cifras', 'error_absoluto', 'error_relativo_pct'],
        [[val_real, val_aprox_3, round(ea_1000, 4), round(er_1000, 4)]]
    )

def analizar_deriva(valores, etiquetas, directorio):
    monto = np.float32(1000000.0)
    v_f32 = np.float32(valores)

    usd = monto / v_f32
    recuperado = usd * v_f32
    deriva = monto - recuperado

    print(f"[B2] Deriva ida y vuelta float32: min = {np.min(deriva):.4f}, max = {np.max(deriva):.4f} CLP")

    # Grafico 5: Comparacion precio del dolar vs deriva en float32
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    ax1.plot(etiquetas, valores, color='steelblue', marker='o', markersize=3, label='Precio Dolar (CLP)')
    ax1.set_ylabel('Dolar (CLP)')
    ax1.set_title('Grafico 5: Precio del Dolar vs Deriva en Float32 (Ida y Vuelta)')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend()

    ax2.plot(etiquetas, deriva, color='red', marker='o', markersize=3, linestyle='--', label='Deriva (CLP)')
    ax2.axhline(0, color='black', linewidth=1)
    ax2.set_ylabel('Deriva (CLP)')
    ax2.set_xlabel('Mes')
    ax2.tick_params(axis='x', rotation=90, labelsize=7)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(os.path.join(directorio, '../graficos/5_deriva_flotante.png'))
    plt.close()

def analizar_cancelacion_b4(directorio):
    v23 = 874.67
    v22 = 875.66
    resta_exacta = v23 - v22  # -0.99

    # En float64 (doble precision)
    f64_23 = np.float64(v23)
    f64_22 = np.float64(v22)
    resta_f64 = f64_23 - f64_22

    # En float32 (simple precision)
    f32_23 = np.float32(v23)
    f32_22 = np.float32(v22)
    resta_f32 = f32_23 - f32_22

    print(f"[B4] Resta 874.67 - 875.66:")
    print(f"     Exacto:  {resta_exacta:.4f}")
    print(f"     Float64: {resta_f64:.16f}")
    print(f"     Float32: {resta_f32:.10f}")

    ruta_csv = os.path.join(directorio, '../evaluacion_errores.csv')
    escribir_seccion_csv(
        ruta_csv,
        'a',
        ' B4: cancelacion en maquina (874.67 - 875.66) ',
        ['tipo', 'resultado', 'cifras_validas'],
        [
            ['valor_exacto', str(resta_exacta), 'Todas'],
            ['float64', f"{float(resta_f64):.16f}", '~15 cifras'],
            ['float32', f"{float(resta_f32):.10f}", '~5 cifras']
        ]
    )

if __name__ == '__main__':
    directorio_script = os.path.dirname(__file__)
    ruta_csv_datos = os.path.join(directorio_script, '../data/dolar_observado_sii_2022_2025.csv')
    valores, etiquetas = cargar_csv(ruta_csv_datos)

    analizar_b1_cifras_significativas(directorio_script)
    analizar_deriva(valores, etiquetas, directorio_script)
    analizar_cancelacion_b4(directorio_script)
