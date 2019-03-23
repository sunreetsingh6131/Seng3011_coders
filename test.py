import sqlite3
from sqlite3 import Error
 
 connection = sqlite3.connect('data.db')
 
 
 cursor = connection.cursor()
 
create_table = "CREATE TABLE title_table (id int, title text)"
cursor.execute(create_table)