--this script should be executed on snowflake worksheet

--creating warehous
CREATE WAREHOUSE CRYPTO_WH;

--defining database
CREATE DATABASE cryptodb;
CREATE schema cryptoschema;
CREATE TABLE cryptodb.cryptoschema.btcusdt(
Open_time timestamp,
Open float,
High float,
Low float,
Close float,
Volume float,
Quote_asset_volume float,
Num_trades bigint,
Taker_base_vol float,
Taker_quote_vol float,
Price_diff float,
Price_change float
);



--select statement to verify table creation
SELECT * FROM cryptodb.cryptoschema.btcusdt;


--file format object creation     
CREATE  or replace SCHEMA file_format;
-- creation of file format
CREATE OR REPLACE file format cryptodb.file_format.format_csv
    type = 'CSV'
    field_delimiter = ','
    RECORD_DELIMITER = '\n'
    skip_header = 1

    
    

--stage schema creation
CREATE or replace SCHEMA external_stage;

--stage creation
CREATE OR REPLACE STAGE cryptodb.external_stage.crypto_ext_stage 
    url="s3://transformedcryptodatabucket/"
    credentials=(aws_key_id='aws_access_keys'
    aws_secret_key='aws_secrete key')
    FILE_FORMAT = cryptodb.file_format.format_csv;

--listing available stages
list @cryptodb.external_stage.crypto_ext_stage;



-- schema creation for snowpipe
CREATE OR REPLACE SCHEMA cryptodb.snowpipe;

--Create Pipe for market two data 
CREATE OR REPLACE PIPE cryptodb.snowpipe.refineddatapipe
AUTO_INGEST = TRUE
AS
COPY INTO cryptodb.cryptoschema.btcusdt
FROM @cryptodb.external_stage.crypto_ext_stage
PATTERN = '.*refined_cryptodata.csv';


--Describing  Pipe
DESC PIPE cryptodb.snowpipe.refineddatapipe;



