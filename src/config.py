import pyodbc
import json
import os

def config_connection():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=pricebuddydemo.database.windows.net;"
        "Database=PriceBuddyDemo;"
        "uid=lfmont;"
        "pwd=pass@word1"
    )