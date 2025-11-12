# Dataseat SP500 & CSI500

Projeto para análise e processamento de dados de mercado financeiro dos índices **S&P 500** (EUA) e **CSI 500** (China).

## 📋 Descrição

Este projeto contém dados históricos de preços e informações de empresas dos dois maiores índices:
- **S&P 500**: Índice do mercado de ações dos Estados Unidos
- **CSI 500**: Índice do mercado de ações da China

## 📁 Estrutura do Projeto

```
Dataseat_SP500_CSI500/
├── README.md                 # Este arquivo
├── sp500/                    # Dados do S&P 500
│   ├── sp500_companies.csv       # Lista de empresas (informações básicas)
│   ├── sp500_data_part1.csv      # Dados históricos - Parte 1 (~250k registros)
│   └── sp500_data_part2.csv      # Dados históricos - Parte 2 (~250k registros)
├── csi500/                   # Dados do CSI 500
│   ├── csi500_companies.csv      # Lista de empresas (informações básicas)
│   ├── csi500_data_part1.csv     # Dados históricos - Parte 1 (~250k registros)
│   └── csi500_data_part2.csv     # Dados históricos - Parte 2 (~250k registros)
└── scripts/                  # Scripts de processamento
    ├── generate_csi500_data.py      # Gera dados sintéticos do CSI 500
    ├── get_csi500_english.py        # Enriquece dados com informações em inglês
    ├── get_csi500_prices.py         # Baixa preços históricos do CSI 500
    ├── split_csi500.py              # Divide dados do CSI 500 em 2 partes
    └── split_csv.py                 # Divide dados do S&P 500 em 2 partes
```

## 📊 Arquivos de Dados

### Companies (Empresas)
- **Colunas**: Symbol, Name (e outras informações das empresas)
- **Formato**: CSV com encoding UTF-8
- **Uso**: Referência das empresas que compõem cada índice

### Data (Dados Históricos)
Os dados foram divididos em 2 partes para facilitar processamento:

**Colunas principais:**
- `id`: Identificador único do registro
- `symbol`: Símbolo da ação (ex: AAPL para Apple)
- `observation_date`: Data da observação (formato YYYY-MM-DD)
- `stock_price`: Preço da ação
- `volume`: Volume de negociação
- `market_cap`: Capitalização de mercado
- `pe_ratio`: Índice P/E (Price-to-Earnings)
- `pb_ratio`: Índice P/B (Price-to-Book)
- `dividend_yield`: Taxa de dividendo
- `year`, `month`, `quarter`: Extrações de tempo

## 🔧 Scripts de Processamento

### 1. `generate_csi500_data.py`
Gera aproximadamente 500.000 registros de dados sintéticos do CSI 500.

**Entrada:**
- `csi500_companies.csv`

**Saída:**
- `csi500_data_500k.csv`

**Detalhes:**
- Cria dados históricos de 10 anos
- Baseado em dias úteis (business days)
- Inclui múltiplas métricas financeiras sintéticas

### 2. `get_csi500_english.py`
Enriquece dados com informações em inglês via Yahoo Finance.

**Entrada:**
- `csi500_companies.csv`

**Saída:**
- `csi500_companies_english.csv`

**Dados coletados:**
- Nome em inglês
- Setor e indústria
- Localização
- Market cap

### 3. `get_csi500_prices.py`
Baixa dados históricos de preços do índice CSI 500.

**Saída:**
- `csi500_prices.csv`

**Características:**
- Obtém histórico máximo disponível
- Tenta múltiplos tickers (000905.SS, 399905.SZ, 000905.SH)
- Período: preços de fechamento diários

### 4. `split_csi500.py`
Divide dados do CSI 500 em duas partes iguais.

**Entrada:**
- `csi500_data_500k.csv`

**Saída:**
- `csi500_data_part1.csv` (~250k registros)
- `csi500_data_part2.csv` (~250k registros)

### 5. `split_csv.py`
Divide dados do S&P 500 em duas partes iguais.

**Entrada:**
- `sp500_data_500k.csv`

**Saída:**
- `sp500_data_part1.csv` (~250k registros)
- `sp500_data_part2.csv` (~250k registros)

## 📈 Dados Disponíveis

### S&P 500
- **Período**: Últimos 10 anos
- **Tipo de Dados**: Sintéticos (gerados para análise)
- **Registro Total**: ~500k (divididos em 2 partes de ~250k cada)
- **Empresas**: 500 do índice S&P 500

### CSI 500
- **Período**: Últimos 10 anos
- **Tipo de Dados**: Sintéticos (gerados para análise)
- **Registro Total**: ~500k (divididos em 2 partes de ~250k cada)
- **Empresas**: ~500 do índice CSI 500 (mercado chinês)

## 🚀 Como Usar

### Carregar dados no Python:

```python
import pandas as pd

# Carregar empresas
sp500_companies = pd.read_csv('sp500/sp500_companies.csv')
csi500_companies = pd.read_csv('csi500/csi500_companies.csv')

# Carregar dados históricos
sp500_part1 = pd.read_csv('sp500/sp500_data_part1.csv')
sp500_part2 = pd.read_csv('sp500/sp500_data_part2.csv')

# Combinar partes se necessário
sp500_data = pd.concat([sp500_part1, sp500_part2], ignore_index=True)
```

## 📝 Notas Importantes

- Os dados de preços históricos são **sintéticos** e gerados para propósitos de análise/teste
- Os scripts utilizam bibliotecas como `pandas`, `numpy` e `yfinance`
- Alguns scripts requerem conexão com internet (Yahoo Finance)
- Os arquivos estão em encoding **UTF-8** com separador de vírgula

## 📦 Dependências

Os scripts requerem:
- `pandas` - Manipulação de dados
- `numpy` - Computação numérica
- `yfinance` - Download de dados financeiros (alguns scripts)

## 🔄 Workflow Típico

1. **Geração de dados**: `generate_csi500_data.py`
2. **Enriquecimento**: `get_csi500_english.py`
3. **Download de preços do índice**: `get_csi500_prices.py`
4. **Divisão em partes**: `split_csi500.py` e `split_csv.py`
5. **Análise**: Use os arquivos `*_part1.csv` e `*_part2.csv`

## 📄 Última Atualização

Novembro 2024

## ⚙️ Estrutura de Commits

O projeto usa git para versionamento. Para contribuições:
- Faça commits claros e descritivos
- Mantenha a estrutura de pastas
- Documente mudanças no README