-- dbt test
WITH vendas_comparacao_preco AS (
    SELECT
        f.venda_id,
        f.valor_venda,
        d.valor_sugerido,
        CASE
            WHEN f.valor_venda <= d.valor_sugerido AND f.valor_venda >= d.valor_sugerido * 0.95 THEN TRUE
            ELSE FALSE
        END AS regra_respeitada
    FROM {{ source('sources', 'silver_vendas') }} f
    JOIN {{ source('sources', 'silver_veiculos') }} d ON f.veiculo_id = d.veiculo_id
)

SELECT venda_id, valor_venda, valor_sugerido
FROM vendas_comparacao_preco
WHERE regra_respeitada = FALSE
