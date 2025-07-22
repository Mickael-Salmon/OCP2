
<h3 align="center">

📚 BookStore Scraper 2.0 - Version Moderne

Bienvenue ! Vous trouverez ici le Projet 2 du parcours<a href="https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python" target="_blank" rel="noreferrer"> Développeur d'application - Python</a> 👋


**[BookStore Scraper 2.0](#)** est une application modernisée qui analyse les prix de livres en ligne en utilisant
Python, Rich pour de belles interfaces en terminal, et Typer pour des commandes simples et efficaces.

</h3>

<h2 align="center">

# Utilisez les bases de Python pour l'analyse de marché 💻 !

</h2>

> Scénario 💬 
> ###  

### Features modernisées :

- **Interface Rich** : Couleurs, tableaux, progression visuelle
- **CLI avec Typer** : Commandes simplifiées et options faciles
- **Scraping asynchrone** : Pour une rapidité accrue
- **Modularité** : Code refactorisé en modules et packages

---

### Scénario 🎯



<p align="center" href="" class="oc-imageLink oc-imageLink--disabled"><img src="https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png"></p>


</br>
> Livrables attendus 🔭  
> ##   

1.  Un document TXT ou PDF contenant le lien vers le **repository GitHub** public qui doit contenir les éléments suivants:

-   l'ensemble de votre code d'application ;
-   le fichier requirements.txt, mais pas l'environnement virtuel lui-même ;
-   un fichier README.md expliquant comment créer et activer l'environnement virtuel, puis exécuter le code d'application ;
-   les données/images extraites ne doivent pas faire partie du repository lui-même.

3.  Un fichier compressé ZIP contenant toute la **data** : les **données extraites et les images associées** dans un format ou une structure facile à suivre.
4.  Un **mail** (pas plus d’une page) **au responsable d’équipe**, Sam, décrivant comment l’application permet d’établir un pipeline ETL, au format PDF.

</br>


<h2> Installation et démarrage du projet</h2> 

### Récupération du projet et préparation

#### Cloner le dépôt

```bash
# Clonez le projet depuis votre dépôt Git
$ git clone https://github.com/MicSa/public/
$ cd public
```

#### Créer un environnement virtuel et installer les dépendances

```bash
# Créer l'environnement virtuel
$ python -m venv venv

# Activer l'environnement virtuel
$ source venv/bin/activate # pour Bash
$ source venv/bin/activate.fish # pour Fish
$ venv\\Scripts\\activate # pour Windows

# Installer les dépendances
$ pip install -r Requirements.txt
```

### Utilisation

#### Lancer le programme interactif

```bash
# Lancez le mode interactif
$ venv/bin/python main.py interactive
```

Vous pouvez choisir plusieurs options interactives pour scraper et analyser les données :

- Analyser un livre par URL
- Analyser une catégorie
- Analyser l'ensemble du site

Les résultats sont sauvegardés dans le dossier `output/`.

#### Commandes directes

Vous pouvez aussi utiliser les commandes directes pour plus de contrôle :

```bash
# Analyse un livre
$ venv/bin/python main.py single <url_du_livre>

# Analyse une catégorie
$ venv/bin/python main.py category --name Fiction

# Analyse tout le site (cela peut être très long)
$ venv/bin/python main.py all
```

### Version Python recommandée

- Python 3.10+

### Contact et support

Pour toute question ou rapport de bugs, veuillez contacter mic@example.com.

---

<h3>Récupération du projet</h3> 

$ git clone https://github.com/MicSa/public/

<h3>Activer l'environnement virtuel </h3> 

#### Création de l'environnement virtuel 

```cd public```
```python -m venv env```
```source env/bin/activate```

#### Installation des packages/modules 

```pip install -r requirements.txt```

### Utilisation
Lancer le script ```codeSHOW.py```

4 options sont proposées : 
- Télécharger par URL
- Télécharger par catégorie 
- Télécharger l'intégralité
- Quitter

Les fichiers csv sont ouvrables avec un tableaur.

### Version Python 
Python 3.10.9 (main, Dec 19 2022, 17:35:49) [GCC 12.2.0] on linux

<h2>MacOS et Linux : </h2>

#### Création de l'environnement virtuel 

```cd public```
```python -m venv env```
```source env/bin/activate```

#### Installation des packages/modules 

```pip install -r requirements.txt```

### Utilisation
Lancer le script ```codeSHOW.py```

4 options sont proposées : 
- Télécharger par URL
- Télécharger par catégorie 
- Télécharger l'intégralité
- Quitter

Les fichiers csv sont ouvrables avec un tableaur.

### Version Python 
Python 3.10.9 (main, Dec 19 2022, 17:35:49) [GCC 12.2.0] on linux
<h3>Lancer le programme </h3>

$ python ```codeSHOW.py```
