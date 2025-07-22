"""
📖 Modèle de données pour représenter un livre
"""
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Book:
    """Représente un livre avec toutes ses informations."""
    
    product_page_url: str
    universal_product_code: str
    title: str
    price_including_tax: Decimal
    price_excluding_tax: Decimal
    number_available: int
    product_description: str
    category: str
    review_rating: str
    image_url: str
    
    def __post_init__(self):
        """Validation et conversion des données après initialisation."""
        # Convertir les prix en Decimal si ce sont des strings
        if isinstance(self.price_including_tax, str):
            # Supprimer le symbole monétaire et convertir
            price_str = self.price_including_tax.replace('£', '').replace('€', '').replace('$', '')
            self.price_including_tax = Decimal(price_str)
            
        if isinstance(self.price_excluding_tax, str):
            price_str = self.price_excluding_tax.replace('£', '').replace('€', '').replace('$', '')
            self.price_excluding_tax = Decimal(price_str)
    
    @property
    def formatted_price_inc_tax(self) -> str:
        """Prix TTC formaté."""
        return f"£{self.price_including_tax:.2f}"
    
    @property
    def formatted_price_exc_tax(self) -> str:
        """Prix HT formaté."""
        return f"£{self.price_excluding_tax:.2f}"
    
    @property
    def availability_number(self) -> int:
        """Extrait le nombre de livres disponibles."""
        if isinstance(self.number_available, str):
            # Extrait le nombre de "In stock (XX available)"
            import re
            match = re.search(r'\((\d+) available\)', self.number_available)
            return int(match.group(1)) if match else 0
        return self.number_available
    
    def to_dict(self) -> dict:
        """Convertit le livre en dictionnaire pour export CSV."""
        return {
            'product_page_url': self.product_page_url,
            'universal_product_code': self.universal_product_code,
            'title': self.title,
            'price_including_tax': str(self.price_including_tax),
            'price_excluding_tax': str(self.price_excluding_tax),
            'number_available': self.number_available,
            'product_description': self.product_description,
            'category': self.category,
            'review_rating': self.review_rating,
            'image_url': self.image_url
        }


@dataclass
class Category:
    """Représente une catégorie de livres."""
    
    nom: str
    url: str
    
    @property
    def safe_name(self) -> str:
        """Nom sécurisé pour créer des dossiers/fichiers."""
        return self.nom.strip().replace(" ", "_").lower()
