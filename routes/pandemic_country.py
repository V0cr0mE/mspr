from flask import Blueprint, jsonify, request
from services.pandemic_country import get_all_pandemic_country, add_pandemic_country, delete_pandemic_country, update_pandemic_country,get_pandemic_country_by_id

bp = Blueprint('pandemic_country', __name__, url_prefix='/pandemic_country')

# Route pour récupérer toutes les données de pandémie par pays
@bp.route('', methods=['GET'])
def get_pandemic_countries():
    pandemic_countries = get_all_pandemic_country()
    return jsonify(pandemic_countries)

# Route pour récupérer les données de pandémie par pays et id_pandemic
@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_pandemic_country_by_id_route(id_country, id_pandemic):
    pandemic_country = get_pandemic_country_by_id(id_country, id_pandemic)
    if pandemic_country:
        return jsonify(pandemic_country)
    else:
        return jsonify({"message": "Pandemic data not found for the given country and pandemic ID"}), 404


# Route pour ajouter une entrée pour un pays et une pandémie
@bp.route('', methods=['POST'])
def add_new_pandemic_country():
    data = request.get_json()
    id_country = data.get('id_country')
    id_pandemic = data.get('id_pandemic')
    total_confirmed = data.get('total_confirmed')
    total_deaths = data.get('total_deaths')
    total_recovered = data.get('total_recovered')
    active_cases = data.get('active_cases')
    serious_or_critical = data.get('serious_or_critical')
    total_tests = data.get('total_tests')
    total_tests_per_1m_population = data.get('total_tests_per_1m_population')
    total_deaths_per_1m_population = data.get('total_deaths_per_1m_population')
    total_cases_per_1m_population = data.get('total_cases_per_1m_population')

    add_pandemic_country(id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                         active_cases, serious_or_critical, total_tests,
                         total_tests_per_1m_population, total_deaths_per_1m_population,
                         total_cases_per_1m_population)
    return jsonify({"message": "Données de pandémie ajoutées avec succès"}), 201

# Route pour supprimer une entrée pour un pays et une pandémie
@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['DELETE'])
def delete_pandemic_country_route(id_country, id_pandemic):
    delete_pandemic_country(id_country, id_pandemic)
    return jsonify({"message": "Données de pandémie supprimées avec succès"}), 200

# Route pour mettre à jour une entrée pour un pays et une pandémie
@bp.route('/<int:id_country>/<int:id_pandemic>', methods=['PUT'])
def update_pandemic_country_route(id_country, id_pandemic):
    data = request.get_json()
    total_confirmed = data.get('total_confirmed')
    total_deaths = data.get('total_deaths')
    total_recovered = data.get('total_recovered')
    active_cases = data.get('active_cases')
    serious_or_critical = data.get('serious_or_critical')
    total_tests = data.get('total_tests')
    total_tests_per_1m_population = data.get('total_tests_per_1m_population')
    total_deaths_per_1m_population = data.get('total_deaths_per_1m_population')
    total_cases_per_1m_population = data.get('total_cases_per_1m_population')

    update_pandemic_country(id_country, id_pandemic, total_confirmed, total_deaths, total_recovered,
                            active_cases, serious_or_critical, total_tests,
                            total_tests_per_1m_population, total_deaths_per_1m_population,
                            total_cases_per_1m_population)
    return jsonify({"message": "Données de pandémie mises à jour avec succès"}), 200
