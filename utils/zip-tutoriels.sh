#!/bin/bash

for A in ??_tutoriel
do
   zip -r ${A}.zip ${A} -x "${A}/.ipynb_checkpoints/*"
done
