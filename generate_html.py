"""
Injeta gráficos animados + melhorias visuais no apresentacao/index.html.

Rodando:
    python generate_html.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

BASE_DIR  = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "saints_clean.csv")
HTML_PATH = os.path.join(BASE_DIR, "apresentacao", "index.html")

# ── Dados ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
df_anim = df.dropna(subset=["century_of_death"]).copy()
df_anim["century_of_death"] = df_anim["century_of_death"].astype(int)
df_anim = df_anim.sort_values("century_of_death")

all_centuries = sorted(df_anim["century_of_death"].unique())
all_cats      = sorted(df_anim["category"].dropna().unique())
continents    = sorted(df_anim["continent"].dropna().unique())

# Estatísticas para o terminal
n_total      = len(df)
n_paises     = df["origin_country"].nunique()
media_anos   = int(df["years_to_canonization"].mean())
mais_demorou = df.loc[df["years_to_canonization"].idxmax(), "name"]
mais_rapido  = df.loc[df["years_to_canonization"].idxmin(), "name"]
top_pais     = df["origin_country"].value_counts().idxmax()
top_cat      = df["category"].value_counts().idxmax()

# ── Cores: GitHub Dark com toque dourado ─────────────────────────────────────
COLOR_CATEGORY = {
    "Martyr":    "#f78166",
    "Confessor": "#79c0ff",
    "Doctor":    "#e3b341",
    "Other":     "#8b949e",
}
COLOR_CONTINENT = {
    "Europe":        "#58a6ff",
    "Asia":          "#f78166",
    "Africa":        "#e3b341",
    "North America": "#56d364",
    "South America": "#bc8cff",
}

PLOT_LAYOUT = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#161b22",
    font=dict(color="#e6edf3", family="'Consolas', 'Courier New', monospace"),
    title_font=dict(size=16, color="#e3b341"),
    legend=dict(
        bgcolor="#161b22", bordercolor="#30363d", borderwidth=1,
        font=dict(family="'Segoe UI', sans-serif", size=12),
    ),
    xaxis=dict(
        gridcolor="#21262d", linecolor="#30363d", tickcolor="#8b949e",
        title_font=dict(size=12, color="#8b949e"),
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor="#21262d", linecolor="#30363d", tickcolor="#8b949e",
        title_font=dict(size=12, color="#8b949e"),
        tickfont=dict(size=11),
    ),
    margin=dict(t=60, b=50, l=60, r=30),
    hoverlabel=dict(
        bgcolor="#161b22", bordercolor="#30363d",
        font_color="#e6edf3", font_family="'Segoe UI', sans-serif",
    ),
    height=460,
)

def set_speed(fig, frame_ms=1000, trans_ms=700):
    try:
        b = fig.layout.updatemenus[0].buttons[0]
        b.args[1]["frame"]["duration"]      = frame_ms
        b.args[1]["transition"]["duration"] = trans_ms
    except Exception:
        pass

# ── Gráfico 1: Categorias por século ─────────────────────────────────────────
full_idx = pd.MultiIndex.from_product(
    [all_centuries, all_cats], names=["century_of_death", "category"]
)
df_cat = (
    df_anim.groupby(["century_of_death", "category"]).size()
    .reindex(full_idx, fill_value=0)
    .reset_index(name="count")
)

fig1 = px.bar(
    df_cat, x="category", y="count",
    animation_frame="century_of_death",
    color="category", color_discrete_map=COLOR_CATEGORY,
    title="Distribuição de Santos por Categoria · por Século",
    labels={"count": "Santos", "category": "Categoria", "century_of_death": "Século"},
    range_y=[0, df_cat["count"].max() + 2],
    category_orders={"category": all_cats},
)
fig1.update_layout(**PLOT_LAYOUT)
fig1.update_traces(
    marker_line_color="#0d1117", marker_line_width=1.5,
    hovertemplate="<b>%{x}</b><br>%{y} santos<extra></extra>",
)
for frame in fig1.frames:
    for d in frame.data:
        d.marker.line.color = "#0d1117"
        d.marker.line.width = 1.5
set_speed(fig1)

# ── Gráfico 2: Continentes acumulado ─────────────────────────────────────────
rows = []
for c in all_centuries:
    for cont in continents:
        total = len(df_anim[(df_anim["century_of_death"] <= c) & (df_anim["continent"] == cont)])
        rows.append({"Século": c, "Continente": cont, "Total": total})
df_cum = pd.DataFrame(rows)

fig2 = px.bar(
    df_cum, x="Continente", y="Total",
    animation_frame="Século",
    color="Continente", color_discrete_map=COLOR_CONTINENT,
    title="Santos por Continente · Total Acumulado até o Século",
    range_y=[0, df_cum["Total"].max() + 3],
)
fig2.update_layout(**PLOT_LAYOUT)
fig2.update_traces(
    marker_line_color="#0d1117", marker_line_width=1.5,
    hovertemplate="<b>%{x}</b><br>%{y} santos acumulados<extra></extra>",
)
for frame in fig2.frames:
    for d in frame.data:
        d.marker.line.color = "#0d1117"
        d.marker.line.width = 1.5
set_speed(fig2)

# ── Gráfico 3: Scatter cumulativo animado — Anos até canonização ──────────────
df_sc = df_anim.dropna(subset=["years_to_canonization", "death_year"]).copy()
df_sc["death_year"] = df_sc["death_year"].astype(int)
mediana = int(df_sc["years_to_canonization"].median())

sc_centuries = sorted(df_sc["century_of_death"].unique())

def _scatter_traces(subset):
    traces = []
    for cat in all_cats:
        s = subset[subset["category"] == cat]
        traces.append(go.Scatter(
            x=s["death_year"].tolist(),
            y=s["years_to_canonization"].tolist(),
            mode="markers+text",
            name=cat,
            text=s["name"].tolist(),
            textposition="top center",
            textfont=dict(size=8, color="rgba(230,237,243,0.50)"),
            marker=dict(
                color=COLOR_CATEGORY.get(cat, "#8b949e"),
                size=10,
                line=dict(color="#0d1117", width=1),
                opacity=0.85,
            ),
            customdata=list(zip(
                s["origin_country"].fillna("—"),
                s["canonization_year"].fillna("—"),
                s["century_of_death"].astype(int),
            )),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Morte: %{x} d.C.<br>"
                "Anos até canonização: %{y}<br>"
                "País: %{customdata[0]}<br>"
                "Canonizado em: %{customdata[1]}<br>"
                "Século: %{customdata[2]}<extra></extra>"
            ),
        ))
    return traces

# Frame inicial vazio + frames cumulativos
frames = []
for c in sc_centuries:
    subset = df_sc[df_sc["century_of_death"] <= c]
    frames.append(go.Frame(data=_scatter_traces(subset), name=str(c)))

fig3 = go.Figure(
    data=_scatter_traces(df_sc[df_sc["century_of_death"] <= sc_centuries[0]]),
    frames=frames,
)

# Linha mediana
fig3.add_hline(
    y=mediana, line_dash="dash", line_color="#8b949e", line_width=1,
    annotation_text=f"  mediana = {mediana} anos",
    annotation_font=dict(color="#8b949e", size=11),
    annotation_position="right",
)

# Play / pause + slider
fig3.update_layout(
    **PLOT_LAYOUT,
    title="Anos até Canonização × Ano de Morte · Acumulado por Século",
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        y=1.15, x=0.0, xanchor="left",
        buttons=[
            dict(label="▶ Play", method="animate",
                 args=[None, {"frame": {"duration": 1000, "redraw": True},
                              "transition": {"duration": 700},
                              "fromcurrent": True}]),
            dict(label="⏸ Pause", method="animate",
                 args=[[None], {"frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0}}]),
        ],
        bgcolor="#21262d", bordercolor="#30363d",
        font=dict(color="#e6edf3", size=12),
    )],
    sliders=[dict(
        active=0,
        steps=[dict(method="animate", args=[[str(c)],
                    {"frame": {"duration": 1000, "redraw": True},
                     "mode": "immediate", "transition": {"duration": 700}}],
                    label=f"Séc. {c}") for c in sc_centuries],
        x=0, y=0, len=1.0,
        bgcolor="#21262d", bordercolor="#30363d",
        tickcolor="#8b949e",
        font=dict(color="#8b949e", size=10),
        currentvalue=dict(
            prefix="até o século: ", font=dict(color="#e3b341", size=13),
            visible=True, xanchor="center",
        ),
        pad=dict(t=40),
    )],
)
fig3.update_xaxes(title_text="Ano de Morte (d.C.)", dtick=200)
fig3.update_yaxes(title_text="Anos até Canonização")

# ── Serializa com div IDs fixos ───────────────────────────────────────────────
div1 = pio.to_html(fig1, full_html=False, include_plotlyjs=True,  div_id="graf-cat")
div2 = pio.to_html(fig2, full_html=False, include_plotlyjs=False, div_id="graf-cont")
div3 = pio.to_html(fig3, full_html=False, include_plotlyjs=False, div_id="graf-scatter")

# ── CSS extra injetado no <head> do index.html ────────────────────────────────
CSS_EXTRA = """
<style id="tech-overlay">
  /* Monospace / tech elements */
  .section-tag { font-family: 'Consolas','Courier New',monospace; }
  .section-tag::before { content: '$ '; opacity: 0.5; }

  /* Terminal box */
  .terminal {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 0;
    margin-bottom: 48px;
    overflow: hidden;
    font-family: 'Consolas','Courier New',monospace;
  }
  .terminal-bar {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .terminal-dot { width: 12px; height: 12px; border-radius: 50%; }
  .terminal-title { font-size: 12px; color: #8b949e; margin-left: 8px; }
  .terminal-body { padding: 20px 24px; font-size: 13px; line-height: 2; color: #e6edf3; }
  .t-prompt { color: #56d364; }
  .t-cmd    { color: #79c0ff; }
  .t-key    { color: #e3b341; }
  .t-val    { color: #f78166; }
  .t-str    { color: #a5d6ff; }
  .t-cmt    { color: #8b949e; }

  /* Speed control */
  .speed-control {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 20px; flex-wrap: wrap;
  }
  .speed-label {
    font-size: 12px; color: #8b949e;
    font-family: 'Consolas','Courier New',monospace;
    margin-right: 4px;
  }
  .speed-btn {
    padding: 5px 14px; border-radius: 6px; font-size: 12px; font-weight: 600;
    cursor: pointer; border: 1px solid #30363d; background: #21262d; color: #8b949e;
    transition: all 0.15s; font-family: 'Consolas','Courier New',monospace;
  }
  .speed-btn:hover { border-color: #C9A84C; color: #e6edf3; }
  .speed-btn.active { background: #1f2d1f; border-color: #56d364; color: #56d364; }

  /* Anim tabs */
  .anim-tabs {
    display: flex; gap: 0; margin-bottom: 24px;
    border-bottom: 1px solid #30363d;
  }
  .anim-tab {
    padding: 10px 20px; cursor: pointer; font-size: 13px; font-weight: 600;
    color: #8b949e; border: none; background: none;
    border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s;
    font-family: 'Consolas','Courier New',monospace;
  }
  .anim-tab:hover { color: #e6edf3; }
  .anim-tab.active { color: #e3b341; border-bottom-color: #C9A84C; }
  .anim-panel { display: none; }
  .anim-panel.active { display: block; }

  .anim-desc {
    font-size: 12px; color: #8b949e;
    margin-bottom: 16px; padding: 10px 14px;
    background: #161b22; border-left: 3px solid #30363d;
    border-radius: 0 6px 6px 0;
    font-family: 'Consolas','Courier New',monospace;
  }
  .anim-desc::before { content: '// '; color: #30363d; }
</style>
"""

# ── Seção de gráficos animados ────────────────────────────────────────────────
NOVA_SECAO = f"""
<!-- GRAFICOS ANIMADOS (gerado por generate_html.py) -->
<div class="full-bg" id="graficos-animados">
  <div class="inner">
    <span class="section-tag">animated_charts.py</span>
    <h2>Gráficos Interativos & Animados</h2>
    <p class="section-desc">Dados em movimento — cada frame é um século da história da Igreja Católica.</p>
    <div class="divider"></div>

    <!-- Terminal com stats -->
    <div class="terminal">
      <div class="terminal-bar">
        <span class="terminal-dot" style="background:#ff5f56"></span>
        <span class="terminal-dot" style="background:#ffbd2e"></span>
        <span class="terminal-dot" style="background:#27c93f"></span>
        <span class="terminal-title">python · santos_ai_project · dataset_stats.py</span>
      </div>
      <div class="terminal-body">
        <div><span class="t-prompt">❯ </span><span class="t-cmd">python</span> <span class="t-str">dataset_stats.py</span></div>
        <div style="margin-top:8px">
          <span class="t-key">total_santos</span>     <span class="t-cmt">=</span> <span class="t-val">{n_total}</span>
        </div>
        <div><span class="t-key">paises_origem</span>    <span class="t-cmt">=</span> <span class="t-val">{n_paises}</span></div>
        <div><span class="t-key">media_canonizacao</span> <span class="t-cmt">=</span> <span class="t-val">{media_anos}</span> <span class="t-cmt"># anos após a morte</span></div>
        <div><span class="t-key">mais_demorou</span>     <span class="t-cmt">=</span> <span class="t-str">"{mais_demorou}"</span></div>
        <div><span class="t-key">mais_rapido</span>      <span class="t-cmt">=</span> <span class="t-str">"{mais_rapido}"</span></div>
        <div><span class="t-key">top_pais</span>         <span class="t-cmt">=</span> <span class="t-str">"{top_pais}"</span></div>
        <div><span class="t-key">top_categoria</span>    <span class="t-cmt">=</span> <span class="t-str">"{top_cat}"</span></div>
        <div style="margin-top:8px"><span class="t-cmt"># ✅ dataset loaded — ready to plot</span></div>
      </div>
    </div>

    <!-- Controle de velocidade -->
    <div class="speed-control">
      <span class="speed-label">animation.speed =</span>
      <button id="speed-lento"  class="speed-btn" onclick="setSpeed('lento')">🐢 devagar</button>
      <button id="speed-normal" class="speed-btn active" onclick="setSpeed('normal')">▶ normal</button>
      <button id="speed-rapido" class="speed-btn" onclick="setSpeed('rapido')">⚡ rápido</button>
    </div>

    <!-- Abas -->
    <div class="anim-tabs">
      <button class="anim-tab active" onclick="switchAnim('cat',this)"># categorias</button>
      <button class="anim-tab" onclick="switchAnim('cont',this)"># continentes</button>
      <button class="anim-tab" onclick="switchAnim('scatter',this)"># anos_ate_canonizacao</button>
    </div>

    <div id="anim-cat" class="anim-panel active">
      <div class="anim-desc">Mártires dominam os primeiros séculos (perseguições romanas). Confessores e Doutores crescem com a consolidação da Igreja medieval.</div>
      {div1}
    </div>
    <div id="anim-cont" class="anim-panel">
      <div class="anim-desc">Total acumulado de santos por continente até cada século. Europa = 74% do total. Clique em ▶ para ver a evolução.</div>
      {div2}
    </div>
    <div id="anim-scatter" class="anim-panel">
      <div class="anim-desc">Todos os 77 santos. Eixo Y = anos entre a morte e a canonização. Linha tracejada = mediana. Tamanho = temas de padroado. Hover para ver nome e detalhes.</div>
      {div3}
    </div>
  </div>
</div>

<script>
  /* ── Controle de velocidade das animações ─────────────────────── */
  const SPEEDS = {{ lento: 2200, normal: 1000, rapido: 350 }};
  let currentSpeed = 1000;

  function setSpeed(name) {{
    currentSpeed = SPEEDS[name];
    const trans  = Math.round(currentSpeed * 0.7);
    ['graf-cat', 'graf-cont', 'graf-scatter'].forEach(id => {{
      const gd = document.getElementById(id);
      if (!gd || !gd.layout || !gd.layout.updatemenus) return;
      const menus = JSON.parse(JSON.stringify(gd.layout.updatemenus));
      if (menus[0] && menus[0].buttons && menus[0].buttons[0]) {{
        menus[0].buttons[0].args[1].frame.duration      = currentSpeed;
        menus[0].buttons[0].args[1].transition.duration = trans;
      }}
      Plotly.relayout(id, {{ updatemenus: menus }});
    }});
    document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('speed-' + name).classList.add('active');
  }}

  /* ── Troca de aba ─────────────────────────────────────────────── */
  function switchAnim(id, btn) {{
    document.querySelectorAll('.anim-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.anim-tab').forEach(t  => t.classList.remove('active'));
    document.getElementById('anim-' + id).classList.add('active');
    btn.classList.add('active');
  }}
</script>
<!-- /GRAFICOS ANIMADOS -->
"""

# ── Injeta no HTML existente ──────────────────────────────────────────────────
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Remove versão anterior dos gráficos animados
MARCA_INI = "<!-- GRAFICOS ANIMADOS"
MARCA_FIM = "<!-- /GRAFICOS ANIMADOS -->"
if MARCA_INI in html:
    ini = html.index(MARCA_INI)
    fim = html.index(MARCA_FIM) + len(MARCA_FIM)
    html = html[:ini] + html[fim:]

# Remove CSS extra anterior
if '<style id="tech-overlay">' in html:
    ini = html.index('<style id="tech-overlay">')
    fim = html.index("</style>", ini) + len("</style>")
    html = html[:ini] + html[fim:]

# Injeta CSS no </head>
html = html.replace("</head>", CSS_EXTRA + "\n</head>", 1)

# Injeta seção antes de "Descobertas"
ANCORA = '<div class="full-bg">\n  <div class="inner">\n    <span class="section-tag">Descobertas</span>'
if ANCORA in html:
    html = html.replace(ANCORA, NOVA_SECAO + "\n\n" + ANCORA, 1)
else:
    html = html.replace("<footer>", NOVA_SECAO + "\n\n<footer>", 1)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Gerado: {HTML_PATH}")
print("   Abra apresentacao/index.html no navegador.")