#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/your/file.csv"
  exit 1
fi

# Read the path to the CSV file
CSV_FILE="$1"
DB_NAME=$(basename "$CSV_FILE" .csv)  # Use the file name (without .csv extension) as the database name
TABLE_NAME=$(basename "$CSV_FILE" .csv)  # Use the file name (without .csv extension) as the table name

# Load environment variables from .env file, ignoring DB_NAME
if [ -f .env ]; then
  export $(grep -v '^#' .env | grep -v 'DB_NAME' | xargs)  # Load all variables except DB_NAME
else
  echo ".env file not found"
  exit 1
fi

# Create the new database with the CSV file's name if it doesn't exist
psql -h $DB_HOST -U $DB_USER -p $DB_PORT -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || psql -h $DB_HOST -U $DB_USER -p $DB_PORT -c "CREATE DATABASE $DB_NAME;"
echo "Database '$DB_NAME' created or already exists."

# Get column names from the CSV file header
COLUMN_NAMES=$(head -n 1 "$CSV_FILE" | sed 's/,/ VARCHAR,/g')
COLUMN_NAMES="${COLUMN_NAMES} VARCHAR"  # Add VARCHAR to the last column

# Create the table in the newly created database
psql -h $DB_HOST -d $DB_NAME -U $DB_USER -p $DB_PORT -c "CREATE TABLE IF NOT EXISTS $TABLE_NAME ($COLUMN_NAMES);"
echo "Table '$TABLE_NAME' created in database '$DB_NAME'."

# Import CSV into the new table
psql -h $DB_HOST -d $DB_NAME -U $DB_USER -p $DB_PORT -c "\copy $TABLE_NAME FROM '$CSV_FILE' DELIMITER ',' CSV HEADER;"

echo "CSV file '$CSV_FILE' imported into database '$DB_NAME' and table '$TABLE_NAME'."
