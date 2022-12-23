import pandas as pd
import sqlalchemy as sa

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


def getAllCampaign():

    query = f"""
        SELECT *
        FROM dbo.Campaign
    """
    campaign = pd.read_sql_query(query, con=engine)

    return campaign
