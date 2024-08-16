import streamlit as st
import pandas as pd
import numpy as np
import datetime
from streamlit_gsheets import GSheetsConnection
from streamlit.dataframe_util import convert_anything_to_pandas_df

# Streamlit app title
st.title("Form Pekerjaan")

# Select box for choosing the type of work
job_type = st.selectbox("Jenis Pekerjaan",
                        options=["", "Kocor Pupuk", "Spray"])

if job_type == "Kocor Pupuk":
    st.header("Form Pemupukan Kocor")

    conn = st.connection('gsheets', type=GSheetsConnection)
    existing_data = conn.read(worksheet='pupuk_kocor',
                              usecols=list(range(7)),
                              ttl=5)

    # Load data
    blok_katalog = pd.read_csv('lokasi_katalog.csv', header=None)
    blok_katalog_options = blok_katalog.values.flatten().tolist()

    pupuk_katalog = pd.read_csv('pupuk_katalog.csv', header=None)
    pupuk_katalog.columns = ['Material', 'Unit']
    pupuk_katalog['Takaran'] = 0

    # Reorder columns
    pupuk_katalog = pupuk_katalog[['Material', 'Takaran', 'Unit']]

    # User input fields
    date = st.date_input("Tanggal Pelaksanaan")
    dropdown_selection = st.selectbox("Lokasi",
                                      options=blok_katalog_options,
                                      index=None)
    tangki = st.number_input("Jumlah Tangki",
                             min_value=0,
                             max_value=120,
                             step=1)

    pupuk_katalog_reset = pupuk_katalog.reset_index(drop=True)
    data_editor = st.data_editor(pupuk_katalog_reset)

    # Create new data DataFrame
    new_data = pd.DataFrame(columns=existing_data.columns)
    for index, row in data_editor.iterrows():
        material = row['Material']
        takaran = row['Takaran']
        unit = row['Unit']
        new_row = {
            'tanggal_pengisian': datetime.date.today(),
            'tanggal_pelaksanaan': date,
            'blok': dropdown_selection,
            'jumlah_tangki': tangki,
            'material': material,
            'takaran': takaran,
            'unit': unit
        }
        new_data = pd.concat([new_data, pd.DataFrame([new_row])],
                             ignore_index=True)

    # Drop rows with zero takaran
    new_data = new_data[new_data['takaran'] != 0]

    save_button = st.button('Save')

    if save_button:
        if not date or not dropdown_selection:
            st.warning("Pengisian data belum lengkap!")
            st.stop()
        elif tangki == 0:
            st.warning("Jumlah tangki tidak boleh nol!")
            st.stop()
        else:
            updated_data = pd.concat([existing_data, new_data],
                                     ignore_index=True)
            conn.update(worksheet='pupuk_kocor', data=updated_data)
            st.success("Data berhasil disimpan!")

elif job_type == "Spray":
    st.header("Form Penyemprotan (Spray)")

    conn = st.connection('gsheets', type=GSheetsConnection)
    existing_data = conn.read(worksheet='spray', usecols=list(range(7)), ttl=5)

    # Load data
    blok_katalog = pd.read_csv('lokasi_katalog.csv', header=None)
    blok_katalog_options = blok_katalog.values.flatten().tolist()

    spray_katalog = pd.read_csv('spray_katalog.csv', header=None)
    spray_katalog.columns = ['Material', 'Unit']
    spray_katalog['Takaran'] = 0

    # Reorder columns
    spray_katalog = spray_katalog[['Material', 'Takaran', 'Unit']]

    # User input fields
    date = st.date_input("Tanggal Pelaksanaan")
    dropdown_selection = st.selectbox("Lokasi",
                                      options=blok_katalog_options,
                                      index=None)
    tangki = st.number_input("Jumlah Tangki",
                             min_value=0,
                             max_value=120,
                             step=1)

    spray_katalog_reset = spray_katalog.reset_index(drop=True)
    data_editor = st.data_editor(spray_katalog_reset)

    # Create new data DataFrame
    new_data = pd.DataFrame(columns=existing_data.columns)
    for index, row in data_editor.iterrows():
        material = row['Material']
        takaran = row['Takaran']
        unit = row['Unit']
        new_row = {
            'tanggal_pengisian': datetime.date.today(),
            'tanggal_pelaksanaan': date,
            'blok': dropdown_selection,
            'jumlah_tangki': tangki,
            'material': material,
            'takaran': takaran,
            'unit': unit
        }
        new_data = pd.concat([new_data, pd.DataFrame([new_row])],
                             ignore_index=True)

    # Drop rows with zero takaran
    new_data = new_data[new_data['takaran'] != 0]

    save_button = st.button('Save')

    if save_button:
        if not date or not dropdown_selection:
            st.warning("Pengisian data belum lengkap!")
            st.stop()
        elif tangki == 0:
            st.warning("Jumlah tangki tidak boleh nol!")
            st.stop()
        else:
            updated_data = pd.concat([existing_data, new_data],
                                     ignore_index=True)
            conn.update(worksheet='spray', data=updated_data)
            st.success("Data berhasil disimpan!")

st.markdown('''
---
Created by [Java in Paradise](https://github.com/your-github)
''')
