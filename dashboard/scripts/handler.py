import pandas as pd
import sqlalchemy as sa
import os

DATABASE = 'AIDAChula'
USER = ''
PASSWORD = ''
# HOST = 'DESKTOP-637DI6V'
HOST = 'localhost'
PORT = '1433'
DRIVER = 'ODBC Driver 17 for SQL Server'

engine = sa.create_engine(
    f'mssql+pyodbc://{USER}:{PASSWORD}@{HOST}/{DATABASE}?driver={DRIVER}'
)


def colCheck(col, type):
    if col == 10 and type == "GS":
        return True
    elif col == 20 and type == "FB":
        return True
    elif col == 44 and type == "LM":
        return True
    elif col == 15 and type == "LP":
        return True
    elif col == 17 and type == "GC":
        return True
    else:
        return False


def getAllCampaign():

    query = f"""
        SELECT *
        FROM dbo.Campaign
    """
    campaign = pd.read_sql_query(query, con=engine)

    return campaign


def writeCSV(file):
    TEMPPATH = './dashboard/tmp/temp.csv'
    try:
        with open(TEMPPATH, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        df = pd.read_csv(TEMPPATH)
        return len(df.columns)
    except FileNotFoundError:
        print(os.listdir())
