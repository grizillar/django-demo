import pandas as pd
import sqlalchemy as sa
import pyodbc
import dashboard.scripts.dbmap as dbmap
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


def applyDate(df, date):
    if "date" in df.columns:
        df["date"] = date
    return df


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


def getCampaignLength():
    query = f"""
        SELECT COUNT(cid)
        FROM dbo.Campaign
    """
    return int(pd.read_sql_query(query, con=engine).iloc[0])


def getSitetrafficLength():
    query = f"""
        SELECT COUNT(sid)
        FROM dbo.SiteTraffic
    """
    return int(pd.read_sql_query(query, con=engine).iloc[0])


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


def insertCampaign(df):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+HOST +
                          ';DATABASE='+DATABASE+';UID='+USER+';PWD=' + PASSWORD)
    cursor = cnxn.cursor()

    df['cid'] = df['cid'] + getCampaignLength()
    df.rename(columns={'name': 'cname'}, inplace=True)

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO dbo.Campaign (date, cid, name, pid, spending, reach, impression, engagement, objective, video_view, landing_page_view, product_view, add_to_cart, purchase, dateadded) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       row.date, row.cid, row.cname, row.pid, row.spending, row.reach, row.impression, row.engagement, row.objective, row.video_view, row.landing_page_view, row.product_view, row.add_to_cart, row.purchase, row.dateadded)

    cnxn.commit()
    cursor.close()


def insertSiteTraffic(df):
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+HOST +
                          ';DATABASE='+DATABASE+';UID='+USER+';PWD=' + PASSWORD)
    cursor = cnxn.cursor()

    df['sid'] = df['sid'] + getSitetrafficLength()
    df.rename(columns={'name': 'cname'}, inplace=True)

    for index, row in df.iterrows():
        cursor.execute("INSERT INTO dbo.SiteTraffic (sid, pid, uri, all_user, new_user, order_count, revenue, dateadded) values (?,?,?,?,?,?,?,?)",
                       row.sid, row.pid, row.uri, row.all_user, row.new_user, row.order_count, row.revenue, row.dateadded)

    cnxn.commit()
    cursor.close()
