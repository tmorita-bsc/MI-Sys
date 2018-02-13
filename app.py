from flask import Flask, request, render_template
from flask_restful import Api
from flask_jwt import JWT
from flask_bootstrap import Bootstrap

from security import authenticate, identity
from employee import EmployeeRegister
from bento import Bento, BentoList
from atdinfo import AtdData, AtdDataList

import pdb

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
bootstrap = Bootstrap(app)

jwt = JWT(app, authenticate, identity)

api.add_resource( AtdData, '/atdinfo/<string:name>/date')
api.add_resource( AtdDataList, '/atdlist/date')
api.add_resource( Bento, '/bento/<string:name>')
api.add_resource( BentoList, '/bentolist')
api.add_resource( EmployeeRegister, '/employee_register')

@app.route('/')
def layout():
    return render_template('index.html',message="message is here")

if __name__ == '__main__':
    app.run(debug=True)


