#!/bin/bash

# Start the Ollama server in the background
echo "Starting Ollama server..."
ollama serve &

# Wait for the Ollama server to fully start
echo "Waiting for Ollama server to initialize..."
sleep 1 # Adjust if needed based on server initialization time
#!/bin/bash

# Path to the JSON file
json_file="data/user_inputs/config.json"

# Extract model names using jq
embed_model=$(jq -r '.embedmodel' "$json_file")
vis_model=$(jq -r '.vismodel' "$json_file")

# Check if models were extracted correctly
if [[ -n "$embed_model" && -n "$vis_model" ]]; then
    echo "Pulling models: $embed_model and $vis_model"

    # Pull the embed model
    ollama pull "$embed_model"

    # Pull the vis model
    ollama pull "$vis_model"
else
    echo "Error: Failed to extract model names from the JSON file."
fi
