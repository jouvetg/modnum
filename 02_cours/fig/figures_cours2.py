"""Figures du cours 2 (fond noir), exportées en SVG et PNG.

Usage (depuis ce dossier) : python figures_cours2.py
"""

import numpy as np
import matplotlib.pyplot as plt

BLEU = "#6cc3ff"
ORANGE = "#ffb454"
VERT = "#8be28b"
GRIS = "#9a9a9a"
BLANC = "#ffffff"

plt.rcParams.update({
    "figure.facecolor": "black",
    "axes.facecolor": "black",
    "savefig.facecolor": "black",
    "text.color": BLANC,
    "axes.labelcolor": BLANC,
    "xtick.color": GRIS,
    "ytick.color": GRIS,
    "font.family": "DejaVu Sans",
    "font.size": 17,
    "mathtext.fontset": "cm",
})


def axes_fleches(ax, xlabel=None, ylabel=None):
    """Axes minimalistes : deux flèches partant de l'origine."""
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    kw = dict(arrowstyle="-|>", color=GRIS, lw=1.8, mutation_scale=18)
    ax.annotate("", xy=(x1, y0), xytext=(x0, y0), arrowprops=kw, annotation_clip=False)
    ax.annotate("", xy=(x0, y1), xytext=(x0, y0), arrowprops=kw, annotation_clip=False)
    if xlabel:
        ax.text(x1, y0 - 0.04 * (y1 - y0), xlabel, ha="right", va="top", fontsize=22)
    if ylabel:
        ax.text(x0 + 0.02 * (x1 - x0), y1, ylabel, ha="left", va="top", fontsize=22)


def sauver(fig, nom):
    fig.savefig(f"{nom}.svg")
    fig.savefig(f"{nom}.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 1. Définition de la dérivée : sécantes -> tangente quand dt -> 0
# ---------------------------------------------------------------------------
def fig_derivee():
    f = lambda t: 2.4 * t - 0.36 * t**2
    df = lambda t: 2.4 - 0.72 * t
    t0, dt = 1.2, 2.2

    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.set_xlim(0, 7.2)
    ax.set_ylim(0, 5.6)

    tt = np.linspace(0, 6.4, 300)
    ax.plot(tt, f(tt), color=BLANC, lw=3, zorder=3)
    ax.text(6.45, f(6.4), r"$x(t)$", fontsize=24, va="center")

    # Sécantes de plus en plus proches de la tangente
    ts = np.linspace(-0.2, 4.6, 2)
    for h, a in [(1.4, 0.45), (0.7, 0.3)]:
        p = (f(t0 + h) - f(t0)) / h
        ax.plot(ts, f(t0) + p * (ts - t0), color=ORANGE, lw=1.5, alpha=a, zorder=2)
    p = (f(t0 + dt) - f(t0)) / dt
    ax.plot(ts, f(t0) + p * (ts - t0), color=ORANGE, lw=2.5, zorder=2)

    # Tangente
    tg = np.linspace(0.1, 3.1, 2)
    ax.plot(tg, f(t0) + df(t0) * (tg - t0), color=BLEU, lw=3, zorder=2)

    # Points et repères sur l'axe
    for t, lab in [(t0, r"$t$"), (t0 + dt, r"$t+dt$")]:
        ax.plot([t, t], [0, f(t)], ls=":", color=GRIS, lw=1.5)
        ax.plot(t, f(t), "o", color=BLANC, ms=9, zorder=4)
        ax.text(t, -0.12, lab, ha="center", va="top", fontsize=24)
    ax.text(t0 + 0.1, f(t0) - 0.2, r"$x(t)$", fontsize=22, ha="left", va="top")
    ax.text(t0 + dt + 0.1, f(t0 + dt) + 0.1, r"$x(t+dt)$", fontsize=22, ha="left", va="bottom")

    # Accroissements dt et x(t+dt) - x(t)
    ax.plot([t0, t0 + dt], [f(t0)] * 2, ls="--", color=ORANGE, lw=1.5)
    ax.plot([t0 + dt] * 2, [f(t0), f(t0 + dt)], ls="--", color=ORANGE, lw=1.5)
    ax.text(t0 + dt / 2, f(t0) - 0.12, r"$dt$", color=ORANGE, ha="center", va="top", fontsize=22)
    ax.text(t0 + dt + 0.1, f(t0) + 0.45, r"$x(t+dt)-x(t)$",
            color=ORANGE, ha="left", va="center", fontsize=20)

    # dt -> 0
    ax.annotate("", xy=(3.2, f(t0) + df(t0) * 2.0), xytext=(4.3, f(t0) + p * 3.1),
                arrowprops=dict(arrowstyle="-|>", color=BLANC, lw=1.5,
                                connectionstyle="arc3,rad=0.3", mutation_scale=16))
    ax.text(4.25, 5.1, r"$dt \to 0$", fontsize=24, ha="left")

    # Légende
    ax.text(0.25, 5.2, "sécante, pente", color=ORANGE, fontsize=17, ha="left")
    ax.text(0.25, 4.45, r"$\dfrac{x(t+dt)-x(t)}{dt}$", color=ORANGE, fontsize=22, ha="left")
    ax.text(0.25, 3.55, "tangente, pente", color=BLEU, fontsize=17, ha="left")
    ax.text(0.25, 2.85, r"$\dfrac{dx(t)}{dt}$", color=BLEU, fontsize=24, ha="left")

    axes_fleches(ax)
    fig.tight_layout()
    sauver(fig, "def_derivees")


# ---------------------------------------------------------------------------
# 2. Genève -> Saint-Gall : position x(t) et vitesse dx/dt
# ---------------------------------------------------------------------------
def boite_lisse(t, a, b, w=0.06):
    """Vaut ~1 sur [a, b], ~0 ailleurs, avec des bords lisses."""
    return 0.5 * (np.tanh((t - a) / w) - np.tanh((t - b) / w))


def fig_trajet():
    t = np.linspace(0, 4.2, 3000)
    v = 115 * boite_lisse(t, 0.15, 4.05, 0.05)
    villes = [("Lausanne", 0.62, 45, 0.05), ("Berne", 1.55, 60, 0.07),
              ("Zurich", 2.75, 115, 0.13), ("Saint-Gall", 4.18, 0, 0)]
    for _, tc, dv, w in villes[:-1]:
        v -= dv * boite_lisse(t, tc - w, tc + w, 0.05)
    v += 10 * np.sin(2 * np.pi * t / 0.45) * boite_lisse(t, 0.8, 1.35) \
        + 12 * np.sin(2 * np.pi * t / 0.5) * boite_lisse(t, 3.0, 3.8)
    v = np.maximum(v, 0)
    x = np.concatenate([[0], np.cumsum(0.5 * (v[1:] + v[:-1]) * np.diff(t))])

    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 6.2), sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.25, 1], hspace=0.12))

    a1.plot(t, x, color=BLEU, lw=3)
    a2.plot(t, v, color=ORANGE, lw=3)

    points = [("Genève", 0.0)] + [(n, tc) for n, tc, _, _ in villes]
    for nom, tc in points:
        xc = np.interp(tc, t, x)
        for a in (a1, a2):
            a.axvline(tc, color=GRIS, ls="--", lw=1, alpha=0.7)
        a1.plot(tc, xc, "s", color=BLANC, ms=9, zorder=4)
        a1.text(tc - 0.06, xc + 12, nom, ha="right", va="bottom", fontsize=16)

    # Arrêt à Zurich : x constant <-> v = 0
    tz = 2.75
    a2.annotate("arrêt : $v=0$", xy=(tz, 3), xytext=(tz + 0.35, 25), fontsize=15,
                arrowprops=dict(arrowstyle="-|>", color=BLANC, lw=1.2))
    a1.annotate("$x$ constant", xy=(tz, np.interp(tz, t, x)), xytext=(tz + 0.3, 170),
                fontsize=15, arrowprops=dict(arrowstyle="-|>", color=BLANC, lw=1.2))

    a1.set_ylabel("position $x(t)$\n[km]", fontsize=17)
    a2.set_ylabel(r"vitesse $\dfrac{dx(t)}{dt}$" + "\n[km/h]", fontsize=17)
    a2.set_xlabel("temps $t$ [h]", fontsize=17)
    a1.set_ylim(-10, 470)
    a2.set_ylim(0, 150)
    a2.set_yticks([0, 50, 100])
    a1.set_yticks([0, 100, 200, 300, 400])
    for a in (a1, a2):
        a.set_xlim(-0.45, 4.3)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            a.spines[s].set_color(GRIS)
        a.tick_params(labelsize=14)
    fig.subplots_adjust(left=0.14, right=0.98, top=0.97, bottom=0.12)
    sauver(fig, "geneve-zurich")


# ---------------------------------------------------------------------------
# 3. Espace continu vs espace discret
# ---------------------------------------------------------------------------
def fig_continu_discret():
    f = lambda t: 1.6 * (1 - np.exp(-1.3 * t)) + 0.7 * np.exp(-((t - 2.3) / 0.6) ** 2) \
        + 0.25 * np.sin(1.4 * t)
    T = 6.0
    tt = np.linspace(0, T, 400)
    tn = np.linspace(0, T, 9)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5.2))
    for a in (a1, a2):
        a.set_xlim(0, T + 0.6)
        a.set_ylim(0, 3.4)

    # Continu
    a1.plot(tt, f(tt), color=BLEU, lw=3)
    a1.set_title("Espace continu", fontsize=28, color=BLEU, pad=12)
    a1.text(3.0, 0.45, r"$x(t)$ connu pour tout $t \in [0, T]$", fontsize=18, ha="center")
    axes_fleches(a1, r"$t$", r"$x(t)$")

    # Discret
    a2.plot(tt, f(tt), color=BLEU, lw=1.5, alpha=0.35)
    a2.plot(tn, f(tn), color=ORANGE, lw=2)
    a2.plot(tn, f(tn), "o", color=ORANGE, ms=10, zorder=4)
    for n, t in enumerate(tn):
        a2.plot([t, t], [0, f(t)], ls=":", color=GRIS, lw=1.2)
        a2.plot([t, t], [-0.06, 0.06], color=GRIS, lw=1.8, clip_on=False)
        if n <= 3:
            a2.text(t, -0.1, rf"$t^{n}$", ha="center", va="top", fontsize=22)
        if 1 <= n <= 3:
            a2.text(t, f(t) + 0.12, rf"$x(t^{n})$", ha="center", va="bottom",
                    fontsize=18, color=ORANGE)
    a2.text(tn[5], -0.1, r"$\cdots$", ha="center", va="top", fontsize=22)
    # pas de temps dt
    y = 0.45
    a2.annotate("", xy=(tn[5], y), xytext=(tn[4], y),
                arrowprops=dict(arrowstyle="<|-|>", color=BLANC, lw=1.5, mutation_scale=14))
    a2.text((tn[4] + tn[5]) / 2, y + 0.07, r"$dt$", ha="center", va="bottom", fontsize=22)
    a2.set_title("Espace discret", fontsize=28, color=ORANGE, pad=12)
    axes_fleches(a2, r"$t$", None)

    fig.tight_layout(w_pad=4)
    sauver(fig, "espaces_continus_discrets_s2")


if __name__ == "__main__":
    fig_derivee()
    fig_trajet()
    fig_continu_discret()
