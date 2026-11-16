import pandas as pd
import streamlit as st

# Configuração inicial da página
st.set_page_config(page_title="Dashboard Olist", page_icon="📊", layout="wide")


@st.cache_data
def carregar_dados():
    df_orders = pd.read_csv("data/olist_orders_dataset.csv")
    df_items = pd.read_csv("data/olist_order_items_dataset.csv")

    df_orders = df_orders[df_orders["order_status"] == "delivered"].copy()

    colunas_data = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for col in colunas_data:
        df_orders[col] = pd.to_datetime(df_orders[col])

    df_orders["dias_entrega"] = (
        df_orders["order_delivered_customer_date"]
        - df_orders["order_purchase_timestamp"]
    ).dt.days

    df_completo = pd.merge(df_orders, df_items, on="order_id", how="inner")

    df_completo["valor_total"] = df_completo["price"] + df_completo["freight_value"]
    df_completo["mes_compra"] = (
        df_completo["order_purchase_timestamp"].dt.to_period("M").astype(str)
    )

    return df_completo

df = carregar_dados()

# BARRA LATERAL (FILTROS)
st.sidebar.header("Filtros")

anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione o(s) Ano(s)",
    options=anos_disponiveis,
    default=anos_disponiveis,
)

# Filtro de faixa de preço do produto
preco_min = float(df["price"].min())
preco_max = float(df["price"].max())
faixa_preco = st.sidebar.slider(
    "Faixa de Preço do Item (R$):",
    min_value=preco_min,
    max_value=min(preco_max, 2000.0), # Limitando para 2000 para facilitar o arraste
    value=(preco_min, min(preco_max, 2000.0)),
)

# Aplcar os filtros no DataFrame
df_filtrado = df[
    (df["ano"].isin(anos_selecionados))
    & (df["price"] >= faixa_preco[0])
    & (df["price"] >= faixa_preco[1])
]

# INTERFACE VISUAL
st.title("Painel Executivo de E-commerce (Olist)")
st.markdown("Análise operacional de vendas, ticket médio e logística de entregas.")

st.divider()

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados. Ajuste a barra lateral.")
else:
    faturamento_total = df["valor_total"].sum()
    ticket_medio = df.groupby("order_id")["valor_total"].sum().mean()
    tempo_entrega = df["dias_entrega"].mean()
    peso_frete = (df["freight_value"].sum() / faturamento_total) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
    col2.metric("Ticket Médio / Pedido", f"R$ {ticket_medio:,.2f}")
    col3.metric("Tempo Médio de Entrega", f"{tempo_entrega:,.1f} dias")
    col4.metric("Peso de Frete", f"{peso_frete:,.1f}%")

    st.divider()

    st.subheader("Amostra dos Dados Processados")
    st.dataframe(df[
        [
            "order_id",
            "mes_compra",
            "price",
            "freight_value",
            "valor_total",
            "dias_entrega",
        ]
    ].head(15),
    use_container_width=True    
    )