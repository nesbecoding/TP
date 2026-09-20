#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# detecting a failure and not touching the db

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"src"))
from tp_complet import process_all_files
import sqlite3

def test_integration():
    test_csv=Path("this_file_does_not_exist.csv")
    db_path=Path("database.db")

    #before trying to insert something thats not compatible
    connx=sqlite3.connect(db_path)
    count_beofre_insert_transactions=connx.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    res=process_all_files([test_csv],db_path)
    exist=0
    for i in res:
        if i[0]=="inserted": exist +=1


    #after trying to insert something thats not compatible
    count_after_insert_transactions=connx.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]

    # print("count_beofre_insert_transactions",count_beofre_insert_transactions)
    # print("count_after_insert_transactions",count_after_insert_transactions)

    assert exist==0
    assert count_beofre_insert_transactions==count_after_insert_transactions

