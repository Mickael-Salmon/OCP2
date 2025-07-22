"""
🎨 Interface CLI moderne avec Typer et Rich
"""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

from ..scraper import BookStoreScraper
from ..utils.file_handler import FileHandler, save_image

# Configuration de l'application Typer
app = typer.Typer(
    name="bookstore-scraper",
    help="🔍 Scraper moderne pour analyser les prix de livres sur books.toscrape.com",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()


def display_banner():
    """Affiche la bannière de bienvenue avec Rich."""
    banner = Panel.fit(
        Text("📚 BookStore Scraper 2.0", style="bold cyan", justify="center"),
        subtitle="Analyse moderne des prix de livres",
        style="blue"
    )
    console.print(banner)


def display_categories(categories):
    """Affiche la liste des catégories dans un tableau Rich."""
    table = Table(title="🏷️ Catégories disponibles")
    table.add_column("Nom", style="cyan", no_wrap=True)
    table.add_column("ID", style="magenta")
    
    for i, category in enumerate(categories, 1):
        table.add_row(category.nom.title(), str(i))
    
    console.print(table)


@app.command("single")
def scrape_single_book(
    url: str = typer.Argument(..., help="URL du livre à analyser"),
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Dossier de sortie"),
    download_images: bool = typer.Option(False, "--images", "-i", help="Télécharger les images")
):
    """🔍 Analyse un livre unique à partir de son URL."""
    display_banner()
    
    console.print(f"🔍 [bold cyan]Analyse du livre: {url}[/bold cyan]")
    
    scraper = BookStoreScraper()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("📖 Extraction des données...", total=None)
        
        book = scraper.get_book_details(url)
        
        if not book:
            console.print("[red]❌ Impossible de récupérer les informations du livre[/red]")
            raise typer.Exit(1)
        
        progress.update(task, description="💾 Sauvegarde en cours...")
        
        # Création du dossier de sortie
        FileHandler.create_directory(output)
        
        # Sauvegarde en CSV
        csv_path = output / "single_book.csv"
        FileHandler.save_books_to_csv([book.to_dict()], csv_path)
        
        # Téléchargement de l'image si demandé
        if download_images and book.image_url:
            img_dir = output / "images"
            FileHandler.create_directory(img_dir)
            
            img_filename = FileHandler.sanitize_filename(book.title) + ".jpg"
            img_path = img_dir / img_filename
            
            progress.update(task, description="🖼️ Téléchargement image...")
            save_image(book.image_url, img_path)
    
    # Affichage des résultats
    result_table = Table(title="📊 Résultats de l'analyse")
    result_table.add_column("Propriété", style="cyan")
    result_table.add_column("Valeur", style="green")
    
    result_table.add_row("Titre", book.title)
    result_table.add_row("Prix TTC", book.formatted_price_inc_tax)
    result_table.add_row("Prix HT", book.formatted_price_exc_tax)
    result_table.add_row("Catégorie", book.category)
    result_table.add_row("Note", book.review_rating)
    result_table.add_row("Disponibilité", str(book.availability_number))
    
    console.print(result_table)
    console.print(f"✅ [green]Données sauvegardées dans: {csv_path}[/green]")


@app.command("category")
def scrape_category(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Dossier de sortie"),
    download_images: bool = typer.Option(False, "--images", "-i", help="Télécharger les images"),
    category_name: Optional[str] = typer.Option(None, "--name", "-n", help="Nom de la catégorie")
):
    """📚 Analyse tous les livres d'une catégorie spécifique."""
    display_banner()
    
    scraper = BookStoreScraper()
    
    # Récupération des catégories
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("🔍 Récupération des catégories...", total=None)
        categories = scraper.get_all_categories()
    
    if not categories:
        console.print("[red]❌ Aucune catégorie trouvée[/red]")
        raise typer.Exit(1)
    
    # Sélection de la catégorie
    if category_name:
        selected_category = next((cat for cat in categories if cat.nom == category_name.lower()), None)
        if not selected_category:
            console.print(f"[red]❌ Catégorie '{category_name}' non trouvée[/red]")
            display_categories(categories)
            raise typer.Exit(1)
    else:
        display_categories(categories)
        
        while True:
            choice = Prompt.ask("Choisissez une catégorie (numéro ou nom)", default="1")
            
            # Essaie d'interpréter comme un numéro
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    selected_category = categories[idx]
                    break
            except ValueError:
                # Essaie d'interpréter comme un nom
                selected_category = next((cat for cat in categories if cat.nom == choice.lower()), None)
                if selected_category:
                    break
            
            console.print("[red]❌ Choix invalide[/red]")
    
    console.print(f"📚 [bold cyan]Catégorie sélectionnée: {selected_category.nom.title()}[/bold cyan]")
    
    # Récupération des liens des livres
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("🔗 Récupération des liens...", total=None)
        book_links = scraper.get_books_from_category(selected_category)
    
    if not book_links:
        console.print("[red]❌ Aucun livre trouvé dans cette catégorie[/red]")
        raise typer.Exit(1)
    
    console.print(f"📖 [green]{len(book_links)} livres trouvés[/green]")
    
    # Scraping des livres
    books_data = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("📖 Extraction des données...", total=len(book_links))
        
        for i, book_url in enumerate(book_links):
            book = scraper.get_book_details(book_url)
            if book:
                books_data.append(book.to_dict())
                
                # Téléchargement d'image si demandé
                if download_images and book.image_url:
                    img_dir = output / selected_category.safe_name / "images"
                    FileHandler.create_directory(img_dir)
                    
                    img_filename = FileHandler.sanitize_filename(book.title) + ".jpg"
                    img_path = img_dir / img_filename
                    save_image(book.image_url, img_path)
            
            progress.update(task, advance=1, description=f"📖 Livre {i+1}/{len(book_links)}")
    
    # Sauvegarde
    cat_dir = output / selected_category.safe_name
    FileHandler.create_directory(cat_dir)
    
    csv_path = cat_dir / f"{selected_category.safe_name}.csv"
    FileHandler.save_books_to_csv(books_data, csv_path)
    
    console.print(f"✅ [green]{len(books_data)} livres sauvegardés dans: {csv_path}[/green]")


@app.command("all")
def scrape_all_books(
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Dossier de sortie"),
    download_images: bool = typer.Option(False, "--images", "-i", help="Télécharger les images")
):
    """🌍 Analyse TOUS les livres du site (attention: très long!)."""
    display_banner()
    
    if not Confirm.ask("⚠️ Cette opération peut prendre plusieurs heures. Continuer?"):
        raise typer.Exit()
    
    scraper = BookStoreScraper()
    
    # Récupération des catégories
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("🔍 Récupération des catégories...", total=None)
        categories = scraper.get_all_categories()
    
    if not categories:
        console.print("[red]❌ Aucune catégorie trouvée[/red]")
        raise typer.Exit(1)
    
    console.print(f"📚 [green]{len(categories)} catégories à traiter[/green]")
    
    # Traitement de toutes les catégories
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        main_task = progress.add_task("🏷️ Catégories", total=len(categories))
        
        for category in categories:
            progress.update(main_task, description=f"📚 {category.nom.title()}")
            
            # Récupère les livres de la catégorie
            book_links = scraper.get_books_from_category(category)
            
            if book_links:
                books_data = []
                book_task = progress.add_task(f"  📖 Livres de {category.nom}", total=len(book_links))
                
                for book_url in book_links:
                    book = scraper.get_book_details(book_url)
                    if book:
                        books_data.append(book.to_dict())
                        
                        # Images si demandé
                        if download_images and book.image_url:
                            img_dir = output / category.safe_name / "images"
                            FileHandler.create_directory(img_dir)
                            
                            img_filename = FileHandler.sanitize_filename(book.title) + ".jpg"
                            img_path = img_dir / img_filename
                            save_image(book.image_url, img_path)
                    
                    progress.update(book_task, advance=1)
                
                # Sauvegarde de la catégorie
                cat_dir = output / category.safe_name
                FileHandler.create_directory(cat_dir)
                
                csv_path = cat_dir / f"{category.safe_name}.csv"
                FileHandler.save_books_to_csv(books_data, csv_path)
                
                progress.remove_task(book_task)
            
            progress.update(main_task, advance=1)
    
    console.print("✅ [green]Scraping complet terminé![/green]")


@app.command("interactive")
def interactive_mode():
    """🎮 Mode interactif avec menu."""
    display_banner()
    
    while True:
        console.print("\\n[bold cyan]🎯 Que souhaitez-vous faire ?[/bold cyan]")
        
        choices_table = Table()
        choices_table.add_column("Option", style="magenta")
        choices_table.add_column("Description", style="cyan")
        
        choices_table.add_row("1", "🔍 Analyser un livre (URL)")
        choices_table.add_row("2", "📚 Analyser une catégorie")
        choices_table.add_row("3", "🌍 Analyser tout le site")
        choices_table.add_row("0", "❌ Quitter")
        
        console.print(choices_table)
        
        choice = Prompt.ask("Votre choix", choices=["0", "1", "2", "3"], default="1")
        
        if choice == "0":
            console.print("👋 [yellow]Au revoir![/yellow]")
            break
        elif choice == "1":
            url = Prompt.ask("🔗 URL du livre")
            download_imgs = Confirm.ask("🖼️ Télécharger les images?", default=False)
            scrape_single_book(url, Path("output"), download_imgs)
        elif choice == "2":
            download_imgs = Confirm.ask("🖼️ Télécharger les images?", default=False)
            scrape_category(Path("output"), download_imgs, None)
        elif choice == "3":
            download_imgs = Confirm.ask("🖼️ Télécharger les images?", default=False)
            scrape_all_books(Path("output"), download_imgs)


if __name__ == "__main__":
    app()
