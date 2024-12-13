import os
from datetime import datetime, timedelta, date
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup

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

AWS_SOURCE_SYNC_ZONE_PATH = "s3-dev-datamaster"
GCP_LANDING_BUCKET_PATH = "gcp-brsp-dev-datamaster"
GCP_PROCESSING_BUCKET_PATH = "gcp-brsp-dev-datamaster"
GCP_DEST_SYNC_ZONE_PATH = f"estados/raw/dt_ingest_{date.today()}"
AWS_CONN_ID = "aws_default"
GCS_CONN_ID = "google_cloud_default"
POSTGRES_CONN_ID = "postgres"
WAIT_FOR_OPERATION_POKE_INTERVAL = int(os.environ.get("WAIT_FOR_OPERATION_POKE_INTERVAL", 5))

# default args & init dag
current_date = datetime.now()
get_year = current_date.year
get_month = current_date.month
get_day = current_date.day
get_hour = current_date.hour

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
    init = DummyOperator(task_id="init")

    # transfer_postgres_to_gcs = PostgresToGCSOperator(
    #     task_id="transfer_postgres_to_gcs",
    #     sql="SELECT * FROM public.estados",
	#     bucket=GCP_LANDING_BUCKET_PATH,
	#     filename=f"{GCP_DEST_SYNC_ZONE_PATH}.parquet",
	#     export_format="parquet",
	#     gzip=False,
	#     gcp_conn_id=GCS_CONN_ID,
	#     postgres_conn_id=POSTGRES_CONN_ID,
    # )
    
    
  
    # export_file_to_gcs = aql.export_to_file(
    #     task_id="transfer_postgresFile_to_s3",
    #     input_data=postgres_table,
    #     output_file=File(
    #         path=f"s3://s3-dev-datamaster/vendedores/bronze/dt_ingest_{date.today()}.parquet",
    #         conn_id=AWS_CONN_ID,
    #         filetype=FileType.PARQUET
    #     ),
    #     if_exists="replace"
    # )
   
      
    with TaskGroup("extract_data") as task_group_storage_s3:
        tabelas = ["cidades","clientes","concessionarias","estados","fluxo","op_faturamento","veiculos","vendas","vendedores"]

        for tabela in tabelas:
            postgres_table = Table(name=tabela, conn_id=POSTGRES_CONN_ID, metadata=Metadata(schema="public"))
            path =  f"s3://s3-dev-datamaster/{tabela}/bronze/dt_ingest_{date.today()}.parquet"
            aql.export_to_file(
                task_id=tabela,
                input_data=postgres_table,
                output_file=File(path,
                    conn_id=AWS_CONN_ID,
                    filetype=FileType.PARQUET
                ),
                if_exists="replace"
            )
        

    # carregar dados em dataframe
    # dataframe = aql.load_file(
    #     task_id="gcs_to_dataframe",
    #     input_file=File(path="gs://gcp-brsp-dev-datamaster/estados/raw/dt_ingest_2024-12-11.parquet"),
    # )
    
    # def column(df):
    #     df['dt_ingest']
    #     print("##############",df, "################")
    #     return df

    # test_to_broze = aql.export_file(
    #         task_id="save_dataframe_to_gcs",
    #         input_data=column(dataframe),
    #         output_file=File(
    #             path="gs://gcp-brsp-dev-datamaster/estados/siver/dt_ingest_2024-12-11.parquet",
    #             conn_id=GCS_CONN_ID,
    #         ),
    #         if_exists="replace",
    #     )

    # delete_file_task = GCSDeleteObjectsOperator(
    #     task_id='delete_file_from_gcs',
    #     bucket_name=GCP_LANDING_BUCKET_PATH,
    #     objects=[f"{GCP_DEST_SYNC_ZONE_PATH}"],
    #     gcp_conn_id=GCS_CONN_ID
    # )

    # def transfer_data_to_s3(**kwargs):
    #     postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    #     s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
        
    #     # Fetch data from Postgres
    #     query = "SELECT * FROM public.cidades;"
    #     records = postgres_hook.get_records(query)
        
    #     # Process records and convert to desired format (e.g., CSV)
    #     csv_data = '\n'.join([','.join(map(str, record)) for record in records])
        
    #     # Save data to S3
    #     s3_hook.load_string(csv_data, bucket_name=AWS_SOURCE_SYNC_ZONE_PATH, key='your_file_name.csv', replace=True)

    # # Trav=sferir aquivo
    # transfer_task = PythonOperator(
    #     task_id='transfer_data',
    #     python_callable=load_data,
    #     provide_context=True,
    # )

    # s3 to gcs = user
    # sync_s3_to_gcs_user_json_files = S3ToGCSOperator(
    #     task_id="sync_s3_to_gcs_user_json_files",
    #     bucket=AWS_SOURCE_SYNC_ZONE_PATH,
    #     prefix="cadastro/",
    #     dest_gcs="gs://gcp-brsp-dev-datamaster",
    #     replace=False,
    #     gzip=False,
    # )


    # # create bucket for processing
    create_processing_bucket = GCSCreateBucketOperator(
    task_id="create_processing_bucket",
    bucket_name=GCP_PROCESSING_BUCKET_PATH,
    storage_class="REGIONAL",
    location="US-EAST1"
    )

    create_bucket_grant_full_control = S3CreateBucketOperator(
        task_id="create_s3_bucket_grant_full_control",
        bucket_name="datamaster-test-create-bucket",  # Replace with a unique bucket name
        region_name="us-east-2",
        aws_conn_id=AWS_CONN_ID,
    )

    # finish
    finish = DummyOperator(task_id="finish")

    # define sequence
    chain(init, create_processing_bucket, task_group_storage_s3, create_bucket_grant_full_control, finish)


# init dag
dag = ingest_data()