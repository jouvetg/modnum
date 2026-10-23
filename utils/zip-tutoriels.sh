#!/bin/bash

python3 utils/fix_kernels.py   # kernel « Python 3 » partout, avant de zipper

for A in ??_tutoriel
do
   zip -r ${A}.zip ${A} -x "${A}/.ipynb_checkpoints/*"
done
