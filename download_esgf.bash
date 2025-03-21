#!/bin/bash

# The following script download CMIP6 models data from th ESGF nodes, links come from a generix txt calles "urls.txt"


input_file="urls.txt"

# Create a directory for the downloaded files
mkdir -p CMIP6_Downloads
cd CMIP6_Downloads || exit

# Read each line from the input file
while IFS="'" read -r _ file_name _ file_url _ hash_type _ expected_hash _; do
    echo "Downloading: $file_name from $file_url"
    
    # Download the file
    wget -O "$file_name" "$file_url"
    
    # Verify the file integrity using SHA256
    echo "Verifying file integrity using $hash_type..."
    computed_hash=$(sha256sum "$file_name" | awk '{print $1}')
    
    if [[ "$computed_hash" == "$expected_hash" ]]; then
        echo "✅ Hash match: $computed_hash"
    else
        echo "❌ Hash mismatch! Expected: $expected_hash, Got: $computed_hash"
    fi
    
    echo "Download completed: $file_name"
    echo "-----------------------------------"
done < "../$input_file"

echo "All downloads completed."
