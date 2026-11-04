import pandas as pd

# Carregar uma amostra dos dados
print("Carregando pedidos...")
# Lê a planilha olist_orders_dataset
df_orders = pd.read_csv("data/olist_orders_dataset.csv")

print("Carregando itens...")
# Lê a planilha olist_order_items_dataset
df_items = pd.read_csv("data/olist_order_items_dataset.csv")

# Inspeção inicial
print("\n--- Estrutura de Pedidos ---")
print(df_orders.info())
print("\nPrimeiras 3 linhas:")
print(df_orders.head(3))

print("\n--- Estrutura de Itens ---")
print(df_items.info())
