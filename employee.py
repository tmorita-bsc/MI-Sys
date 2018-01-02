#/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from flask_restful import Resource, reqparse

class Employee(Resource):
    TABLE_NAME = "employee_table"

    def __init__(self, _id, username, password):
        self.id = _id
        self.name = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class EmployeeRegister(Resource):
    TABLE_NAME = "employee_table"

    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannnot be left blank!"
            )
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannnot be left blank!"
            )

    def post(self):
        employee = EmployeeRegister.parser.parse_args()

        if Employee.find_by_username(employee['username']):
            return {"message": "Employee with that name already exists."}, 400

        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        # self.TABLENAME is OK?
        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, ( employee['username'], employee['password']))

        connection.commit()
        connection.close()

        return {"message": "Employee created successfully."}, 201
