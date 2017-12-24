
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class AtdData(Resource):
    TABLE_NAME = 'atd_table'

    parser = reqparse.RequestParser()
    parser.add_argument('name',
            type=str,
            required=True,
            help="This field cannot be left blank!"
            )

    @jwt_required()
    def get(self, name):
        atd_data = self.find_by_name(name)
        if atd_data:
            return atd_data
        return {'message': 'User not Found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('atd_data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connedtion.close()

        if row:
            return {'atd_data': { 'name': row[0], 'arrival_time': row[1], 'leave_time': row[2]}}
            #return {'atd_data': { 'name': row[0], 'date': row[1], 'a_day_of_the_week': row[2], \
            #        'holiday': row[3], 'arrival_time': row[4], 'leave_time': row[5], \
            #        'is_paid_holiday': row[6], 'is_compensatory': row[7]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An atd_data with name '{}' already exist.".format(name)}

        atd_data = AtdData.parser.parse_args()

        insertdb_item = {'name': name, 'arrival_time': atd_data['arrival_time'], \
                'leave_time': atd_data['leave_time']}

        try:
            AtdData.insert(insertdb_item)
        except:
            return {"message": "An error occurred inserting the item."}

        return insertdb_item
    
    @classmethod
    def insert(cls, insertdb_item):
        connection = sqlite3.connect('atd_data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO {table} VALUE(?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (insertdb_item['name'], insertdb_item['arrival_time'], insertdb_item['leave_time']))

        connedtion.commit()
        connedtion.close()
