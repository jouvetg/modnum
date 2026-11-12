"""Séquence « coder pas à pas » (séance 7) : 8 figures de même taille.

À gauche le code qui se remplit (orange = lignes ajoutées à cette étape, rouge barré =
lignes retirées), à droite ce que donne le run de cette étape (figure + console).
Le code de chaque étape est réellement exécuté : le résultat affiché est le vrai.

Usage (depuis la racine) : python3 07_cours/fig/pas_a_pas_s7.py
Écrit 07_cours/fig/pas_a_pas_1_s7.svg ... pas_a_pas_8_s7.svg
"""

import contextlib
import io
import os
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from pygments.lexers import PythonLexer
from pygments.token import Keyword, Name, Number, String, Comment, Operator

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'utils'))
from style_figures import *  # noqa: E402,F401,F403

DOSSIER = os.path.dirname(os.path.abspath(__file__))
N = 8
TITRES = [
    "Paramètres et grille",
    "Temps, pas de temps, boucle",
    "Champ initial + figure",
    "Diffusion",
    "Advection",
    "Pas de temps stable",
    "Condition (flag)",
    "Affichage dans la boucle",
]
VERIF = [
    "dx a la bonne valeur ?",
    "la boucle va bien jusqu'à la durée ?",
    "la tache est au bon endroit ?",
    "la tache s'étale ?",
    "le calcul explose : dt trop grand !",
    "la tache avance de V × durée = 6 ?",
    "la date d'arrivée est plausible ?",
    "on suit la tache en direct",
]
ECHEC = {5}   # étapes dont le run révèle un problème

# Exemple fictif : une tache de colorant transportée et étalée dans un canal.
# (texte, première étape, dernière étape)
INF = N
CODE = [
    ("import numpy as np", 1, INF),
    ("import matplotlib.pyplot as plt", 1, INF),
    ("from IPython.display import display, clear_output", 8, INF),
    ("", 1, INF),
    ("D, V, L   = 0.01, 1.0, 10.0   # diffusion, vitesse, longueur", 1, INF),
    ("nx, duree = 201, 6.0          # nombre de nœuds, durée", 1, INF),
    ("x0, w     = 2.0, 0.3          # centre et largeur de la tache", 3, INF),
    ("x_st, seuil = 7.0, 0.1        # station, seuil de détection", 7, INF),
    ("freq_affich = 25              # fréquence d'affichage", 8, INF),
    ("x  = np.linspace(0, L, nx)    # grille", 1, INF),
    ("dx = x[1] - x[0]", 1, INF),
    ("print('dx =', dx)", 1, 1),
    ("dt = duree / 60               # provisoire", 2, 5),
    ("dt = min(dx**2/(2.1*D), dx/(2.1*V))   # stabilité", 6, INF),
    ("nt = int(duree / dt)          # nombre de pas de temps", 2, INF),
    ("C = np.exp(-((x - x0) / w)**2)        # tache initiale", 3, INF),
    ("fig, ax = plt.subplots()", 3, INF),
    ("i_st, flag = int(x_st / dx), 0        # indice de la station", 7, INF),
    ("temps = 0.0", 2, INF),
    ("for it in range(nt):", 2, INF),
    ("    temps += dt", 2, INF),
    ("    q = -D * (C[1:] - C[:-1]) / dx            # flux diffusif", 4, INF),
    ("    C[1:-1] -= dt * (q[1:] - q[:-1]) / dx     # diffusion", 4, INF),
    ("    C[1:] -= dt * V * (C[1:] - C[:-1]) / dx   # advection (upwind)", 5, INF),
    ("    if C[i_st] > seuil and flag == 0:         # 1re arrivée", 7, INF),
    ("        t_arr, flag = temps, 1", 7, INF),
    ("    if it % freq_affich == 0:", 8, INF),
    ("        clear_output(wait=True); ax.cla()", 8, INF),
    ("        ax.plot(x, C); ax.set_title(f't = {temps:.1f}')", 8, INF),
    ("        display(fig)", 8, INF),
    ("print('temps final =', round(temps, 2))", 2, 6),
    ("print('arrivée à la station : t =', round(t_arr, 2))", 7, INF),
    ("ax.plot(x, C)", 3, 7),
]


# coloration syntaxique (couleurs proches d'un thème sombre d'éditeur)
COUL = [(Comment, "#8a8a8a"), (String, "#a5e075"), (Number, "#c59bff"),
        (Keyword, "#ff79c6"), (Name.Builtin, "#8be9fd"), (Operator, "#ff79c6")]
LEXER = PythonLexer()
FS, CW = 13, 13 * 0.6 / 72   # taille de police et largeur d'un caractère (pouces) en monospace


def couleur(tok):
    for t, c in COUL:
        if tok in t:
            return c
    return "#e6e6e6"


def ecrire_ligne(ax, x0, y, txt):
    """Écrit une ligne de code, colorée token par token (police à chasse fixe)."""
    col = 0
    for tok, val in LEXER.get_tokens(txt):
        val = val.rstrip("\n")
        if val.strip():
            ax.text(x0 + col * CW, y, val, fontsize=FS, family=MONO, color=couleur(tok),
                    va="center", style="italic" if tok in Comment else "normal")
        col += len(val)


def lignes(k):
    """Lignes visibles à l'étape k : (texte, statut) avec statut 'ancien', 'nouveau', 'retire'."""
    out = []
    for txt, a, b in CODE:
        if a <= k <= b:
            out.append((txt, "nouveau" if a == k and k > 1 else "ancien"))
        elif b == k - 1:
            out.append((txt, "retire"))
    return out


def code_etape(k):
    return "\n".join(t for t, a, b in CODE if a <= k <= b)


class Ax:
    """Remplace l'axe matplotlib : enregistre ce que le code demande de tracer."""

    def __init__(self):
        self.courbes, self.historique, self.titre, self.xl, self.yl = [], [], "", "", ""

    def plot(self, x, y, *a, **k):
        self.courbes.append((np.array(x, float), np.array(y, float)))

    def cla(self):
        if self.courbes:
            self.historique.append(self.courbes)
        self.courbes = []

    def set_title(self, t):
        self.titre = t

    def set_xlabel(self, t):
        self.xl = t

    def set_ylabel(self, t):
        self.yl = t


def executer(k):
    ax = Ax()
    fake_plt = type("P", (), {"subplots": staticmethod(lambda *a, **kw: (None, ax))})
    ns = {"__name__": "__etape__"}
    src = code_etape(k).replace("import matplotlib.pyplot as plt", "plt = __plt")
    src = src.replace("from IPython.display import display, clear_output",
                      "display = clear_output = lambda *a, **kw: None")
    ns["__plt"] = fake_plt
    sortie = io.StringIO()
    with contextlib.redirect_stdout(sortie), np.errstate(all="ignore"):
        exec(src, ns)
    return ax, sortie.getvalue().rstrip("\n").splitlines(), ns


def figure(k):
    ax_rec, console, ns = executer(k)
    W, H = 16, 9
    fig = plt.figure(figsize=(W, H))
    fond = fig.add_axes([0, 0, 1, 1])
    fond.set_xlim(0, W)
    fond.set_ylim(0, H)
    fond.axis("off")

    # --- bandeau : étape k/N + progression ---
    fond.text(0.45, 8.45, f"Étape {k}/{N}", fontsize=24, color=ORANGE, weight="bold", va="center")
    fond.text(2.75, 8.45, TITRES[k - 1], fontsize=24, color=BLANC, va="center")
    for i in range(N):
        c = ORANGE if i + 1 == k else (GRIS if i + 1 < k else GRIS_FOND)
        fond.add_patch(Rectangle((10.6 + i * 0.62, 8.3), 0.5, 0.3, color=c, ec=GRIS_BORD, lw=1))

    # --- code (gauche) ---
    fond.add_patch(FancyBboxPatch((0.3, 0.3), 9.0, 7.6, boxstyle="round,pad=0,rounding_size=0.12",
                                  fc=GRIS_FOND, ec=GRIS_BORD, lw=1.2))
    y, dy = 7.62, 0.226
    for txt, st in lignes(k):
        if st == "nouveau":
            fond.add_patch(Rectangle((0.32, y - dy / 2), 8.96, dy, color=ORANGE, alpha=0.22, lw=0))
            fond.add_patch(Rectangle((0.32, y - dy / 2), 0.07, dy, color=ORANGE, lw=0))
            fond.text(0.45, y, "+", fontsize=FS, family=MONO, color=ORANGE, va="center", weight="bold")
            ecrire_ligne(fond, 0.7, y, txt)
        elif st == "retire":
            fond.text(0.45, y, "−", fontsize=FS, family=MONO, color=ROUGE, va="center")
            fond.text(0.7, y, txt, fontsize=FS, family=MONO, color=ROUGE, va="center")
            fond.plot([0.7, 0.7 + max(len(txt), 1) * CW], [y, y], color=ROUGE, lw=1.2)
        else:
            ecrire_ligne(fond, 0.7, y, txt)
        y -= dy

    # --- run (droite) ---
    ok = k not in ECHEC
    fond.add_patch(FancyBboxPatch((9.6, 7.35), 6.1, 0.55, boxstyle="round,pad=0,rounding_size=0.1",
                                  fc=VERT if ok else ROUGE, ec="none"))
    fond.text(9.8, 7.62, "▶ Run", fontsize=16, color="black", weight="bold", va="center")
    fond.text(11.15, 7.62, ("✓ " if ok else "✗ ") + VERIF[k - 1], fontsize=12.5, color="black",
              va="center")

    # figure
    axr = fig.add_axes([9.6 / W + 0.035, 2.75 / H, 5.55 / W, 4.2 / H])
    axr.set_facecolor("black")
    for s in axr.spines.values():
        s.set_color(GRIS)
    if not ax_rec.courbes and not ax_rec.historique:
        axr.set_xticks([])
        axr.set_yticks([])
        axr.text(0.5, 0.5, "pas encore de figure", transform=axr.transAxes, ha="center",
                 va="center", color=GRIS, fontsize=14, style="italic")
    else:
        hist = ax_rec.historique
        for i, courbes in enumerate(hist):
            for xx, yy in courbes:
                axr.plot(xx, yy, color=BLEU, lw=1.2, alpha=0.25 + 0.5 * i / max(len(hist), 1))
        nan = False
        for xx, yy in ax_rec.courbes:
            if not np.all(np.isfinite(yy)):
                nan = True
                yy = np.where(np.isfinite(yy), yy, np.nan)
            axr.plot(xx, yy, color=BLANC, lw=2)
        axr.set_xlim(0, 10)
        if nan:
            axr.set_ylim(-1, 1)
            axr.text(0.5, 0.5, "C contient des nan :\nle schéma explose", transform=axr.transAxes,
                     ha="center", va="center", color=ROUGE, fontsize=16, weight="bold")
        axr.set_xlabel(ax_rec.xl, fontsize=12)
        axr.set_ylabel(ax_rec.yl, fontsize=12)
        axr.set_title(ax_rec.titre, fontsize=13, color=BLANC)
        axr.tick_params(labelsize=10)

    # console
    fond.add_patch(FancyBboxPatch((9.6, 0.3), 6.1, 1.45, boxstyle="round,pad=0,rounding_size=0.1",
                                  fc="#0b0b0b", ec=GRIS_BORD, lw=1.2))
    fond.text(9.75, 1.55, "console", fontsize=10, color=GRIS, va="center", style="italic")
    if not console:
        console = ["(aucune sortie)"]
    yc = 1.2
    for l in console[-3:]:
        fond.text(9.8, yc, l, fontsize=12, family=MONO, va="center",
                  color=GRIS if l == "(aucune sortie)" else VERT)
        yc -= 0.32

    sauver(fig, f"pas_a_pas_{k}_s7.svg")
    return ns


def sauver(fig, nom):
    """Comme sauver_svg, mais SANS bbox 'tight' : toutes les figures gardent exactement
    la même taille (16 x 9), pour que rien ne bouge d'une slide à l'autre."""
    chemin = os.path.join(DOSSIER, nom)
    fig.savefig(chemin, facecolor="black")
    if os.environ.get("APERCU"):
        fig.savefig(os.path.join(os.environ["APERCU"], nom.replace(".svg", ".png")), dpi=60,
                    facecolor="black")
    with open(chemin, encoding="utf-8") as f:
        svg = f.read()
    svg = svg.replace('<text style="', '<text xml:space="preserve" style="white-space: pre; ')
    svg = svg.replace("'DejaVu Sans Mono'", "'DejaVu Sans Mono', monospace")
    svg = svg.replace("'DejaVu Sans';", "'DejaVu Sans', sans-serif;")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(svg)
    print("écrit", os.path.relpath(chemin))
    plt.close(fig)


def main():
    for k in range(1, N + 1):
        figure(k)


if __name__ == "__main__":
    main()
