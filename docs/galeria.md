# Galería de evidencia experimental

Fotografías del montaje, lecturas del multímetro y capturas del osciloscopio, ordenadas por etapa. La numeración de las figuras coincide con la del informe. [Volver al README](../README.md)

## Diagrama de bloques

<p align="center"><img src="img/diagrama_bloques.png" width="90%"><br><sub><b>Figura 1.</b> Diagrama de bloques funcionales del amplificador de instrumentación de tres op-amps y de la cadena experimental: generación y acondicionamiento → etapa de entrada diferencial (A1, A2) → restador (A3) → instrumentación de medición, con alimentación dual de ±12 V y desacople.</sub></p>

## Etapa A — Montaje y verificación

### Medición y apareamiento de resistencias (multímetro UNI-T UT33B+)

<table align="center">
<tr>
<td align="center" width="25%"><img src="img/etapaA/resistencias/01_R1a_9k77.jpg" width="100%"><br><sub>9.77 kΩ (R1a)</sub></td>
<td align="center" width="25%"><img src="img/etapaA/resistencias/02_R1b_9k77.jpg" width="100%"><br><sub>9.77 kΩ (R1b)</sub></td>
<td align="center" width="25%"><img src="img/etapaA/resistencias/03_R2a_9k79.jpg" width="100%"><br><sub>9.79 kΩ (R2a)</sub></td>
<td align="center" width="25%"><img src="img/etapaA/resistencias/04_R2b_9k80.jpg" width="100%"><br><sub>9.80 kΩ (R2b)</sub></td>
</tr>
<tr>
<td align="center"><img src="img/etapaA/resistencias/05_R3a_9k80.jpg" width="100%"><br><sub>9.80 kΩ (R3a)</sub></td>
<td align="center"><img src="img/etapaA/resistencias/06_R3b_9k80.jpg" width="100%"><br><sub>9.80 kΩ (R3b)</sub></td>
<td align="center"><img src="img/etapaA/resistencias/07_RD1_9k84.jpg" width="100%"><br><sub>9.84 kΩ (RD1)</sub></td>
<td align="center"><img src="img/etapaA/resistencias/08_RD2_97R8.jpg" width="100%"><br><sub>97.8 Ω (RD2)</sub></td>
</tr>
</table>
<p align="center"><sub><b>Figura 2.</b> Mediciones en ohm de las resistencias utilizadas. Las cuatro del restador (R2a, R2b, R3a, R3b) quedaron apareadas en ≈ 9.8 kΩ.</sub></p>

<p align="center"><img src="../hardware/esquematicos/01_etapaA_reposo.png" width="80%"><br><sub><b>Figura 3.</b> Esquemático del amplificador de instrumentación con TL084N y alimentación de ±12 V, en configuración de reposo (V1 = V2 = GND).</sub></p>

<table align="center"><tr>
<td align="center" width="50%"><img src="img/montaje/etapaA_montaje_reposo.jpg" height="420"><br><sub><b>Figura 4.</b> Montaje en protoboard durante la verificación en vacío (TL084N, resistencias, capacitores de 100 nF y puntas del multímetro en VOUT y GND).</sub></td>
<td align="center" width="50%"><img src="img/etapaA/vout_dc_-0v007.jpg" height="420"><br><sub><b>Figura 5.</b> Tensión continua en VOUT con el multímetro del FNIRSI 2C23T: <b>−0.007 V DC</b> (sin saturación).</sub></td>
</tr></table>

> El signo negativo se debe a que las bananas de las puntas se conectaron con los colores invertidos (rojo en COM, negro en VΩ); la magnitud residual de 7 mV no cambia.

## Etapa B — Respuesta a una señal diferencial

<p align="center"><img src="../hardware/esquematicos/02_etapaB_senal_diferencial.png" width="80%"><br><sub><b>Figura 6.</b> Esquemático de la Etapa B: señal diferencial en V1 mediante el divisor RD1–RD2, con V2 conectada a GND.</sub></p>

<table align="center"><tr>
<td align="center" width="50%"><img src="img/etapaB/osc_captura1_vout_0v21pp.jpg" width="100%"><br><sub><b>Figura 7.</b> Primera captura (ganancia 21): CH1 azul (VOUT) = <b>0.21 Vpp</b> a 100 mV/div, 60.24 Hz; CH2 amarillo (V1) = <b>0.01 Vpp</b> a 20 mV/div, en fase.</sub></td>
<td align="center" width="50%"><img src="img/etapaB/osc_captura2_vout_0v22pp.jpg" width="100%"><br><sub><b>Figura 8.</b> Segunda captura (fluctuación a ganancia 22): CH1 azul (VOUT) = <b>0.22 Vpp</b>; CH2 amarillo (V1) = 0.01 Vpp, en fase.</sub></td>
</tr></table>

<p align="center"><img src="img/montaje/etapaB_conexion_divisor.jpg" width="75%"><br><sub><b>Figura 9.</b> Conexión del circuito, el divisor resistivo de entrada y las puntas CH1/CH2 en la Etapa B.</sub></p>

## Etapa C — Respuesta a una señal de modo común

<p align="center"><img src="../hardware/esquematicos/03_etapaC_modo_comun.png" width="80%"><br><sub><b>Figura 10.</b> Esquemático de la Etapa C: la misma señal se aplica simultáneamente a V1 y V2 para evaluar su rechazo en la salida.</sub></p>

<table align="center"><tr>
<td align="center" width="50%"><img src="img/etapaC/osc_modo_comun_1v05pp.jpg" height="460"><br><sub><b>Figura 11.</b> CH2 amarillo (V1 = V2) = <b>1.05 Vpp</b> a 60.98 Hz; CH1 azul (VOUT) plano dentro del piso de ruido de <b>0.01 Vpp</b> (Freq: 0.00 Hz).</sub></td>
<td align="center" width="50%"><img src="img/montaje/etapaC_conexion_modo_comun.jpg" height="460"><br><sub><b>Figura 12.</b> Conexión en modo común (V1 puenteada con V2 y entrada directa del generador).</sub></td>
</tr></table>

## Figuras de análisis

Generadas por [`analysis/analisis_cmrr.py`](../analysis/analisis_cmrr.py).

<table align="center">
<tr>
<td align="center" width="50%"><img src="img/resultados/etapaB_vs_etapaC.png" width="100%"><br><sub>Entrada y salida en las Etapas B y C (escala logarítmica).</sub></td>
<td align="center" width="50%"><img src="img/resultados/cmrr_comparacion.png" width="100%"><br><sub>CMRR experimental, modelado y de peor caso frente a la IEC 60601-2-25.</sub></td>
</tr>
<tr>
<td align="center"><img src="img/resultados/resistencias_desviacion.png" width="100%"><br><sub>Desviación de cada resistencia respecto a su valor nominal.</sub></td>
<td align="center"><img src="img/resultados/acm_vs_tolerancia.png" width="100%"><br><sub>Acm del restador sin aparear en función de la tolerancia.</sub></td>
</tr>
</table>
