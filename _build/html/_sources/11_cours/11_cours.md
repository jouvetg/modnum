---
marp: true
theme: default
class: invert
backgroundColor: black
color: white
---

# Cours 11

![](../illu_mod_num_s.png)

---

# Objectifs du cours
 
- Formuler l'équation de la glace en 2D
- Résoudre l'équation en 2D
- Implémenter l'équation 2D dans un code

---

# Modelisation des glaciers en 2D

  
 
![width:750](https://images.contenthub.dev/xshiytapvw9a/e404ac0c4deb0f9ef3d3bd6859603bb2/Gornergletscher%20Wanderung%20Rotenboden.jpg?fm=avif&fit=fill&q=45&h=640&w=1140)

*Le Glacier du Gorner vers Zermatt*

---

# L'équation de la glace en 2D

En reprenant les notations, le modèle 1D se généralise en 2D:

$$\frac{\partial h}{\partial t} = - \frac{\partial q_x}{\partial x}  
- \frac{\partial q_y}{\partial y} + b(s), \qquad (1) $$
 
$$ q_x = - D(h) \frac{\partial s}{\partial x}, \qquad q_y = - D(h) \frac{\partial s}{\partial y}, \qquad (2) $$

$$D(h) = f_\mathrm{d} (\rho g)^3 h^5 \lvert\lvert  \nabla s \rvert \rvert^2.  \qquad (3)$$

Comme en 1D, la non-linéarité vient du fait que le diffusivité $D$ dépende elle-même de la solution, l'épaisseur locale de la glace $h$ et de la pente de sa surface $s$:

$$\lvert\lvert  \nabla s \rvert \rvert^2 =  (\frac{\partial s}{\partial x})^2 + (\frac{\partial s}{\partial y})^2.$$

---

# Résolution numérique

Comme en 1D, il faut :

1. Mettre à jour l'altitude de la surface du glacier s=l+h.
2. Mettre à jour la diffusivité D.
3. Mettre à jour le pas de temps dt.
4. Mettre à jour le bilan de masse b.
5. Veiller à ce que l'épaisseur de glace reste positive.
6. Forcer l'épaisseur à être zéro sur les bords.

La difficulté en 2D est de gérer la discrétisation spatiale sur la grille 2D. Seuls 2., 3., 6. différent entre les cas 1d et 2D, et sont donc traités plus bas. Pour les autres, il n'y a auncune différence d'implémementation vu dans le cours précédent.

---

# Traitement de la grille en 2D (1/4)

Le problème est comparbale au cas 1D, mais la position de toutes les valeurs sur la grille est plus complexe en 2D: les diverses quantités (tableaux ou matrices 2D) utilisées dans les équations (1)-(3) sont à des endroits spécifiques sur la grille 2D:


```
□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□
|       |       |       |       |       |       |       |       |       |
-   o   -   o   -   o   -   o   -   o   -   o   -   o   -   o   -   o   -
|       |       |       |       |       |       |       |       |       |
□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□
|       |       |       |       |       |       |       |       |       |
-   o   -   o   -   o   -   o   -   o   -   o   -   o   -   o   -   o   -
|       |       |       |       |       |       |       |       |       |
□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□
|       |       |       |       |       |       |       |       |       |
-   o   -   o   -   o   -   o   -   o   -   o   -   o   -   o   -   o   -
|       |       |       |       |       |       |       |       |       |
□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□---+---□
```

---

# Traitement de la grille en 2D (2/4)

- Les variables originales (épaisseur de glace, altitude du glacier) sont définies aux nœuds des grilles (`□` ci-dessus, taille `(ny,nx)`).

- La diffusivité $D$ est calculée aux centres des cellules (`o` ci-dessus, taille `(ny-1,nx-1)`). Pour satisfaire cette taille, la diffusivité est obtenue à partir de l'équation (Eq. (3)) :

    - de l'épaisseur de glace $h$ moyennée localement sur les épaisseurs aux quatre cellules voisines.

    - des pentes $s_x = \frac{\partial s}{\partial x}$ et $s_y = \frac{\partial s}{\partial y}$, qui sont obtenues en dérivant dans les directions $x$ et $y$, respectivement, puis en moyennant dans les directions $y$ et $x$.


---

# Traitement de la grille en 2D (3/4)

Une fois $D$ calculée, nous pouvons calculer les flux de glace $q_x$ et $q_y$ via l'équation:
$$ q_x = - D(h) \frac{\partial s}{\partial x}, \qquad (3).$$
Notons que :
- $D$ est de taille `(ny-1,nx-1)` (voir la diapositive précédente),
- $\frac{\partial s}{\partial x}$ est de taille `(ny,nx-1)`,
- $q_x$ doit être de taille `(ny-2,nx-1)` puisque $\frac{\partial q_x}{\partial x}$ est de taille `(ny-2,nx-2)`.

Pour que (3) soit consistante en taille `(ny-2,nx-1)`, il faut donc moyenner $D$ en $y$ pour perdre une cellule, et tronquer la première et la dernière ligne de $\frac{\partial s}{\partial x}$.

La même stratégie est appliquée pour calculer $q_y$ en inversant $x$ et $y$.

---

# Traitement de la grille en 2D (4/4)

Une fois $q_x$ et $q_y$ calculés, nous avons :

- $q_x$ de taille `(ny-2,nx-1)` est défini aux interfaces verticales (`-` ci-dessus).

- $q_y$ de taille `(ny-1,nx-2)` est défini aux interfaces horizontales (`+` ci-dessus).

Il suffit de mettre à jour l'épaisseur de glace en fonction des flux, comme d'habitude, de sorte que $dh/dt$ soit de taille `(ny-2,nx-2)` :

```python
dhdt = - ( (qx[:,1:] - qx[:,:-1]) / dx + (qy[1:,:] - qy[:-1,:]) / dy )
h[1:-1, 1:-1] += dt * dhdt
```
 
---

# Ebauche de code


```python
# Calculate H_avg, size (ny-1,nx-1)
h_avg = …

# Compute Snorm, size (ny-1,nx-1)
snorm = …

# Compute D, size (ny-1,nx-1)
D = …

# Compute qx, size (ny-2,nx-1)
Qx = …

# Compute qy, size (ny-1,nx-2)
Qy = …

# Compute dHdt, and update rule, size (ny-2,nx-2)
dhdt = ...
h[1:-1, 1:-1] += dt * dHdt
```
---

# Pas de temps

Pour assurer la stabilité de la méthode, nous prendrons le pas de temps $dt$ adaptatif suivant qui généralise celui que l'on a vu en 1D: 

$$ dt = \min \left\{ dt_{max} , \frac{min(dx, dy)^2}{4.1 \times \max(|D|)} \right\}. $$

Comme dans le cas 1D, le pas de temps est adaptatif, c.a.d. il doit être mis à jour comme la diffusité.

---

# Conditions de bords

Forcer l'épaisseur de glace à être nulle sur les 4 cotés du domaine modélisé s'écrit:

```python
h[0,:]  = 0
h[-1,:] = 0
h[:,0]  = 0
h[:,-1] = 0
```

 