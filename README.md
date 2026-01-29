# Teste Técnico IntuitiveCare — ETL e Análise de Dados (ANS)

## 1. Origem dos Dados
- Fonte oficial: ANS — Indicadores Econômico-Financeiros (IAP)  
  https://dadosabertos.ans.gov.br/FTP/PDA/IAP/
- Arquivo utilizado: `iap.csv` (download manual realizado em jan/2026)
- Observação: tentativas de download automático foram realizadas, porém o servidor da ANS não disponibilizou listagem consistente de arquivos por período, inviabilizando automação completa nesta etapa.

## 2. O que foi feito
- Leitura e normalização do CSV original
- Padronização de nomes de colunas
- Extração de CNPJ e Razão Social
- Conversão de dados mensais para agregação trimestral
- Agregação por operadora, ano e trimestre
- Geração de dataset consolidado (`consolidado_despesas.csv`)
- Remoção de trimestres e operadoras sem movimentação (`consolidado_despesas_limpo.csv`)
- Cálculo da média trimestral de despesas por operadora
- Geração de ranking das 5 operadoras com maior média trimestral
- Visualização dos resultados por meio de gráficos

## 3. Sobre os Valores Apresentados
- O campo `valor_despesas` representa um indicador econômico-financeiro extraído do IAP da ANS.
- O arquivo original não explicita de forma direta a unidade (ex: R$ milhões ou índice financeiro).
- Considera-se, portanto, que os valores representam indicadores comparáveis entre operadoras, sendo adequados para análise relativa e ranking.
- Para uso financeiro oficial, recomenda-se validação com a documentação técnica da ANS.

## 4. Como Executar
1. Instale as dependências:
   ```bash
   pip install pandas matplotlib
Execute o processamento dos dados:

python src/process_iap.py
Gere as visualizações:

python src/plot_iap_analysis.py
Os arquivos finais estarão disponíveis em:

data/processed/
├── consolidado_despesas.csv
├── consolidado_despesas_limpo.csv
└── figs/
    ├── top5_operadoras_bar.png
    
5. Resultados
Top 5 operadoras por média trimestral de despesas:

CNPJ	Razão Social	Média Trimestral
406708	A.P.S ASSISTÊNCIA PERSONALIZADA À SAÚDE LTDA	225.74
324213	UNIMED NORTE/NORDESTE-FEDERAÇÃO INTERFEDERATIVA	185.36
419362	HOSPITAL BOM SAMARITANO S/S LTDA	179.50
402478	ORALCLASS ASSISTÊNCIA MÉDICA E ODONTOLÓGICA LTDA	152.05
418781	SAÚDE CASSEB ASSISTÊNCIA MÉDICA LTDA	146.19
Os gráficos gerados permitem observar tanto o ranking médio quanto a evolução trimestral das despesas dessas operadoras ao longo do tempo.

6. Conclusão
O pipeline ETL foi implementado com foco em clareza, rastreabilidade e reprodutibilidade.

A análise permite identificar operadoras com maior nível médio de despesas e observar tendências temporais.

O projeto pode ser facilmente estendido para novas métricas, períodos adicionais ou integração com outras bases da ANS.