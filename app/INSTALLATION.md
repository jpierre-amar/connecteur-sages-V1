# Guide d'Installation - Connecteur BATISIMPLY

Ce guide vous accompagne dans l'installation du connecteur BATISIMPLY sur votre poste de travail.

## Prérequis

- Windows 10 ou supérieur
- Python 3.8 ou supérieur
- Git (optionnel, pour la mise à jour du logiciel)
- Accès à Internet pour l'installation des dépendances
- PostgreSQL 14 ou supérieur
- SQL Server (pour la connexion à Batigest)

## Étapes d'installation

### 1. Installation de Python

1. Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
2. Lors de l'installation, **IMPORTANT** : cochez la case "Add Python to PATH"
3. Cliquez sur "Install Now"
4. Vérifiez l'installation en ouvrant un terminal (PowerShell) et en tapant :
   ```bash
   python --version
   ```

### 2. Installation de PostgreSQL

1. Téléchargez PostgreSQL depuis [postgresql.org](https://www.postgresql.org/download/windows/)
2. Lancez l'installateur et suivez les étapes :
   - Choisissez le port par défaut (5432)
   - Définissez un mot de passe pour l'utilisateur 'postgres'
   - **IMPORTANT** : Notez ce mot de passe, il sera nécessaire pour la configuration
3. Une fois l'installation terminée, vérifiez que le service PostgreSQL est en cours d'exécution :
   - Ouvrez les Services Windows (services.msc)
   - Recherchez "PostgreSQL"
   - Assurez-vous que le service est "En cours d'exécution"
   - Si non, démarrez-le manuellement

### 3. Installation du connecteur

1. Créez un dossier pour le connecteur (par exemple : `C:\Connecteur-BATISIMPLY`)
2. Copiez les fichiers du connecteur dans ce dossier
3. Ouvrez un terminal (PowerShell) dans le dossier du connecteur
4. Installez les dépendances en exécutant :
   ```bash
   pip install -r requirements.txt
   ```

   > **Note :** Si vous obtenez une erreur indiquant que pip n'est pas reconnu, suivez ces étapes :
   > 1. Fermez et rouvrez PowerShell
   > 2. Si le problème persiste, essayez d'utiliser la commande complète :
   >    ```bash
   >    py -m pip install -r requirements.txt
   >    ```
   > 3. Si cela ne fonctionne toujours pas, vérifiez que Python est bien dans votre PATH :
   >    - Ouvrez les Paramètres Windows
   >    - Recherchez "variables d'environnement"
   >    - Cliquez sur "Modifier les variables d'environnement système"
   >    - Cliquez sur "Variables d'environnement"
   >    - Dans "Variables système", trouvez "Path"
   >    - Vérifiez que les chemins suivants sont présents :
   >      ```
   >      C:\Users\[VotreNom]\AppData\Local\Programs\Python\Python3x\
   >      C:\Users\[VotreNom]\AppData\Local\Programs\Python\Python3x\Scripts\
   >      ```
   >    - Si non, ajoutez-les et redémarrez PowerShell

### 4. Configuration

1. Ouvrez le fichier `backend/config.json` dans un éditeur de texte
2. Copiez et collez le modèle de configuration suivant, puis adaptez les valeurs selon votre environnement :

```json
{
    "batigest": {
        "server": "localhost\\SAGEBAT",
        "port": 1433,
        "database": "BTG_DOS_DEMO",
        "username": "votre_utilisateur_sql",
        "password": "votre_mot_de_passe_sql",
        "connection_type": "pymssql"
    },
    "batisimply": {
        "apiUrl": "https://api.batisimply.com",
        "apiKey": "votre_clé_api",
        "companyId": "votre_id_entreprise"
    },
    "postgres": {
        "host": "localhost",
        "port": "5432",
        "database": "connecteur_buffer",
        "username": "postgres",
        "password": "Test"
    },
    "advanced": {
        "logLevel": "INFO",
        "logRetention": "30",
        "keepHistory": true,
        "autoStart": false,
        "minimizeTray": false
    },
    "auto_sync": {
        "enabled": false,
        "batigestToBatisimply": {
            "frequency": "daily",
            "time": "00:00"
        },
        "batisimplyToBatigest": {
            "frequency": "daily",
            "time": "00:00"
        }
    }
}
```

3. Modifiez les paramètres suivants :
   - `batigest.server` : L'adresse de votre serveur SQL Server (ex: "localhost\\SAGEBAT")
   - `batigest.database` : Le nom de votre base de données Batigest
   - `batigest.username` : Votre identifiant de connexion SQL Server
   - `batigest.password` : Votre mot de passe SQL Server
   - `batisimply.apiKey` : Votre clé API Batisimply
   - `batisimply.companyId` : L'identifiant de votre entreprise sur Batisimply
   - `postgres.password` : Le mot de passe PostgreSQL défini lors de l'installation

> **Note de sécurité** : Ne partagez jamais votre fichier `config.json` contenant vos identifiants. Ce fichier contient des informations sensibles.

### 5. Démarrage du connecteur

1. Pour démarrer le connecteur, exécutez dans le terminal :
   ```bash
   python backend/main.py
   ```

2. Pour arrêter le connecteur, appuyez sur Ctrl+C dans le terminal

### 6. Accès à l'interface web

1. Une fois le connecteur démarré, vous verrez un message indiquant que le serveur est en cours d'exécution sur `http://0.0.0.0:8000`
2. Pour accéder à l'interface web, ouvrez votre navigateur et utilisez l'une des URLs suivantes :
   - `http://localhost:8000`
   - `http://127.0.0.1:8000`

> **Note :** N'utilisez pas `http://0.0.0.0:8000` directement dans votre navigateur, cette adresse est utilisée par le serveur pour écouter toutes les interfaces réseau.

## Utilisation de l'interface

### Onglet Synchronisation

L'onglet Synchronisation vous permet de :
- Synchroniser les données de Batigest vers Batisimply (heures, employés, catégories)
- Synchroniser les temps saisis de Batisimply vers Batigest
- Voir le statut de la dernière synchronisation

### Onglet Configuration

L'onglet Configuration vous permet de :
- Configurer les connexions à Batigest et Batisimply
- Configurer la base de données PostgreSQL
- Définir les paramètres avancés (niveau de log, rétention des logs, etc.)
- Configurer la synchronisation automatique

### Onglet Logs

L'onglet Logs vous permet de :
- Consulter l'historique des opérations et des erreurs
- Filtrer les logs par niveau (INFO, WARNING, ERROR)
- Exporter les logs au format CSV
- Effacer les logs

## Dépannage courant

### Le connecteur ne démarre pas
- Vérifiez que Python est bien installé
- Vérifiez que toutes les dépendances sont installées
- Vérifiez les logs dans le fichier `connecteur.log`

### Erreurs de connexion à PostgreSQL
Si vous obtenez l'erreur "connection was closed in the middle of operation" :
1. Vérifiez que le service PostgreSQL est en cours d'exécution :
   ```bash
   net start postgresql
   ```
2. Vérifiez que les paramètres de connexion dans `config.json` sont corrects :
   - Le mot de passe PostgreSQL est correct (par défaut : "Test")
   - Le port est bien "5432" (en tant que chaîne de caractères)
   - L'utilisateur est bien "postgres"
3. Vérifiez que PostgreSQL accepte les connexions locales :
   - Ouvrez pgAdmin 4
   - Connectez-vous au serveur
   - Vérifiez que la base de données "connecteur_buffer" existe
   - Si elle n'existe pas, créez-la :
     ```sql
     CREATE DATABASE connecteur_buffer;
     ```

### Erreurs de connexion à SQL Server
Si vous rencontrez des problèmes de connexion à SQL Server :
1. Vérifiez que le service SQL Server est en cours d'exécution :
   - Ouvrez les Services Windows (services.msc)
   - Recherchez "SQL Server (SAGEBAT)" ou le nom de votre instance
   - Assurez-vous que le service est "En cours d'exécution"
2. Vérifiez que les paramètres de connexion dans `config.json` sont corrects :
   - Le nom du serveur est correct (ex: "localhost\\SAGEBAT")
   - Le port est bien 1433
   - Le nom de la base de données est correct
   - Les identifiants sont valides
3. Testez la connexion via SQL Server Management Studio (SSMS) avec les mêmes paramètres

### Erreurs de synchronisation
- Vérifiez les paramètres de connexion à Batigest et Batisimply
- Vérifiez que les données à synchroniser existent dans les deux systèmes
- Consultez les logs pour plus de détails sur l'erreur

### Problèmes de connexion
- Vérifiez votre connexion Internet
- Vérifiez les paramètres de configuration dans `config.json`
- Vérifiez que les identifiants sont corrects

## Sauvegarde de la base de données

Le connecteur permet de créer des sauvegardes de la base de données PostgreSQL. Les sauvegardes sont stockées dans le dossier du connecteur avec un nom au format `backup_YYYYMMDD_HHMMSS.sql`.

Pour créer une sauvegarde manuelle, vous pouvez utiliser l'interface web ou exécuter la commande suivante dans le terminal :
```bash
python -c "from backend.database.postgres_manager import PostgresManager; import asyncio; asyncio.run(PostgresManager('localhost', '5432', 'connecteur', 'postgres', 'votre_mot_de_passe').backup_database())"
```

## Support

En cas de problème, contactez le support technique :
- Email : Jean-pierre : dev2@groupe-sages.com , Gabriel : dev3@groupe-sages.com
- Téléphone : 04 67 34 01 01

## Mise à jour

Pour mettre à jour le connecteur :
1. Arrêtez le connecteur
2. Sauvegardez votre fichier de configuration
3. Remplacez les fichiers par les nouvelles versions
4. Restaurez votre configuration
5. Redémarrez le connecteur 