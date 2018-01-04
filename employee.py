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

    @classmethod
    def find_max_id(cls):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        query = "SELECT MAX(id) FROM {table}".format(table=cls.TABLE_NAME)
        result = cursor.execute(query)
        res = result.fetchone()[0]
        if res:
            max_id = res
        else:
            max_id = None

        connection.close()
        return max_id

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

        # find max id in employee_table
        Employee.next_employee_id = Employee.find_max_id() + 1
        query = "INSERT INTO {table} VALUES (?, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, ( Employee.next_employee_id, employee['username'], employee['password']))

        connection.commit()
        connection.close()

        return {"message": "Employee created successfully."}, 201
