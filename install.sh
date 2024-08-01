#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo "Error: Python is not installed."
    exit 1
fi

# Check if pip is installed
if ! command_exists pip3; then
    echo "Error: pip is not installed."
    exit 1
fi

# Install the required Python packages
pip3 install -r requirements.txt

# Define the path to the secrets file
SECRETS_FILE=".streamlit/secrets.toml"

# Get the key from the input argument
KEY=$1

# Check if the secrets file exists
if [ -f "$SECRETS_FILE" ]; then
    # Overwrite the key in the existing file
    sed -i.bak "s/^key = .*/api_key = \"$KEY\"/" "$SECRETS_FILE"
    rm "${SECRETS_FILE}.bak"
else
    # Create the directory if it does not exist
    mkdir -p .streamlit
    # Create the file and write the key
    echo "api_key = \"$KEY\"" > "$SECRETS_FILE"
fi

make app
