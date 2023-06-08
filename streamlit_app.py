import streamlit as st
import numpy as np
import pandas as pd

st.title("house_expenditure")

#data=pd.read_csv("house_building_expenditure.csv")
#print(data)
#data

# Read the CSV file
import tkinter as tk
import pandas as pd

# Read the expense data from CSV
df = pd.read_csv('house_building_expenditure.csv')

# Function to calculate total expenses and display in GUI
def calculate_expenses():
    selected_start_date = start_date_entry.get()
    selected_end_date = end_date_entry.get()
    selected_attribute = attribute_entry.get()
    
    selected_expenses = df[(df['Date'] >= selected_start_date) & (df['Date'] <= selected_end_date) & (df['Attribute'] == selected_attribute)]
    total_expenses = selected_expenses['Expense'].sum()
    
    result_label.config(text=f"Total expenses of {selected_attribute} from {selected_start_date} to {selected_end_date}: {total_expenses}")

# Create GUI window
window = tk.Tk()
window.title("Expense Calculator")

# Date range input fields
start_date_label = tk.Label(window, text="Start Date (YYYY-MM-DD): ")
start_date_label.pack()
start_date_entry = tk.Entry(window)
start_date_entry.pack()

end_date_label = tk.Label(window, text="End Date (YYYY-MM-DD): ")
end_date_label.pack()
end_date_entry = tk.Entry(window)
end_date_entry.pack()

# Attribute input field
attribute_label = tk.Label(window, text="Attribute: ")
attribute_label.pack()
attribute_entry = tk.Entry(window)
attribute_entry.pack()

# Calculate button
calculate_button = tk.Button(window, text="Calculate", command=calculate_expenses)
calculate_button.pack()

# Result label
result_label = tk.Label(window, text="")
result_label.pack()

# Start GUI event loop
window.mainloop()


