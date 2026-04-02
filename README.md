# ✝ Data Science dos Santos Católicos

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626?style=flat-square&logo=jupyter&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?style=flat-square&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.24-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

> Projeto de aprendizado de IA/ML que usa dados históricos dos Santos Católicos para praticar as principais técnicas de Ciência de Dados — desde coleta até Machine Learning e NLP.

---

## 📊 Visualizações

<table>
  <tr>
    <td><img src="outputs/figures/03_top20_paises.png" width="100%"/><br><sub>Top 20 países com mais santos</sub></td>
    <td><img src="outputs/figures/03_series_temporal.png" width="100%"/><br><sub>Santos canonizados por século</sub></td>
  </tr>
  <tr>
    <td><img src="outputs/figures/03_heatmap_seculo_continente.png" width="100%"/><br><sub>Heatmap: século × continente</sub></td>
    <td><img src="outputs/figures/03_stacked_categorias.png" width="100%"/><br><sub>Mártires vs Confessores vs Doutores</sub></td>
  </tr>
  <tr>
    <td><img src="outputs/figures/04_pca_clusters.png" width="100%"/><br><sub>Clustering PCA dos santos</sub></td>
    <td><img src="outputs/figures/05_shap_summary.png" width="100%"/><br><sub>SHAP: importância das variáveis (Random Forest)</sub></td>
  </tr>
  <tr>
    <td><img src="outputs/figures/06_wordclouds.png" width="100%"/><br><sub>Word Clouds por categoria</sub></td>
    <td><img src="outputs/figures/05_roc_pr_curves.png" width="100%"/><br><sub>Curvas ROC e Precision-Recall</sub></td>
  </tr>
</table>

---

## 📓 Notebooks

| # | Notebook | Técnicas |
|---|----------|----------|
| `00` | Setup do Projeto | Python, Jupyter, pathlib |
| `01` | Coleta de Dados | Web Scraping, Wikipedia API, pd.read_html |
| `02` | Limpeza de Dados | pandas, SimpleImputer, missingno |
| `03` | EDA & Visualizações | seaborn, matplotlib, plotly — **13 gráficos** |
| `04` | ML: Clustering | K-Means, PCA, t-SNE, Dendrograma |
| `05` | ML: Classificação | Random Forest, ROC Curve, SHAP, Cross-Validation |
| `06` | NLP | TF-IDF, LDA, WordCloud, TextBlob |

---

## 🔍 Principais Descobertas

- **Itália lidera em Santos** — seguida de França e Espanha, refletindo a centralidade de Roma
- **Mártires são canonizados mais rápido** — testemunho claro acelera o processo
- **Século XIII foi o mais produtivo** — Francisco de Assis, Tomás de Aquino, Domingos de Gusmão
- **Random Forest prevê mártires com boa acurácia** — usando apenas século e país de origem

---

## 🚀 Como rodar localmente

```bash
# 1. Instalar dependências (Anaconda recomendado)
pip install -r requirements.txt

# 2. Abrir notebooks
jupyter lab

# 3. App interativo com chat + gráficos animados
streamlit run app.py

# 4. Regenerar apresentação HTML
python generate_html.py
```

---

## 🗂 Estrutura

```
santos_ai_project/
├── notebooks/          # 7 notebooks Jupyter (00 → 06)
├── data/
│   ├── raw/            # Dados brutos coletados
│   └── processed/      # saints_clean.csv — dataset principal
├── outputs/
│   ├── figures/        # 13 gráficos exportados
│   └── models/         # Modelos ML treinados
├── apresentacao/       # Apresentação HTML com gráficos animados
├── app.py              # App Streamlit (chat + explorador)
├── generate_html.py    # Injeta gráficos animados no HTML
└── requirements.txt
```

---

## 🛠 Stack

| Área | Bibliotecas |
|------|-------------|
| Manipulação de dados | pandas, numpy, scipy |
| Visualização | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn, shap |
| NLP | nltk, textblob, wordcloud |
| Coleta de dados | requests, beautifulsoup4, wikipedia-api |
| App interativo | streamlit |

---

*Projeto de estudo pessoal — Mateu, 2025*