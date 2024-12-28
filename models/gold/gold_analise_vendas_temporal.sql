{{ config(materialized='table') }}
SELECT
    DATE_TRUNC('month', TO_TIMESTAMP(data_venda)) AS mes_venda,
    COUNT(venda_id) AS numero_vendas,
    SUM(valor_venda) AS total_vendas,
    AVG(valor_venda) AS valor_medio_venda
FROM {{ source('sources', 'silver_vendas') }}
GROUP BY DATE_TRUNC('month', TO_TIMESTAMP(data_venda))
ORDER BY mes_venda
