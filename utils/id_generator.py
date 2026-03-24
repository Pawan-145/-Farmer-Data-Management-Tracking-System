def generate_farmer_ids(df):
    ids = []

    for i in range(len(df)):
        ids.append(f"FRM-2026-{str(i+1).zfill(4)}")

    df["Farmer_ID"] = ids
    return df