import os
import json
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from models import db, Note

load_dotenv()

app = Flask(__name__)

app.config['DEBUG'] = os.getenv('DEBUG')
app.config['ENV'] = os.getenv('ENV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)

@app.route('/')
def main():
    
    data = {
        "title": "API REST Luis Mario",
        "get_test": {
            "url": "/api/test",
            "method": "GET",
            "body": "none",
            "params": "none"
        },
        "post_test": {
            "url": "/api/test",
            "method": "POST",
            "body": "none",
            "params": "none"
        },
        "put_test": {
            "url": "/api/test",
            "method": "PUT",
            "body": "none",
            "params": "none"
        },
        "delete_test": {
            "url": "/api/test",
            "method": "DELETE",
            "body": "none",
            "params": "none"
        }
    }
    
    return jsonify(data)

@app.route('/api/test', methods=['GET'])
def get_test():
    return jsonify({"msg": "Testing GET method"})

@app.route('/api/test', methods=['POST'])
def post_test():
    return jsonify({ "msg": "Testing POST method"})

@app.route('/api/test', methods=['PUT'])
def put_test():
    return jsonify({ "msg": "Testing PUT method"})

@app.route('/api/test', methods=['DELETE'])
def delete_test():
    return jsonify({ "msg": "Testing DELETE method"})

@app.route('/api/greeting_all/<name>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def greeting_all_methods(name):
    if request.method == 'GET':
        return jsonify({ "msg": f"Hello, {name} Testing GET method"})
    if request.method == 'POST':
        return jsonify({ "msg": f"Hello, {name} Testing POST method"})
    if request.method == 'PUT':
        return jsonify({ "msg": f"Hello, {name} Testing PUT method"})
    if request.method == 'DELETE':
        return jsonify({ "msg": f"Hello, {name} Testing DELETE method"})  
    
@app.route('/api/greeting/<name>', methods=['POST', 'PUT'])
def greeting_post_put(name):
    if request.method == 'POST':
    
        # 1era forma de recibir los datos
        #body_request = request.data
        #body_json = json.loads(body_request)
        #lastname = body_json["lastname"]
        
        # 2da forma de recibir los datos
        #body_json = request.get_json()
        #lastname = body_json["lastname"]
        #print(body_json)
        
        #3era forma de recibir los datos de manera individual
        lastname = request.json.get("lastname")
        email = request.json.get("email")
        
        return jsonify({ "msg": f"Hello, {name} {lastname} Testing POST method"})
    
    
    
    if request.method == 'PUT':
        
        # 1era forma de recibir los datos
        #body_request = request.data
        #body_json = json.loads(body_request)
        #lastname = body_json["lastname"]
        
        # 2da forma de recibir los datos
        #body_json = request.get_json()
        #lastname = body_json["lastname"]
        #print(body_json)
        
        #3era forma de recibir los datos de manera individual
        lastname = request.json.get("lastname")
        email = request.json.get("email")
        
        return jsonify({ "msg": f"Hello, {name} {lastname} Testing PUT method"})
  

@app.route('/api/notes', methods=['GET', 'POST'])
@app.route('/api/notes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def notes(id = None):
    if request.method == 'GET':
        
        if id is not None:
            
            note = Note.query.get(id) # SELECT * FROM notes WHERE id = ?
            if not note: return jsonify({ "status": "error", "msg": "Note not found"}), 404

            return jsonify(note.get_dict()), 200
            
        else:
            notes = Note.query.all() # SELECT * FROM notes; // [<Note 1>]
            notes = list(map(lambda note: note.get_dict(), notes))
            
            return jsonify(notes), 200
        
        
    if request.method == 'POST':
        message = request.json.get("message")

        if not message: return jsonify({"status": "error", "msg": "Message is required"}), 400
        
        note = Note()
        note.message = message
        
        db.session.add(note) # INSERT INTO notes (message) VALUES ('?');
        db.session.commit() # COMMIT;
        
        return jsonify({ "status": "success", "msg": "Note created"}), 201
    
    if request.method == 'PUT':
        message = request.json.get("message")

        if not message: return jsonify({"status": "error", "msg": "Message is required"}), 400
        
        note = Note.query.get(id) # SELECT * FROM notes WHERE id = ?
        if not note: return jsonify({ "status": "error", "msg": "Note not found"}), 404
            
        note.message = message # UPDATE notes SET message = ? WHERE id = ? 
        
        db.session.commit() # COMMIT;
        
        return jsonify({ "status": "success", "msg": "Note updated"}), 200
        
    
    if request.method == 'DELETE':
        
        note = Note.query.get(id)
        if not note: return jsonify({ "status": "error", "msg": "Note not found"}), 404
        
        db.session.delete(note) # DELETE FROM notes WHERE id = ?
        db.session.commit() # COMMIT;
        
        return jsonify({ "status": "success", "msg": "Note deleted"}), 200
        


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()