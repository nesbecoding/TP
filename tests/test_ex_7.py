#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"src"))

from tp_complet import Transaction, insert_transactions
from datetime import datetime
from decimal import Decimal
import sqlite3
from types import SimpleNamespace

def test_retry():
    transaction : Transaction ={
        "datetime_transaction": datetime(2024, 3, 1, 9, 0),
        "iban_origine": "FR001",
        "pays_source": "FR",
        "banque_source": "BNPPARIBAS",
        "iban_destinataire": "DE001",
        "pays_destinataire": "DE",
        "montant": Decimal("500.00"),
        "devise": "EUR",
    }


    calls=[]
    def executemany(*args: object, **kwargs: object):
        calls.append(1)

        if len(calls)==1 : raise sqlite3.OperationalError("db is locked")

    connx=SimpleNamespace(executemany=executemany)

    insert_transactions([transaction], connx,max_error=1)

    assert len(calls)==2

