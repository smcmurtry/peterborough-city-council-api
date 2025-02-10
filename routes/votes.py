from flask import Blueprint, jsonify, request
from models.vote import Vote
from models.database import db

votes_bp = Blueprint('votes', __name__)

@votes_bp.route('/', methods=['GET'])
def get_votes():
    votes = Vote.query.all()
    return jsonify({
        'votes': [vote.to_dict() for vote in votes]
    })

@votes_bp.route('/<uuid:vote_id>', methods=['GET'])
def get_vote(vote_id):
    vote = Vote.query.get_or_404(vote_id)
    return jsonify(vote.to_dict())

@votes_bp.route('/', methods=['POST'])
def create_vote():
    data = request.get_json()
    
    required_fields = ['title', 'meeting_id']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    vote = Vote(
        title=data['title'],
        meeting_id=data['meeting_id'],
        carried=data.get('carried', False)
    )
    
    db.session.add(vote)
    db.session.commit()
    
    return jsonify(vote.to_dict()), 201
