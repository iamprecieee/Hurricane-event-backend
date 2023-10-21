from flask import Blueprint, request, jsonify
import json
from models.user import *

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET', 'POST'])
@api.route('/users/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def users(id=None):
    if request.method == "GET":
        if id is None:
            # GET /users: Retrieve a list of all users
            users = User.query.all()
            data = users.serialize()
            result = json.dumps(data, indent=4)

            return result, 201, {'Content-Type': 'application/json'}
        else:
            if user := User.query.get(id):
                data = user.serialize()
                result = json.dumps(data, indent=4)

                return result, 201, {'Content-Type": "application/json'}
            else:
                return jsonify(message='User not found!'), 404

    elif request.method == 'POST':
        # POST /users: Create a new user
        data = request.json
        new_user = data.get('id', 'name', 'email', 'avatar')

        db.session.add(new_user)
        db.session.commit()

        result = new_user.serialize()
        result = json.dumps(result, indent=4)

        return result, 201, {'Content-Type': 'application/json'}

    elif request.method == "PUT":
        if user := User.query.get(id):
            # Get data
            data = request.json

            # Update data
            name = request.json.get('name')
            email = request.json.get('email')
            avatar = request.json.get('avatar')

            # Save modifications
            user.name = name
            user.email = email
            user.avatar = avatar

            # Commit changes to db
            db.session.commit()

            data = user.serialize()
            result = json.dumps(data, indent=4)
            return result, 201, {'Content-Type': 'application/json'}
        else:
            return jsonify(message='User not found'), 404

    elif request.method == 'DELETE':
        if user := User.query.get(id):
            db.session.delete(user)
            db.session.commit()
            return jsonify(message='User has been deleted.')
        else:
            return jsonify(message='User not found')
