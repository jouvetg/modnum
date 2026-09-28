"""Figures de la séance 8 (fond noir, SVG éditables).

Usage (depuis la racine) : python3 08_cours/fig/figures_s8.py
Écrit les SVG listés dans DEST, dans 08_cours/fig et les dossiers fig voisins.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch, Circle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# figure -> fichiers SVG écrits (chemins relatifs à ce dossier)
DEST = {
    '8.2_meshgrid': ['meshgrid_s8.svg', '../../08_tutoriel/fig/meshgrid_s8.svg'],
    '8.3_meshgrid_usage': ['../../08_tutoriel/fig/meshgrid_usage_s8.svg'],
}

FLUX = "#e8836f"      # flux de chaleur (flèches rouges de 08_exercice/fig/ex_1.png)
CROUTE = "#3a352b"
CMAP = "jet"          # comme ex_1.png et la solution (vmin=0, vmax=900)
VMIN, VMAX = 0, 900

# ---------------------------------------------------------------------------
# Paramètres et simulation : copie de 08_exercice_solution.ipynb
# ---------------------------------------------------------------------------
D, Lx, Lz = 150.0, 50.0, 25000.0 / 1000
T_haut, T_bas, T_bas_droite, q_base, duree = 25.0, 700.0, 900.0, 4500.0, 10.0
nx, nz = 50, 60
dx, dz = Lx / (nx - 1), Lz / (nz - 1)
x = np.linspace(0, Lx, nx)
z = np.linspace(0, Lz, nz)
dt_max = 0.01


# ---------------------------------------------------------------------------
# utilitaires
# ---------------------------------------------------------------------------
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


def code(ax, xx, yy, txt, color=BLANC, size=14, **kw):
    kw.setdefault("ha", "left")
    kw.setdefault("va", "center")
    return ax.text(xx, yy, txt, family=MONO, fontsize=size, color=color, **kw)


# ---------------------------------------------------------------------------
# 8.2 np.meshgrid : deux vecteurs -> deux matrices
# ---------------------------------------------------------------------------
def fig_meshgrid():
    xs = np.linspace(0, 3, 4)          # nx = 4
    ys = np.linspace(0, 2, 3)          # ny = 3
    Xs, Ys = np.meshgrid(xs, ys)
    jj, ii = 1, 2                      # point mis en valeur
    W = 1.0
    fig, ax = axes_vides((19, 8.4), (-0.3, 24.5), (-1.3, 9.0))

    # --- vecteurs ---
    code(ax, 0.0, 8.5, "x = np.linspace(0, 3, 4)", size=14)
    code(ax, 0.0, 7.9, "y = np.linspace(0, 2, 3)", size=14)
    for i, v in enumerate(xs):
        on = i == ii
        ax.add_patch(Rectangle((0.3 + i * W, 5.7), W, W, fc=ORANGE if on else BLEU_FOND,
                               ec="black" if on else BLEU, lw=1.5))
        code(ax, 0.3 + i * W + W / 2, 6.2, f"{v:g}", ha="center",
             color="black" if on else BLANC, size=15)
        code(ax, 0.3 + i * W + W / 2, 5.45, f"{i}", ha="center", va="top", color=GRIS,
             size=11)
    code(ax, 0.3 + 4 * W + 0.2, 6.2, "x  (nx,)", color=BLEU, size=14)
    for j, v in enumerate(ys):
        on = j == jj
        yb = 1.0 + j * W
        ax.add_patch(Rectangle((1.3, yb), W, W, fc=ORANGE if on else BLEU_FOND,
                               ec="black" if on else BLEU, lw=1.5))
        code(ax, 1.3 + W / 2, yb + W / 2, f"{v:g}", ha="center",
             color="black" if on else BLANC, size=15)
        code(ax, 1.15, yb + W / 2, f"{j}", ha="right", color=GRIS, size=11)
    code(ax, 2.5, 2.5, "y  (ny,)", color=BLEU, size=14)

    fleche(ax, (5.3, 4.0), (6.4, 4.0), color=BLANC, lw=2.2, ms=22)
    code(ax, 5.85, 4.55, "np.meshgrid", ha="center", size=13, color=GRIS)

    # --- matrices X et Y (ligne j = 0 en bas, comme origin='lower') ---
    def matrice(x0, M, nom):
        for j in range(3):
            for i in range(4):
                on = (i == ii and j == jj)
                ax.add_patch(Rectangle((x0 + i * W, 1.0 + j * W), W, W,
                                       fc=ORANGE if on else BLEU_FOND,
                                       ec="black" if on else BLEU, lw=1.5))
                code(ax, x0 + i * W + W / 2, 1.0 + j * W + W / 2, f"{M[j, i]:g}",
                     ha="center", color="black" if on else BLANC, size=15)
        for i in range(4):
            code(ax, x0 + i * W + W / 2, 0.85, f"{i}", ha="center", va="top", color=GRIS,
                 size=11)
        for j in range(3):
            code(ax, x0 - 0.15, 1.0 + j * W + W / 2, f"{j}", ha="right", color=GRIS,
                 size=11)
        code(ax, x0 + 2 * W, 0.3, "i (colonne) →", ha="center", va="top", color=GRIS,
             size=11)
        code(ax, x0 + 2 * W, 4.4, f"{nom}  (ny, nx) = (3, 4)", ha="center", color=BLEU,
             size=14)
    matrice(7.2, Xs, "X")
    matrice(12.2, Ys, "Y")
    ax.text(7.2 + 2, 5.3, "x recopié sur\nchaque ligne", ha="center", va="center",
            fontsize=12.5, color=GRIS)
    ax.text(12.2 + 2, 5.3, "y recopié sur\nchaque colonne", ha="center", va="center",
            fontsize=12.5, color=GRIS)
    ax.text(10.7, 7.2, "X, Y = np.meshgrid(x, y)", ha="center", va="center",
            fontsize=16, family=MONO)
    ax.text(10.7, -0.6, "ligne j = 0 en bas, comme imshow(…, origin='lower')",
            ha="center", va="center", fontsize=12, color=GRIS)

    # --- grille physique ---
    gx0, gy0, s = 18.3, 1.0, 1.55
    for j in range(3):
        ax.plot([gx0, gx0 + 3 * s], [gy0 + j * s] * 2, color=GRIS_BORD, lw=1, zorder=0)
    for i in range(4):
        ax.plot([gx0 + i * s] * 2, [gy0, gy0 + 2 * s], color=GRIS_BORD, lw=1, zorder=0)
    for j in range(3):
        for i in range(4):
            on = (i == ii and j == jj)
            ax.plot(gx0 + i * s, gy0 + j * s, "o", ms=16 if on else 11,
                    mfc=ORANGE if on else BLEU_FOND, mec=ORANGE if on else BLEU, mew=2)
    for i in range(4):
        code(ax, gx0 + i * s, gy0 - 0.4, f"{xs[i]:g}", ha="center", va="top", size=12,
             color=GRIS)
    for j in range(3):
        code(ax, gx0 - 0.35, gy0 + j * s, f"{ys[j]:g}", ha="right", size=12, color=GRIS)
    ax.text(gx0 + 1.5 * s, gy0 - 1.05, "x", ha="center", va="top", fontsize=14,
            color=GRIS, style="italic")
    ax.text(gx0 - 1.0, gy0 + s, "y", ha="center", va="center", fontsize=14,
            color=GRIS, style="italic")
    px, py = gx0 + ii * s, gy0 + jj * s
    ax.text(px + 0.25, py + 0.35, "point (i=2, j=1)", fontsize=13, color=ORANGE,
            ha="left", va="bottom")
    code(ax, gx0 + 1.5 * s, 6.6, "X[1, 2] = 2   → sa coordonnée x", ha="center",
         color=ORANGE, size=13.5)
    code(ax, gx0 + 1.5 * s, 5.9, "Y[1, 2] = 1   → sa coordonnée y", ha="center",
         color=ORANGE, size=13.5)
    ax.text(gx0 + 1.5 * s, 7.6, "la grille des points", ha="center", va="center",
            fontsize=15)
    ax.text(gx0 + 1.5 * s, 8.5, "X[j, i], Y[j, i] : ligne j d'abord !", ha="center",
            va="center", fontsize=14, color=VERT, family=MONO)
    sauver_svg(fig, DOSSIER, DEST["8.2_meshgrid"])


# ---------------------------------------------------------------------------
# 8.3 Utiliser X, Y (ou X, Z) : condition initiale et masques
# ---------------------------------------------------------------------------
def fig_meshgrid_usage():
    fig = plt.figure(figsize=(20, 8.6))
    # --- exemple générique : un champ 2D calculé sans boucle ---
    axg = fig.add_axes([0.0, 0.0, 0.52, 1.0])
    axg.axis("off")
    axg.set_xlim(-0.5, 11.5)
    axg.set_ylim(-1.8, 9.2)
    nxs, nys = 4, 6
    xs = np.arange(nxs, dtype=float)
    ys = np.arange(nys, dtype=float)
    Xs, Ys = np.meshgrid(xs, ys)
    Cs = Xs + Ys
    cm = plt.get_cmap("viridis")
    W, H = 0.8, 1.0

    def mat(x0, M, colore=False):
        for j in range(nys):
            for i in range(nxs):
                fc = cm(M[j, i] / Cs.max()) if colore else BLEU_FOND
                axg.add_patch(Rectangle((x0 + i * W, j * H), W, H, fc=fc,
                                        ec="black" if colore else BLEU, lw=1.3))
                axg.text(x0 + i * W + W / 2, j * H + H / 2, f"{M[j, i]:g}", ha="center",
                         va="center", family=MONO, fontsize=12.5,
                         color="black" if colore and M[j, i] > 3 else BLANC)
        for j in range(nys):
            axg.text(x0 - 0.1, j * H + H / 2, f"{j}", ha="right", va="center",
                     family=MONO, fontsize=10.5, color=GRIS)
    xX, xY, xC = 0.4, 4.3, 8.2
    mat(xX, Xs)
    mat(xY, Ys)
    mat(xC, Cs, colore=True)
    for x0, nom, col in [(xX, "X", BLEU), (xY, "Y", BLEU), (xC, "C", ORANGE)]:
        axg.text(x0 + 2 * W, 6.3, nom, ha="center", va="bottom", family=MONO,
                 fontsize=16, color=col)
    axg.text(xX + 4 * W + 0.27, 3.0, "+", ha="center", va="center", fontsize=24)
    axg.text(xY + 4 * W + 0.27, 3.0, "=", ha="center", va="center", fontsize=24)
    axg.text(5.5, 8.7, "construire un champ 2D, sans boucle", ha="center",
             va="center", fontsize=16)
    code(axg, 5.5, 7.75, "X, Y = np.meshgrid(x, y)", ha="center", size=13.5)
    code(axg, 5.5, 7.2, "C = X + Y", ha="center", size=13.5, color=ORANGE)
    axg.text(5.5, -0.6, "x = [0, 1, 2, 3],  y = [0, 1, …, 5] : chaque case de C\n"
             "est calculée à partir de ses propres coordonnées", ha="center", va="top",
             fontsize=12, color=GRIS)

    # --- masques du tutoriel (grille réelle du tutoriel, zoom) ---
    xt = np.linspace(0, 10, 100)
    yt = np.linspace(0, 3, 50)
    Xt, Yt = np.meshgrid(xt, yt)
    x0, y0, seuil = 5.0, 2.0, 0.5
    d_disque = np.sqrt((Xt - x0) ** 2 + (Yt - y0) ** 2)
    d_carre = np.maximum(np.abs(Xt - x0), np.abs(Yt - y0))
    sel = (np.abs(Xt - x0) < 0.85) & (np.abs(Yt - y0) < 0.85)
    for k, (d, nom, formule) in enumerate(
            ((d_disque, "d_disque", "np.sqrt((X-x0)**2 + (Y-y0)**2)"),
             (d_carre, "d_carre", "np.maximum(np.abs(X-x0), np.abs(Y-y0))"))):
        ax = fig.add_axes([0.56 + k * 0.23, 0.24, 0.2, 0.5])
        m = (d < seuil) & sel
        ax.plot(Xt[sel & ~m], Yt[sel & ~m], "o", ms=3.2, color=GRIS_BORD)
        ax.plot(Xt[m], Yt[m], "o", ms=5, color=ORANGE)
        ax.plot(x0, y0, "*", ms=16, color=ROUGE, mec="black")
        if k == 0:
            ax.add_patch(Circle((x0, y0), seuil, fc="none", ec=VERT, lw=2))
        else:
            ax.add_patch(Rectangle((x0 - seuil, y0 - seuil), 2 * seuil, 2 * seuil,
                                   fc="none", ec=VERT, lw=2))
        ax.set_xlim(x0 - 0.8, x0 + 0.8)
        ax.set_ylim(y0 - 0.8, y0 + 0.8)
        ax.set_aspect("equal")
        ax.set_xticks([4.5, 5, 5.5])
        ax.set_yticks([1.5, 2, 2.5])
        ax.tick_params(labelsize=11)
        ax.set_title(f"{nom} < seuil", family=MONO, fontsize=15, color=ORANGE, pad=10)
        fig.text(0.56 + k * 0.23 + 0.1, 0.86 - 0.0 * k, formule, ha="center",
                 va="center", family=MONO, fontsize=11.2, color=BLANC)
        fig.text(0.56 + k * 0.23 + 0.1, 0.16,
                 "un disque" if k == 0 else "un carré", ha="center", va="center",
                 fontsize=14, color=VERT)
    fig.text(0.775, 0.955, "masques du tutoriel : x0 = 5, y0 = 2, seuil = 0.5",
             ha="center", va="center", fontsize=16)
    fig.text(0.64, 0.07, "● True (dans la zone)", ha="center", va="center",
             fontsize=12.5, color=ORANGE)
    fig.text(0.76, 0.07, "● False", ha="center", va="center", fontsize=12.5, color=GRIS)
    fig.text(0.86, 0.07, "★ (x0, y0)", ha="center", va="center", fontsize=12.5,
             color=ROUGE)
    sauver_svg(fig, DOSSIER, DEST["8.3_meshgrid_usage"])


def main():
    fig_meshgrid()
    fig_meshgrid_usage()


if __name__ == "__main__":
    if len(sys.argv) > 1:              # p.ex. python3 figures_s8.py fig_meshgrid
        for nom in sys.argv[1:]:
            globals()[nom]()
    else:
        main()
