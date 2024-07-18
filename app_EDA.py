# Import required libraries
import os
import streamlit as st
import pandas as pd

# Title
st.title('AI Assistant for Data Science 🤖')

# Welcoming message
st.write("Hello, 👋 I am your AI Assistant and I am here to help you with your data science projects.")

# Explanation sidebar
with st.sidebar:
    st.write('*Your Data Science Adventure Begins with a CSV File.*')
    st.caption('''**You may already know that every exciting data science journey starts with a dataset.
    That's why I'd love for you to upload a CSV file.
    Once we have your data in hand, we'll dive into understanding it and have some fun exploring it.
    Then, we'll work together to shape your business challenge into a data science framework.
    I'll introduce you to the coolest machine learning models, and we'll use them to tackle your problem. Sounds fun right?**
    ''')

    st.divider()

    st.caption("<p style='text-align:center'>made with ❤️ by Ana</p>", unsafe_allow_html=True)

# Function to read CSV file
@st.cache
def load_data(file):
    try:
        df = pd.read_csv(file, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Initialize the key in session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

# Function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True

st.button("Let's get started", on_click=clicked, args=[1])
if st.session_state.clicked[1]:
    user_csv = st.file_uploader("Upload your file here", type="csv")
    if user_csv is not None:
        user_csv.seek(0)  # Reset file pointer to start
        df = load_data(user_csv)
        if df is not None:
            # Display data overview
            st.write("**Data Overview**")
            st.write("The first rows of your dataset look like this:")
            st.write(df.head())

            # Further analysis options
            st.subheader('Variable of Study')
            user_question_variable = st.text_input('What variable are you interested in?')
            if user_question_variable:
                st.write(f"You are interested in: {user_question_variable}")

            # Additional functionalities can be added here based on user interactions

