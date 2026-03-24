import pandas as pd

def validate_data(df):
    errors = []

    for index, row in df.iterrows():
        row_errors = {}

        # Example validations
        if "Name" in df.columns and row["Name"] == "N/A":
            row_errors["Name"] = "Missing Name"

        if "Phone" in df.columns:
            phone = str(row["Phone"])
            if not phone.isdigit() or len(phone) != 10:
                row_errors["Phone"] = "Invalid Phone"

        if row_errors:
            row_errors["Row"] = index
            errors.append(row_errors)

    return pd.DataFrame(errors)