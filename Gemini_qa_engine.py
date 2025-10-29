import os
import pandas as pd
import google.generativeai as genai

# ================== SETUP ==================
# 🔑 Configure Gemini API key (keep this secure, never push to GitHub)
os.environ["GOOGLE_API_KEY"] = "AIzaSyCeuJjPUJs4LJfsF3g9x-UaYP_NzQnQugM"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load Gemini model
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

# Load and prepare dataset
try:
    data = pd.read_csv("final_merged_data.csv")
    data.columns = [c.strip().replace(" ", "_") for c in data.columns]
    data.dropna(subset=["State", "Crop", "Production_Tonnes"], inplace=True)
    print("✅ Data loaded successfully. Gemini Q&A Engine ready!\n")
except Exception as e:
    print(f"Error loading data: {e}")
    data = None


# ================== CORE FUNCTION ==================
def answer_question(question: str) -> str:
    """
    Main function to answer user questions using both
    data insights (via pandas) and Gemini reasoning.
    """

    if data is None:
        return " Data not available. Please check final_merged_data.csv."

    q_lower = question.lower()
    result_text = ""

    try:
        #  Try to detect state and crop automatically
        detected_state = next((state for state in data["State"].unique() if state.lower() in q_lower), None)
        detected_crop = next((crop for crop in data["Crop"].unique() if crop.lower() in q_lower), None)

        if detected_state and detected_crop:
            df = data[
                (data["State"].str.lower() == detected_state.lower()) &
                (data["Crop"].str.lower() == detected_crop.lower())
            ]

            if df.empty:
                result_text = f"No data found for {detected_crop} in {detected_state}."
            else:
                # Analyze trend (last 10 years if available)
                recent_years = sorted(df["Year"].unique())[-10:]
                df_recent = df[df["Year"].isin(recent_years)]
                trend = df_recent.groupby("Year")["Production_Tonnes"].sum()

                avg_prod = trend.mean()
                change = ((trend.iloc[-1] - trend.iloc[0]) / trend.iloc[0]) * 100 if len(trend) > 1 else 0

                result_text += (
                    f"📊 {detected_crop.title()} Production in {detected_state.title()} (Last Decade):\n"
                    f"{trend.to_string()}\n\n"
                    f"Average Production: {avg_prod:,.2f} tonnes\n"
                    f"Change Over Period: {change:+.2f}%\n"
                )
        else:
            result_text = (
                "🔍 Could not find a clear match for crop or state.\n"
                "Gemini will still try to answer the question based on general data context.\n"
            )

    except Exception as e:
        result_text = f"⚠️ Error analyzing data: {e}"

    # ========== Gemini Reasoning ==========
    prompt = f"""
    The user asked: "{question}"

    Here is the summarized agricultural data:
    {result_text}

    Use this data and your reasoning to provide a clear, concise, and insightful answer
    (mention trends, insights, and possible implications if relevant).
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini API Error: {e}"


# ================== CLI TESTING MODE ==================
if __name__ == "__main__":
    print("🤖 Gemini Agricultural Q&A Engine Running... Type 'exit' to stop.\n")
    while True:
        q = input("Ask a question: ")
        if q.lower() == "exit":
            break
        print("\nAnswer:", answer_question(q), "\n")

