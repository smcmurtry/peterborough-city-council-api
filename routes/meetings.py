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
        'date': meeting.date.isoformat(),
        'title': meeting.title,
        'status': meeting.status,
        'minutes_url': meeting.minutes_url
    } for meeting in meetings])

@meetings_bp.route('/<int:meeting_id>', methods=['GET'])
def get_meeting(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    return jsonify({
        'id': meeting.id,
        'date': meeting.date.isoformat(),
        'title': meeting.title,
        'status': meeting.status,
        'minutes_url': meeting.minutes_url
    })

@meetings_bp.route('/', methods=['POST'])
def create_meeting():
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    try:
        meeting_date = datetime.fromisoformat(data.get('date')) if data.get('date') else datetime.utcnow()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use ISO format (YYYY-MM-DD)'}), 400
    
    meeting = Meeting(
        title=data['title'],
        date=meeting_date,
        description=data.get('description'),
        minutes_url=data.get('minutes_url')
    )
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 201
