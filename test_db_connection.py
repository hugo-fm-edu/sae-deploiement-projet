"""
Script pour tester la connexion à la base de données.
À exécuter avant de lancer l'API pour vérifier que PostgreSQL est accessible.
"""

from app.database.db import test_connection, DATABASE_URL

if __name__ == "__main__":
    print(f"🔍 Test de connexion à la base de données...")
    print(f"📍 URL: {DATABASE_URL}")
    print()
    
    if test_connection():
        print("\n✅ Tout fonctionne! La base de données est accessible.")
    else:
        print("\n❌ Erreur: Impossible de se connecter à la base de données.")
        print("\n💡 Vérifiez que:")
        print("  1. PostgreSQL est installé et démarré")
        print("  2. Le fichier .env contient les bonnes informations")
        print("  3. La base de données 'sae_project_db' existe")
        print("  4. L'utilisateur 'sae_user' a les droits nécessaires")
