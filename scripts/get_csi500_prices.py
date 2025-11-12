"""
Script para baixar dados históricos do índice CSI 500.

Este script obtém dados históricos de preço de fechamento do índice CSI 500
da API Yahoo Finance, cobrindo o período máximo disponível.

Saída:
    - csi500_prices.csv (dados históricos com datas e preços de fechamento)

Tickers testados: 000905.SS, 399905.SZ, 000905.SH

Nota: Dependente de conexão com Yahoo Finance API.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Baixar dados históricos do CSI 500
print("Baixando dados históricos do CSI 500 Index (000905.SS)...")

# Definir período (últimos 10 anos)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# Tentar diferentes tickers do CSI 500
tickers_to_try = ["000905.SS", "399905.SZ", "000905.SH"]

df = None
for ticker in tickers_to_try:
    print(f"Tentando ticker: {ticker}")
    try:
        csi500 = yf.Ticker(ticker)
        temp_df = csi500.history(period="max")  # Pegar todo histórico disponível
        if len(temp_df) > 1:
            df = temp_df
            print(f"✓ Sucesso com {ticker}: {len(df)} registros")
            break
    except Exception as e:
        print(f"✗ Erro com {ticker}: {e}")

if df is None or len(df) <= 1:
    print("\nNenhum ticker funcionou. Tentando download direto...")
    # Fallback: tentar período específico
    csi500 = yf.Ticker("000905.SS")
    df = csi500.history(period="10y", interval="1d")

# Resetar index para ter a data como coluna
df = df.reset_index()

# Renomear colunas para manter consistência com o formato do S&P 500
df_final = pd.DataFrame({
    'observation_date': df['Date'].dt.strftime('%Y-%m-%d'),
    'CSI500': df['Close']
})

# Remover valores nulos
df_final = df_final.dropna(subset=['CSI500'])

print(f"\nTotal de datas: {len(df_final)}")
print(f"Período: {df_final['observation_date'].min()} a {df_final['observation_date'].max()}")

# Salvar
output_file = 'csi500_prices.csv'
df_final.to_csv(output_file, index=False)

print(f"\n✅ Arquivo salvo: {output_file}")
print("\nAmostra dos dados:")
print(df_final.head(10))
print("\nÚltimos registros:")
print(df_final.tail(10))