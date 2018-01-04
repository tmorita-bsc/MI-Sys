import sqlite3

connection = sqlite3.connect('atd_info.db')

cursor = connection.cursor()

# create table_name( elements)
create_table = "CREATE TABLE IF NOT EXISTS employee_table (id INTEGER KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS atd_table (name text, date text, weekday text, arrival_time text, leave_time text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS bento_table (name text, order_bento_id text, o_mori text)"
cursor.execute(create_table)

connection.commit()
connection.close()
