from flask import Blueprint, jsonify, request
from services.continent import get_all_continents, add_continent, delete_continent, update_continent

bp = Blueprint('continent', __name__, url_prefix='/continent')

# Route pour récupérer tous les continents
@bp.route('', methods=['GET'])
def get_continents():
    continents = get_all_continents()
    return jsonify(continents)

# Route pour ajouter un continent
@bp.route('', methods=['POST'])
def add_new_continent():
    data = request.get_json()
    continent_name = data.get('continent')
    add_continent(continent_name)
    return jsonify({"message": "Continent ajouté avec succès"}), 201

# Route pour supprimer un continent
@bp.route('/<int:id>', methods=['DELETE'])
def delete_continent_route(id):
    delete_continent(id)
    return jsonify({"message": "Continent supprimé avec succès"}), 200

# Route pour mettre à jour un continent
@bp.route('/<int:id>', methods=['PUT'])
def update_continent_route(id):
    data = request.get_json()
    continent_name = data.get('continent')
    update_continent(id, continent_name)
    return jsonify({"message": "Continent mis à jour avec succès"}), 200
