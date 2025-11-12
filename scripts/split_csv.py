"""
Script para dividir dados do S&P 500 em duas partes.

Este script carrega o arquivo com ~500k registros e o divide em duas partes
iguais para facilitar o processamento e armazenamento.

Entrada:
    - sp500_data_500k.csv (~500k registros)

Saída:
    - sp500_data_part1.csv (primeira metade)
    - sp500_data_part2.csv (segunda metade)
"""

import pandas as pd

# Carregar o arquivo grande
print("Carregando arquivo sp500_data_500k.csv...")
df = pd.read_csv('sp500_data_500k.csv')

print(f"Total de registros: {len(df):,}")

# Dividir ao meio
meio = len(df) // 2

df_parte1 = df.iloc[:meio]
df_parte2 = df.iloc[meio:]

print(f"\nParte 1: {len(df_parte1):,} registros")
print(f"Parte 2: {len(df_parte2):,} registros")

# Salvar as duas partes
print("\nSalvando parte 1...")
df_parte1.to_csv('sp500_data_part1.csv', index=False, encoding='utf-8')

print("Salvando parte 2...")
df_parte2.to_csv('sp500_data_part2.csv', index=False, encoding='utf-8')

print("\n✅ Arquivos divididos com sucesso!")
print("   - sp500_data_part1.csv")
print("   - sp500_data_part2.csv")