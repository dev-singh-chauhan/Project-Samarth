import pandas as pd

# ---------- RAINFALL DATA CLEANING ----------
rain = pd.read_csv("rainfall.csv", header=None)

# Assign 19 column names (based on your rainfall CSV)
rain.columns = [
    "State", "Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
    "Aug", "Sep", "Oct", "Nov", "Dec", "Annual", "Jan-Feb", "Jun-Sep", "Oct-Dec", "Extra"
]

# Keep only required columns
rain = rain[["State", "Year", "Annual"]]
rain = rain.rename(columns={"Annual": "Rainfall_mm"})
rain.to_csv("clean_rainfall.csv", index=False)

# ---------- CROP PRODUCTION DATA CLEANING ----------
crop = pd.read_csv("crop_production.csv", header=None)

# Assign proper column names (based on your CSV sample)
crop.columns = [
    "Index", "State", "District", "Year", "Season", "Crop", "Area_Hectare", "Production_Tonnes"
]

# Keep only the useful columns
crop = crop[["State", "District", "Year", "Season", "Crop", "Area_Hectare", "Production_Tonnes"]]
crop.to_csv("clean_crop.csv", index=False)

print("✅ Clean files ready!")
