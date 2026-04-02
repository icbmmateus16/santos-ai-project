import os
import re
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Santos Católicos AI", layout="wide")
st.title("Santos Católicos — Análise de Dados")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "processed", "saints_clean.csv")


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# CHAT — motor de respostas gratuito (pandas puro)
# ─────────────────────────────────────────────────────────────────────────────

def responder(pergunta: str, dataframe: pd.DataFrame) -> str:
    p = pergunta.lower().strip()
    p = re.sub(r"[áàãâä]", "a", p)
    p = re.sub(r"[éèêë]", "e", p)
    p = re.sub(r"[íìîï]", "i", p)
    p = re.sub(r"[óòõôö]", "o", p)
    p = re.sub(r"[úùûü]", "u", p)
    p = re.sub(r"[ç]", "c", p)

    # ── Quantos santos existem no total ──────────────────────────────────────
    if re.search(r"quantos santos|total de santos|quantos ha|quantos tem", p):
        return f"O dataset possui **{len(dataframe)} santos** católicos."

    # ── Santo que mais demorou para ser canonizado ────────────────────────────
    if re.search(r"mais demorou|maior tempo|mais anos|demorou mais|mais longe", p):
        row = dataframe.loc[dataframe["years_to_canonization"].idxmax()]
        return (
            f"O santo que mais demorou foi **{row['name']}** ({row['origin_country']}), "
            f"com **{int(row['years_to_canonization'])} anos** entre a morte ({int(row['death_year'])}) "
            f"e a canonização ({int(row['canonization_year'])})."
        )

    # ── Santo que menos demorou para ser canonizado ───────────────────────────
    if re.search(r"menos demorou|menor tempo|menos anos|mais rapido|rapidez", p):
        row = dataframe.loc[dataframe["years_to_canonization"].idxmin()]
        return (
            f"O santo canonizado mais rápido foi **{row['name']}** ({row['origin_country']}), "
            f"com apenas **{int(row['years_to_canonization'])} ano(s)** após a morte."
        )

    # ── Santo mais antigo ─────────────────────────────────────────────────────
    if re.search(r"mais antigo|primeiro santo|santo mais velho|mais antigos", p):
        row = dataframe.loc[dataframe["death_year"].idxmin()]
        return (
            f"O santo mais antigo é **{row['name']}** ({row['origin_country']}), "
            f"que morreu em **{int(row['death_year'])} d.C.**"
        )

    # ── Santo mais recente ────────────────────────────────────────────────────
    if re.search(r"mais recente|ultimo santo|canonizado recente|moderno", p):
        row = dataframe.loc[dataframe["canonization_year"].idxmax()]
        return (
            f"O santo canonizado mais recentemente é **{row['name']}** ({row['origin_country']}), "
            f"canonizado em **{int(row['canonization_year'])}**."
        )

    # ── Quantos santos por categoria ─────────────────────────────────────────
    if re.search(r"categoria|martir|confessor|doutor|doctor|tipos de santo", p):
        counts = dataframe["category"].value_counts()
        linhas = "\n".join([f"- **{cat}**: {n} santos" for cat, n in counts.items()])
        media = dataframe.groupby("category")["years_to_canonization"].mean().dropna()
        media_txt = "\n".join([f"  - {cat}: média de {int(v)} anos" for cat, v in media.items()])
        return (
            f"O dataset tem as seguintes categorias:\n{linhas}\n\n"
            f"Média de anos para canonização por categoria:\n{media_txt}"
        )

    # ── Quantos santos por continente ────────────────────────────────────────
    if re.search(r"continente|europa|asia|africa|america", p):
        counts = dataframe["continent"].value_counts()
        linhas = "\n".join([f"- **{cont}**: {n} santos ({n/len(dataframe)*100:.1f}%)" for cont, n in counts.items()])
        return f"Distribuição por continente:\n{linhas}"

    # ── Países ────────────────────────────────────────────────────────────────
    if re.search(r"pais|paises|origem|italia|franca|espanha|portugal", p):
        counts = dataframe["origin_country"].value_counts().head(10)
        linhas = "\n".join([f"- **{pais}**: {n} santos" for pais, n in counts.items()])
        return f"Top 10 países de origem:\n{linhas}"

    # ── Média de anos para canonização ───────────────────────────────────────
    if re.search(r"media|average|canonizacao|quanto tempo|anos para", p):
        media = dataframe["years_to_canonization"].mean()
        mediana = dataframe["years_to_canonization"].median()
        return (
            f"Em média, um santo leva **{int(media)} anos** para ser canonizado após a morte.\n\n"
            f"A mediana é de **{int(mediana)} anos** (metade acima, metade abaixo desse valor)."
        )

    # ── Ordens religiosas ─────────────────────────────────────────────────────
    if re.search(r"ordem|beneditino|franciscan|jesui|dominican|carmelita", p):
        ordens = dataframe["religious_order"].dropna()
        ordens = ordens[ordens != "None"].value_counts().head(8)
        linhas = "\n".join([f"- **{o}**: {n} santos" for o, n in ordens.items()])
        return f"Principais ordens religiosas:\n{linhas}"

    # ── Papas que mais canonizaram ────────────────────────────────────────────
    if re.search(r"papa|canonizou|quem canonizou|pontifice", p):
        papas = dataframe["canonizing_pope"].dropna()
        papas = papas[papas != "Pre-Congregation"].value_counts().head(8)
        linhas = "\n".join([f"- **Papa {p}**: {n} canonizações" for p, n in papas.items()])
        return f"Papas que mais canonizaram santos:\n{linhas}"

    # ── Busca por nome de santo ───────────────────────────────────────────────
    palavras = p.split()
    for palavra in palavras:
        if len(palavra) > 3:
            encontrados = dataframe[dataframe["name"].str.lower().str.contains(palavra, na=False)]
            if not encontrados.empty:
                santo = encontrados.iloc[0]
                ytc = f"{int(santo['years_to_canonization'])} anos" if pd.notna(santo["years_to_canonization"]) else "desconhecido"
                ordem = santo["religious_order"] if pd.notna(santo["religious_order"]) and santo["religious_order"] != "None" else "nenhuma"
                padroeiro = santo["patron_topics"] if pd.notna(santo["patron_topics"]) else "não registrado"
                return (
                    f"**{santo['name']}** — {santo['category']} de {santo['origin_country']} ({santo['continent']})\n\n"
                    f"- Morte: {int(santo['death_year'])} d.C.\n"
                    f"- Canonização: {int(santo['canonization_year'])}\n"
                    f"- Tempo até canonização: {ytc}\n"
                    f"- Ordem religiosa: {ordem}\n"
                    f"- Padroeiro de: {padroeiro}"
                )

    # ── Ajuda ─────────────────────────────────────────────────────────────────
    if re.search(r"ajuda|help|o que|como usar|comandos|perguntas", p):
        return (
            "Posso responder perguntas como:\n\n"
            "- *Quantos santos existem no dataset?*\n"
            "- *Qual santo demorou mais para ser canonizado?*\n"
            "- *Qual é o santo mais antigo?*\n"
            "- *Quantos santos há por continente?*\n"
            "- *Quais são as categorias de santos?*\n"
            "- *Quais ordens religiosas aparecem mais?*\n"
            "- *Quais papas mais canonizaram?*\n"
            "- *Me fale sobre São Pedro* (busca por nome)\n"
            "- *Qual é a média de anos para canonização?*"
        )

    # ── Fallback ──────────────────────────────────────────────────────────────
    return (
        "Não encontrei uma resposta específica para isso. Tente perguntas como:\n"
        "- *Qual santo demorou mais?*\n"
        "- *Quantos santos há por continente?*\n"
        "- *Me fale sobre São Francisco*\n\n"
        "Digite **ajuda** para ver todas as perguntas disponíveis."
    )


# ─────────────────────────────────────────────────────────────────────────────
# ABAS
# ─────────────────────────────────────────────────────────────────────────────
tab_chat, tab_graphs, tab_explorer = st.tabs(
    ["💬 Chat com os Santos", "📊 Gráficos Animados", "🔍 Explorador de Santos"]
)

# ── TAB 1: CHAT ───────────────────────────────────────────────────────────────
with tab_chat:
    st.header("Chat com os Santos")
    st.markdown("Faça perguntas sobre o dataset — 100% gratuito, sem API externa.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ex: Qual santo demorou mais para ser canonizado?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        answer = responder(prompt, df)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

    if st.session_state.messages and st.button("🗑️ Limpar conversa"):
        st.session_state.messages = []
        st.rerun()


# ── TAB 2: GRÁFICOS ANIMADOS ──────────────────────────────────────────────────
with tab_graphs:
    st.header("Gráficos Animados")

    chart_choice = st.selectbox(
        "Escolha o gráfico:",
        [
            "Categorias por Século (barras animadas)",
            "Santos por Continente — acumulado por século",
            "Morte × Canonização por Século",
        ],
    )

    df_anim = df.dropna(subset=["century_of_death"]).copy()
    df_anim["century_of_death"] = df_anim["century_of_death"].astype(int)
    df_anim = df_anim.sort_values("century_of_death")

    COLOR_CATEGORY = {
        "Martyr": "#C0392B",
        "Confessor": "#2980B9",
        "Doctor": "#F39C12",
        "Other": "#7F8C8D",
    }
    COLOR_CONTINENT = {
        "Europe": "#3498DB",
        "Asia": "#E74C3C",
        "Africa": "#F39C12",
        "North America": "#2ECC71",
        "South America": "#9B59B6",
    }

    if chart_choice == "Categorias por Século (barras animadas)":
        df_cat = df_anim.groupby(["century_of_death", "category"]).size().reset_index(name="count")
        fig = px.bar(
            df_cat,
            x="category", y="count",
            animation_frame="century_of_death",
            color="category", color_discrete_map=COLOR_CATEGORY,
            title="Santos por Categoria em cada Século",
            labels={"count": "Número de Santos", "category": "Categoria", "century_of_death": "Século"},
            range_y=[0, df_cat["count"].max() + 2],
        )
        fig.update_layout(height=520, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Pressione ▶ para animar. Cada frame é um século.")

    elif chart_choice == "Santos por Continente — acumulado por século":
        centuries = sorted(df_anim["century_of_death"].unique())
        continents = sorted(df_anim["continent"].dropna().unique())
        rows = []
        for c in centuries:
            for cont in continents:
                total = len(df_anim[(df_anim["century_of_death"] <= c) & (df_anim["continent"] == cont)])
                rows.append({"Século": c, "Continente": cont, "Total acumulado": total})
        df_cum = pd.DataFrame(rows)
        fig = px.bar(
            df_cum,
            x="Continente", y="Total acumulado",
            animation_frame="Século",
            color="Continente", color_discrete_map=COLOR_CONTINENT,
            title="Total Acumulado de Santos por Continente (até cada século)",
            range_y=[0, df_cum["Total acumulado"].max() + 3],
        )
        fig.update_layout(height=520, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Mostra quantos santos de cada continente existiam até aquele século.")

    elif chart_choice == "Morte × Canonização por Século":
        df_sc = df_anim.dropna(subset=["years_to_canonization"]).copy()
        fig = px.scatter(
            df_sc,
            x="death_year", y="canonization_year",
            animation_frame="century_of_death",
            color="category", size="num_patron_topics",
            hover_name="name",
            hover_data={"origin_country": True, "years_to_canonization": True, "century_of_death": False},
            color_discrete_map=COLOR_CATEGORY,
            title="Ano de Morte × Ano de Canonização (por século)",
            labels={
                "death_year": "Ano de Morte",
                "canonization_year": "Ano de Canonização",
                "century_of_death": "Século",
            },
        )
        fig.update_layout(height=520)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Tamanho do ponto = número de temas de padroado. Passe o mouse para ver o nome.")


# ── TAB 3: EXPLORADOR ─────────────────────────────────────────────────────────
with tab_explorer:
    st.header("Explorador de Santos")

    col1, col2, col3 = st.columns(3)
    with col1:
        cats = sorted(df["category"].dropna().unique())
        cat_filter = st.multiselect("Categoria", cats, default=cats)
    with col2:
        conts = sorted(df["continent"].dropna().unique())
        cont_filter = st.multiselect("Continente", conts, default=conts)
    with col3:
        c_min, c_max = int(df["century_of_death"].min()), int(df["century_of_death"].max())
        century_range = st.slider("Século de Morte", c_min, c_max, (c_min, c_max))

    mask = (
        df["category"].isin(cat_filter)
        & df["continent"].isin(cont_filter)
        & df["century_of_death"].between(century_range[0], century_range[1])
    )
    filtered = df[mask]

    st.markdown(f"**{len(filtered)} santos encontrados**")
    display_cols = ["name", "category", "origin_country", "continent", "death_year", "canonization_year", "years_to_canonization"]
    st.dataframe(filtered[display_cols].sort_values("death_year"), use_container_width=True, hide_index=True)

    st.subheader("Detalhes do Santo")
    if filtered.empty:
        st.info("Nenhum santo encontrado com os filtros selecionados.")
    else:
        selected = st.selectbox("Selecione um santo:", filtered["name"].tolist())
        saint = filtered[filtered["name"] == selected].iloc[0]

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"**Nome:** {saint['name']}")
            st.markdown(f"**Categoria:** {saint['category']}")
            st.markdown(f"**País:** {saint['origin_country']}")
            st.markdown(f"**Continente:** {saint['continent']}")
            st.markdown(f"**Gênero:** {'Masculino' if saint['gender'] == 'M' else 'Feminino'}")
            if pd.notna(saint["religious_order"]) and saint["religious_order"] != "None":
                st.markdown(f"**Ordem Religiosa:** {saint['religious_order']}")
        with col_b:
            st.markdown(f"**Ano de Morte:** {int(saint['death_year'])}")
            st.markdown(f"**Ano de Canonização:** {int(saint['canonization_year'])}")
            if pd.notna(saint["years_to_canonization"]):
                st.markdown(f"**Anos até Canonização:** {int(saint['years_to_canonization'])}")
            if pd.notna(saint["patron_topics"]):
                st.markdown(f"**Padroeiro de:** {saint['patron_topics']}")
            if pd.notna(saint["canonizing_pope"]) and saint["canonizing_pope"] != "Pre-Congregation":
                st.markdown(f"**Canonizado por:** Papa {saint['canonizing_pope']}")

        if pd.notna(saint.get("wikipedia_summary")):
            st.markdown("**Resumo (Wikipedia):**")
            st.info(saint["wikipedia_summary"])