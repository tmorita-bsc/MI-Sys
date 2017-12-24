#/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from flask_restful import Resource, reqparse


class Employee(Resource):
    TABLE_NAME = "employees"

    def __init__(self, e_id, e_name, e_password):
        self.e_id = e_id
        self.e_name = e_name
        self.e_password = e_password

    @classmethod
    def find_by_e_name(cls, name):
        connection = mysql.connector.connect( user='smart', password='igap', host='localhost', database='register_employee')
        cur = conn.cursor()

        cur.execute("select
