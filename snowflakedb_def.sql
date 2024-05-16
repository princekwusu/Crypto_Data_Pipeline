--this script should be executed on snowflake

--defining database
CREATE DATABASE cryptodb;
CREATE schema cryptoschema;
CREATE TABLE cryptodb.cryptoschema.btcusd(
open_time int,
open float,
high float,
low float,
close float,
volume float,
close_time int,
quote_asset_volume float,
num_trades int,
taker_base_vol float,
taker_quote_vol float,
ignore int
);



--select statement to verify table creation
SELECT * FROM cryptodb.cryptoschema.btcusd LIMIT 10;


--file format object creation
CREATE SCHEMA file_format;

CREATE OR REPLACE file format cryptodb.file_format.format_csv
    type = 'CSV'
    field_delimiter = ','
    RECORD_DELIMITER = '\n'
    skip_header = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    
    

--stage schema creation
CREATE SCHEMA external_stage;

--stage creation
CREATE OR REPLACE STAGE cryptodb.external_stage.crypto_ext_stage 
    url="s3://transformedcryptodatabucket/"
    credentials=(aws_key_id='keyid'
    aws_secret_key='secretkey')
    FILE_FORMAT = cryptodb.file_format.format_csv;

list @cryptodb.external_stage.crypto_ext_stage;

-- schema creation for snowpipe

CREATE OR REPLACE SCHEMA cryptodb.snowpipe;


CREATE OR REPLACE PIPE cryptodb.snowpipe.refineddatapipe
AUTO_INGEST = TRUE
AS
COPY INTO cryptodb.cryptoschema.btcusd
FROM @cryptodb.external_stage.crypto_ext_stage
PATTERN = '.*refined_cryptodata.csv';





DESC PIPE cryptodb.snowpipe.refineddatapipe;

TRUNCATE TABLE cryptodb.cryptoschema.btcusd;





