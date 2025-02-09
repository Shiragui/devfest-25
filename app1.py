import streamlit as st

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
