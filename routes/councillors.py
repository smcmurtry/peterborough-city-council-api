from flask import Blueprint, jsonify, request
from models.councillor import Councillor
from models.database import db

councillors_bp = Blueprint('councillors', __name__)

@councillors_bp.route('/', methods=['GET'])
def get_councillors():
    councillors = Councillor.query.all()
    return jsonify([councillor.to_dict() for councillor in councillors])

@councillors_bp.route('/<int:councillor_id>', methods=['GET'])
def get_councillor(councillor_id):
    councillor = Councillor.query.get_or_404(councillor_id)
    return jsonify(councillor.to_dict())

@councillors_bp.route('/', methods=['POST'])
def create_councillor():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
        
    councillor = Councillor(
        name=data['name'],
        email=data.get('email'),
        ward=data.get('ward')
    )
    
    db.session.add(councillor)
    db.session.commit()
    
    return jsonify(councillor.to_dict()), 201
