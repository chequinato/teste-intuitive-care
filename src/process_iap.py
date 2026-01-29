import pandas as pd
import re
from pathlib import Path
import unicodedata

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Função para remover acentuação e normalizar nomes de colunas
def normalize_col(col):
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
    return col.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')

# Função para extrair CNPJ do campo de razão social
def extract_cnpj(razao):
    match = re.search(r'\((\d{6,})\)', razao)
    return match.group(1) if match else None

def month_to_quarter(month):
    if month in [1,2,3]: return 1
    if month in [4,5,6]: return 2
    if month in [7,8,9]: return 3
    if month in [10,11,12]: return 4
    return None

def process_iap_csv(input_path):
    # Lê o CSV, tenta encoding utf-8 e fallback para latin1
    try:
        df = pd.read_csv(input_path, sep=';', encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(input_path, sep=';', encoding='latin1')
    # Normaliza nomes de colunas
    df.columns = [normalize_col(c) for c in df.columns]
    # Extrai CNPJ e limpa razão social
    df['cnpj'] = df['razao_social_registro_ans'].apply(extract_cnpj)
    df['razao_social'] = df['razao_social_registro_ans'].apply(lambda x: re.sub(r'\s*\(\d+\)', '', x).strip())
    # Identifica colunas de meses (ex: jan/22, fev/22, ...)
    meses = [c for c in df.columns if re.match(r'^[a-z]{3}_\d{2}$', c) or re.match(r'^[a-z]{3}/\d{2}$', c) or re.match(r'^\w{3}/\d{2}$', c)]
    # Transforma para formato longo
    df_long = df.melt(id_vars=['cnpj', 'razao_social'], value_vars=meses, var_name='mes_ano', value_name='valor_despesas')
    # Remove valores nulos e converte para float
    df_long = df_long.dropna(subset=['valor_despesas'])
    df_long['valor_despesas'] = df_long['valor_despesas'].astype(str).str.replace(',', '.').str.replace(' ', '').astype(float)
    # Extrai mês e ano
    def parse_mes_ano(s):
        s = s.replace('_', '/').lower()
        meses = {'jan':1,'fev':2,'mar':3,'abr':4,'mai':5,'jun':6,'jul':7,'ago':8,'set':9,'out':10,'nov':11,'dez':12}
        m = re.match(r'([a-z]{3})/(\d{2})', s)
        if m:
            mes = meses.get(m.group(1))
            ano = int('20'+m.group(2))
            return mes, ano
        return None, None
    df_long[['mes','ano']] = df_long['mes_ano'].apply(lambda x: pd.Series(parse_mes_ano(x)))
    df_long = df_long.dropna(subset=['mes','ano'])
    df_long['trimestre'] = df_long['mes'].apply(month_to_quarter)
    # Agrupa por CNPJ, Razão Social, Ano, Trimestre
    df_trim = df_long.groupby(['cnpj','razao_social','ano','trimestre'], as_index=False)['valor_despesas'].sum()
    # Salva consolidado
    out_path = PROCESSED_DIR / 'consolidado_despesas.csv'
    df_trim.to_csv(out_path, index=False, encoding='utf-8')
    print(f"Consolidado salvo em {out_path}")
    return df_trim

if __name__ == "__main__":
    process_iap_csv(RAW_DIR / "iap (1).csv")
