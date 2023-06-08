import streamlit as st
import numpy as np
import pandas as pd

st.title("house_expenditure")

#data=pd.read_csv("house_building_expenditure.csv")
#print(data)
#data
import streamlit as st
import pandas as pd

# Read the expense data from CSV
df = pd.read_csv('house_building_expenditure.csv')

# Function to calculate total expenses and display in Streamlit
def calculate_expenses():
    selected_start_date = start_date_input.value
    selected_end_date = end_date_input.value
    selected_attribute = attribute_input.value
    
    selected_expenses = df[(df['Date'] >= selected_start_date) & (df['Date'] <= selected_end_date) & (df['Attribute'] == selected_attribute)]
    total_expenses = selected_expenses['Expense'].sum()
    
    result_text = f"Total expenses of {selected_attribute} from {selected_start_date} to {selected_end_date}: {total_expenses}"
    result_text = f"**{result_text}**"
    st.markdown(result_text)

# Create Streamlit app
st.title("Expense Calculator")

# Sidebar input fields
start_date_input = st.sidebar.text_input("Start Date (YYYY-MM-DD):")
end_date_input = st.sidebar.text_input("End Date (YYYY-MM-DD):")
attribute_input = st.sidebar.text_input("Attribute:")

# Calculate button
calculate_button = st.sidebar.button("Calculate", on_click=calculate_expenses)

# Result area
st.markdown("---")
result_text = "Total expenses will be displayed here."
st.markdown(result_text)



