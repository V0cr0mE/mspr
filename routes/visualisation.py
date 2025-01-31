from flask import Blueprint, send_from_directory,render_template
import os

# Créer un Blueprint pour la visualisation
bp = Blueprint('visualisation', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('plateforme.html')
