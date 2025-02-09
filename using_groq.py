import os
from groq import Groq

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def get_recommendations(user_prefs):

    query = f"""
    I am looking for restaurants in {user_prefs['location']} that match these preferences:
    - Allergies: {', '.join(user_prefs.get('allergies', ['None']))}
    - Health Options: {', '.join(user_prefs.get('health_options', ['None']))}
    - Religious Preferences: {', '.join(user_prefs.get('religious_diet', ['None']))}
    - Preferred Cuisines: {', '.join(user_prefs.get('cuisines', ['Any']))}
    - Budget: {user_prefs.get('budget', 'Any')}
    - Eating Preference: {user_prefs.get('eating_preference', 'Any')}

    Suggest some restaurants in the correct location preferred by user which is within 40 miles given with:
    - **Restaurant Name**
    - **Address**
    - **Google Maps Link** (Format: `https://www.google.com/maps/search/Restaurant+Name+Address`
    - The location of the restaurant is important to keep in mind and should be aligned with the location mentioned in the prompt.)
    - A short reason why they match the preferences.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": query}],
    )

    return response.choices[0].message.content


# import streamlit as st
# from pymongo import MongoClient
# import datetime
# from datetime import datetime, timezone
# from using_groq import get_recommendations

# # MongoDB Connection
# client = MongoClient("mongodb+srv://annanya:lettuceDecide@cluster0.lrcdj.mongodb.net/?ssl=true&tlsAllowInvalidCertificates=true")
# db = client["food_finder"]
# preferences_collection = db["user_preferences"]

# # Initialize session state for page tracking and preferences
# if "page" not in st.session_state:
#     st.session_state.page = 1
# if "preferences" not in st.session_state:
#     st.session_state.preferences = {}  # ✅ Fix: Initialize preferences as an empty dictionary

# # Function to move to the next page
# def next_page():
#     st.session_state.page += 1

# # Function to go back
# def prev_page():
#     st.session_state.page -= 1

# st.title("Let's eat!")
# st.write("Welcome! Find restaurants based on your preferences.")

# # Page 1: Individual or Group Search
# if st.session_state.page == 1:
#     st.subheader("Are you searching alone or with a group?")
    
#     search_type = st.radio("Choose one:", ["Individual", "Group"])
#     st.session_state.preferences["search_type"] = search_type
    
#     if search_type == "Group":
#         st.write("In the future, this will allow groups to join a shared session!")

#     st.button("Next", on_click=next_page, key="next_1")

# # Page 2: Location Selection
# elif st.session_state.page == 2:
#     st.subheader("Where are you?")
#     location = st.text_input("Enter your location:", st.session_state.preferences.get("location", ""))
#     st.session_state.preferences["location"] = location

#     st.button("Back", on_click=prev_page, key="back_2")
#     st.button("Next", on_click=next_page, key="next_2")

# # Page 3: Allergies
# elif st.session_state.page == 3:
#     st.subheader("Select your allergies:")
#     allergies = st.multiselect(
#         "Choose any that apply:",
#         ["Peanuts", "Shellfish", "Dairy", "Gluten", "Soy", "Tree Nuts", "Eggs", "Other"],
#         default=st.session_state.preferences.get("allergies", [])
#     )
#     st.session_state.preferences["allergies"] = allergies
    
#     if "Other" in allergies:
#         custom_allergy = st.text_input("Specify other allergies:", st.session_state.preferences.get("custom_allergy", ""))
#         st.session_state.preferences["custom_allergy"] = custom_allergy

#     st.button("Back", on_click=prev_page, key="back_3")
#     st.button("Next", on_click=next_page, key="next_3")

# # Page 4: Health-related dietary preferences
# elif st.session_state.page == 4:
#     st.subheader("Select your health-related dietary preference:")
#     health_options = st.multiselect("Choose any that apply:",
#         ["Low-Sodium", "Low-Carb", "Diabetic-Friendly"],
#         default=st.session_state.preferences.get("health_options", [])
#     )
#     st.session_state.preferences["health_options"] = health_options

#     st.button("Back", on_click=prev_page, key="back_4")
#     st.button("Next", on_click=next_page, key="next_4")

# # Page 5: Religious/Dietary Preferences
# elif st.session_state.page == 5:
#     st.subheader("Select your religious or dietary restrictions:")
#     religious_diet = st.multiselect("Choose any that apply:",
#         ["Halal", "Kosher", "Vegetarian", "Vegan", "Pescatarian", "Hindu-Friendly (No Beef)", "Jain-Friendly"],
#         default=st.session_state.preferences.get("religious_diet", [])
#     )
#     st.session_state.preferences["religious_diet"] = religious_diet

#     st.button("Back", on_click=prev_page, key="back_5")
#     st.button("Next", on_click=next_page, key="next_5")

# # Page 6: Cuisine Preferences
# elif st.session_state.page == 6:
#     st.subheader("Select your cuisine preferences:")
#     cuisines = st.multiselect("Which cuisines do you enjoy?",
#         ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "Thai", "Mediterranean", "Middle Eastern",
#          "Korean", "American", "French", "African", "Latin American", "Greek"],
#         default=st.session_state.preferences.get("cuisines", [])
#     )
#     st.session_state.preferences["cuisines"] = cuisines

#     st.button("Back", on_click=prev_page, key="back_6")
#     st.button("Next", on_click=next_page, key="next_6")

# # Page 7: Budget and Eating Preference
# elif st.session_state.page == 7:
#     st.subheader("Select your budget and eating preference:")
    
#     budget = st.radio("What is your budget preference?", ["Budget", "Mid-Range", "Fancy"], 
#                     index=["Budget", "Mid-Range", "Fancy"].index(st.session_state.preferences.get("budget", "Budget")))
#     eating_preference = st.radio("How do you prefer to eat?", ["Dine-In", "Takeout", "Delivery"],
#                                  index=["Dine-In", "Takeout", "Delivery"].index(st.session_state.preferences.get("eating_preference", "Dine-In"))
#                                 )
    
#     st.session_state.preferences["budget"] = budget
#     st.session_state.preferences["eating_preference"] = eating_preference

# def save_preferences():
#     preferences_data = st.session_state.preferences.copy()
#     preferences_data["timestamp"] = datetime.now(timezone.utc)

#     preferences_collection.insert_one(preferences_data)
#     st.success("Your preferences have been saved!")

#     recommendations = get_recommendations(preferences_data)
#     st.write("### Recommended Restaurants:")
#     st.write(recommendations)

# st.button("Submit", on_click=save_preferences, key="submit_preferences")


#Ann#lettucedecide