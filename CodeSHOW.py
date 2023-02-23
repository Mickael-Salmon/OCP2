####################################################################
#           Projet 2 OpenClassrooms -                              #
#           Analysez les ventes d'un site e-commerce               #
#           Web Scraping bookstoscrape.com                         #           
####################################################################

#Importation des modules nécessaires
import requests
from bs4 import BeautifulSoup
import csv
import os
import time

#URL du site à scrapper 
url = "http://books.toscrape.com/"

# Définition d'un user agent pour simuler un navigateur Chrome Edge sur windows 10. 
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

#Création d'un menu au lancement du programme pour faciliter l'interaction avec l'utilisateur
#Pour se faire on utilise la fonction input
#On demande à l'utilisateur de choisir une action parmi les choix proposés
#On utilise la fonction strip() pour supprimer les espaces en début et fin de chaîne
#On utilise la fonction lower() pour convertir la chaîne en minuscule
#On utilise la fonction strip().lower() pour supprimer les espaces en début et fin de chaîne et convertir la chaîne en minuscule
def get_menu():
    return input("Le programme d'analyse des prix a bien démarré ! Faites un choix parmi les choix suivants : \n "
                 "1 - Récupérer les détails d'un livre par son url \n "
                 "2 - Récupérer les livres d'une catégorie sélectionnée \n "
                 "3 - Récupération de l'intégralité des livres du site \n "
                 "0 - Quitter\n "
                 " ").strip().lower()


# Pour ce choix, on part du principe que l'utilisateur connaît l'URL du livre et qu'il la saisit dans le menu
# On récupère l'URL du livre   

def get_select_url():
    return input("Veuillez saisir l'URL du livre : ").strip().lower()


# Pour ce choix, on part du principe que l'utilisateur saisit le nom de la catégorie
# On récupère le nom de la catégorie
def input_select_cat():
    return input("Veuillez saisir la catégorie à récupérer : ").strip().lower()

# Pour ce choix, on laisse à l'utilisateur le choix de télécharger ou non les images
# On récupère le choix de l'utilisateur
# La boucle while permet de valider le choix de l'utilisateur
# On retourne le choix de l'utilisateur
# Si l'utilisateur a choisi "y", alors on retourne True
# Si l'utilisateur a choisi "n", alors on retourne False
# Pour gérer le cas où l'utilisateur a fait une erreur de frappe, on utilise while not (choix == "y" or choix == "n") pour valider le choix de l'utilisateur
# On fait un print pour lui indiquer qu'il a fait une erreur 
def with_picture():
    text_picture = "Voulez-vous télécharger les images (y/n) : "
    with_picture_choice = input(text_picture).strip().lower()
    while not (with_picture_choice in allowed_with_picture):
        print("Le choix n'est pas valide")
        with_picture_choice = input(text_picture)
    # Si l'utilisateur a choisi "y", alors on retourne True
    if with_picture_choice == "y":
        with_picture = True
    # Si l'utilisateur a choisi "n", alors on retourne False
    else:
        with_picture = False
    # On retourne le choix de l'utilisateur
    return with_picture

###############################################################
# Utilisation d'un dictionnaire pour stocker les informations #
###############################################################

# Fonction pour récupérer les informations d'un livre
def key_in_dict(dictionary, key, search):
    # On récupère la clé de la valeur recherchée dans le dictionnaire si elle existe, sinon none
    return next((i for i, item in enumerate(dictionary) if item[key] == search), None)

# Fonction pour récupérer toutes les catégories du site
def get_dict_all_category():
    # site a scrapper
    # url = "http://books.toscrape.com/"
    # On récupère le contenu de la page
    # On utilise la fonction get() pour récupérer le contenu de la page
    response = requests.get(url)
    # On vérifie que la requête a bien abouti
    page = response.content
    # On parse le contenu de la page
    soup = BeautifulSoup(page, "html.parser")


    # On utilise la fonction find_all() pour récupérer toutes les catégories de la page principale
    # On utilise la fonction find() pour récupérer le lien de la catégorie
    all_category_ul = soup.find_all("ul", class_="nav-list")
    category = []

    # Boucle FOR pour récupérer toutes les catégories
    for bloc_category in all_category_ul:
        # On utilise la fonction find_all() pour récupérer toutes les catégories
        all_a_cat = bloc_category.find_all("a")
        # Boucle FOR pour récupérer toutes les catégories
        for a_info in all_a_cat:
            # On récupère le lien de la catégorie
            # On utilise la fonction strip() pour supprimer les espaces en début et fin de chaîne
            # On utilise la fonction lower() pour convertir la chaîne en minuscule
            # On utilise la fonction strip().lower() pour supprimer les espaces en début et fin de chaîne et convertir la chaîne en minuscule
            # link_cat = a_info.get("href").strip().lower()
            category.append({'nom': a_info.get_text().strip().lower(), 'url': a_info.get('href')})

  
    # On utilise la fonction pop() pour supprimer la 1ere catégorie qui est un titre
    category.pop(0)
    # On retourne le tableau des catégories + url associées
    return category


# On va charger les données dans un fichier csv
# On utilise la fonction open() pour ouvrir le fichier
# On utilise la fonction writer() pour écrire dans le fichier
# On utilise la fonction writerow() pour écrire une ligne dans le fichier
def charger_donnees(
        nom_fichier,
        en_tete,
        detail_livre
):
    # On ouvre le fichier en mode écriture
    with open(nom_fichier, 'w', encoding="utf8", newline='') as fichier_csv:
        # On utilise la fonction writer() pour écrire dans le fichier
        writer = csv.writer(fichier_csv, delimiter=',')
        # Si le fichier est vide, alors on insère l'entête
        if os.path.getsize(nom_fichier) == 0:
            writer.writerow(en_tete)
        writer.writerows([detail_livre])

# Tableau des infos produit

# Bloc de code : récupération des informations d'un livre
def get_detail_livre(url_detail_livre, with_picture=False, cat_dir=""):

    response_detail_livre = requests.get(url_detail_livre)
    page_detail_livre = response_detail_livre.content
    soup_detail_livre = BeautifulSoup(page_detail_livre, "html.parser")

    product_page_url = url_detail_livre

    
    # On utilise la fonction find() pour récupérer le titre du livre
    # On utilise la fonction get_text() pour récupérer le texte du titre du livre
    product_information = soup_detail_livre.find_all("td")

    # On utilise la fonction find() pour récupérer le titre du livre
    # On utilise la fonction get_text() pour récupérer le texte du titre du livre
    # On utilise la fonction strip() pour supprimer les espaces en début et fin de chaîne
    # On utilise la fonction lower() pour convertir la chaîne en minuscule
    # On utilise la fonction strip().lower() pour supprimer les espaces en début et fin de chaîne et convertir la chaîne en minuscule
    universal_product_code = product_information[0].get_text().strip()
    price_including_tax = product_information[3].get_text().strip()[1:]
    price_excluding_tax = product_information[2].get_text().strip()[1:]
    number_available = product_information[5].get_text().strip()

    # On retrouve le titre du livre dans la balise <H1>
    title = soup_detail_livre.find("h1").get_text().strip()
    
    product_description = soup_detail_livre.find_all('p')[3].get_text().strip()

    # La catégorie est dans le breadcrumb trail (fil d'ariane)
    # On utilise donc une série de <a href> pour retrouver la catégorie
    category = soup_detail_livre.find_all("a")[3].get_text().strip()

    # On utilise la fonction find() pour récupérer la note du livre
    # Ici on a une classe (star_rating) et la balise <p> qui contient la note
    review_rating = soup_detail_livre.find('p', class_="star-rating").get('class')[1]

    # l'URL de l'image n'est pas absolue et commence par ../..
    # Il va donc falloir construire une REGEX 
    # donc on les retire et on concatène avec l'URL du site pour avoir l'URL complete

    # On utilise la fonction find() pour récupérer l'image du livre
    # On utilise la fonction get() pour récupérer l'attribut src de l'image
    image_url = url + soup_detail_livre.find('img').get('src')[6:]

    if with_picture:
        name_picture = title.lower()
        char_replace = "!#$%^&*()?,': ’“\\/\"."
        for char in char_replace:
            name_picture = name_picture.replace(char, "_")

        if cat_dir != "":
            name_picture = cat_dir + "/pictures/" + name_picture


        picture = requests.get(image_url)
        with open(name_picture + ".jpg", 'wb') as f:
            f.write(picture.content)
            f.close()

    data_return = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                   number_available, product_description, category, review_rating, image_url]
    return data_return


    # IF pour vérifier si on veut télécharger l'image

    if with_picture:
        name_picture = title.lower()
        # On utilise la fonction replace() pour remplacer les espaces par des tirets
        # On utilise la fonction replace() pour remplacer les caractères spéciaux par des tirets
        # On utilise la fonction replace() pour remplacer les caractères accentués par des tirets
        # On utilise la fonction replace() pour remplacer les tirets par des tirets
        char_replace = "!#$%^&*()?,': ’“\\/\"."
        for char in char_replace:
            name_picture = name_picture.replace(char, "_")
        if cat_dir != "":
            name_picture = cat_dir + "/pictures/" + name_picture

            name_picture = "pictures/" + name_picture
        f = open(name_picture + ".jpg", "wb")
        picture = requests.get(image_url)
        f.write(picture.content)
        f.close()
    # On retourne le tableau des infos produit
    data_return = [product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                   number_available, product_description, category, review_rating, image_url]
    # TEST print(data_return)
    return data_return


# Bloc de code : livres par catégorie 
def get_list_book_by_category(category_url, link=None, page="index.html"):

    reponse_category_par_page = requests.get(category_url + page)
    page_category_par_page = reponse_category_par_page.content
    soup_category_par_page = BeautifulSoup(page_category_par_page, "html.parser")

    all_link_livre = soup_category_par_page.find_all("div", class_="image_container")
# IF Statement pour vérifier si on a un lien
    if link is None:
        link = []
    # On utilise la fonction find_all() pour récupérer tous les liens
    # On utilise la fonction get() pour récupérer l'attribut href de chaque lien
    # On utilise la fonction append() pour ajouter chaque lien dans le tableau
    for bloc_link_livre in all_link_livre:
        all_a_livre = bloc_link_livre.find_all("a")
        for link_livre in all_a_livre:
            link.append(url + 'catalogue/' + link_livre.get('href')[9:])
    # On utilise la fonction find() pour récupérer le lien vers la page suivante

    have_pagination = soup_category_par_page.find_all("li", class_="next")
    if have_pagination:
        for link_pagination in have_pagination:
            a_pagination = link_pagination.find_all("a")
            url_pagination = a_pagination[0].get('href')
            # On rappelle la fonction dans laquelle et s'il y a une page suivante et on rajoute les livres à la suite
            link = get_list_book_by_category(category_url, link, url_pagination)
    # 
    return link

# Bloc de code : récupération de tous les détails des livres
def get_all_book_detail(category_dict, with_picture=False):

    for category in category_dict:
        url_category_split = category['url'][:-10]
        category_url = url + url_category_split

        all_link_livre = get_list_book_by_category(category_url)
        cat_dir = category["nom"].strip().replace(" ", "_").lower()
        if not os.path.exists(cat_dir):
            os.makedirs(cat_dir)
        if with_picture and not os.path.exists(cat_dir + "/pictures"):
            os.makedirs(cat_dir + "/pictures")
        with open(cat_dir + '/' + category["nom"] + ".csv", 'w', encoding="utf8", newline='') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            # Si le fichier est vide, alors on met l'entête
            if os.path.getsize(cat_dir + '/' + category["nom"] + ".csv") == 0:
                writer.writerow(en_tete)
            for link_livre in all_link_livre:
                writer.writerows([get_detail_livre(link_livre, with_picture, cat_dir)])

if __name__ == "__main__":

    url_choice = ""

    # entête du fichier CSV
    en_tete = [
        "product_page_url",
        "universal_product_code (upc)",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url"
    ]

    # On gère le choix du menu principal
    allowed_menu_choice = ["1", "2", "3", "0"]
    allowed_with_picture = ["y", "n"]

    menu_choice = get_menu()
    index_cat_in_dict = None

    # Tant que le choix est invalide, on demande de ressaisir
    while not(menu_choice in allowed_menu_choice):
        print("Le choix n'est pas valide")
        menu_choice = get_menu()

    if menu_choice == "1":
        url_choice = get_select_url()
        test_url = requests.get(url_choice)
        while test_url.status_code != 200:
            print("URL invalide")
            url_choice = get_select_url()
            test_url = requests.get(url_choice)

        with_picture = with_picture()

        detail_livre = get_detail_livre(url_choice, with_picture, "")
        charger_donnees("detail_livre.csv", en_tete, detail_livre)

    elif menu_choice == "2":
        # On récupère un dictionnaire de toutes les catégories
        all_category = get_dict_all_category()
        # On affiche l'input de selection de la catégorie
        cat_select = input_select_cat()
        # On récupère la clé de la catégorie recherchée dans le dictionnaire de toutes les catégories, sinon None
        index_cat_in_dict = key_in_dict(all_category, "nom", cat_select)

        # Tant qu'on n'a pas de clé trouvée, on redemande de saisir la catégorie, jusqu'a en avoir une valide
        while index_cat_in_dict is None:
            print("La catégorie saisie n'existe pas")
            cat_select = input_select_cat()
            index_cat_in_dict = key_in_dict(all_category, "nom", cat_select)

        with_picture = with_picture()

        get_all_book_detail([all_category[index_cat_in_dict]], with_picture)

    elif menu_choice == "3":
        # On récupère un dictionnaire de toutes les catégories
        all_category = get_dict_all_category()

        with_picture = with_picture()

        get_all_book_detail(all_category, with_picture)

    elif menu_choice == "0":
        exit()