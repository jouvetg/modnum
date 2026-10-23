#!/bin/bash

python3 utils/fix_kernels.py   # kernel « Python 3 » partout, avant de regénérer

for A in ??_exercice
do
  cd $A
  echo $A
  python3 ../utils/rm_solutions.py 
  cd ..
done
  

