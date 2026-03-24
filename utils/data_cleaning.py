import pandas as pd
import numpy as np

def clean_data(df):
    # Remove duplicates
    df = df.drop_duplicates()

    # Replace -1 or invalid values with NaN
    df.replace(-1, np.nan, inplace=True)

    # Fill missing values
    df.fillna("N/A", inplace=True)

    return df