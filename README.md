🧪 Teste Técnico IntuitiveCare — ETL e Análise de Dados (ANS)
📌 1. Origem dos Dados

Fonte oficial: ANS — Indicadores Econômico-Financeiros (IAP)
🔗 https://dadosabertos.ans.gov.br/FTP/PDA/IAP/

Arquivo utilizado: iap.csv

Download: realizado manualmente em jan/2026

Observação:
Foram realizadas tentativas de download automático, porém o servidor da ANS não disponibilou uma listagem consistente de arquivos por período, o que inviabilizou a automação completa nesta etapa.

⚙️ 2. O que foi feito

Leitura e normalização do CSV original

Padronização dos nomes de colunas

Extração de CNPJ e Razão Social

Conversão de dados mensais → trimestrais

Agregação por:

Operadora

Ano

Trimestre

Geração de dataset consolidado:

consolidado_despesas.csv

Remoção de trimestres e operadoras sem movimentação:

consolidado_despesas_limpo.csv

Cálculo da média trimestral de despesas por operadora

Geração do ranking das Top 5 operadoras

Criação de visualizações gráficas para apoio à análise

📊 3. Sobre os Valores Apresentados

O campo valor_despesas representa um indicador econômico-financeiro extraído do IAP da ANS.

O arquivo original não explicita de forma direta a unidade (ex.: R$ milhões ou índice financeiro).

Os valores foram tratados como indicadores comparáveis, adequados para:

Análises relativas

Rankings

Evolução temporal

Para uso financeiro oficial, recomenda-se validação com a documentação técnica da ANS.

▶️ 4. Como Executar
4.1 Instalar dependências
pip install pandas matplotlib

4.2 Processar os dados
python src/process_iap.py

4.3 Gerar visualizações
python src/plot_iap_analysis.py

4.4 Estrutura de saída
data/processed/
├── consolidado_despesas.csv
├── consolidado_despesas_limpo.csv
└── figs/
    ├── top5_operadoras_bar.png
    └── evolucao_top5.png

🏆 5. Resultados
Top 5 operadoras por média trimestral de despesas
CNPJ	Razão Social	Média Trimestral
406708	A.P.S ASSISTÊNCIA PERSONALIZADA À SAÚDE LTDA	225.74
324213	UNIMED NORTE/NORDESTE – FEDERAÇÃO INTERFEDERATIVA	185.36
419362	HOSPITAL BOM SAMARITANO S/S LTDA	179.50
402478	ORALCLASS ASSISTÊNCIA MÉDICA E ODONTOLÓGICA LTDA	152.05
418781	SAÚDE CASSEB ASSISTÊNCIA MÉDICA LTDA	146.19

Os gráficos permitem visualizar:

📊 O ranking médio das operadoras

📈 A evolução trimestral das despesas ao longo do tempo

✅ 6. Conclusão

O pipeline ETL foi implementado com foco em:

Clareza

Rastreabilidade

Reprodutibilidade

A análise permite identificar:

Operadoras com maior nível médio de despesas

Tendências ao longo dos trimestres

O projeto está estruturado para:

Inclusão de novas métricas

Expansão para outros períodos

Integração com novas bases da ANS
