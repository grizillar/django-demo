import pandas as pd


def applyBaseCPR(df):

    objectives = ["link_click", "reach", "engagement",
                  "video_thruplay", "view_product", "add_to_cart", "purchase"]
    columns = ["objective", 'spending', 'cost/reach', 'cost/impression', 'cost/engagement',
               'cost/video_view', 'cost/landing_page_view', 'cost/product_view', 'cost/add_to_cart', 'cost/purchase']
    base = pd.DataFrame(columns=columns)
    base["objective"] = objectives
    base.fillna(0, inplace=True)

    for i in range(df.shape[0]):
        obj = df.loc[i, "objective"]
        base.loc[base.loc["objective"] == obj] = obj.loc[i]

    return base


# Example DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Replace rows where A is greater than 1
df.loc[df['A'] == 1] = pd.Series({'A': 100, 'B': 200})

# Display updated DataFrame
print(df)
