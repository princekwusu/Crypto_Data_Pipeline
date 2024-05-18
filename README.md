# Crpto Data Pipeline(Kline Data)

Welcome to our Trade Data Pipeline, a powerful solution for fetching, storing, and analyzing trade data from the Binance API. 
At the heart of this pipeline lies the intricate tapestry of trade data, each thread representing a unique trade executed on the exchange

### Description of Kline Data
Kline data, also known as candlestick data, provides a summarized view of trading activity for a specific trading pair within a given time frame. Each data point, represented by a candlestick, includes information about the opening price, closing price, highest price, lowest price, and trading volume during that period.

#### Contents of Kline Data
The Kline data includes the following fields:
- **open_time**: Timestamp for the start of the candlestick period.
- **open**: Opening price of the asset.
- **high**: Highest price of the asset during the period.
- **low**: Lowest price of the asset during the period.
- **close**: Closing price of the asset.
- **volume**: Total trading volume of the asset during the period.
- **close_time**: Timestamp for the end of the candlestick period.
- **quote_asset_volume**: Total volume of the quote asset traded during the period.
- **num_trades**: Number of trades executed during the period.
- **taker_base_vol**: Total volume of trades taken by the taker during the period.
- **taker_quote_vol**: Total volume of the quote asset traded during the period by takers.
- **ignore**: Placeholder field, not used in analysis.
- **order_book**: Data related to the order book at the time of closing the candlestick.

#### Purpose of Kline Data

The Kline data provides valuable insights for traders, analysts, and researchers, allowing them to:

- Analyze price movements: Identify trends, support, and resistance levels.
- Gauge market sentiment: Determine buying and selling pressure.
- Understand trading volume: Assess liquidity and market activity.
- Develop trading strategies: Use historical data to backtest and optimize trading strategies.
  
#### Example Usage

The provided functions `get_klines()` and `save_klines_to_csv()` allow users to retrieve Kline data for a specific trading pair and time frame from the Binance API and save it as a CSV file. 

For instance, `save_klines_to_csv("BTCUSDT", "1h")` retrieves hourly Kline data for the BTCUSDT trading pair and saves it to a CSV file named "BTCUSDT_1h.csv".

By utilizing this data, users can conduct various analyses, create visualizations, and develop trading strategies based on historical price action and trading volume.



## Overview

The crypto_data_pipeline(Kline Data) streamlines the extraction, transformation, and loading of BTCUSDT data from Binance into Snowflake for analysis. The pipeline comprises the following steps:

1. **Data Extraction**
   - Data is extracted from Binance using the binance api.
   - Extracted data is loaded into an  S3 bucket created to house raw data.

2. **Data Transformation:**
   - Transformation involves data cleaning, column removal and derivation
   - Transformed data is stored in another  S3 bucket created to house transformed data.

3. **Loading data into Warehouse Or Snowpipe Integration:**
   - Snowpipe is configured to monitor the transformed data file in the  S3 bucket housing the transformed data.
   - A snowpipe is created to automatically ingest data into Snowflake tables upon arrival of the transformed data in the s3 bucket containing the raw data..


 Below is a contextual diagram to visually represent the pipeline architecture and flow of data:

```plaintext
+---------------------+
|                     |
|   Binance API       |
|                     |
+----------+----------+
           |
           v
+----------+----------+
|                     |
|    Data Extraction  |
|                     |
+----------+----------+
           |
           v
+----------+----------+
|                     |
|  Data Transformation|
|                     |
+----------+----------+
           |
           v
+----------+----------+
|                     |
|    S3 Buckets       |
| (Raw & Transformed) |
+----------+----------+
           |
           v
+----------+----------+
|                     |
|   Loading Data into  |
|    Snowflake         |
|                     |
+---------------------+


```

In this diagram:

- **Binance API**: Represents the source of trade data, from which data is extracted.
- **Data Extraction**: Denotes the process of fetching data from the Binance API.
- **Data Transformation**: Refers to the step where the extracted data is cleaned, processed, and transformed into a suitable format.
- **Loading Data into Snowflake**: Represents the final step where the transformed data is loaded into Snowflake for storage and analysis.

This diagram provides a visual representation of the pipeline's components and the flow of data from extraction to storage. It helps users understand the overall architecture and how each component interacts with the others.


## Components

- **Apache Airflow**: Airflow is used to manage and schedule the ETL tasks.
- **Snowflake Snowpipe**: Snowpipe is utilized for loading data into Snowflake from S3.
- **Python**: Python scripts are used for data extraction, transformation, and loading.
- **S3 Buckets**: AWS S3 buckets are used for storing both raw and transformed data.



### Pros and Cons of the Binance Data Pipeline

#### Pros:

1. **Scalability**: The pipeline is designed to handle large volumes of data efficiently, making it suitable for scaling as your data needs grow.
   
2. **Flexibility**: Users can easily customize the pipeline according to their specific requirements by adjusting configurations and modifying the main script.

3. **Reliability**: By persisting data in S3 before loading it into databases, the pipeline ensures data integrity and provides a backup in case of failures during database loading.

4. **Ease of Deployment**: With clear setup instructions and minimal dependencies, deploying the pipeline on different environments is straightforward.

5. **Comprehensive Data Handling**: The pipeline fetches BTCUSDT data using  Binance API, stores it in S3, transform the data and stores it in another s3 , loads the transformed data stored in the s3 into a database in snowflake warehouse, covering a wide range of data storage and processing needs.

#### Cons:

1. **Complexity**: Setting up the pipeline requires configuring AWS services, managing dependencies, and understanding the flow of data between different components, which may be complex for users unfamiliar with AWS or data pipelines.

2. **Cost**: Running the pipeline involves costs associated with AWS services such as S3 storage and snowflake which can accumulate depending on the volume of data and usage patterns.

3. **Maintenance Overhead**: Regular maintenance is required to ensure the pipeline runs smoothly, including monitoring for errors, updating dependencies, and optimizing performance.

4. **Limited Error Handling**: While the pipeline performs basic error handling, it may not handle all possible failure scenarios, requiring additional implementation for robust error management.

5. **Potential Security Risks**: Improperly configured AWS credentials or inadequate security measures could lead to unauthorized access or data breaches, emphasizing the importance of security best practices.

By considering these pros and cons, users can make informed decisions about whether this pipeline meets their specific data processing needs and fits within their operational constraints.


## Setup

### Prerequisites

Before running the pipeline, ensure you have the following:

- Docker to run airflow
- Access to an Apache Airflow environment or container on Docker
- AWS acount with AWS S3 credentials with permissions to read from and write to S3 buckets.
- Snowflake account with credentials and privileges to create pipes and tables.
- Python environment with necessary packages installed (`boto3`, `pandas`, etc.).

### Configuration

1. **Airflow Container Setup:**
   - Ensure you have an Airflow environment or container configured and running.
   - Mount the project directory containing DAG definition file into the Airflow container.

2. **AWS Configuration:**
   - Configure aws  with  your IAM access keys and secrete keys or make sure the one configured already has permissions to access s3 buckets in your account.

3. **Snowflake Configuration:**
   - Update  Snowflake SQL script (`snowflakedb_def.sql`) with your aws accesskeys and secrete keys.
   - Run the (`snowflakedb_def.sql`) script in Snowflake worksheet to set up the database,schema,tables and pipes.

## Usage

1. Clone the Repository and install requirement:
   ```bash
   git clone "https://github.com/princekwusu/Crypto_Data_Pipeline.git"
   cd Crypto_Data_Pipeline
   pip install -r requirements.txt 
   ```
2. Start the Airflow container(make sure you are in the repository directory):
   ```bash
   docker-compose up -d 
   ```
3. Access the web server at https://localhost:8080

4. Login using the default credentials (username: airflow, password: airflow).

5. Make sure the DAG file (`crypto_data_pipeline.py`) is in the DAGs directory of your Airflow environment.

6. Trigger the DAG manually or set up a new schedule for automatic execution.

7. Monitor the Airflow UI for task execution and check logs for any errors.

8. Verify data ingestion in Snowflake tables using SQL queries like 
   ```bash
   SELECT * FROM cryptodb.cryptoschema.btcusdt;
   ```



## Customization

- Adjust the Binance API endpoint, S3 bucket name,parameters according to your setup.
- Modify the main script (`crypto_data_pipeline.py`) if you need to change the data processing logic or add additional steps to the pipeline.

## Contributing

Pull requests and suggestions are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## GROUP MEMBERS
1. Eugene Hayford Kwakye
2. Edward Kuagbenu
3. Priscilla Kyeremah
4. Prince Owusu
5. Orlando kojo Peter
