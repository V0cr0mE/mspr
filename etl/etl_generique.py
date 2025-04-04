import os
from etl_coronavirus_summary import load_summary
from etl_coronavirus_daily import load_daily
from etl_monkeypox import load_monkeypox

def detect_and_process(file_path):
    filename = os.path.basename(file_path).lower()

    if "worldometer_summary" in filename:
        print("Fichier détecté : Données cumulées (summary)")
        load_summary(file_path)

    elif "worldometer_daily" in filename:
        print("Fichier détecté : Données journalières (daily)")
        load_daily(file_path)

    elif "monkeypox" in filename:
        print("Fichier détecté : Monkeypox")
        load_monkeypox(file_path)

    else:
        print("Type de fichier inconnu : aucun traitement associé.")

if __name__ == "__main__":
    file_path = input("Entrez le chemin du fichier à traiter : ")
    detect_and_process(file_path)
