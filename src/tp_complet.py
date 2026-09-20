#!/usr/bin/env python
# coding: utf-8

# In[10]:


import csv
from pathlib import Path 
PROJECT_ROOT=Path(__file__).resolve().parent.parent

#i used ai to generate the data
data = [
    [
        ["2024-03-01T09:12:00", "FR7630006000011234567890189", "FR", "BNPPARIBAS", "DE89370400440532013000", "DE", "1250.00", "EUR"],
        ["2024-03-01T10:45:00", "FR7630006000011234567890189", "FR", "BNPPARIBAS", "ES9121000418450200051332", "ES", "7400.50", "EUR"],
        ["2024-03-01T11:20:00", "FR7612345000019876543210189", "FR", "SOCGEN", "IT60X0542811101000000123456", "IT", "300.00", "EUR"],
        ["2024-03-01T14:05:00", "FR7612345000019876543210189", "FR", "SOCGEN", "BE68539007547034", "BE", "6200.00", "EUR"],
        ["2024-03-01T16:30:00", "FR7630006000011234567890189", "FR", "BNPPARIBAS", "NL91ABNA0417164300", "NL", "850.00", "EUR"],
    ],
    [
        ["2024-03-02T08:15:00", "FR7630006000011234567890189", "FR", "BNPPARIBAS", "DE89370400440532013000", "DE", "450.00", "EUR"],
        ["2024-03-02T09:50:00", "FR7611111000012345678901234", "FR", "CREDITMUTUEL", "ES9121000418450200051332", "ES", "900.00", "EUR"],
        ["2024-03-02T13:00:00", "FR7611111000012345678901234", "FR", "CREDITMUTUEL", "IT60X0542811101000000123456", "IT", "3000.00", "EUR"],
        ["2024-03-02T15:40:00", "FR7612345000019876543210189", "FR", "SOCGEN", "BE68539007547034", "BE", "700.00", "EUR"],
        ["2024-03-02T18:10:00", "FR7630006000011234567890189", "FR", "BNPPARIBAS", "NL91ABNA0417164300", "NL", "5600.00", "EUR"],
        ["2024-03-02T19:25:00", "FR7611111000012345678901234", "FR", "CREDITMUTUEL", "DE89370400440532013000", "DE", "125.00", "EUR"],
    ],
    [
        ["2024-03-03T07:45:00", "FR7622222000019876500001234", "FR", "LCL", "ES9121000418450200051332", "ES", "200.00", "EUR"],
        ["2024-03-03T10:10:00", "FR7622222000019876500001234", "FR", "LCL", "BE68539007547034", "BE", "1500.00", "EUR"],
        ["2024-03-03T12:35:00", "FR7612345000019876543210189", "FR", "SOCGEN", "IT60X0542811101000000123456", "IT", "800.00", "EUR"],
        ["2024-03-03T15:00:00", "FR7630006000011234567890189", "FR", "BNPPARIBAS", "NL91ABNA0417164300", "NL", "2500.00", "EUR"],
        ["2024-03-03T17:20:00", "FR7622222000019876500001234", "FR", "LCL", "DE89370400440532013000", "DE", "400.00", "EUR"],
    ],
]

header= [
    "datetime_transaction",
    "iban_origine",
    "pays_source",
    "banque_source",
    "iban_destinataire",
    "pays_destinataire",
    "montant",
    "devise"
        ]

def generate_data(output_dir : Path) -> list[Path] :
    output_dir.mkdir(parents=True, exist_ok=True)
    paths=[]
    for i, rows in enumerate(data):
        path=output_dir / f"transactions_{i+1}.csv"
        with open(path,"w",newline="") as file :
            writer=csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        paths.append(path)

    return paths



# In[ ]:


from decimal import Decimal, InvalidOperation
from typing import TypedDict
from datetime import datetime


class Transaction(TypedDict) :
    datetime_transaction: datetime
    iban_origine: str
    pays_source: str
    banque_source: str
    iban_destinataire: str
    pays_destinataire: str
    montant: Decimal
    devise: str

def loading_data(path : Path):
    transactions : list[Transaction]=[]
    invalid_transactions : int =0

    with open(path, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    transaction = Transaction(
                        datetime_transaction=datetime.fromisoformat(row["datetime_transaction"]),
                        iban_origine=row["iban_origine"],
                        pays_source=row["pays_source"],
                        banque_source=row["banque_source"],
                        iban_destinataire=row["iban_destinataire"],
                        pays_destinataire=row["pays_destinataire"],
                        montant=Decimal(row["montant"]),
                        devise=row["devise"],
                    )
                    transactions.append(transaction)
                except (KeyError, ValueError,InvalidOperation):
                    #print("something is off with the data entered")
                    invalid_transactions+=1

    return transactions,invalid_transactions


# In[12]:


def sum_iban_origine_sent(transactions : list[Transaction])-> dict[str,Decimal]:
    res : dict[str,Decimal]={}
    for transaction in transactions:
        if transaction["iban_origine"] not in res :
            res[transaction["iban_origine"]]=transaction["montant"]

        else : res[transaction["iban_origine"]]+=transaction["montant"]

    return res 


def sum_banque_source_sent(transactions : list[Transaction])-> dict[str,Decimal]:
    res : dict[str,Decimal]={}
    for transaction in transactions:
        if transaction["banque_source"] not in res :
            res[transaction["banque_source"]]=transaction["montant"]

        else : res[transaction["banque_source"]]+=transaction["montant"]

    return res 


def sum_iban_destinataire_received(transactions : list[Transaction])-> dict[str,Decimal]:
    res : dict[str,Decimal]={}
    for transaction in transactions:
        if transaction["iban_destinataire"] not in res :
            res[transaction["iban_destinataire"]]=transaction["montant"]

        else : res[transaction["iban_destinataire"]]+=transaction["montant"]

    return res 


def flag_montant(transactions : list[Transaction], threshold : Decimal=Decimal("5000")) -> list[bool]:
    res : list[bool]=[]

    for transaction in transactions:
        if transaction["montant"]>threshold :
            res.append(True)     
        else : res.append(False)   

    return res   


# In[13]:


# transactions_1,_ = loading_data(r"data\transactions_1.csv")
# transactions_2,_ = loading_data(r"data\transactions_2.csv")
# transactions_3,_ = loading_data(r"data\transactions_3.csv")

# transactions=transactions_1+transactions_2+transactions_3


# In[14]:


# print(len(transactions))


# In[15]:


#test
# print(sum_iban_origine_sent(transactions_1))


# In[16]:


import sqlite3

retryable_errors=sqlite3.OperationalError

def create_tables(connx : sqlite3.Connection) ->None :
    connx.execute("CREATE TABLE IF NOT EXISTS transactions (" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "datetime_transaction TEXT NOT NULL," \
    "iban_origine TEXT NOT NULL," \
    "pays_source TEXT NOT NULL," \
    "banque_source TEXT NOT NULL," \
    "iban_destinataire TEXT NOT NULL," \
    "pays_destinataire TEXT NOT NULL," \
    "montant TEXT NOT NULL," \
    "devise TEXT NOT NULL" \
    ")")

    connx.execute(
        "CREATE TABLE IF NOT EXISTS processed_files " \
    "(id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "file_hash TEXT NOT NULL UNIQUE," \
    "file_name TEXT NOT NULL)"
    )

    connx.commit()


def insert_transactions(transactions : list[Transaction],connx : sqlite3.Connection, max_error : int=3)-> None :
    rows= [
        (
            transaction["datetime_transaction"].isoformat(),
            transaction["iban_origine"],
            transaction["pays_source"],
            transaction["banque_source"],
            transaction["iban_destinataire"],
            transaction["pays_destinataire"],
            str(transaction["montant"]),
            transaction["devise"],
        )
        for transaction in transactions
    ]

    c=0
    while True:
        try:
            connx.executemany(
                "INSERT INTO transactions (datetime_transaction, iban_origine, pays_source,banque_source,iban_destinataire,pays_destinataire,montant,devise) VALUES (?,?,?,?,?,?,?,?)",rows
            )
            break

        except retryable_errors:
            c+=1
            if c> max_error : raise



# In[ ]:


import hashlib
import sys

def check_file(path:Path)->str :
    hasher=hashlib.sha256()
    with open(path,"rb") as file:
        hasher.update(file.read())

    return hasher.hexdigest()


def process_file(path :Path, connx:sqlite3.Connection)-> tuple[str,str]:
    try:
        checked_file=check_file(path)
        processed_files=connx.execute("SELECT * FROM processed_files WHERE file_hash= ?",(checked_file,)).fetchone()
        if processed_files :
            return ("skipped","message : deja traite")

        else :
            transactions,invalid_transactions=loading_data(path)
            insert_transactions(transactions,connx)
            connx.execute("INSERT INTO processed_files (file_hash, file_name) VALUES (?,?)",(checked_file,path.name))
            connx.commit()

            return ("inserted",f"message : data was inserted with {invalid_transactions} invalid transactions")

    except (OSError,sqlite3.Error):
        connx.rollback()
        return ("failed",f"message : error occurred")


def process_all_files(data_paths: list[Path], db_path : Path)-> list[tuple[str,str]]:
    connx=sqlite3.connect(db_path)
    create_tables(connx)

    all_messages : list[tuple[str,str]]=[]
    for path in data_paths:
        res=process_file(path,connx)
        all_messages.append(res)

    connx.close()

    return all_messages


def full_pipeline(data_dir : Path, db_path:Path)-> list[tuple[str,str]]:
    csv_paths=generate_data(data_dir)
    return process_all_files(csv_paths,db_path)


if __name__=="__main__":
    #res=full_pipeline(Path("data"),Path("database.db"))
    res=full_pipeline(PROJECT_ROOT / "data",PROJECT_ROOT / "database.db")
    for i,j in res:
        print(f"{i} {j}")

    exit_code=1 if any(i=="failed" for i,_ in res) else 0
    sys.exit(exit_code)





# In[ ]:





# In[ ]:


# import sqlite3
# c = sqlite3.connect("database.db")
# print(c.execute("SELECT COUNT(*) FROM transactions").fetchone())
# print(c.execute("SELECT COUNT(*) FROM processed_files").fetchone())

# c.close()

