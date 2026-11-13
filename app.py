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