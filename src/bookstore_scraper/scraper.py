"""
🔍 Scraper principal modernisé avec support asynchrone et gestion d'erreurs robuste
"""
import asyncio
import re
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import aiohttp
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, TaskID

from .models.book import Book, Category
from .utils.file_handler import save_image

console = Console()


class BookStoreScraper:
    """Scraper moderne pour books.toscrape.com avec interface Rich."""
    
    def __init__(self, base_url: str = "http://books.toscrape.com/"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_all_categories(self) -> List[Category]:
        """Récupère toutes les catégories disponibles sur le site."""
        console.print("🔍 [bold cyan]Récupération des catégories...[/bold cyan]")
        
        try:
            response = self.session.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            categories = []
            
            # Trouve toutes les catégories dans la navigation
            nav_list = soup.find("ul", class_="nav-list")
            if not nav_list:
                console.print("[red]❌ Impossible de trouver la liste des catégories[/red]")
                return []
            
            links = nav_list.find_all("a")
            
            for link in links[1:]:  # Skip le premier qui est "Books"
                category_name = link.get_text().strip()
                category_url = link.get('href')
                
                if category_name and category_url:
                    categories.append(Category(
                        nom=category_name.lower(),
                        url=category_url
                    ))
            
            console.print(f"✅ [green]{len(categories)} catégories trouvées[/green]")
            return categories
            
        except requests.RequestException as e:
            console.print(f"[red]❌ Erreur lors de la récupération des catégories: {e}[/red]")
            return []
    
    def get_book_details(self, book_url: str) -> Optional[Book]:
        """Récupère les détails d'un livre à partir de son URL."""
        try:
            response = self.session.get(book_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extraction des informations produit
            product_info = soup.find_all("td")
            if len(product_info) < 6:
                console.print(f"[yellow]⚠️ Informations incomplètes pour {book_url}[/yellow]")
                return None
            
            # Extraction des données
            upc = product_info[0].get_text().strip()
            price_exc_tax = product_info[2].get_text().strip()[1:]  # Remove £
            price_inc_tax = product_info[3].get_text().strip()[1:]  # Remove £ 
            availability = product_info[5].get_text().strip()
            
            # Titre
            title_elem = soup.find("h1")
            title = title_elem.get_text().strip() if title_elem else "Titre inconnu"
            
            # Description
            description_elem = soup.find("article", class_="product_page")
            description = ""
            if description_elem:
                desc_paragraphs = description_elem.find_all('p')
                if len(desc_paragraphs) >= 4:
                    description = desc_paragraphs[3].get_text().strip()
            
            # Catégorie depuis le breadcrumb
            breadcrumb = soup.find("ul", class_="breadcrumb")
            category = "Unknown"
            if breadcrumb:
                links = breadcrumb.find_all("a")
                if len(links) >= 3:
                    category = links[2].get_text().strip()
            
            # Rating
            rating_elem = soup.find('p', class_="star-rating")
            rating = rating_elem.get('class')[1] if rating_elem else "Unknown"
            
            # Image URL
            img_elem = soup.find('img')
            image_url = ""
            if img_elem:
                img_src = img_elem.get('src', '')
                if img_src.startswith('../..'):
                    image_url = urljoin(self.base_url, img_src[6:])
                else:
                    image_url = urljoin(self.base_url, img_src)
            
            return Book(
                product_page_url=book_url,
                universal_product_code=upc,
                title=title,
                price_including_tax=price_inc_tax,
                price_excluding_tax=price_exc_tax,
                number_available=availability,
                product_description=description,
                category=category,
                review_rating=rating,
                image_url=image_url
            )
            
        except requests.RequestException as e:
            console.print(f"[red]❌ Erreur lors du scraping de {book_url}: {e}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]❌ Erreur inattendue pour {book_url}: {e}[/red]")
            return None
    
    def get_books_from_category(self, category: Category) -> List[str]:
        """Récupère tous les liens des livres d'une catégorie (avec pagination)."""
        book_links = []
        
        # Construction de l'URL de base pour la catégorie
        category_base_url = urljoin(self.base_url, category.url[:-10])  # Remove index.html
        
        page = 1
        
        while True:
            # URL de la page courante
            if page == 1:
                page_url = urljoin(category_base_url, "index.html")
            else:
                page_url = urljoin(category_base_url, f"page-{page}.html")
            
            try:
                response = self.session.get(page_url)
                
                # Si la page n'existe pas, on s'arrête
                if response.status_code == 404:
                    break
                    
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Trouve tous les conteneurs d'images (qui contiennent les liens)
                book_containers = soup.find_all("div", class_="image_container")
                
                if not book_containers:
                    break
                
                # Extrait les liens des livres
                for container in book_containers:
                    link_elem = container.find("a")
                    if link_elem:
                        book_link = link_elem.get('href')
                        if book_link:
                            # Construit l'URL complète
                            if book_link.startswith('../../../'):
                                full_url = urljoin(self.base_url, 'catalogue/' + book_link[9:])
                            else:
                                full_url = urljoin(self.base_url, book_link)
                            book_links.append(full_url)
                
                # Vérifie s'il y a une page suivante
                next_button = soup.find("li", class_="next")
                if not next_button:
                    break
                    
                page += 1
                
            except requests.RequestException as e:
                console.print(f"[red]❌ Erreur page {page} de {category.nom}: {e}[/red]")
                break
        
        return book_links
    
    async def download_image_async(self, session: aiohttp.ClientSession, 
                                  image_url: str, file_path: Path) -> bool:
        """Télécharge une image de manière asynchrone."""
        try:
            async with session.get(image_url) as response:
                if response.status == 200:
                    content = await response.read()
                    file_path.write_bytes(content)
                    return True
        except Exception as e:
            console.print(f"[red]❌ Erreur téléchargement image: {e}[/red]")
        return False
