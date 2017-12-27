#/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from flask_restful import Resource, reqparse


class Employee(Resource):
    TABLE_NAME = "employee_table"

    def __init__(self, e_id, e_name, e_password):
        self.e_id = e_id
        self.e_name = e_name
        self.e_password = e_password

    @classmethod
    def find_by_e_name(cls, e_name):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE username=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (e_name,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_e_id(cls, e_id):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE id=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (e_id,))
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
    parser.add_argument('e_name',
            type=str,
            required=True,
            help="This field cannnot be left blank!"
            )
    parser.add_argument('e_password',
            type=str,
            required=True,
            help="This field cannnot be left blank!"
            )

    def post(self):
        employee = EmployeeRegister.parser.parse_args()

        if Employee.find_by_e_name(employee['e_name']):
            return {"message": "Employee with that name already exists."}, 400

        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        # self.TABLENAME is OK?
        query = "INSERT INTO {table} VALUES (NULL, ?, ?)".format(table=self.TABLE_NAME)
        cursor.execute(query, (employee['e_name'], employee['e_password']))

        connection.commit()
        connection.close()

        return {"message": "Employee created successfully."}, 201
