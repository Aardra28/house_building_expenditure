import streamlit as st
import numpy as np
import pandas as pd
st.title("house_expenditure")

#data=pd.read_csv("house_building_expenditure.csv")
#print(data)
#data

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('house_building_expenditure.csv')

# Get the date and expense columns
date_col = df['Date']
expense_col = df['Expense']

# Get the selected date or range of dates
selected_date = input('Enter a date (YYYY-MM-DD): ')
selected_range = input('Enter a range of dates (YYYY-MM-DD): ')

# Get the total expense for the selected date or range of dates
if selected_date:
    total_expense = df[df['Date'] == selected_date]['Expense'].sum()
elif selected_range:
    total_expense = df[df['Date'].between(selected_range[0], selected_range[1])]['Expense'].sum()

# Plot the expenses
plt.plot(date_col, expense_col)
plt.xlabel('Date')
plt.ylabel('Expense')
plt.title('Expenses')
plt.show()

# Print the total expense
print('Total expense:', total_expense)

