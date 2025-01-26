from flask import Blueprint, request, jsonify
from services.daily_pandemic_country import (
    get_daily_data,
    add_daily_data,
    update_daily_data,
    delete_daily_data
)

bp = Blueprint('daily_pandemic_country', __name__, url_prefix='/daily_pandemic_country')

@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['GET'])
@bp.route('/<int:id_country>/<int:id_pandemic>/<string:date>', methods=['GET'])
def get_daily_data_route(id_country, id_pandemic, date=None):
    try:
        if date:  # Si une date est fournie dans l'URL
            daily_data = get_daily_data(id_country, id_pandemic, date)
            if daily_data:
                return jsonify(daily_data)
            else:
                return jsonify({"message": "No daily data found for the given parameters"}), 404
        else:  # Si aucune date n'est fournie
            all_daily_data = get_daily_data(id_country, id_pandemic)
            if all_daily_data:
                return jsonify(all_daily_data)
            else:
                return jsonify({"message": "No daily data found for the given country and pandemic"}), 404
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400



# Ajouter des données journalières
@bp.route('/', methods=['POST'])
def add_daily_data_route():
    data = request.get_json()
    id_country = data.get('id_country')
    id_pandemic = data.get('id_pandemic')
    date = data.get('date')
    daily_new_deaths = data.get('daily_new_deaths')
    daily_new_cases = data.get('daily_new_cases')
    add_daily_data(id_country, id_pandemic, date, daily_new_deaths, daily_new_cases)
    return jsonify({"message": "Daily data added successfully"}), 201

# Mettre à jour des données journalières
@bp.route('/<int:id_country>/<int:id_pandemic>/<string:date>', methods=['PUT'])
def update_daily_data_route(id_country, id_pandemic, date):
    data = request.get_json()
    daily_new_deaths = data.get('daily_new_deaths')
    daily_new_cases = data.get('daily_new_cases')
    update_daily_data(id_country, id_pandemic, date, daily_new_deaths, daily_new_cases)
    return jsonify({"message": "Daily data updated successfully"})

# Supprimer des données journalières
@bp.route('/<int:id_country>/<int:id_pandemic>/<string:date>', methods=['DELETE'])
def delete_daily_data_route(id_country, id_pandemic, date):
    delete_daily_data(id_country, id_pandemic, date)
    return jsonify({"message": "Daily data deleted successfully"})
