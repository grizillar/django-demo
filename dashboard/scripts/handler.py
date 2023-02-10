import pandas as pd
import sqlalchemy as sa
import pyodbc
import dashboard.scripts.dbmap as dbmap
import os
from datetime import date

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


def listToSQLString(lst):
    if (type(lst) is list):
        if len(lst) == 0:
            return "('0')"
        query_str = "("
        for i in range(len(lst)):
            query_str = query_str + "'" + lst[i] + "'"
            if i != len(lst) - 1:
                query_str = query_str + ","
        query_str = query_str + ")"
        return query_str
    return lst


def normalizeQueryParams(startdate=None, enddate=None, platform=None):
    if startdate == None or startdate == "":
        startdate = "2000-1-1"
    if enddate == None or enddate == "":
        enddate = date.today()

    if platform == None:
        platform = "('1','2','3','4','5','6','7')"
    elif platform == ['']:
        platform = "('0')"

    return (startdate, enddate, platform)


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


def getSiteTrafficLength():
    query = f"""
        SELECT COUNT(sid)
        FROM dbo.SiteTraffic
    """
    return int(pd.read_sql_query(query, con=engine).iloc[0])


def getAllSummary(startdate=None, enddate=None, platform=None):

    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f"""
        SELECT t2.pid, t2.[platform_name], t1.spending, t1.reach, t1.impression, t1.engagement, t2.[user], t2.[new_user], t2.[order], t2.revenue
        FROM 
        (
            SELECT p.pid as 'pid', p.platform_name as 'platform_name', sum(c.spending) as 'spending', sum(c.reach) as 'reach', sum(c.impression) as 'impression', sum(c.engagement)  as 'engagement'
            FROM dbo.Campaign as c JOIN dbo.Platform as p ON c.pid = p.pid
            WHERE c.date BETWEEN '{startdate}' AND '{enddate}' AND p.pid IN {platform}
            GROUP BY p.pid, p.platform_name
        ) t1
        RIGHT OUTER JOIN
        (
            SELECT p.pid as 'pid', p.platform_name as 'platform_name', sum(s.all_user) as 'user', sum(s.new_user) as 'new_user', sum(s.order_count) as 'order', sum(s.revenue)  as 'revenue'
            FROM dbo.SiteTraffic as s JOIN dbo.Platform as p ON s.pid = p.pid
            WHERE p.pid IN {platform}
            GROUP BY p.pid, p.platform_name
        ) t2
        ON t1.pid = t2.pid
    """
    summary = pd.read_sql_query(query, con=engine)

    return summary


def getCostPerResult(startdate=None, enddate=None, platform=None):
    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString([p for p in platform if "1" == p or "2" == p])

    query = f"""
        SELECT c.objective, 
            ROUND(SUM(c.spending),0) as 'spending', 
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.reach), 0), 3) as 'cost/reach', 
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.impression), 0), 3) as 'cost/impression', 
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.engagement), 0), 3) as 'cost/engagement',
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.video_view), 0), 3) as 'cost/video_view',
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.landing_page_view), 0), 3) as 'cost/landing_page_view',
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.product_view), 0), 3) as 'cost/product_view',
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.add_to_cart), 0), 3) as 'cost/add_to_cart',
            ROUND(SUM(c.spending)/ NULLIF(SUM(c.purchase), 0), 3) as 'cost/purchase'
        FROM dbo.Campaign as c
        WHERE c.pid IN {platform} AND c.objective != '0' AND c.objective != 'actions:onsite_conversion.messaging_conversation_started_7d' AND c.objective != 'actions:rsvp' AND c.objective != 'estimated_ad_recallers' AND c.date BETWEEN '{startdate}' AND '{enddate}'
        GROUP BY c.objective
        ORDER BY CASE c.objective
            WHEN 'reach' THEN 1
            WHEN 'engagement' THEN 2
            WHEN 'video_thruplay' THEN 3
            WHEN 'link_click' THEN 4
            WHEN 'view_product' THEN 5
            WHEN 'add_to_cart' THEN 6
            WHEN 'purchase' THEN 7
            END
    """

    costperresult = pd.read_sql_query(query, con=engine)

    return costperresult


def getSummaryPerMonth(startdate=None, enddate=None, platform=None):
    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f'''
        SELECT SUM(c.spending) as 'spending', SUM(c.reach) as 'reach', SUM(c.impression) as 'impression', SUM(c.engagement) as 'engagement', MONTH(c.date) as 'month', YEAR(c.date) as 'year'
        FROM dbo.Campaign as c
        WHERE pid IN {platform} AND c.date BETWEEN '{startdate}' AND '{enddate}'
        GROUP BY YEAR(c.date), MONTH(c.date)
        ORDER BY YEAR(c.date), MONTH(c.date)
    '''
    summaryPerMonth = pd.read_sql_query(query, con=engine)

    return summaryPerMonth


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
        return df.shape
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
