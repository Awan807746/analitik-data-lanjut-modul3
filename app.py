import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector


# ==========================================
# KONEKSI KE DATABASE
# ==========================================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_dal"
    )


# ==========================================
# MENGAMBIL DATA DARI DATABASE
# ==========================================
def get_data_from_db():
    conn = get_connection()

    query = """
    SELECT id, semester, jumlah, program_studi, universitas
    FROM pddikti_example
    """

    data = pd.read_sql(query, conn)

    conn.close()

    return data


# ==========================================
# JUDUL APLIKASI
# ==========================================
st.title("Streamlit Simple App")


# ==========================================
# NAVIGASI
# ==========================================
page = st.sidebar.radio(
    "Pilih halaman",
    ["Dataset", "Visualisasi", "Form Input"]
)


# ==========================================
# HALAMAN DATASET
# ==========================================
if page == "Dataset":

    st.header("Halaman Dataset")

    data = get_data_from_db()

    st.write(data)


# ==========================================
# HALAMAN VISUALISASI
# ==========================================
elif page == "Visualisasi":

    st.header("Halaman Visualisasi")

    data = get_data_from_db()

    # Pilih universitas
    selected_university = st.selectbox(
        "Pilih Universitas",
        data["universitas"].unique()
    )

    # Filter data berdasarkan universitas
    filtered_data = data[
        data["universitas"] == selected_university
    ]

    # Membuat grafik
    fig, ax = plt.subplots(figsize=(12, 6))

    for program_studi in filtered_data["program_studi"].unique():

        subset = filtered_data[
            filtered_data["program_studi"] == program_studi
        ]

        # Urutkan berdasarkan ID
        subset = subset.sort_values(
            by="id",
            ascending=False
        )

        ax.plot(
            subset["semester"],
            subset["jumlah"],
            label=program_studi
        )

    ax.set_title(
        "Visualisasi Data untuk " + selected_university
    )

    ax.set_xlabel("Semester")
    ax.set_ylabel("Jumlah")

    plt.xticks(rotation=90)

    ax.legend()

    st.pyplot(fig)


# ==========================================
# HALAMAN FORM INPUT
# ==========================================
elif page == "Form Input":

    st.header("Halaman Form Input")

    with st.form("form_input"):

        # Semester
        semester = st.text_input(
            "Semester",
            value="Gasal 2023"
        )

        # Jumlah
        jumlah = st.number_input(
            "Jumlah",
            min_value=0,
            value=100,
            step=1
        )

        # Program Studi
        program_studi = st.text_input(
            "Program Studi",
            value="Program Studi 1"
        )

        # Universitas
        universitas = st.text_input(
            "Universitas",
            value="UNIVERSITAS A"
        )

        # Tombol Submit
        submit = st.form_submit_button("Submit")

        if submit:
            st.success("Data berhasil dikirim!")