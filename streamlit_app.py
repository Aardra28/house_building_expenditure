import streamlit as st
import numpy as np
import pandas as pd
st.title("house_expenditure")
import requests

url = 'house_building_expenditure.csv'

response = requests.get(url)

if response.status_code == 200:
    with open('file.csv', 'wb') as f:
        f.write(response.content)

