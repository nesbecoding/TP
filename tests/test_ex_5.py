#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from decimal import Decimal
import sqlite3
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"src"))

from tp_complet import data, full_pipeline


#testing the nb of inserted lines
def test_nb_inserted_lines():
    connx=sqlite3.connect("database.db")
    nb_lines_data : int=0
    for file_rows in data:
        for row in file_rows:
            nb_lines_data+=1

    nb_lines_db : int=0
    nb_lines_db=connx.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    # print("nb_lines_data",nb_lines_data)
    # print("nb_lines_db",nb_lines_db)

    assert nb_lines_db==nb_lines_data


#testing the total iban
def test_total_iban():
    connx=sqlite3.connect("database.db")
    #checking the data
    totals_data: dict[str,Decimal]={}
    for file_rows in data:
        for row in file_rows:
            iban,montant=row[1],Decimal(row[6])
            if iban not in list(totals_data.keys()): totals_data[iban]=montant
            else : totals_data[iban]+=montant

    #checking the db
    totals_db : dict[str,Decimal]={}
    for iban_origine, montant in connx.execute("SELECT iban_origine,montant FROM transactions"):
        if iban_origine not in list(totals_db.keys()): totals_db[iban_origine]=Decimal(montant)
        else : totals_db[iban_origine]+=Decimal(montant)

    # print("totals_data",totals_data)
    # print("totals_db",totals_db)
    assert totals_data==totals_db


# testing the nb of transaction>5000
def test_transactions_5000():
    connx=sqlite3.connect("database.db")
    nb_transactions_data : int=0
    for file_rows in data:
        for row in file_rows:
            if Decimal(row[6])>5000 : nb_transactions_data+=1

    nb_transactions_db : int=0
    nb_transactions_db=connx.execute("SELECT COUNT(*) FROM transactions WHERE CAST (montant AS REAL)>5000").fetchone()[0]

    # print("nb_transactions_data",nb_transactions_data)
    # print("nb_transactions_db",nb_transactions_db)

    assert nb_transactions_data==nb_transactions_db

#testing that rerunning the code wont insert extra lines
def test_rerun_code_no_line_insertion():
    connx=sqlite3.connect("database.db")
    # e=full_pipeline(Path("data"),Path("database.db"))
    nb_rows_db : int=0
    nb_rows_db=connx.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    nb_rows_data: int=0
    for file_rows in data:
        for row in file_rows: nb_rows_data+=1

    # print("nb_rows_db",nb_rows_db)
    # print("nb_rows_data",nb_rows_data)

    assert nb_rows_db==nb_rows_data




