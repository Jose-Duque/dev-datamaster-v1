CREATE TABLE IF NOT EXISTS public.op_faturamento
(
    plano_de_contas character varying(255) COLLATE pg_catalog."default",
    operacao character varying(255) COLLATE pg_catalog."default",
    segmento character varying(255) COLLATE pg_catalog."default",
    valor numeric(10,2),
    data date,
    unidade character varying(255) COLLATE pg_catalog."default"
);

INSERT INTO public.op_faturamento(
	plano_de_contas, operacao, segmento, valor, data, unidade)
VALUES
('Mensalidade','Faturamento','Academia',NULL,NULL,NULL),
('Salarios','Despesas','Academia',NULL,NULL,NULL);