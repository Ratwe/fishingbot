#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <database_name> [backup_directory]"
  exit 1
fi

# Capture the current date
current_date=$(date +%d_%m_%Y)

# Database name passed as the first argument
database_name=$1

# If a backup directory is provided as the second argument, use it; otherwise, use the current directory
backup_directory=${2:-.}

# Execute pg_dump command
pg_dump "$database_name" > "$backup_directory/$current_date.dump"

# Check if the pg_dump command was successful
if [ "$?" -eq 0 ]; then
  echo "Backup completed successfully: $backup_directory/$current_date.dump"
else
  echo "Error: Backup failed!"
fi
