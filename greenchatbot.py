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
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

# Ensure necessary NLTK data files are available
required_nltk_resources = ['punkt', 'wordnet', 'omw-1.4', 'stopwords']
for resource in required_nltk_resources:
    try:
        nltk.data.find(f"tokenizers/{resource}" if resource == "punkt" else resource)
    except LookupError:
        nltk.download(resource, download_dir=nltk_data_path)

# Load intents from the JSON file (Make sure the Intent.json is in the same directory or adjust path)
file_path = os.path.join(os.getcwd(), "Intent.json")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Intent.json file not found at {file_path}")

with open(file_path, "r") as file:
    intents = json.load(file)

# Initialize lemmatizer for preprocessing
lemmatizer = WordNetLemmatizer()

# Preprocess text by tokenizing and lemmatizing
def preprocess_text(text):
    words = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(word) for word in words if word.isalnum()]

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
    }

    .biofeast-header {
        text-align: center;
        background-color: #A9BFA8;
        padding: 20px;
        color: Olivegreen;
        font-size: 2.5em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Main function for Streamlit app
def main():
    add_custom_css()  # Apply custom CSS for the sustainable theme

    # Display BIOFEAST Header
    st.markdown("""
    <div class="biofeast-header">
        BIOFEAST Chatbot
    </div>
    """, unsafe_allow_html=True)

    # Create a sidebar menu with options
    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    chat_log_path = os.path.join(os.getcwd(), "chat_log.csv")

    # Home Menu
    if choice == "Home":
        st.write("Welcome to the Sustainable Food Practices Chatbot. Type a message to start!")

        # Ensure chat log file exists
        if not os.path.exists(chat_log_path):
            with open(chat_log_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response'])

        # User input
        user_input = st.text_input("You:")

        if user_input:
            # Get chatbot response
            response = chatbot(user_input)
            st.markdown(f"**Chatbot:** {response}")

            # Save to chat log
            with open(chat_log_path, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input, response])

    # Conversation History Menu
    elif choice == "Conversation History":
        st.header("Conversation History")
        if os.path.exists(chat_log_path):
            with open(chat_log_path, 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader, None)  # Skip the header row
                for row in csv_reader:
                    st.markdown(f"**User:** {row[0]}  \n**Chatbot:** {row[1]}  \n---")

    # About Menu
    elif choice == "About":
        st.write("This chatbot promotes sustainable food practices.")
        st.write("It helps users make informed decisions about food choices and reducing waste.")

if __name__ == '__main__':
    main()
