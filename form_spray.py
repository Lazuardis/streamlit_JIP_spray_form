import streamlit as st
import pandas as pd
import numpy as np
import datetime
from streamlit_gsheets import GSheetsConnection

# Streamlit app title
st.title("Form Penyemprotan (Spray)")

conn = st.connection('gsheets', type=GSheetsConnection)

existing_data = conn.read(worksheet='spray', usecols=list(range(7)), ttl=5)

# st.dataframe(existing_data)

# Load data

blok_katalog = pd.read_csv('lokasi_katalog.csv', header=None)
blok_katalog_options = blok_katalog.values.flatten().tolist()

spray_katalog = pd.read_csv('spray_katalog.csv', header=None)
spray_katalog.columns = ['Material', 'Unit']
spray_katalog['Takaran'] = 0

# Reorder columns name of spray_katalog into Material, Takaran, Unit 
spray_katalog = spray_katalog[['Material', 'Takaran', 'Unit']]

# User input fields
st.header("Enter your data:")
date = st.date_input(label="Tanggal Pelaksanaan")
dropdown_selection = st.selectbox("Lokasi", options=blok_katalog_options, index=None)
tangki = st.number_input("Jumlah Tangki", min_value=0, max_value=120, step=1)

# Remove the index for display
spray_katalog_reset = spray_katalog.reset_index(drop=True)

# Use data_editor to edit data without showing index
data_editor = st.data_editor(spray_katalog_reset)

# Create new_data DataFrame with the same columns as spray_data
new_data = pd.DataFrame(columns=existing_data.columns)

# Populate new_data with the values from data_editor and the input fields
for index, row in data_editor.iterrows():
    material = row['Material']
    takaran = row['Takaran']
    unit =  row['Unit']
    new_row = {
        'tanggal_pengisian': datetime.date.today(),
        'tanggal_pelaksanaan': date,
        'blok': dropdown_selection,
        'jumlah_tangki': tangki,
        'material': material,
        'takaran': takaran,
        'unit': unit
    }
    new_data = pd.concat([new_data, pd.DataFrame([new_row])], ignore_index=True)

# Drop rows with zero takaran
new_data = new_data[new_data['takaran'] != 0]

# # Show the new_data DataFrame
# st.write("New Data to be Saved:")
# st.dataframe(new_data)

# Save the new data to CSV (append mode)
save_button = st.button('Save')

if save_button:
    if not date or not dropdown_selection:
        st.warning("Pengisian data belum lengkap!")
        st.stop()
    elif tangki == 0:
        st.warning("Jumlah tangki tidak boleh nol!")
        st.stop()
    else:
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        
        conn.update(worksheet='spray', data = updated_data)

        st.success("Data berhasil disimpan!")

st.markdown('''
---
Created by [Java in Paradise](https://github.com/your-github)
''')
