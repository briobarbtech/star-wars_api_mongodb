import json
from operator import imod
from urllib import response
from flask import Flask, Response, request
from flask_pymongo import PyMongo
import http as http
from bson import json_util, ObjectId

from entities.character import Character
from entities.report import Report

### Inicializo Flask
app = Flask(__name__)
### Defino una propiedad que va a decir donde buscar MongoDB. MongoDB siempre trabaja en el puerto 27017
app.config['MONGO_URI']='mongodb://localhost/starwarsdb'
### Le paso la configuración de mi app a PyMongo
mongo = PyMongo(app)
### to report Post request to http://localhost:5000/report
@app.route('/report', methods=["POST"])
def report_sighting():
    report = Report(request.json['userId'],request.json['id'],request.json['title'],request.json['body'])
    id = mongo.db.report.insert_one({
        "userId":report.userId,
        "id":report.id,
        "title":report.title,
        "body":report.body})
    response = {
        "id":str(id),
        "userId":report.userId,
        "id":report.id,
        "title":report.title,
        "body":report.body}
    return response, http.HTTPStatus.CREATED

@app.route('/character', methods=['POST'])
def create_character():
### http://localhost:5000/characters/?page=
    id = mongo.db.character.insert_one(request.json)
    response = {"id" : str(id)}
    return response,http.HTTPStatus.CREATED
### to get all characters Get request to http://localhost:5000/characters
@app.route('/characters', methods=["GET"])
def index():
    characters = mongo.db.character.find()
    response = json_util.dumps(characters)
    return Response(response, mimetype='application/json')

### to get characters by id Get request to http://localhost:5000/characters/<id>
@app.route('/characters/<id>', methods=['GET'])
def getPage(id):
    character = mongo.db.character.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(character)
    return Response(response, mimetype='application/json')
@app.errorhandler(404)
### response default for errors
def not_found(error=None):
    message = {'message': 'Resource Not Found: ' + request.url,'status' : 404}
    return message
if __name__ == "__main__":
    app.run(debug=True)