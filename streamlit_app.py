import streamlit as st
import numpy as np
import pandas as pd
st.title("house_expenditure")
import requests

url = 'https://raw.githubusercontent.com/user/repo/branch/path/to/file.csv'

response = requests.get(url)

if response.status_code == 200:
    with open('file.csv', 'wb') as f:
        f.write(response.content)

