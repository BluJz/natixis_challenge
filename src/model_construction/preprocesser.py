import pandas as pd
import numpy as np
import datetime as dt

today = np.datetime64(dt.date.today())


def preprocesser(df: pd.DataFrame, today=today) -> pd.DataFrame:
    df["Total_Requested_Volume"] = pd.to_numeric(
        df["Total_Requested_Volume"], errors="coerce"
    )  # Convert to float, invalid parsing will be set as NaN
    df = df[df["Total_Requested_Volume"] > 0]
    # if B_price is < 0, drop
    df["B_Price"] = pd.to_numeric(
        df["B_Price"], errors="coerce"
    )  # Convert to float, invalid parsing will be set as NaN
    df = df[df["B_Price"] > 0]
    df = df.drop(
        [
            "Sales_Name",
            "Sales_Initial",
            "Tier",
            "AssumedMaturity",
            "YTWDate",
            "Cusip",
            "SpreadvsBenchmarkMid",
            "GSpreadMid",
        ],
        axis=1,
    )
    col_clean = [
        "Instrument",
        "BloomIndustrySector",
        "cdcissuer",
        "Country",
        "MidASWSpread",
        "Rating_Moodys",
        "MidZSpread",
        "MidYTM",
        "Rating_Fitch",
        "Rating_SP",
        "Coupon",
        "Ccy",
        "Country",
        "Classification",
    ]
    df = df.dropna(subset=col_clean)
    df = df[pd.notna(df["Country"]) & df["Country"].apply(lambda x: isinstance(x, str))]
    df = df[
        pd.notna(df["BloomIndustrySubGroup"])
        & df["BloomIndustrySubGroup"].apply(lambda x: isinstance(x, str))
    ]
    df = df[
        pd.notna(df["cdcissuer"]) & df["cdcissuer"].apply(lambda x: isinstance(x, str))
    ]
    # Convert to datetime
    df["Deal_Date"] = pd.to_datetime(df["Deal_Date"])
    df["Maturity"] = pd.to_datetime(df["Maturity"])
    df = df[df["Maturity"] > today]
    # Calculate the difference in days
    df["dl_maturity_days"] = (df["Maturity"] - today).dt.days
    df["dl_maturity_months"] = df["dl_maturity_days"] // 30
    df["dl_maturity_years"] = round(df["dl_maturity_days"] / 365, 2)
    bins = [0, 4, 10, float("inf")]
    labels = ["short", "mid", "long"]
    df["dl_m_category"] = pd.cut(
        df["dl_maturity_years"], bins=bins, labels=labels, right=False
    )
    df["Total_requested_Price*Amount"] = df["MidPrice"] * df["Total_Requested_Volume"]

    return df
