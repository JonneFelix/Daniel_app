import streamlit as st

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

st.title("Optimale Herzfrequenz-Rechner für Trainingszonen")
st.write("Berechne die optimale Herzfrequenz basierend auf deinem Alter, deiner Ruheherzfrequenz und optional deiner maximalen Herzfrequenz.")

# Eingaben des Nutzers
age = st.number_input("Alter (in Jahren):", min_value=1, max_value=120, value=30)
resting_hr = st.number_input("Ruheherzfrequenz (in bpm):", min_value=30, max_value=150, value=70)
max_hr_option = st.checkbox("Maximale Herzfrequenz manuell eingeben")
max_hr = None

if max_hr_option:
    max_hr = st.number_input("Maximale Herzfrequenz (in bpm):", min_value=100, max_value=220, value=190)

# Zonen berechnen
if st.button("Berechnen"):
    zones = calculate_heart_rate_zones(age, resting_hr, max_hr)

    st.subheader("Trainingszonen:")
    for zone, (low, high) in zones.items():
        st.write(f"{zone}: {int(low)} - {int(high)} bpm")
