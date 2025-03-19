#!/bin/bash

for A in ??_exercice
do
  cd $A
  echo $A
  python3 ../utils/rm_solutions.py 
  cd ..
done
  

