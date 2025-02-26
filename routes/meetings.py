from flask import Blueprint, jsonify, request, make_response
from models.meeting import Meeting
from datetime import datetime
from models.database import db

meetings_bp = Blueprint('meetings', __name__)

def jsonify_meeting_list(meetings):
    return jsonify([{
        'id': meeting.id,
        'name': meeting.name,
        'date': meeting.date,
        'location': meeting.location,
        'minutes_fname': meeting.minutes_fname
    } for meeting in meetings])

@meetings_bp.route('/', methods=['GET'])
def get_meetings():
    meetings = Meeting.query.all()
    response = make_response(jsonify_meeting_list(meetings))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

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
def search_meetings():
    name = request.args.get('name')
    date_str = request.args.get('date')
    
    if not name and not date_str:
        return jsonify({'error': 'You must provide a name and/or a date as query parameters'}), 400
    date = None
    if date_str:
        try:
            # Parse date string in format YYYY-MM-DD
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Date must be in YYYY-MM-DD format'}), 400

    query = Meeting.query
    if name:
        query = query.filter(Meeting.name == name)
    if date:
        query = query.filter(Meeting.date == date)

    meetings = query.all()
    
    if not meetings:
        return jsonify({'error': 'Meetings not found'}), 404
    
    return jsonify_meeting_list(meetings)


@meetings_bp.route('/', methods=['POST'])
def create_meeting():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    
    meeting = Meeting(
        id=data['id'],
        name=data['name'],
        location=data['location'],
        date=data['date'],
        minutes_fname=data['minutes_fname']
    )
    
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify(meeting.to_dict()), 201
