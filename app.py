from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from employee import EmployeeRegister
from insert_atd import AtdData, AtdDataList


app = Flask(__name__)
app.security_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource( AtdData, '/atdinfo/<string:name>')
api.add_resource( AtdDataList, '/atdlist')
api.add_resource( EmployeeRegister, '/employee_register')

if __name__ == '__main__':
    app.run(debug=True)
