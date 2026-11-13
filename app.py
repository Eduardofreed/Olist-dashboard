import pandas as pd

# Carregar os dois datasets
df_orders = pd.read_csv("data/olist_orders_dataset.csv")
df_items = pd.read_csv("data/olist_order_items_dataset.csv")

# Filtrar apenas pedidos que realmente foram entregues
df_orders = df_orders[df_orders["order_status"] == "delivered"].copy()

# Converter colunas de texto para formato de Data real (datetime)
colunas_data = ["order_purchase_timestamp", "order_delivered_customer_date"]
for col in colunas_data:
    df_orders[col] = pd.to_datetime(df_orders[col])

# Criar uma coluna nova: tempo de entrega em dias
df_orders["dias_entrega"] = (
    df_orders["order_delivered_customer_date"] - df_orders["order_purchase_timestamp"]
).dt.days

# Juntar (Merge) pedidos com itens usando o ID do pedido
df_completo = pd.merge(df_orders, df_items, on="order_id", how="inner")

# Validação do resultado
print("Total de linhas após junção:", len(df_completo))
print("\nAmostra dos dados tratados:")
print(df_completo[["order_id", "price", "freight_value", "dias_entrega"]].head(5))
print("\nValores nulos restantes nas colunas principais:")
print(df_completo[["price", "dias_entrega"]].isnull().sum())

# Colunas para valor total e o mês da compra
df_completo["valor_total"] = df_completo["price"] + df_completo["freight_value"]
df_completo["mes_compra"] = df_completo["order_purchase_timestamp"].dt.to_period("M")

# KPIs (Indicadores de performance chave) Gerais 
faturamento_total = df_completo["valor_total"].sum()
# Como um pedido tem vários itens, foi feito um agrupamento por order_id para achar o ticket médio real por pedido
ticket_medio_pedido = df_completo.groupby("order_id")["valor_total"].sum().mean()
tempo_medio_entrega = df_completo["dias_entrega"].mean()

print("=== INDICADORES GERAIS ===")
print(f'Faturamento Total (Produtos + Frete): R$ {faturamento_total:,.2f}')
print(f'Ticket Médio por Pedido: R$ {ticket_medio_pedido:,.2f}')
print(f'Tempo Médio de Entrega: {tempo_medio_entrega:,.2f} dias')

print('\n === TOP 5 MESES EM FATURAMENTO === ')
faturamento_mensal = (
    df_completo.groupby("mes_compra")["valor_total"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)
print(faturamento_mensal)

# Impacto do Frete
peso_frete = (df_completo["freight_value"].sum() / faturamento_total) * 100
print(f'\nRepresentativade do Frete no Faturamento: {peso_frete:.1f}%')