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
    '4.5_temperature_sol': ['temperature_sol_s4.svg'],
    '4.6_conservation': ['principe_conservation_s4.svg'],
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
# 4.5 Le sol filtre les saisons : onde thermique saisonnière (solution exacte)
# ---------------------------------------------------------------------------
def fig_temperature_sol():
    D = 1e-6                                  # diffusivité d'un sol courant, m2/s
    an = 365.25 * 24 * 3600                   # une année, s
    w = 2 * np.pi / an
    d = np.sqrt(2 * D / w)                    # profondeur d'amortissement, ~3.2 m
    Tm, A = 10.0, 10.0                        # moyenne annuelle et amplitude en surface, °C
    t_froid = 15 / 365.25                     # le plus froid en surface : mi-janvier

    def T(z, t_an):                           # t en années
        return Tm - A * np.exp(-z / d) * np.cos(w * (t_an - t_froid) * an - z / d)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 7.2),
                                 gridspec_kw=dict(width_ratios=[1, 1.45], wspace=0.28))
    # --- gauche : profils T(z) aux quatre saisons, et enveloppe
    z = np.linspace(0, 15, 300)
    env = A * np.exp(-z / d)
    a1.fill_betweenx(z, Tm - env, Tm + env, color="#22303d", lw=0)
    a1.plot(Tm - env, z, color=GRIS, lw=1, ls="--")
    a1.plot(Tm + env, z, color=GRIS, lw=1, ls="--")
    saisons = [("mi-janvier", 15, BLEU), ("mi-avril", 105, VERT),
               ("mi-juillet", 196, ORANGE), ("mi-octobre", 288, ROUGE)]
    for nom, jour, col in saisons:
        a1.plot(T(z, jour / 365.25), z, color=col, lw=2.6, label=nom)
    a1.axvline(Tm, color=GRIS, lw=1, ls=":")
    a1.set_ylim(15, 0)
    a1.set_xlim(-1, 21)
    a1.set_xlabel("température, °C", fontsize=15)
    a1.set_ylabel("profondeur, m", fontsize=15)
    a1.legend(loc="lower left", fontsize=13, frameon=False)
    a1.text(Tm + 0.4, 12.6, "vers 10 m :\nquasi constante\n≈ moyenne annuelle", fontsize=13,
            color=BLANC, va="center")
    a1.set_title("profils de température aux 4 saisons", fontsize=16, pad=12)

    # --- droite : T au cours de l'année, à plusieurs profondeurs
    t = np.linspace(0, 1, 400)
    mins = []
    for zz, col, lw in [(0, BLANC, 2.6), (1, "#bfe3ff", 2.2), (3, BLEU, 2.2), (6, "#3d7fbf", 2.2)]:
        a2.plot(t * 12, T(zz, t), color=col, lw=lw)
        tmin = (t_froid + zz / d / (2 * np.pi)) % 1          # instant le plus froid à zz
        mins.append((tmin * 12, T(zz, tmin)))
        a2.plot(tmin * 12, T(zz, tmin), "o", color=col, ms=8, zorder=4)
        a2.text(12.15, T(zz, 1.0), f"z = {zz} m", color=col, fontsize=14, va="center")
    mx, my = zip(*mins)
    a2.plot(mx, my, color=GRIS, lw=1.3, ls=":", zorder=3)
    a2.text(mx[-1] + 0.25, my[-1] - 1.3, "le plus froid arrive\nde plus en plus tard",
            fontsize=13, color=GRIS, va="top")
    a2.set_xlim(0, 13.6)
    a2.set_ylim(-1, 21)
    a2.set_xticks(np.arange(0.5, 12, 1))
    a2.set_xticklabels(list("JFMAMJJASOND"), fontsize=13)
    a2.set_ylabel("température, °C", fontsize=15)
    a2.set_title("température au cours de l'année, à différentes profondeurs", fontsize=16,
                 pad=12)
    for a in (a1, a2):
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
        a.tick_params(labelsize=12)

    sauver_svg(fig, DOSSIER, DEST["4.5_temperature_sol"])


# ---------------------------------------------------------------------------
# 4.6 Principe de conservation : bilan de particules dans une cellule
# ---------------------------------------------------------------------------
def fig_conservation():
    fig, ax = axes_vides((12, 5.6), (0, 12), (0, 5.6))
    x0, x1, y0, y1 = 4.2, 7.8, 1.5, 3.4                 # la cellule
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=GRIS_FOND, ec=BLANC, lw=2.5))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.25, r"$n$ particules", ha="center",
            va="center", fontsize=20)
    ax.text((x0 + x1) / 2, (y0 + y1) / 2 - 0.35, r"$C = n\,/\,dx$", ha="center",
            va="center", fontsize=17, color=GRIS)
    # ce qui reste dans la cellule
    ax.add_patch(Rectangle((x0, y1), x1 - x0, 0.75, fc="none", ec=VERT, lw=2, ls="--"))
    ax.text((x0 + x1) / 2, y1 + 0.38, r"$\Delta n$", ha="center", va="center",
            fontsize=21, color=VERT)
    ax.text((x0 + x1) / 2, y1 + 1.05, "ce qui reste dans la cellule, pendant $dt$",
            ha="center", va="center", fontsize=15, color=VERT)
    # flux entrant et sortant
    ym = (y0 + y1) / 2
    fleche(ax, (1.6, ym), (x0 - 0.05, ym), color=ORANGE, lw=3, ms=22)
    fleche(ax, (x1 + 0.05, ym), (10.4, ym), color=ORANGE, lw=3, ms=22)
    ax.text((1.6 + x0) / 2, ym + 0.45, r"$q_x(x)$", ha="center", fontsize=20, color=ORANGE)
    ax.text((1.6 + x0) / 2, ym - 0.6, "ce qui entre", ha="center", fontsize=14,
            color=ORANGE)
    ax.text((x1 + 10.4) / 2, ym + 0.45, r"$q_x(x+dx)$", ha="center", fontsize=20,
            color=ORANGE)
    ax.text((x1 + 10.4) / 2, ym - 0.6, "ce qui sort", ha="center", fontsize=14,
            color=ORANGE)
    # largeur de la cellule
    fleche(ax, (x0, y0 - 0.35), (x1, y0 - 0.35), color=BLANC, lw=1.6, ms=14, style="<|-|>")
    ax.text((x0 + x1) / 2, y0 - 0.7, r"$dx$", ha="center", va="top", fontsize=19)
    sauver_svg(fig, DOSSIER, DEST["4.6_conservation"])


def main():
    fig_grille_1d()
    fig_slicing()
    fig_grille_decalee()
    fig_temperature_sol()
    fig_conservation()


if __name__ == "__main__":
    main()
