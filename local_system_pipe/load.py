import psycopg2
import os
import boto3
from io import StringIO

# PostgreSQL Configuration
DB_NAME = 'your_database_name'
DB_USER = 'your username'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_PORT = '5432'
#SCHEMA_NAME = 'cryptoschema'
TABLE_NAME = 'btcusdt' ##update your table name here


# S3 transformed file URL 
S3_FILE_URL = 's3://transformedcryptodatabucket/refined_cryptodata.csv'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)



cursor = conn.cursor()

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
obj = s3.get_object(Bucket='transformedcryptodatabucket', Key='refined_cryptodata.csv')
data = obj['Body'].read().decode('utf-8')

# Load data into PostgreSQL
buffer = StringIO(data)
next(buffer)
cursor.copy_from(buffer, f'{TABLE_NAME}', sep=',')
conn.commit()

# Close connection
cursor.close()
conn.close()

print(f"Data loaded from S3 into PostgreSQL table {TABLE_NAME}")