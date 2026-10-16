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

# Cours 5


![](../illu_mod_num_s.png)

---

# Objectifs du cours

- Équation de diffusion de la température
- Conditions aux bords de Dirichlet ou Neumann
- Condition d'arrêt d'un modèle
- Code multi-questions

---

# Loi de Fick pour la concentration $C$ (rappel)

**Le flux de particules $q_x$ dépend de la dérivée de la concentration $C$**

Plus la **variation (dérivée) de concentration est grande**, plus les particules vont se **déplacer** (rapidement), plus il y a de **diffusion**:
$$q_x = -D \frac{\partial C}{\partial x},$$
où $D$ est le paramètre de diffusion.

![width:550px](./fig/graph_concentration_s5.png)

---

# Loi de Fourier pour la température $T$ (nouveau)

**Le flux de chaleur $q_x$ dépend de la dérivée de la température $T$**

Plus la **variation (dérivée) de température est grande**, plus la chaleur va se **déplacer** (rapidement), plus il y a de **diffusion**:

$$q_x = -D \frac{\partial T}{\partial x},$$

où $D$ est le paramètre de diffusion.

![width:550px](./fig/fourier_chaleur_s5.png)


---

# Équation de la diffusion thermique

→ **Loi de Fourier**

$$q_x = -D \frac{\partial T}{\partial x},$$

→ **Principe de conservation**

$$\frac{\partial T}{\partial t} = -\frac{\partial q_x}{\partial x} $$

Diffusivité thermique ($m^2/s$) de l’aluminium (0.0001), du béton (0.0000005), de l’eau (0.0000001),  la glace (0.000001), ...

**Le modèle de diffusion est strictement le même que pour la concentration.**

---

# Discrétisation de la diffusion thermique

Si on connait la température au temps précédent, on obtient la température au temps suivant en trois étapes comme pour la concentration:

→ 1) mettre à jour le flux en discrétisant : $q_x = -D \frac{\partial T}{\partial x},$
```python
qx = - D * ( T[1:] - T[:-1] ) / dx  # taille nx-1
```
→ 2) mettre à jour `dTdt` en discrétisant: $\frac{\partial T}{\partial t} = -\frac{\partial q_x}{\partial x},$
```python
dTdt  = - ( qx[1:] - qx[:-1] ) / dx  # taille nx-2
```
→ 3) mettre à jour la température.
```python
T[1:-1] += dTdt * dt               # taille nx-2
```
---

# Ou vivent `T`, `qx`, `dTdt` ?
 
```
T                   |-----|-----|-----|-----|-----|-----|-----|-----|
T[1:]                     |-----|-----|-----|-----|-----|-----|-----|
T[:-1]              |-----|-----|-----|-----|-----|-----|-----|
qx                     |-----|-----|-----|-----|-----|-----|-----|
dTdt                      |-----|-----|-----|-----|-----|-----|
```

Pour obtenir les coordonnées **entre** les nœuds, on moyenne 2 points successifs :

```
x                       |-----|-----|-----|-----|-----|-----|-----|-----|
x[1:]                         |-----|-----|-----|-----|-----|-----|-----|
x[:-1]                  |-----|-----|-----|-----|-----|-----|-----|
xm = (x[1:]+x[:-1])/2      |-----|-----|-----|-----|-----|-----|-----|
```

On perd une cellule : `xm` est de taille $n_x - 1$.

Par example, cela permetrait de tracer la fonction flux avec `plt.plot(xm,qx)`

---

# Les conditions aux bords (CdB)

Si les équations décrivent la diffusion à l'intérieur du domaine

→ il faut préciser ce qui se passe à ses bords via les CdBs.

```
  CdB gauche                                                   CdB droite
     |------------------------------------------------------------|
```


Celles-ci peuvent influencer énormément la solution !


- CbD **du type  “Dirichlet”** sur la **fonction** T ou C
→ Fixe la **concentration** ou **température** sur les bords  

- CbD **du type “Neumann”** sur la **dérivée** de T ou C
→ Fixe le **flux** de concentration ou température sur les bords 

---

# Condition aux bords de Dirichlet

→ Fixe la concentration ou température sur les bords

→ Condition sur T ou C, p.e.

$$C(0) = a, \qquad\qquad\qquad\qquad
\qquad\qquad\qquad\qquad\qquad\qquad C(1) = b$$


→ Dans le code, cela sera:
```python
C[0]  = a
C[-1] = b
```

---

# Condition aux bords de Neumann

→ Fixe le **flux** / la **dérivée** de concentration ou de température sur les bords

→ Condition sur la dérivée T ou C, p.e.

$$\frac{dC}{dx}(0) = a, \qquad\qquad\qquad\qquad
\qquad\qquad\qquad\qquad\qquad\qquad \frac{dC}{dx}(1) =b$$


→ Dans le code, cela sera:
```python
C[0]  = C[1]  - dx * a
C[-1] = C[-2] + dx * b
```

En effet $\frac{dC}{dx}(0) = a$ se discrétise $\frac{C_1 - C_0}{dx} = a$, ce qui se ré-écrit $C_0 = C_1 - a \, dx$.

**Attention:** c'est bien $dx$ (le pas d'espace) qui intervient, et non $dt$.

---

# Condition de flux nul (Neumann, cas spécial)

→ Impose un **flux** / une **dérivée** nul(le) de concentration ou de température sur les bords.

→ Condition sur la dérivée de T ou C, p.e.
$$\frac{dC}{dx}(0) = 0, \qquad\qquad\qquad\qquad
\qquad\qquad\qquad\qquad\qquad\qquad \frac{dC}{dx}(1) =0$$

→ Dans le code, cela sera:
```python
C[0]  = C[1]
C[-1] = C[-2]
```

En effet $\frac{dC}{dx}(0) = 0$ se discrétise $\frac{C_1 - C_0}{dx} = 0$, ce qui se ré-écrit $C_0 = C_1$.

---

# Récapitulatif : trois conditions aux bords

![height:500px](./fig/trois_conditions_s5.svg)

---

# Conditions aux bords mixtes

On peut avoir deux conditions aux bords différentes à gauche et à droite :

$$C(0) = 500, \quad \frac{dC}{dx}(1) =0$$

ou

$$\frac{dC}{dx}(0) = 0, \quad C(1) = 500$$

---

# Conditions aux bords (CDB)

Les CDB agissent à tout moment : il faut donc les implémenter dans la boucle.

```python
# Initialisation
C = ...

# Boucle temporelle
for it in range(nt):

  # Mise a jour condition équation de diffusion
  qx      = ...
  dCdt    = ...
  C[1:-1] += ...

  # Mise a jour condition aux bords
  C[0]    = C[1]
  C[-1]   = C_droit
```
---

# Stabilité et pas de temps

Comme pour la concentration, la contrainte de la diffusion est

$$ dt_\mathrm{diff} = \frac{dx^2}{2.1 \times D}, \qquad
dt = \min \left( dt_\mathrm{max}, \ dt_\mathrm{diff} \right)$$

```python
dt_diff = dx**2 / (2.1 * D)     # contrainte de la diffusion
dt      = min(dt_max, dt_diff)  # pas de temps retenu
```

---

# Condition d'arrêt d'un modèle

Souvent, nous voulons arrêter notre modèle lorsque celui-ci n'évolue quasi plus. 

Pour cela, nous mesurons la différence entre l'ancienne et la nouvelle solution, ce qui suppose d'en faire une copie avant la mise à jour :

```python
T_old = np.copy(T)
```
Ensuite, nous pouvons arrêter le modèle après la mise à jour avec un `break`:
```python
somme = np.sum(np.abs(T_old - T))
if somme < tol:
     break
```

Notons qu'en Python, il faut demander une copie via `T_old = np.copy(T)`, car la commande `T_old = T` ne le fera pas: `T_old` serait modifié avec `T` (*adresse*).

---

# Condition d'arrêt : un exemple

![height:480px](./fig/condition_arret_s5.svg)

---

# Code avec plusieurs variantes

Souvent, nous créons un code contenant plusieurs variantes (pour les différentes questions). Pour cela, il est pratique d'utiliser une variable `Q` comme suit :

```python
Q = 1  # Paramètre indiquant la question 1 ou 2 à définir au début du code

if Q == 1:
    ft = 600   # Paramètre de la question 1

elif Q == 2:
    ft = 90    # Paramètre de la question 2
```
 
Le but n'est pas de construire un nouveau code (quasiment identique à l'original), mais de ne modifier que la portion de code concernée.

→ Cela rend votre code bien plus **concis**!

---

<!-- _class: invert pratique -->

# La séance pratique

![](../05_exercice/fig/intrusions.svg)

**Que veut-on modéliser ?** — la chaleur de deux intrusions magmatiques successives, qui se diffuse dans la roche.

**Ce qui est nouveau**
- les **conditions aux bords** : Dirichlet, Neumann avc flux nul
- un **événement au milieu** du calcul : la seconde intrusion arrive
- un **code unique** pour plusieurs questions, piloté par `Q`
- une **condition d'arrêt** sur une sonde posée dans le domaine

**L'exercice** — dater le moment où la sonde franchit son seuil de température, puis voir comment ce moment dépend des conditions aux bords.

**Le tutoriel** — des tailles cohérentes en 1D, et comment écrire un seul code pour plusieurs questions.