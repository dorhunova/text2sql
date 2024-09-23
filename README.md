# text2sql
A repository showcasing the integration of Vanna.ai's text-to-SQL engine for converting natural language queries into SQL commands.

## How to Setup Locally

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/text2sql.git
    cd text2sql
    ```

2. **Install Dependencies**

    ```bash
    poetry install
    ```

3. **Run the Application**

    ```bash
    poetry run python text2sql/main.py
    ```

## Environment Setup

Before running the application, you need to create a `.env` file in the root directory of the project. This file should contain the following environment variables:

```bash
# Azure OpenAI Config
API_BASE=<your_azure_openai_api_base_url>
API_VERSION=2023-03-15-preview
API_KEY=<your_azure_openai_api_key>
DEPLOYMENT=<your_azure_openai_deployment_name>

# Client Config
CLIENT=fs

# DB Config
DB_HOST=localhost
DB_NAME=fs
DB_USER=postgres
DB_PASSWORD=<your_database_password>
DB_PORT=5432

# Vanna Flask App Config
DEBUG=False
SQL=True
CHART=True
REDRAW_CHART=True
ALLOW_LLM_TO_SEE_DATA=True
SUMMARIZATION=True
```

## How to Setup Remotely using Docker Compose


### How to Run the PostgreSQL Configuration Script
In order to make your local postgres instance accessible to the vanna flask app, you need to run the following script:

#### Step-by-Step Instructions

1. **Make the script executable**:
   ```bash
   chmod +x configure_postgres.sh
   ```

2. **Run the script**:
   ```bash
   ./configure_postgres.sh
   ```

This script will configure PostgreSQL to allow connections from Docker containers or other external sources by updating the necessary configuration files and restarting the PostgreSQL service.

Once completed, your Docker containers should be able to connect to your local PostgreSQL instance using host.docker.internal or your machine's IP address.

3. **And, finally, you can run the following command to start the application:**

```bash 
docker-compose up
```
Your application should now be running on `http://0.0.0.0:8084`