"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():

    members = jackson_family.get_all_members()

    response_body = {
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):

    member = jackson_family.get_member(member_id)

    if member is not None:
        response_body = {"message": "Member shown successfully", "family": member}
        return jsonify(response_body), 200
    else:
        response_body = {"message": "Member not found"}
        return jsonify(response_body), 404

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):

    deleted_member = jackson_family.delete_member(member_id)

    members = jackson_family.get_all_members()

    if deleted_member is not None:
        response_body = {"message": "Member deleted successfully", "family": members}
        return jsonify(response_body), 200
    else:
        response_body = {"message": "Member not found"}
        return jsonify(response_body), 405

@app.route('/add_member', methods=['POST'])
def add_new_member():

    request_body = request.json

    new_member = {
        "id": jackson_family._generateId(),
        "first_name": request_body["first_name"],
        "last_name": "Jackson",
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }

    jackson_family.add_member(new_member)

    members = jackson_family.get_all_members()

    response_body = {
        "family": members
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
