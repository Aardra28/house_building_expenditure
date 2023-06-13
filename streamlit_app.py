import streamlit as st
import pandas as pd
import altair as alt
import datetime

primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"
def main():
    navigation = st.sidebar.radio(options=["About", "Home", "Update"], label="Navigation", index=get_navigation_index())

    if navigation == 'About':
        about()
    elif navigation == 'Home':
        home()
    elif navigation == 'Update':
        update()

def get_navigation_index():
    navigation = st.experimental_get_query_params().get("navigation", ["About"])
    if navigation[0] == "Home":
        return 1
    elif navigation[0] == "Update":
        return 2
    else:
        return 0

def about():
    st.markdown("<h1 style='color:#45145a; font-family: Sans serif;font-size: 100px;'>House Building Expense</h1>", unsafe_allow_html=True)

    st.title("About")
    st.write("to estimate your house construction expense...")

    if st.button('HOME'):
        st.experimental_set_query_params(navigation="Home")


def home():
    st.markdown("<h1 style='text-align: center; color:#752673;font-size: 60px;'>Welcome!</h1>", unsafe_allow_html=True)

    st.title("")
    st.title("Wanna estimate your house price....")
    st.title("")

    if st.button('WANT TO UPDATE OR PREDICT'):
        if st.experimental_get_query_params().get("navigation") == ["Update"]:
            st.experimental_set_query_params(navigation="Home")
        else:
            st.experimental_set_query_params(navigation="Update")

    if st.button('ABOUT'):
        st.experimental_set_query_params(navigation="About")


def update():
    st.markdown("<h1>Update Selection</h1>", unsafe_allow_html=True)
    st.write("to make changes..")
    data = pd.read_csv("/home/aardra/Downloads/house_building_expenditure.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Update Selection
    st.header("Add and Remove Data")
    update_option = st.radio('Update dataset?', ('Add entries', 'Remove entries', 'No'))
    st.write('You selected:', update_option)

    if update_option == 'Add entries':
        st.header("Add New Data")
        new_date = st.date_input("Choose the date", datetime.date(2023, 7, 6))
        new_date_with_time = pd.to_datetime(new_date).strftime('%Y-%m-%d %H:%M:%S')  # Convert to datetime format

        new_feature = st.radio('Select a feature', data.columns)
        new_cost = st.number_input("Enter the cost")

        if st.button("Add Data"):
            data.at[new_date_with_time, new_feature] = new_cost
            data.reset_index(inplace=True)
            data.to_csv("/home/aardra/Downloads/house_building_expenditure.csv", index=False)
            st.success("Data added successfully!")
            st.write(data)

    elif update_option == 'Remove entries':
        st.header("Remove Data")
        remove_date = st.date_input("Choose the date to remove entries", datetime.date(2023, 7, 6))

        st.write("Current Data:")
        st.write(data)

        remove_feature = st.radio('Select a feature', data.columns)

        if st.button("Remove Data"):
            data = data[~((data.index == remove_date) & (data[remove_feature] != None))]
            data.reset_index(inplace=True)
            data.to_csv("/home/aardra/Downloads/house_building_expenditure.csv", index=False)
            st.success("Data removed successfully!")
            st.write("Updated Data:")
            st.write(data)
    st.markdown("<h1>Data Analysis</h1>", unsafe_allow_html=True)

    st.header("Calculate the amount")
    option = st.selectbox('Select an option', ('Select date range', 'Select feature'))

    if option == 'Select date range':
        start_date = st.date_input("Select a start date")
        end_date = st.date_input("Select an end date")

        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date)

        filtered_data = data.loc[(data.index >= start_datetime) & (data.index <= end_datetime)]
        amount = filtered_data.sum().sum()

        st.write("Total Amount:")
        st.markdown(
            f"<style>.title-text{{color:BLACK;}}</style>",
            unsafe_allow_html=True
        )

        st.markdown(f"<h1 class='title-text'>{amount}</h1>", unsafe_allow_html=True)

        if not filtered_data.empty:
            st.write("Features and Costs for Selected Date Range:")
            non_null_data = filtered_data.dropna(how='all')

            for column in non_null_data.columns:
                if non_null_data[column].dtype == 'object':
                    non_null_data[column] = non_null_data[column].str.replace('"', '').str.replace(',', '').astype(float)

            non_zero_data = non_null_data.loc[:, (non_null_data != 0).any()]
            st.write(non_zero_data)

            chart_data = filtered_data.reset_index().melt('Date', var_name='Feature', value_name='Cost')

            line_chart = alt.Chart(chart_data).mark_line().encode(
                x='Date:T',
                y='Cost:Q',
                color=alt.Color('Feature:N', scale=alt.Scale(scheme='category20')),
                tooltip=['Feature', 'Cost']
            ).properties(
                width=600,
                height=400
            ).interactive()

            st.altair_chart(line_chart, use_container_width=True)

    elif option == 'Select feature':
        selected_feature_name = st.selectbox("Select a Feature", data.columns)
        feature_data = data[selected_feature_name]
        feature_sum = feature_data.sum()

        st.write(f"Total Amount for {selected_feature_name}:")
        st.markdown(
            f"<style>.title-text{{color: BLACK;}}</style>",
            unsafe_allow_html=True
        )

        st.markdown(f"<h1 class='title-text'>{feature_sum}</h1>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
