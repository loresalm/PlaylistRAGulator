#!/bin/bash

# Start the Ollama server in the background
echo "Starting Ollama server..."
ollama serve &

# Execute the Python script
echo "Running dataset preprocessing script..."
python3 python_scripts/preprocessing.py

# Check if the Python script completed successfully
if [ $? -eq 0 ]; then
    echo "Preprocessing script completed successfully."
else
    echo "Preprocessing script encountered an error." >&2
fi

# Execute the Python script
echo "Running vector db generation script..."
python3 python_scripts/make_vector_db.py

# Check if the Python script completed successfully
if [ $? -eq 0 ]; then
    echo "Vector DB completed successfully."
else
    echo "Vector DB encountered an error." >&2
fi

# Stop the container
echo "All tasks completed. Exiting container..."

exit 0