import streamlit as st
from flask import Flask, render_template_string

app = Flask(__name__)

# Color Palette
color_palette = {
    'background': '#f0f8ff',
    'table': '#ffebcd',
    'friends': ['#ff6347', '#4682b4', '#32cd32', '#ffd700'],
}

@app.route('/friends_meeting')
def friends_meeting():
    return '''
    <html>
    <head>
        <style>
            body {
                background-color: {background};
            }
            .table {
                background-color: {table};
                width: 400px;
                height: 200px;
                position: relative;
                margin: auto;
                border-radius: 10px;
            }
            .friend {
                width: 50px;
                height: 50px;
                border-radius: 50%;
                position: absolute;
                animation: move 2s infinite;
            }
            @keyframes move {
                0% { transform: translate(0, 0); }
                50% { transform: translate(100px, 0); }
                100% { transform: translate(0, 0); }
            }
        </style>
    </head>
    <body>
        <div class='table'>
            <div class='friend' style='background-color: {friends[0]}; top: 20px; left: 20px;'></div>
            <div class='friend' style='background-color: {friends[1]}; top: 20px; right: 20px;'></div>
            <div class='friend' style='background-color: {friends[2]}; bottom: 20px; left: 20px;'></div>
            <div class='friend' style='background-color: {friends[3]}; bottom: 20px; right: 20px;'></div>
        </div>
    </body>
    </html>
    '''.format(**color_palette)

# Title and introductory text
st.title("Food Finder")
st.write("Welcome! Find restaurants based on your preferences.")

# Input for location
location = st.text_input("Enter your location:")
if location:
    st.write(f"Searching for restaurants near {location}...")

    # Once the location is entered, show the survey
    st.header("Food Preferences Survey")

    # Allergies/Dietary Restrictions
    allergies = st.multiselect(
        "Select your allergies or dietary restrictions:",
        ["Peanuts", "Shellfish", "Dairy", "Gluten", "Soy", "Tree Nuts", "Eggs", "Other (Specify)"]
    )
    custom_allergy = ""
    if "Other (Specify)" in allergies:
        custom_allergy = st.text_input("Please specify your custom allergy:")

    # Health Options
    health_options = st.radio(
        "Select your health-related dietary preference:",
        ["Low-sodium", "Low-carb", "Diabetic-friendly", "None"]
    )

    # Religious/Dietary Preferences
    religious_preferences = st.multiselect(
        "Select your religious/dietary preferences:",
        ["Halal", "Kosher", "Vegetarian", "Vegan", "Pescatarian", "Hindu-friendly (No beef)", "Jain-friendly (Strict Vegetarian)"]
    )

    # Cuisine Preferences
    cuisine_preferences = st.multiselect(
        "Select your preferred cuisines:",
        ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "Thai", "Mediterranean", "Middle Eastern", 
         "Korean", "American", "French", "African", "Latin American", "Greek"]
    )
    not_preferred_cuisine = st.multiselect(
        "Select cuisines you don't prefer:",
        ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "Thai", "Mediterranean", "Middle Eastern", 
         "Korean", "American", "French", "African", "Latin American", "Greek"]
    )

    # Budget/Eating Preferences
    budget = st.radio(
        "Select your budget preference:",
        ["Low", "Mid-range", "Fancy"]
    )
    eating_preference = st.radio(
        "Select your eating preference:",
        ["Dine-in", "Takeout", "Delivery"]
    )
