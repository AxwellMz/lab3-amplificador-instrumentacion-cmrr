# Datos experimentales

| Archivo | Contenido |
|---|---|
| `tabla1_resistencias.csv` | Etapa A (paso 1): valor nominal y valor medido de las nueve resistencias, con su función en el circuito. |
| `tabla2_etapaA_offset.csv` | Etapa A (paso 5): tensión continua en VOUT con V1 = V2 = GND. |
| `tabla3_etapaB_diferencial.csv` | Etapa B (paso 8): dos capturas del osciloscopio con la señal diferencial (V1, VOUT, frecuencia, fase). |
| `tabla4_etapaC_modo_comun.csv` | Etapa C (paso 10): señal de modo común V1 = V2 y piso de ruido medido en VOUT. |
| `resultados_resumen.csv` | Generado por `analysis/analisis_cmrr.py`: Ad teórica, Ad medida, Acm, CMRR y errores. |
| `peor_caso_tolerancia.csv` | Generado por `analysis/analisis_cmrr.py`: Acm y CMRR del restador sin aparear para tolerancias de 0.1 % a 10 %. |

Unidades: ohm (Ω) y voltios (V). Resistencias medidas con multímetro UNI-T UT33B+; tensiones y capturas con el multímetro-osciloscopio portátil FNIRSI 2C23T (acoplamiento AC, sondas ×1, 5 ms/div). La numeración de las tablas coincide con la del informe.
