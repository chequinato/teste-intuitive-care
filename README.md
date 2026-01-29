# Teste Técnico Intuitive Care — ETL e Análise de Dados ANS

## 1. Origem dos Dados
- Fonte: [ANS - Indicadores Econômico-Financeiros (IAP)](https://dadosabertos.ans.gov.br/FTP/PDA/IAP/)
- Arquivo utilizado: iap.csv (baixado manualmente em Jan/2026)
- Observação: O download automático não foi possível devido a limitações do servidor ANS (detalhes no log/tentativas_download.json).

## 2. O que foi feito
- Leitura e normalização do CSV original
- Extração de CNPJ e Razão Social
- Conversão de valores mensais para trimestres
- Agregação por operadora, ano e trimestre
- Geração de dataset consolidado (`consolidado_despesas.csv`)
- Filtragem para remover trimestres/operadoras sem movimentação (`consolidado_despesas_limpo.csv`)
- Cálculo da média trimestral de despesas por operadora
- Geração do ranking das 5 maiores operadoras por média trimestral (`top5_operadoras_media_trimestral.csv`)

## 3. Significado dos Números
- Os valores de `valor_despesas` representam indicadores extraídos do IAP da ANS.
- Não há nota técnica clara no CSV, mas normalmente são valores em R$ milhões ou índices financeiros.
- Recomenda-se consultar a documentação oficial da ANS para confirmação da unidade.

## 4. Como rodar
1. Instale as dependências:
   ```
   pip install pandas
   ```
2. Execute o processamento:
   ```
   python src/process_iap.py
   ```
3. Os resultados estarão em `data/processed/`.

## 5. Resultados
- Top 5 operadoras por média trimestral de despesas:

| CNPJ    | Razão Social                                         | Média Trimestral |
|---------|------------------------------------------------------|------------------|
| 406708  | A.P.S ASSISTÊNCIA PERSONALIZADA À SAÚDE LTDA         | 225.74           |
| 324213  | UNIMED NORTE/NORDESTE-FEDERAÇÃO INTERFEDERATIVA      | 185.36           |
| 419362  | HOSPITAL BOM SAMARITANO S/S LTDA                     | 179.50           |
| 402478  | ORALCLASS ASSISTENCIA MÉDICA E ODONTOLOGICA LTDA.    | 152.05           |
| 418781  | SAUDE CASSEB ASSISTENCIA MEDICA LTDA                 | 146.19           |

## 6. Conclusão
- O pipeline ETL foi implementado com sucesso, entregando dados limpos e análise objetiva.
- O significado exato dos valores pode variar conforme a metodologia da ANS; consulte sempre a fonte oficial.
- O código está pronto para ser expandido para outras análises ou integrações.

---

> Dúvidas, limitações e trade-offs estão documentados no código e neste README.
