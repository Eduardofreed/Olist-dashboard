# Painel Executivo de E-commerce (Olist)

Dashboard interativo desenvolvido em **Python** e **Streamlit** para análise operacional de vendas, ticket médio e logística de entregas utilizando o dataset público da Olist (e-commerce brasileiro).

## Objetivo do Projeto
Consolidar o ciclo completo de análise de dados — extração, limpeza de datas, junção relacional, cálculo de regras de negócio e visualização interativa — em uma aplicação web local leve e reativa.

## Principais Indicadores (KPIs) e Visualizações
- **Faturamento Total:** Soma consolidada de produtos e frete para pedidos efetivamente entregues.
- **Ticket Médio por Pedido:** Cálculo agrupado por `order_id` para evitar distorções causadas por pedidos com múltiplos itens.
- **Tempo Médio de Entrega & Distribuição Logística:** Diferença em dias entre a compra e a entrega ao cliente, com filtro de outliers visuais (até 30 dias).
- **Representatividade do Frete:** Peso percentual do custo logístico sobre a receita bruta.
- **Evolução Mensal:** Série temporal interativa filtrável por ano e faixa de preço do produto.

## Tecnologias Utilizadas
- **Python 3**
- **Pandas** (ETL, tratamento de datas `datetime`, `merge` e agregações)
- **Streamlit** (Interface web, cache de dados `@st.cache_data` e gráficos nativos)
- **Git & GitHub** (Versionamento via terminal Bash)

## Como Executar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/olist-dashboard.git
cd olist-dashboard
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Baixe os arquivos `olist_orders_dataset.csv` e `olist_order_items_dataset.csv` (Kaggle - *Brazilian E-Commerce Public Dataset by Olist*) e coloque-os dentro da pasta `data/`.

4. Execute a aplicação:
```bash
python -m streamlit run app.py
```
