import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_heart_rate_zones(age, resting_hr, max_hr=None):
    if max_hr is None:
        max_hr = 220 - age  # Standardformel für maximale Herzfrequenz

    reserve_hr = max_hr - resting_hr

    # Trainingszonen basierend auf Prozenten der Herzfrequenz-Reserve
    zones = {
        "Erholung (50-60%)": (0.5 * reserve_hr + resting_hr, 0.6 * reserve_hr + resting_hr),
        "Fettverbrennung (60-70%)": (0.6 * reserve_hr + resting_hr, 0.7 * reserve_hr + resting_hr),
        "Aerob (70-80%)": (0.7 * reserve_hr + resting_hr, 0.8 * reserve_hr + resting_hr),
        "Anaerob (80-90%)": (0.8 * reserve_hr + resting_hr, 0.9 * reserve_hr + resting_hr),
        "Maximal (90-100%)": (0.9 * reserve_hr + resting_hr, max_hr),
    }

    return zones

# Streamlit App-Konfiguration
st.set_page_config(
    page_title="Herzfrequenz Rechner",
    page_icon="💓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏃 Optimale Herzfrequenz-Rechner")
st.write("Berechne deine optimale Herzfrequenz basierend auf Alter, Ruheherzfrequenz und optional deiner maximalen Herzfrequenz.")

# Eingaben in der Sidebar
with st.sidebar:
    st.header("Eingaben")
    age = st.number_input("Alter (in Jahren):", min_value=1, max_value=120, value=30)
    resting_hr = st.number_input("Ruheherzfrequenz (in bpm):", min_value=30, max_value=150, value=70)
    max_hr_option = st.checkbox("Maximale Herzfrequenz manuell eingeben")
    max_hr = None

    if max_hr_option:
        max_hr = st.number_input("Maximale Herzfrequenz (in bpm):", min_value=100, max_value=220, value=190)

# Zonenberechnung
zones = calculate_heart_rate_zones(age, resting_hr, max_hr)

# Ergebnisse anzeigen
st.subheader("Trainingszonen")
if zones:
    for zone, (low, high) in zones.items():
        st.write(f"{zone}: **{int(low)} - {int(high)} bpm**")

# Exportfunktion
st.subheader("Exportiere deine Ergebnisse")
if st.button("Ergebnisse als CSV herunterladen"):
    df = pd.DataFrame(zones).transpose()
    df.columns = ["Untergrenze (bpm)", "Obergrenze (bpm)"]
    csv = df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="trainingszonen.csv",
        mime="text/csv",
    )

# Erklärung der Trainingszonen
st.info(
    "**Trainingszonen:**\n"
    "- **Erholung (50-60%)**: Ideal für langsames Joggen und Regeneration.\n"
    "- **Fettverbrennung (60-70%)**: Verbessert die Grundlagenausdauer und hilft bei der Fettverbrennung.\n"
    "- **Aerob (70-80%)**: Steigert die allgemeine Fitness und Ausdauer.\n"
    "- **Anaerob (80-90%)**: Erhöht die Leistungsfähigkeit und Laktattoleranz.\n"
    "- **Maximal (90-100%)**: Für Spitzenleistungen und kurze intensive Belastungen."
)

# Visualisierung der Zonen
st.subheader("Visualisierung der Trainingszonen")
fig, ax = plt.subplots()
labels = list(zones.keys())
values = [high - low for _, (low, high) in zones.items()]
ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
st.pyplot(fig)

# Motivation und Feedback
st.success("Großartig! Halte deine Trainingszonen im Blick und bleib motiviert! 💪")
