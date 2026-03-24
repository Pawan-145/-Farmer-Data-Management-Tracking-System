import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Farmer Data System", layout="wide")

DATA_FILE = "farmers_data.csv"

# -----------------------------
# Load Data
# -----------------------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Farmer_ID", "Name", "Phone", "State", "Crop", "Land"])

# -----------------------------
# ID Generator
# -----------------------------
def generate_id(df):
    return f"FRM-2026-{str(len(df)+1).zfill(4)}"

# -----------------------------
# Sidebar Navigation
# -----------------------------
menu = st.sidebar.selectbox("Menu", ["Add Farmer", "View / Manage", "Dashboard"])

# =============================
# ➕ ADD FARMER
# =============================
if menu == "Add Farmer":
    st.title("➕ Add Farmer")

    with st.form("farmer_form"):
        col1, col2 = st.columns(2)

        name = col1.text_input("Name")
        phone = col2.text_input("Phone")

        state = col1.text_input("State")
        crop = col2.selectbox("Crop", ["Wheat", "Rice", "Corn", "Other"])

        land = col1.number_input("Land (acres)", min_value=0.0)

        submit = st.form_submit_button("Add Farmer")

    if submit:
        errors = []

        if not name:
            errors.append("Name required")

        if not phone.isdigit() or len(phone) != 10:
            errors.append("Invalid phone")

        if land <= 0:
            errors.append("Land must be > 0")

        if phone in df["Phone"].astype(str).values:
            errors.append("Duplicate phone")

        if errors:
            for e in errors:
                st.error(e)
        else:
            farmer_id = generate_id(df)

            new_data = {
                "Farmer_ID": farmer_id,
                "Name": name,
                "Phone": phone,
                "State": state,
                "Crop": crop,
                "Land": land
            }

            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.toast("✅ Farmer added successfully!", icon="🎉")


# =============================
# 📋 VIEW / MANAGE
# =============================
elif menu == "View / Manage":
    st.title("📋 Manage Farmers")

    # 🔍 Search
    search = st.text_input("Search by Name or Phone")

    # 🎯 Filter
    crop_filter = st.selectbox("Filter by Crop", ["All"] + list(df["Crop"].unique()))

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search, case=False) |
            filtered_df["Phone"].astype(str).str.contains(search)
        ]

    if crop_filter != "All":
        filtered_df = filtered_df[filtered_df["Crop"] == crop_filter]

    st.dataframe(filtered_df)

    # ✏️ EDIT
    st.subheader("✏️ Edit Farmer")

    selected_id = st.selectbox("Select Farmer ID", df["Farmer_ID"])

    filtered = df[df["Farmer_ID"] == selected_id]

    if not filtered.empty:
     selected_row = filtered.iloc[0]
    else:
     st.warning("⚠️ No data found for selected farmer")
     st.stop()

    new_name = st.text_input("Name", selected_row["Name"])
    new_phone = st.text_input("Phone", selected_row["Phone"])
    new_state = st.text_input("State", selected_row["State"])
    new_crop = st.selectbox("Crop", ["Wheat", "Rice", "Corn", "Other"], index=0)
    new_land = st.number_input("Land", value=float(selected_row["Land"]))

    if st.button("Update"):
        df.loc[df["Farmer_ID"] == selected_id, ["Name", "Phone", "State", "Crop", "Land"]] = [
            new_name, new_phone, new_state, new_crop, new_land
        ]
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Updated!")

    # ❌ DELETE
    st.subheader("❌ Delete Farmer")

    delete_id = st.selectbox("Select ID to Delete", df["Farmer_ID"])

    if st.button("🗑️ Delete Farmer"):
        df = df[df["Farmer_ID"] != delete_id]
        df.to_csv(DATA_FILE, index=False)
        st.success("🗑️ Deleted!")

# =============================
# 📊 DASHBOARD
# =============================
elif menu == "Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Farmers", len(df))
    col2.metric("Unique Crops", df["Crop"].nunique())
    col3.metric("Avg Land", round(df["Land"].mean(), 2) if len(df) > 0 else 0)

    st.subheader("🌾 Crop Distribution")
    st.bar_chart(df["Crop"].value_counts())

    st.subheader("📍 State Distribution")
    st.bar_chart(df["State"].value_counts())

# =============================
# ⬇️ DOWNLOAD
# =============================
st.sidebar.download_button(
    "⬇️ Download Data",
    data=df.to_csv(index=False),
    file_name="farmers_data.csv",
    mime="text/csv"
)

st.sidebar.info("ℹ️ Data is stored temporarily. Download to save. Future upgrade: SQL / Google Sheets.")
st.sidebar.success("🚀 System Status: Running")