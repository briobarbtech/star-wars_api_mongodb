from flask import Flask, Response, request
from flask_pymongo import PyMongo
import http as http
from bson import json_util, ObjectId
from models.report import Report

### Inicializo Flask
app = Flask(__name__)
### Defino una propiedad que va a decir donde buscar MongoDB. MongoDB siempre trabaja en el puerto 27017
app.config['MONGO_URI']='mongodb://mydb/starwarsdb'
### Le paso la configuración de mi app a PyMongo
mongo = PyMongo(app)
### to report Post request to http://localhost:5000/report
@app.route('/report', methods=["POST"])
def report_sighting():
    report = Report(request.json['name'],request.json['title'],request.json['body'], request.json['date'])
    id = mongo.db.report.insert_one({
        "name":report.name,
        "title":report.title,
        "body":report.body,
        "date":report.date})

    return {'message':'Éxito'},http.HTTPStatus.CREATED

### to get all reports do GET request to http://localhost:5000/report
@app.route('/report', methods=["GET"])
def get_reports():
    reports = mongo.db.report.find()
    response = json_util.dumps(reports)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK

@app.route('/character', methods=['POST'])
def create_character():
    id = mongo.db.characters.insert_one(request.json)
    response = {"id" : str(id)}
    return response,http.HTTPStatus.CREATED

### to get all characters Get request to http://localhost:5000/characters
@app.route('/characters', methods=["GET"])
def index():
    characters = mongo.db.characters.find()
    response = json_util.dumps(characters)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK

### to get characters by id Get request to http://localhost:5000/characters/<id>
@app.route('/characters/<id>', methods=['GET'])
def getPage(id):
    character = mongo.db.characters.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(character)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK
@app.route('/characters', methods=['DELETE'])
def deleteAllcharacters():
    mongo.db.characters.drop()
    response = mongo.db.characters.find()
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK
@app.errorhandler(404)


### response default for errors
def not_found(error=None):
    message = {'message': 'Resource Not Found: ' + request.url,'status' : 404}
    return message
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)