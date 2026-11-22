"""
Análisis de datos - Laboratorio N.º 3, Instrumentación Biomédica III (UNMSM)
Amplificador de instrumentación (3 op-amps, TL084N) y rechazo de modo común

    Etapa A: offset en reposo          ->  |VOUT| < 1 V con V1 = V2 = GND
    Etapa B: ganancia diferencial      ->  Ad = VOUT / V1   (V2 = GND, divisor RD1-RD2)
    Etapa C: ganancia de modo común    ->  Acm = VOUT / Vcm (V1 = V2)
             razón de rechazo          ->  CMRR = 20·log10(Ad / Acm)

Modelo exacto con las resistencias medidas (Tabla 1):
    Gd1 = 1 + (R1a + R1b) / Rg
    p = R3a / R2a ,  q = R3b / R2b
    VOUT = [(1+q)·p/(1+p)]·Vo1 − q·Vo2
    Ad   = (Gd1/2)·[(1+q)·p/(1+p) + q]
    Acm  = (p − q) / (1 + p)

Uso:
    pip install pandas numpy matplotlib
    python analysis/analisis_cmrr.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
IMG = ROOT / "docs" / "img" / "resultados"
IMG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.3, "figure.dpi": 150,
})
AZUL, NARANJA, VERDE, ROJO, GRIS = "#1F4E79", "#E07B39", "#2E8B57", "#C0392B", "#7F7F7F"


def db(x):
    return 20 * np.log10(x)


# ---------------------------------------------------------------- Tabla 1
t1 = pd.read_csv(DATA / "tabla1_resistencias.csv").set_index("Resistencia")
R = t1["Medido_ohm"]
t1["Desviacion_%"] = (t1["Medido_ohm"] - t1["Nominal_ohm"]) / t1["Nominal_ohm"] * 100

# ------------------------------------------------- Modelo con valores medidos
Gd1 = 1 + (R["R1a"] + R["R1b"]) / R["Rg"]
p = R["R3a"] / R["R2a"]
q = R["R3b"] / R["R2b"]
k_pos = (1 + q) * p / (1 + p)                       # ganancia de la rama no inversora de A3
Ad_teo = (Gd1 / 2) * (k_pos + q)                    # ganancia diferencial
Acm_teo = (p - q) / (1 + p)                         # ganancia de modo común (desajuste resistivo)
Ad_eff = k_pos * (1 + R["R1a"] / R["Rg"]) + q * (R["R1b"] / R["Rg"])  # V2 = 0 (Etapa B)
CMRR_teo = db(Ad_teo / Acm_teo)

# ---------------------------------------------------------------- Etapa A
t2 = pd.read_csv(DATA / "tabla2_etapaA_offset.csv")
vout_dc = t2.loc[0, "VOUT_DC_V"]

# ---------------------------------------------------------------- Etapa B
t3 = pd.read_csv(DATA / "tabla3_etapaB_diferencial.csv")
t3["Ad_medida"] = t3["VOUT_Vpp"] / t3["V1_Vpp"]
t3["Error_%"] = (t3["Ad_medida"] - Ad_teo).abs() / Ad_teo * 100
div = R["RD2"] / (R["RD1"] + R["RD2"])

# ---------------------------------------------------------------- Etapa C
t4 = pd.read_csv(DATA / "tabla4_etapaC_modo_comun.csv")
vcm = t4.loc[0, "V1_igual_V2_Vpp"]
ruido = t4.loc[0, "VOUT_ruido_Vpp"]
Acm_exp = ruido / vcm                               # cota superior (VOUT real < ruido)
Ad_med = t3.loc[0, "Ad_medida"]
CMRR_exp = db(Ad_med / Acm_exp)                     # cota inferior
v1_div = vcm * div                                  # V1 real estimado en la Etapa B
vout_est = v1_div * Ad_eff
vout_cm_teo = vcm * Acm_teo

# ------------------------------------------- CMRR global estimado (TL084 + R)
def cmrr_global(cmrr_op_db):
    cmrr_op = 10 ** (cmrr_op_db / 20)
    return db(1 / (1 / cmrr_op + 1 / (Gd1 / Acm_teo)))

# --------------------------------------------- Peor caso sin aparear (±ε)
eps = np.array([0.001, 0.0025, 0.005, 0.01, 0.02, 0.05, 0.10])
acm_wc = 2 * eps / (1 - eps)
pc = pd.DataFrame({
    "Tolerancia_%": eps * 100,
    "Acm_max": acm_wc.round(6),
    "VOUT_fuga_mVpp_con_1.05Vpp": (acm_wc * vcm * 1000).round(2),
    "CMRR_dB": db(Ad_teo / acm_wc).round(2),
})
pc.to_csv(DATA / "peor_caso_tolerancia.csv", index=False)

# ------------------------------------------------------------- Resumen
res = pd.DataFrame([
    ("Offset VOUT (Etapa A)", vout_dc, "V"),
    ("Gd1 = 1 + (R1a+R1b)/Rg", Gd1, "-"),
    ("p = R3a/R2a", p, "-"),
    ("q = R3b/R2b", q, "-"),
    ("Ad teorica (valores medidos)", Ad_teo, "-"),
    ("Ad efectiva con V2 = 0", Ad_eff, "-"),
    ("Ad medida captura 1", t3.loc[0, "Ad_medida"], "-"),
    ("Ad medida captura 2", t3.loc[1, "Ad_medida"], "-"),
    ("Error Ad captura 1", t3.loc[0, "Error_%"], "%"),
    ("Error Ad captura 2", t3.loc[1, "Error_%"], "%"),
    ("V1 estimado con divisor medido", v1_div * 1000, "mVpp"),
    ("VOUT estimado Etapa B", vout_est, "Vpp"),
    ("Acm experimental (cota superior)", Acm_exp, "-"),
    ("Acm teorica (desajuste resistivo)", Acm_teo, "-"),
    ("VOUT teorico Etapa C", vout_cm_teo * 1000, "mVpp"),
    ("CMRR experimental (cota inferior)", CMRR_exp, "dB"),
    ("CMRR modelo resistivo", CMRR_teo, "dB"),
    ("CMRR global estimado (TL084 tip. 86 dB)", cmrr_global(86), "dB"),
    ("CMRR global estimado (TL084 min. 70 dB)", cmrr_global(70), "dB"),
], columns=["Magnitud", "Valor", "Unidad"])
res["Valor"] = res["Valor"].astype(float).round(7)
res.to_csv(DATA / "resultados_resumen.csv", index=False)

print(f"[Etapa A] VOUT = {vout_dc*1000:.0f} mV DC -> {'CUMPLE' if abs(vout_dc) < 1 else 'SATURADO'} (|VOUT| < 1 V)")
print(f"[Modelo ] Gd1 = {Gd1:.4f} | p = {p:.6f} | q = {q:.6f} | Ad = {Ad_teo:.4f} | Ad(V2=0) = {Ad_eff:.4f}")
for _, r in t3.iterrows():
    print(f"[Etapa B] Captura {int(r.Captura)}: {r.VOUT_Vpp:.2f}/{r.V1_Vpp:.2f} -> Ad = {r.Ad_medida:.1f} | error = {r['Error_%']:.2f} %")
print(f"[Etapa B] Divisor medido: V1 = {v1_div*1000:.3f} mVpp -> VOUT esperado = {vout_est:.4f} Vpp")
print(f"[Etapa C] Acm < {Acm_exp:.6f} -> CMRR > {CMRR_exp:.2f} dB (limitado por el piso de ruido de {ruido*1000:.0f} mVpp)")
print(f"[Modelo ] Acm = {Acm_teo:.7f} | fuga = {vout_cm_teo*1000:.3f} mVpp | CMRR = {CMRR_teo:.2f} dB")
print(f"[Global ] CMRR estimado: {cmrr_global(86):.2f} dB (TL084 típ.) | {cmrr_global(70):.2f} dB (TL084 mín.)")
print(f"[Peor c.] ±5 %: Acm = {acm_wc[5]:.4f}, CMRR = {db(Ad_teo/acm_wc[5]):.2f} dB | ±1 %: Acm = {acm_wc[3]:.4f}, CMRR = {db(Ad_teo/acm_wc[3]):.2f} dB")

# ============================================================== Figuras
# 1) Desviación de las resistencias
fig, ax = plt.subplots(figsize=(7.5, 3.6))
cols = [VERDE if n in ("R2a", "R2b", "R3a", "R3b") else AZUL for n in t1.index]
bars = ax.bar(t1.index, t1["Desviacion_%"], color=cols)
for b, v in zip(bars, t1["Desviacion_%"]):
    ax.text(b.get_x() + b.get_width() / 2, v / 2, f"{v:.1f} %", ha="center", va="center", fontsize=8, color="white", weight="bold")
ax.axhline(-5, color=ROJO, ls="--", lw=1, label="Límite de tolerancia (−5 %)")
ax.set_ylim(-5.8, 0.5)
ax.set_ylabel("Desviación respecto al nominal (%)")
ax.set_title("Tabla 1 · Resistencias medidas (verde: pares apareados del restador)")
ax.legend(loc="lower right", fontsize=8)
fig.tight_layout(); fig.savefig(IMG / "resistencias_desviacion.png"); plt.close(fig)

# 2) Entrada vs salida en las Etapas B y C (escala logarítmica)
fig, ax = plt.subplots(figsize=(7, 4))
x = np.arange(2); w = 0.36
vin = [t3.loc[0, "V1_Vpp"], vcm]
vout = [t3.loc[0, "VOUT_Vpp"], ruido]
b1 = ax.bar(x - w / 2, vin, w, color=NARANJA, label="Entrada (CH2)")
b2 = ax.bar(x + w / 2, vout, w, color=AZUL, label="Salida VOUT (CH1)")
b2[1].set_hatch("//"); b2[1].set_alpha(0.55)
ax.set_yscale("log"); ax.set_ylim(3e-3, 3)
ax.set_xlim(-0.6, 1.75)
ax.set_xticks(x, ["Etapa B · señal diferencial\n(V2 = GND)", "Etapa C · modo común\n(V1 = V2)"])
ax.set_ylabel("Amplitud (Vpp, escala log)")
for b, v in zip(list(b1) + list(b2), vin + vout):
    ax.text(b.get_x() + b.get_width() / 2, v * 1.15, f"{v:.2f}", ha="center", fontsize=9)
ax.text(1 + w / 2, ruido * 0.6, "piso de\nruido", ha="center", va="center", fontsize=7, color="white", weight="bold")
ax.annotate("×21", xy=(0.18, 0.21), xytext=(-0.18, 0.06), fontsize=11, color=VERDE, weight="bold",
            arrowprops=dict(arrowstyle="->", color=VERDE))
ax.annotate("< ÷105", xy=(1.30, 0.016), xytext=(1.22, 0.3), fontsize=11, color=ROJO, weight="bold",
            arrowprops=dict(arrowstyle="->", color=ROJO))
ax.set_title("Amplifica la diferencia y rechaza lo común (60 Hz)")
ax.legend(loc="upper left", fontsize=8)
fig.tight_layout(); fig.savefig(IMG / "etapaB_vs_etapaC.png"); plt.close(fig)

# 3) Comparación de CMRR
items = [
    ("Peor caso ±5 %\nsin aparear", db(Ad_teo / acm_wc[5]), GRIS),
    ("Peor caso ±1 %\nsin aparear", db(Ad_teo / acm_wc[3]), GRIS),
    ("Experimental\n(cota inferior)", CMRR_exp, AZUL),
    ("Global estimado\n(TL084 típ.)", cmrr_global(86), NARANJA),
    ("Modelo resistivo\n(apareado)", CMRR_teo, VERDE),
]
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar([i[0] for i in items], [i[1] for i in items], color=[i[2] for i in items])
bars[2].set_hatch("//")
for b, (_, v, _) in zip(bars, items):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.2f} dB", ha="center", fontsize=9)
ax.axhline(89, color=ROJO, ls="--", lw=1)
ax.text(-0.45, 90.2, "IEC 60601-2-25: ≥ 89 dB", color=ROJO, fontsize=8)
ax.set_ylim(0, 105); ax.set_ylabel("CMRR (dB)")
ax.set_title("Razón de rechazo de modo común del circuito armado")
plt.xticks(fontsize=8)
fig.tight_layout(); fig.savefig(IMG / "cmrr_comparacion.png"); plt.close(fig)

# 4) Acm del restador vs tolerancia
e = np.logspace(-4, -1, 200)
fig, ax = plt.subplots(figsize=(7, 4))
ax.loglog(e * 100, 2 * e / (1 - e), color=AZUL, label="Peor caso sin aparear: 2ε/(1−ε)")
ax.axhline(Acm_exp, color=NARANJA, ls="--", lw=1, label=f"Cota experimental: Acm < {Acm_exp:.5f}")
ax.axhline(Acm_teo, color=VERDE, ls="--", lw=1, label=f"Montaje apareado (modelo): {Acm_teo:.7f}")
for t, c in ((1, GRIS), (5, ROJO)):
    a = 2 * t / 100 / (1 - t / 100)
    ax.plot(t, a, "o", color=c); ax.text(t * 1.1, a * 0.7, f"±{t} %: {a:.4f}", fontsize=8, color=c)
ax.set_xlabel("Tolerancia de las resistencias del restador, ε (%)")
ax.set_ylabel("Ganancia de modo común, Acm")
ax.set_title("Por qué se aparean R2a–R2b y R3a–R3b")
ax.legend(fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(IMG / "acm_vs_tolerancia.png"); plt.close(fig)

print(f"\nFiguras guardadas en {IMG.relative_to(ROOT)}/ y tablas en data/")
