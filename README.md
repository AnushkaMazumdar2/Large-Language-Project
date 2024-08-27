# Library Management System with LLM Integration

## Overview

This project is a Library Management System built using Streamlit and integrates language models to provide a comprehensive platform for both admin and student users. It features visualizations for book data and allows users to search for book details using advanced language model capabilities.

## Features

- **Admin Dashboard**:
  - Visualizations of books by subject, campus, year, author, library, and sample books by ISBN.
  - Search functionality to find detailed information about books using a language model.
  
- **Student Dashboard**:
  - Allows students to enter queries to get book recommendations and suggestions using the language model.

## Technologies Used

- **Streamlit**: Framework for building interactive web applications.
- **Plotly Express**: Library for creating interactive visualizations.
- **LangChain**: For creating language model agents to interact with the CSV data.
- **Pandas**: Data manipulation and analysis library.
- **Plotly**: Graphing library for visualizations.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AnushkaMazumdar2/Large-Language-Project.git
   cd Large-Language-Project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the following files are in place**:
   - `combined_library_data.csv`: The CSV file containing the library data.

## Usage

1. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   - Open your web browser and go to `http://localhost:8501`.

3. **Log in**:
   - **Admin**: Username `admin`, Password `adminpass`
   - **Student**: Username `student`, Password `studentpass`

## Functionality

- **Admin Dashboard**:
  - **Books by Subject**: Bar chart showing the number of books per subject.
  - **Books by Campus**: Pie chart showing the distribution of books by campus.
  - **Books by Year**: Line chart showing the number of books published each year.
  - **Books by Author**: Bar chart showing the top 10 authors by book count.
  - **Books by Library**: Bar chart showing the number of books per library.
  - **Books Sample by ISBN**: Table displaying a sample of books with their ISBNs.
  - **Search for a Book**: Search for books and get detailed information using the language model.

- **Student Dashboard**:
  - **Query Input**: Enter a query to get book recommendations or suggestions based on the language model.

## File Structure

- `app.py`: The main Streamlit application file.
- `requirements.txt`: List of Python packages required for the project.
- `combined_library_data.csv`: The dataset used by the application.

## Troubleshooting

- **Search Functionality Issues**: Ensure that the CSV file is correctly loaded and the path to the file is accurate.
- **Visualization Issues**: Verify that Plotly and related dependencies are correctly installed.


**Note**: Update the repository URL and paths as necessary based on your setup and file locations.
