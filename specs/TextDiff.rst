################################ Spécifications widget de comparaison de texte ################################

1 Introduction
**************
!!!orthographe!!!
!!! faire fonctionner les images  !!! 

1.1 But du projet
=================

Ce widget aura pour but de comparer differentes version d'un même texte dans une même langue.

Il peut être utilisé par toutes les personnes nécessitant d'extraire les différences entre deux textes de même nature, que se soit pour de la recherche littéraire ou pour tout autre besoin de comparaison de texte.

Les widgets pouvant être acceptées en entrée seront Text Field et Text Files.
Le widget doit et ne peux avoir plus de 2 widgets en entrée.
Le widget dans sa version principale a un output de type tableau qui retourne la comparaison entre les deux textes. (dans sa version optionnelle il peut se lier à un widget visualize-distribution).

Ce widget sera utile à toute personne qui souhaite comparer deux texte de même nature simplement. La plus value du widget sera de pouvoir effectuer une comparaison entre deux textes sans avoir à crée son propre scripte python, cela permettra donc de rendre cette fonctionnalité accessible aux personnes moins enclines à la programmation. 


1.2 Aperçu des étapes
=====================
* Première version des spécifications: 17.03.2025
* Remise des spécifications: 24.03.2025
* Version alpha du projet: 21.04.2025
* Version finale du projet: 26.05.2025

1.3 Équipe et responsabilités => qui va faire quoi => qui prends en charge quoi => rôle (coordination du code / => beaucoup plus spécifique)
=============================
* Ilana Senape (ilana.senape@unil.ch)
	Spécialité : Documentation
* Valentin Armbruster (valentin.armbruster@unil.ch)
	Spécialité : Code
* Nada Waly (nada.waly@unl.ch)
	Spécialité : Code
* Théo Esseiva (théo.esseiva@unil.ch)
	Spécialité : Code 
* Alyssa Gheza (alyssa.gheza@unil.ch)
	Spécialité : Documentation

2. Technique
************

2.1 Dépendances
===============
* Orange 3-3.40
* Orange Textable 3.2.7
* Fork étudiant : `https://github.com/SIla25T/orange3-textable-prototypes.git`
* Diff lib (librairie intégrée à Python) 

2.2 Fonctionnalités minimales
=============================
.. image:: images/<widget>_vm1.png ##

* FM1 — Le widget doit pouvoir accepter deux inputs Text Files ou Text Field et refuser ce qui n'y correspond pas.
* FM2 — Le widget doit pouvoir comparer deux textes et sortir une liste/un tableau des différences entre les textes.
* FM3 - Le widget doit pouvoir segmenter efficacement les textes pour que la comparaison soit pertinente (gérer par difflib).  

2.3 Fonctionnalités principales
===============================
.. image:: images/<widget>_vp1.png  ##

* FP1 — Le widget peut reconnaitre le type de modification qu'a subit un texte (ajout, suppression, modification)
* FP2 — Le widget peut montrer l'endroit qui a subit une modification

2.4 Fonctionnalités optionnelles
================================
.. image:: images/<widget>_optional.png ##

* FO1 — Le widget pourrait être relié à une visualisation distribution qui permet de voir dans quelles partie du texte il y a le plus de modification en fonction d'une fenêtre de recherche
* FO2 — Le widget pourrait se moduler en fonction du type de changement chercher et de son intensité

2.5 Tests
=========
Décrire une liste de scénarios (voir capsules “Specs 3”).
Exiger au moins :
- 2–3 scénarios OK
	1) Tester qu'il y a bien deux inputs
	2) Tester que les inputs sont du bon type
	3) Tester qu'il y ait au moins une similarité entre les textes
- 2 scénarios None / entrée manquante
	1) Tester si il n'y a rien dans le fichier Text File ou Test Field => message 
	indiquant qu'il n'y a rien
	2) Si il n'y a pas d'input => message d'erreur
- 1 scénario paramètre invalide
	1) -
- 1 scénario erreur/exception (si pertinent)
	1) -

3. Étapes
*********

3.1 Version alpha
=================
* L'interface graphique est construite (même minimalement).
* Les fonctionnalités minimales sont implémentées et testables.
* Le widget est intégrable dans Orange (install -e, visible, mini workflow).

3.2 Version finale
==================
* Fonctionnalités principales complètes
* Robustesse (None, erreurs, outputs vidés correctement)
* Documentation (EN) cohérente
* Tests / scénarios de validation exécutés

4. Infrastructure
*****************

Le projet est disponible sur GitHub :
`https://github.com/SIla25T/orange3-textable-prototypes.git`

Organisation recommandée :
- `specs/TextDiff.rst`
- `doc/widgets/TextDiff.rst` (EN)
- `orangecontrib/textable_prototypes/widgets/TextDiff.py`
- `orangecontrib/textable_prototypes/widgets/icons/TextDiff.(png|svg)`
