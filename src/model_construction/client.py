import pandas as pd

cols_key = ['ISIN',
            'BloomIndustrySector', 'BloomIndustrySubGroup',
            'Country','Ccy','Type',
            'Rating_SP',
            'Coupon', 'Frequency',
            'dl_maturity_years','dl_m_category'
           ]

def client_avg(df):
	grouped = df.groupby('company_short_name').nunique()
	client_avg_diversity = {col: round(grouped[col].mean(),2) for col in cols_key}
	return client_avg_diversity # return dict

def client_detail(client_name, df):
    grouped = df.groupby('company_short_name').nunique()
    client_diversity = {col: round(grouped.loc[client_name][col].mean(),2) for col in cols_key}
    return client_diversity # return dict

def client_weighted_hist_pref(client_name,df,preference):
    client_mask = df.company_short_name == client_name
    client_df = df[client_mask]
    weighted_sums = client_df.groupby(preference)['Total_requested_Price*Amount'].sum()
    return weighted_sums # return pd series with preference value as index

