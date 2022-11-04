from flask import request
import http as http
def paginar_10(response, ix):
        characters = []
        if ix > 0 and ix <10:
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
        else:
            message = {'message': 'Resource Not Found: ' + request.url,'status' : 404},http.HTTPStatus.OK
            return message
        return characters