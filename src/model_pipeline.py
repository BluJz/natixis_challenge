import mlflow
import streamlit as st
from model_construction.rfq_data_loader import load_data
from model_construction.preprocesser import preprocesser
from model_construction.client import (
    client_avg,
    client_detail,
    client_weighted_hist_pref,
)
from model_construction.unique_ISIN import unique_ISIN
from model_construction.sim_matrix import (
    sim_calculator,
    find_top_n_similar_bonds,
    is_newbond,
    isin_to_features_func,
    client_apetite,
    client_apetite_dict,
    bond_to_n_client,
)
from model_construction.new_bond import new_bond_to_df, new_bond_to_vec


@st.cache_data
def global_run(file_path="RFQ_Data_Challenge_HEC.csv"):
    model_hash = "H4SH4M0D3L"

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
    isin_to_features_dict = isin_to_features_func(
        df_unique=df_unique, features=features
    )

    # Create for each client the average bonds (specifying if we take only the 100 more recent transactions or all the transactions)
    client_apetite_dict_hist = client_apetite_dict(
        recent100=False, df=df, isin_to_features=isin_to_features_dict
    )
    client_apetite_dict_recent = client_apetite_dict(
        recent100=True, df=df, isin_to_features=isin_to_features_dict
    )

    return (
        isin_to_features_dict,
        client_apetite_dict_hist,
        client_apetite_dict_recent,
        features,
        df_unique,
        similarity_matrix,
        scaler,
        one_hot_encoder,
        df,
        model_hash,
    )


def recommender_isin_code(
    isin_code,
    isin_to_features_dict=None,
    client_apetite_dict_hist=None,
    client_apetite_dict_recent=None,
    features=None,
    df_unique=None,
    n=3,
    offset=0,  # New offset parameter
):
    new_bond_features = isin_to_features_dict[isin_code].reshape(1, -1)
    client_hist_new_bond = bond_to_n_client(
        bond_vect=new_bond_features, client_apetite_dict=client_apetite_dict_hist, n=n
    )
    client_recent_new_bond = bond_to_n_client(
        bond_vect=new_bond_features,
        client_apetite_dict=client_apetite_dict_recent,
        n=n,
    )
    bonds_new_bond = find_top_n_similar_bonds(
        new_bond_features=new_bond_features,
        existing_features=features,
        df_unique=df_unique,
        n=n,
    )

    all_client_recs = bond_to_n_client(
        bond_vect=new_bond_features, 
        client_apetite_dict=client_apetite_dict_hist, 
        n=n+offset,  # Fetch extra recommendations
    )

    all_recommendations = find_top_n_similar_bonds(
        new_bond_features=new_bond_features,
        existing_features=features,
        df_unique=df_unique,
        n=n+offset,  # Fetch extra recommendations
    )

    # Apply the offset and limit
    bonds_new_bond = all_recommendations[offset:offset+n]
    client_recs = all_client_recs[offset:offset+n]

    return client_hist_new_bond, client_recent_new_bond, bonds_new_bond


def recommender_isin_features(
    isin_features,
    scaler=None,
    one_hot_encoder=None,
    client_apetite_dict_hist=None,
    client_apetite_dict_recent=None,
    features=None,
    df_unique=None,
    n=3,
    offset=0,  # New offset parameter
):
    new_bond_df = new_bond_to_df(isin_features)
    new_bond_vec = new_bond_to_vec(
        new_bond_df=new_bond_df, scaler=scaler, one_hot_encoder=one_hot_encoder
    )

    client_hist_new_bond = bond_to_n_client(
        bond_vect=new_bond_vec, client_apetite_dict=client_apetite_dict_hist, n=n
    )
    client_recent_new_bond = bond_to_n_client(
        bond_vect=new_bond_vec,
        client_apetite_dict=client_apetite_dict_recent,
        n=n,
    )
    bonds_new_bond = find_top_n_similar_bonds(
        new_bond_features=new_bond_vec,
        existing_features=features,
        df_unique=df_unique,
        n=n,
    )

    all_client_recs = bond_to_n_client(
        bond_vect=new_bond_vec, 
        client_apetite_dict=client_apetite_dict_hist, 
        n=n+offset,  # Fetch extra recommendations
    )

    all_recommendations = find_top_n_similar_bonds(
        new_bond_features=new_bond_vec,
        existing_features=features,
        df_unique=df_unique,
        n=n+offset,  # Fetch extra recommendations
    )

    # Apply the offset and limit
    bonds_new_bond = all_recommendations[offset:offset+n]
    client_recs = all_client_recs[offset:offset+n]

    return client_hist_new_bond, client_recent_new_bond, bonds_new_bond


def recommender_client(
    client_name, df=None, isin_to_features_dict=None, features=None, df_unique=None, n=3, offset=0
):
    client_hist_apetite = client_apetite(
        client=client_name,
        recent100=False,
        df=df,
        isin_to_features=isin_to_features_dict,
    )
    # Fetch more recommendations than needed
    all_recommendations = find_top_n_similar_bonds(
        new_bond_features=client_hist_apetite,
        existing_features=features,
        df_unique=df_unique,
        n=n+offset,
    )

    # Slice the recommendations to get the correct set
    top_n_bonds = all_recommendations[offset:offset+n]

    return client_hist_apetite, top_n_bonds
