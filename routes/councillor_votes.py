from flask import Blueprint, jsonify, request
from models.councillor_vote import CouncillorVote
from models.database import db

votes_bp = Blueprint('councillor_votes', __name__)

@votes_bp.route('/', methods=['GET'])
def get_votes():
    councillorVotes = CouncillorVote.query.all()
    return jsonify({
        'councillorVotes': [{
            'id': councillorVote.id,
            'meeting_id': councillorVote.meeting_id,
            'councillor_id': councillorVote.councillor_id,
            'vote': councillorVote.vote
        } for councillorVote in councillorVotes]
    })

@votes_bp.route('/<int:vote_id>', methods=['GET'])
def get_councillor_vote(vote_id):
    councillorVote = CouncillorVote.query.get_or_404(vote_id)
    return jsonify({
        'id': councillorVote.id,
        'vote_id': councillorVote.vote_id,
        'meeting_id': councillorVote.meeting_id,
        'councillor_id': councillorVote.councillor_id,
        'vote': councillorVote.vote
    })

@votes_bp.route('/', methods=['POST'])
def create_councillor_vote():
    data = request.get_json()
    
    required_fields = ['meeting_id', 'councillor_id', 'vote_id', 'vote_cast']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate vote value
    valid_votes_cast = ['yes', 'no', 'abstain']
    if data['vote_cast'].lower() not in valid_votes_cast:
        return jsonify({'error': 'Vote must be one of: yes, no, abstain'}), 400
    
    councillorVote = CouncillorVote(
        meeting_id=data['meeting_id'],
        vote_id=data['vote_id'],
        councillor_id=data['councillor_id'],
        vote_cast=data['vote_cast'].lower()
    )
    
    db.session.add(councillorVote)
    db.session.commit()
    
    return jsonify({
        'id': councillorVote.id,
        'meeting_id': councillorVote.meeting_id,
        'vote_id': councillorVote.vote_id,
        'councillor_id': councillorVote.councillor_id,
        'vote_cast': councillorVote.vote_cast
    }), 201
