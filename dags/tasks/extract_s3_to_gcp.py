import os
from datetime import datetime, timedelta, date
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator

from astro import sql as aql
from astro.files import File
from astro.table import Table

from airflow.providers.google.cloud.transfers.s3_to_gcs import S3ToGCSOperator
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.cloud_storage_transfer_service import CloudDataTransferServiceGCSToGCSOperator
from airflow.providers.google.cloud.hooks.cloud_storage_transfer_service import GcpTransferOperationStatus
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteObjectsOperator


AWS_SOURCE_SYNC_ZONE_PATH = "s3-dev-datamaster"
GCP_LANDING_BUCKET_PATH = "gcp-brsp-dev-datamaster"
GCP_PROCESSING_BUCKET_PATH = "gcp-brsp-dev-datamaster"
GCP_DEST_SYNC_ZONE_PATH = f"clientes/bronze/dt_ingest_{date.today()}"
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

    transfer_postgres_to_gcs = PostgresToGCSOperator(
        task_id="transfer_postgres_to_gcs",
        sql="SELECT * FROM public.clientes",
	    bucket=GCP_LANDING_BUCKET_PATH,
	    filename=f"{GCP_DEST_SYNC_ZONE_PATH}",
	    export_format="parquet",
	    gzip=False,
	    gcp_conn_id=GCS_CONN_ID,
	    postgres_conn_id=POSTGRES_CONN_ID,
    )

    delete_file_task = GCSDeleteObjectsOperator(
        task_id='delete_file_from_gcs',
        bucket_name=GCP_LANDING_BUCKET_PATH,
        objects=[f"{GCP_DEST_SYNC_ZONE_PATH}"],
        gcp_conn_id=GCS_CONN_ID
    )

    def transfer_data_to_s3(**kwargs):
        postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
        
        # Fetch data from Postgres
        query = "SELECT * FROM public.cidades;"
        records = postgres_hook.get_records(query)
        
        # Process records and convert to desired format (e.g., CSV)
        csv_data = '\n'.join([','.join(map(str, record)) for record in records])
        
        # Save data to S3
        s3_hook.load_string(csv_data, bucket_name=AWS_SOURCE_SYNC_ZONE_PATH, key='your_file_name.csv', replace=True)

    # Trav=sferir aquivo
    transfer_task = PythonOperator(
        task_id='transfer_data',
        python_callable=transfer_data_to_s3,
        provide_context=True,
    )

    # s3 to gcs = user
    sync_s3_to_gcs_user_json_files = S3ToGCSOperator(
        task_id="sync_s3_to_gcs_user_json_files",
        bucket=AWS_SOURCE_SYNC_ZONE_PATH,
        prefix="cadastro/",
        dest_gcs="gs://gcp-brsp-dev-datamaster",
        replace=False,
        gzip=False,
    )


    # # create bucket for processing
    create_processing_bucket = GCSCreateBucketOperator(
    task_id="create_processing_bucket",
    bucket_name=GCP_PROCESSING_BUCKET_PATH,
    storage_class="REGIONAL",
    location="US-EAST1"
    )

    # finish
    finish = DummyOperator(task_id="finish")

    # define sequence
    chain(init,transfer_postgres_to_gcs,transfer_task, sync_s3_to_gcs_user_json_files, create_processing_bucket, delete_file_task, finish)


# init dag
dag = ingest_data()