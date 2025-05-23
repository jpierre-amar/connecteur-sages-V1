# app/routes/form_routes.py

# Module de gestion des routes pour le formulaire de connexion
# Ce fichier contient toutes les routes pour gérer les connexions aux bases de données
# et le transfert des données entre SQL Server et PostgreSQL

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.connex import connect_to_sqlserver, connect_to_postgres, save_credentials, load_credentials
from app.services.chantier import transfer_chantiers

# Création du routeur FastAPI
router = APIRouter()
# Configuration du moteur de templates
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    """
    Route principale affichant le formulaire de connexion.
    
    Args:
        request (Request): Requête FastAPI
        
    Returns:
        TemplateResponse: Page HTML du formulaire
    """
    return templates.TemplateResponse("form.html", {"request": request})


@router.post("/connect-sqlserver", response_class=HTMLResponse)
async def connect_sqlserver(
    request: Request,
    server: str = Form(...),
    user: str = Form(...),
    password: str = Form(...),
    database: str = Form(...)
):
    """
    Route pour tester et sauvegarder la connexion SQL Server.
    
    Args:
        request (Request): Requête FastAPI
        server (str): Nom ou adresse du serveur SQL
        user (str): Nom d'utilisateur
        password (str): Mot de passe
        database (str): Nom de la base de données
        
    Returns:
        TemplateResponse: Page HTML avec le message de résultat
    """
    conn = connect_to_sqlserver(server, user, password, database)
    if conn:
        # Si la connexion réussit, on sauvegarde les identifiants
        creds = load_credentials() or {}
        creds["sqlserver"] = {
            "server": server,
            "user": user,
            "password": password,
            "database": database
        }
        save_credentials(creds)
        message = "✅ Connexion SQL Server réussie !"
    else:
        message = "❌ Connexion SQL Server échouée."
    return templates.TemplateResponse("form.html", {"request": request, "message": message})


@router.post("/connect-postgres", response_class=HTMLResponse)
async def connect_postgres(
    request: Request,
    host: str = Form(...),
    user: str = Form(...),
    password: str = Form(...),
    database: str = Form(...),
    port: str = Form("5432")
):
    """
    Route pour tester et sauvegarder la connexion PostgreSQL.
    
    Args:
        request (Request): Requête FastAPI
        host (str): Nom d'hôte ou adresse IP du serveur
        user (str): Nom d'utilisateur
        password (str): Mot de passe
        database (str): Nom de la base de données
        port (str): Port de connexion (défaut: 5432)
        
    Returns:
        TemplateResponse: Page HTML avec le message de résultat
    """
    conn = connect_to_postgres(host, user, password, database, port)
    if conn:
        # Si la connexion réussit, on sauvegarde les identifiants
        creds = load_credentials() or {}
        creds["postgres"] = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": port
        }
        save_credentials(creds)
        message = "✅ Connexion PostgreSQL réussie !"
    else:
        message = "❌ Connexion PostgreSQL échouée."
    return templates.TemplateResponse("form.html", {"request": request, "message": message})


@router.post("/transfer", response_class=HTMLResponse)
async def transfer_data(request: Request):
    """
    Route pour lancer le transfert des données entre SQL Server et PostgreSQL.
    Vérifie d'abord que les deux connexions sont configurées avant de procéder.
    
    Args:
        request (Request): Requête FastAPI
        
    Returns:
        TemplateResponse: Page HTML avec le message de résultat du transfert
    """
    creds = load_credentials()

    if not creds or "sqlserver" not in creds or "postgres" not in creds:
        message = "❌ Merci de renseigner les informations de connexion SQL Server et PostgreSQL avant de lancer le transfert."
        return templates.TemplateResponse("form.html", {"request": request, "message": message})

    success, message = transfer_chantiers()
    return templates.TemplateResponse("form.html", {"request": request, "message": message})



