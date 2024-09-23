#!/bin/bash

# Define the PostgreSQL configuration directory
PG_CONF_DIR="/opt/homebrew/var/postgresql@14"

# Check if the configuration directory exists
if [ ! -d "$PG_CONF_DIR" ]; then
  echo "PostgreSQL configuration directory not found at $PG_CONF_DIR"
  exit 1
fi

# Check if brew is installed
if ! command -v brew &> /dev/null; then
  echo "Homebrew is not installed. Please install it first."
  exit 1
fi

# Define the configuration files
PG_CONF_FILE="$PG_CONF_DIR/postgresql.conf"
PG_HBA_FILE="$PG_CONF_DIR/pg_hba.conf"

# Add or update listen_addresses in postgresql.conf
if grep -q "^listen_addresses" "$PG_CONF_FILE"; then
  sed -i '' "s/^listen_addresses.*/listen_addresses = 'localhost, 0.0.0.0'/" "$PG_CONF_FILE"
else
  echo "listen_addresses = 'localhost, 0.0.0.0'" >> "$PG_CONF_FILE"
fi
echo "Updated listen_addresses in postgresql.conf"

# Add the necessary entry to pg_hba.conf if it doesn't already exist
if ! grep -q "0.0.0.0/0" "$PG_HBA_FILE"; then
  echo "host    all             all             0.0.0.0/0               md5" >> "$PG_HBA_FILE"
  echo "Added entry to pg_hba.conf to allow external connections"
else
  echo "The entry for external connections already exists in pg_hba.conf"
fi

# Restart PostgreSQL service
echo "Restarting PostgreSQL service..."
brew services restart postgresql@14

if [[ $? -eq 0 ]]; then
  echo "Configuration complete. PostgreSQL is now set up to allow external connections."
else
  echo "Failed to restart PostgreSQL service. Please check the logs for more details."
fi
