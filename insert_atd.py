
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

    #@jwt_required()
    def get(self, name):
        atd_info = self.find_by_name(name)
        if atd_info:
            return atd_info
        return {'message': 'User not Found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'atd_info': { 'name': row[0], 'arrival_time': row[1], 'leave_time': row[2]}}
            #return {'atd_info': { 'name': row[0], 'date': row[1], 'a_day_of_the_week': row[2], \
            #        'holiday': row[3], 'arrival_time': row[4], 'leave_time': row[5], \
            #        'is_paid_holiday': row[6], 'is_compensatory': row[7]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An atd_info with name '{}' already exist.".format(name)}

        # need help   this func can parse comand-line args
        atd_info = AtdData.parser.parse_args()

        insert_atdinfo = {'name': name, 'arrival_time': atd_info['arrival_time'], \
                'leave_time': atd_info['leave_time']}

        try:
            AtdData.insert(insert_atdinfo)
        except:
            return {"message": "An error occurred inserting the atd_info."}

        return insert_atdinfo
    
    @classmethod
    def insert(cls, insert_atdinfo):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO {table} VALUE(?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (insert_atdinfo['name'], insert_atdinfo['arrival_time'], insert_atdinfo['leave_time']))

        connedtion.commit()
        connedtion.close()

    #@jwt_required()
    def put(self, name):
        atd_info = AtdData.parser.parse_args() 
        prev_atdinfo = self.find_by_name(name)
        update_atdinfo = {'name': name, 'arrival_time': atd_info['arrival_time'], 'leave_time': atd_info['leave_time']}

        if prev_atdinfo is None:
            try:
                AtdData.insert(update_atdinfo)
            except:
                return {"message" : "An error occurred inserting the atd_info."}
        else:
            try:
                Item.update(update_atdinfo)
            except:
                raise
                return {"message" : "An error occured updating the atd_info."}

        return update_atdinfo

    @classmethod
    def update(cls, atd_info):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "UPDATE {table} SET arrival_time=? leave_time=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute( query, (atd_info['arrival_time'], atd_info['leave_time']))

        connection.commit()
        connection.close()


class AtdDataList(Resource):
    TABLE_NAME = 'atd_table'

    def get(self):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)

        atd_infolist = []
        
        for row in result:
            atd_infolist.append({'name': row[0], 'arrival_time': row[1], 'leave_time': row[2]})

        connection.close()

        return {'atd_infolist':atd_infolist}
