CREATE TABLE IF NOT EXISTS public.veiculos
(
    id_veiculos integer NOT NULL DEFAULT nextval('veiculos_id_veiculos_seq'::regclass),
    nome character varying(255) COLLATE pg_catalog."default" NOT NULL,
    tipo character varying(100) COLLATE pg_catalog."default" NOT NULL,
    valor numeric(10,2) NOT NULL,
    data_atualizacao timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    data_inclusao timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO public.veiculos(
	id_veiculos, nome, tipo, valor, data_atualizacao, data_inclusao)
VALUES
(1,'AgileXplorer','SUV Compacta','250000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(2,'VoyageRoamer','SUV Média','350000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(3,'EcoPrestige','SUV Premium Híbrida','500000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(4,'WorkMaster','Camionete Média','280000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(5,'DoubleDuty','Camionete Cabine Dupla','320000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(6,'SpeedFury','Superesportivo','800000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(7,'TrailConqueror','Off-road','400000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00'),
(8,'ElegantCruise','Sedã','300000.00','2024-01-28 19:58:27.84701+00','2024-01-28 19:58:27.84701+00');