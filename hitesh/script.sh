#!/bin/bash

# Check that the correct number of input arguments were provided
if [ "$#" -ne 3 ]; then
    echo "Error: Incorrect number of arguments provided."
    echo "Usage: ./my_script.sh input_path out_path out_name"
    exit 1
fi

# Read input arguments
input_path="$1"
out_path="$2"
out_name="$3"

# Create output directory if it doesn't exist
if [ ! -d "$out_path" ]; then
    echo "Output directory '$out_path' not found, creating it now."
    mkdir -p "$out_path"
fi

# Check that the input file exists
if [ ! -f "$input_path" ]; then
    echo "Error: Input file not found at '$input_path'."
    exit 1
fi

# Run the command
cat "$input_path" | ./parser/geoparser-1.3/scripts/run -t plain -top -g geonames -o "$out_path" "$out_name"
