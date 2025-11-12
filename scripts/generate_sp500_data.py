"""
Script para gerar dados históricos sintéticos do S&P 500.

Este script gera aproximadamente 500.000 registros de dados de mercado americano,
incluindo preços de ações, volumes, índice S&P 500 e métricas financeiras.

Entrada:
    - sp500_companies.csv (lista de empresas do índice)

Saída:
    - sp500_data_500k.csv (arquivo com ~500k registros de dados)

Período: Últimos 10 anos de dados de dias úteis (business days)
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

# Carregar dados das empresas do S&P 500
df_companies = pd.read_csv('sp500_companies.csv')

print(f"Total de empresas: {len(df_companies)}")

# Gerar dados históricos de preços sintéticos do S&P 500
# O S&P 500 varia tipicamente entre 2000-5000 nos últimos anos
print("\nGerando dados históricos de preços do S&P 500...")

# Criar datas (últimos 10 anos, dias úteis)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

dates = pd.date_range(start=start_date, end=end_date, freq='B')  # B = business days

# Gerar valores do índice S&P 500 com tendência realista
np.random.seed(42)
base_value = 2000
trend = np.linspace(0, 2500, len(dates))  # Tendência de crescimento
noise = np.random.normal(0, 200, len(dates)).cumsum()  # Volatilidade
sp500_values = base_value + trend + noise

# Garantir que os valores estejam em um range realista
sp500_values = np.clip(sp500_values, 1500, 6000)

df_prices = pd.DataFrame({
    'observation_date': dates,
    'SP500': sp500_values
})

print(f"Total de datas de preços: {len(df_prices)}")

# Gerar aproximadamente 500 mil registros
target_records = 500000
records_per_company = target_records // len(df_companies)

print(f"\nGerando aproximadamente {target_records:,} registros...")
print(f"Registros por empresa: {records_per_company}")

all_records = []

# Setores típicos de empresas americanas
sector_mapping = {
    'Technology': 'Information Technology',
    'Financials': 'Financials',
    'Consumer': 'Consumer Discretionary',
    'Industrials': 'Industrials',
    'Health Care': 'Health Care',
    'Materials': 'Materials',
    'Energy': 'Energy',
    'Real Estate': 'Real Estate',
    'Utilities': 'Utilities',
    'Communication': 'Communication Services'
}

# Setores em inglês
us_sectors = list(sector_mapping.values())

for idx, company in df_companies.iterrows():
    if idx % 50 == 0:
        print(f"Processando empresa {idx + 1}/{len(df_companies)}...")

    # Atribuir setor (usar do CSV se disponível)
    sector = company.get('GICS Sector', random.choice(us_sectors))

    # Selecionar datas aleatórias do histórico
    sample_dates = df_prices.sample(n=min(records_per_company, len(df_prices)), replace=True)

    for _, price_row in sample_dates.iterrows():
        # Calcular preço da ação baseado no índice S&P 500
        base_price = price_row['SP500'] / 10  # Normalizar
        stock_price = base_price * random.uniform(0.5, 3.0)

        # Calcular volume de negociação
        volume = random.randint(1000000, 150000000)

        # Calcular variação percentual
        price_change = random.uniform(-5, 5)  # Mercado americano menos volátil

        # Calcular market cap estimado (em USD bilhões)
        market_cap = stock_price * random.uniform(5, 800) * 1000000

        # Extrair símbolo da empresa
        symbol = company['Symbol']

        record = {
            'id': len(all_records) + 1,
            'symbol': symbol,
            'company_name': company['Security'],
            'sector': sector,
            'exchange': 'NYSE' if 'NYSE' in str(company.get('Exchange', 'NYSE')) else 'NASDAQ',
            'country': 'USA',
            'observation_date': price_row['observation_date'].strftime('%Y-%m-%d'),
            'sp500_index': round(price_row['SP500'], 2),
            'stock_price': round(stock_price, 2),
            'volume': volume,
            'price_change_percent': round(price_change, 2),
            'market_cap': round(market_cap, 2),
            'pe_ratio': round(random.uniform(10, 40), 2),  # P/E ratio típico nos EUA
            'pb_ratio': round(random.uniform(1, 8), 2),  # Price-to-Book
            'dividend_yield': round(random.uniform(0, 3), 2),
            'beta': round(random.uniform(0.5, 2.0), 3),
            'year': price_row['observation_date'].year,
            'month': price_row['observation_date'].month,
            'quarter': (price_row['observation_date'].month - 1) // 3 + 1,
            'day_of_week': price_row['observation_date'].strftime('%A'),
            'is_tech_sector': 1 if sector == 'Information Technology' else 0,
            'is_financial_sector': 1 if sector == 'Financials' else 0,
            'is_consumer_sector': 1 if sector == 'Consumer Discretionary' else 0,
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
output_file = 'sp500_data_500k.csv'
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
    'sp500_index': 'mean',
    'stock_price': 'mean'
}).round(2))

print("\nEstatísticas por Exchange:")
print(df_final.groupby('exchange').agg({
    'id': 'count',
    'stock_price': 'mean',
    'volume': 'mean'
}).round(2))

print("\n✅ Processo concluído!")
