#!/bin/bash

for A in ??_exercice
do
   zip -r ${A}.zip ${A} -x "${A}/${A}_solution.ipynb"
done
