import pandas as pd

# Read the CSV properly — skip the duplicate header row
data = pd.read_csv("final_merged_data.csv", skiprows=[1], low_memory=False)

# Convert numeric columns safely
data["Rainfall_mm"] = pd.to_numeric(data["Rainfall_mm"], errors="coerce")

# Drop missing rainfall or state rows
data = data.dropna(subset=["State", "Rainfall_mm"])

# Group by state and calculate average rainfall
avg_rain = data.groupby("State")["Rainfall_mm"].mean()

if avg_rain.empty:
    print("No valid rainfall data found — check the dataset or merging step.")
else:
    top_state = avg_rain.idxmax()
    top_value = avg_rain.max()
    print(f"The state with the highest average rainfall is **{top_state}** with an average of {round(top_value, 2)} mm per year.")
