from flask import Blueprint, jsonify, request
from models.vote import Vote
from models.database import db

votes_bp = Blueprint('votes', __name__)

@votes_bp.route('/', methods=['GET'])
def get_votes():
    votes = Vote.query.all()
    return jsonify({
        'votes': [{
            'id': vote.id,
            'meeting_id': vote.meeting_id,
            'councillor_id': vote.councillor_id,
            'vote': vote.vote
        } for vote in votes]
    })

@votes_bp.route('/<int:vote_id>', methods=['GET'])
def get_vote(vote_id):
    vote = Vote.query.get_or_404(vote_id)
    return jsonify({
        'id': vote.id,
        'meeting_id': vote.meeting_id,
        'councillor_id': vote.councillor_id,
        'vote': vote.vote
    })

@votes_bp.route('/', methods=['POST'])
def create_vote():
    data = request.get_json()
    
    required_fields = ['meeting_id', 'councillor_id', 'vote']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate vote value
    valid_votes = ['yes', 'no', 'abstain']
    if data['vote'].lower() not in valid_votes:
        return jsonify({'error': 'Vote must be one of: yes, no, abstain'}), 400
    
    vote = Vote(
        meeting_id=data['meeting_id'],
        councillor_id=data['councillor_id'],
        vote=data['vote'].lower()
    )
    
    db.session.add(vote)
    db.session.commit()
    
    return jsonify({
        'id': vote.id,
        'meeting_id': vote.meeting_id,
        'councillor_id': vote.councillor_id,
        'vote': vote.vote
    }), 201
