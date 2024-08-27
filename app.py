import pandas as pd
import streamlit as st
import plotly.express as px
from langchain_experimental.agents import create_csv_agent
from langchain_groq import ChatGroq
from fuzzywuzzy import process

# Initialize the agent
@st.cache_resource
def initialize_agent():
    st.write("Initializing agent...")
    return create_csv_agent(
        ChatGroq(model="llama3-70b-8192", temperature=0),
        "C:/Users/Anushka/OneDrive/Desktop/LLM Project/combined_library_data.csv",
        verbose=True,
        allow_dangerous_code=True,
        handle_parsing_errors=True
    )

# Load data from CSV
@st.cache_data
def load_data():
    st.write("Loading data...")
    return pd.read_csv("C:/Users/Anushka/OneDrive/Desktop/LLM Project/combined_library_data.csv")

# Function to display books by subject
def books_by_subject(df):
    st.subheader("Books by Subject")
    subject_counts = df['Subject'].value_counts()
    fig = px.bar(subject_counts, 
                 x=subject_counts.index, 
                 y=subject_counts.values, 
                 labels={'x':'Subject', 'y':'Book Count'},
                 title="Number of Books by Subject")
    st.plotly_chart(fig)

# Function to display books by campus
def books_by_campus(df):
    st.subheader("Books by Campus")
    campus_counts = df['Library'].value_counts()
    fig = px.pie(campus_counts, 
                 names=campus_counts.index, 
                 values=campus_counts.values,
                 title="Books Distribution by Campus")
    st.plotly_chart(fig)

# Function to display books by year
def books_by_year(df):
    st.subheader("Books by Year")
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    year_counts = df['Year'].value_counts().sort_index()
    fig = px.line(year_counts, 
                  x=year_counts.index, 
                  y=year_counts.values,
                  labels={'x':'Year', 'y':'Book Count'},
                  title="Number of Books by Year")
    st.plotly_chart(fig)

# Function to display books by author
def books_by_author(df):
    st.subheader("Books by Author")
    author_counts = df['Author'].value_counts()
    fig = px.bar(author_counts.head(10), 
                 x=author_counts.head(10).index, 
                 y=author_counts.head(10).values, 
                 labels={'x':'Author', 'y':'Book Count'},
                 title="Top 10 Authors by Book Count")
    st.plotly_chart(fig)

# Function to display books by library
def books_by_library(df):
    st.subheader("Books by Library")
    library_counts = df['Library'].value_counts()
    fig = px.bar(library_counts, 
                 x=library_counts.index, 
                 y=library_counts.values,
                 labels={'x':'Library', 'y':'Book Count'},
                 title="Books by Library")
    st.plotly_chart(fig)

# Function to display sample books by ISBN
def books_by_isbn(df):
    st.subheader("Sample Books by ISBN")
    sample_isbns = df['ISBN'].dropna().unique()[:10]  # Show sample of 10 ISBNs
    sample_books = df[df['ISBN'].isin(sample_isbns)]
    st.write("Sample Books by ISBN:")
    st.dataframe(sample_books)

# Function to search for a book and display its details
def search_book(agent, df):
    st.subheader("Search for a Book")
    search_title = st.text_input("Enter the book title:")
    
    if st.button("Search Book"):
        if search_title:
            # Perform fuzzy matching to find the closest title
            titles = df['Title'].tolist()
            match, score = process.extractOne(search_title, titles)
            
            if score > 80:  # Adjust threshold as needed
                query = f"Find details for the book titled '{match}' from this dataset."
                try:
                    # Use the agent to run the query
                    response = agent.run(query)
                    
                    # Debug: Show raw response
                    st.write("Raw response:", response)
                    
                    # Attempt to parse and display the response
                    if "No book found" in response:
                        st.write("No book details available for the title.")
                    else:
                        st.write("### Book Details:")
                        st.write(response)
                
                except Exception as e:
                    st.write("Error in agent response:", e)
            else:
                st.write(f"No close match found for '{search_title}'.")
        else:
            st.write("Please enter a book title to search.")

# Function to display books (Student View)
def display_books(response):
    try:
        df = pd.read_csv(pd.compat.StringIO(response))
        st.write("### Suggested Books:")
        st.dataframe(df)
    except Exception:
        st.write("### Suggested Books:")
        st.write(response)

# Student dashboard
def student_dashboard(agent):
    st.title("Student Dashboard")
    
    query = st.text_input("Enter your query (e.g., 'Suggest some statistics books'):")
    
    if st.button("Run Query"):
        if query:
            response = agent.run(query)
            display_books(response)
        else:
            st.write("Please enter a query to get recommendations.")

# Admin dashboard with separate search functionality
def admin_dashboard(df, agent):
    st.title("Admin Dashboard")
    
    # Define the navigation options
    options = [
        "Select an Option",
        "Books by Subject",
        "Books by Campus",
        "Books by Year",
        "Books by Author",
        "Books by Library",
        "Books Sample by ISBN"
    ]
    selected_option = st.sidebar.selectbox("Navigate to:", options, index=options.index(st.session_state.get('admin_page', "Select an Option")))
    st.session_state.admin_page = selected_option
    
    # Render the appropriate page based on selection
    if st.session_state.admin_page == "Books by Subject":
        books_by_subject(df)
    elif st.session_state.admin_page == "Books by Campus":
        books_by_campus(df)
    elif st.session_state.admin_page == "Books by Year":
        books_by_year(df)
    elif st.session_state.admin_page == "Books by Author":
        books_by_author(df)
    elif st.session_state.admin_page == "Books by Library":
        books_by_library(df)
    elif st.session_state.admin_page == "Books Sample by ISBN":
        books_by_isbn(df)
    
    # Search for a book (separate button)
    st.subheader("Search for a Book")
    search_book(agent, df)

# Main function for the Streamlit app
def main():
    st.sidebar.title("Login")

    # User management setup
    users = {
        "admin": {"password": "adminpass", "role": "admin"},
        "student": {"password": "studentpass", "role": "student"}
    }

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    # Session state for login
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = "Select an Option"
    
    if login_button:
        if username in users and users[username]["password"] == password:
            st.session_state.role = users[username]["role"]
            st.sidebar.success(f"Logged in as {st.session_state.role.capitalize()}")
        else:
            st.sidebar.error("Invalid username or password")
    
    # Render the appropriate dashboard based on role
    if st.session_state.role:
        if st.session_state.role == "admin":
            df = load_data()
            agent = initialize_agent()
            admin_dashboard(df, agent)
        elif st.session_state.role == "student":
            agent = initialize_agent()
            student_dashboard(agent)

    # Debugging: Show current session state
    st.write("Session State:", st.session_state)

if __name__ == "__main__":
    main()
