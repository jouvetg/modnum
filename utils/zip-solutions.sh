#!/bin/bash
# Zip all NN_exercice/NN_exercice_solution.ipynb into solutions.zip at the repo root.
# The solution notebooks are gitignored, so this archive is the way to back them up or hand them over.
# Run from the repo root.

rm -f solutions.zip
zip -j solutions.zip ??_exercice/??_exercice_solution.ipynb
