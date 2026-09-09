
# Modélisation Numérique -- Syllabus

![width:200px](illu_mod_num_s.png)

- Enseignant: Guillaume Jouvet (guillaume.jouvet (at) unil.ch)

- Assistant(e)s 2026: Fien De Doncker, Brandon Finley, Thomas Gregov, Kejdi Lleshi, Mattia Mazzucchelli, Hélène Morciaux 

## Objectif du cours

Le but est d’être capable de modéliser des processus naturels (p.e. diffusion d'un polluant dans le sol, diffusion de la température suite à une intrusion magmatique, dynamique des glaciers) à l'aide de méthodes numériques en utilisant Python, et de faire des expériences numériques qui reproduisent la réalité. Pour cela, l'approche de ce cours est essentiellement pratique. Il s'agit d'implémenter de façon simple et intuitive les équations qui décrivent la physique des processus étudiés dans un code informatique. Nous mettons notamment l'accent sur la similarité des codes développés pour des processus de natures très différentes. En quelques points, les buts du cours sont de:

- **Implémenter** mathématiquement un **processus physique** et le résoudre **numériquement**.
- **Comprendre les méthodes** de résolution, savoir implémenter chaque **étape** d’un modèle numérique des données aux résultats.
- **Programmer** le modèle en Python.

Le cours s’inscrit dans un **programme à long terme** de la Faculté des Géosciences et de l’Environnement qui permettra d’implémenter des **modèles complexes** durant le Master en environnement ou en géologie.

## Pré-requis

 - Mathématiques: Calcul Matriciel, Dérivées Partielles
 - Physique: Principe de base (p.e. loi de Newton)
 - Programmation: Notion de Python

Le premier dossier permet aux étudiants d'acquérir les notions essentielles de Python, si celles-ci ne sont pas déjà maîtrisées.

## Organisation du cours
 
| **Type d'activité**       | **Détails**                                                   |
|---------------------------|---------------------------------------------------------------|
| **Cours**                 | en salle Géopolis-2137 le vendredi 10.15-11.00                |
| **Travaux pratiques**     | encadrés au Géopolis 2145+2153+2138 le vendredi 11.00-13.00   |
| **Contrôle continu**      | Test I : 40 % , Test II : 60%                                 | 

## Page Moodle 

https://moodle.unil.ch/course/view.php?id=24768

## Plan du cours

Chaque séance comprend un **cours**, un **tutoriel** (courte mise en train pratique en début de travaux pratiques) et un **exercice**.

| **Séance** | **Cours** | **Tutoriel** | **Exercice** |
|---|---|---|---|
| 1 | Introduction, initialisation et règle de mise à jour, solution analytique vs. numérique | Notions fondamentales de Python pour ce cours | Le compte en banque |
| 2 | Équation du mouvement en 1D, discrétisation temporelle, approximation d'une dérivée | Se familiariser avec les figures interactives | Trajectoire d'une voiture en 1D puis en 2D |
| 3 | Bonnes pratiques de programmation, équations d'un projectile en 2D | La structure d'un code : la seiche du Léman | Trajectoire d'une bombe volcanique |
| 4 | Équation de diffusion, EDP, discrétisation spatiale | Discrétisation spatiale et dérivées | Diffusion d'une concentration ; fuite chimique de Daillens |
| 5 | Diffusion de la température, conditions aux bords, condition d'arrêt | Se familiariser avec les conditions aux bords | Intrusion magmatique |
| 6 | Diffusion-advection-réaction 1D, méthode de splitting, schéma upwind | Le décentrage « upwind » | Contamination d'une rivière au cyanure |
|  | **Test I** |  |  |
|  | _Pause_ |  |  |
| 7 | Diffusion 2D, conditions aux bords de Dirichlet | Affichage interactif de résultats 2D | Permafrost du Cervin |
| 8 | Diffusion-advection 2D, advection uniforme, conditions de Neumann | Construire des matrices 2D avec `np.meshgrid` | Température de la croûte terrestre |
| 9 | Diffusion-advection-réaction 2D, advection non uniforme | Champs de vitesse 2D et matrices de booléens | Contamination d'un lac |
| 10 | Équation de la glace 1D, diffusion non linéaire | Diffusivité variable et flux aux interfaces | Modélisation d'un glacier synthétique |
|  | **Test II** |  |  |

> 🧭 **Séance 11 — hors-programme, pour les curieux.** L'équation de la glace **en 2D** (diffusion non linéaire en deux dimensions) et la modélisation d'un glacier réel, le **glacier du Gorner** (VS), ne font **pas partie de la matière évaluée** et ne sont pas traitées en séance. Le cours, le tutoriel et l'exercice restent disponibles en ligne pour qui souhaite aller plus loin : ils réutilisent tout ce qui a été vu aux séances 7 à 10 et constituent un bon projet personnel.

 
## Grille d'évaluation d'un code

Cette grille sert à relire son propre code lors des exercices et de base pour l'évaluation des tests :

| **Code** | **Critère** | **Questions à se poser** |
|---|---|---|
| | **Présentation générale** | |
| **RU** | Le code fonctionne | Le code s'exécute-t-il sans erreur, pour toutes les questions ? Toutes les variables sont-elles définies avant usage ? |
| **CO** | Présentation du code | Le code est-il bien structuré (paramètres → discrétisation → initialisation → boucle → figure) ? Un seul code pour toutes les questions ? Propre et bien commenté ? Chaque instruction est-elle au bon endroit (dans ou hors boucle) ? |
| **DE** | Définition des variables | Tous les paramètres sont-ils définis en tête de code ? Les unités sont-elles adaptées ? Pas de « hard-coding » (valeurs écrites en dur) ? |
| **FI** | Figure | Est-elle dans la boucle et mise à jour ? Temps dans le titre, arrondi et avec unité ? Labels et limites d'axes (ou colorbar) fixés ? Bonnes variables tracées ? Lisible ? |
| | **Partie technique** | |
| **IC** | Condition initiale | Bonne valeur sur toute la grille, bonnes dimensions ? Apparaît avant la boucle ? |
| **PT** | Pas de temps et boucle temporelle | `dt` issu de la condition de stabilité ? Boucle `for` si le nombre de pas est connu, `while` sinon ? Temps mis à jour à chaque pas ? |
| **ED** | Équation de diffusion | Bien implémentée dans la boucle ? Sur les points intérieurs ? Avec le bon signe ? Adaptée à une diffusivité spatialement variable ou non linéaire ? |
| **ER** | Équation de réaction | Bien implémentée dans la boucle ? Avec les bonnes dimensions ? |
| **EA** | Équation d'advection | Bien implémentée dans la boucle ? Avec les bonnes dimensions ? Schéma « upwind » selon le signe de la vitesse ? Vitesses bien définies ? |
| **BC** | Conditions aux limites | Bien implémentées dans la boucle ? Bon type à chaque bord (Dirichlet / Neumann), bonnes valeurs ? |
| **FO** | Forçage | Bien implémenté dans la boucle ? Position bien convertie en indice ? Bonne valeur imposée ? |
| **CA** | Condition d'arrêt | Bien implémentée dans la boucle ? Sur la bonne variable au bon indice, avec le bon opérateur ? Un « flag » identifie-t-il la première occurrence ? |

## Auteurs

Les personnes suivantes ont contribué à construire ou/et donner/assister ce cours (par ordre chronologique):

Yury Podladchikov, Ludovic Räss, Samuel Omlin, Evangelos Moulas, Frederic Herman, Vjeran Visnjevic, Aleksandar Licul, Luca Malatesta, Daniel Kiss, Lorenzo Candioti, Ian Delaney, Emilie Macherel, Gino Licinil, Guillaume Jouvet, Daniel Bonser, Samuel Cook, Marjolein Gevers, Kejdi Lleshi, Brandon Finley, Vincenzo Guzzardi, Frederik Iat Hin Tam, Mattia Mazzucchelli, Océane Pfister
 
Le re-formatage du cours sous la forme actuelle d'un textbook et sa mise en ligne ont été réalisés par Guillaume Jouvet avec l'aide de Océane Pfister (avec le soutien d'un projet FINV de l'UNIL par Tom Beucler et Christian Kaiser).
