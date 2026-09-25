"""Figure de l'exercice 1.2 : remplissage itératif du vecteur M_sans_interet.

Usage (depuis la racine) : python utils/fig_remplissage_vecteur.py
Écrit 01_exercice/fig/remplissage_vecteur.{svg,png}.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

BLEU = "#1d3b57"      # case déjà remplie
BLEU_BORD = "#6cc3ff"
ORANGE = "#ffb454"    # case remplie à cette itération
GRIS = "#1a1a1a"      # case encore à zéro
GRIS_BORD = "#555555"
TEXTE = "#ffffff"
MONO = "DejaVu Sans Mono"

M_init, M_epargne, duree = 20000, 500, 35
indices = [0, 1, 2, 3, 4, None, duree]   # None = cases non dessinées (…)
W, H, X0 = 1.25, 0.8, 3.2                # largeur/hauteur d'une case, début du vecteur


def xcase(k):
    return X0 + k * W


def ligne(ax, y, it, label):
    """Dessine l'état du vecteur après l'itération `it` (it = 0 : initialisation)."""
    ax.text(X0 - 0.4, y + H / 2, label, ha="right", va="center", fontsize=14,
            family=MONO, color=TEXTE)
    for k, i in enumerate(indices):
        x = xcase(k)
        if i is None:
            ax.text(x + W / 2, y + H / 2, "…", ha="center", va="center", fontsize=16,
                    color=TEXTE)
            continue
        rempli = i <= it
        if i == it:
            fc, ec = ORANGE, ORANGE
        elif rempli:
            fc, ec = BLEU, BLEU_BORD
        else:
            fc, ec = GRIS, GRIS_BORD
        ax.add_patch(Rectangle((x, y), W, H, fc=fc, ec=ec, lw=1.5))
        val = M_init + M_epargne * i if rempli else 0
        ax.text(x + W / 2, y + H / 2, f"{val}", ha="center", va="center", fontsize=12,
                family=MONO, color=("black" if i == it else TEXTE) if rempli else "#777777",
                fontweight="bold" if i == it else "normal")
    if it >= 1:
        k = indices.index(it)
        a = FancyArrowPatch((xcase(k - 1) + W / 2, y + H), (xcase(k) + W / 2, y + H),
                            connectionstyle="arc3,rad=-0.45", arrowstyle="-|>",
                            mutation_scale=14, lw=1.6, color=ORANGE)
        ax.add_patch(a)
        ax.text(xcase(k), y + H + 0.62, "+ M_epargne", ha="center", va="bottom",
                fontsize=11, family=MONO, color=ORANGE)


fig, ax = plt.subplots(figsize=(10, 6.2), facecolor="black")
ax.set_xlim(0, xcase(len(indices)) + 0.2)
ax.set_ylim(-0.3, 10.6)
ax.axis("off")

# indices des cases
y_top = 8.6
for k, i in enumerate(indices):
    if i is not None:
        ax.text(xcase(k) + W / 2, y_top + H + 0.15, f"[{i}]", ha="center", va="bottom",
                fontsize=12, family=MONO, color="#9a9a9a")
ax.text(X0 - 0.4, y_top + H + 0.15, "indice", ha="right", va="bottom", fontsize=12,
        family=MONO, color="#9a9a9a")

lignes = [(0, "initialisation"), (1, "it = 1"), (2, "it = 2"), (3, "it = 3"), (duree, "it = 35")]
ys = [8.6, 6.5, 4.4, 2.3, 0.0]
for (it, label), y in zip(lignes, ys):
    ligne(ax, y, it, label)
ax.text(X0 - 1.3, 1.45, "⋮", ha="center", va="center", fontsize=18, color=TEXTE)

fig.tight_layout()
for ext in ("svg", "png"):
    fig.savefig(f"01_exercice/fig/remplissage_vecteur.{ext}", dpi=150, facecolor="black")
