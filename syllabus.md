
# Syllabus

![width:200px](illu_mod_num_s.png)

- Enseignant: Guillaume Jouvet (guillaume.jouvet (at) unil.ch)

- Assistant(e)s 2024:  Brandon Finley, Frederik Iat Hin Tam, Kejdi Lleshi, Mattia Mazzucchelli, Océane Pfister

## Objectif du cours

Le but est d’être capable de modéliser des processus naturels (p.e. diffusion d'un polluant dans le sol, diffusion de la température suite à une intrusion magmatique, dynamique des glaciers) à l'aide de méthodes numériques en utilisant Python, et de faire des expériences numériques qui reproduisent la réalité. Pour cela, l'approche de ce cours est essentiellement pratique. Il s'agit d'implémenter de façon simple et intuitive les équations qui décrivent la physique des processus étudiés dans un code informatique. Nous mettons notamment l'accent sur la similarité des codes développés pour des processus de natures très différentes.

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


## Exercices

Une semaine sur deux, les exercices donnés le vendredi sont à rendre pour le mercredi 20h00 sur la platforme moodle. L'autre semaine, la solution sera donnée une semaine plus tard.

## Plan du cours

| **Cours**  | **Contenu**  et _exercices_ |
|------------------|---------------------------------------------------------------------------------|
| 1          | Introduction, initialisation et règle de mis à jour, sauvegarde des résultats. _Exercice du compte en banque_  |
| 2          | Equation du mouvement en 1D, discrétisation temp., approximation d'une dérivée. _Exercice du mouvement d'une voiture en 1D & exercice plot interactif_  |
| 3          | Equation du mouvement en 2D, discrétisation spatiale. _Exercice de la bombe volcanique, exercice discrétisation spatiale_  |
| 4          | Equation de diffusion, EDP et conditions de bord. _Exercice diffusion concentration, fuite de Dayllens_   |
| 5          | Equation de diffusion (température), conditions de bord, condition d'arrêt. _Exercice diffusion température, intrusion magmatique_  |
| 6          | Diffusion-advection-réaction 1D, méthode de splitting et schéma upwind. _Exercice diffusion d'un polluant dans une rivière_ |
|                  | **Test I**   |
|                  | _Pause_   
| 7          | Diffusion 2D. _Exercice manipulation Grille 2D, Modélisation Periglesol Cervin_  |
| 8          | Diffusion-advection 2D. _Exercice diffusion de la température dans la croûte terrestre_  |
| 9          | Diffusion-advection-réaction 2D. Advection non-uniforme. _Exercice d'une contamination dans un lac_ |
| 10         | Equation de la glace 1D, equation de diffusion non-linéaire 1D. _Modélisation d'un glacier synthétique_                                           |
| 11         | Equation de la glace 2D, equation de diffusion non-linéaire 2D. _Modélisation d'un glacier réel, le glacier du Gorner (VS)_ |
|                  | **Test II**                                                                     |

 
## Documents (pdf)

Le cours vient avec des document annexes:

- [Introduction à Python pour la modélisation numérique](documents/Python_pour_la_modelisation_numerique.pdf)

- [Check-list d'un modèle numérique](documents/Check-list-mod-num.pdf)


## Auteurs

Les personnes suivantes ont contribué à construire ou/et donner/assister ce cours (par ordre chronologique):

Yury Podladchikov, Ludovic Räss, Samuel Omlin, Evangelos Moulas, Frederic Herman, Vjeran Visnjevic, Aleksandar Licul, Luca Malatesta, Daniel Kiss, Lorenzo Candioti, Ian Delaney, Emilie Macherel, Gino Licinil, Guillaume Jouvet, Daniel Bonser, Samuel Cook, Marjolein Gevers, Kejdi Lleshi, Brandon Finley, Vincenzo Guzzardi, Frederik Iat Hin Tam, Mattia Mazzucchelli, Océane Pfister
 
Le re-formatage du cours sous la forme actuelle d'un textbook et sa mise en ligne ont été réalisées par Guillaume Jouvet avec l'aide de Océane Pfister (avec le soutien d'un project FINV de l'UNIL par Tom Buecler et Christian Kaiser).