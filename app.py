from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from employee import EmployeeRegister
from bento import Bento, BentoList
from atdinfo import AtdData, AtdDataList

import pdb

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource( AtdData, '/atdinfo/today/<string:name>')
#api.add_resource( AtdData, '/atdinfo/<string:date>/<string:name>')
api.add_resource( AtdDataList, '/atdlist/today')
#api.add_resource( AtdDataList, '/atdlist/<string:date>')
api.add_resource( Bento, '/bento/<string:name>')
api.add_resource( BentoList, '/bentolist')
api.add_resource( EmployeeRegister, '/employee_register')

if __name__ == '__main__':
    app.run(debug=True)
