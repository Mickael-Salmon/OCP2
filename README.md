# 📚 BookStore Scraper 2.0 - Version Moderne

<div align="center">

**Projet 2 OpenClassrooms** - [Développeur d'application - Python](https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python) 👋

*Scraper moderne avec interface Rich pour l'analyse de prix de livres*

</div>

---

## 🚀 Features modernisées

- **🎨 Interface Rich** : Couleurs, tableaux, barres de progression animées
- **⚡ CLI avec Typer** : Commandes simplifiées et options faciles
- **🔧 Architecture modulaire** : Code refactorisé en packages Python
- **📊 Gestion d'erreurs robuste** : Meilleure stabilité et fiabilité
- **🖼️ Téléchargement d'images** : Support asynchrone pour les images
- **💾 Export CSV amélioré** : Données structurées avec pathlib moderne

---

## 📋 Scénario

Vous êtes analyste marketing chez Books Online, une importante librairie en ligne spécialisée dans les livres d'occasion. Dans le cadre de vos fonctions, vous essayez de suivre manuellement les prix des livres d'occasion sur les sites web de vos concurrents, mais cela représente trop de travail et vous n'arrivez pas à y faire face : il y a trop de livres et trop de librairies en ligne ! 

Vous et votre équipe avez décidé d'automatiser cette tâche laborieuse via un programme (un scraper) développé en Python, capable d'extraire les informations tarifaires d'autres librairies en ligne.

<p align="center">
<img src="https://user.oc-static.com/upload/2020/09/22/1600779540759_Online%20bookstore-01.png" alt="BookStore Analysis">
</p>

---

## 🛠️ Installation et démarrage

### Prérequis
- Python 3.10+ 
- Git

### 1. Récupération du projet

```bash
# Clonez le projet depuis votre dépôt Git
git clone https://github.com/votre-username/bookstore-scraper.git
cd bookstore-scraper
```

### 2. Configuration de l'environnement

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate        # Pour Bash/Zsh
source venv/bin/activate.fish   # Pour Fish
venv\Scripts\activate           # Pour Windows

# Installer les dépendances
pip install -r Requirements.txt
```

---

## 🎯 Utilisation

### Mode interactif (Recommandé)

```bash
# Lancez le mode interactif avec une belle interface
python main.py interactive
```

**Fonctionnalités disponibles :**
- 🔍 **Analyser un livre** par son URL
- 📚 **Analyser une catégorie** spécifique
- 🌍 **Analyser tout le site** (attention: très long!)
- 🖼️ **Option de téléchargement d'images**

### Commandes directes

```bash
# Analyse un livre spécifique
python main.py single "http://books.toscrape.com/catalogue/book-url/"

# Analyse une catégorie par nom
python main.py category --name "Poetry" --images

# Analyse toutes les catégories (très long!)
python main.py all --output data/ --images
```

### Options disponibles

- `--output, -o` : Dossier de sortie (défaut: `output/`)
- `--images, -i` : Télécharger les images des livres
- `--name, -n` : Nom de la catégorie (pour la commande category)

---

## 📁 Structure des résultats

```
output/
├── poetry/                    # Catégorie
│   ├── poetry.csv            # Données des livres
│   └── images/               # Images (si option activée)
│       ├── Book_Title_1.jpg
│       └── Book_Title_2.jpg
├── fiction/
│   ├── fiction.csv
│   └── images/
└── ...
```

### Format CSV

Chaque fichier CSV contient les colonnes suivantes :
- `product_page_url` : URL de la page produit
- `universal_product_code` : Code UPC
- `title` : Titre du livre
- `price_including_tax` : Prix TTC
- `price_excluding_tax` : Prix HT
- `number_available` : Disponibilité
- `product_description` : Description
- `category` : Catégorie
- `review_rating` : Note (étoiles)
- `image_url` : URL de l'image

---

## 🏗️ Architecture moderne

```
src/
├── bookstore_scraper/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── book.py              # Modèles de données
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_handler.py      # Gestion fichiers
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py              # Interface CLI
│   └── scraper.py               # Logique de scraping
├── main.py                      # Point d'entrée
└── Requirements.txt             # Dépendances
```

---

## 🎨 Captures d'écran

L'interface Rich offre une expérience utilisateur moderne avec :

- 🎯 **Menu interactif** avec tableaux colorés
- ⠋ **Barres de progression** animées en temps réel
- ✅ **Messages de statut** colorés et informatifs
- 📊 **Tableaux de résultats** bien formatés
- 🏷️ **Navigation facile** par catégories

---

## 🔧 Développement

### Structure modulaire

Le code est organisé en modules séparés pour une meilleure maintenabilité :

- **Models** : Classes de données avec type hints
- **Scraper** : Logique d'extraction avec gestion d'erreurs
- **Utils** : Utilitaires pour fichiers et images
- **CLI** : Interface utilisateur avec Rich et Typer

### Technologies utilisées

- **Requests** : Requêtes HTTP
- **BeautifulSoup4** : Parsing HTML
- **Rich** : Interface terminal moderne
- **Typer** : CLI framework
- **Pathlib** : Gestion moderne des chemins
- **Type hints** : Code plus robuste

---

## 📋 Livrables du projet

1. **Repository GitHub** public contenant :
   - L'ensemble du code d'application modernisé
   - Le fichier `Requirements.txt` 
   - Ce README.md avec instructions complètes
   - Structure modulaire organisée

2. **Fichier ZIP** avec toutes les données extraites et images

3. **Email PDF** au responsable décrivant le pipeline ETL

---

## 🤝 Support

Pour toute question, suggestion ou rapport de bug :

- 📧 **Email** : votre.email@example.com
- 🐛 **Issues** : Utilisez les issues GitHub
- 📚 **Documentation** : Consultez ce README

---

## 📜 Licence

Projet éducatif OpenClassrooms - Tous droits réservés

---

<div align="center">

**Made with ❤️ and modern Python**

*BookStore Scraper 2.0 - Une interface terminal qui fait plaisir à utiliser !*

</div>
