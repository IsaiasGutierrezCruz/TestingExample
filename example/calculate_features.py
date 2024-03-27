from datetime import datetime, timedelta

def vector_add(v, w):
    """Adds two vectors componentwise"""
    return [v_i + w_i for v_i, w_i in zip(v,w)]


def calculate_weekly_sales_last_n_days(data, n_days, last_day): 
    df = data.copy()
    limit_date = last_day - timedelta(days=n_days)
    df = df[
        df['Date'] >= limit_date
    ]
    return df.groupby('Store')['Weekly_Sales'].sum()