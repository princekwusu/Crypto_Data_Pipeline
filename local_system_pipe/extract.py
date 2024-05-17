from datetime import datetime
import boto3
import os
import csv
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

# Your AWS keys 
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

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
        "20 April, 2020",
        datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    filename = f"{symbol}_{interval}.csv"
    
    # Check if file exists in S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3_raw_bucket_name = 'rawcryptodatabucket'

    
    # try:
    #     s3_client.head_object(Bucket=s3_raw_bucket_name, Key=filename)
    #     file_exists = True
    # except:
    #     file_exists = False
    
    # Write klines data to local CSV file
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                             'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore', 'order_book'])
        writer.writerows(klines)
    
    # Upload file to s3
    s3_client.upload_file(filename, s3_raw_bucket_name, filename)

    # Remove local CSV file
    os.remove(filename)

def main():
    extractdata_intos3('BTCUSDT','1h')
    print("Data has been extracted successfully")

main()
