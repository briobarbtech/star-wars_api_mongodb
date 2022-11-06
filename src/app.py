from flask import Flask, Response, request
from flask_pymongo import PyMongo
import http as http
from bson import json_util, ObjectId
import json
from models.resources import paginar_10

app = Flask(__name__)
### Defino una propiedad que va a decir donde buscar MongoDB. MongoDB siempre trabaja en el puerto 27017
app.config['MONGO_URI']='mongodb://mydb/starwarsdb'
### Le paso la configuración de mi app a PyMongo
mongo = PyMongo(app)

### to create a character POST request to http://localhost:5000/character
@app.route('/character', methods=['POST'])
def create_character():
    id = mongo.db.people.insert_one(request.json)
    response = {"id" : str(id)}
    return response,http.HTTPStatus.CREATED

### to get character's page by id Get request to http://localhost:5000/characters/<id>
@app.route('/people/page=<id>', methods=['GET'])
def getCharacters(id):
    characters_data = mongo.db.people.find()
    response = {"count": 0,"next": str(int(id)+1),"previous":str(int(id)-1)}
    characters_data_list = json.loads(json_util.dumps(characters_data))
    characters = paginar_10(characters_data_list, int(id))
    response['count']=len(characters_data_list)
    response['results']=characters
    response = json_util.dumps(response)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK

### to get character's page by id Get request to http://localhost:5000/characters/<id>
@app.route('/people/<id>', methods=['GET'])
def getCharacterById(id):
    characters_data = mongo.db.people.find()
    response = {}
    characters_data_list = json.loads(json_util.dumps(characters_data))
    response = characters_data_list[int(id)-1]
    response = json_util.dumps(response)
    return Response(response, mimetype='application/json'),http.HTTPStatus.OK

### Manejador de errores
@app.errorhandler(404)
### response default for errors
def not_found(error=None):
    message = {'message': 'Resource Not Found: ' + request.url,'status' : 404}
    return message

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)