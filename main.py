import json
from flask import Flask, request, jsonify

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://webtech-1b839-default-rtdb.firebaseio.com/"})
ref = db.reference('py/')
voter_ref = ref.child('voter')
election_ref = ref.child('election')
voter_ref.set({})
election_ref.set({})

app = Flask(__name__)



# @app.route("/register", methods=['GET', 'POST'])
# @app.route("/deregister", methods=['GET', 'DELETE'])
# @app.route('/edit-voter', methods=['GET', 'PUT'])
# @app.route('/view-voter', methods=['GET'])
# @app.route('/new-election', methods=['GET', 'POST'])
# @app.route('/view-election', methods=['GET'])
# @app.route("/delete-election", methods=['GET', 'DELETE'])
# @app.route("/vote", methods=['GET', 'PUT'])

@app.route("/")
def voter_functions(request):
    if request.method == 'GET':
        if request.path == '/view-voter':
            voterId = request.args.get('voterId')
            return jsonify(voter_ref.child(voterId).get())
        elif request.path == '/view-election':
            ElectionId = request.args.get('ElectionId')
            return jsonify(election_ref.child(ElectionId).get())
        else:
            return 'Method not supported for this function'

    elif request.method == 'POST':
        if request.path == '/register':
            voterId = request.args.get('voterId')
            name = request.args.get('name')
            email = request.args.get('email')
            yeargroup = request.args.get('yeargroup')
            contact = request.args.get('contact')
            major = request.args.get('major')
            voter_ref.child(voterId).set({
                "name": name,
                "email": email,
                "yeargroup": yeargroup,
                "contact": contact,
                "major": major
            })
            return jsonify({'status': '200 Ok'})
        elif request.path == '/new-election':
            ElectionId = request.args.get("ElectionId")
            Election = request.args.get("Election")
            Year = request.args.get("Year")
            Position = request.args.get("Position")
            Candidate = request.args.get("Candidate")
            count = request.args.get("count")
            election_ref.child(ElectionId).set({
                "Election": Election,
                "Year": Year,
                "Position": Position,
                "Candidate": Candidate,
                "count": count
            })
            return jsonify({'status': '200 Ok'})
        else:
            return 'Method not supported for this function'

    elif request.method == 'PUT':
        if request.path == '/edit-voter':
            voterId = request.args.get('voterId')
            major = request.args.get('major')
            contact = request.args.get('contact')
            voter_ref.child(voterId).update({
                "major": major,
                "contact": contact
            })
            return jsonify(voter_ref.child(voterId).get())
        elif request.path == '/vote':
            ElectionId = request.args.get('ElectionId')
            Candidate = request.args.get('Candidate')
            count = election_ref.child(ElectionId).child("count").get()
            election_ref.child(ElectionId).update({
                "count": str(int(count)+1)
            })
            return jsonify(election_ref.child(ElectionId).get())

        else:
            return 'Method not supported for this function'
    elif request.method == 'DELETE':
        if request.path == '/deregister':
            voterId = request.args.get('voterId')
            voter_ref.child(voterId).delete()
            return jsonify({'status': '200 Ok'})
        elif request.path == '/delete-election':
            ElectionId = request.args.get('ElectionId')
            election_ref.child(ElectionId).delete()
            return jsonify({'status': '200 Ok'})
        else:
            return 'Method not supported for this function'

