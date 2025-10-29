# import pandas as pd

# data = pd.read_csv("final_merged_data.csv", skiprows=[1], low_memory=False)
# print("Rainfall column preview:")
# print(data["Rainfall_mm"].head(20))

# print("\nNon-null rainfall values count:", data["Rainfall_mm"].notna().sum())


# import pandas as pd

# rain = pd.read_csv("rainfall.csv")
# print(rain.head(10))
# print(list(rain.columns))


#sk-90b13d27f3244eab9ee65e575d5869bf

# import google.generativeai as genai
# genai.configure(api_key="AIzaSyCeuJjPUJs4LJfsF3g9x-UaYP_NzQnQugM")

# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)
