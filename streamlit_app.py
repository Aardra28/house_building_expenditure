import streamlit as st
import pandas as pd
import altair as alt
import datetime
from streamlit_extras.let_it_rain import rain
import base64
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="HOUSE PRICE ESTIMATION",
    page_icon=":house:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("f4e2e1.png")
imga = get_img_as_base64("image2.jpg")


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{imga}");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
filter:blur
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
data = pd.read_csv("house_building_expenditure.csv")

def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=['Home', 'Main', 'Update'],
            icons=["house", "file-earmark-fill", "calendar-plus-fill"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

    if selected == 'Home':
        home()
    elif selected == 'Main':
        Main()
    elif selected == 'Update':
        update()

def get_navigation_index():
    selected = st.experimental_get_query_params().get("selected", ["Home"])
    if selected[0] == "Main":
        return 1
    elif selected[0] == "Update":
        return 2
    else:
        return 0

    
def home():
    st.markdown("<h1 style='color:#45145a; font-family: Sans serif;font-style:italic;font-size: 98px;'>House Building Expense</h1>", unsafe_allow_html=True)
    st.title("Wanna estimate your house price.")
    #if st.button('  CALCULATE  THE COST  '):
        #st.experimental_set_query_params(navigation="Main")
    #elif st.button('  MAKE ANY  UPDATES  '):
        #st.experimental_set_query_params(navigation="Update")

    rain(
    emoji="🌸",
    font_size=30,
    falling_speed=2,
    animation_length=1.5,
    #animation_length="infinite",
)

#st.markdown(
       #     """
        #<style>
        #.stButton>button {
        #    border-radius: 200%;
        #    background-color:pink;
        #    font-weight: 900;
        #    font-style:italic;
        #}
        #}
        
        #</style>
        #""",
        #    unsafe_allow_html=True,
        #)

def Main():
    data = pd.read_csv("house_building_expenditure.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    st.header("Calculate the amount")
    option = st.selectbox('Select an option', ('Select the date','Select date range', 'Select feature'))

    if option=="Select the date":
        date_i = st.date_input("Choose the date", datetime.date(2023, 7, 6))
        fil = data.loc[data.index == pd.to_datetime(date_i)]
        amount = fil.sum().sum()
        st.write("Total Amount:")
        st.markdown(
            f"<style>.title-text{{color:BLACK;font-family: Arial, sans-serif;}}</style>",
            unsafe_allow_html=True
        )

        st.markdown(f"<h1 class='title-text'>{amount}</h1>", unsafe_allow_html=True)


        non_zero_features = fil.columns[fil.any()]

        for feature in non_zero_features:
            values = fil[feature].values
            for value in values:
                if value != 0:
                    st.write(f"{feature}: {value}")
        
    elif option == 'Select date range':
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
            #st.write(non_zero_data)

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
        selected_feature_name = st.selectbox("Select a Feature", data.columns[data.columns != 'Date'])
        feature_data = data[selected_feature_name]
        feature_sum = feature_data.sum()

        st.write(f"Total Amount for {selected_feature_name}:")
        st.markdown(
            f"<style>.title-text{{color: BLACK;}}</style>",
            unsafe_allow_html=True
        )
        st.markdown(f"<h1 class='title-text'>{feature_sum}</h1>", unsafe_allow_html=True)
        selected_dates = data.loc[(data[selected_feature_name] != 0) & data[selected_feature_name].notnull()].index
        selected_dates = [date.strftime('%b %d') for date in selected_dates]

        st.write("Dates when the feature was brought:")
        for date in selected_dates:
            st.write(date)
        selected_cost = data.loc[(data[selected_feature_name] != 0) & data[selected_feature_name].notnull(), selected_feature_name]
        plot_data = pd.DataFrame({'Date': selected_dates, 'Cost': selected_cost})

        chart = alt.Chart(plot_data).mark_circle(color='red', opacity=1).encode(
        x=alt.X('Date:T', axis=alt.Axis(format='%b %d')),
        y='Cost:Q',
        tooltip=['Date', 'Cost']
    ).properties(
        width=600,
        height=500
)
        st.altair_chart(chart, use_container_width=True)

def update():
    st.markdown("<h1>Update Selection</h1>", unsafe_allow_html=True)
    st.write("to make changes..")
    data = pd.read_csv("house_building_expenditure.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    st.header("Add and Remove Data")
    update_option = st.radio('Update dataset?', ('Add entries', 'Remove entries'))
    st.write('You selected:', update_option)

    if update_option == 'Add entries':
        st.header("Add New Data")
        new_date = st.date_input("Choose the date", datetime.date(2023, 7, 6))
        new_date_with_time = pd.to_datetime(new_date).strftime('%Y-%m-%d %H:%M:%S')  # Convert to datetime format

        columns = list(data.columns)
        columns.append("Add New Feature")  # Add an option to add a new feature
        new_feature = st.selectbox('Select a feature', columns)

        if new_feature == "Add New Feature":
            new_feature = st.text_input("Enter the new feature")  # Prompt for the new feature name

        if new_feature != "Add New Feature":  # Proceed only if a feature is selected or a new feature name is provided
            if new_feature not in data.columns:  # Check if the selected feature already exists in the dataset
                new_cost = st.number_input("Enter the cost")

                if st.button("Add Data"):
                    data.at[new_date_with_time, new_feature] = new_cost
                    data.reset_index(inplace=True)
                    data.to_csv("/home/aardra/Downloads/house_building_expenditure.csv", index=False)
                    st.success("Data added successfully!")
                    st.write(data)
        
    elif update_option == 'Remove entries':
        st.header("Remove Data")
        remove_date = st.date_input("Choose the date to remove entries", datetime.date(2023, 7, 6), key="remove_date_input")
        new_date_with_time = pd.to_datetime(remove_date).strftime('%Y-%m-%d %H:%M:%S')  
        st.write("Current Data:")
        st.write(data)

        remove_feature = st.selectbox('Select a feature to remove', data.columns)
        if st.button("Remove Data"):
            if remove_feature in data.columns:
                data.loc[data.index == new_date_with_time, remove_feature] = None
                data = data.loc[:, data.notnull().any()]
                data = data.dropna(axis=0, how='all')  # Remove rows with all None values
                data.reset_index(inplace=True)  # Reset the index
                data.to_csv("house_building_expenditure.csv", index=False)
                st.success("Data removed successfully!")
                st.write(data)
            else:
                st.error("Invalid feature selection. Please choose a valid feature.")
            st.snow()
   
if __name__ == "__main__":
    main()
    navigation_index = get_navigation_index()

