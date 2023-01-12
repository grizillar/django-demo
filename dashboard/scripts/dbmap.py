import pandas as pd
import numpy as np

# TEMPPATH = "../tmp/temp.csv"  # NOT FOR PROD
TEMPPATH = "./dashboard/tmp/temp.csv"

campaign_template_columns = ['date', 'cid', 'name', 'pid', 'spending', 'reach', 'impression', 'engagement',
                             'objective', 'video_view', 'landing_page_view', 'product_view', 'add_to_cart', 'purchase', 'dateadded']


def appendCampaign(campaign, df):
    df['cid'] = df['cid'] + campaign.shape[0]
    return pd.concat([campaign, df], axis=0, ignore_index=True)


def appendSiteTraffic(site_traffic, df):
    df['sid'] = df['sid'] + site_traffic.shape[0]
    return pd.concat([site_traffic, df], axis=0, ignore_index=True)


def objective(obj_str):
    obj_str = str(obj_str)
    if "click" in obj_str:
        return "link_click"
    elif "reach" in obj_str:
        return "reach"
    elif "engagement" in obj_str:
        return "engagement"
    elif "video" in obj_str:
        return "video_thruplay"
    elif "content" in obj_str or "Product" in obj_str:
        return "view_product"
    elif "cart" in obj_str:
        return "add_to_cart"
    elif "purchase" in obj_str:
        return "purchase"
    else:
        return obj_str


def FBTransform():

    df = pd.read_csv(TEMPPATH)

    df = df[df['การเข้าถึง'] != 0]

    ig = df[df["ชื่อแคมเปญ"].str.contains("IG")]
    fb = df[~df["ชื่อแคมเปญ"].str.contains("IG")]

    fb.reset_index(drop=True, inplace=True)
    ig.reset_index(drop=True, inplace=True)

    fb_campaign = pd.DataFrame(columns=campaign_template_columns)
    fb_campaign['date'] = fb['เริ่ม']
    fb_campaign['cid'] = np.arange(fb.shape[0])
    fb_campaign['name'] = fb['ชื่อแคมเปญ']
    fb_campaign['pid'] = 1
    fb_campaign['spending'] = fb['จำนวนเงินที่ใช้จ่ายไป (THB)']
    fb_campaign['reach'] = fb['การเข้าถึง']
    fb_campaign['impression'] = fb['อิมเพรสชัน']
    fb_campaign['engagement'] = fb['การมีส่วนร่วมกับโพสต์']
    fb_campaign['objective'] = fb['ตัวระบุผลลัพธ์'].map(objective)
    fb_campaign['video_view'] = fb['ThruPlay']
    fb_campaign['landing_page_view'] = fb['การเข้าชมแลนดิ้งเพจ']
    fb_campaign['product_view'] = fb['การรับชมเนื้อหา']
    fb_campaign['add_to_cart'] = fb['การหยิบใส่รถเข็น']
    fb_campaign['purchase'] = fb['การซื้อ']
    fb_campaign['dateadded'] = pd.Timestamp.now().to_pydatetime()

    ig_campaign = pd.DataFrame(columns=campaign_template_columns)
    ig_campaign['date'] = ig['เริ่ม']
    ig_campaign['cid'] = np.arange(ig.shape[0])
    ig_campaign['name'] = ig['ชื่อแคมเปญ']
    ig_campaign['pid'] = 2
    ig_campaign['spending'] = ig['จำนวนเงินที่ใช้จ่ายไป (THB)']
    ig_campaign['reach'] = ig['การเข้าถึง']
    ig_campaign['impression'] = ig['อิมเพรสชัน']
    ig_campaign['engagement'] = ig['การมีส่วนร่วมกับโพสต์']
    ig_campaign['objective'] = ig['ตัวระบุผลลัพธ์'].map(objective)
    ig_campaign['video_view'] = ig['ThruPlay']
    ig_campaign['landing_page_view'] = ig['การเข้าชมแลนดิ้งเพจ']
    ig_campaign['product_view'] = ig['การรับชมเนื้อหา']
    ig_campaign['add_to_cart'] = ig['การหยิบใส่รถเข็น']
    ig_campaign['purchase'] = ig['การซื้อ']
    ig_campaign['dateadded'] = pd.Timestamp.now().to_pydatetime()

    df = appendCampaign(fb_campaign, ig_campaign)
    df = df.fillna(value=0)

    return df


def LPTransform():
    lp = pd.read_csv(TEMPPATH)

    lp_campaign = pd.DataFrame(columns=campaign_template_columns)

    lp_campaign['date'] = lp['Date'].apply(str)
    lp_campaign['cid'] = np.arange(lp.shape[0])
    lp_campaign['name'] = lp['Post URL']
    lp_campaign['pid'] = 3
    lp_campaign['spending'] = 0
    lp_campaign['reach'] = lp['Reached Accounts']
    lp_campaign['impression'] = lp['Impressions']
    lp_campaign['engagement'] = lp['Clicks']
    lp_campaign['dateadded'] = pd.Timestamp.now().to_pydatetime()

    lp_campaign = lp_campaign.fillna(value=0)

    return lp_campaign


def LMTransform():
    lm = pd.read_csv(TEMPPATH)

    lm_campaign = pd.DataFrame(columns=campaign_template_columns)

    lm_campaign['date'] = lm['sentDate'].map(lambda x: x.split()[0])
    lm_campaign['cid'] = np.arange(lm.shape[0])

    lm_campaign['name'] = lm['cmsUrl']
    lm_campaign['pid'] = 3
    lm_campaign['spending'] = lm['deliveredCount'].map(lambda x: x * 0.04)
    lm_campaign['reach'] = lm['deliveredCount']
    lm_campaign['impression'] = lm['deliveredCount']
    lm_campaign['engagement'] = lm['open']
    lm_campaign['dateadded'] = pd.Timestamp.now().to_pydatetime()

    lm_campaign = lm_campaign.fillna(value=0)

    return lm_campaign


def GCTransform():
    ga = pd.read_csv(TEMPPATH)

    ga = ga.dropna()
    ga = ga.replace(',', '', regex=True)

    ga["การแสดงผล"] = ga["การแสดงผล"].astype('int64')
    ga["การโต้ตอบ"] = ga["การโต้ตอบ"].astype('int64')

    ga_campaign = pd.DataFrame(columns=campaign_template_columns)

    ga_campaign['date'] = pd.NA
    ga_campaign['cid'] = np.arange(ga.shape[0])

    ga_campaign['name'] = ga['แคมเปญ']
    ga_campaign['pid'] = 4
    ga_campaign['spending'] = ga['ค่าใช้จ่าย']
    ga_campaign['impression'] = ga['การแสดงผล']
    ga_campaign['engagement'] = ga['การโต้ตอบ']
    ga_campaign['dateadded'] = pd.Timestamp.now().to_pydatetime()

    ga_campaign = ga_campaign.fillna(value=0)
    ga_campaign["date"] = ga_campaign["date"].replace(0, None)

    return ga_campaign


def GSTransform():
    dfga = pd.read_csv(TEMPPATH)

    dfga = dfga.dropna()

    dfga = dfga.replace(',', '', regex=True)

    dfga["รายได้"] = dfga["รายได้"].replace('US\$', '', regex=True)
    dfga["ผู้ใช้"] = dfga["ผู้ใช้"].astype('int64')
    dfga["ผู้ใช้ใหม่"] = dfga["ผู้ใช้ใหม่"].astype('int64')
    dfga["ธุรกรรม"] = dfga["ธุรกรรม"].astype('int64')
    dfga["รายได้"] = dfga["รายได้"].astype('float64')

    fbKeywords = ["facebook"]
    igKeywords = ["instagram", "IG", "linktr.ee"]
    lineKeywords = ["line", "broadcast", "chatbot"]
    lineExclusion = ["line / lap", "offline"]
    googleKeywords = ["google"]
    googleExclusion = ["google / organic"]

    dfga_fb = dfga[dfga["แหล่งที่มา/สื่อ"].str.contains("|".join(fbKeywords))]

    dfga_ig = dfga[dfga["แหล่งที่มา/สื่อ"].str.contains("|".join(igKeywords))]

    dfga_line = dfga[dfga["แหล่งที่มา/สื่อ"]
                     .str.contains("|".join(lineKeywords))]
    # Exclusion
    dfga_line = dfga_line[~dfga_line["แหล่งที่มา/สื่อ"]
                          .str.contains("|".join(lineExclusion))]
    dfga_google = dfga[dfga["แหล่งที่มา/สื่อ"]
                       .str.contains("|".join(googleKeywords))]
    dfga_google = dfga_google[~dfga_google["แหล่งที่มา/สื่อ"].str.contains(
        "|".join(googleExclusion))]  # Exclusion
    dfga_gorganic = dfga[dfga["แหล่งที่มา/สื่อ"]
                         .str.contains("|".join(["google / organic"]))]
    dfga_direct = dfga[dfga["แหล่งที่มา/สื่อ"]
                       .str.contains("(direct) / (none)", regex=False)]

    dfga_other = pd.concat([dfga, dfga_fb]).drop_duplicates(keep=False)
    dfga_other = pd.concat([dfga_other, dfga_ig]).drop_duplicates(keep=False)
    dfga_other = pd.concat([dfga_other, dfga_line]).drop_duplicates(keep=False)
    dfga_other = pd.concat([dfga_other, dfga_google]
                           ).drop_duplicates(keep=False)
    dfga_other = pd.concat([dfga_other, dfga_gorganic]
                           ).drop_duplicates(keep=False)
    dfga_other = pd.concat([dfga_other, dfga_direct]
                           ).drop_duplicates(keep=False)

    dfga_fb.reset_index(drop=True, inplace=True)
    dfga_ig.reset_index(drop=True, inplace=True)
    dfga_line.reset_index(drop=True, inplace=True)
    dfga_google.reset_index(drop=True, inplace=True)
    dfga_gorganic.reset_index(drop=True, inplace=True)
    dfga_direct.reset_index(drop=True, inplace=True)
    dfga_other.reset_index(drop=True, inplace=True)

    site_traffic_template_columns = [
        'sid', 'pid', 'uri', 'all_user', 'new_user', 'order_count', 'revenue', 'dateadded']
    site_traffic = pd.DataFrame(columns=site_traffic_template_columns)

    fb_st = pd.DataFrame(columns=site_traffic_template_columns)

    fb_st['sid'] = np.arange(dfga_fb.shape[0])
    fb_st['pid'] = 1
    fb_st['uri'] = dfga_fb['แหล่งที่มา/สื่อ']
    fb_st['all_user'] = dfga_fb['ผู้ใช้']
    fb_st['new_user'] = dfga_fb['ผู้ใช้ใหม่']
    fb_st['order_count'] = dfga_fb['ธุรกรรม']
    fb_st['revenue'] = dfga_fb['รายได้']
    fb_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    ig_st = pd.DataFrame(columns=site_traffic_template_columns)

    ig_st['sid'] = np.arange(dfga_ig.shape[0])
    ig_st['pid'] = 2
    ig_st['uri'] = dfga_ig['แหล่งที่มา/สื่อ']
    ig_st['all_user'] = dfga_ig['ผู้ใช้']
    ig_st['new_user'] = dfga_ig['ผู้ใช้ใหม่']
    ig_st['order_count'] = dfga_ig['ธุรกรรม']
    ig_st['revenue'] = dfga_ig['รายได้']
    ig_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    ln_st = pd.DataFrame(columns=site_traffic_template_columns)

    ln_st['sid'] = np.arange(dfga_line.shape[0])
    ln_st['pid'] = 3
    ln_st['uri'] = dfga_line['แหล่งที่มา/สื่อ']
    ln_st['all_user'] = dfga_line['ผู้ใช้']
    ln_st['new_user'] = dfga_line['ผู้ใช้ใหม่']
    ln_st['order_count'] = dfga_line['ธุรกรรม']
    ln_st['revenue'] = dfga_line['รายได้']
    ln_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    g_st = pd.DataFrame(columns=site_traffic_template_columns)

    g_st['sid'] = np.arange(dfga_google.shape[0])
    g_st['pid'] = 4
    g_st['uri'] = dfga_google['แหล่งที่มา/สื่อ']
    g_st['all_user'] = dfga_google['ผู้ใช้']
    g_st['new_user'] = dfga_google['ผู้ใช้ใหม่']
    g_st['order_count'] = dfga_google['ธุรกรรม']
    g_st['revenue'] = dfga_google['รายได้']
    g_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    go_st = pd.DataFrame(columns=site_traffic_template_columns)

    go_st['sid'] = np.arange(dfga_gorganic.shape[0])
    go_st['pid'] = 5
    go_st['uri'] = dfga_gorganic['แหล่งที่มา/สื่อ']
    go_st['all_user'] = dfga_gorganic['ผู้ใช้']
    go_st['new_user'] = dfga_gorganic['ผู้ใช้ใหม่']
    go_st['order_count'] = dfga_gorganic['ธุรกรรม']
    go_st['revenue'] = dfga_gorganic['รายได้']
    go_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    d_st = pd.DataFrame(columns=site_traffic_template_columns)

    d_st['sid'] = np.arange(dfga_direct.shape[0])
    d_st['pid'] = 6
    d_st['uri'] = dfga_direct['แหล่งที่มา/สื่อ']
    d_st['all_user'] = dfga_direct['ผู้ใช้']
    d_st['new_user'] = dfga_direct['ผู้ใช้ใหม่']
    d_st['order_count'] = dfga_direct['ธุรกรรม']
    d_st['revenue'] = dfga_direct['รายได้']
    d_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    o_st = pd.DataFrame(columns=site_traffic_template_columns)

    o_st['sid'] = np.arange(dfga_other.shape[0])
    o_st['pid'] = 7
    o_st['uri'] = dfga_other['แหล่งที่มา/สื่อ']
    o_st['all_user'] = dfga_other['ผู้ใช้']
    o_st['new_user'] = dfga_other['ผู้ใช้ใหม่']
    o_st['order_count'] = dfga_other['ธุรกรรม']
    o_st['revenue'] = dfga_other['รายได้']
    o_st['dateadded'] = pd.Timestamp.now().to_pydatetime()

    site_traffic = appendSiteTraffic(site_traffic, fb_st)
    site_traffic = appendSiteTraffic(site_traffic, ig_st)
    site_traffic = appendSiteTraffic(site_traffic, ln_st)
    site_traffic = appendSiteTraffic(site_traffic, g_st)
    site_traffic = appendSiteTraffic(site_traffic, go_st)
    site_traffic = appendSiteTraffic(site_traffic, d_st)
    site_traffic = appendSiteTraffic(site_traffic, o_st)

    return site_traffic
