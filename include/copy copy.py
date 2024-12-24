# load_s3_to_table = aql.load_file(
#         task_id="load_s3_to_table",
#         input_file=File(f"s3://{S3_BUCKET}/{S3_KEY_INPUT}", conn_id=AWS_CONN_ID), # Conexão AWS no Airflow
#         output_table=Table(name="s3_input_table", temp=True, conn_id=POSTGRES_CONN_ID)
#     )

#     test_datasets = silver.s_veiculos(
#         s3_input_table_veiculos=load_s3_to_table,
#         output_table=Table(name="s3_output_table"),
#     )

#     export_table_to_s3 = aql.export_to_file(
#         task_id="export_table_to_s3",
#         input_data=Table(name="s3_output_table",conn_id=POSTGRES_CONN_ID),
#         output_file=File(f"s3://{S3_BUCKET}/{S3_KEY_OUTPUT}", conn_id=AWS_CONN_ID), # Conexão AWS no Airflow
#         if_exists="replace" # Opções: "replace", "append", "raise"
#     )

#     estados_snowflake = aql.load_file(
#         input_file=File(path=f"s3://s3-dev-datamaster/veiculos/silver/dt_ingest_{date.today()}.json", conn_id=AWS_CONN_ID),
#         output_table=Table(name="tb_veiculos",
#             conn_id=SNOWFLAKE_CONN_ID,
#         ),
#         assume_schema_exists=True,
#         if_exists="replace",
#         use_native_support=True,
#         columns_names_capitalization="original"
#     )




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
    # create_processing_bucket = GCSCreateBucketOperator(
    # task_id="create_processing_bucket",
    # bucket_name=GCP_PROCESSING_BUCKET_PATH,
    # storage_class="REGIONAL",
    # location="US-EAST1"
    # )