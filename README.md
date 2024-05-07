# Binance Data Pipeline

This project is a data pipeline for fetching trade data from Binance API, persisting it in an S3 bucket, and loading it into Redshift and RDS databases. 

## Overview

The pipeline consists of the following steps:

1. Fetch data from the Binance API.
2. Persist the data in a compressed format (JSON) in an S3 bucket.
3. Load the data from S3 into Redshift.
4. Load the data from S3 into an RDS database.

## Prerequisites

- Python 3.x installed on your system.
- AWS account with appropriate permissions to access S3, Redshift, and RDS.
- Boto3 library for AWS interaction.
- Psycopg2 library for PostgreSQL database interaction.

## Setup

1. Clone this repository to your local machine.

```bash
git clone https://github.com/yourusername/binance-data-pipeline.git
```

2. Install the required Python packages.

```bash
pip install -r requirements.txt
```

3. Configure your AWS credentials. You can set them up using the AWS CLI or through environment variables.

```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
```

## Usage

1. Run the main Python script to execute the data pipeline.

```bash
python main.py
```

This script will fetch the latest trade data from Binance, persist it in S3, and load it into Redshift and RDS databases.

## Configuration

- `main.py`: Main script to execute the data pipeline.
- `config.py`: Configuration file containing AWS credentials, endpoint URLs, and database credentials.
- `requirements.txt`: List of Python dependencies.

## Customization

- Adjust the Binance API endpoint, S3 bucket name, Redshift parameters, and RDS parameters in the `config.py` file according to your setup.
- Modify the main script (`main.py`) if you need to change the data processing logic or add additional steps to the pipeline.

## Contributing

Pull requests and suggestions are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
