from flask import Blueprint, jsonify, request
from models.meeting import Meeting
from datetime import datetime
from models.database import db

meetings_bp = Blueprint('meetings', __name__)

@meetings_bp.route('/', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([{
        'id': meeting.id,
        'name': meeting.name,
        'date': meeting.date,
        'location': meeting.location,
        'minutes_fname': meeting.minutes_fname
    } for meeting in meetings])

@meetings_bp.route('/<string:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return jsonify({
        'id': meeting.id,
        'name': meeting.name,
        'date': meeting.date,
        'location': meeting.location,
        'minutes_fname': meeting.minutes_fname
    })

@meetings_bp.route('/search', methods=['GET'])
def search_meeting():
    name = request.args.get('name')
    date_str = request.args.get('date')
    
    if not name or not date_str:
        return jsonify({'error': 'Both name and date are required query parameters'}), 400
    
    try:
        # Parse date string in format YYYY-MM-DD
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Date must be in YYYY-MM-DD format'}), 400
    
    meeting = Meeting.query.filter_by(
        name=name,
        date=date
    ).first()
    
    if not meeting:
        return jsonify({'error': 'Meeting not found'}), 404
    
    return jsonify(meeting.to_dict())


@meetings_bp.route('/', methods=['POST'])
def create_meeting():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    
    meeting = Meeting(
        name=data['name'],
        location=data.get('location'),
        date=data.get('date'),
        minutes_fname=data.get('minutes_fname')
    )
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 201
