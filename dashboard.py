
import streamlit as st
import pandas as pd
import plotly.express as px
from Gemini_qa_engine import answer_question

try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from Gemini_qa_engine import answer_question
    voice_supported = False

    # Try importing optional modules (safe for Streamlit Cloud)
    try:
        import speech_recognition as sr
        from gtts import gTTS
        import tempfile
        import os
        voice_supported = True
    except ImportError:
        st.warning("🎙️ Voice features not supported on this deployment environment.")

except Exception as e:
    st.error(f"Critical import error: {e}")
    st.stop()

# -----------------------------------------------
# 🌱 PAGE CONFIGURATION
# -----------------------------------------------
st.set_page_config(page_title="Project Samarth", layout="wide", page_icon="🌾")

# -----------------------------------------------
# 🌾 HEADER
# -----------------------------------------------
st.title("🌾 Project Samarth: AI-Powered Agricultural Insights")
st.caption("Integrating IMD Rainfall + Crop Production datasets from data.gov.in with Gemini AI")

# -----------------------------------------------
# 📂 LOAD DATA
# -----------------------------------------------
try:
    data = pd.read_csv("final_merged_data.csv")
    data.columns = data.columns.str.strip().str.replace(" ", "_")
    for col in ["Rainfall_mm", "Production_Tonnes", "Area_Hectare", "Year"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    st.sidebar.success("✅ Data loaded successfully!")
except Exception as e:
    st.sidebar.error(f"⚠️ Error loading data: {e}")
    data = None

# -----------------------------------------------
# 🧭 CREATE TABS
# -----------------------------------------------
if voice_supported:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Data Insights",
        "📈 Advanced Analytics",
        "💬 Ask Samarth AI",
        "🎤 Talk to Samarth",
        "ℹ️ About Project"
    ])
else:
    tab1, tab2, tab3, tab5 = st.tabs([
        "📊 Data Insights",
        "📈 Advanced Analytics",
        "💬 Ask Samarth AI",
        "ℹ️ About Project"
    ])

# -----------------------------------------------
# TAB 1: DATA INSIGHTS
# -----------------------------------------------
with tab1:
    if data is not None:
        st.sidebar.header("🔍 Filter Data")
        states = sorted(data["State"].dropna().unique())
        selected_state = st.sidebar.selectbox("Select a State", states)
        filtered_data = data[data["State"] == selected_state]

        st.subheader(f"📍 Data Overview for {selected_state}")
        st.dataframe(filtered_data.head(), use_container_width=True)

        if "Rainfall_mm" in filtered_data.columns:
            fig1 = px.line(filtered_data, x="Year", y="Rainfall_mm",
                           title=f"🌧 Rainfall Trend in {selected_state}", markers=True)
            st.plotly_chart(fig1, use_container_width=True)

        if "Production_Tonnes" in filtered_data.columns:
            fig2 = px.line(filtered_data, x="Year", y="Production_Tonnes", color="Crop",
                           title=f"🌾 Crop Production Trends in {selected_state}", markers=True)
            st.plotly_chart(fig2, use_container_width=True)

        if "Rainfall_mm" in filtered_data.columns and "Production_Tonnes" in filtered_data.columns:
            corr = filtered_data["Rainfall_mm"].corr(filtered_data["Production_Tonnes"])
            st.metric(label="📊 Correlation (Rainfall vs Crop Production)", value=f"{corr:.2f}")

        st.caption("🔗 Source: data.gov.in — IMD Rainfall & Ministry of Agriculture datasets")
    else:
        st.error("⚠️ Data not loaded. Please check final_merged_data.csv file.")

# -----------------------------------------------
# TAB 2: ADVANCED ANALYTICS
# -----------------------------------------------
with tab2:
    if data is not None:
        st.header("📈 Advanced Analytics")

        states = st.multiselect("Select States for Comparison", sorted(data["State"].unique()))
        crops = st.multiselect("Select Crops", sorted(data["Crop"].unique()))
        year_range = st.slider("Select Year Range", int(data["Year"].min()), int(data["Year"].max()),
                               (int(data["Year"].min()), int(data["Year"].max())))

        mask = (data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])
        df_filtered = data[mask]

        if states:
            df_filtered = df_filtered[df_filtered["State"].isin(states)]
        if crops:
            df_filtered = df_filtered[df_filtered["Crop"].isin(crops)]

        st.markdown("### 🌦 Rainfall vs Production Comparison")
        if not df_filtered.empty:
            fig3 = px.scatter(df_filtered, x="Rainfall_mm", y="Production_Tonnes",
                              color="State", size="Area_Hectare",
                              hover_data=["Crop", "Year"],
                              title="Rainfall vs Production across Selected States & Crops")
            st.plotly_chart(fig3, use_container_width=True)

            yearly = df_filtered.groupby(["State", "Year"]).agg({
                "Rainfall_mm": "mean",
                "Production_Tonnes": "sum"
            }).reset_index()

            fig4 = px.line(yearly, x="Year", y="Rainfall_mm", color="State",
                           title="Average Annual Rainfall per State")
            st.plotly_chart(fig4, use_container_width=True)

            fig5 = px.line(yearly, x="Year", y="Production_Tonnes", color="State",
                           title="Total Crop Production per State")
            st.plotly_chart(fig5, use_container_width=True)

            st.caption("📘 Insights generated from merged IMD rainfall & agriculture datasets.")
        else:
            st.warning("Select at least one State and one Crop to analyze.")

# -----------------------------------------------
# TAB 3: ASK SAMARTH AI
# -----------------------------------------------
with tab3:
    st.subheader("💬 Ask Samarth AI Anything")
    st.markdown("""
    Ask complex, natural questions such as:
    - *Compare average rainfall in Punjab and Kerala over the last 10 years.*
    - *Which state produced the most rice in 2020?*
    - *How does rainfall affect wheat yield in Uttar Pradesh?*
    """)

    user_query = st.text_area("Type your question here:", height=100)
    include_sources = st.checkbox("Include Source Citations", value=True)

    if st.button("Ask Question"):
        if user_query.strip():
            with st.spinner("Gemini is analyzing your question..."):
                sample = data.sample(min(500, len(data)))
                context = sample[["State", "Year", "Crop", "Rainfall_mm", "Production_Tonnes"]].to_csv(index=False)

                prompt = f"""
You are Samarth AI, an expert on Indian agriculture and climate data.
User asked: "{user_query}"
Use the following dataset context (from data.gov.in merged rainfall & crop datasets):

{context}

Provide a factual, concise answer and cite data sources.
"""
                response = answer_question(prompt)
                if include_sources:
                    response += "\n\n📘 Source: data.gov.in — IMD Rainfall & Ministry of Agriculture datasets"

                st.success("✅ AI Response")
                st.write(response)
        else:
            st.warning("Please enter a question first.")

# -----------------------------------------------
# TAB 4: TALK TO SAMARTH (Voice)
# -----------------------------------------------
if voice_supported:
    with tab4:
        st.subheader("🎙️ Talk to Samarth (Voice AI)")
        st.markdown("Click below to speak your question:")

        if st.button("🎤 Start Recording"):
            recognizer = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    st.info("🎧 Listening... please speak now.")
                    audio = recognizer.listen(source, phrase_time_limit=8)

                user_question = recognizer.recognize_google(audio)
                st.success(f"🗣️ You said: {user_question}")

                with st.spinner("Samarth is thinking..."):
                    ai_answer = answer_question(user_question)
                    ai_answer += "\n\n📘 Source: data.gov.in — IMD & Ministry of Agriculture"
                    st.write(ai_answer)

                # 🔊 Text-to-Speech
                tts = gTTS(ai_answer)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_file.name)
                st.audio(temp_file.name, format="audio/mp3")

            except Exception as e:
                st.error(f"⚠️ Voice recognition unavailable or failed: {e}")

# -----------------------------------------------
# TAB 5: ABOUT PROJECT
# -----------------------------------------------
with tab5:
    st.header("ℹ️ About Project Samarth")
    st.markdown("""
**Project Samarth** is an intelligent agricultural analytics system combining **open government data** with **Gemini AI reasoning**.

### 💡 Key Features
- 🌧️ Real-time Rainfall & Crop Correlation Analysis  
- 🤖 Gemini-powered Q&A and reasoning  
- 🎤 Voice interaction (where supported)  
- 📊 Advanced visualization with Plotly  
- 🔗 Source: [data.gov.in](https://data.gov.in)

### 🧠 Architecture
1. **Data Layer:** IMD + Ministry of Agriculture datasets  
2. **AI Layer:** Gemini Q&A reasoning  
3. **Frontend:** Streamlit dashboard with charts, chat, and voice

---
🌾 *Empowering Indian Agriculture through AI and Open Data (© 2025)*
""")

st.caption("🌱 Developed by Dev Singh Chauhan | Powered by Gemini AI | Project Samarth © 2025")
