"""
📁 Utilitaires pour la gestion des fichiers avec pathlib moderne
"""
import csv
import re
from pathlib import Path
from typing import List, Dict, Any

import aiofiles
import requests
from rich.console import Console

console = Console()


class FileHandler:
    """Gestionnaire de fichiers modernisé."""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Nettoie un nom de fichier pour le rendre valide sur le système."""
        # Caractères à remplacer
        invalid_chars = r'[<>:"/\\|?*\']'
        # Remplace les caractères invalides par des underscores
        sanitized = re.sub(invalid_chars, '_', filename)
        # Limite la longueur
        return sanitized[:200]  # Max 200 caractères
    
    @staticmethod
    def create_directory(path: Path) -> bool:
        """Crée un répertoire s'il n'existe pas."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            console.print(f"[red]❌ Erreur création du dossier {path}: {e}[/red]")
            return False
    
    @staticmethod
    def save_books_to_csv(books: List[Dict[str, Any]], output_path: Path) -> bool:
        """Sauvegarde une liste de livres en CSV."""
        if not books:
            console.print("[yellow]⚠️ Aucun livre à sauvegarder[/yellow]")
            return False
        
        try:
            # S'assure que le répertoire parent existe
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # En-têtes CSV
            headers = [
                "product_page_url",
                "universal_product_code",
                "title", 
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url"
            ]
            
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(books)
            
            console.print(f"✅ [green]{len(books)} livres sauvegardés dans {output_path}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Erreur sauvegarde CSV {output_path}: {e}[/red]")
            return False
    
    @staticmethod
    def save_image(image_url: str, output_path: Path) -> bool:
        """Télécharge et sauvegarde une image."""
        try:
            # S'assure que le répertoire parent existe
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ Erreur téléchargement image {image_url}: {e}[/red]")
            return False
    
    @staticmethod
    async def save_image_async(session, image_url: str, output_path: Path) -> bool:
        """Télécharge et sauvegarde une image de manière asynchrone."""
        try:
            # S'assure que le répertoire parent existe
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with session.get(image_url) as response:
                if response.status == 200:
                    async with aiofiles.open(output_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    return True
                    
        except Exception as e:
            console.print(f"[red]❌ Erreur téléchargement async image {image_url}: {e}[/red]")
        return False


# Fonction utilitaire pour compatibilité
def save_image(image_url: str, output_path: Path) -> bool:
    """Fonction utilitaire pour sauvegarder une image."""
    return FileHandler.save_image(image_url, output_path)
