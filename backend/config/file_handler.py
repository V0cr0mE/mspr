import os
import base64
from werkzeug.utils import secure_filename
from config.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(contents, filename):
    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    with open(filepath, "wb") as f:
        f.write(decoded)
    return filepath