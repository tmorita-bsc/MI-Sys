
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request

import sqlite3

harapeko = ["なし", "からあげ弁当", "日替わり弁当"]

class Bento(Resource):
    TABLE_NAME = 'bento_table'

    parser = reqparse.RequestParser()
    parser.add_argument('order_bento_id',
            type=int,
            required=True,
            help="This field cannot be left blank!"
            )
    parser.add_argument('o_mori',
            type=int,
            required=True,
            help="This field cannot be left blank!"
            )

    def get(self, name):
        bento_info = self.find_by_name(name)
        if bento_info:
            return bento_info
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
            return {'bento_info': { 'name': row[0], 'order_bento_id': harapeko[int(row[1])], 'o_mori': row[2]}}

    def delete(self, name):
        # not delete , just initialize
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "UPDATE {table} SET order_bento_id=? WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute( query, (0, name))
        query = "UPDATE {table} SET o_mori=? WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute( query, (0, name))

        connection.commit()
        connection.close()

    def put(self, name): # update leave_time
        # need user name
        bento_info = Bento.parser.parse_args() 
        prev_bentoinfo = self.find_by_name(name)
        
        if prev_bentoinfo is None:
            try:
                update_bentoinfo = {'name': name, 'order_bento_id': bento_info['order_bento_id'], 'o_mori': bento_info['o_mori']}

                Bento.insert(update_bentoinfo)
            except:
                return {"message" : "An error occurred inserting the bento_info."}
        else:
            try:
                if bento_info['order_bento_id'] is "":
                    bento_info['order_bento_id'] = prev_bentoinfo['order_bento_id']
                elif bento_info['o_mori'] is "":
                    bento_info['o_mori'] = prev_bentoinfo['o_mori']

                update_bentoinfo = {'name': name, 'order_bento_id': bento_info['order_bento_id'], 'o_mori': bento_info['o_mori']}

                Bento.update(update_bentoinfo)
            except:
                raise
                return {"message" : "An error occured updating the bento_info."}

        return update_bentoinfo

    @classmethod
    def insert(cls, bento_info): # insert arrival_time
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO {table} VALUES(?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (bento_info['name'], bento_info['order_bento_id'], bento_info['o_mori']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, bento_info):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()
        
        query = "UPDATE {table} SET order_bento_id=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute( query, (bento_info['order_bento_id'], bento_info['name']))
        query = "UPDATE {table} SET o_mori=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute( query, (bento_info['o_mori'], bento_info['name']))

        connection.commit()
        connection.close()


class BentoList(Resource):
    TABLE_NAME = 'bento_table'

    def get(self):
        connection = sqlite3.connect('atd_info.db')
        cursor = connection.cursor()

        query = "SELECT order_bento_id, count(*), sum(o_mori) FROM {table} GROUP BY order_bento_id".format(table=self.TABLE_NAME)
        result = cursor.execute(query)

        bento_infolist = []
        o_mori_count = 0
        
        for row in result:
            o_mori_count += row[2]
            bento_infolist.append({'order_bento_id': harapeko[int(row[0])], 'count': row[1]})

        bento_infolist.append({'total_o_mori':o_mori_count})

        connection.close()

        return {'bento_infolist':bento_infolist}
