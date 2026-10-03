"""
Dashboard Executivo — Acidentes de Trânsito no Brasil (2015-2024)
Projeto G1 — Linguagem de Programação: Análise e Visualização de Dados com Python
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database.models import load_dataframe

sns.set_theme(style="whitegrid")

st.set_page_config(
    page_title="Acidentes de Trânsito no Brasil",
    page_icon="🚧",
    layout="wide",
)

# Coordenadas aproximadas (capital) de cada UF, usadas no mapa interativo
UF_COORDS = {
    "AC": (-9.97, -67.81), "AL": (-9.65, -35.73), "AM": (-3.10, -60.02),
    "AP": (0.03, -51.07), "BA": (-12.97, -38.51), "CE": (-3.73, -38.52),
    "DF": (-15.78, -47.93), "ES": (-20.32, -40.34), "GO": (-16.68, -49.25),
    "MA": (-2.53, -44.30), "MG": (-19.92, -43.93), "MS": (-20.44, -54.65),
    "MT": (-15.60, -56.10), "PA": (-1.46, -48.50), "PB": (-7.12, -34.86),
    "PE": (-8.05, -34.90), "PI": (-5.09, -42.80), "PR": (-25.43, -49.27),
    "RJ": (-22.91, -43.17), "RN": (-5.79, -35.21), "RO": (-8.76, -63.90),
    "RR": (2.82, -60.67), "RS": (-30.03, -51.23), "SC": (-27.60, -48.55),
    "SE": (-10.91, -37.07), "SP": (-23.55, -46.63), "TO": (-10.25, -48.32),
}


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    try:
        df = load_dataframe()
    except Exception:
        caminho_csv = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "dados",
            "simulacao_acidentes_transito_brasil.csv",
        )
        df = pd.read_csv(caminho_csv, encoding="utf-8-sig")
        df["data"] = pd.to_datetime(df["data"])
    df["taxa_letalidade"] = (df["obitos"] / df["acidentes"].replace(0, np.nan)) * 100
    return df


df = carregar_dados()


def fmt(n: int) -> str:
    """Formata inteiros com separador de milhar no padrão brasileiro (172.190)."""
    return f"{n:,}".replace(",", ".")

# ---------------------------------------------------------------- Cabeçalho
st.title("🚧 Dashboard Executivo — Acidentes de Trânsito no Brasil")
st.markdown(
    """
    Este dashboard analisa **ocorrências simuladas de acidentes de trânsito nas rodovias
    brasileiras entre 2015 e 2024**, cobrindo as 5 regiões e 20 estados do país. O objetivo é
    identificar padrões de gravidade, sazonalidade, condições climáticas e localidades críticas
    que possam apoiar políticas públicas de segurança viária.
    """
)

# ---------------------------------------------------------------- Filtros
st.sidebar.header("🔎 Filtros")
st.sidebar.caption("Combine os filtros abaixo para refinar a análise.")

anos = st.sidebar.multiselect(
    "Ano", sorted(df["ano"].unique()), default=sorted(df["ano"].unique())
)
regioes = st.sidebar.multiselect(
    "Região", sorted(df["regiao"].unique()), default=sorted(df["regiao"].unique())
)
ufs_disponiveis = sorted(df[df["regiao"].isin(regioes)]["uf"].unique())
ufs = st.sidebar.multiselect("UF", ufs_disponiveis, default=ufs_disponiveis)
tipos = st.sidebar.multiselect(
    "Tipo de acidente",
    sorted(df["tipo_acidente"].unique()),
    default=sorted(df["tipo_acidente"].unique()),
)
climas = st.sidebar.multiselect(
    "Condição climática",
    sorted(df["condicao_climatica"].unique()),
    default=sorted(df["condicao_climatica"].unique()),
)
periodos = st.sidebar.multiselect(
    "Período do dia",
    sorted(df["periodo_dia"].unique()),
    default=sorted(df["periodo_dia"].unique()),
)
gravidades = st.sidebar.multiselect(
    "Nível de gravidade",
    sorted(df["nivel_gravidade"].unique()),
    default=sorted(df["nivel_gravidade"].unique()),
)

df_f = df[
    df["ano"].isin(anos)
    & df["regiao"].isin(regioes)
    & df["uf"].isin(ufs)
    & df["tipo_acidente"].isin(tipos)
    & df["condicao_climatica"].isin(climas)
    & df["periodo_dia"].isin(periodos)
    & df["nivel_gravidade"].isin(gravidades)
]

if df_f.empty:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

# ---------------------------------------------------------------- KPIs
st.subheader("📌 Indicadores-chave (KPIs)")

total_acidentes = int(df_f["acidentes"].sum())
total_obitos = int(df_f["obitos"].sum())
total_feridos = int(df_f["feridos"].sum())
total_veiculos = int(df_f["veiculos_envolvidos"].sum())
taxa_letalidade = (total_obitos / total_acidentes * 100) if total_acidentes else 0
pct_critico = (
    df_f.loc[df_f["nivel_gravidade"] == "Crítico", "acidentes"].sum()
    / total_acidentes
    * 100
    if total_acidentes
    else 0
)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Acidentes", fmt(total_acidentes))
c2.metric("Óbitos", fmt(total_obitos))
c3.metric("Feridos", fmt(total_feridos))
c4.metric("Veículos envolvidos", fmt(total_veiculos))
c5.metric("Taxa de letalidade", f"{taxa_letalidade:.2f}%")
c6.metric("Ocorrências críticas", f"{pct_critico:.1f}%")

st.divider()

# ---------------------------------------------------------------- Seções em abas
aba_geral, aba_temporal, aba_geo, aba_causas, aba_dados, aba_conclusao = st.tabs(
    [
        "📊 Visão Geral",
        "📈 Análise Temporal",
        "🗺️ Análise Geográfica",
        "🌦️ Causas e Condições",
        "📋 Dados Detalhados",
        "✅ Conclusão",
    ]
)

# ----- Visão Geral
with aba_geral:
    col1, col2 = st.columns(2)

    with col1:
        por_regiao = (
            df_f.groupby("regiao", as_index=False)["acidentes"].sum().sort_values(
                "acidentes", ascending=False
            )
        )
        fig = px.bar(
            por_regiao,
            x="regiao",
            y="acidentes",
            color="regiao",
            title="Acidentes por região",
            labels={"regiao": "Região", "acidentes": "Acidentes"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        por_gravidade = df_f.groupby("nivel_gravidade", as_index=False)["acidentes"].sum()
        fig = px.pie(
            por_gravidade,
            names="nivel_gravidade",
            values="acidentes",
            title="Distribuição por nível de gravidade",
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        por_tipo = (
            df_f.groupby("tipo_acidente", as_index=False)["acidentes"]
            .sum()
            .sort_values("acidentes", ascending=True)
        )
        fig = px.bar(
            por_tipo,
            x="acidentes",
            y="tipo_acidente",
            orientation="h",
            title="Acidentes por tipo",
            labels={"tipo_acidente": "Tipo", "acidentes": "Acidentes"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        top_rodovias = (
            df_f.groupby("rodovia", as_index=False)
            .agg(acidentes=("acidentes", "sum"), obitos=("obitos", "sum"))
            .sort_values("acidentes", ascending=False)
            .head(10)
        )
        fig = px.bar(
            top_rodovias,
            x="rodovia",
            y="acidentes",
            color="obitos",
            title="Top 10 rodovias com mais acidentes",
            labels={"rodovia": "Rodovia", "acidentes": "Acidentes", "obitos": "Óbitos"},
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"""
        **Interpretação:** a região **{por_regiao.iloc[0]['regiao']}** concentra o maior volume
        de acidentes no recorte filtrado, com destaque para ocorrências do tipo
        **{por_tipo.iloc[-1]['tipo_acidente']}**. A rodovia **{top_rodovias.iloc[0]['rodovia']}**
        lidera o ranking de ocorrências, o que a torna prioritária para ações de fiscalização.
        """
    )

# ----- Análise Temporal
with aba_temporal:
    serie_anual = df_f.groupby("ano", as_index=False).agg(
        acidentes=("acidentes", "sum"), obitos=("obitos", "sum")
    )
    fig = px.line(
        serie_anual,
        x="ano",
        y=["acidentes", "obitos"],
        markers=True,
        title="Evolução anual de acidentes e óbitos",
        labels={"value": "Ocorrências", "ano": "Ano", "variable": "Indicador"},
    )
    st.plotly_chart(fig, use_container_width=True)

    df_f["mes_nome"] = df_f["data"].dt.month
    sazonalidade = df_f.groupby("mes_nome", as_index=False)["acidentes"].sum()
    fig2, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=sazonalidade, x="mes_nome", y="acidentes", marker="o", ax=ax)
    ax.set_title("Sazonalidade mensal de acidentes (todos os anos agregados)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Acidentes")
    ax.set_xticks(range(1, 13))
    st.pyplot(fig2)

    variacao = (
        (serie_anual["acidentes"].iloc[-1] - serie_anual["acidentes"].iloc[0])
        / serie_anual["acidentes"].iloc[0]
        * 100
        if len(serie_anual) > 1 and serie_anual["acidentes"].iloc[0]
        else 0
    )
    tendencia = "crescimento" if variacao > 0 else "queda"
    st.markdown(
        f"""
        **Interpretação:** entre {serie_anual['ano'].min()} e {serie_anual['ano'].max()} houve
        **{tendencia} de {abs(variacao):.1f}%** no total de acidentes no recorte selecionado.
        O mês **{int(sazonalidade.sort_values('acidentes', ascending=False).iloc[0]['mes_nome'])}**
        concentra o maior volume histórico de ocorrências, sugerindo um padrão sazonal a ser
        monitorado por órgãos de trânsito.
        """
    )

# ----- Análise Geográfica
with aba_geo:
    por_uf = df_f.groupby("uf", as_index=False).agg(
        acidentes=("acidentes", "sum"),
        obitos=("obitos", "sum"),
        feridos=("feridos", "sum"),
    )
    por_uf["lat"] = por_uf["uf"].map(lambda u: UF_COORDS.get(u, (np.nan, np.nan))[0])
    por_uf["lon"] = por_uf["uf"].map(lambda u: UF_COORDS.get(u, (np.nan, np.nan))[1])

    fig = px.scatter_geo(
        por_uf,
        lat="lat",
        lon="lon",
        size="acidentes",
        color="obitos",
        hover_name="uf",
        hover_data={"acidentes": True, "obitos": True, "feridos": True, "lat": False, "lon": False},
        color_continuous_scale="OrRd",
        size_max=40,
        title="Mapa interativo — acidentes (tamanho) e óbitos (cor) por estado",
    )
    fig.update_geos(
        scope="south america",
        center={"lat": -14.2, "lon": -51.9},
        projection_scale=1.0,
        lataxis_range=[-35, 6],
        lonaxis_range=[-75, -32],
        showcountries=True,
        showland=True,
        landcolor="rgb(235,235,235)",
    )
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)

    pior_uf = por_uf.sort_values("obitos", ascending=False).iloc[0]
    st.markdown(
        f"""
        **Interpretação:** o estado **{pior_uf['uf']}** registra o maior número absoluto de
        óbitos ({int(pior_uf['obitos'])}) no recorte selecionado, concentrando esforços de
        fiscalização e sinalização nesta unidade federativa.
        """
    )

# ----- Causas e Condições
with aba_causas:
    col1, col2 = st.columns(2)
    with col1:
        por_clima = df_f.groupby("condicao_climatica", as_index=False)["acidentes"].sum()
        fig = px.bar(
            por_clima.sort_values("acidentes", ascending=False),
            x="condicao_climatica",
            y="acidentes",
            title="Acidentes por condição climática",
            labels={"condicao_climatica": "Condição climática", "acidentes": "Acidentes"},
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        por_periodo = df_f.groupby("periodo_dia", as_index=False)["acidentes"].sum()
        fig = px.bar(
            por_periodo.sort_values("acidentes", ascending=False),
            x="periodo_dia",
            y="acidentes",
            title="Acidentes por período do dia",
            labels={"periodo_dia": "Período", "acidentes": "Acidentes"},
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Correlação estatística entre variáveis numéricas")
    colunas_num = ["acidentes", "feridos", "obitos", "veiculos_envolvidos", "taxa_letalidade"]
    fig3, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        df_f[colunas_num].corr(), annot=True, cmap="coolwarm", center=0, fmt=".2f", ax=ax
    )
    ax.set_title("Matriz de correlação")
    st.pyplot(fig3)

    clima_critico = por_clima.sort_values("acidentes", ascending=False).iloc[0]
    periodo_critico = por_periodo.sort_values("acidentes", ascending=False).iloc[0]
    st.markdown(
        f"""
        **Interpretação:** a condição climática **{clima_critico['condicao_climatica']}** e o
        período **{periodo_critico['periodo_dia']}** concentram o maior número de acidentes,
        indicando maior necessidade de atenção (sinalização, iluminação, fiscalização) nesses
        cenários. A correlação entre `veiculos_envolvidos` e `feridos` tende a ser a mais forte
        da matriz, como esperado em colisões com múltiplos veículos.
        """
    )

# ----- Dados Detalhados
with aba_dados:
    st.markdown("Tabela filtrada de acordo com os filtros selecionados na barra lateral.")
    st.dataframe(
        df_f.sort_values("data", ascending=False).drop(columns=["mes_nome"], errors="ignore"),
        use_container_width=True,
        height=420,
    )
    st.download_button(
        "⬇️ Baixar dados filtrados (CSV)",
        data=df_f.to_csv(index=False).encode("utf-8-sig"),
        file_name="acidentes_filtrados.csv",
        mime="text/csv",
    )

# ----- Conclusão
with aba_conclusao:
    st.markdown(
        f"""
        ### Conclusão executiva

        No recorte analisado ({len(anos)} ano(s), {len(regioes)} região(ões)), foram registrados
        **{fmt(total_acidentes)}** acidentes, resultando em **{fmt(total_obitos)}** óbitos e
        **{fmt(total_feridos)}** feridos, com uma taxa de letalidade de **{taxa_letalidade:.2f}%**.

        **Principais achados:**
        - A região **{por_regiao.iloc[0]['regiao']}** e o estado **{pior_uf['uf']}** concentram as
          ocorrências mais críticas, sendo prioritários para políticas públicas de segurança viária.
        - Condições de **{clima_critico['condicao_climatica'].lower()}** e o período da
          **{periodo_critico['periodo_dia'].lower()}** estão associados a mais acidentes.
        - O tipo de acidente **{por_tipo.iloc[-1]['tipo_acidente'].lower()}** é o mais recorrente,
          reforçando a necessidade de campanhas educativas e melhorias na sinalização.

        **Recomendações:** reforçar a fiscalização nos horários e condições climáticas mais
        críticas, priorizar investimentos de infraestrutura nas rodovias e estados com maior
        concentração de óbitos, e acompanhar a sazonalidade mensal para antecipar campanhas de
        prevenção.
        """
    )

st.sidebar.divider()
st.sidebar.caption(
    "Projeto G1 — Linguagem de Programação: Análise e Visualização de Dados com Python."
)
