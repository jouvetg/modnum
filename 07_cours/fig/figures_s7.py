"""Figures de la séance 7 (fond noir, SVG éditables).

Usage (depuis la racine) : python3 07_cours/fig/figures_s7.py
Écrit les SVG listés dans DEST, dans 07_cours/fig et les dossiers fig voisins.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# figure -> fichiers SVG écrits (chemins relatifs à ce dossier)
DEST = {
    '7.2_matrice_carte': ['matrice_carte_s7.svg', '../../07_tutoriel/fig/matrice_carte_s7.svg'],
    '7.3_discretisation': ['discretisation_2d_s7.svg'],
}

CX = "#e660aa"   # direction x : colonnes, axe 1, qx, dx
CY = "#40d0d0"   # direction y : lignes, axe 0, qy, dy
POLLUANT = "#e8836f"
CMAP_POLL = LinearSegmentedColormap.from_list("poll", ["#161616", "#5a3029", POLLUANT,
                                                       "#ffd9c9"])


def fleche(ax, p0, p1, color=BLANC, lw=1.6, ms=14, style="-|>", rad=0.0, **kw):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, **kw)
    ax.add_patch(a)
    return a


def axes_vides(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


# ---------------------------------------------------------------------------
# 7.2 Matrice <-> carte : T[j, i], axes, bords, origin='lower'
# ---------------------------------------------------------------------------
def fig_matrice_carte():
    nx, ny = 6, 4
    jx, ix = 1, 4   # case mise en valeur
    fig, ax = axes_vides((16, 7.4), (-2.6, 26.6), (-2.4, 9.9))

    def grille(X0, Y0, bas_en_haut, off=0.15):
        """Dessine la matrice ; renvoie la fonction ordonnée(j)."""
        def yl(j):
            return Y0 + (j if bas_en_haut else ny - 1 - j)
        for j in range(ny):
            for i in range(nx):
                on = (j, i) == (jx, ix)
                ax.add_patch(Rectangle((X0 + i, yl(j)), 1, 1,
                                       fc=ORANGE if on else GRIS_FOND,
                                       ec="black" if on else GRIS_BORD, lw=1.2))
                if on:
                    ax.text(X0 + i + 0.5, yl(j) + 0.5, f"T[{j},{i}]", ha="center",
                            va="center", fontsize=11, family=MONO, color="black",
                            fontweight="bold")
        for i in range(nx):
            ax.text(X0 + i + 0.5, Y0 + ny + 0.15, f"{i}", ha="center", va="bottom",
                    fontsize=13, family=MONO, color=CX)
        for j in range(ny):
            ax.text(X0 - off, yl(j) + 0.5, f"{j}", ha="right", va="center",
                    fontsize=13, family=MONO, color=CY)
        return yl

    # --- gauche : affichage par défaut
    X0, Y0 = 1.0, 2.0
    ax.text(X0 + nx / 2, 9.6, "ax.imshow(T)", ha="center", va="top", fontsize=17,
            family=MONO, color=ROUGE)
    ax.text(X0 + nx / 2, 8.75, "défaut : ligne 0 en haut, comme print(T)", ha="center",
            va="top", fontsize=13, color=GRIS)
    yl = grille(X0, Y0, bas_en_haut=False)
    ax.add_patch(Rectangle((X0, yl(0)), nx, 1, fc="none", ec=ROUGE, lw=2.5))
    ax.text(X0 + nx + 0.25, yl(0) + 0.5, "T[0,:]\nen haut ✗", ha="left", va="center",
            fontsize=13, family=MONO, color=ROUGE)
    ax.text(X0 + nx / 2, 0.9, "la carte est à l'envers :\nle Sud se retrouve en haut",
            ha="center", va="top", fontsize=14, color=ROUGE, linespacing=1.3)
    # axe 0 vers le bas
    fleche(ax, (X0 - 1.3, Y0 + ny), (X0 - 1.3, Y0), color=CY, lw=1.8)
    ax.text(X0 - 1.55, Y0 + ny / 2, "j, axe 0", ha="right", va="center", fontsize=13,
            color=CY, rotation=90)

    # --- droite : origin='lower' = carte
    X1, Y1 = 17.5, 2.0
    ax.text(X1 + nx / 2, 9.6, "ax.imshow(T, origin='lower')", ha="center", va="top",
            fontsize=17, family=MONO, color=VERT)
    ax.text(X1 + nx / 2, 8.75, "origine au coin Sud-Ouest : T[0,0]", ha="center",
            va="top", fontsize=13, color=GRIS)
    yl = grille(X1, Y1, bas_en_haut=True, off=0.3)
    # bords
    e = 0.1
    ax.plot([X1, X1 + nx], [Y1 - e, Y1 - e], color=VERT, lw=4)
    ax.plot([X1, X1 + nx], [Y1 + ny + e, Y1 + ny + e], color=VERT, lw=4)
    ax.plot([X1 - e, X1 - e], [Y1, Y1 + ny], color=VERT, lw=4)
    ax.plot([X1 + nx + e, X1 + nx + e], [Y1, Y1 + ny], color=VERT, lw=4)
    ax.text(X1 + nx / 2, Y1 - 0.3, "T[0, :]   bas (Sud)", ha="center", va="top",
            fontsize=14, family=MONO, color=VERT)
    ax.text(X1 + nx / 2, Y1 + ny + 0.75, "T[-1, :]   haut (Nord)", ha="center",
            va="bottom", fontsize=14, family=MONO, color=VERT)
    ax.text(X1 - 1.35, Y1 + ny / 2, "T[:, 0]\ngauche\n(Ouest)", ha="right",
            va="center", fontsize=14, family=MONO, color=VERT, linespacing=1.3)
    ax.text(X1 + nx + 0.4, Y1 + ny / 2, "T[:, -1]\ndroite\n(Est)", ha="left",
            va="center", fontsize=14, family=MONO, color=VERT, linespacing=1.3)
    ax.plot([X1], [Y1], "o", ms=10, color=BLANC, zorder=6)
    # axes physiques
    fleche(ax, (X1 - 0.9, Y1), (X1 - 0.9, Y1 + ny + 0.2), color=CY, lw=1.8)
    ax.text(X1 - 0.9, Y1 + ny + 0.3, "y", ha="center", va="bottom", fontsize=15,
            style="italic", color=CY)
    fleche(ax, (X1, Y1 - 1.1), (X1 + nx + 0.2, Y1 - 1.1), color=CX, lw=1.8)
    ax.text(X1 + nx + 0.35, Y1 - 1.1, "x", ha="left", va="center", fontsize=15,
            style="italic", color=CX)
    ax.text(X1 + nx / 2, Y1 - 1.8, "x ↔ i (colonnes, axe 1)", ha="center", va="top",
            fontsize=13, color=CX)
    ax.text(X1 + nx / 2, Y1 - 2.5, "y ↔ j (lignes, axe 0)", ha="center", va="top",
            fontsize=13, color=CY)

    # centre : lecture
    xm = 11.4
    ax.text(xm, 5.2, "T[j, i]", ha="center", va="center", fontsize=22, family=MONO,
            color=ORANGE)
    ax.text(xm, 4.3, "j : ligne ↔ y", ha="center", va="center", fontsize=14,
            color=CY)
    ax.text(xm, 3.6, "i : colonne ↔ x", ha="center", va="center", fontsize=14,
            color=CX)
    fleche(ax, (9.6, 6.2), (13.2, 6.2), color=GRIS, lw=1.5, rad=-0.25)
    ax.text(xm, 7.0, "même matrice", ha="center", va="bottom", fontsize=12,
            color=GRIS)
    sauver_svg(fig, DOSSIER, DEST["7.2_matrice_carte"])


# ---------------------------------------------------------------------------
# 7.3 Discrétisation d'un domaine rectangulaire
# ---------------------------------------------------------------------------
def fig_discretisation():
    nx, ny = 6, 5
    g = 2.1
    X0, Y0 = 2.4, 1.8
    xn = X0 + g * np.arange(nx)
    yn = Y0 + g * np.arange(ny)
    fig, ax = axes_vides((16, 7.6), (-0.3, 29.0), (-1.9, 11.9))

    Lx, Ly = xn[-1] - X0, yn[-1] - Y0
    ax.add_patch(Rectangle((X0, Y0), Lx, Ly, fc="#262626", ec=BLANC, lw=1.8, zorder=0))
    for xi in xn:
        ax.plot([xi, xi], [Y0, yn[-1]], color=GRIS_BORD, lw=0.8, zorder=1)
    for yi in yn:
        ax.plot([X0, xn[-1]], [yi, yi], color=GRIS_BORD, lw=0.8, zorder=1)
    XX, YY = np.meshgrid(xn, yn)
    ax.plot(XX.ravel(), YY.ravel(), "o", ms=12, mfc=BLEU_FOND, mec=BLEU, mew=1.8,
            zorder=3)

    # x[i] en bas, y[j] à gauche
    for i, xi in enumerate(xn):
        ax.text(xi, Y0 - 0.35, f"x[{i}]", ha="center", va="top", fontsize=12,
                family=MONO, color=CX)
    for j, yi in enumerate(yn):
        ax.text(X0 - 0.35, yi, f"y[{j}]", ha="right", va="center", fontsize=12,
                family=MONO, color=CY)
    ax.text(X0, Y0 - 1.0, "0", ha="center", va="top", fontsize=14, style="italic")
    ax.text(xn[-1], Y0 - 1.0, "Lx", ha="center", va="top", fontsize=14,
            style="italic", color=CX)
    ax.text(X0 - 1.45, yn[-1], "Ly", ha="right", va="center", fontsize=14,
            style="italic", color=CY)

    # cotes dx, dy
    yc = yn[-1] + 0.55
    fleche(ax, (xn[1], yc), (xn[2], yc), color=CX, style="<|-|>", ms=11, lw=1.5)
    ax.text((xn[1] + xn[2]) / 2, yc + 0.15, "dx", ha="center", va="bottom",
            fontsize=15, family=MONO, color=CX)
    xc = xn[-1] + 0.55
    fleche(ax, (xc, yn[2]), (xc, yn[3]), color=CY, style="<|-|>", ms=11, lw=1.5)
    ax.text(xc + 0.2, (yn[2] + yn[3]) / 2, "dy", ha="left", va="center", fontsize=15,
            family=MONO, color=CY)

    # nœuds vs intervalles (en bas)
    ax.text((X0 + xn[-1]) / 2, Y0 - 1.55,
            "nx = 6 nœuds  →  nx − 1 = 5 intervalles", ha="center", va="top",
            fontsize=14, color=BLANC)

    # code à droite
    xt = 15.4
    ax.text(xt, 11.2, "code", ha="left", va="top", fontsize=13, color=GRIS)
    lignes = [
        ("dx = Lx / (nx - 1)          # 5 intervalles en x", CX),
        ("dy = Ly / (ny - 1)          # 4 intervalles en y", CY),
        ("", None),
        ("x = np.linspace(0, Lx, nx)  # nx = 6 abscisses", CX),
        ("y = np.linspace(0, Ly, ny)  # ny = 5 ordonnées", CY),
        ("", None),
        ("T = np.ones((ny, nx)) * Tinit", BLEU),
    ]
    y = 10.2
    for s, c in lignes:
        if s:
            ax.text(xt, y, s, ha="left", va="center", fontsize=13.5, family=MONO,
                    color=c)
        y -= 1.0
    ax.text(xt, y - 0.1, "une valeur par nœud ●  :  taille (ny, nx) = (5, 6)",
            ha="left", va="center", fontsize=14, color=BLEU)
    ax.text(xt, y - 1.3, "piège :  dx = Lx / nx", ha="left", va="center",
            fontsize=14, family=MONO, color=ROUGE)
    ax.text(xt, y - 2.1, "compte les nœuds au lieu des intervalles ✗", ha="left",
            va="center", fontsize=13, color=ROUGE)
    sauver_svg(fig, DOSSIER, DEST["7.3_discretisation"])


def main():
    fig_matrice_carte()
    fig_discretisation()


if __name__ == "__main__":
    main()
