from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


cols_re = ['Coupon']
cols_ri = ['BloomIndustrySubGroup','Classification','Country','Ccy','Rating_SP','Maturity','dl_maturity_years','Type']
categorical_features = ['BloomIndustrySubGroup', 'Classification', 'Country', 'Ccy', 'Type']
numerical_features = ['Coupon', 'dl_maturity_years', 'Rating_SP_Ordinal']

def sim_calculator(df_unique):
	# Convert categorical variables to numeric using one-hot encoding
	one_hot_encoder = OneHotEncoder()
	encoded_categorical = one_hot_encoder.fit_transform(df_unique[categorical_features])

	# Normalize numerical features
	scaler = StandardScaler()
	scaled_numerical = scaler.fit_transform(df_unique[numerical_features])

	# Combine all features
	features = np.hstack((scaled_numerical, encoded_categorical.toarray()))

	# Compute Similarity Matrix
	similarity_matrix = cosine_similarity(features)

	return similarity_matrix, scaler, one_hot_encoder, features

def is_newbond(isin,df_unique):
	if isin in df_unique['ISIN'].values:
		return True
	else:
		return False

def find_top_n_similar_bonds(new_bond_features, existing_features, df_unique, n=10):
    # Compute similarity with existing bonds
    similarity_scores = cosine_similarity(new_bond_features, existing_features)

    # Get the indices of the top N similar bonds
    top_indices = np.argsort(similarity_scores[0])[::-1][:n]

    # Select the top N similar bonds from the DataFrame
    top_similar_bonds = df_unique.iloc[top_indices]

    return top_similar_bonds

def isin_to_features(df_unique,features):
    result = {isin: features for isin, features in zip(df_unique['ISIN'], features)}
    return result

def client_apetite(client,df,isin_to_features, recent100=False):
    client_mask = df.company_short_name == client
    client_df = df[client_mask]
    if recent100:
        client_df = client_df.tail(100)
    weighted_sum = client_df.groupby('ISIN')['Total_requested_Price*Amount'].sum()
    overall_total = weighted_sum.sum()
    percentage = (weighted_sum / overall_total) * 100
    average_array_shape = next(iter(isin_to_features.values())).shape
    weighted_average_array = np.zeros(average_array_shape)
    for isin, weight in percentage.iteritems():
        if isin in isin_to_features:
            # Multiply the array by its weight and add it to the running total
            weighted_average_array += isin_to_features[isin] * weight
    vect = weighted_average_array.reshape(1,-1)
    return vect

def client_apetite_dict(df, isin_to_features, recent100=False):
    # Assuming client_apetite returns a vector for each client
    diction = {client: client_apetite(client=client,df=df,isin_to_features=isin_to_features, recent100=recent100) for client in df.company_short_name.unique()}
    return diction

def bond_to_n_client(bond_vect,client_apetite_dict,n=10):
    similarities = {}
    
    # Calculate cosine similarity between bond_vect and each client's vector
    for client, client_vect in client_apetite_dict.items():
        similarity_score = cosine_similarity(bond_vect, client_vect)[0, 0]
        similarities[client] = similarity_score

    # Get the top n clients with highest similarity scores
    top_clients = sorted(similarities, key=similarities.get, reverse=True)[:n]

    return top_clients

