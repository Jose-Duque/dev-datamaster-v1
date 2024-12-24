import os
from datetime import datetime, timedelta, date

import sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from dags.models.TransformToSilver import TransformToSilver
from dags.utils.common import *

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup
from airflow import Dataset

from astro import sql as aql
from astro.constants import FileType
from astro.files import File
from astro.table import Table, Metadata

from airflow.providers.google.cloud.transfers.s3_to_gcs import S3ToGCSOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.cloud_storage_transfer_service import CloudDataTransferServiceGCSToGCSOperator
from airflow.providers.google.cloud.hooks.cloud_storage_transfer_service import GcpTransferOperationStatus
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteObjectsOperator
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from astronomer.providers.snowflake.operators.snowflake import SnowflakeOperatorAsync
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.snowflake.transfers.s3_to_snowflake import S3ToSnowflakeOperator

AWS_SOURCE_SYNC_ZONE_PATH = "s3-dev-datamaster"
GCP_LANDING_BUCKET_PATH = "gcp-brsp-dev-datamaster"
GCP_PROCESSING_BUCKET_PATH = "gcp-brsp-dev-datamaster"
GCP_DEST_SYNC_ZONE_PATH = f"estados/raw/dt_ingest_{date.today()}"
AWS_CONN_ID = "aws_default"
GCS_CONN_ID = "google_cloud_default"
POSTGRES_CONN_ID = "postgres"
SNOWFLAKE_CONN_ID = "snowflake_default"
WAIT_FOR_OPERATION_POKE_INTERVAL = int(os.environ.get("WAIT_FOR_OPERATION_POKE_INTERVAL", 5))


S3_BUCKET = AWS_SOURCE_SYNC_ZONE_PATH  # Substitua pelo seu bucket S3
S3_KEY_INPUT = f"veiculos/bronze/dt_ingest_{date.today()}.json" # Caminho para o arquivo de entrada no S3
S3_KEY_OUTPUT = f"veiculos/silver/dt_ingest_{date.today()}.json" # Caminho para o arquivo de saída no S3

# default args & init dag
current_date = datetime.now()
get_year = current_date.year
get_month = current_date.month
get_day = current_date.day
get_hour = current_date.hour

silver = TransformToSilver

default_args = {
    "owner": "duque",
    "retries": 1,
    "retry_delay": 0
}
# declare dag
@dag(
    dag_id="extract-sync-s3-to-gcs-json-files-hourly",
    start_date=datetime(2022, 11, 22),
    max_active_runs=1,
    schedule_interval=timedelta(hours=1),
    default_args=default_args,
    catchup=False,
    tags=['hourly', 'development', 'ingestion', 's3', 'gcs']
)
# init main function
def ingest_data():
    
    # set tasks

    # init
    init = EmptyOperator(task_id="init")
      
    with TaskGroup("extract_data") as task_group_storage_s3:
        tabelas = ["cidades","concessionarias","estados"]

        for tabela in tabelas:
            postgres_table = Table(name=tabela, conn_id=POSTGRES_CONN_ID, metadata=Metadata(schema="public"))
            path =  f"s3://s3-dev-datamaster/{tabela}/bronze/dt_ingest_{date.today()}.json"
            aql.export_to_file(
                task_id=tabela,
                input_data=postgres_table,
                output_file=File(path,
                    conn_id=AWS_CONN_ID,
                    filetype=FileType.JSON
                ),
                if_exists="replace"
            )

    with TaskGroup("carregar_tabela") as carregar_tabela_to_db:
        tabelas =  ["cidades","concessionarias","estados"]
        carregar_tabela(tabelas,POSTGRES_CONN_ID,AWS_CONN_ID)

    with TaskGroup("salvar_tabela_s3") as salvar_tabela_to_s3:
        tabelas =  ["cidades","concessionarias","estados"]
        salvar_tabela_s3(tabelas,POSTGRES_CONN_ID)

    with TaskGroup("export_table_to_s3") as exportar_tabela_silver_s3:
        tabelas =  ["cidades","concessionarias","estados"]
        export_table_to_s3(tabelas,POSTGRES_CONN_ID,AWS_CONN_ID)
    
    with TaskGroup("export_table_to_snowflake") as export_tabela_to_snowflake:
        tabelas =  ["cidades","concessionarias","estados"]
        export_table_to_snowflake(tabelas,AWS_CONN_ID,SNOWFLAKE_CONN_ID)

    with TaskGroup("drop_table_tmp") as drop_tabela_temporaria:
        tabelas =  ["cidades","concessionarias","estados"]
        drop_table_tmp(tabelas,POSTGRES_CONN_ID) 

    create_bucket_grant_full_control = S3CreateBucketOperator(
        task_id="create_s3_bucket_grant_full_control",
        bucket_name="datamaster-test-create-bucket",  # Replace with a unique bucket name
        region_name="us-east-2",
        aws_conn_id=AWS_CONN_ID,
    )

    # finish
    finish = EmptyOperator(task_id="finish")

    # define sequence
    chain(init,
          create_bucket_grant_full_control, 
          task_group_storage_s3,
          carregar_tabela_to_db,
          salvar_tabela_to_s3,
          exportar_tabela_silver_s3,
          [export_tabela_to_snowflake, drop_tabela_temporaria],
          finish
    )


# init dag
dag = ingest_data()