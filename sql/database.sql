-- Desativar foreign_keys para evitar erros na DROP TABLE. Estas são atividades no povoar.sql
-- para garantir a integridade referencial
PRAGMA foreign_keys = off;
.mode columns
.headers on
.nullvalue NULL

DROP TABLE IF EXISTS Account;
CREATE TABLE Account (
  account_id INTEGER PRIMARY KEY,
  district_id INTEGER REFERENCES District(id),
  frequency VARCHAR(255),
  creation_year INTEGER,
  creation_month INTEGER,
  creation_day INTEGER,
  creation_date VARCHAR(255),
);

DROP TABLE IF EXISTS Card;
CREATE TABLE Card (
  card_id INTEGER PRIMARY KEY,
  disp_id INTEGER REFERENCES Disposition(disp_id),
  type VARCHAR(255),
  issued_year INTEGER,
  issued_month INTEGER,
  issued_day INTEGER,
  issued_date VARCHAR(255),
);

DROP TABLE IF EXISTS Client;
CREATE TABLE Client (
  client_id INTEGER PRIMARY KEY,
  district_id INTEGER REFERENCES District(id),
  birthdate_year INTEGER,
  birthdate_month INTEGER,
  birthdate_day INTEGER,
  sex VARCHAR(255),
  birthdate VARCHAR(255),
);

DROP TABLE IF EXISTS Disposition;
CREATE TABLE Disposition (
  disp_id INTEGER PRIMARY KEY,
  client_id INTEGER REFERENCES Client(client_id),
  account_id INTEGER REFERENCES Account(account_id),
  type VARCHAR(255),
);

DROP TABLE IF EXISTS District;
CREATE TABLE District (
  id INTEGER PRIMARY KEY,
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
  num_crimes_96 INTEGER,
  region_direction VARCHAR(255),
  city VARCHAR(255),
);

DROP TABLE IF EXISTS Loan;
CREATE TABLE Loan (
  loan_id INTEGER,
  account_id INTEGER REFERENCES Account(account_id),
  amount INTEGER,
  duration INTEGER,
  payments INTEGER,
  status INTEGER,
  loan_year INTEGER,
  loan_month INTEGER,
  loan_day INTEGER,
  loan_date VARCHAR(255),
);

DROP TABLE IF EXISTS Transactions;
CREATE TABLE Transactions (
  trans_id INTEGER,
  account_id INTEGER REFERENCES Account(account_id),
  type VARCHAR(255),
  operation REAL,
  amount REAL,
  balance REAL,
  k_symbol VARCHAR(255),
  bank VARCHAR(255),
  account REAL,
  trans_year INTEGER,
  trans_month INTEGER,
  trans_day INTEGER,
  trans_date VARCHAR(255),
);