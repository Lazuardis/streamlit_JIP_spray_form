import streamlit as st
import pandas as pd
import numpy as np
import datetime

# Streamlit app title
st.title("Form Penyemprotan (Spray)")

# Load data
spray_data = pd.read_csv('form_spray.csv')
blok_katalog = pd.read_csv('lokasi_katalog.csv', header=None)
blok_katalog_options = blok_katalog.values.flatten().tolist()

spray_katalog = pd.read_csv('spray_katalog.csv', header=None)
spray_katalog.columns = ['Material', 'Unit']
spray_katalog['Takaran'] = 0

# Reorder columns name of spray_katalog into Material, Takaran, Unit 
spray_katalog = spray_katalog[['Material', 'Takaran', 'Unit']]

# User input fields
st.header("Enter your data:")
date = st.date_input("Tanggal Pelaksanaan")
dropdown_selection = st.selectbox("Lokasi", blok_katalog_options)
tangki = st.number_input("Jumlah Tangki", min_value=0, max_value=120, step=1)

# Remove the index for display
spray_katalog_reset = spray_katalog.reset_index(drop=True)

# Use data_editor to edit data without showing index
data_editor = st.data_editor(spray_katalog_reset)

# Create new_data DataFrame with the same columns as spray_data
new_data = pd.DataFrame(columns=spray_data.columns)

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
if st.button('Save'):
    spray_data = pd.concat([spray_data, new_data], ignore_index=True)
    spray_data.to_csv('form_spray.csv', index=False)
    st.success("Data Sukses Tersimpan!")

st.markdown('''
---
Created by [Java in Paradise](https://github.com/your-github)
''')
