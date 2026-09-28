"""Figures de la séance 1 (fond noir, SVG éditables).

Usage (depuis la racine) : python3 01_cours/fig/figures_s1.py
Écrit les SVG listés dans DEST, dans 01_cours/fig et les dossiers fig voisins.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch, Polygon, Arc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

ICI = os.path.dirname(os.path.abspath(__file__))

# figure -> fichiers SVG écrits (chemins relatifs à ce dossier)
DEST = {
    '1.1_boucle': ['boucle_s1.svg'],
    '1.2_historique': ['historique_s1.svg'],
    '1.4_indexation': ['indexation_s1.svg', '../../01_tutoriel/fig/indexation_s1.svg'],
    '1.5_indentation': ['indentation_s1.svg'],
    '1.9_seiche': ['../../01_tutoriel/fig/seiche_s1.svg'],
}

# Paramètres de l'exercice 1
M_init, M_epargne, duree, interet, depense = 20000, 500, 35, 0.006, 1125


def fleche(ax, p0, p1, color=BLANC, lw=1.8, rad=0.0, ms=16, style="-|>", **kw):
    a = FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={rad}", arrowstyle=style,
                        mutation_scale=ms, lw=lw, color=color, **kw)
    ax.add_patch(a)
    return a


def case(ax, x, y, w, h, texte, etat, fs=14, bold=None, ec=None):
    """Case de vecteur : etat = 'actif' (orange), 'stocke' (bleu), 'vide' (gris),
    'piege' (rouge)."""
    fc, ec, tc = {
        "actif": (ORANGE, ORANGE, "black"),
        "stocke": (BLEU_FOND, BLEU, BLANC),
        "vide": (GRIS_FOND, GRIS_BORD, "#777777"),
        "piege": (ROUGE, ROUGE, "black"),
    }[etat] if ec is None else (lambda t: (t[0], ec, t[2]))({
        "actif": (ORANGE, ORANGE, "black"),
        "stocke": (BLEU_FOND, BLEU, BLANC),
        "vide": (GRIS_FOND, GRIS_BORD, "#777777"),
        "piege": (ROUGE, ROUGE, "black"),
    }[etat])
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.5))
    if bold is None:
        bold = etat in ("actif", "piege")
    ax.text(x + w / 2, y + h / 2, texte, ha="center", va="center", fontsize=fs,
            family=MONO, color=tc, fontweight="bold" if bold else "normal")


def axe_vide(figsize, xlim, ylim):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------------------
# 1.1 La boucle, vue de l'intérieur
# ---------------------------------------------------------------------------
def fig_boucle():
    fig, ax = axe_vide((13, 6.6), (0, 26), (-3.6, 9.6))

    # Bloc INITIALISATION
    ax.add_patch(FancyBboxPatch((0.3, 3.6), 6.2, 3.8, boxstyle="round,pad=0.1,rounding_size=0.3",
                                fc=BLEU_FOND, ec=BLEU, lw=1.8))
    ax.text(3.4, 6.75, "INITIALISATION", ha="center", va="center", fontsize=17,
            color=BLEU, fontweight="bold")
    for k, l in enumerate(["temps = 0", "dt    = 1", "nt    = 1000"]):
        ax.text(1.0, 5.75 - 0.8 * k, l, ha="left", va="center", fontsize=16, family=MONO)
    ax.text(3.4, 2.9, "une seule fois,\navant la boucle", ha="center", va="top", fontsize=14,
            color=GRIS)

    # Anneau MISE À JOUR
    cx, cy, r = 13.2, 5.5, 3.0
    ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=110, theta2=430, color=ORANGE, lw=4))
    # pointe de flèche au bout de l'arc (sens antihoraire)
    t = np.deg2rad(430 - 360)
    tip = (cx + r * np.cos(t), cy + r * np.sin(t))
    t2 = np.deg2rad(430 - 360 - 8)
    fleche(ax, (cx + r * np.cos(t2), cy + r * np.sin(t2)), tip, color=ORANGE, lw=0, ms=30)
    ax.text(cx, cy + 0.75, "MISE À JOUR", ha="center", va="center", fontsize=17,
            color=ORANGE, fontweight="bold")
    ax.text(cx, cy - 0.3, "temps += dt", ha="center", va="center", fontsize=17, family=MONO)
    ax.text(cx, cy + r + 0.35, "for it in range(nt):", ha="center", va="bottom", fontsize=16,
            family=MONO, color=BLANC)
    ax.text(cx, cy - r - 0.3, "tourne nt = 1000 fois", ha="center", va="top", fontsize=14,
            color=ORANGE)

    # Flèches INIT -> anneau -> FIN
    fleche(ax, (6.75, 5.5), (cx - r - 0.2, 5.5), lw=2.2, ms=20)
    ax.add_patch(FancyBboxPatch((21.2, 4.6), 3.6, 1.8, boxstyle="round,pad=0.1,rounding_size=0.3",
                                fc=GRIS_FOND, ec=GRIS, lw=1.8))
    ax.text(23.0, 5.5, "FIN", ha="center", va="center", fontsize=17, fontweight="bold")
    fleche(ax, (cx + r + 0.2, 5.5), (21.0, 5.5), lw=2.2, ms=20)
    ax.text(18.6, 5.8, "après le\n1000e tour", ha="center", va="bottom", fontsize=13, color=GRIS)

    # Frise : valeur de temps après chaque tour
    y = -1.6
    xs = [1.5, 5.0, 8.5, 12.0, 15.5, 19.0, 23.0]
    vals = ["0", "1", "2", "3", "4", None, "1000"]
    ax.plot([0.8, 16.8], [y, y], color=GRIS, lw=1.5)
    ax.plot([21.6, 24.2], [y, y], color=GRIS, lw=1.5)
    ax.text(0.6, y - 0.8, "temps", ha="right", va="center", fontsize=15, family=MONO, color=GRIS)
    ax.text(0.6, y + 1.4, "tour", ha="right", va="center", fontsize=15, color=GRIS)
    for k, (x, v) in enumerate(zip(xs, vals)):
        if v is None:
            ax.text(x, y + 0.15, "…", ha="center", va="center", fontsize=20)
            continue
        col = BLEU if k == 0 else ORANGE
        ax.plot(x, y, "o", color=col, ms=11, zorder=4)
        ax.text(x, y - 0.45, v, ha="center", va="top", fontsize=16, family=MONO, color=col)
    for k in range(4):
        fleche(ax, (xs[k] + 0.15, y + 0.2), (xs[k + 1] - 0.15, y + 0.2), color=ORANGE, lw=1.6,
               rad=-0.5, ms=13)
        ax.text((xs[k] + xs[k + 1]) / 2, y + 1.15, f"it = {k}", ha="center", va="bottom",
                fontsize=14, family=MONO)
        ax.text((xs[k] + xs[k + 1]) / 2, y - 0.45, "+ dt", ha="center", va="top",
                fontsize=13, family=MONO, color=ORANGE)
    fleche(ax, (xs[5] + 1.0, y + 0.2), (xs[6] - 0.15, y + 0.2), color=ORANGE, lw=1.6,
           rad=-0.5, ms=13)
    ax.text((xs[5] + 1.0 + xs[6]) / 2, y + 1.15, "it = 999", ha="center", va="bottom",
            fontsize=14, family=MONO)

    fig.tight_layout()
    sauver_svg(fig, ICI, DEST["1.1_boucle"])


# ---------------------------------------------------------------------------
# 1.2 Une variable s'écrase, un vecteur garde tout
# ---------------------------------------------------------------------------
def fig_variable_vs_vecteur():
    fig, ax = axe_vide((14, 6.4), (-0.3, 29.5), (-2.6, 10.2))
    W, H = 2.3, 1.0
    valeurs = [300, 350, 400, 450]
    labels = ["i = 0", "i = 1", "i = 2", "i = 3"]
    ys = [7.6, 5.4, 3.2, 1.0]

    # colonne gauche : une seule variable
    xg, xo = 8.3, 6.2          # case de la variable, ancienne valeur barrée
    xcg = 5.8                  # centre de la colonne gauche
    ax.text(xcg, 9.75, "une variable", ha="center", va="center", fontsize=18,
            fontweight="bold")
    ax.text(xg + W / 2, 8.8, "fortune", ha="center", va="bottom", fontsize=14, family=MONO,
            color=GRIS)
    # colonne droite : un vecteur
    X0 = 17.4
    ax.text(X0 + 2.5 * W, 9.75, "un vecteur", ha="center", va="center", fontsize=18,
            fontweight="bold")
    for i in range(5):
        ax.text(X0 + i * W + W / 2, 8.8, f"[{i}]", ha="center", va="bottom", fontsize=14,
                family=MONO, color=GRIS)
    ax.text(X0 - 0.3, 8.8, "fortune", ha="right", va="bottom", fontsize=14,
            family=MONO, color=GRIS)
    ax.plot([12.6, 12.6], [0.2, 10.0], color=GRIS_BORD, lw=1.2)

    for k, (v, lab, y) in enumerate(zip(valeurs, labels, ys)):
        ax.text(0.0, y + H / 2, lab, ha="left", va="center", fontsize=15, family=MONO)
        # variable : ancienne valeur barrée, puis nouvelle valeur
        case(ax, xg, y, W, H, f"{v}", "actif", fs=15)
        if k >= 1:
            ax.text(xo, y + H / 2, f"{valeurs[k - 1]}", ha="center", va="center", fontsize=14,
                    family=MONO, color=GRIS)
            ax.plot([xo - 0.85, xo + 0.85], [y + H / 2 - 0.08, y + H / 2 + 0.08], color=ROUGE,
                    lw=2.4)
            fleche(ax, (xo + 0.95, y + H / 2), (xg - 0.1, y + H / 2), color=GRIS, lw=1.2, ms=11)
        # vecteur : historique
        for i in range(5):
            etat = "actif" if i == k else ("stocke" if i < k else "vide")
            case(ax, X0 + i * W, y, W, H, f"{valeurs[i]}" if i <= k else "0", etat, fs=14)
        if k >= 1:
            fleche(ax, (X0 + (k - 1) * W + W / 2, y + H), (X0 + k * W + W / 2, y + H),
                   color=ORANGE, lw=1.6, rad=-0.45, ms=14)
    ax.text(xo, ys[1] + H + 0.15, "écrasée", ha="center", va="bottom", fontsize=13,
            color=ROUGE)

    ax.text(xcg, -0.8, "ne garde que la dernière valeur", ha="center", va="center",
            fontsize=16, color=ORANGE)
    ax.text(X0 + 2.5 * W, -0.8, "garde tout l'historique", ha="center", va="center",
            fontsize=16, color=BLEU)
    ax.text(xcg, -1.9, "fortune = fortune + 50", ha="center",
            va="center", fontsize=15, family=MONO, color=GRIS)
    ax.text(X0 + 2.5 * W, -1.9, "fortune[i] = fortune[i-1] + 50", ha="center",
            va="center", fontsize=15, family=MONO, color=GRIS)

    fig.tight_layout()
    sauver_svg(fig, ICI, DEST["1.2_historique"])


# ---------------------------------------------------------------------------
# 1.4 Indexation en boîtes
# ---------------------------------------------------------------------------
def fig_indexation():
    fig, ax = axe_vide((13, 5.2), (-3.2, 18.6), (-3.6, 5.1))
    colors = ["red", "green", "blue", "yellow", "white", "black"]
    teinte = {"red": ("#d94a4a", BLANC), "green": ("#3f9e4d", BLANC),
              "blue": ("#3e6fd1", BLANC), "yellow": ("#f0cf45", "black"),
              "white": ("#f2f2f2", "black"), "black": ("#000000", BLANC)}
    W, H, X0 = 2.5, 1.5, 2.4

    ax.text(-3.0, 4.35, "colors = ['red', 'green', 'blue', 'yellow', 'white', 'black']",
            ha="left", va="center", fontsize=16, family=MONO)
    for i, c in enumerate(colors):
        fc, tc = teinte[c]
        ax.add_patch(Rectangle((X0 + i * W, 0), W, H, fc=fc, ec=GRIS, lw=1.8))
        ax.text(X0 + i * W + W / 2, H / 2, f"'{c}'", ha="center", va="center", fontsize=15,
                family=MONO, color=tc)
        ax.text(X0 + i * W + W / 2, H + 0.35, f"{i}", ha="center", va="bottom", fontsize=20,
                family=MONO, color=BLEU, fontweight="bold" if i == 0 else "normal")
        ax.text(X0 + i * W + W / 2, -0.35, f"{i - 6}", ha="center", va="top", fontsize=20,
                family=MONO, color=ORANGE)
    ax.text(X0 - 0.4, H + 0.65, "indice positif", ha="right", va="center", fontsize=15,
            color=BLEU)
    ax.text(X0 - 0.4, -0.65, "indice négatif", ha="right", va="center", fontsize=15,
            color=ORANGE)
    ax.text(X0 + 6 * W + 0.4, H + 0.65, "depuis le début →", ha="left", va="center",
            fontsize=13, color=BLEU)
    ax.text(X0 + 6 * W + 0.4, -0.65, "← depuis la fin", ha="left", va="center",
            fontsize=13, color=ORANGE)

    ax.text(X0 + 3 * W, -2.6, "Python compte à partir de 0 !", ha="center", va="center",
            fontsize=18, fontweight="bold")
    fig.tight_layout()
    sauver_svg(fig, ICI, DEST["1.4_indexation"])


# ---------------------------------------------------------------------------
# 1.5 Indentation en bandes colorées
# ---------------------------------------------------------------------------
def fig_indentation():
    lignes = [
        ("for i in range(10):", "for"),
        ("    print(i)", "for"),
        ("", None),
        ("if i == 0:", "if"),
        ('    print("i est égal à zéro")', "if"),
        ("", None),
        ("i = 0", None),
        ("while i < 10:", "while"),
        ("    print(i)", "while"),
        ("    i += 1", "while"),
    ]
    couleurs = {"for": (BLEU, BLEU_FOND), "if": (VERT, "#1e3d22"), "while": (ORANGE, "#4a3515")}
    etiq = {"for": "dans la boucle for", "if": "dans le if", "while": "dans le while"}
    fs = 20
    # position verticale de chaque ligne (les lignes vides sont plus courtes)
    ys, y = [], 0.0
    for l, _ in lignes:
        ys.append(y)
        y += 1.0 if l else 0.45
    fig = plt.figure(figsize=(14, 6.4))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.axis("off")
    ax.set_ylim(ys[-1] + 1.9, -0.8)
    ax.set_xlim(-1, 60)
    # largeur d'un caractère mono, mesurée sur le rendu
    t = ax.text(0, 0, "x" * 40, fontsize=fs, family=MONO)
    fig.canvas.draw()
    bb = t.get_window_extent().transformed(ax.transData.inverted())
    cw = bb.width / 40
    t.remove()
    ind = 4 * cw
    larg = 31 * cw

    blocs = {}
    for n, (l, bloc) in enumerate(lignes):
        if bloc and l.startswith("    "):
            blocs.setdefault(bloc, []).append(ys[n])
    for bloc, yb in blocs.items():
        c, fond = couleurs[bloc]
        y0, y1 = min(yb) - 0.45, max(yb) + 0.45
        ax.add_patch(Rectangle((ind - 0.6 * cw, y0), larg - ind + 0.3 * cw, y1 - y0, fc=fond, ec="none"))
        ax.add_patch(Rectangle((ind - 0.6 * cw, y0), 0.25 * cw, y1 - y0, fc=c, ec="none"))
        # accolade + étiquette
        xb = larg + 1.0
        ax.plot([xb, xb + 0.6, xb + 0.6, xb], [y0 + 0.05, y0 + 0.05, y1 - 0.05, y1 - 0.05],
                color=c, lw=2)
        ax.plot([xb + 0.6, xb + 1.3], [(y0 + y1) / 2] * 2, color=c, lw=2)
        ax.text(xb + 1.8, (y0 + y1) / 2, etiq[bloc], ha="left", va="center", fontsize=18,
                color=c)

    for n, (l, bloc) in enumerate(lignes):
        ax.text(0, ys[n], l, ha="left", va="center", fontsize=fs, family=MONO)
        if l.endswith(":"):
            k = len(l) - 1
            ax.add_patch(FancyBboxPatch((k * cw + 0.12 * cw, ys[n] - 0.33), 0.76 * cw, 0.66,
                                        boxstyle="round,pad=0.05,rounding_size=0.1",
                                        fc="none", ec=ROUGE, lw=2))
            ax.text(k * cw, ys[n], ":", ha="left", va="center", fontsize=fs,
                    family=MONO, color=ROUGE, fontweight="bold")

    # « 4 espaces »
    ax.annotate("", xy=(ind, ys[1] + 0.62), xytext=(0, ys[1] + 0.62),
                arrowprops=dict(arrowstyle="<|-|>", color=GRIS, lw=1.3, mutation_scale=12,
                                shrinkA=0, shrinkB=0))
    ax.text(ind / 2, ys[1] + 0.72, "4 espaces", ha="center", va="top", fontsize=12,
            color=GRIS)

    # légende des deux points
    yl = ys[-1] + 1.3
    ax.text(0, yl, ":", ha="left", va="center", fontsize=fs, family=MONO, color=ROUGE,
            fontweight="bold")
    ax.add_patch(FancyBboxPatch((0.12 * cw, yl - 0.33), 0.76 * cw, 0.66,
                                boxstyle="round,pad=0.05,rounding_size=0.1",
                                fc="none", ec=ROUGE, lw=2))
    ax.text(1.6 * cw, yl, "ouvre un bloc : toutes les lignes indentées qui suivent en font partie",
            ha="left", va="center", fontsize=16, color=ROUGE)
    sauver_svg(fig, ICI, DEST["1.5_indentation"])


# ---------------------------------------------------------------------------
# 1.9 La seiche du Léman
# ---------------------------------------------------------------------------
def fig_seiche():
    L_km, H_m = 72.0, 154.0
    xs = np.linspace(0, L_km, 400)
    u = 2 * xs / L_km - 1
    terre = 0.45                              # niveau des berges
    fond = -1.0 + (1.0 + terre) * u ** 12     # fond schématique (profondeur exagérée)
    amp = 0.32
    ybas, yhaut = -1.75, 2.3

    fig, axs = plt.subplots(1, 2, figsize=(15, 6.2), gridspec_kw=dict(wspace=0.06))

    def coupe(ax, surf, titre):
        ax.set_xlim(-8, L_km + 8)
        ax.set_ylim(ybas, yhaut)
        ax.axis("off")
        ax.fill_between(xs, fond, surf, where=surf > fond, color=BLEU_FOND, lw=0,
                        interpolate=True)
        ok = surf > fond
        ax.plot(xs[ok], surf[ok], color=BLEU, lw=2.8)
        # terrain : sous le lac et berges
        brun = "#2e2721"
        ax.fill_between(xs, fond, ybas, color=brun, lw=1, ec=brun)
        for x0, x1 in [(-8, 0.2), (L_km - 0.2, L_km + 8)]:
            ax.fill_between([x0, x1], [terre] * 2, ybas, color=brun, lw=1, ec=brun)
            ax.plot([x0 if x0 < 0 else L_km, 0 if x0 < 0 else x1],
                    [terre] * 2, color=GRIS, lw=2)
        ax.plot(xs, fond, color=GRIS, lw=2)
        ax.plot([0, L_km], [0, 0], color=BLANC, lw=1.2, ls="--", alpha=0.6)
        ax.text(-4, terre + 0.08, "Genève\n(ouest)", ha="center", va="bottom", fontsize=14)
        ax.text(L_km + 4, terre + 0.08, "Villeneuve\n(est)", ha="center", va="bottom",
                fontsize=14)
        ax.text(-7.5, yhaut, titre, ha="left", va="top", fontsize=17, fontweight="bold")

    # (a) vent : surface inclinée vers Villeneuve
    a = axs[0]
    surf = -amp * np.cos(np.pi * xs / L_km)
    coupe(a, surf, "(a) le vent pousse l'eau vers Villeneuve")
    for yv in (1.55, 1.1):
        for xv in (10, 31, 52):
            fleche(a, (xv, yv), (xv + 11, yv), color=BLANC, lw=2, ms=16)
    a.text(L_km / 2 + 2, 1.72, "vent", ha="center", va="bottom", fontsize=15)
    a.annotate("", xy=(L_km - 4, amp), xytext=(L_km - 4, 0),
               arrowprops=dict(arrowstyle="<|-|>", color=ORANGE, lw=2, mutation_scale=14,
                               shrinkA=0, shrinkB=0))
    a.text(L_km - 5.5, amp / 2 + 0.03, r"$\eta$", ha="right", va="center", fontsize=26,
           color=ORANGE)
    xh = 0.6 * L_km
    a.annotate("", xy=(xh, -1.0), xytext=(xh, 0),
               arrowprops=dict(arrowstyle="<|-|>", color=GRIS, lw=1.3, mutation_scale=12,
                               shrinkA=0, shrinkB=0))
    a.text(xh + 1.5, -0.55, "H = 154 m", ha="left", va="center", fontsize=14, color=GRIS)
    a.annotate("", xy=(L_km, -1.3), xytext=(0, -1.3),
               arrowprops=dict(arrowstyle="<|-|>", color=GRIS, lw=1.3, mutation_scale=12,
                               shrinkA=0, shrinkB=0))
    a.text(L_km / 2, -1.4, "L = 72 km", ha="center", va="top", fontsize=14, color=GRIS)

    # (b) vent tombé : la surface bascule
    b = axs[1]
    coupe(b, -amp * np.cos(np.pi * xs / L_km), "(b) le vent tombe : l'eau oscille")
    b.plot(xs, amp * np.cos(np.pi * xs / L_km), color=BLEU, lw=1.8, ls=":")
    fleche(b, (L_km - 4, amp + 0.02), (L_km - 4, -amp + 0.02), color=ORANGE, lw=2.2, ms=17)
    fleche(b, (4, -amp - 0.02), (4, amp - 0.02), color=ORANGE, lw=2.2, ms=17)
    b.plot(L_km / 2, 0, "o", color=BLANC, ms=6, zorder=5)
    b.text(L_km / 2, -0.3, "nœud", ha="center", va="top", fontsize=13, color=GRIS)
    b.text(L_km / 2, -1.4, "échelle verticale très exagérée", ha="center", va="top",
           fontsize=12, color=GRIS)

    # encart eta(t), avec les paramètres du tutoriel
    ins = b.inset_axes([0.2, 0.67, 0.62, 0.22])
    g, eta0, tau = 9.81, 0.10, 12 * 3600.0
    omega = np.pi * np.sqrt(g * H_m) / (L_km * 1000)
    t = np.linspace(0, 3 * 3600, 600)
    eta = eta0 * np.exp(-t / tau) * np.cos(omega * t)
    ins.plot(t / 60, eta * 100, color=ORANGE, lw=2)
    ins.plot(t / 60, eta0 * 100 * np.exp(-t / tau), color=GRIS, lw=1, ls="--")
    ins.axhline(0, color=GRIS_BORD, lw=0.8)
    ins.set_xlim(0, 180)
    ins.set_ylim(-12, 12)
    ins.set_xticks([0, 60, 120, 180])
    ins.set_yticks([-10, 0, 10])
    ins.tick_params(labelsize=12)
    ins.set_xlabel("temps [min]", fontsize=13, labelpad=1)
    ins.set_ylabel(r"$\eta$ [cm]", fontsize=15, color=ORANGE, labelpad=2)
    ins.set_title("dénivelé à Villeneuve (modèle du tutoriel)", fontsize=13, color=GRIS, pad=4)
    ins.set_facecolor("black")
    for sp in ("top", "right"):
        ins.spines[sp].set_visible(False)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.98, bottom=0.02)
    sauver_svg(fig, ICI, DEST["1.9_seiche"])


if __name__ == "__main__":
    fig_boucle()
    fig_variable_vs_vecteur()
    fig_indexation()
    fig_indentation()
    fig_seiche()
