import sqlite3

import config

connection = sqlite3.connect(config.DB_File_address)

cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price;
""")

cursor.execute("""
    DROP TABLE stock;
""")

connection.commit()
