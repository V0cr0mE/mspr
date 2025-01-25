import os
import importlib.util
import sys
from flask import Flask
from routes.continent import bp as continent_bp

# Ajouter les dossiers 'load' et 'etl' au chemin d'importation
sys.path.append(os.path.join(os.path.dirname(__file__), 'load'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'etl'))

def execute_scripts_in_directory(directory):
    # Lister tous les fichiers Python dans un dossier spécifique
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            file_path = os.path.join(directory, filename)
            script_name = filename[:-3]  # Enlever l'extension '.py' pour le nom du module
            
            # Dynamique d'importation du module
            spec = importlib.util.spec_from_file_location(script_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            print(f"Exécution du fichier {filename}...")
            # Appeler la fonction main() de chaque fichier s'il y en a une
            if hasattr(module, 'main'):
                module.main()

# Créer une instance de l'application Flask
def create_app():
    app = Flask(__name__)

    # Enregistrer les Blueprints (routes) pour chaque table
    app.register_blueprint(continent_bp)

    return app

def main():
    # # Exécuter les scripts dans les dossiers 'etl' et 'load'
    # print("Exécution des scripts dans le dossier 'etl'...")
    # execute_scripts_in_directory(os.path.join(os.path.dirname(__file__), 'etl'))

    # print("Exécution des scripts dans le dossier 'load'...")
    # execute_scripts_in_directory(os.path.join(os.path.dirname(__file__), 'load'))

    # Lancer le serveur Flask
    print("Démarrage du serveur Flask...")
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()
