CREATE TABLE IF NOT EXISTS public.my_first_dbt_model
(
    id integer
);

INSERT INTO public.my_first_dbt_model(
	id)
VALUES
(1),
(NULL);