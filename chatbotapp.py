import os
import json
import random
import nltk
import ssl
import streamlit as st
import csv
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# SSL fix for nltk
ssl._create_default_https_context = ssl._create_unverified_context

# Set NLTK data path explicitly to avoid lookup errors
nltk_data_path = os.path.abspath("nltk_data")
nltk.data.path.append(nltk_data_path)

# Function to ensure NLTK data is downloaded
def ensure_nltk_data():
    nltk_dependencies = [
        ('tokenizers/punkt', 'punkt'),
        ('corpora/wordnet', 'wordnet'),
        ('corpora/omw-1.4', 'omw-1.4'),
        ('corpora/stopwords', 'stopwords')
    ]

    for resource, name in nltk_dependencies:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(name, download_dir=nltk_data_path)

# Ensure all necessary NLTK data is available
ensure_nltk_data()

# Load intents from the JSON file (Make sure the Intent.json is in the same directory or adjust path)
file_path = os.path.abspath("Intent.json")    
with open(file_path, "r") as file:
    intents = json.load(file)

# Initialize lemmatizer for preprocessing
lemmatizer = WordNetLemmatizer()

# Preprocess text by lemmatizing
def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in words]

# Function to get chatbot response
def chatbot(input_text):
    input_words = preprocess_text(input_text)
    best_match = None
    max_overlap = 0

    # Check for the best matching intent based on overlapping words
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_words = preprocess_text(pattern)
            overlap = len(set(input_words) & set(pattern_words))
            if overlap > max_overlap:
                best_match = intent
                max_overlap = overlap

    if best_match:
        return random.choice(best_match["responses"])

    return "I'm still learning, please rephrase your question."

# Adding custom HTML and CSS for the sustainable food practices theme
def add_custom_css():
    st.markdown("""
    <style>
    body {
        background-color: #E4F1DC;
        font-family: 'Arial', sans-serif;
        color: #3A6A40;
        line-height: 1.6;
    }

    h1, h2 {
        color: #2A7B35;
    }

    .stButton>button {
        background-color: #A3C36B;
        color: white;
        border-radius: 8px;
        border: 2px solid #A3C36B;
        padding: 10px 20px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #7C9F47;
        border-color: #7C9F47;
    }

    .stTextArea {
        background-color: #FFFFFF;
        border-radius: 8px;
        border: 1px solid #A3C36B;
    }

    .stTextInput>div>input {
        background-color: #F1F9E7;
        color: #3A6A40;
        border: 1px solid #A3C36B;
        border-radius: 8px;
        padding: 8px 12px;
    }

    .stTextInput>div>input:focus {
        outline-color: #7C9F47;
    }

    .stMarkdown {
        margin-top: 20px;
    }

    .history-item {
        background-color: #F9F9F9;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid #A3C36B;
    }

    .history-item-user {
        background-color: #86A788;
    }

    .history-item-chatbot {
        background-color: #638C6D;
        color: white;
    }

    .biofeast-header {
        text-align: center;
        background-color: #A9BFA8;
        padding: 20px;
        color: Olivegreen;
        font-size: 2.5em;
        font-weight: bold;
    }

    /* Sidebar Menu Customization */
    .sidebar .sidebar-content {
        background-color: #D39D55;  /* Brown Soil color */
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize global counter variable
counter = 0  # Initialize before usage

# Main function
def main():
    global counter  # Declare that we're using the global counter variable
    add_custom_css()  # Apply custom CSS for the sustainable theme

    # Display BIOFEAST Header without logo
    st.markdown("""
    <div class="biofeast-header">
        BIOFEAST Chatbot
    </div>
    """, unsafe_allow_html=True)

    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Home Menu
    if choice == "Home":
        st.write("Welcome to the Sustainable Food Practices Chatbot. Please type a message and press Enter to start the conversation.")

        # Check if the chat_log.csv file exists, and if not, create it with column names
        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response'])

        # Increment the counter
        counter += 1  # This now works because `counter` is initialized globally
