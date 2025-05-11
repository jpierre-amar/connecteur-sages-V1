# app/services/chantier_service.py
import psycopg2
from app.services.connex import connect_to_sqlserver, connect_to_postgres, load_credentials

def transfer_chantiers():
    try:
        creds = load_credentials()
        if not creds or "sqlserver" not in creds or "postgres" not in creds:
            return False, "❌ Informations de connexion manquantes"

        sql = creds["sqlserver"]
        pg = creds["postgres"]

        sqlserver_conn = connect_to_sqlserver(
            sql["server"], sql["user"], sql["password"], sql["database"]
        )
        postgres_conn = connect_to_postgres(
            pg["host"], pg["user"], pg["password"], pg["database"], pg.get("port", "5432")
        )

        if not sqlserver_conn or not postgres_conn:
            return False, "❌ Connexion aux bases échouée"

        sqlserver_cursor = sqlserver_conn.cursor()
        postgres_cursor = postgres_conn.cursor()

        sqlserver_cursor.execute("""
            SELECT Code, DateDebut, DateFin, NomClient, Libelle, AdrChantier, CPChantier, VilleChantier 
            FROM dbo.ChantierDef
        """)
        rows = sqlserver_cursor.fetchall()

        for row in rows:
            code, date_debut, date_fin, nom_client, description, adr_chantier, cp_chantier, ville_chantier = row
            postgres_cursor.execute(
                """
                INSERT INTO batigest_chantiers 
                (code, date_debut, date_fin, nom_client, description, adr_chantier, cp_chantier, ville_chantier)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO NOTHING
                """,
                (code, date_debut, date_fin, nom_client, description, adr_chantier, cp_chantier, ville_chantier)
            )

        postgres_conn.commit()

        sqlserver_cursor.close()
        postgres_cursor.close()
        sqlserver_conn.close()
        postgres_conn.close()

        return True, "✅ Transfert terminé avec succès"

    except Exception as e:
        return False, f"❌ Erreur lors du transfert : {e}"
