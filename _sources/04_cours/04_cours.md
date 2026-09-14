---
marp: true
theme: default
class: invert
backgroundColor: black
color: white

style: |
  section.pratique { font-size: 22px; }
  section.pratique h1 { font-size: 38px; margin: 0 0 0.3em 0; }
  section.pratique p, section.pratique ul { max-width: 58%; margin: 0.4em 0; }
  section.pratique li { margin-bottom: 0.1em; }
  section.pratique p:nth-of-type(1) {
    position: absolute; right: 50px; top: 122px;
    width: 38%; max-width: none; margin: 0; text-align: center; }
  section.pratique p:nth-of-type(1) img {
    max-width: 100%; max-height: 385px; width: auto; height: auto; }
  section.pratique p:last-of-type {
    position: absolute; right: 50px; bottom: 50px;
    width: 38%; max-width: none; margin: 0; }
---

# Cours 4

![](../illu_mod_num_s.png)

---

# Objectifs du cours

- Introduction au modèle de diffusion en 1D
- Illustration par des exemples
- Principes physiques de la diffusion
- Formulation mathématique
- Discrétisation spatiale
- Slicing et approximation numérique
- Implémentation en Python
- Conditions aux bords (aperçu) et utilisation d'un flag
- Stabilité et pas de temps

---

# Exemple 1: Un contaminant se diffuse

![Alt text](fig/contaminant_diffusion_s4.png)

Source: https://youtu.be/6hmqOFITPbs

---

# Ex 2: Pollution des sols (accident de Daillens)

![width:700px](./fig/pollution_sols_s4.png)

---

# Exemple 3:  Température dans le sol

![height:400px](./fig/temp_sol_s4.jpg) ![height:400px](./fig/temp_sol2_s4.jpg)

Source 1: https://www.energie-environnement.ch/
Source 2: https://en.wikipedia.org/wiki/Active_layer

---

# Introduction à la diffusion

L'équation de diffusion peut être utilisée pour représenter une grande variété de processus naturels et environnementaux. L'expression mathématique que nous allons dériver peut servir à modéliser:

- le transfert de chaleur dans la croûte terrestre,
- l'évolution des sols,
- le transport de contaminants dans un aquifère ou dans l'atmosphère,
- l'érosion des chaînes de montagnes,
- l'évolution des glaciers, etc.


<small>Loi introduite par **Fourier** en 1822 pour calculer la distribution de la température dans les matériaux, puis, elle a été utilisée par **Fick** pour modéliser la diffusion de la matière.</small>

---

# Interprétation graphique

À partir de l'exemple de la variation de concentration d'un colorant se déplaçant dans un gel, l'équation de diffusion permet de représenter le déplacement de molécules depuis une zone de haute concentration vers une zone de basse concentration, comme l'illustre cette figure (où $C$ représente la concentration).

![width:700px](./fig/diffusion.png)

<small>*Gauche : représentation continue de la diffusion de molécules d'une zone hautement concentrée vers une zone à faible concentration. Droite : représentation discrétisée en temps et en espace.*</small>

---

# Interprétation graphique

- La diffusion désigne le déplacement de particules d'une zone de haute concentration vers une zone de basse concentration.

- Le mouvement de particules de gauche à droite est plus marqué lorsque le saut de concentration est élevé, tandis qu'il est faible lorsque la concentration est homogène.

- Cela entraîne un transfert de particules qui dépend de la différence de concentration $\Delta C$ de part et d'autre d'une cellule de largeur $\Delta x$.

- Ainsi, le flux de particules (le nombre de particules traversant par unité de temps et de surface) dépend du gradient de concentration.

---

# Formalisation mathématique

Un problème de diffusion peut être décrit par une **équation aux dérivées partielles** (EDP). Dans le cas de la diffusion d'un liquide dans un autre, cette EDP modélise l'évolution de la concentration $C$ en fonction du temps $t$ et de l'espace $x$, en tenant compte de la **concentration initiale** et des **conditions aux bords**.

- Supposons une discrétisation uniforme de l'espace avec un pas $dx$, et une section unitaire ($1 \, \textup{m}^2$)
- Définissons $C$ comme la concentration d'un polluant donnée par $C = \frac{n}{dx}$ (en $\textup{mol}/\textup{m}^3$), où $n$ est le nombre de particules (en mol).
- Le flux de particules $q_x$ est défini comme le nombre de particules déplacées par unité de temps et de surface $\left(\frac{\textup{mol}}{\textup{m}^2 \, \text{s}}\right)$.

L'EDP de diffusion repose sur deux principes :

---

# 1. Loi de Fick (Fourier dans le cas de la chaleur)

Comme vu précédemment, le transfert de particules dépend de la différence de concentration $\Delta C$ de part et d'autre d'une cellule de largeur $\Delta x$: plus la **variation** (dérivée) de concentration est grande, plus les particules se **déplacent** rapidement, ce qui augmente la **diffusion**. En d'autres termes, le flux de particules dépend du gradient de concentration :

$$ q_x = -D \frac{\partial C}{\partial x}, \qquad (1) $$

où $D$ est le coefficient de diffusion, ou *diffusivité*. Ce coefficient varie selon les problèmes et définit la vitesse de transfert des particules (molécules de pollution dans un sol ou particules de sol sur une colline).

---

# 2. Principe de conservation (1/2)

![width:800px](./fig/principe_conservation_s4.png)

---

# 2. Principe de conservation (2/2)

Selon le principe de conservation, le changement du nombre de particules *n* dans un bloc entre l’instant *t* et l’instant $t + dt$ peut être calculé à partir de la différence des flux entrants et sortants :

$$\Delta n = \big( q_x(x) - q_x(x+\Delta x) \big) \, dt.$$

En utilisant la définition de la concentration *C = n/dx*, l'équation précédente s'écrit :

$$\frac{\Delta C}{dt} = \frac{q_x(x) - q_x(x+\Delta x)}{\Delta x},$$

qui se transforme en forme continue :

$$\frac{\partial C}{\partial t} = -\frac{\partial q_x}{\partial x}, \qquad (2)$$


---

# Mise en équation de la diffusion

**L'équation de diffusion** peut être exprimée comme une dérivée seconde de la concentration $C$ en combinant

→ Loi de Fick/Fourier

$$q_x = -D \frac{\partial C}{\partial x},  \qquad (1)$$

→ Principe de conservation

$$\frac{\partial C}{\partial t} = -\frac{\partial q_x}{\partial x},  \qquad (2)$$


ce qui donne l'EDP suivante (que nous n'utiliserons pas sous cette forme):

$$ \frac{\partial C}{\partial t} = D \frac{\partial^2 C}{\partial x^2}.$$

---

# Discrétisation spatiale

Pour modéliser l'évolution spatio-temporelle d'une quantité physique comme la concentration, il est nécessaire de discrétiser le temps et l'espace, c'est-à-dire de diviser le domaine spatial de modélisation en intervalles avec un ensemble de points où la solution sera calculée :
```
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
```
Par exemple: $x_0 = 0, x_1 = 0.1, x_2 = 0.2, ..., x_{10} = 1$

avec une longueur d'intervalle $dx = 0.1$. Cette discrétisation se code ainsi:

```python
import numpy as np
a = 0 ; b = 1 ; nx = 11
x  = np.linspace(a, b, nx)
dx = (b-a)/(nx-1)
```

---

# Variable discrétisée

Maintenant que notre domaine est discrétisé, nous pouvons initialiser une variable (p.e. la concentration $C$) sur ce domaine. Dans le domaine discrétisé, $C$ devient un vecteur, dont les valeurs sont définies aux nœuds de discrétisation:

```python
C = np.ones(nx)*2 # Initialisation à 2 partout
```

Pour accéder ou modifier la valeur de la concentration $C$ en un point du domaine, p.e. au point $x = 0.6$, il convient de trouver l'indice qui lui correspond, c'est-à-dire le point de discrétisation qui est le plus proche du point $x = 0.6$ (car il est possible que $x = 0.6$ ne tombe pas exactement sur un nœud):

```python
xp = 0.6
ixp = round((xp-a)/dx) # indice de la composante la plus proche de xp
C[ixp] = 6             # modification de la valeur en ce point
```

---

# Rappel sur le "Slicing" d'un vecteur

Si l'on a un vecteur de taille 9:
```
x                   |-----|-----|-----|-----|-----|-----|-----|-----|
```
alors nous obtenons les sous-vecteurs suivants:
```
x[1:]                     |-----|-----|-----|-----|-----|-----|-----|
x[3:]                                 |-----|-----|-----|-----|-----|
x[3:5]                                |-----|
x[3:7]                                |-----|-----|-----|
x[:-1]              |-----|-----|-----|-----|-----|-----|-----|
x[:-4]              |-----|-----|-----|-----|
x[::2]              |-----------|-----------|-----------|-----------|
x[::4]              |-----------------------|-----------------------|
```

**Ces écritures servent à toutes les discrétisations qui suivent.**

---

# Valeurs aux noeuds et au centre des cellules

Il est parfois nécessaire de calculer des valeurs entre les nœuds de discrétisation. Cela peut se faire en faisant une moyenne entre deux points successifs:

```python
Cmid = (C[1:]+C[:-1])/2 # calcul de la concentration au milieu des cellules
xmid = (x[1:]+x[:-1])/2 # calcul des coordonnées  au milieu des cellules
```

Cela se justifie visuellement comme cela:

```
x                   |-----|-----|-----|-----|-----|-----|-----|-----|
x[1:]                     |-----|-----|-----|-----|-----|-----|-----|
x[:-1]              |-----|-----|-----|-----|-----|-----|-----|
(x[1:]+x[:-1])/2       |-----|-----|-----|-----|-----|-----|-----|
```

Notons qu'en faisant cela, nous avons perdu une cellule ; le vecteur `(x[1:]+x[:-1])/2`est maintenant de dimension $n_x - 1$.

---

# Approximation numérique

Pour approcher la dérivée en temps, la règle de mise à jour permet de définir l'état futur (à l’instant $t + dt$) de notre modèle en ajoutant à l'état actuel au temps $t$ le taux de changement $\partial f / \partial t$ fois le pas de temps $dt$:

$$ \frac{\partial f}{\partial t} \sim \frac{f^{new} - f^{old}}{dt}\ \ \rightarrow \ \ f^{new} \sim f^{old}+\frac{\partial f}{\partial t} \times dt.  \qquad (4) $$

Si on a une discrétisation du temps, que l’on connait la concentration au temps précédent, comment la mettre à jour ?

 1) mettre à jour le flux en discrétisant : $q_x = -D \frac{\partial C}{\partial x},$
 2) mettre à jour `dCdt` en discrétisant: $\frac{\partial C}{\partial t} = -\frac{\partial q_x}{\partial x}$,
 3) mettre à jour la concentration.

---

# 1) Approximation numérique du flux `qx`

Discrétiser le flux

$$q_x = -D \frac{\partial C}{\partial x},$$

peut se faire par différences finies :

$$ (q_x)^n_i = -D \ \frac{C_{i+1}^n - C_i^n}{dx}, \quad i=0,...,n_x-2$$

lequel se code en python ainsi:

```python
qx = - D * ( C[1:] - C[:-1] ) / dx
```

Attention, après cela `qx` a perdu une cellule (taille $n_x - 1$), et est défini au centre des cellules (contrairement à `C`, qui a une taille de $n_x$).

---

# 2) Approximation numérique de `dCdt`

Discrétiser `dCdt`

$$\frac{\partial C}{\partial t} = -\frac{\partial q_x}{\partial x}$$

se fait aussi par différences finies :

$$ (dCdt)^n_i  = - \frac{(q_x)_{i}^n - (q_x)_{i-1}^n}{dx}, \quad i=1,...,n_x-2$$

lequel se code en python ainsi:

```python
dCdt = - ( qx[1:] - qx[:-1] ) / dx
```
Une fois encore, on perd une cellule, de sorte que `dCdt` a une taille $n_x - 2$. On revient donc aux nœuds où $C$ est défini.

---

# 3) Règle de mise à jour

Enfin, la dernière étape consiste à mettre à jour la concentration $C$ en discrétisant par difference finies:

$$\frac{\partial C}{\partial t} = dCdt,$$

ce qui donne

$$\frac{C^{n+1}_i - C^n_i}{dt} = (dCdt)^n_i, \quad i=1,...,n_x-2$$

lequel se code en python :

```python
C[1:-1] += dCdt * dt
```

---

# Dérivées et taille de vecteurs

La mise à jour de la concentration $C$ par diffusion est le résultat de deux dérivées successives. À chaque dérivée, on perd une cellule. Pour $n_x$ nœuds, il y aura $n_x - 1$ flux entre eux, et $n_x - 2$ valeurs pour `dCdt`.


```
Vecteur                                                               Taille

C                         |-----|-----|-----|-----|-----|-----|-----|  nx
C[1:]                           |-----|-----|-----|-----|-----|-----|
C[:-1]                    |-----|-----|-----|-----|-----|-----|

qx = -D*(C[1:]-C[:-1])/dx    |-----|-----|-----|-----|-----|-----|     nx-1
dCdt = -(qx[1:]-qx[:-1])/dx     |-----|-----|-----|-----|-----|        nx-2
C[1:-1] += dCdt * dt            |-----|-----|-----|-----|-----|        nx-2
```


**Attention :** il faut faire des opérations sur des vecteurs de tailles compatibles !



---

![bg](./fig/scheme_1.png)

---

![bg](./fig/scheme_2.png)

---

![bg](./fig/scheme_3.png)

---

# Conditions aux bords

La règle de mise à jour
```python
C[1:-1] += dCdt * dt
```
n'agit pas sur les valeurs de `C` aux extrémités (c'est-à-dire `C[0]` et `C[-1]`).

Si l'on ne fait rien, les valeurs de bord de `C` ne sont donc pas mises à jour et restent à leur état initial.

Dans ce cours, nous n'irons pas plus loin. Toutefois, nous verrons dans le cours suivant qu'il y a plusieurs options pour mettre à jour les valeurs au bord selon les conditions physiques du problème. C'est ce qu'on appelle les conditions aux bords.

---

# Pas de temps $dt$ et stabilité

La **stabilité** et la **précision** d’un modèle numérique dépendent de son pas de temps $dt$, lequel doit être suffisamment petit, comme le montre la figure suivante.

![width:550px](./fig/graph_precision_s4.png) ![width:550px](./fig/graph_precision2_s4.png)


Dans le cas d'un problème de diffusion, la stabilité est assurée si le pas de temps ne dépasse pas

$$ dt_\mathrm{diff} = \frac{dx^2}{2.1 \times D}.$$

---

# Pas de temps $dt$: écriture systématique

Convention gardée **jusqu'à la fin du cours**: on calcule la contrainte de chaque processus séparément, et on retient la plus petite:

$$ dt = \min \left( dt_\mathrm{max}, \ dt_\mathrm{diff} \right)$$

```python
dt_max  = 0.1                   # pas de temps maximal
dt_diff = dx**2 / (2.1 * D)     # contrainte de la diffusion
dt      = min(dt_max, dt_diff)  # pas de temps retenu
```

→ Au cours 6, l'advection ajoutera sa propre contrainte $dt_\mathrm{adv}$.

---

# Utilisation d'un flag

Il peut être utile de détecter quand une condition est remplie pour la première fois, par exemple, pour trouver à quel moment une température au milieu du domaine passe pour la première fois au-dessus de zéro:

```python
[...]
flag_firstfois = True
for it in range(nt):
    ix = int(nx/2)                       # indice du milieu du domaine
    if (T[ix] > 0) & (flag_firstfois):
        temps_passage_seuil = it * dt    # le temps vaut it * dt
        flag_firstfois = False
    [...]
```
Sans la variable "flag", la variable `temps_passage_seuil` serait réécrite à chaque pas de temps (car la condition reste satisfaite), et l'on perdrait l'information du moment où cette condition a été remplie pour la première fois. Alternativement, on aurait pu utiliser un `break`.

---

<!-- _class: invert pratique -->

# Séance 4 — la séance pratique

![](../04_exercice/fig/fuite_chimique_shema_s5.png)

**Que veut-on modéliser ?** — un polluant qui diffuse dans le sol depuis le lieu d'un accident, jusqu'à la rivière voisine.

**Ce qui est nouveau**
- une **dérivée spatiale**, et le flux $q_x = -D\,\partial C/\partial x$
- des tableaux de **tailles différentes** : $n$, $n-1$, $n-2$
- la contrainte de stabilité $dt_\mathrm{diff} = dx^2/(2.1\,D)$
- un `flag` pour dater le franchissement d'un seuil

**L'exercice** — dater l'arrivée du polluant dans la rivière, puis le moment où le flux qui s'y déverse commence enfin à décroître.

**Le tutoriel** — discrétisation spatiale, slicing, indexation et assignation, et l'approximation d'une dérivée.
