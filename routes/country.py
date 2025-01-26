from flask import Blueprint, jsonify, request
from services.country import get_all_countries, add_country, delete_country, update_country

bp = Blueprint('country', __name__, url_prefix='/country')

# Route pour récupérer tous les pays
@bp.route('', methods=['GET'])
def get_countries():
    countries = get_all_countries()
    return jsonify(countries)

# Route pour ajouter un pays
@bp.route('', methods=['POST'])
def add_new_country():
    data = request.get_json()
    country_name = data.get('country')
    population = data.get('population')
    id_continent = data.get('Id_continent')
    add_country(country_name, population, id_continent)
    return jsonify({"message": "Pays ajouté avec succès"}), 201

# Route pour supprimer un pays
@bp.route('/<int:id>', methods=['DELETE'])
def delete_country_route(id):
    delete_country(id)
    return jsonify({"message": "Pays supprimé avec succès"}), 200

# Route pour mettre à jour un pays
@bp.route('/<int:id>', methods=['PUT'])
def update_country_route(id):
    data = request.get_json()
    country_name = data.get('country')
    population = data.get('population')
    id_continent = data.get('Id_continent')
    update_country(id, country_name, population, id_continent)
    return jsonify({"message": "Pays mis à jour avec succès"}), 200
