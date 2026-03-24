def get_stats(df):
    stats = {}

    stats["total"] = len(df)

    if "Crop" in df.columns:
        stats["crops"] = df["Crop"].nunique()
    else:
        stats["crops"] = 0

    if "Land" in df.columns:
        stats["avg_land"] = round(df["Land"].replace("N/A", 0).astype(float).mean(), 2)
    else:
        stats["avg_land"] = 0

    return stats