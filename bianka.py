import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import date

DB_NAME = "bianka"
DB_USER = "postgres"
DB_PASSWORD = "Knoting13"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def insert_data(datum, idopont, etel, szenhidrat, vercukor_elotte, vercukor_utana):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO naplo (datum, idopont, etel, szenhidrat, vercukor_elotte, vercukor_utana)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (datum, idopont, etel, szenhidrat, vercukor_elotte, vercukor_utana))
            conn.commit()

def load_data():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM naplo ORDER BY datum DESC, id ASC;")
            rows = cur.fetchall()
            return pd.DataFrame(rows)

def main():
    st.set_page_config(page_title="Bianka napló", layout="centered")

    oldal = st.sidebar.radio("Menü", ["Új bejegyzés", "Adatok megtekintése"])

    if oldal == "Új bejegyzés":
        st.title("📝 Cirmos étkezési adatai")

        with st.form("uj_bejegyzes", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                datum = st.date_input("📅 Dátum", value=date.today())
                idopont = st.selectbox("⏰ Időpont", ["Reggeli", "Tízórai", "Ebéd", "Uzsonna", "Vacsora", "Nasi"])
                etel = st.text_input("🍽️ Étel")

            with col2:
                szenhidrat = st.number_input("🥖 Szénhidrát (g)", min_value=0.0, format="%.1f")
                vercukor_elotte = st.number_input("🩸 Vércukorszint előtte", min_value=0.0, format="%.1f")
                vercukor_utana = st.number_input("🩸 Vércukorszint utána", min_value=0.0, format="%.1f")

            submitted = st.form_submit_button("💾 Mentés")
            if submitted:
                insert_data(datum, idopont, etel, szenhidrat, vercukor_elotte, vercukor_utana)
                st.success("✅ Bejegyzés elmentve!")

    elif oldal == "Adatok megtekintése":
        st.title("📊 Mentett adatok")
        df = load_data()
        if df.empty:
            st.info("Nincs elmentett adat.")
        else:
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()


