import subprocess
import sys
import os

def execute_python_files(directory, exclude_files=None):
    """
    Exécute tous les fichiers Python dans le répertoire donné, sauf ceux exclus.
    """
    if exclude_files is None:
        exclude_files = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename not in exclude_files:
            filepath = os.path.join(directory, filename)
            print(f"Exécution de {filepath}...")
            # on force le cwd sur le dossier du script afin que "../donnes_clean" fonctionne
            subprocess.run([sys.executable, filepath], check=True, cwd=directory)

if __name__ == "__main__":
    models_directory = os.path.join(os.getcwd(),"backend", "models")
    load_directory = os.path.join(os.getcwd(), "backend", "load")
    
    if os.path.exists(models_directory):
        # on exécute dans l'ordre correct pour respecter les FK :
        for script in [
            "continent.py",
            "country.py",
            "pandemic.py",                # créer pandemic AVANT daily_pandemic_country
            "daily_pandemic_country.py",
            "pandemic_country.py"
        ]:
            path = os.path.join(models_directory, script)
            if os.path.exists(path):
                print(f"Exécution de {path}...")
                subprocess.run([sys.executable, path], check=True, cwd=models_directory)
    else:
        print(f"Le répertoire {models_directory} n'existe pas.")
    
    if os.path.exists(load_directory):
        execute_python_files(load_directory, exclude_files=["__init__.py"])
    else:
        print(f"Le répertoire {load_directory} n'existe pas.")
