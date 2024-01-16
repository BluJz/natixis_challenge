import mlflow
from rfq_data_loader import load_data
from preprocesser import preprocesser
from client import client_avg, client_detail, client_weighted_hist_pref
from unique_ISIN import unique_ISIN
from sim_matrix import (
    sim_calculator,
    find_top_n_similar_bonds,
    is_newbond,
    isin_to_features,
    client_apetite,
    client_apetite_dict,
    bond_to_n_client,
)
from new_bond import new_bond_df, new_bond_to_vec


def global_run(file_path="RFQ_Data_Challenge_HEC.csv"):
    # Extract the raw data
    df = load_data(file_path)
    # Make a series of operations to the data to have a cleaned dataframe to work with
    df = preprocesser(df)

    # Get a dataframe with unique ISIN codes, with their returns and risks
    df_unique = unique_ISIN(df=df)

    # Create similarity matrix and preprocessors for future use
    similarity_matrix, scaler, one_hot_encoder, features = sim_calculator(
        df_unique=df_unique
    )
    # Create a dict to map ISIN codes to its features
    isin_to_features_dict = isin_to_features(df_unique=df_unique, features=features)

    # Create for each client the average bonds (specifying if we take only the 100 more recent transactions or all the transactions)
    client_apetite_dict_hist = client_apetite_dict(
        recent100=False, df=df, isin_to_features=isin_to_features_dict
    )
    client_apetite_dict_recent = client_apetite_dict(
        recent100=True, df=df, isin_to_features=isin_to_features_dict
    )


def recommenderISIN(isin_features: dict):
    new_bond_features = isin_to_features_dict[isin_code].reshape(1, -1)
    return recommendations, feedback_infos
