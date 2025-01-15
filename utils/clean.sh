#!/bin/bash

# Remove temporary files
rm *~

# Loop through image files with specified extensions
for A in *.jpg *.jpeg *.png *.JPG; do
    # Check if the file is referenced in any .md or .ipynb files in the parent directory
    grep -q "$A" ../*.md

    if [ $? -eq 0 ]; then
        echo "$A FOUND"
    else
        echo "$A DELETED"
        # Uncomment the following line to actually delete the files
        rm "$A"
    fi

done

