from flask import Blueprint, jsonify, request
from services.pandemic import get_all_pandemics, add_pandemic, delete_pandemic, update_pandemic

# Création d'un Blueprint pour les pandémies
bp = Blueprint('pandemic', __name__, url_prefix='/pandemic')

# Route pour récupérer toutes les pandémies
@bp.route('', methods=['GET'])
def get_pandemics():
    pandemics = get_all_pandemics()
    return jsonify(pandemics)

# Route pour ajouter une nouvelle pandémie
@bp.route('', methods=['POST'])
def add_new_pandemic():
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'message': 'Le nom de la pandémie est requis.'}), 400

    add_pandemic(name)
    return jsonify({'message': 'Pandémie ajoutée avec succès.'}), 201

# Route pour supprimer une pandémie
@bp.route('/<int:pandemic_id>', methods=['DELETE'])
def delete_pandemic_route(pandemic_id):
    delete_pandemic(pandemic_id)
    return jsonify({'message': 'Pandémie supprimée avec succès.'}), 200

# Route pour mettre à jour une pandémie
@bp.route('/<int:pandemic_id>', methods=['PUT'])
def update_pandemic_route(pandemic_id):
    data = request.get_json()
    name = data.get('name')
    
    if not name:
        return jsonify({'message': 'Le nom de la pandémie est requis.'}), 400

    update_pandemic(pandemic_id, name)
    return jsonify({'message': 'Pandémie mise à jour avec succès.'}), 200
