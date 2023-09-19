# Routes for handling event related functionality (event creation, updating and deleting)

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request, abort
from models import db, Event

event = Blueprint('event', __name__)


@event.route('/api/events', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    start_date = data.get('start_date')
    start_time = data.get('start_time')
    end_date = data.get('end_date')
    end_time = data.get('end_time')
    thumbnail = data.get('thumbnail')

    current_user_id = get_jwt_identity()
    
    # Create a new event
    event = Event(
        title=title,
        description=description,
        location=location,
        start_date=start_date,
        start_time=start_time,
        end_date=end_date,
        end_time=end_time,
        thumbnail_url=thumbnail,
        user_id=current_user_id
    )

    db.session.add(event)
    db.session.commit()

    return jsonify({'message': 'Event successfully added'}), 201
