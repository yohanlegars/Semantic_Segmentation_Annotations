#!/bin/bash

source_dir="/home/yohan-sl-intern/Documents/off_road_dataset/terra/images/rugd"
destination_dir="/home/yohan-sl-intern/Documents/off_road_dataset/terra/images/terra"


function zero_pad {
	printf "%06d" "$1"
}

# Check if the source directory exists
if [ ! -d "$source_dir" ]; then
    echo "Source directory '$source_dir' not found."
    exit 1
fi
# Check if the destination directory exists; if not, create it
if [ ! -d "$destination_dir" ]; then
    mkdir -p "$destination_dir"
fi



# Find the last used number in the destination directory
last_number=$(ls "$destination_dir" | grep -Eo '^[0-9]+' | sort -n | tail -n 1)
# Initialize the counter based on the last used number (if available)
if [ -n "$last_number" ]; then
    counter=$((last_number + 1))
else
    counter=1
fi

# Move into the source directory
cd "$source_dir"

# Iterate through each image file in the source directory
for file in *
do
	   # Check if the file exists and is a regular file
    if [ -f "$file" ]; then
        # Get the file extension in lowercase
        extension="${file##*.}"
        #extension_lower="${extension,,}"  # Convert to lowercase

        # Create the new filename with zero padding and the original extension
        new_filename="$counter.$extension"

        # Copy the file to the destination directory and rename it
        cp "$file" "$destination_dir/$new_filename"

        # Increment the counter for the next file
        ((counter++))
    fi
done














