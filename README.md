# public
### Scénario

Vous êtes analyste marketing chez Books Online, une importante librairie en ligne spécialisée dans les livres d'occasion. Dans le cadre de vos fonctions, vous essayez de suivre manuellement les prix des livres d'occasion sur les sites web de vos concurrents, mais cela représente trop de travail et vous n'arrivez pas à y faire face : il y a trop de livres et trop de librairies en ligne ! Vous et votre équipe avez décidé d'automatiser cette tâche laborieuse via un programme (un scraper) développé en Python, capable d'extraire les informations tarifaires d'autres librairies en ligne.

### Livrables

   Un document TXT ou PDF contenant le lien vers le **repository GitHub** public qui doit contenir les éléments suivants:

-   l'ensemble de votre code d'application 
-   le fichier requirements.txt, mais pas l'environnement virtuel lui-même 
-   un fichier README.md expliquant comment créer et activer l'environnement virtuel, puis exécuter le code d'application 
-   les données/images extraites ne doivent pas faire partie du repository lui-même.

  Un fichier compressé ZIP contenant toute la **data** : les **données extraites et les images associées** dans un format ou une structure facile à suivre.
  Un **mail** (pas plus d’une page) **au responsable d’équipe**, Sam, décrivant comment l’application permet d’établir une pipeline ETL, au format PDF.

#### Création de l'environnement virtuel 

cd public
python -m venv env
source env/bin/activate

#### Installation des packages/modules 

pip install -r requirements.txt

### Utilisation
Lancer le script codeSHOW.py

4 options sont proposées : 
- Télécharger par URL
- Télécharger par catégorie 
- Télécharger l'intégralité
- Quitter

Les fichiers csv sont ouvrables avec un tableaur.

### Version Python 
Python 3.10.9 (main, Dec 19 2022, 17:35:49) [GCC 12.2.0] on linux
