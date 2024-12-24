from datetime import date
from astro import sql as aql
from astro.constants import FileType
from astro.files import File
from astro.table import Table, Metadata
from dags.models.TransformToSilver import TransformToSilver

# S3_BUCKET = "s3-dev-datamaster"
# S3_KEY_INPUT = f"s3-dev-datamaster/veiculos/bronze/dt_ingest_{date.today()}.json" # Caminho para o arquivo de entrada no S3
# S3_KEY_OUTPUT = f"s3-dev-datamaster/veiculos/silver/dt_ingest_{date.today()}.json" # Caminho para o arquivo de saída no S3


def extract_data_to_s3(DB_CONN_ID: str, CLOUD_CONN_ID: str):
    tabelas = ["cidades","concessionarias","estados","fluxo","op_faturamento","veiculos","vendas","vendedores"]
    for table in tabelas:
        postgres_table = Table(name=table, conn_id=DB_CONN_ID, metadata=Metadata(schema="public"))
        path =  f"s3://s3-dev-datamaster/{table}/bronze/dt_ingest_{date.today()}.json"
        aql.export_to_file(
            task_id=table,
            input_data=postgres_table,
            output_file=File(path,
                conn_id=CLOUD_CONN_ID,
                filetype=FileType.JSON
            ),
            if_exists="replace"
        )

def carregar_tabela(tables: list, DB_CONN_ID: str, CLOUD_CONN_ID: str):  
    for table in tables:
        aql.load_file(
                task_id=table,
                input_file=File(f"s3://s3-dev-datamaster/{table}/bronze/dt_ingest_{date.today()}.json", conn_id=CLOUD_CONN_ID), # Conexão AWS no Airflow
                output_table=Table(name=f"s3_input_table_{table}_v2", temp=True, conn_id=DB_CONN_ID)
        )


def salvar_tabela_s3(tables: list, DB_CONN_ID: str):
    silver = TransformToSilver
    for table in tables:
        dicionario_funcoes = {
            'cidades': silver.cidades,
            'estados': silver.estados,
            'concessionarias': silver.concessionarias
        }
        funcao = dicionario_funcoes[table]
        funcao(
            table = Table(name=f"s3_input_table_{table}_v2", temp=True, conn_id=DB_CONN_ID),
            output_table=Table(name=f"s3_output_table_{table}_v2"),
        )

def export_table_to_s3(tables: list, DB_CONN_ID: str, CLOUD_CONN_ID: str):
    for table in tables:
        aql.export_to_file(
                task_id=table,
                input_data=Table(name=f"s3_output_table_{table}_v2", conn_id=DB_CONN_ID),
                output_file=File(f"s3://s3-dev-datamaster/{table}/silver/dt_ingest_{date.today()}.json", conn_id=CLOUD_CONN_ID), # Conexão AWS no Airflow
                if_exists="replace" # Opções: "replace", "append", "raise"
            )

def export_table_to_snowflake(tables: list, CLOUD_CONN_ID: str, DW_CONN_ID):
    for table in tables:
        aql.load_file(
            task_id=table,
            input_file=File(path=f"s3://s3-dev-datamaster/{table}/silver/dt_ingest_{date.today()}.json", conn_id=CLOUD_CONN_ID),
            output_table=Table(name=f"silver_{table}",
                conn_id=DW_CONN_ID,
            ),
            assume_schema_exists=True,
            if_exists="replace",
            use_native_support=True,
            columns_names_capitalization="original"
        )

def drop_table_tmp(tables: list, DB_CONN_ID):
    for table in tables:
        tbs = {
            f"tb_input_{table}": f"s3_input_table_{table}_v2",
            f"tb_output_{table}": f"s3_output_table_{table}_v2",
        }
        for tb in tbs.values():
            aql.drop_table(
                task_id=tb,
                table=Table(name=tb, conn_id=DB_CONN_ID)
            )