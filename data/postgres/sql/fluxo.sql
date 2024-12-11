CREATE TABLE IF NOT EXISTS public.fluxo
(
    plano_de_contas character varying(255) COLLATE pg_catalog."default",
    valor numeric(10,2),
    data date,
    unidade character varying(255) COLLATE pg_catalog."default"
);

INSERT INTO public.fluxo(
	plano_de_contas, valor, data, unidade)
VALUES
('Mensalidade','10000.00','2024-07-01','Ipatinga'),
('Salarios','1500.50','2024-07-02','Timoteo'),
('Devolucao Holding','2000.75','2024-07-03','Alfenas'),
('Antecipacao de Dividendos','2500.25','2024-07-04','Carrao'),
('Mensalidade','10000.00','2024-07-01','Ipatinga'),
('Salarios','1500.50','2024-07-02','Timoteo'),
('Devolucao Holding','2000.75','2024-07-03','Alfenas'),
('Antecipacao de Dividendos','2500.25','2024-07-04','Carrao'),
('Mensalidade','10000.00','2024-07-01','Ipatinga'),
('Salarios','1500.50','2024-07-02','Timoteo'),
('Devolucao Holding','2000.75','2024-07-03','Alfenas'),
('Antecipacao de Dividendos','2500.25','2024-07-04','Carrao'),
('Mensalidade','10000.00','2024-07-01','Ipatinga'),
('Salarios','1500.50','2024-07-02','Timoteo'),
('Devolucao Holding','2000.75','2024-07-03','Alfenas'),
('Antecipacao de Dividendos','2500.25','2024-07-04','Carrao');