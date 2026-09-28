"""Style commun des figures du cours (fond noir, comme les figures existantes).

Palette reprise de utils/fig_remplissage_vecteur.py et 02_cours/fig/figures_cours2.py :
orange = ce qui change / est calculé maintenant, bleu = déjà calculé / stocké,
gris = inactif / vide, vert = conditions / validation, rouge = erreur / piège.
"""

import os
import matplotlib.pyplot as plt

ORANGE = "#ffb454"
BLEU = "#6cc3ff"
BLEU_FOND = "#1d3b57"
VERT = "#8be28b"
ROUGE = "#ff6b6b"
GRIS = "#9a9a9a"
GRIS_FOND = "#1a1a1a"
GRIS_BORD = "#555555"
BLANC = "#ffffff"
MONO = "DejaVu Sans Mono"

plt.rcParams.update({
    "figure.facecolor": "black",
    "axes.facecolor": "black",
    "savefig.facecolor": "black",
    "text.color": BLANC,
    "axes.labelcolor": BLANC,
    "axes.edgecolor": GRIS,
    "xtick.color": GRIS,
    "ytick.color": GRIS,
    "font.family": "DejaVu Sans",
    "font.size": 15,
    "mathtext.fontset": "cm",
    "svg.fonttype": "none",   # texte gardé comme texte : SVG éditable (Inkscape)
})


def sauver_svg(fig, dossier, chemins):
    """Écrit la figure en SVG (texte éditable) à chacun des chemins, relatifs à `dossier`."""
    for rel in chemins:
        chemin = os.path.normpath(os.path.join(dossier, rel))
        fig.savefig(chemin, bbox_inches="tight", facecolor="black")
        # Les lecteurs SVG fusionnent les espaces successifs : l'indentation du code serait
        # perdue. On force la conservation des espaces sur chaque élément texte.
        with open(chemin, encoding="utf-8") as f:
            svg = f.read()
        svg = svg.replace('<text style="', '<text xml:space="preserve" style="white-space: pre; ')
        # polices de secours si DejaVu n'est pas installé chez le lecteur
        svg = svg.replace("'DejaVu Sans Mono'", "'DejaVu Sans Mono', monospace")
        svg = svg.replace("'DejaVu Sans';", "'DejaVu Sans', sans-serif;")
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(svg)
        print("écrit", os.path.relpath(chemin))
    plt.close(fig)
