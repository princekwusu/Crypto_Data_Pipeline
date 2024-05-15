from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from datetime import datetime, timedelta
import boto3
import pandas as pd
from io import BytesIO
import os
import csv
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

# Your AWS keys (replace with your actual keys)
AWS_ACCESS_KEY_ID = 'access key'
AWS_SECRET_ACCESS_KEY = "secrete key"

def extractdata_intos3(symbol, interval):
    client = Client(os.getenv("API_KEY"), os.getenv("SECRET_KEY"))
    interval_map = {
        '1m': client.KLINE_INTERVAL_1MINUTE,
        '3m': client.KLINE_INTERVAL_3MINUTE,
        '5m': client.KLINE_INTERVAL_5MINUTE,
        '15m': client.KLINE_INTERVAL_15MINUTE,
        '30m': client.KLINE_INTERVAL_30MINUTE,
        '1h': client.KLINE_INTERVAL_1HOUR,
        '2h': client.KLINE_INTERVAL_2HOUR,
        '4h': client.KLINE_INTERVAL_4HOUR,
        '6h': client.KLINE_INTERVAL_6HOUR,
        '8h': client.KLINE_INTERVAL_8HOUR,
        '12h': client.KLINE_INTERVAL_12HOUR,
        '1d': client.KLINE_INTERVAL_1DAY,
        '3d': client.KLINE_INTERVAL_3DAY,
        '1w': client.KLINE_INTERVAL_1WEEK,
        '1M': client.KLINE_INTERVAL_1MONTH
    }
    
    klines = client.get_historical_klines(
        symbol,
        interval_map[interval],
        "01 January, 2024",
        datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    filename = f"{symbol}_{interval}.csv"
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                         'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore', 'order_book'])
        writer.writerows(klines)
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3_raw_bucket_name = 'rawcryptodatabucket'
    s3_client.upload_file(filename, s3_raw_bucket_name, filename)

def transformdata_andloadtos3():
    s3_raw_bucket_name = 'rawcryptodatabucket'
    s3_transformed_bucket_name = 'transformedcryptodatabucket'

    # Load raw data from S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    obj = s3.get_object(Bucket=s3_raw_bucket_name, Key='BTCUSDT_1h.csv')
    cryptodata = pd.read_csv(BytesIO(obj['Body'].read()))
    cryptodata = cryptodata.drop(columns=['order_book'])
    
    # Upload transformed data to S3
    with BytesIO() as f:
        cryptodata.to_csv(f, index=False)
        f.seek(0)
        s3.upload_fileobj(f, s3_transformed_bucket_name, 'refined_cryptodata.csv')

    print("Transformed data uploaded to S3 successfully.")

default_args = {
    'owner': 'DE_GROUP',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=15),
}

dag = DAG(
    'CRYPTO_DATA_PIPELINE',
    default_args=default_args,
    description="A pipeline to get data from Binance, transform it, and load it to Redshift",
    schedule_interval="@daily",
    catchup=False
)

with dag:
    extract_data_intos3_task = PythonOperator(
        task_id="extract_dataintoS3",
        python_callable=extractdata_intos3,
        op_kwargs={'symbol': 'BTCUSDT', 'interval': '1h'},
    )

    transform_data_and_load_tos3_task = PythonOperator(
        task_id="transformdata_andloadtos3",
        python_callable=transformdata_andloadtos3,
    )

   


    extract_data_intos3_task >> transform_data_and_load_tos3_task
