
import sqlite3

connection = sqlite3.connect('data.db')
 
 
cursor = connection.cursor()

# 1st table: id, heading, url
create_table_1 = "CREATE TABLE title_table (id int, heading text, url text)"
# 2nd table: id, location
create_table_2 = "CREATE TABLE location_table (id int,location text)"
# 3rd table: id, report id
create_table_3 = "CREATE TABLE report_id_table (id int, report_id int)"
# 4th table: TODO

# Create tables
cursor.execute(create_table_1)
cursor.execute(create_table_2)
cursor.execute(create_table_3)