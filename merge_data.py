import pandas as pd

# Load both cleaned datasets
rain = pd.read_csv("clean_rainfall.csv")
crop = pd.read_csv("clean_crop.csv")

# Merge on State and Year (common columns)
merged = pd.merge(crop, rain, on=["State", "Year"], how="left")

# Save the final dataset
merged.to_csv("final_merged_data.csv", index=False)

print("✅ Final merged dataset ready! -> final_merged_data.csv")
