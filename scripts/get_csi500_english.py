"""
Script para obter nomes em inglês das empresas do CSI 500 via Yahoo Finance.

Este script busca informações em inglês para cada empresa do CSI 500,
incluindo nome, setor, indústria e market cap.

Entrada:
    - csi500_companies.csv (lista de empresas com símbolos)

Saída:
    - csi500_companies_english.csv (empresas com dados enriquecidos em inglês)

Nota: Este script depende de conexão com Yahoo Finance API.
"""

import pandas as pd
import yfinance as yf
import time

# Carregar símbolos do CSI 500
df = pd.read_csv('csi500_companies.csv')
print(f"Total de empresas no CSI 500: {len(df)}")

companies_data = []

for idx, row in df.iterrows():
    symbol = row['Symbol']

    if idx % 50 == 0:
        print(f"Processando {idx}/{len(df)}...")

    try:
        # Buscar informações no Yahoo Finance
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Extrair informações relevantes
        company_info = {
            'Symbol': symbol,
            'Chinese_Name': row['Name'],
            'English_Name': info.get('longName', info.get('shortName', row['Name'])),
            'Sector': info.get('sector', 'Unknown'),
            'Industry': info.get('industry', 'Unknown'),
            'City': info.get('city', 'Unknown'),
            'Country': info.get('country', 'China'),
            'Market_Cap': info.get('marketCap', 0),
            'Exchange': info.get('exchange', 'Unknown')
        }

        companies_data.append(company_info)

        # Pequeno delay para não sobrecarregar a API
        time.sleep(0.1)

    except Exception as e:
        print(f"Erro ao processar {symbol}: {e}")
        # Adicionar com dados limitados
        companies_data.append({
            'Symbol': symbol,
            'Chinese_Name': row['Name'],
            'English_Name': row['Name'],
            'Sector': 'Unknown',
            'Industry': 'Unknown',
            'City': 'Unknown',
            'Country': 'China',
            'Market_Cap': 0,
            'Exchange': 'Unknown'
        })

# Criar DataFrame
df_companies = pd.DataFrame(companies_data)

# Salvar
output_file = 'csi500_companies_english.csv'
df_companies.to_csv(output_file, index=False, encoding='utf-8')

print(f"\n✅ Arquivo salvo: {output_file}")
print(f"Total de empresas: {len(df_companies)}")
print("\nAmostra dos dados:")
print(df_companies.head(10))