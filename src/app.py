from flask import Flask, Response, request
from flask_pymongo import PyMongo
import http as http
from bson import json_util, ObjectId
import json
from models.report import Report
from models.character import Character
### Inicializo Flask
app = Flask(__name__)
### Defino una propiedad que va a decir donde buscar MongoDB. MongoDB siempre trabaja en el puerto 27017
app.config['MONGO_URI']='mongodb://localhost/starwarsdb'
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
    id = mongo.db.people.insert_one(request.json)
    response = {"id" : str(id)}
    return response,http.HTTPStatus.CREATED

### to get all characters Get request to http://localhost:5000/characters
@app.route('/characters', methods=["GET"])
def index():
    characters = mongo.db.character.find()
    response = json_util.dumps(characters)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK

### to get characters by id Get request to http://localhost:5000/characters/<id>
""" @app.route('/characters/<id>', methods=['GET'])
def getPage(id):
    character = mongo.db.character.find({'_id': ObjectId(id)})
    response = json_util.dumps(character)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK
 """
@app.route('/characters/<id>', methods=['GET'])
def getCharacters(id):
    characterDB = mongo.db.people.find()
    respuesta = {"count": 82,"next": str(int(id)+1),"previous":id == "1" if None else str(int(id)-1)}
    response2 = json_util.dumps(characterDB)
    response = json.loads(response2)
    def recorrer_10(response, ix):
        characters = []
        if int(id) > 0 and int(id)<10:
            try:
                if ix == 1:
                    for i in range(0, 10):
                        character = response[i]
                        characters.append(character)
                else:
                    for i in range((10*ix)-10, (ix*10)):
                        character = response[i]
                        characters.append(character)
            except IndexError:
                    pass
        return characters
    characters = recorrer_10(response, int(id))
    respuesta['results']=characters


    return Response(json_util.dumps(respuesta), mimetype='application/json'),http.HTTPStatus.OK


### Manejador de errores
@app.errorhandler(404)


### response default for errors
def not_found(error=None):
    message = {'message': 'Resource Not Found: ' + request.url,'status' : 404}
    return message
if __name__ == "__main__":
    app.run(debug=True)