from flask import Blueprint, jsonify, request
from models.councillor import Councillor
from models.database import db

councillors_bp = Blueprint('councillors', __name__)

@councillors_bp.route('/', methods=['GET'])
def get_councillors():
    councillors = Councillor.query.all()
    return jsonify([councillor.to_dict() for councillor in councillors])

@councillors_bp.route('/<string:councillor_id>', methods=['GET'])
def get_councillor(councillor_id):
    councillor = Councillor.query.get_or_404(councillor_id)
    return jsonify(councillor.to_dict())

@councillors_bp.route('/', methods=['POST'])
def create_councillor():
    data = request.get_json()
    
    if not data or not data.get("id") or not data.get('name') or not data.get('title') or not data.get('start_date'):
        return jsonify({'error': 'id, name, title, start_date are required'}), 400
        
    councillor = Councillor(
        id=data["id"],
        name=data['name'],
        title=data['title'],
        ward=data['ward'] if 'ward' in data else None,
        start_date=data['start_date'],
        end_date=data['end_date'] if 'end_date' in data else None,
    )
    
    db.session.add(councillor)
    db.session.commit()
    
    return jsonify(councillor.to_dict()), 201
