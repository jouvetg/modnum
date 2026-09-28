"""Figures de la séance 4 (fond noir, SVG éditables).

Usage (depuis la racine) : python3 04_cours/fig/figures_s4.py
Écrit les SVG listés dans DEST, dans 04_cours/fig et les dossiers fig voisins.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# figure -> fichiers SVG écrits (chemins relatifs à ce dossier)
DEST = {
    '4.1_grille_1d': ['grille_1d_s4.svg', '../../04_tutoriel/fig/grille_1d_s4.svg'],
    '4.2_slicing': ['slicing_s4.svg', '../../04_tutoriel/fig/slicing_s4.svg'],
    '4.3_grille_decalee': ['grille_decalee_s4.svg'],
    '4.4_conditions_bords': ['../../04_exercice/fig/conditions_bords.svg'],
}

# couleurs de la figure fuite_chimique_shema_s5 (sol, molasse, rivière, polluant)
SOL = "#3a352b"
MOLASSE = "#2a2a33"
RIVIERE = "#5aa9d8"
POLLUANT = "#e8836f"


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


# ---------------------------------------------------------------------------
# 4.1 Grille 1D et variable discrétisée
# ---------------------------------------------------------------------------
def fig_grille_1d():
    a, b, nx = 0, 1, 11
    dx = (b - a) / (nx - 1)
    x = np.linspace(a, b, nx)
    xp = 0.63
    ixp = round((xp - a) / dx)
    C = np.ones(nx) * 2
    C[ixp] = 6

    fig, ax = axes_vides((16, 8), (-0.2, 1.2), (-2.6, 5.5))
    s = 0.45  # échelle verticale des barres (C=6 -> 2.7)

    # axe x et nœuds
    ax.plot([a, b], [0, 0], color=BLANC, lw=2)
    for i, xi in enumerate(x):
        ax.plot([xi, xi], [-0.12, 0.12], color=BLANC, lw=2)
        ax.text(xi, -0.35, f"{i}", ha="center", va="top", fontsize=15, family=MONO,
                color=ORANGE if i == ixp else GRIS)
        ax.text(xi, -0.9, f"{xi:.1f}", ha="center", va="top", fontsize=13, family=MONO,
                color=BLANC)
    ax.text(a - 0.05, -0.35, "i", ha="right", va="top", fontsize=15, family=MONO, color=GRIS)
    ax.text(a - 0.05, -0.9, "x[i]", ha="right", va="top", fontsize=13, family=MONO,
            color=BLANC)
    ax.text(a - 0.02, 0, "a", ha="right", va="center", fontsize=17, style="italic")
    ax.text(b + 0.02, 0, "b", ha="left", va="center", fontsize=17, style="italic")

    # cote dx entre x_2 et x_3
    yc = -1.75
    fleche(ax, (x[2], yc), (x[3], yc), color=BLANC, style="<|-|>", ms=12, lw=1.3)
    for xi in (x[2], x[3]):
        ax.plot([xi, xi], [yc - 0.12, -1.45], color=GRIS, lw=0.8, ls=":")
    ax.text((x[2] + x[3]) / 2, yc - 0.15, "dx = 0.1", ha="center", va="top", fontsize=14,
            family=MONO)

    # barres C
    w = 0.045
    for i, xi in enumerate(x):
        orange = i == ixp
        ax.add_patch(Rectangle((xi - w / 2, 0.15), w, C[i] * s,
                               fc=ORANGE if orange else BLEU_FOND,
                               ec=ORANGE if orange else BLEU, lw=1.5))
        ax.text(xi, 0.15 + C[i] * s + 0.1, f"{C[i]:g}", ha="center", va="bottom",
                fontsize=13, family=MONO, color=ORANGE if orange else BLEU,
                fontweight="bold" if orange else "normal")
    ax.text(a - 0.05, 0.15 + 2 * s * 0.75, "C", ha="right", va="center", fontsize=18,
            family=MONO, color=BLEU)

    # point xp
    yxp = 4.3
    ax.plot([xp, xp], [yxp - 0.2, 0], color=VERT, lw=1.2, ls="--")
    ax.plot([xp], [0], marker="v", color=VERT, ms=11, zorder=5)
    ax.text(xp, yxp, "xp = 0.63", ha="center", va="bottom", fontsize=15, family=MONO,
            color=VERT)
    fleche(ax, (xp - 0.005, yxp - 0.35), (x[ixp] + 0.005, 0.15 + C[ixp] * s + 0.5),
           color=ORANGE, rad=0.35, lw=1.8)
    ax.text(0.72, 3.55, "ixp = round((xp − a)/dx)\n    = round(6.3) = 6", ha="left",
            va="center", fontsize=14, family=MONO, color=ORANGE)
    ax.text(0.72, 2.55, "C[ixp] = 6", ha="left", va="center", fontsize=14, family=MONO,
            color=ORANGE)

    # code d'initialisation
    ax.text(a - 0.15, 5.3, "x = np.linspace(a, b, nx)     # a = 0, b = 1, nx = 11\n"
            "C = np.ones(nx)*2", ha="left", va="top", fontsize=14, family=MONO,
            color=BLANC, linespacing=1.5)
    sauver_svg(fig, DOSSIER, DEST["4.1_grille_1d"])


# ---------------------------------------------------------------------------
# 4.2 Slicing
# ---------------------------------------------------------------------------
def fig_slicing():
    n = 9
    W, H, X0 = 1.0, 0.62, 2.6
    lignes = [("x[1:]", range(1, 9)), ("x[3:]", range(3, 9)), ("x[3:5]", range(3, 5)),
              ("x[3:7]", range(3, 7)), ("x[:-1]", range(0, 8)), ("x[:-4]", range(0, 5)),
              ("x[::2]", range(0, 9, 2))]
    pas = 0.92
    y_top = len(lignes) * pas + 0.3
    fig, ax = axes_vides((16, 8.2), (0, 17.0), (-0.35, y_top + 1.15))

    def rangee(y, sel, label, couleur_label=BLANC):
        ax.text(X0 - 0.3, y + H / 2, label, ha="right", va="center", fontsize=17,
                family=MONO, color=couleur_label)
        for k in range(n):
            on = k in sel
            ax.add_patch(Rectangle((X0 + k * W, y), W, H,
                                   fc=ORANGE if on else GRIS_FOND,
                                   ec="black" if on else GRIS_BORD, lw=1.5))
            ax.text(X0 + k * W + W / 2, y + H / 2, f"{k}", ha="center", va="center",
                    fontsize=14, family=MONO, color="black" if on else "#666666",
                    fontweight="bold" if on else "normal")
        ax.text(X0 + n * W + 0.35, y + H / 2, "→  indices " + ", ".join(str(k) for k in sel),
                ha="left", va="center", fontsize=14, family=MONO,
                color=ORANGE if sel else GRIS)

    # vecteur complet
    ax.text(X0 - 0.3, y_top + H / 2, "x", ha="right", va="center", fontsize=17,
            family=MONO)
    for k in range(n):
        ax.add_patch(Rectangle((X0 + k * W, y_top), W, H, fc=BLEU_FOND, ec=BLEU, lw=1.5))
        ax.text(X0 + k * W + W / 2, y_top + H / 2, f"{k}", ha="center", va="center",
                fontsize=14, family=MONO)
        ax.text(X0 + k * W + W / 2, y_top + H + 0.1, f"{k - n}", ha="center", va="bottom",
                fontsize=11, family=MONO, color=GRIS)
    ax.text(X0 + n * W + 0.35, y_top + H / 2, "taille 9 : indices 0 … 8", ha="left",
            va="center", fontsize=14, family=MONO, color=BLEU)
    ax.text(X0 + n * W + 0.35, y_top + H + 0.1, "(en gris : indices négatifs)",
            ha="left", va="bottom", fontsize=11, color=GRIS)

    for j, (label, sel) in enumerate(lignes):
        y = (len(lignes) - 1 - j) * pas
        rangee(y, list(sel), label)
        if label == "x[3:5]":
            # case 5 : fin exclue
            ax.add_patch(Rectangle((X0 + 5 * W, y), W, H, fc="none", ec=ROUGE, lw=2.2,
                                   ls="--", zorder=4))
            ax.add_patch(Rectangle((X0 + 3 * W, y), W, H, fc="none", ec=VERT, lw=2.6,
                                   zorder=4))
            ax.text(X0 + n * W + 3.4, y + H / 2 + 0.17, "début 3 : inclus",
                    ha="left", va="center", fontsize=14, color=VERT)
            ax.text(X0 + n * W + 3.4, y + H / 2 - 0.17, "fin 5 : exclue",
                    ha="left", va="center", fontsize=14, color=ROUGE)
    sauver_svg(fig, DOSSIER, DEST["4.2_slicing"])


# ---------------------------------------------------------------------------
# 4.3 Grille décalée : C, qx, dCdt
# ---------------------------------------------------------------------------
def fig_grille_decalee():
    nx = 7
    dxg = 1.35
    X0 = 5.3
    xn = X0 + dxg * np.arange(nx)             # nœuds
    xc = (xn[1:] + xn[:-1]) / 2               # centres
    yC, yq, yd, yN = 6.0, 4.2, 2.4, 0.6
    fig, ax = axes_vides((16, 8.4), (-0.2, 17.6), (-0.3, 7.6))

    # repères verticaux aux nœuds
    for xi in xn:
        ax.plot([xi, xi], [yN - 0.45, yC + 0.45], color="#333333", lw=1, ls=":", zorder=0)

    # liens (flèches fines) : qx_i <- C_i, C_i+1 ; dCdt_i <- qx_i, qx_i+1
    k_ex = 2  # exemple mis en valeur
    for i in range(nx - 1):
        col, lw = (ORANGE, 1.8) if i == k_ex else ("#555555", 0.9)
        for xs in (xn[i], xn[i + 1]):
            fleche(ax, (xs, yC - 0.2), (xc[i], yq + 0.22), color=col, lw=lw, ms=10)
    for i in range(nx - 2):
        col, lw = (ORANGE, 1.8) if i == k_ex else ("#555555", 0.9)
        for xs in (xc[i], xc[i + 1]):
            fleche(ax, (xs, yq - 0.2), (xn[i + 1], yd + 0.22), color=col, lw=lw, ms=10)
        fleche(ax, (xn[i + 1], yd - 0.22), (xn[i + 1], yN + 0.24),
               color=ORANGE if i == k_ex else "#555555", lw=1.8 if i == k_ex else 0.9,
               ms=10)

    # rangée C (déjà stocké)
    ax.plot(xn, [yC] * nx, "o", ms=17, mfc=BLEU_FOND, mec=BLEU, mew=2)
    for i, xi in enumerate(xn):
        ax.text(xi, yC + 0.35, f"C[{i}]", ha="center", va="bottom", fontsize=12,
                family=MONO, color=BLEU)
    # rangée qx (centres des cellules)
    ax.plot(xc, [yq] * (nx - 1), "s", ms=15, mfc=ORANGE, mec=ORANGE)
    for i, xi in enumerate(xc):
        ax.text(xi + 0.2, yq, f"qx[{i}]", ha="left", va="center", fontsize=12,
                family=MONO, color=ORANGE)
    # rangée dCdt (nœuds intérieurs)
    ax.plot(xn[1:-1], [yd] * (nx - 2), "o", ms=15, mfc=ORANGE, mec=ORANGE)
    for i, xi in enumerate(xn[1:-1]):
        ax.text(xi + 0.2, yd, f"dCdt[{i}]", ha="left", va="center", fontsize=11,
                family=MONO, color=ORANGE)
    # rangée C mis à jour
    ax.plot(xn[1:-1], [yN] * (nx - 2), "o", ms=17, mfc=ORANGE, mec=ORANGE)
    ax.plot(xn[[0, -1]], [yN] * 2, "o", ms=17, mfc=GRIS_FOND, mec=GRIS_BORD, mew=2)
    for i, xi in enumerate(xn):
        ax.text(xi, yN - 0.35, f"C[{i}]", ha="center", va="top", fontsize=12,
                family=MONO, color=GRIS if i in (0, nx - 1) else ORANGE)

    # code à gauche, taille à droite
    xcode, xtaille = -0.1, xn[-1] + 0.9
    rangs = [(yC, "C", "nx   = 7", BLEU),
             (yq, "qx = -D*(C[1:]-C[:-1])/dx", "nx-1 = 6", ORANGE),
             (yd, "dCdt = -(qx[1:]-qx[:-1])/dx", "nx-2 = 5", ORANGE),
             (yN, "C[1:-1] += dCdt*dt", "5 mis à jour", ORANGE)]
    for y, code, taille, col in rangs:
        ax.text(xcode, y, code, ha="left", va="center", fontsize=13.5, family=MONO,
                color=BLANC)
        ax.text(xtaille, y, taille, ha="left", va="center", fontsize=14, family=MONO,
                color=col)
    ax.text(xtaille, yC + 0.75, "taille", ha="left", va="bottom", fontsize=13, color=GRIS)
    ax.text(xcode, yC + 0.75, "code", ha="left", va="bottom", fontsize=13, color=GRIS)
    ax.text(xtaille, yN - 0.48, "C[0], C[-1] : non mis\nà jour par C[1:-1] += …",
            ha="left", va="top", fontsize=12, color=GRIS)

    # légende sur l'emplacement
    ax.text((xn[0] + xn[-1]) / 2, 7.45, "nœuds  ●      centres des cellules  ■",
            ha="center", va="top", fontsize=13, color=GRIS)
    sauver_svg(fig, DOSSIER, DEST["4.3_grille_decalee"])


# ---------------------------------------------------------------------------
# 4.4 Conditions aux bords (Daillens)
# ---------------------------------------------------------------------------
def fig_bords():
    fig, (axg, axd) = plt.subplots(1, 2, figsize=(16, 7.4))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.9, bottom=0.14, wspace=0.12)
    nn = 6
    dxg = 1.0

    # --- bord gauche : Neumann
    ax = axg
    xn = dxg * np.arange(nn)
    Cg = np.array([1.0, 1.0, 1.35, 1.9, 2.55, 3.2])
    ax.add_patch(Rectangle((-0.9, -0.35), 0.9, 4.3, fc=MOLASSE, ec=GRIS_BORD,
                           hatch="//", lw=1))
    ax.text(-0.45, 1.8, "molasse imperméable", rotation=90, ha="center", va="center",
            fontsize=13, color=BLANC)
    ax.add_patch(Rectangle((0, -0.35), xn[-1] + 0.6, 4.3, fc=SOL, ec="none", zorder=0))
    ax.plot(xn, Cg, "-", color=POLLUANT, lw=2.2)
    ax.plot(xn[1:], Cg[1:], "o", ms=12, mfc=BLEU_FOND, mec=BLEU, mew=2, zorder=4)
    ax.plot(xn[0], Cg[0], "o", ms=13, mfc=VERT, mec=VERT, zorder=5)
    ax.plot(xn[:2], Cg[:2], "-", color=VERT, lw=4, zorder=3)
    for i, xi in enumerate(xn):
        ax.text(xi, -0.55, f"C[{i}]", ha="center", va="top", fontsize=13, family=MONO,
                color=VERT if i == 0 else BLEU)
    ax.text(0.5, Cg[0] + 0.3, "pente nulle", ha="center", va="bottom", fontsize=13,
            color=VERT)
    # flux : rien ne sort
    fleche(ax, (2.3, 0.55), (0.25, 0.55), color=GRIS, lw=1.6, ms=14)
    ax.text(1.3, 0.2, "diffusion vers le mur", ha="center", va="top", fontsize=12,
            color=GRIS)
    ax.text(0.05, 3.25, "flux nul :\nrien ne sort", ha="left", va="center", fontsize=14,
            color=VERT)
    ax.set_xlim(-1.0, xn[-1] + 0.6)
    ax.set_ylim(-1.1, 4.0)
    ax.axis("off")
    ax.set_title("Bord gauche : Neumann", fontsize=17, color=BLANC, pad=12)
    ax.text(0.5, -0.07, "C[0] = C[1]", transform=ax.transAxes, ha="center", va="top",
            fontsize=17, family=MONO, color=VERT)

    # --- bord droit : Dirichlet
    ax = axd
    xn = dxg * np.arange(nn)
    Cd = np.array([2.6, 2.1, 1.6, 1.07, 0.54, 0.0])
    ax.add_patch(Rectangle((-0.6, -0.35), xn[-1] + 0.6, 4.3, fc=SOL, ec="none", zorder=0))
    ax.plot([xn[-1], xn[-1]], [-0.35, 3.95], color=GRIS, lw=1.2, ls="--")
    ax.plot(xn, Cd, "-", color=POLLUANT, lw=2.2)
    ax.plot(xn[:-1], Cd[:-1], "o", ms=12, mfc=BLEU_FOND, mec=BLEU, mew=2, zorder=4)
    ax.plot(xn[-1], Cd[-1], "o", ms=13, mfc=VERT, mec=VERT, zorder=5)
    labels = ["C[-6]", "C[-5]", "C[-4]", "C[-3]", "C[-2]", "C[-1]"]
    for i, xi in enumerate(xn):
        ax.text(xi, -0.55, labels[i], ha="center", va="top", fontsize=13, family=MONO,
                color=VERT if i == nn - 1 else BLEU)
    ax.text(xn[-1] + 0.15, 0.05, "C = 0\nimposé", ha="left", va="bottom", fontsize=13,
            color=VERT)
    fleche(ax, (xn[-1] - 1.6, 1.7), (xn[-1] + 1.1, 1.7), color=POLLUANT, lw=2.5, ms=20)
    ax.text(xn[-1] - 0.35, 1.95, "le polluant sort", ha="center", va="bottom",
            fontsize=14, color=POLLUANT)
    ax.set_xlim(-0.6, xn[-1] + 1.2)
    ax.set_ylim(-1.1, 4.0)
    ax.axis("off")
    ax.set_title("Bord droit : Dirichlet", fontsize=17, color=BLANC, pad=12)
    ax.text(0.5, -0.07, "C[-1] = 0", transform=ax.transAxes, ha="center", va="top",
            fontsize=17, family=MONO, color=VERT)
    sauver_svg(fig, DOSSIER, DEST["4.4_conditions_bords"])


def main():
    fig_grille_1d()
    fig_slicing()
    fig_grille_decalee()
    fig_bords()


if __name__ == "__main__":
    main()
