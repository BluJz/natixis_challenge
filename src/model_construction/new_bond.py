import numpy as np 
import pandas as pd 
import datetime as dt 

cols_re = ['Coupon']
cols_ri = ['BloomIndustrySubGroup','Classification','Country','Ccy','Rating_SP','Maturity','dl_maturity_years','Type']
categorical_features = ['BloomIndustrySubGroup', 'Classification', 'Country', 'Ccy', 'Type']
numerical_features = ['Coupon', 'dl_maturity_years', 'Rating_SP_Ordinal']

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

today = np.datetime64(dt.date.today())

def new_bond_df(new_bond,cols_re=cols_re,cols_ri=cols_ri,rating_mapping=rating_mapping, today=today):
    df = pd.DataFrame([new_bond])
    df['Maturity'] = pd.to_datetime(df['Maturity'])
    df['dl_maturity_days'] = (df['Maturity'] - today).dt.days
    df['dl_maturity_years'] = round(df['dl_maturity_days']/365,2)
    bins = [0, 4, 10, float('inf')]  
    labels = ['short', 'mid', 'long']
    df['dl_m_category'] = pd.cut(df['dl_maturity_years'], bins=bins, labels=labels, right=False)
    df = df[['ISIN']+cols_re+cols_ri]
    df['Rating_SP_Ordinal'] = df['Rating_SP'].map(rating_mapping)
    return df

def new_bond_to_vec(new_bond_df, scaler, one_hot_encoder, numerical_features=numerical_features, categorical_features=categorical_features):
    new_bond_scaled_numerical = scaler.transform(new_bond_df[numerical_features])
    new_bond_encoded_categorical = one_hot_encoder.transform(new_bond_df[categorical_features])
    new_bond_features = np.hstack((new_bond_scaled_numerical, new_bond_encoded_categorical.toarray()))
    return new_bond_features