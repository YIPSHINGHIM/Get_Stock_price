import os
import sqlite3

import config

os.system("rm -rf app.db")

connection = sqlite3.connect(config.DB_File_address)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS US_stock(
	id INTEGER PRIMARY KEY,
	symbol TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL,
	buying_date DATE NOT NULL

);
    """
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS UK_stock(
	id INTEGER PRIMARY KEY,
	symbol TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL,
	buying_date DATE NOT NULL
);
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Crypto(
	id INTEGER PRIMARY KEY,
	symbol TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL,
	buying_date DATE NOT NULL

);
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS US_stock_price(
	id INTEGER PRIMARY KEY,
	US_stock_id INTEGER,
	date DATETIME,
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume FLOAT,
	FOREIGN KEY (US_stock_id) REFERENCES US_stock (id)
);
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS UK_stock_price(
	id INTEGER PRIMARY KEY,
	UK_stock_id INTEGER,
	date DATETIME,
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume FLOAT,
	FOREIGN KEY (UK_stock_id) REFERENCES stock (UK_stock_price)
);
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Crypto_price(
	id INTEGER PRIMARY KEY,
	Crypto_id INTEGER,
	date DATETIME,
	open FLOAT,
	high FLOAT,
	low FLOAT,
	close FLOAT,
	volume FLOAT,
	FOREIGN KEY (Crypto_id) REFERENCES Crypto (id)
);
    """
)

connection.commit()
# print("done")
