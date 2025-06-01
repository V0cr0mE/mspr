from flask import Blueprint, jsonify
from IA.predict import predict_daily_cases_from_db

bp = Blueprint('prediction', __name__)

@bp.route('/predict/<int:id_country>/<int:id_pandemic>', methods=['GET'])
def get_prediction(id_country, id_pandemic):
    try:
        predictions = predict_daily_cases_from_db(id_country, id_pandemic)
        return jsonify(predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
