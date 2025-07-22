#!/usr/bin/env python3
"""
🚀 Point d'entrée principal du scraper modernisé
BookStore Scraper 2.0 - Interface Rich moderne
"""
import sys
from pathlib import Path

# Ajoute le répertoire src au PYTHONPATH pour les imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bookstore_scraper.cli.main import app

if __name__ == "__main__":
    app()
