"""
Gera um GIF animado da distribuição de santos por categoria/século.
Salva em outputs/figures/animation_categorias.gif

Rodando:
    python generate_gif.py
"""

import os
import io
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image

BASE_DIR  = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "saints_clean.csv")
OUT_PATH  = os.path.join(BASE_DIR, "outputs", "figures", "animation_categorias.gif")

# ── Dados ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
df_anim = df.dropna(subset=["century_of_death"]).copy()
df_anim["century_of_death"] = df_anim["century_of_death"].astype(int)

all_centuries = sorted(df_anim["century_of_death"].unique())
all_cats      = sorted(df_anim["category"].dropna().unique())

COLOR_CATEGORY = {
    "Martyr":    "#f78166",
    "Confessor": "#79c0ff",
    "Doctor":    "#e3b341",
    "Other":     "#8b949e",
}

full_idx = pd.MultiIndex.from_product(
    [all_centuries, all_cats], names=["century_of_death", "category"]
)
df_cat = (
    df_anim.groupby(["century_of_death", "category"]).size()
    .reindex(full_idx, fill_value=0)
    .reset_index(name="count")
)

max_count = df_cat["count"].max() + 2

LAYOUT = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#161b22",
    font=dict(color="#e6edf3", family="'Consolas', 'Courier New', monospace", size=13),
    xaxis=dict(
        gridcolor="#21262d", linecolor="#30363d",
        tickfont=dict(size=13, color="#e6edf3"),
        title_text="Categoria",
        title_font=dict(size=13, color="#8b949e"),
    ),
    yaxis=dict(
        gridcolor="#21262d", linecolor="#30363d",
        tickfont=dict(size=12),
        title_text="Número de Santos",
        title_font=dict(size=13, color="#8b949e"),
        range=[0, max_count],
    ),
    legend=dict(
        bgcolor="#161b22", bordercolor="#30363d", borderwidth=1,
        font=dict(size=12),
        orientation="h", y=-0.18,
    ),
    margin=dict(t=70, b=80, l=70, r=30),
    width=820,
    height=480,
)

# ── Gera um frame PNG por século ───────────────────────────────────────────────
print(f"Gerando {len(all_centuries)} frames...")
frames_pil = []

for c in all_centuries:
    subset = df_cat[df_cat["century_of_death"] == c]

    bars = []
    for cat in all_cats:
        val = subset.loc[subset["category"] == cat, "count"].values
        count = int(val[0]) if len(val) > 0 else 0
        bars.append(go.Bar(
            x=[cat], y=[count],
            name=cat,
            marker_color=COLOR_CATEGORY.get(cat, "#8b949e"),
            marker_line_color="#0d1117",
            marker_line_width=1.5,
            showlegend=True,
        ))

    fig = go.Figure(data=bars)
    fig.update_layout(
        **LAYOUT,
        title=dict(
            text=f"Santos por Categoria  ·  Século <b style='color:#e3b341'>{c}</b>",
            font=dict(size=16, color="#e3b341"),
            x=0.5, xanchor="center",
        ),
        barmode="group",
    )

    img_bytes = pio.to_image(fig, format="png", width=820, height=480, scale=1.5)
    img = Image.open(io.BytesIO(img_bytes))
    frames_pil.append(img)

# Repete o último frame 4× para dar pausa no final
frames_pil += [frames_pil[-1]] * 4

# ── Salva GIF ─────────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
frames_pil[0].save(
    OUT_PATH,
    save_all=True,
    append_images=frames_pil[1:],
    duration=900,       # ms por frame
    loop=0,             # loop infinito
    optimize=True,
)

print(f"✅ GIF salvo em: {OUT_PATH}")
print("   Tamanho:", round(os.path.getsize(OUT_PATH) / 1024), "KB")