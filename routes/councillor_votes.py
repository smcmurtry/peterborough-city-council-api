from flask import Blueprint, jsonify, request
from models.councillor_vote import CouncillorVote
from models.vote import Vote
from models.database import db

councillor_votes_bp = Blueprint('councillor_votes', __name__)

@councillor_votes_bp.route('/', methods=['GET'])
def get_votes():
    councillorVotes = CouncillorVote.query.all()
    return jsonify({
        'councillorVotes': [{
            'id': councillorVote.id,
            'councillor_id': councillorVote.councillor_id,
            'vote_id': councillorVote.vote_id,
            'vote_cast': councillorVote.vote_cast
        } for councillorVote in councillorVotes]
    })

@councillor_votes_bp.route('/vote/<int:vote_id>', methods=['GET'])
def get_councillor_vote(vote_id):
    councillorVote = CouncillorVote.query.get_or_404(vote_id)
    return jsonify({
        'id': councillorVote.id,
        'vote_id': councillorVote.vote_id,
        'councillor_id': councillorVote.councillor_id,
        'vote_cast': councillorVote.vote_cast
    })

@councillor_votes_bp.route('/councillor/<string:councillor_id>', methods=['GET'])
def get_all_votes_for_councillor(councillor_id):
    councillor_votes = CouncillorVote.query\
        .join(Vote, CouncillorVote.vote_id == Vote.id)\
        .filter(CouncillorVote.councillor_id == councillor_id)\
        .all()
    
    if not councillor_votes:
        return jsonify({'error': 'No votes found for this councillor'}), 404
    
    return jsonify([{
        'id': cv.id,
        'councillor_id': cv.councillor_id,
        'vote_cast': cv.vote_cast,
        'vote': {
            'id': cv.vote.id,
            'title': cv.vote.title,
            'votes_for': cv.vote.votes_for,
            'votes_against': cv.vote.votes_against,
            'carried': cv.vote.carried,
            'meeting_id': cv.vote.meeting_id
        }
    } for cv in councillor_votes])

@councillor_votes_bp.route('/', methods=['POST'])
def create_councillor_vote():
    data = request.get_json()
    
    required_fields = ['councillor_id', 'vote_id', 'vote_cast']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate vote exists
    vote = Vote.query.get(data['vote_id'])
    if not vote:
        return jsonify({'error': 'Vote not found'}), 404

    # Validate vote value
    valid_votes_cast = ['for', 'against', 'abstain']
    if data['vote_cast'].lower() not in valid_votes_cast:
        return jsonify({'error': 'Vote must be one of: for, against, abstain'}), 400
    
    councillorVote = CouncillorVote(
        vote_id=data['vote_id'],
        councillor_id=data['councillor_id'],
        vote_cast=data['vote_cast'].lower()
    )
    
    db.session.add(councillorVote)
    
    # Update vote counts
    if data['vote_cast'].lower() == 'for':
        vote.votes_for += 1
    elif data['vote_cast'].lower() == 'against':
        vote.votes_against += 1
    
    db.session.commit()
    
    return jsonify({
        'id': councillorVote.id,
        'vote_id': councillorVote.vote_id,
        'councillor_id': councillorVote.councillor_id,
        'vote_cast': councillorVote.vote_cast
    }), 201
