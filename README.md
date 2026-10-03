# 🚧 Acidentes de Trânsito no Brasil (2015–2024)

Projeto G1 — Disciplina **Linguagem de Programação: Análise e Visualização de Dados com Python**

> Análise exploratória, KPIs e dashboard interativo sobre ocorrências simuladas de acidentes de
> trânsito nas rodovias brasileiras, cobrindo as 5 regiões e 20 estados do país entre 2015 e 2024.

## 🔗 Links do projeto

| Recurso | Link |
|---|---|
| Repositório GitHub | <https://github.com/marcelobfb/projeto-g1-acidentes-transito> |
| Página do projeto (GitHub Pages) | <https://marcelobfb.github.io/projeto-g1-acidentes-transito/> |
| Dashboard (Streamlit Community Cloud) | <https://projeto-g1-acidentes-transito-bfb.streamlit.app/> |
| Notebook de análise | [`notebooks/analise_acidentes_transito.ipynb`](notebooks/analise_acidentes_transito.ipynb) |

## 🎯 Perguntas de negócio

- Qual é o volume total de acidentes, feridos e óbitos no período analisado?
- Quais regiões, estados e rodovias concentram mais ocorrências e mais óbitos?
- Existe variação temporal (anual/mensal) relevante no número de acidentes?
- Quais condições climáticas e períodos do dia são mais críticos?
- Qual a relação entre o número de veículos envolvidos e a quantidade de feridos/óbitos?

## 📊 Indicadores (KPIs)

- Total de acidentes, feridos e óbitos
- Taxa de letalidade (óbitos / acidentes)
- Total de veículos envolvidos
- Percentual de ocorrências classificadas como críticas

## 🗂️ Base de dados

`dados/simulacao_acidentes_transito_brasil.csv` — 8.880 linhas, 15 colunas, cobrindo ocorrências
simuladas de 2015 a 2024. Colunas: `ano`, `mes`, `data`, `regiao`, `uf`, `municipio`, `rodovia`,
`tipo_acidente`, `condicao_climatica`, `periodo_dia`, `acidentes`, `feridos`, `obitos`,
`veiculos_envolvidos`, `nivel_gravidade`.

## 🧰 Tecnologias utilizadas

- Python, Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Streamlit
- SQLAlchemy + SQLite (persistência em banco)
- GitHub, GitHub Pages, Streamlit Community Cloud

## ✅ Funcionalidades implementadas

**Intermediárias:**
- Filtros múltiplos no Streamlit (ano, região, UF, tipo de acidente, clima, período, gravidade)
- KPIs dinâmicos, recalculados conforme os filtros aplicados
- Gráficos interativos (Plotly)
- Análise temporal (evolução anual e sazonalidade mensal)
- Dashboard organizado em seções (abas)

**Avançadas:**
- Persistência em banco de dados (SQLAlchemy + SQLite) — ver [`database/models.py`](database/models.py)
- Mapas interativos (Plotly `scatter_geo`) por estado
- Correlação estatística entre variáveis numéricas (heatmap)

## 📁 Estrutura do projeto

```
projeto-g1-acidentes-transito/
│
├── app.py                 # Dashboard Streamlit
├── requirements.txt
├── README.md
├── index.html              # Página de apresentação (GitHub Pages)
├── dados/                  # Base de dados (CSV)
├── database/                # Modelos SQLAlchemy + SQLite
├── notebooks/               # Notebook de análise exploratória
└── imagens/                 # Gráficos exportados do notebook
```

## ▶️ Como executar localmente

```bash
# 1. Criar e ativar um ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. (Opcional) gerar o banco SQLite a partir do CSV
python database/models.py

# 4. Rodar o dashboard
streamlit run app.py
```

## 📓 Como abrir o notebook no Google Colab

1. Acesse [colab.research.google.com](https://colab.research.google.com) e faça upload do
   arquivo `notebooks/analise_acidentes_transito.ipynb`.
2. Faça upload também do arquivo `dados/simulacao_acidentes_transito_brasil.csv` (ou monte o
   Google Drive) e ajuste o caminho de leitura do CSV na primeira célula de código, se necessário.
3. Execute as células em sequência (`Ambiente de execução → Executar tudo`).

## 📌 Conclusão executiva

A análise identificou a região Sudeste como a de maior concentração de acidentes e óbitos no
período, com padrões sazonais e associações relevantes entre condição climática, período do dia
e gravidade das ocorrências. Esses achados reforçam a importância de ações direcionadas de
fiscalização e infraestrutura nas localidades e condições mais críticas — detalhes completos na
aba **Conclusão** do dashboard e na seção 10 do notebook.
