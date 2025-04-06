from flask import Blueprint, jsonify, request, render_template
from services.continent import get_all_continents, add_continent, delete_continent, update_continent

bp = Blueprint('continent', __name__, url_prefix='/continent')

# Route pour récupérer tous les continents
@bp.route('', methods=['GET'])
def get_continents():
    """
    Récupérer tous les continents
    ---
    responses:
      200:
        description: Liste des continents
        schema:
          type: array
          items:
            type: object
            properties:
              id_continent:
                type: integer
              name:
                type: string
    """
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


@bp.route("/index/test",  methods=['GET'])
def index():
    return render_template('index.html')
