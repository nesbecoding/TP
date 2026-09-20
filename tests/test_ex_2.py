#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime
from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/"src"))

from tp_complet import (
    Transaction,
    sum_iban_origine_sent,
    sum_banque_source_sent,
    sum_iban_destinataire_received,
    flag_montant,
    loading_data

)

#used ai to generate data

#testing sum_iban_origine_sent
def test_sum_iban_origine_sent():
    transactions : list[Transaction] =[
        {
            "datetime_transaction": datetime(2024, 3, 1, 9, 0),
            "iban_origine": "FR001",
            "pays_source": "FR",
            "banque_source": "BNPPARIBAS",
            "iban_destinataire": "DE001",
            "pays_destinataire": "DE",
            "montant": Decimal("100.00"),
            "devise": "EUR",
        },
        {
            "datetime_transaction": datetime(2024, 3, 1, 10, 0),
            "iban_origine": "FR001",
            "pays_source": "FR",
            "banque_source": "BNPPARIBAS",
            "iban_destinataire": "IT001",
            "pays_destinataire": "IT",
            "montant": Decimal("50.00"),
            "devise": "EUR",
        },
        {
            "datetime_transaction": datetime(2024, 3, 1, 11, 0),
            "iban_origine": "FR002",
            "pays_source": "FR",
            "banque_source": "SOCGEN",
            "iban_destinataire": "DE001",
            "pays_destinataire": "DE",
            "montant": Decimal("30.00"),
            "devise": "EUR",
        },
    ] 

    assert sum_iban_origine_sent(transactions)=={
        "FR001" : Decimal("150.00"),
        "FR002" : Decimal("30.00")
    }


# testing sum_banque_source_sent
def test_sum_banque_source_sent():
    transactions: list[Transaction] = [
            {
                "datetime_transaction": datetime(2024, 3, 1, 9, 0),
                "iban_origine": "FR001",
                "pays_source": "FR",
                "banque_source": "BNPPARIBAS",
                "iban_destinataire": "DE001",
                "pays_destinataire": "DE",
                "montant": Decimal("200.00"),
                "devise": "EUR",
            },
            {
                "datetime_transaction": datetime(2024, 3, 2, 5, 0),
                "iban_origine": "FR001",
                "pays_source": "FR",
                "banque_source": "BNPPARIBAS",
                "iban_destinataire": "DE001",
                "pays_destinataire": "DE",
                "montant": Decimal("100.00"),
                "devise": "EUR",
            },
            {
                "datetime_transaction": datetime(2024, 3, 1, 10, 0),
                "iban_origine": "FR002",
                "pays_source": "FR",
                "banque_source": "SOCGEN",
                "iban_destinataire": "IT001",
                "pays_destinataire": "IT",
                "montant": Decimal("75.00"),
                "devise": "EUR",
            },
        ]

    assert sum_banque_source_sent(transactions)=={
        "BNPPARIBAS": Decimal("300.00"),
        "SOCGEN": Decimal("75.00")
    }


#test sum_iban_destinataire_received 
def test_sum_iban_destinataire_received():
    transactions: list[Transaction] = [
            {
                "datetime_transaction": datetime(2024, 3, 1, 9, 0),
                "iban_origine": "FR001",
                "pays_source": "FR",
                "banque_source": "BNPPARIBAS",
                "iban_destinataire": "DE001",
                "pays_destinataire": "DE",
                "montant": Decimal("500.00"),
                "devise": "EUR",
            },
    {
                "datetime_transaction": datetime(2024, 5, 3, 12, 0),
                "iban_origine": "FR002",
                "pays_source": "FR",
                "banque_source": "SOCGEN",
                "iban_destinataire": "DE001",
                "pays_destinataire": "DE",
                "montant": Decimal("200.00"),
                "devise": "EUR",
            },
            {
                "datetime_transaction": datetime(2024, 3, 1, 10, 0),
                "iban_origine": "FR002",
                "pays_source": "FR",
                "banque_source": "SOCGEN",
                "iban_destinataire": "DE001",
                "pays_destinataire": "DE",
                "montant": Decimal("300.00"),
                "devise": "EUR",
            },
        ]


    assert sum_iban_destinataire_received(transactions)=={
            "DE001":Decimal("1000.00")
        }


#test flag_montant
def test_flag_montant():
    transactions: list[Transaction] = [
            {
                "datetime_transaction": datetime(2024, 3, 1, 9, 0),
                "iban_origine": "FR001",
                "pays_source": "FR",
                "banque_source": "BNPPARIBAS",
                "iban_destinataire": "DE001",
                "pays_destinataire": "DE",
                "montant": Decimal("6000.00"),
                "devise": "EUR",
            },
            {
                "datetime_transaction": datetime(2024, 3, 1, 10, 0),
                "iban_origine": "FR001",
                "pays_source": "FR",
                "banque_source": "BNPPARIBAS",
                "iban_destinataire": "IT001",
                "pays_destinataire": "IT",
                "montant": Decimal("100.00"),
                "devise": "EUR",
            },
        ]

    assert flag_montant(transactions)==[True,False]




# In[ ]:


"""
loading testing
"""

from pathlib import  Path

test_csv=Path("checking.csv")

#testing inserting a valid row 
def test_insert_valid_row():
        test_csv.write_text("datetime_transaction,iban_origine,pays_source,banque_source,"
                "iban_destinataire,pays_destinataire,montant,devise\n"
                "2024-03-01T09:12:00,FR001,FR,BNPPARIBAS,DE001,DE,1250.00,EUR\n")

        transactions, invalid_count=loading_data(test_csv)

        assert invalid_count==0
        assert len(transactions)==1

#testing inserting a row with an invalid montant
def test_insert_invalid_amount():
        test_csv.write_text(
                "datetime_transaction,iban_origine,pays_source,banque_source,"
                "iban_destinataire,pays_destinataire,montant,devise\n"
                "2024-03-01T09:12:00,FR001,FR,BNPPARIBAS,DE001,DE,text,EUR\n")

        transactions, invalid_count=loading_data(test_csv)

        assert invalid_count==1
        assert len(transactions)==0


#testing an invalid date
def test_invalid_date():

        test_csv.write_text(
                "datetime_transaction,iban_origine,pays_source,banque_source,"
                "iban_destinataire,pays_destinataire,montant,devise\n"
                "12/12/2012,FR001,FR,BNPPARIBAS,DE001,DE,text,EUR\n")


        transactions, invalid_count=loading_data(test_csv)

        assert invalid_count==1
        assert len(transactions)==0


#testing a missing column
def test_insert_missing_column():
        test_csv.write_text(
                "datetime_transaction,iban_origine,pays_source,banque_source,"
                "iban_destinataire,pays_destinataire,montant,devise\n"
                "FR001,FR,BNPPARIBAS,DE001,DE,text,EUR\n")


        transactions, invalid_count=loading_data(test_csv)

        assert invalid_count==1
        assert len(transactions)==0

