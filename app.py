# app.py — fixed numeric conversion version
import pandas as pd

# Step 1: Load the merged dataset safely
data = pd.read_csv("final_merged_data.csv", low_memory=False)

# Step 2: Clean up the column names (remove any stray spaces)
data.columns = data.columns.str.strip()

# Step 3: Convert numeric columns safely
for col in ['Rainfall_mm', 'Production_Tonnes', 'Area_Hectare', 'Year']:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Step 4: Preview data
print("📊 Here's a glimpse of your cleaned data:")
print(data.head())

# Step 5: Basic analysis
print("\n🌦️ Average rainfall by state:")
avg_rain = data.groupby('State')['Rainfall_mm'].mean().round(2)
print(avg_rain)

print("\n🌾 Average crop production by state:")
avg_prod = data.groupby('State')['Production_Tonnes'].mean().round(2)
print(avg_prod)

print("\n🔗 Correlation between rainfall and crop production:")
corr = data['Rainfall_mm'].corr(data['Production_Tonnes'])
print(f"Correlation value: {corr:.2f}")

# Step 6: Export summary
summary = pd.DataFrame({
    'Average_Rainfall_mm': avg_rain,
    'Average_Production_Tonnes': avg_prod
})
summary.to_csv("state_summary.csv")
print("\n✅ Analysis complete! Summary saved as 'state_summary.csv'")
