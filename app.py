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

# INTERFACE VISUAL
st.title("Painel Executivo de E-commerce (Olist)")
st.markdown("Análise operacional de vendas, ticket medio e logística de entregas.")

st.divider()

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