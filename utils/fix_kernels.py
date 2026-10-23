"""Remet le kernel « Python 3 » dans tous les notebooks du cours.

VS Code réécrit le kernel choisi localement (p.e. « igm ») dans les métadonnées
quand on enregistre un notebook. Ce script le remplace par le kernel standard,
en ne modifiant que les lignes concernées (pas de reformatage du fichier).

Usage (depuis la racine) : python3 utils/fix_kernels.py
"""

import glob
import json
import re

for f in sorted(glob.glob("0*_*/*.ipynb") + glob.glob("1*_*/*.ipynb")):
    with open(f, encoding="utf-8") as fh:
        texte = fh.read()
    k = json.loads(texte).get("metadata", {}).get("kernelspec", {})
    if k.get("display_name") == "Python 3" and k.get("name") == "python3":
        continue
    nouveau = re.sub(r'("display_name": )"[^"]*"', r'\1"Python 3"', texte, count=1)
    nouveau = re.sub(r'("kernelspec": \{[^}]*?"name": )"[^"]*"', r'\1"python3"', nouveau,
                     count=1, flags=re.S)
    json.loads(nouveau)                      # vérifie que le JSON reste valide
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(nouveau)
    print("kernel « Python 3 » remis dans", f)
