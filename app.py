import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Set Streamlit page configuration
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# CSS styling
st.markdown("""
    <style>
    .main {
        background-color: black;
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-size: 2.5em;
        color: white;
        background-color: black;
        text-align: center;
        margin-bottom: 30px;
    }
    .subtitle {
        font-size: 1.5em;
        color: white;
        margin-bottom: 20px;
    }
    .input-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .prediction-section {
        background-color: #eaf2f8;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Define function to take user inputs
def user_input():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.header("Input House Details")
    st.write("Please provide the details of the house below:")

    # Split into columns for a better layout
    col1, col2 = st.columns(2)

    with col1:
        square_feet = st.number_input('Square Feet', min_value=100, max_value=10000, value=1000, step=10, help="Total square feet of the house")
        bedrooms = st.slider('Number of Bedrooms', 1, 10, 3, help="Total number of bedrooms in the house")
        bathrooms = st.slider('Number of Bathrooms', 1, 10, 2, help="Total number of bathrooms in the house")

    with col2:
        neighborhood = st.selectbox('Neighborhood', ['Urban', 'Suburb', 'Rural'], help="Location of the house")
        year_built = st.slider('Year Built', 1800, datetime.now().year, 2000, help="Year the house was built")

    # Encode categorical variable
    neighborhood_encoded = 0 if neighborhood == 'Urban' else (1 if neighborhood == 'Suburb' else 2)

    # Calculate the age of the house
    current_year = datetime.now().year
    age_of_the_house = current_year - year_built

    # Create a dictionary with the user inputs
    user_data = {
        'SquareFeet': square_feet,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Neighborhood': neighborhood_encoded,
        #'YearBuilt': year_built,
        'AgeOfTheHouse': age_of_the_house
    }
    
    st.markdown('</div>', unsafe_allow_html=True)
    return user_data

# Main function to run the app
def main():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="title">House Price Prediction</div>', unsafe_allow_html=True)
    st.write("""
        This application predicts the price of a house based on various characteristics. 
        Please provide the details of the house and click 'Predict' to see the estimated price.
    """)

    # Get user input
    user_data = user_input()

    # Convert user data to dataframe
    input_df = pd.DataFrame([user_data])

    # Load the model
    with open('house_price_model.pkl', 'rb') as pickle_in:
        model = pickle.load(pickle_in)
    
    # Display the user input
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.subheader('Summary of Input Details')
    st.write(input_df)
    st.markdown('</div>', unsafe_allow_html=True)

    # Make predictions with the model
    if st.button('Predict'):
        prediction = model.predict(input_df)
        st.markdown('<div class="prediction-section">', unsafe_allow_html=True)
        st.subheader('Prediction Result')
        st.markdown(f"<h3 style='color: #4CAF50;'>Estimated Price: ${prediction[0]:,.2f}</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
