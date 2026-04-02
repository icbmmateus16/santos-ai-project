"""
Gera 3 GIFs animados para o README do projeto.
Usa matplotlib puro (sem kaleido).

    python generate_gif.py

Saídas:
    outputs/figures/animation_categorias.gif   — barras por categoria/século
    outputs/figures/animation_linha.gif        — linha acumulada por século
    outputs/figures/animation_bar_race.gif     — corrida de países
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
import numpy as np

BASE_DIR  = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "saints_clean.csv")
OUT_DIR   = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Paleta GitHub Dark ────────────────────────────────────────────────────────
BG    = "#0d1117"
BG2   = "#161b22"
BORDER= "#30363d"
TEXT  = "#e6edf3"
MUTED = "#8b949e"
GOLD  = "#e3b341"
BLUE  = "#58a6ff"
GREEN = "#56d364"
RED   = "#f78166"

COLORS_CAT = {
    "Martyr":    "#f78166",
    "Confessor": "#79c0ff",
    "Doctor":    "#e3b341",
    "Other":     "#8b949e",
}
COLORS_COUNTRY = [
    "#58a6ff","#f78166","#56d364","#e3b341","#bc8cff",
    "#79c0ff","#ffa657","#ff7b72","#d2a8ff","#7ee787",
]

# ── Dados ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
df_anim = df.dropna(subset=["century_of_death"]).copy()
df_anim["century_of_death"] = df_anim["century_of_death"].astype(int)
all_centuries = sorted(df_anim["century_of_death"].unique())
all_cats = [c for c in ["Martyr","Confessor","Doctor","Other"]
            if c in df_anim["category"].unique()]

full_idx = pd.MultiIndex.from_product(
    [all_centuries, all_cats], names=["century_of_death","category"]
)
df_cat = (
    df_anim.groupby(["century_of_death","category"]).size()
    .reindex(full_idx, fill_value=0)
    .reset_index(name="count")
)

def _style_ax(ax):
    ax.set_facecolor(BG2)
    for sp in ax.spines.values():
        sp.set_edgecolor(BORDER); sp.set_linewidth(0.8)
    ax.tick_params(colors=MUTED, labelsize=11)
    ax.grid(color=BORDER, linewidth=0.6, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

# ══════════════════════════════════════════════════════════════════════════════
# GIF 1 — Barras por categoria/século
# ══════════════════════════════════════════════════════════════════════════════
print("▶ GIF 1/3 — Barras por categoria...")

max_count = df_cat["count"].max() + 1
x = np.arange(len(all_cats))

fig1, ax1 = plt.subplots(figsize=(10, 5.5), facecolor=BG)
_style_ax(ax1)
ax1.set_xlim(-0.6, len(all_cats)-0.4)
ax1.set_ylim(0, max_count)
ax1.set_xticks(x)
ax1.set_xticklabels(all_cats, color=TEXT, fontsize=13, fontfamily="monospace")
ax1.set_ylabel("Número de Santos", color=MUTED, fontsize=11, fontfamily="monospace")

t_title1  = fig1.text(0.5, 0.93, "Santos por Categoria", ha="center",
                       color=GOLD, fontsize=16, fontweight="bold", fontfamily="monospace")
t_sec1    = fig1.text(0.5, 0.86, "", ha="center", color=TEXT,
                       fontsize=13, fontfamily="monospace")

bars1 = ax1.bar(x, [0]*len(all_cats), width=0.55,
                color=[COLORS_CAT.get(c, MUTED) for c in all_cats],
                edgecolor=BG, linewidth=1.2, zorder=3)
blabels1 = [ax1.text(xi, 0, "", ha="center", va="bottom",
                     color=TEXT, fontsize=12, fontweight="bold",
                     fontfamily="monospace") for xi in x]
for cat in all_cats:
    ax1.plot([], [], color=COLORS_CAT.get(cat, MUTED), lw=8, label=cat)
ax1.legend(loc="upper right", frameon=True, facecolor=BG, edgecolor=BORDER,
           labelcolor=TEXT, fontsize=11, handlelength=1.2)
fig1.tight_layout(rect=[0,0.02,1,0.84])

frames1 = list(all_centuries) + [all_centuries[-1]]*5

def update1(century):
    sub = df_cat[df_cat["century_of_death"]==century]
    counts = [int(sub.loc[sub["category"]==c,"count"].values[0])
               if c in sub["category"].values else 0 for c in all_cats]
    for bar, h in zip(bars1, counts): bar.set_height(h)
    for lbl, xi, h in zip(blabels1, x, counts):
        lbl.set_position((xi, h+0.05)); lbl.set_text(str(h) if h>0 else "")
    t_sec1.set_text(f"Século {century}")
    return bars1

ani1 = animation.FuncAnimation(fig1, update1, frames=frames1, interval=850, blit=False)
ani1.save(os.path.join(OUT_DIR,"animation_categorias.gif"),
          writer=animation.PillowWriter(fps=1.15), dpi=130)
plt.close(fig1)
print(f"   ✅ animation_categorias.gif")

# ══════════════════════════════════════════════════════════════════════════════
# GIF 2 — Linha acumulada por século
# ══════════════════════════════════════════════════════════════════════════════
print("▶ GIF 2/3 — Linha acumulada...")

df_line = (df_anim.groupby(["century_of_death","category"])
           .size().reset_index(name="count"))
df_total = df_anim.groupby("century_of_death").size().reset_index(name="total")
df_total = df_total.sort_values("century_of_death")
centuries_l = df_total["century_of_death"].tolist()
totals_l    = df_total["total"].tolist()

# Acumulado por categoria
cat_acc = {}
for cat in all_cats:
    s = df_line[df_line["category"]==cat].set_index("century_of_death")["count"]
    s = s.reindex(centuries_l, fill_value=0)
    cat_acc[cat] = s.cumsum().tolist()

fig2, ax2 = plt.subplots(figsize=(10, 5.5), facecolor=BG)
_style_ax(ax2)
ax2.set_xlim(centuries_l[0]-0.5, centuries_l[-1]+0.5)
ax2.set_ylim(0, max(c for vals in cat_acc.values() for c in vals)*1.12)
ax2.set_xlabel("Século", color=MUTED, fontsize=11, fontfamily="monospace")
ax2.set_ylabel("Santos acumulados", color=MUTED, fontsize=11, fontfamily="monospace")
ax2.set_xticks(centuries_l)
ax2.set_xticklabels([str(c) for c in centuries_l], rotation=45, color=MUTED, fontsize=9)

fig2.text(0.5, 0.93, "Santos Acumulados por Categoria",
          ha="center", color=GOLD, fontsize=16,
          fontweight="bold", fontfamily="monospace")
t_sec2 = fig2.text(0.5, 0.86, "", ha="center", color=TEXT,
                    fontsize=13, fontfamily="monospace")

lines2, dots2, area_fills = {}, {}, {}
for cat in all_cats:
    color = COLORS_CAT.get(cat, MUTED)
    line, = ax2.plot([], [], color=color, lw=2.5, label=cat, zorder=4)
    dot,  = ax2.plot([], [], "o", color=color, ms=7, zorder=5)
    lines2[cat] = line
    dots2[cat]  = dot

ax2.legend(loc="upper left", frameon=True, facecolor=BG, edgecolor=BORDER,
           labelcolor=TEXT, fontsize=11, handlelength=1.5)
fig2.tight_layout(rect=[0,0.02,1,0.84])

frames2 = list(range(1, len(centuries_l)+1)) + [len(centuries_l)]*5

def update2(n):
    cxs = centuries_l[:n]
    for cat in all_cats:
        ys = cat_acc[cat][:n]
        lines2[cat].set_data(cxs, ys)
        if n > 0:
            dots2[cat].set_data([cxs[-1]], [ys[-1]])
    t_sec2.set_text(f"Até o século {centuries_l[n-1]}" if n>0 else "")
    return list(lines2.values()) + list(dots2.values())

ani2 = animation.FuncAnimation(fig2, update2, frames=frames2, interval=700, blit=False)
ani2.save(os.path.join(OUT_DIR,"animation_linha.gif"),
          writer=animation.PillowWriter(fps=1.3), dpi=130)
plt.close(fig2)
print(f"   ✅ animation_linha.gif")

# ══════════════════════════════════════════════════════════════════════════════
# GIF 3 — Bar chart race: corrida de países
# ══════════════════════════════════════════════════════════════════════════════
print("▶ GIF 3/3 — Bar chart race de países...")

TOP_N = 10

# Acumulado de santos por país até cada século
rows = []
all_countries = df_anim["origin_country"].dropna().unique()
for c in all_centuries:
    sub = df_anim[df_anim["century_of_death"] <= c]
    counts = sub["origin_country"].value_counts()
    for country in all_countries:
        rows.append({"century": c, "country": country,
                     "count": int(counts.get(country, 0))})
df_race = pd.DataFrame(rows)

# Atribui cor fixa por país (top países do último século)
top_final = (df_race[df_race["century"]==all_centuries[-1]]
             .nlargest(TOP_N, "count")["country"].tolist())
country_colors = {c: COLORS_COUNTRY[i % len(COLORS_COUNTRY)]
                  for i, c in enumerate(top_final)}

fig3, ax3 = plt.subplots(figsize=(10, 6), facecolor=BG)
_style_ax(ax3)
ax3.set_facecolor(BG)
for sp in ax3.spines.values(): sp.set_visible(False)
ax3.tick_params(left=False, bottom=False)
ax3.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,_: f"{int(x)}"))

fig3.text(0.5, 0.94, "Corrida de Países · Santos Acumulados",
          ha="center", color=GOLD, fontsize=16,
          fontweight="bold", fontfamily="monospace")
t_sec3 = fig3.text(0.98, 0.02, "", ha="right", color=GOLD,
                    fontsize=22, fontweight="bold", fontfamily="monospace",
                    alpha=0.35)
fig3.tight_layout(rect=[0,0.02,1,0.90])

frames3 = list(all_centuries) + [all_centuries[-1]]*6

def update3(century):
    ax3.clear()
    ax3.set_facecolor(BG)
    for sp in ax3.spines.values(): sp.set_visible(False)
    ax3.tick_params(left=False, bottom=False, colors=MUTED, labelsize=11)
    ax3.grid(axis="x", color=BORDER, linewidth=0.6, linestyle="--", alpha=0.5)
    ax3.set_axisbelow(True)
    ax3.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,_: f"{int(x)}"))

    sub = df_race[df_race["century"]==century].nlargest(TOP_N,"count")
    sub = sub.sort_values("count", ascending=True)

    colors = [country_colors.get(c, MUTED) for c in sub["country"]]
    bars = ax3.barh(sub["country"], sub["count"],
                    color=colors, edgecolor=BG, linewidth=0.8,
                    height=0.75)

    # Valor dentro da barra
    for bar, val in zip(bars, sub["count"]):
        if val > 0:
            ax3.text(val - 0.15, bar.get_y() + bar.get_height()/2,
                     f"  {int(val)}", va="center", ha="right" if val>2 else "left",
                     color=BG if val>2 else TEXT, fontsize=11,
                     fontweight="bold", fontfamily="monospace")

    ax3.set_yticks(range(len(sub)))
    ax3.set_yticklabels(sub["country"], color=TEXT,
                         fontsize=11, fontfamily="monospace")
    ax3.set_xlim(0, df_race["count"].max() * 1.12)
    t_sec3.set_text(f"Séc. {century}")

ani3 = animation.FuncAnimation(fig3, update3, frames=frames3, interval=900, blit=False)
ani3.save(os.path.join(OUT_DIR,"animation_bar_race.gif"),
          writer=animation.PillowWriter(fps=1.1), dpi=130)
plt.close(fig3)
print(f"   ✅ animation_bar_race.gif")

print("\n🎉 Todos os GIFs gerados em outputs/figures/")