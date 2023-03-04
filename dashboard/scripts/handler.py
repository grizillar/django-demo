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

# connection_string = (
#     r"Driver=ODBC Driver 17 for SQL Server;"
#     r"Server=;"
#     r"Database=AIDAChula;"
#     r"UID=;"
#     r"PWD=;"
#     r"Thrusted_Connection=yes;"
# )

# connection_url = sa.engine.URL.create(
#     "mssql.pyodbc",
#     query={"odbc_connect": connection_string}
# )

# engine = sa.create_engine(connection_url)

engine = sa.create_engine(
    f'mssql+pyodbc://{USER}:{PASSWORD}@{HOST}/{DATABASE}?driver={DRIVER}')

# Utils functions


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


def normalizePlatform(platform=None):
    if platform == None:
        platform = "('1','2','3','4','5','6','7')"
    elif platform == ['']:
        platform = "('0')"
    return platform


def getPeriodRange(period):
    if period == None or period == '':
        return "('1','2','3','4','5','6','7','8','9','10','11','12','13')"
    return f"('{period}')"


def formQueryArray(func, period_list, year_list, platform):
    arr = []
    for i in range(len(year_list)):
        arr.append(func(
            period_list[i], year_list[i], platform).to_json())
    return ("|".join(a for a in arr))


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

# General queries


def getAllCampaign():

    query = f"""
        SELECT *
        FROM dbo.Campaign
    """
    campaign = pd.read_sql_query(query, con=engine)

    campaign.replace(to_replace=[r'\\t|\\n|\\r|\\"', '\t|\n|\r|\"'], value=[
                     " ", " "], regex=True, inplace=True)

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


def getPossibleYear():
    query = f"""
        SELECT DISTINCT year
        FROM Campaign
        UNION
        SELECT DISTINCT year
        FROM SiteTraffic
    """
    years = pd.read_sql_query(query, con=engine)

    return years


def getSitetrafficLength():
    query = f"""
        SELECT COUNT(sid)
        FROM dbo.SiteTraffic
    """
    return int(pd.read_sql_query(query, con=engine).iloc[0])

# By date queries


def getPlatformCount(startdate=None, enddate=None, platform=None):

    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f"""
        SELECT c.pid as 'pid', COUNT(c.cid) as 'count'
        FROM Campaign as c
        WHERE c.date BETWEEN '{startdate}' AND '{enddate}' AND c.pid IN {platform}
        GROUP BY c.pid
    """

    platformCount = pd.read_sql_query(query, con=engine)
    return platformCount


def getCampaignCount(startdate=None, enddate=None, platform=None):

    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f"""
        SELECT count(c.cid)
        FROM Campaign as c
        WHERE c.date BETWEEN '{startdate}' AND '{enddate}' AND c.pid IN {platform}
    """

    return int(pd.read_sql_query(query, con=engine).iloc[0])


def getAllSummary(startdate=None, enddate=None, platform=None):

    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f"""
        SELECT p.pid, p.[platform_name], t1.spending, t1.reach, t1.impression, t1.engagement, t2.[user], t2.[new_user], t2.[order], t2.revenue
        FROM 
		(
			SELECT p.pid, p.platform_name
			FROM Platform as p
		) p
		LEFT JOIN
        (
            SELECT p.pid as 'pid', p.platform_name as 'platform_name', sum(c.spending) as 'spending', sum(c.reach) as 'reach', sum(c.impression) as 'impression', sum(c.engagement)  as 'engagement'
            FROM dbo.Campaign as c JOIN dbo.Platform as p ON c.pid = p.pid
            WHERE c.date BETWEEN '{startdate}' AND '{enddate}' AND p.pid IN {platform}
            GROUP BY p.pid, p.platform_name
        ) t1
        ON p.pid = t1.pid
        FULL OUTER JOIN
        (
            SELECT p.pid as 'pid', p.platform_name as 'platform_name', sum(s.all_user) as 'user', sum(s.new_user) as 'new_user', sum(s.order_count) as 'order', sum(s.revenue)  as 'revenue'
            FROM dbo.SiteTraffic as s JOIN dbo.Platform as p ON s.pid = p.pid
            WHERE p.pid IN {platform}
            GROUP BY p.pid, p.platform_name
        ) t2
        ON p.pid = t2.pid
    """
    summary = pd.read_sql_query(query, con=engine)

    return summary

    # Note: excluding NAN (large data too)


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
        WHERE c.pid IN {platform} AND c.objective != 'nan' AND c.objective != '0' AND c.objective != 'actions:onsite_conversion.messaging_conversation_started_7d' AND c.objective != 'actions:rsvp' AND c.objective != 'estimated_ad_recallers' AND c.date BETWEEN '{startdate}' AND '{enddate}'
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


def getTopCostPerCampaign(startdate=None, enddate=None, platform=None, top=5, order="reach"):
    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString([p for p in platform if "1" == p or "2" == p])

    if (order in ["reach", "impression", "engagement"]):
        order = "costper" + order
    else:
        order = "costperreach"

    query = f"""
        SELECT TOP({top}) c.cid, c.name,
	        ROUND(c.spending/c.reach, 3) as costperreach,
	        ROUND(c.spending/c.impression, 3) as costperimpression,
	        ROUND(c.spending/c.engagement, 3) as costperengagement
        FROM dbo.Campaign as c
        WHERE c.pid IN {platform} AND c.date BETWEEN '{startdate}' AND '{enddate}'
        ORDER BY {order} ASC
    """

    topCPO = pd.read_sql_query(query, con=engine)

    topCPO.replace(to_replace=[r'\\t|\\n|\\r|\\"', '\t|\n|\r|\"'], value=[
        " ", " "], regex=True, inplace=True)

    return topCPO


def getTopCampaign(startdate=None, enddate=None, platform=None):

    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f"""
        SELECT TOP(5) c.cid, c.name, c.pid,
	        c.reach,
			c.impression,
			c.engagement,
			(c.reach + c.impression + c.engagement) as total
        FROM dbo.Campaign as c
        WHERE c.pid IN {platform} AND c.date BETWEEN '{startdate}' AND '{enddate}'
        ORDER BY total DESC
        """

    topCampaign = pd.read_sql_query(query, con=engine)

    topCampaign.replace(to_replace=[r'\\t|\\n|\\r|\\"', '\t|\n|\r|\"'], value=[
        " ", " "], regex=True, inplace=True)

    return topCampaign


def getSimpleCampaign(startdate=None, enddate=None, platform=None):
    startdate, enddate, platform = normalizeQueryParams(
        startdate, enddate, platform)

    platform = listToSQLString(platform)

    query = f"""
        SELECT c.cid, c.name, c.spending, c.reach, c.impression, c.engagement
        FROM Campaign as c
        WHERE c.pid IN {platform} AND c.date BETWEEN '{startdate}' AND '{enddate}'
    """
    simpleCampaign = pd.read_sql_query(query, con=engine)

    simpleCampaign.replace(to_replace=[r'\\t|\\n|\\r|\\"', '\t|\n|\r|\"'], value=[
        " ", " "], regex=True, inplace=True)

    return simpleCampaign


# By period queries

def getAllSummaryByPeriod(period=None, year=None, platform=None):

    period = getPeriodRange(period)

    platform = listToSQLString(normalizePlatform(platform))

    query = f"""
        SELECT p.pid, p.[platform_name], t1.spending, t1.reach, t1.impression, t1.engagement, t2.[user], t2.[new_user], t2.[order], t2.revenue
        FROM 
        (
			SELECT p.pid, p.platform_name
			FROM Platform as p
		) p
		LEFT JOIN
        (
            SELECT p.pid as 'pid', p.platform_name as 'platform_name', sum(c.spending) as 'spending', sum(c.reach) as 'reach', sum(c.impression) as 'impression', sum(c.engagement)  as 'engagement'
            FROM dbo.Campaign as c JOIN dbo.Platform as p ON c.pid = p.pid
            WHERE c.period in {period} AND c.year = {year} AND p.pid IN {platform}
            GROUP BY p.pid, p.platform_name
        ) t1
        ON p.pid = t1.pid
        FULL OUTER JOIN
        (
            SELECT p.pid as 'pid', p.platform_name as 'platform_name', sum(s.all_user) as 'user', sum(s.new_user) as 'new_user', sum(s.order_count) as 'order', sum(s.revenue)  as 'revenue'
            FROM dbo.SiteTraffic as s JOIN dbo.Platform as p ON s.pid = p.pid
            WHERE s.period in {period} AND s.year = {year} AND p.pid IN {platform}
            GROUP BY p.pid, p.platform_name
        ) t2
        ON p.pid = t2.pid
    """
    summary = pd.read_sql_query(query, con=engine)

    return summary


def getPlatformCountByPeriod(period=None, year=None, platform=None):

    period = getPeriodRange(period)

    platform = listToSQLString(normalizePlatform(platform))

    query = f"""
        SELECT c.pid as 'pid', COUNT(c.cid) as 'count'
        FROM Campaign as c
        WHERE c.period in {period} AND c.year = {year} AND c.pid IN {platform}
        GROUP BY c.pid
    """

    platformCount = pd.read_sql_query(query, con=engine)
    return platformCount


def getCampaignCountByPeriod(period=None, year=None, platform=None):

    period = getPeriodRange(period)

    platform = listToSQLString(normalizePlatform(platform))

    query = f"""
        SELECT COUNT(c.cid)
        FROM Campaign as c
        WHERE c.period in {period} AND c.year = {year} AND c.pid IN {platform}
    """

    return int(pd.read_sql_query(query, con=engine).iloc[0])


def getSitetrafficLengthByPeriod(period=None, year=None, platform=None):

    period = getPeriodRange(period)

    platform = listToSQLString(normalizePlatform(platform))

    query = f"""
        SELECT COUNT(s.sid)
        FROM dbo.SiteTraffic as s
        WHERE s.period in {period} AND s.year = {year} AND s.pid IN {platform}
    """
    return int(pd.read_sql_query(query, con=engine).iloc[0])


def getCostPerResultByPeriod(period=None, year=None, platform=None):

    period = getPeriodRange(period)

    platform = normalizePlatform(platform)
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
        WHERE c.pid IN {platform} AND c.objective != 'nan' AND c.objective != '0' AND c.objective != 'actions:onsite_conversion.messaging_conversation_started_7d' AND c.objective != 'actions:rsvp' AND c.objective != 'estimated_ad_recallers' AND c.period in {period} AND c.year = {year}
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


def getSummaryByPeriod(period=None, year=None, platform=None):
    period = getPeriodRange(period)

    platform = listToSQLString(normalizePlatform(platform))

    query = f'''
        SELECT p.period, t1.spending, t1.reach, t1.impression, t1.engagement, t2.[user], t2.new_user, t2.[order], t2.revenue
        FROM
        (
            SELECT DISTINCT period
            FROM Campaign
            WHERE year = {year}
            UNION
            SELECT DISTINCT period
            FROM SiteTraffic
            WHERE year = {year}
        ) p
        LEFT JOIN
        (
            SELECT c.period, SUM(c.spending) as 'spending', SUM(c.reach) as 'reach', SUM(c.impression) as 'impression', SUM(c.engagement) as 'engagement'
            FROM dbo.Campaign as c, dbo.SiteTraffic as s
            WHERE c.year = {year} AND c.pid IN {platform}
            GROUP BY c.period
        ) t1
        ON p.period = t1.period
        FULL OUTER JOIN
        (
            SELECT s.period, SUM(s.all_user) as 'user', SUM(s.new_user) as 'new_user', SUM(s.order_count) as 'order', SUM(s.revenue) as 'revenue'
            FROM dbo.SiteTraffic as s
            WHERE s.year = {year} AND s.pid IN {platform}
            GROUP BY s.period
        ) t2
        ON p.period = t2.period
    '''
    summaryPerPeriod = pd.read_sql_query(query, con=engine)
    summaryPerPeriod.fillna(0, inplace=True)

    return summaryPerPeriod
