# app/routes/form_routes.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.connex import connect_to_sqlserver, connect_to_postgres, save_credentials, load_credentials

from app.services.chantier import transfer_chantiers

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@router.post("/connect-sqlserver", response_class=HTMLResponse)
async def connect_sqlserver(
    request: Request,
    server: str = Form(...),
    user: str = Form(...),
    password: str = Form(...),
    database: str = Form(...)
):
    conn = connect_to_sqlserver(server, user, password, database)
    if conn:
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
    conn = connect_to_postgres(host, user, password, database, port)
    if conn:
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


from app.services.connex import load_credentials

@router.post("/transfer", response_class=HTMLResponse)
async def transfer_data(request: Request):
    creds = load_credentials()

    if not creds or "sqlserver" not in creds or "postgres" not in creds:
        message = "❌ Merci de renseigner les informations de connexion SQL Server et PostgreSQL avant de lancer le transfert."
        return templates.TemplateResponse("form.html", {"request": request, "message": message})

    success, message = transfer_chantiers()
    return templates.TemplateResponse("form.html", {"request": request, "message": message})



