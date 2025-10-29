import pandas as pd

# --- Load crop and rainfall datasets safely ---
crop = pd.read_csv("clean_crop.csv", low_memory=False)
rain = pd.read_csv("rainfall.csv")

# --- Clean the data ---
# Drop any accidental header rows that got read as data
crop = crop[crop["Year"].str.isnumeric()]  # keep only rows where 'Year' is numeric

# --- Rename rainfall columns for consistency ---
rain = rain.rename(columns={
    "SUBDIVISION": "State",
    "YEAR": "Year",
    "ANNUAL": "Rainfall_mm"
})

# --- Select only required columns ---
rain = rain[["State", "Year", "Rainfall_mm"]]

# --- Standardize names and types ---
crop["State"] = crop["State"].str.strip().str.title()
rain["State"] = rain["State"].str.strip().str.title()

# Convert year to integer
crop["Year"] = crop["Year"].astype(int)
rain["Year"] = rain["Year"].astype(int)


# --- Fix common state name mismatches ---
state_corrections = {
    "Andaman & Nicobar Islands": "Andaman And Nicobar Islands",
    "Delhi": "Nct Of Delhi",
    "Odisha": "Orissa",
    "Pondicherry": "Puducherry",
    "Jammu & Kashmir": "Jammu And Kashmir",
    "Uttaranchal": "Uttarakhand"
}

rain["State"] = rain["State"].replace(state_corrections)


# --- Merge datasets ---
merged = pd.merge(crop, rain, on=["State", "Year"], how="left")

# --- Save final merged dataset ---
merged.to_csv("final_merged_data.csv", index=False)

# --- Print check summary ---
print("✅ Merged dataset created successfully!")
print("Total rows:", len(merged))
print("Non-null rainfall values:", merged["Rainfall_mm"].notna().sum())
print("\nSample preview:")
print(merged.head())
