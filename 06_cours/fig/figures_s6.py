"""Figures de la séance 6 (fond noir, SVG éditables).

Usage (depuis la racine) : python3 06_cours/fig/figures_s6.py
Écrit les SVG listés dans DEST, dans 06_cours/fig et les dossiers fig voisins.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

DOSSIER = os.path.dirname(os.path.abspath(__file__))

# figure -> fichiers SVG écrits (chemins relatifs à ce dossier)
DEST = {
    '6.3_splitting': ['splitting_s6.svg'],
    '6.5_upwind_slicing': ['upwind_slicing_s6.svg'],
    '6.7_domaine_riviere': ['../../06_exercice/fig/domaine_riviere.svg'],
}

# couleurs reprises de 06_cours/fig/advection_v_s9.png (Vx > 0 rose, Vx < 0 cyan)
ROSE = "#ea6fb5"
CYAN = "#4fd1d1"
# couleurs des trois processus (figure du splitting)
DIFF = "#b39dff"      # diffusion
ADV = ROSE            # advection
REAC = "#f2e36b"      # réaction
RIVIERE = "#5aa9d8"
POLLUANT = "#e8836f"


# ---------------------------------------------------------------------------
# outils
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


def largeur(ax, t):
    """Largeur (unités de données) d'un objet texte déjà placé."""
    r = ax.figure.canvas.get_renderer()
    bb = t.get_window_extent(renderer=r)
    inv = ax.transData.inverted()
    return inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0]


def ligne(ax, x, y, morceaux, fontsize=16, family=MONO, ha="left", va="center", gap=0.0,
          **kw):
    """Écrit une ligne faite de morceaux (texte, couleur) juxtaposés.

    En police mono, la largeur est calculée au nombre de caractères (les espaces comptent) ;
    sinon (mathtext) à partir de l'emprise du texte, plus `gap` entre morceaux.
    """
    if family == MONO:
        ref = ax.text(0, 0, "M" * 20, fontsize=fontsize, family=MONO)
        wc = largeur(ax, ref) / 20
        ref.remove()
    objets, cur = [], x
    for s, c in morceaux:
        t = ax.text(cur, y, s, color=c, fontsize=fontsize, family=family, ha="left",
                    va=va, **kw)
        cur += (len(s) * wc) if family == MONO else (largeur(ax, t) + gap)
        objets.append(t)
    total = cur - x - (0 if family == MONO else gap)
    dec = {"left": 0, "center": total / 2, "right": total}[ha]
    for t in objets:
        px, py = t.get_position()
        t.set_position((px - dec, py))
    return objets


# ---------------------------------------------------------------------------
# 6.3 Splitting : un pas de temps en trois étapes
# ---------------------------------------------------------------------------
def fig_splitting():
    # petit calcul réel, effets volontairement exagérés pour être visibles
    nx, Lx = 101, 10.0
    x = np.linspace(0, Lx, nx)
    dx = Lx / (nx - 1)
    C = np.where((x >= 2.0) & (x <= 3.5), 1.0, 0.0)
    etats = [C.copy()]
    D = 1.0
    dt = dx ** 2 / (2.1 * D)
    for _ in range(60):                       # diffusion
        qx = - D * (C[1:] - C[:-1]) / dx
        dCdt_d = - (qx[1:] - qx[:-1]) / dx
        C[1:-1] += dt * dCdt_d
    etats.append(C.copy())
    Vx = 1.0
    dt = dx / (2.1 * abs(Vx))
    for _ in range(45):                       # advection
        dCdt_a = -Vx * (C[1:] - C[:-1]) / dx
        C[1:] += dt * dCdt_a
    etats.append(C.copy())
    dCdt_r = - C * 0.35                       # réaction (un pas « gamma*dt = 0.35 »)
    C += 1.0 * dCdt_r
    etats.append(C.copy())

    fig, ov = axes_vides((20, 8.6), (0, 20), (0, 8.6))
    W, G, X0, yb, h = 4.0, 1.2, 0.5, 3.0, 4.3
    titres = [r"$C^{n}$", r"$C^{n+1/3}$", r"$C^{n+2/3}$", r"$C^{n+1}$"]
    noms = ["diffusion", "advection", "réaction"]
    couls = [DIFF, ADV, REAC]
    eqs = [
        r"$C^{n+1/3} = C^{n} - \dfrac{\partial q_x}{\partial x}\,dt$",
        r"$C^{n+2/3} = C^{n+1/3} - V_x\dfrac{\partial C}{\partial x}\,dt$",
        r"$C^{n+1} = C^{n+2/3} - \gamma\, C\, dt$",
    ]
    for k in range(4):
        xa = X0 + k * (W + G)
        a = fig.add_axes([xa / 20, yb / 8.6, W / 20, h / 8.6])
        a.set_xlim(0, Lx)
        a.set_ylim(-0.05, 1.15)
        a.set_xticks([])
        a.set_yticks([])
        for sp in a.spines.values():
            sp.set_color(GRIS_BORD)
        a.fill_between(x, 0, etats[k], color=BLEU_FOND if k == 0 else "#3a2a10")
        if k > 0:
            a.plot(x, etats[k - 1], color=GRIS, lw=1.6, ls="--")
        a.plot(x, etats[k], color=BLEU if k == 0 else ORANGE, lw=2.6)
        ov.text(xa + W / 2, yb + h + 0.35, titres[k], ha="center", va="bottom",
                fontsize=24, color=BLEU if k == 0 else ORANGE)
        if k > 0:
            # flèche + nom du processus dans l'espace entre deux panneaux
            xg = xa - G
            fleche(ov, (xg + 0.1, yb + h / 2), (xa - 0.1, yb + h / 2), color=couls[k - 1],
                   lw=3, ms=20)
            ov.text(xa - G / 2, yb + h / 2 + 0.35, f"{k}", ha="center", va="bottom",
                    fontsize=16, color=couls[k - 1], fontweight="bold")
            ov.text(xa + W / 2, yb - 0.35, noms[k - 1], ha="center", va="top",
                    fontsize=17, color=couls[k - 1], fontweight="bold")
            ov.text(xa + W / 2, yb - 1.35, eqs[k - 1], ha="center", va="center",
                    fontsize=17, color=BLANC)
    ov.text(X0 + W / 2, yb - 0.35, "début du pas n", ha="center", va="top", fontsize=17,
            color=BLEU)
    ov.text(X0 + W / 2, yb - 1.35, "(pointillés : état\nde l'étape précédente)",
            ha="center", va="center", fontsize=13, color=GRIS)
    ov.text(10, 0.35, "Un seul tableau C : chaque étape repart du C que l'étape précédente "
            "vient de modifier   (effets exagérés pour être visibles)", ha="center",
            va="center", fontsize=14, color=GRIS)
    sauver_svg(fig, DOSSIER, DEST["6.3_splitting"])


# ---------------------------------------------------------------------------
# 6.7 Domaine de l'exercice : Q = 1 et son miroir Q = 2
# ---------------------------------------------------------------------------
def panneau_riviere(ax, X0, Q):
    L = 8.4                 # largeur dessinée pour 10 km
    s = L / 10.0            # unités par km
    yb, hb = 4.4, 1.1
    fuite = (0.4, 0.6) if Q == 1 else (9.4, 9.6)
    positif = Q == 1
    col = ROSE if positif else CYAN

    ax.text(X0 + L / 2, 8.6, f"Q = {Q}", ha="center", va="center", fontsize=20,
            color=col, fontweight="bold")
    ax.text(X0 + L / 2, 8.0, "Vx = +7.2 km/h,  fuite 400–600 m" if positif
            else "Vx = −7.2 km/h,  fuite 9400–9600 m", ha="center", va="center",
            fontsize=14, color=col)

    # rivière
    ax.add_patch(Rectangle((X0, yb), L, hb, fc=RIVIERE, alpha=0.3, lw=0))
    ax.plot([X0, X0 + L], [yb, yb], color=RIVIERE, lw=1.5)
    ax.plot([X0, X0 + L], [yb + hb, yb + hb], color=RIVIERE, lw=1.5)
    for k in range(3):
        xa = X0 + (2.2 + 2.2 * k) * s
        if positif:
            fleche(ax, (xa, yb + hb / 2), (xa + 1.1 * s, yb + hb / 2), color=col, lw=2.2,
                   ms=16)
        else:
            fleche(ax, (xa + 1.1 * s, yb + hb / 2), (xa, yb + hb / 2), color=col, lw=2.2,
                   ms=16)
    # fuite (+ condition initiale en profil au-dessus)
    xf0, xf1 = X0 + fuite[0] * s, X0 + fuite[1] * s
    ax.add_patch(Rectangle((xf0, yb), xf1 - xf0, hb, fc=POLLUANT, lw=0))
    ax.plot([xf0, xf0, xf1, xf1], [yb + hb, yb + hb + 1.2, yb + hb + 1.2, yb + hb],
            color=POLLUANT, lw=2)
    xt = xf1 + 0.2 if positif else xf0 - 0.2
    ax.text(xt, yb + hb + 1.0, "C0 = 1000 ppm", ha="left" if positif else "right",
            va="center", fontsize=13, color=POLLUANT, family=MONO)
    ax.text(xt, yb + hb + 0.45, "condition initiale", ha="left" if positif else "right",
            va="center", fontsize=12, color=POLLUANT)
    # axe en km
    for km in range(0, 11, 2):
        ax.plot([X0 + km * s] * 2, [yb - 0.08, yb - 0.2], color=GRIS, lw=1)
        ax.text(X0 + km * s, yb - 0.28, f"{km}", ha="center", va="top", fontsize=11,
                color=GRIS)
    ax.text(X0 + L / 2, yb - 0.72, "x (km)", ha="center", va="top", fontsize=12,
            color=GRIS)

    # bords
    for gauche in (True, False):
        xb = X0 if gauche else X0 + L
        amont = gauche == positif
        ax.plot([xb, xb], [yb - 0.1, yb + hb + 0.1], color=VERT, lw=4)
        ha = "left" if gauche else "right"
        xt = xb - 0.1 if gauche else xb + 0.1
        ax.text(xt, 2.8, "amont" if amont else "aval", ha=ha, va="center",
                fontsize=15, color=VERT, fontweight="bold")
        ax.text(xt, 2.25, "eau propre (Dirichlet)" if amont else "flux nul (Neumann)",
                ha=ha, va="center", fontsize=12, color=VERT)
        eq = r"$C = 0$" if amont else r"$\partial C / \partial x = 0$"
        ax.text(xt, 1.65, eq, ha=ha, va="center", fontsize=17, color=VERT)


# ---------------------------------------------------------------------------
# 6.5 Upwind : du cas par cas au slicing
# ---------------------------------------------------------------------------
def boite(ax, xc, yc, w, h, coul_bord, coul_fond, lw=2.0):
    b = FancyBboxPatch((xc - w / 2, yc - h / 2), w, h,
                       boxstyle="round,pad=0,rounding_size=0.12",
                       ec=coul_bord, fc=coul_fond, lw=lw)
    ax.add_patch(b)
    return b


def panneau_upwind(ax, xc, positif):
    """Un panneau : 5 cellules, les 4 ecarts entre elles, et qui recoit quoi."""
    coul = ROSE if positif else CYAN
    fond = "#3a1430" if positif else "#0e3838"
    s, yc, yd = 1.75, 6.15, 4.25
    x0 = xc - 2 * s

    # titre + sens du vent
    ax.text(xc - 1.3, 7.75, r"si $V_x > 0$" if positif else r"si $V_x < 0$",
            ha="right", va="center", fontsize=23, color=coul, fontweight="bold")
    xf, xf2 = xc - 0.9, xc + 0.6
    p0, p1 = ((xf, 7.75), (xf2, 7.75)) if positif else ((xf2, 7.75), (xf, 7.75))
    fleche(ax, p0, p1, color=coul, lw=2.2, ms=18)
    ax.text(xc + 1.6, 7.75, "le vent va vers la droite" if positif
            else "le vent va vers la gauche", ha="left", va="center",
            fontsize=14, color=GRIS)

    # ligne de cellules C[0] .. C[4]
    for k in range(5):
        actif = (k >= 1) if positif else (k <= 3)
        boite(ax, x0 + k * s, yc, 1.3, 0.8, coul if actif else GRIS_BORD,
              fond if actif else GRIS_FOND)
        ax.text(x0 + k * s, yc, f"C[{k}]", ha="center", va="center", fontsize=16,
                family=MONO, color=BLANC if actif else GRIS)
    # la cellule laissee de cote, c'est le bord
    xb = x0 + (0 if positif else 4) * s
    ax.text(xb, yc + 0.78, "bord", ha="center", va="bottom", fontsize=13, color=GRIS)

    # les nx-1 ecarts, poses entre les cellules
    for k in range(4):
        xd = x0 + (k + 0.5) * s
        boite(ax, xd, yd, 1.55, 0.72, coul, "black", lw=1.6)
        ax.text(xd, yd, f"C[{k+1}]-C[{k}]", ha="center", va="center", fontsize=13,
                family=MONO, color=coul)
        # fleche vers la cellule mise a jour
        cible = x0 + (k + 1 if positif else k) * s
        fleche(ax, (xd, yd + 0.38), (cible, yc - 0.42), color=coul, lw=2.0, ms=16,
               rad=0.0)

    # accolade : taille nx-1
    xg, xdr = x0 + 0.5 * s - 0.8, x0 + 3.5 * s + 0.8
    ax.plot([xg, xdr], [yd - 0.62] * 2, color=GRIS, lw=1.2)
    for x in (xg, xdr):
        ax.plot([x] * 2, [yd - 0.62, yd - 0.48], color=GRIS, lw=1.2)
    ax.text(xc, yd - 0.72, "nx-1 écarts, un par intervalle",
            ha="center", va="top", fontsize=13, color=GRIS)

    # ce que dit l'accolade de la formule
    eq = (r"$-V_x\,\frac{C_i^n - C_{i-1}^n}{dx}$" if positif
          else r"$-V_x\,\frac{C_{i+1}^n - C_i^n}{dx}$")
    ax.text(xc, 2.08, eq, ha="center", va="center", fontsize=25, color=coul)

    # ce que ca donne en python
    code = "C[1:] += dt*dCdt_a" if positif else "C[:-1] += dt*dCdt_a"
    boite(ax, xc, 0.78, 5.6, 0.95, coul, fond, lw=2.0)
    ax.text(xc, 0.78, code, ha="center", va="center", fontsize=19, family=MONO,
            color=BLANC)
    ax.text(xc, 2.95, "chaque écart met à jour la cellule de "
            + ("droite" if positif else "gauche"),
            ha="center", va="center", fontsize=15, color=coul)


def fig_upwind_slicing():
    fig, ax = axes_vides((20, 9.8), (0, 20), (0, 9.8))

    # la ligne de calcul, commune aux deux cas
    boite(ax, 10, 9.1, 13.0, 0.95, GRIS_BORD, GRIS_FOND, lw=1.6)
    ax.text(10, 9.1, "dCdt_a = - Vx * ( C[1:] - C[:-1] ) / dx", ha="center",
            va="center", fontsize=19, family=MONO, color=BLANC)
    ax.text(10, 8.35, "la même ligne dans les deux cas : ce qui change, "
            "c'est la cellule qui reçoit l'écart", ha="center", va="center",
            fontsize=15, color=GRIS)

    panneau_upwind(ax, 5.1, True)
    panneau_upwind(ax, 14.9, False)
    ax.plot([10, 10], [0.2, 8.0], color="#333333", lw=1)

    fig.savefig(os.path.join(DOSSIER, "upwind_slicing_s6.png"), dpi=150,
                bbox_inches="tight", facecolor="black")
    sauver_svg(fig, DOSSIER, DEST["6.5_upwind_slicing"])


def fig_domaine():
    fig, ax = axes_vides((18, 7.4), (0, 19.6), (1.2, 9.1))
    panneau_riviere(ax, 0.6, 1)
    panneau_riviere(ax, 10.6, 2)
    ax.plot([9.8, 9.8], [1.3, 9.0], color="#333333", lw=1)
    ax.text(9.8, 4.95, "miroir", ha="center", va="center", fontsize=12, color=GRIS,
            rotation=90, bbox=dict(fc="black", ec="none"))
    sauver_svg(fig, DOSSIER, DEST["6.7_domaine_riviere"])


def main():
    fig_splitting()
    fig_upwind_slicing()
    fig_domaine()


if __name__ == "__main__":
    main()
