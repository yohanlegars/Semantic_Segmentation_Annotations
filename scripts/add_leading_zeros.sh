#/bin/bash

directory_path="/home/yohan-sl-intern/Documents/off_road_dataset/terra/images/terra"

cd "$directory_path"

for file in *.png *.jpg; do
	filename=$(basename -- "$file")
	filename_no_ext="${filename%.*}"

	ext="${file##*.}"

	num=$(echo "$filename_no_ext" | sed 's/^0*//')

	new_name=$(printf "%06d.%s" "$num" "$ext")

	mv "$file" "$new_name"

done
