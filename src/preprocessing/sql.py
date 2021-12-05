import sqlite3
import csv
import ast

def init_db():
  connection = sqlite3.connect('./data/ac-v01.db')
  cursor = connection.cursor()

  # -- Table Account
  cursor.execute("DROP TABLE IF EXISTS account")
  cursor.execute('''CREATE TABLE account (
                      account_id INTEGER PRIMARY KEY,
                      district_id INTEGER,
                      frequency VARCHAR(255),
                      date INTEGER);
                  ''')

  contents = csv.reader(open('./data/raw/account.csv'), delimiter=';')
  insert_records = "INSERT INTO account(account_id, district_id, frequency, date) VALUES(?, ?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: insert.append([int(row[0]), int(row[1]), row[2], int(row[3])])
  cursor.executemany(insert_records, insert)

  # -- Table Card
  cursor.execute("DROP TABLE IF EXISTS card")
  cursor.execute('''CREATE TABLE card (
    card_id INTEGER PRIMARY KEY,
    disp_id INTEGER,
    type VARCHAR(255),
    issued INTEGER);''')

  contents = csv.reader(open('./data/raw/card_comp.csv'), delimiter=';')
  insert_records = "INSERT INTO card(card_id, disp_id, type, issued) VALUES(?, ?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: insert.append([int(row[0]), int(row[1]), row[2], int(row[3])])
  cursor.executemany(insert_records, insert)

  # -- Table Client
  cursor.execute("DROP TABLE IF EXISTS client")
  cursor.execute('''CREATE TABLE client (
    client_id INTEGER PRIMARY KEY,
    district_id VARCHAR(255),
    birthnumber INTEGER);''')

  contents = csv.reader(open('./data/raw/client.csv'), delimiter=';')
  insert_records = "INSERT INTO client(client_id, birthnumber, district_id) VALUES(?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: insert.append([int(row[0]), row[1], int(row[2])])
  cursor.executemany(insert_records, insert)

  # -- Table Disposition
  cursor.execute("DROP TABLE IF EXISTS disp")
  cursor.execute('''CREATE TABLE disp (
    disp_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    account_id INTEGER,
    type VARCHAR(255));''')

  contents = csv.reader(open('./data/raw/disp.csv'), delimiter=';')
  insert_records = "INSERT INTO disp(disp_id, client_id, account_id, type) VALUES(?, ?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: insert.append([int(row[0]), int(row[1]), int(row[2]), row[3]])
  cursor.executemany(insert_records, insert)

  # -- Table District
  cursor.execute("DROP TABLE IF EXISTS district")
  cursor.execute('''CREATE TABLE district (
    id INTEGER PRIMARY KEY,
    city VARCHAR(255),
    region  VARCHAR(255),
    num_inhab INTEGER,
    num_municip_inhab_0_499 INTEGER,
    num_municip_inhab_500_1999 INTEGER,
    num_municip_inhab_2000_9999 INTEGER,
    num_municip_inhab_10000_ INTEGER,
    num_cities INTEGER,
    perc_urban_inhab REAL,
    avg_salary REAL,
    perc_unemploy_95 REAL,
    perc_unemploy_96 REAL,
    enterp_per_1000 INTEGER,
    num_crimes_95 INTEGER,
    num_crimes_96 INTEGER);''')

  contents = csv.reader(open('./data/raw/district.csv'), delimiter=';')
  insert_records = "INSERT INTO district(id, city, region, num_inhab, num_municip_inhab_0_499, num_municip_inhab_500_1999, \
    num_municip_inhab_2000_9999, num_municip_inhab_10000_, num_cities, perc_urban_inhab, avg_salary, perc_unemploy_95, \
    perc_unemploy_96, enterp_per_1000, num_crimes_95, num_crimes_96) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: 
          try:
              insert.append([int(row[0]), row[1], row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), \
                  int(row[8]), float(row[9]), float(row[10]), float(row[11]), float(row[12]), int(row[13]), int(row[14]), int(row[15])])
          except Exception as e: # Handle '?'
              insert.append([int(row[0]), row[1], row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7]), \
                  int(row[8]), float(row[9]), float(row[10]), None, float(row[12]), int(row[13]), None, int(row[15])])
  cursor.executemany(insert_records, insert)

  # -- Table Loan
  cursor.execute("DROP TABLE IF EXISTS loan")
  cursor.execute('''CREATE TABLE loan (
    loan_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    date INTEGER,
    amount INTEGER,
    duration INTEGER,
    payments INTEGER,
    status INTEGER);''')

  contents = csv.reader(open('./data/raw/loan_dev.csv'), delimiter=';')
  insert_records = "INSERT INTO loan(loan_id, account_id, date, amount, duration, payments, status) \
      VALUES (?, ?, ?, ?, ?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: 
          insert.append([int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])])
  cursor.executemany(insert_records, insert)

  # -- Table Transactions
  cursor.execute("DROP TABLE IF EXISTS trans")
  cursor.execute('''CREATE TABLE trans (
    trans_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    date VARCHAR(255),
    type VARCHAR(255),
    operation REAL,
    amount REAL,
    balance REAL,
    k_symbol VARCHAR(255),
    bank VARCHAR(255),
    account INTEGER);''')

  contents = csv.reader(open('./data/raw/trans_dev.csv'), delimiter=';')
  insert_records = "INSERT INTO trans(trans_id, account_id, date, type, operation, amount, balance, k_symbol, bank, account) \
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

  insert = []
  for i, row in enumerate(contents):
      if i != 0: 
          row[7] = None if row[7] == '' else row[7]
          row[8] = None if row[8] == '' else row[8]
          row[9] = None if row[9] == '' else int(row[9])

          insert.append([int(row[0]), int(row[1]), int(row[2]), row[3], row[4], float(row[5]), float(row[6]), row[7], row[8], row[9]])
  cursor.executemany(insert_records, insert)

  connection.commit()
  connection.close()