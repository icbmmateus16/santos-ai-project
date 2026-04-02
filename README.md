# ✝ Data Science dos Santos Católicos

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626?style=flat-square&logo=jupyter&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.2-150458?style=flat-square&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.24-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

> Projeto de aprendizado de IA/ML que usa dados históricos dos Santos Católicos para praticar as principais técnicas de Ciência de Dados — desde coleta até Machine Learning e NLP.

**[🌐 Ver apresentação online →](https://SEU_USUARIO.github.io/santos-ai-project/)**

---

## 📊 O que foi construído

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

### Pré-requisitos

```bash
# Anaconda (recomendado) ou Python 3.11+
conda create -n santos python=3.11
conda activate santos
pip install -r requirements.txt
```

### Notebooks (análise completa)

```bash
jupyter lab
# Abra a pasta notebooks/ e rode em ordem: 00 → 06
```

### App interativo (chat + gráficos animados)

```bash
streamlit run app.py
# Abre em http://localhost:8501
```

### Regenerar apresentação HTML

```bash
python generate_html.py
# Atualiza apresentacao/index.html com gráficos animados
```

---

## 🗂 Estrutura do projeto

```
santos_ai_project/
│
├── notebooks/          # 7 notebooks Jupyter (00 a 06)
├── data/
│   ├── raw/            # Dados brutos coletados
│   └── processed/      # saints_clean.csv — dataset principal
├── outputs/
│   ├── figures/        # 13 gráficos estáticos exportados
│   └── models/         # Modelos ML treinados (.pkl)
├── apresentacao/       # Apresentação HTML estática
│   ├── index.html      # Página principal (GitHub Pages)
│   └── data.json       # Metadados do projeto
├── app.py              # App Streamlit
├── generate_html.py    # Injeta gráficos animados no HTML
└── requirements.txt
```

---

## 🛠 Stack tecnológica

| Área | Bibliotecas |
|------|-------------|
| Manipulação de dados | pandas, numpy, scipy |
| Visualização | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn, shap |
| NLP | nltk, textblob, wordcloud |
| Coleta de dados | requests, beautifulsoup4, wikipedia-api |
| App interativo | streamlit |

---

## 📸 Prévia

A apresentação inclui gráficos animados interativos construídos com Plotly:
- **Mapa coroplético** — distribuição mundial dos santos
- **Barras animadas por século** — evolução de mártires, confessores e doutores
- **Scatter cumulativo** — anos até canonização ao longo dos séculos
- **Treemap, Violin, Polar Chart** e muito mais

---

*Projeto de estudo pessoal — Mateu, 2025*