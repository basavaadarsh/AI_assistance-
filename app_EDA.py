# Import required libraries
import os
import streamlit as st
import pandas as pd

# Check if the API key is provided via environment variable or a file named 'apikey.txt'
if 'OPENAI_API_KEY' in os.environ:
    apikey = os.getenv('OPENAI_API_KEY')
else:
    try:
        with open('apikey.txt', 'r') as f:
            apikey = f.read().strip()
    except FileNotFoundError:
        st.error("API key not found. Please provide the API key either via environment variable or in a file named 'apikey.txt'.")
        st.stop()

# Setting up environment variable for OpenAIKey
os.environ['OPENAI_API_KEY'] = apikey

# Importing OpenAI and other necessary modules after setting API key
from langchain_community.llms import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Title and welcome message
st.title('AI Assistant for Data Science 🤖')
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
    st.caption("<p style ='text-align:center'> made with ❤️ by Ana</p>", unsafe_allow_html=True)

# Initialize the key in session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

# Function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True

# Main button to start the assistant
st.button("Let's get started", on_click=clicked, args=[1])

# Check if the button is clicked
if st.session_state.clicked[1]:
    # File uploader for CSV file
    user_csv = st.file_uploader("Upload your file here", type="csv")

    # Process the CSV file if uploaded
    if user_csv is not None:
        user_csv.seek(0)
        df = pd.read_csv(user_csv, low_memory=False)

        # Initialize OpenAI model
        llm = OpenAI(temperature=0)

        # Define functions for data analysis
        @st.cache_data
        def steps_eda():
            steps_eda = llm('What are the steps of EDA')
            return steps_eda

        # Create Pandas agent for DataFrame interaction
        pandas_agent = create_pandas_dataframe_agent(llm, df, verbose=True)

        @st.cache_data
        def function_agent():
            st.write("**Data Overview**")
            st.write("The first rows of your dataset look like this:")
            st.write(df.head())

            st.write("**Data Cleaning**")
            columns_df = pandas_agent.run("What are the meaning of the columns?")
            st.write(columns_df)

            missing_values = pandas_agent.run("How many missing values does this dataframe have? Start the answer with 'There are'")
            st.write(missing_values)

            duplicates = pandas_agent.run("Are there any duplicate values and if so where?")
            st.write(duplicates)

            st.write("**Data Summarisation**")
            st.write(df.describe())

            correlation_analysis = pandas_agent.run("Calculate correlations between numerical variables to identify potential relationships.")
            st.write(correlation_analysis)

            outliers = pandas_agent.run("Identify outliers in the data that may be erroneous or that may have a significant impact on the analysis.")
            st.write(outliers)

            new_features = pandas_agent.run("What new features would be interesting to create?.")
            st.write(new_features)

        @st.cache_data
        def function_question_variable():
            user_question_variable = st.text_input('What variable are you interested in')
            if user_question_variable is not None and user_question_variable != "":
                st.line_chart(df[user_question_variable])

                summary_statistics = pandas_agent.run(f"Give me a summary of the statistics of {user_question_variable}")
                st.write(summary_statistics)

                normality = pandas_agent.run(f"Check for normality or specific distribution shapes of {user_question_variable}")
                st.write(normality)

                outliers = pandas_agent.run(f"Assess the presence of outliers of {user_question_variable}")
                st.write(outliers)

                trends = pandas_agent.run(f"Analyse trends, seasonality, and cyclic patterns of {user_question_variable}")
                st.write(trends)

                missing_values = pandas_agent.run(f"Determine the extent of missing values of {user_question_variable}")
                st.write(missing_values)

        @st.cache_data
        def function_question_dataframe():
            user_question_dataframe = st.text_input("Is there anything else you would like to know about your dataframe?")
            if user_question_dataframe is not None and user_question_dataframe not in ("", "no", "No"):
                dataframe_info = pandas_agent.run(user_question_dataframe)
                st.write(dataframe_info)

        # Main content display
        st.header('Exploratory data analysis')
        st.subheader('General information about the dataset')

        with st.sidebar:
            with st.expander('What are the steps of EDA'):
                st.write(steps_eda())

        function_agent()

        st.subheader('Variable of study')
        function_question_variable()

        st.subheader('Further study')
        function_question_dataframe()
