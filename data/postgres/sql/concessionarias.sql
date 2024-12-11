CREATE TABLE IF NOT EXISTS public.concessionarias
(
    id_concessionarias integer NOT NULL DEFAULT nextval('concessionarias_id_concessionarias_seq'::regclass),
    concessionaria character varying(255) COLLATE pg_catalog."default" NOT NULL,
    id_cidades integer NOT NULL,
    data_inclusao timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO public.concessionarias(
	id_concessionarias, concessionaria, id_cidades, data_inclusao, data_atualizacao)
VALUES
(1,'Concessionária NovaDrive Motors Rio Branco',1,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(2,'Concessionária NovaDrive Motors Maceió',2,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(3,'Concessionária NovaDrive Motors Macapá',3,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(4,'Concessionária NovaDrive Motors Manaus',4,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(5,'Concessionária NovaDrive Motors Salvador',5,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(6,'Concessionária NovaDrive Motors Fortaleza',6,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(7,'Concessionária NovaDrive Motors Brasília',7,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(8,'Concessionária NovaDrive Motors Vitória',8,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(9,'Concessionária NovaDrive Motors Goiânia',9,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(10,'Concessionária NovaDrive Motors São Luís',10,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(11,'Concessionária NovaDrive Motors Cuiabá',11,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(12,'Concessionária NovaDrive Motors Campo Grande',12,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(13,'Concessionária NovaDrive Motors Belo Horizonte',13,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(14,'Concessionária NovaDrive Motors Belém',14,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(15,'Concessionária NovaDrive Motors João Pessoa',15,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(16,'Concessionária NovaDrive Motors Curitiba',16,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(17,'Concessionária NovaDrive Motors Recife',17,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(18,'Concessionária NovaDrive Motors Teresina',18,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(19,'Concessionária NovaDrive Motors Rio de Janeiro',19,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(20,'Concessionária NovaDrive Motors Natal',20,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(21,'Concessionária NovaDrive Motors Porto Alegre',21,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(22,'Concessionária NovaDrive Motors Porto Velho',22,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(23,'Concessionária NovaDrive Motors Boa Vista',23,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(24,'Concessionária NovaDrive Motors Florianópolis',24,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(25,'Concessionária NovaDrive Motors São Paulo',25,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(26,'Concessionária NovaDrive Motors Aracaju',26,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(27,'Concessionária NovaDrive Motors Palmas',27,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(28,'Concessionária NovaDrive Motors São Paulo Centro',25,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00'),
(29,'Concessionária NovaDrive Motors Rio de Janeiro Centro',19,'2024-01-28 19:59:18.49458+00','2024-01-28 19:59:18.49458+00');