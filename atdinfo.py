
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request

import sqlite3
import datetime

# make weekdays
weekdays = ["月", "火", "水", "木", "金", "土", "日"]

class AtdData(Resource):
    TABLE_NAME = 'atd_table'

    #@jwt_required()
    def get(self, name):
        # get query parameters
        atd_info = self.find_by_name(name, request.args)

        if atd_info:
            return atd_info
        return {'message': 'User not Found'}, 404

    @classmethod
    def find_by_name(cls, name, params):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        search_date = params['year'] + "-" + params['month'] + "-" + params['day']

        query = "SELECT * FROM {table} WHERE date=? AND name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (search_date, name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {\
                    'atd_info': { \
                    'name': row[0], \
                    'date': row[1], \
                    'weekday': row[2], \
                    'arrival_time': row[3], \
                    'leave_time': row[4] \
                    } \
                }

    def post(self, name):
        if self.find_by_name(name, request.args):
            return {'message': "An atd_info with name '{}' already exist.".format(name)}

        insert_atdinfo = { \
                "name": name, \
                "date": self.get_time().strftime("%Y-%m-%d"), \
                "weekday": weekdays[self.get_time().weekday()], \
                "arrival_time": self.get_time().strftime("%H:%M") , \
                "leave_time": "" \
                }

        try:
            AtdData.insert(insert_atdinfo)
        except:
            return {"message": "An error occurred inserting the atd_info."}

        return insert_atdinfo

    def get_time(self):
        return datetime.datetime.now()

    # dummy
    #def get_time(self):
        # return datetime.date(2017, 1, 8)  # sunday
        #return datetime.date(2018, 1, 12)  # holiday monday
    
    @classmethod
    def insert(cls, insert_atdinfo): # insert arrival_time
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO {table} VALUES(?, ?, ?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (insert_atdinfo['name'], \
                insert_atdinfo['date'], \
                insert_atdinfo['weekday'], \
                insert_atdinfo['arrival_time'], \
                insert_atdinfo['leave_time'] \
                ))

        connection.commit()
        connection.close()

    #@jwt_required()
    def delete(self, name):
        # not delete , just initialize
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        params = request.args
        search_date = params['year'] + "-" + params['month'] + "-" + params['day']

        query = "UPDATE {table} SET arrival_time=?, leave_time=? WHERE name=? AND date=?".format(table=self.TABLE_NAME)
        cursor.execute( query, ("", "", name, search_date ))

        connection.commit()
        connection.close()

        return 

    #@jwt_required()
    def put(self, name): # update leave_time
        prev_atdinfo = self.find_by_name(name, request.args)
        ##return prev_atdinfo['atd_info']['date']

        if prev_atdinfo is None or prev_atdinfo['atd_info']['date'] < self.get_time().strftime("%Y-%m-%d"):
            try:
                update_atdinfo = { \
                        'name': name, \
                        'date': self.get_time().strftime("%Y-%m-%d"), \
                        "weekday": weekdays[self.get_time().weekday()], \
                        'arrival_time': self.get_time().strftime("%H:%M"), \
                        'leave_time': "" \
                        }
                AtdData.insert(update_atdinfo)
            except:
                return {"message" : "An error occurred inserting the atd_info."}

        elif prev_atdinfo['atd_info']['date'] == self.get_time().strftime("%Y-%m-%d"):
            try:
                update_atdinfo = { \
                        'name': name, \
                        'leave_time': self.get_time().strftime("%H:%M")
                        }
                AtdData.update(update_atdinfo)
            except:
                return {"message" : "An error occured updating the atd_info."}

        else:
            return {"message" : "ERROR"}

        return update_atdinfo

    @classmethod
    def update(cls, atd_info):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        params = request.args
        search_date = params['year'] + "-" + params['month'] + "-" + params['day']
        
        query = "UPDATE {table} SET leave_time=? WHERE name=? AND date=?".format(table=cls.TABLE_NAME)
        cursor.execute( query, (atd_info['leave_time'], atd_info['name'], search_date))

        connection.commit()
        connection.close()


class AtdDataList(Resource):
    TABLE_NAME = 'atd_table'

    def get(self):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        params = request.args
        search_date = params['year'] + "-" + params['month'] + "-" + params['day']

        query = "SELECT * FROM {table} WHERE date=?".format(table=self.TABLE_NAME)
        result = cursor.execute(query, (search_date,))

        atd_infolist = []
        
        for row in result:
            atd_infolist.append({ \
                    'name': row[0], \
                    'date': row[1], \
                    'weekday': row[2], \
                    'arrival_time': row[3], \
                    'leave_time': row[4] \
                    })

        connection.close()

        return {'atd_infolist':atd_infolist}
