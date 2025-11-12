"""
Script para gerar dados históricos sintéticos do CSI 500.

Este script gera aproximadamente 500.000 registros de dados de mercado chinês,
incluindo preços de ações, volumes, índice CSI 500 e métricas financeiras.

Entrada:
    - csi500_companies.csv (lista de empresas do índice)

Saída:
    - csi500_data_500k.csv (arquivo com ~500k registros de dados)

Período: Últimos 10 anos de dados de dias úteis (business days)
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Carregar dados das empresas do CSI 500
df_companies = pd.read_csv('csi500_companies.csv')

print(f"Total de empresas: {len(df_companies)}")

# Gerar dados históricos de preços sintéticos do CSI 500
# O CSI 500 varia tipicamente entre 4000-8000 nos últimos anos
print("\nGerando dados históricos de preços do CSI 500...")

# Criar datas (últimos 10 anos, dias úteis)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

dates = pd.date_range(start=start_date, end=end_date, freq='B')  # B = business days

# Gerar valores do índice CSI 500 com tendência realista
np.random.seed(42)
base_value = 5000
trend = np.linspace(0, 2000, len(dates))  # Tendência de crescimento
noise = np.random.normal(0, 300, len(dates)).cumsum()  # Volatilidade
csi500_values = base_value + trend + noise

# Garantir que os valores estejam em um range realista
csi500_values = np.clip(csi500_values, 3000, 9000)

df_prices = pd.DataFrame({
    'observation_date': dates,
    'CSI500': csi500_values
})

print(f"Total de datas de preços: {len(df_prices)}")

# Gerar aproximadamente 500 mil registros
target_records = 500000
records_per_company = target_records // len(df_companies)

print(f"\nGerando aproximadamente {target_records:,} registros...")
print(f"Registros por empresa: {records_per_company}")

all_records = []

# Setores típicos de empresas chinesas (tradução aproximada)
sector_mapping = {
    'Technology': '信息技术',
    'Financials': '金融',
    'Consumer': '消费',
    'Industrials': '工业',
    'Health Care': '医疗保健',
    'Materials': '材料',
    'Energy': '能源',
    'Real Estate': '房地产',
    'Utilities': '公用事业',
    'Communication': '通信服务'
}

# Inverter para mapear de chinês para inglês
chinese_sectors = list(sector_mapping.keys())

for idx, company in df_companies.iterrows():
    if idx % 50 == 0:
        print(f"Processando empresa {idx + 1}/{len(df_companies)}...")

    # Atribuir setor aleatório (já que não temos essa info)
    sector = random.choice(chinese_sectors)

    # Selecionar datas aleatórias do histórico
    sample_dates = df_prices.sample(n=min(records_per_company, len(df_prices)), replace=True)

    for _, price_row in sample_dates.iterrows():
        # Calcular preço da ação baseado no índice CSI 500
        base_price = price_row['CSI500'] / 10  # Normalizar
        stock_price = base_price * random.uniform(0.5, 3.0)

        # Calcular volume de negociação (tipicamente maior no mercado chinês)
        volume = random.randint(500000, 100000000)

        # Calcular variação percentual
        price_change = random.uniform(-8, 8)  # Mercado chinês pode ser mais volátil

        # Calcular market cap estimado (em RMB bilhões)
        market_cap = stock_price * random.uniform(1, 300) * 1000000

        # Extrair código da empresa (exemplo: 000002.SZ -> 000002)
        stock_code = company['Symbol'].split('.')[0]

        record = {
            'id': len(all_records) + 1,
            'symbol': company['Symbol'],
            'stock_code': stock_code,
            'company_name_cn': company['Name'],
            'company_name_en': f"{company['Name']} Co., Ltd.",  # Placeholder em inglês
            'sector': sector,
            'sub_industry': f"{sector} - Various",
            'exchange': 'Shanghai' if '.SH' in company['Symbol'] or '.SS' in company['Symbol'] else 'Shenzhen',
            'country': 'China',
            'observation_date': price_row['observation_date'].strftime('%Y-%m-%d'),
            'csi500_index': round(price_row['CSI500'], 2),
            'stock_price': round(stock_price, 2),
            'volume': volume,
            'price_change_percent': round(price_change, 2),
            'market_cap': round(market_cap, 2),
            'pe_ratio': round(random.uniform(8, 60), 2),  # P/E ratio típico na China
            'pb_ratio': round(random.uniform(0.5, 5), 2),  # Price-to-Book
            'dividend_yield': round(random.uniform(0, 4), 2),
            'beta': round(random.uniform(0.7, 2.5), 3),
            'year': price_row['observation_date'].year,
            'month': price_row['observation_date'].month,
            'quarter': (price_row['observation_date'].month - 1) // 3 + 1,
            'day_of_week': price_row['observation_date'].strftime('%A'),
            'is_tech_sector': 1 if sector == 'Technology' else 0,
            'is_financial_sector': 1 if sector == 'Financials' else 0,
            'is_consumer_sector': 1 if sector == 'Consumer' else 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        all_records.append(record)

# Criar DataFrame final
df_final = pd.DataFrame(all_records)

# Verificar total de registros
print(f"\n{'=' * 80}")
print(f"Total de registros gerados: {len(df_final):,}")
print(f"{'=' * 80}")

# Exibir amostra dos dados
print("\nAmostra dos primeiros registros:")
print(df_final.head(10))

print("\nEstatísticas dos dados:")
print(df_final.describe())

print("\nInformações das colunas:")
print(df_final.info())

# Salvar em CSV
output_file = 'csi500_data_500k.csv'
df_final.to_csv(output_file, index=False, encoding='utf-8')

print(f"\n{'=' * 80}")
print(f"Arquivo salvo com sucesso: {output_file}")
print(f"{'=' * 80}")

# Estatísticas adicionais
print("\nEstatísticas por Setor:")
print(df_final.groupby('sector').agg({
    'id': 'count',
    'stock_price': 'mean',
    'volume': 'mean',
    'market_cap': 'mean'
}).round(2))

print("\nEstatísticas por Ano:")
print(df_final.groupby('year').agg({
    'id': 'count',
    'csi500_index': 'mean',
    'stock_price': 'mean'
}).round(2))

print("\nEstatísticas por Exchange:")
print(df_final.groupby('exchange').agg({
    'id': 'count',
    'stock_price': 'mean',
    'volume': 'mean'
}).round(2))

print("\n✅ Processo concluído!")
