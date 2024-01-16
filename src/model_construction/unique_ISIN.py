import pandas as pd

# Lets Summarize the Return and Risk featurs to define a bond 
cols_re = ['Coupon']
cols_ri = ['BloomIndustrySubGroup','Classification','Country','Ccy','Rating_SP','Maturity','dl_maturity_years','Type']

rating_mapping = {
    'AAA': 21, 'Aaa': 21,
    'AA+': 20, 'Aa1': 20,
    'AA': 19, 'Aa2': 19,
    'AA-': 18, 'Aa3': 18,
    'A+': 17, 'A1': 17,
    'A': 16, 'A2': 16,
    'A-': 15, 'A3': 15,
    'BBB+': 14, 'Baa1': 14, '(P)Baa1': 14,
    'BBB': 13, 'Baa2': 13,
    'BBB-': 12, 'Baa3': 12,
    'BB+': 11, 'Ba1': 11,
    'BB': 10, 'Ba2': 10,
    'BB-': 9, 'Ba3': 9,
    'B+': 8, 'B1': 8,
    'B': 7, 'B2': 7,
    'B-': 6, 'B3': 6,
    'CCC+': 5, 'Caa1': 5,
    'WR': 0, 'NR': 0  # WR (Withdrawn Rating) and NR (Not Rated) can be treated as 0 or another scheme
}

def unique_ISIN(df):
	df_unique = df.drop_duplicates(subset='ISIN', keep='first')
	df_unique = df_unique[['ISIN']+cols_re+cols_ri]
	df_unique['Rating_SP_Ordinal'] = df_unique['Rating_SP'].map(rating_mapping)
	return df_unique
	