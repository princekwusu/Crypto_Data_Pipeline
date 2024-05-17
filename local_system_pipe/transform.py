from datetime import datetime, timedelta
import boto3
import pandas as pd
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

#Your AWS keys (replace with your actual keys)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

def transformdata_and_load_to_s3():
    s3_raw_bucket_name = 'rawcryptodatabucket'
    s3_transformed_bucket_name = 'transformedcryptodatabucket'
    filename = 'refined_cryptodata.csv'

    # Load raw data from S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # try:
    #     obj = s3.get_object(Bucket=s3_transformed_bucket_name, Key=filename)
    #     existing_data = pd.read_csv(BytesIO(obj['Body'].read()))
    # except:
    #     existing_data = pd.DataFrame()  

    # Load and transform new data
    raw_obj = s3.get_object(Bucket=s3_raw_bucket_name, Key='BTCUSDT_1h.csv')
    new_data = pd.read_csv(BytesIO(raw_obj['Body'].read()))
    
    # transformation logic
    new_data.drop(columns=['ignore', 'order_book'], inplace=True)
    new_data['open_time'] = pd.to_datetime(new_data['open_time'], unit='ms')
    new_data['close_time'] = pd.to_datetime(new_data['close_time'], unit='ms')
    new_data.set_index('open_time', inplace=True)
    
    new_data_resampled = new_data.resample('D').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum',
        'quote_asset_volume': 'sum',
        'num_trades': 'sum',
        'taker_base_vol': 'sum',
        'taker_quote_vol': 'sum',
    }).reset_index()
    new_data_resampled['price_diff'] = new_data_resampled['high'] - new_data_resampled['low']
    new_data_resampled['price_change'] = new_data_resampled['close'] - new_data_resampled['open']

    # # Append new data to existing data (if exists)
    # if not existing_data.empty:
    #     transformed_data = pd.concat([existing_data, new_data_resampled], ignore_index=True)
    # else:
    #     transformed_data = new_data_resampled
    
    # Upload transformed data to S3
    with BytesIO() as f:
        new_data_resampled.to_csv(f, index=False)
        f.seek(0)
        s3.upload_fileobj(f, s3_transformed_bucket_name, filename)

    print("Transformed data uploaded to S3 successfully.")

def main():
    transformdata_and_load_to_s3()

main()





