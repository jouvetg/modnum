"""Figures de la séance 9 (fond noir, SVG éditables).

Usage (depuis la racine) : python3 09_cours/fig/figures_s9.py
Écrit les SVG listés dans DEST, dans 09_cours/fig et les dossiers fig voisins.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch, Circle
from matplotlib.colors import LinearSegmentedColormap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# figure -> fichiers SVG écrits (chemins relatifs à ce dossier)
DEST = {
    '9.4_matrices_booleens': ['matrices_booleens_s9.svg', '../../09_tutoriel/fig/matrices_booleens_s9.svg'],
    '9.7_masque_source': ['masque_zone_s9.svg'],
}

POS = ORANGE   # V > 0
NEG = BLEU     # V < 0
FOND_POS = "#4a3517"
POLLUANT = LinearSegmentedColormap.from_list("polluant", ["#000000", "#5a2d0c", ORANGE,
                                                          "#fff1d6"])
VITESSE = LinearSegmentedColormap.from_list("vitesse", ["#0b0b0b", BLEU_FOND, BLEU,
                                                        "#e8f6ff"])


def fleche(ax, p0, p1, color=BLANC, lw=1.6, ms=14, style="-|>", rad=0.0, **kw):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, lw=lw, color=color,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, **kw)
    ax.add_patch(a)
    return a


def axes_vides(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    return fig, ax


def code(ax, x, y, s, color=BLANC, fs=14, ha="left", va="center", **kw):
    return ax.text(x, y, s, ha=ha, va=va, fontsize=fs, family=MONO, color=color, **kw)


# ---------------------------------------------------------------------------
# 9.4 Matrices de booléens
# ---------------------------------------------------------------------------
def fig_matrices_booleens():
    Vx = np.array([[2, 3, 2, 3, 4, 5],
                   [1, 2, 1, 2, 3, 4],
                   [0, 1, 0, 1, 2, 3],
                   [-1, 0, -1, 0, 1, 2],
                   [-2, -1, -2, -1, 0, 1],
                   [-3, -2, -1, -2, -1, 0]])
    n = 6
    W = 0.7
    larg = n * W
    esp = 1.9
    xs = [i * (larg + esp) for i in range(5)]
    xmin, xmax = -0.4, xs[-1] + larg + 0.4
    ymin, ymax = -1.3, n * W + 1.6
    h = 20 * (ymax - ymin) / (xmax - xmin)
    fig, ax = axes_vides((20, h), (xmin, xmax), (ymin, ymax))
    ax.set_aspect("equal")

    def matrice(x0, M, genre, titre, col_titre, sous_titre):
        for i in range(n):
            for j in range(n):
                v = M[i, j]
                yb = (n - 1 - i) * W
                if genre == "valeurs":
                    if v > 0:
                        fc, tc = POS, "black"
                    elif v < 0:
                        fc, tc = NEG, "black"
                    else:
                        fc, tc = GRIS_FOND, GRIS
                    txt = f"{v:d}"
                else:
                    fc, tc = (VERT, "black") if v else (GRIS_FOND, "#666666")
                    txt = "1" if v else "0"
                ax.add_patch(Rectangle((x0 + j * W, yb), W, W, fc=fc, ec="black", lw=1.5))
                code(ax, x0 + j * W + W / 2, yb + W / 2, txt, fs=14, ha="center",
                     color=tc, fontweight="bold")
        code(ax, x0 + larg / 2, n * W + 1.05, titre, fs=19, ha="center", color=col_titre)
        ax.text(x0 + larg / 2, n * W + 0.4, sous_titre, ha="center", va="center",
                fontsize=13, color=GRIS)

    matrice(xs[0], Vx, "valeurs", "Vx", BLANC, "une vitesse par interface")
    matrice(xs[1], Vx > 0, "masque", "Vx > 0", VERT, "True = 1, False = 0")
    matrice(xs[2], Vx * (Vx > 0), "valeurs", "Vx*(Vx > 0)", POS, "ne garde que les > 0")
    matrice(xs[3], Vx < 0, "masque", "Vx < 0", VERT, "True = 1, False = 0")
    matrice(xs[4], Vx * (Vx < 0), "valeurs", "Vx*(Vx < 0)", NEG, "ne garde que les < 0")

    ym = n * W / 2
    for k, s in ((0, "→"), (1, "× Vx ="), (3, "× Vx =")):
        ax.text(xs[k] + larg + esp / 2, ym, s, ha="center", va="center", fontsize=18,
                color=BLANC, family=MONO)
    ax.plot([xs[3] - esp / 2] * 2, [-0.2, n * W + 1.4], color=GRIS_BORD, lw=1, ls=":")

    ax.text(xs[0], -0.8, "taille (ny, nx-1)", ha="left", va="center", fontsize=14,
            color=GRIS)
    sauver_svg(fig, DOSSIER, DEST["9.4_matrices_booleens"])


# ---------------------------------------------------------------------------
# 9.7 Masque de la source : C[dist_src < r_src] = C_max
# ---------------------------------------------------------------------------
def fig_masque_source():
    Lx = Ly = 50.0
    nx, ny = 120, 110
    x = np.linspace(0, Lx, nx)
    y = np.linspace(0, Ly, ny)
    X, Y = np.meshgrid(x, y)
    x_src, y_src, r_src = Lx / 4, Ly / 4, 1.5
    dist_src = np.sqrt((X - x_src) ** 2 + (Y - y_src) ** 2)
    masque = dist_src < r_src
    nsrc = int(masque.sum())
    print(f"  source : {nsrc} nœuds dans le disque")
    # fenêtre autour de la source
    j0 = np.argmin(abs(x - x_src))
    i0 = np.argmin(abs(y - y_src))
    J = np.arange(j0 - 5, j0 + 6)
    I = np.arange(i0 - 5, i0 + 6)

    fig = plt.figure(figsize=(20, 8.6))
    a1 = fig.add_axes([0.02, 0.15, 0.3, 0.72])
    a2 = fig.add_axes([0.36, 0.15, 0.3, 0.72])
    at = fig.add_axes([0.69, 0.0, 0.31, 1.0])
    at.axis("off")
    at.set_xlim(0, 1)
    at.set_ylim(0, 1)
    for ax in (a1, a2):
        ax.set_aspect("equal")
        ax.set_xlim(x[J[0]] - 0.3, x[J[-1]] + 0.3)
        ax.set_ylim(y[I[0]] - 0.3, y[I[-1]] + 0.3)
        ax.set_xlabel("x, m")
        ax.tick_params(labelsize=12)
    a1.set_ylabel("y, m")
    # panneau 1 : distance et masque
    for ax in (a1, a2):
        ax.add_patch(Circle((x_src, y_src), r_src, fc="none", ec=BLANC, lw=1.6, ls="--",
                            zorder=2))
    for i in I:
        for j in J:
            if masque[i, j]:
                a1.plot(x[j], y[i], "s", ms=15, color=VERT, zorder=3)
                a1.text(x[j], y[i], "1", ha="center", va="center", fontsize=10,
                        family=MONO, color="black", zorder=4, fontweight="bold")
                a2.plot(x[j], y[i], "o", ms=15, color=ORANGE, zorder=3)
            else:
                a1.plot(x[j], y[i], "s", ms=15, mfc=GRIS_FOND, mec=GRIS_BORD, zorder=3)
                a1.text(x[j], y[i], "0", ha="center", va="center", fontsize=10,
                        family=MONO, color="#666666", zorder=4)
                a2.plot(x[j], y[i], "o", ms=13, mfc=BLEU_FOND, mec=BLEU, mew=1.5, zorder=3)
    a1.plot(x_src, y_src, "+", color=BLANC, ms=14, mew=2, zorder=5)
    fleche(a1, (x_src, y_src), (x_src + r_src * np.cos(0.6), y_src + r_src * np.sin(0.6)),
           color=BLANC, lw=1.4, ms=10)
    a1.text(x_src + 0.4, y_src + 1.05, "r", fontsize=13, family=MONO, color=BLANC,
            zorder=6, bbox=dict(fc="black", ec="none", pad=1))
    a1.set_title("d < r", fontsize=18, family=MONO, color=VERT, pad=10)
    a2.set_title("C après la 3e ligne ci-contre", fontsize=18, family=MONO, color=ORANGE,
                 pad=10)
    for sp in list(a1.spines.values()) + list(a2.spines.values()):
        sp.set_color(GRIS_BORD)

    code(at, 0.0, 0.88, "X, Y = np.meshgrid(x, y)", fs=14)
    code(at, 0.0, 0.80, "d = np.sqrt((X - x0)**2 + (Y - y0)**2)", fs=14)
    at.text(0.0, 0.68, "une distance par nœud : taille (ny, nx)", fontsize=13, color=GRIS)
    code(at, 0.0, 0.55, "d < r", fs=14, color=VERT)
    at.text(0.0, 0.49, "matrice de booléens, taille (ny, nx)", fontsize=13, color=GRIS)
    code(at, 0.0, 0.36, "C[d < r] = C0", fs=14, color=ORANGE)
    at.text(0.0, 0.30, "n'écrit que dans les cases True", fontsize=13, color=GRIS)
    fig.text(0.34, 0.95, "Imposer une valeur dans une zone circulaire, sans boucle",
             ha="center", fontsize=17)
    sauver_svg(fig, DOSSIER, DEST["9.7_masque_source"])


def main():
    fig_matrices_booleens()
    fig_masque_source()


if __name__ == "__main__":
    main()
