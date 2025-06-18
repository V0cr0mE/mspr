import os

# Paths relative to this configuration file
BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'donnes')
CLEAN_DATA_FOLDER = os.path.join(BASE_DIR, '..', 'donnes_clean')
ALLOWED_EXTENSIONS = {"csv", "txt", "pdf"}
