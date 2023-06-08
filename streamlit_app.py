import streamlit as st
import numpy as np
import pandas as pd
st.title("house_expenditure")

import streamlit as st
import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

import streamlit as st
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name

