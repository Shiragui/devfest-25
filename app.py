import streamlit as st
from server import start_server 
from client import run_client
import threading


def run_server():
    start_server()

@st.cache_resource
def load_server():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

load_server()

# Initialize session state for page tracking
if "page" not in st.session_state:
    st.session_state.page = 1

# Function to move to the next page
def next_page():
    page = st.session_state.page
    st.session_state.page = page_map[page][1]

# Function to go back
def prev_page():
    st.session_state.page -= 1

st.title("Let's eat!")
st.write("Welcome! Find restaurants based on your preferences.")

# Page 1: Individual or Group Search
if st.session_state.page == 1:
    st.subheader("Are you searching alone or with a group?")
    
    search_type = st.radio(
        "Choose one:",
        ["Individual", "Group"]
    )

    if search_type == "Group":
        st.write("Choose an option:")
        if st.button("Join a Room"):
            st.session_state.page = 2  # Move to page 2 where users can join a room
        elif st.button("Host a Room"):
            st.session_state.page = 3  # Move to page 3 to host a room

    st.button("Next", on_click=next_page)

# Page 2: Options Selection
elif st.session_state.page == 2:
    st.subheader("Join a Room")
    room_code = st.text_input("Enter the 6-digit room code:")

    if st.button("Join"):
        joined_code = run_client("join", room_code)
        if joined_code:
            st.session_state["room_code"] = joined_code  # Store room info
        else:
            st.warning("Invalid room code. Try again.")
    
    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Page 3: Host Room (Generate new room code)
elif st.session_state.page == 3:
    st.subheader("Host a Room")
    room_code = run_client("create")  # Get a new room code from server
    if room_code:
        st.write(f"Your new room code is: {room_code}")
        st.write("Share this code with your friends to join the room.")
        st.session_state["room_code"] = room_code  # Store for reference
    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Continue with the other pages as they are

# Page 4: Location Selection
elif st.session_state.page == 4:
    st.subheader("Where are you searching?")
    location = st.text_input("Enter a location:")

    if not location:
        st.warning("Please enter a location!")
        next_disabled = True
    else:
        next_disabled = False

    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page, disabled=next_disabled)

# Page 5: Allergies
elif st.session_state.page == 5:
    st.subheader("Select your allergies:")
    allergies = st.multiselect(
        "Choose any that apply:",
        ["Peanuts", "Shellfish", "Dairy", "Gluten", "Soy", "Tree Nuts", "Eggs", "Other"]
    )

    st.subheader("Select your health-related dietary preference:")
    health_options = st.multiselect(
        "Choose any that apply:",
        ["Low-Sodium", "Low-Carb", "Diabetic-Friendly"]
    )

    st.subheader("Select your religious or dietary restrictions:")
    religious_diet = st.multiselect(
        "Choose any that apply:",
        ["Halal", "Kosher", "Vegetarian", "Vegan", "Pescatarian", "Hindu-Friendly (No Beef)", "Jain-Friendly"]
    )

    st.subheader("Select your cuisine preferences:")
    cuisines = st.multiselect(
        "Which cuisines do you enjoy?",
        ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "Thai", "Mediterranean", "Middle Eastern",
         "Korean", "American", "French", "African", "Latin American", "Greek"]
    )

    st.subheader("Select your budget and eating preference:")
    budget = st.radio("What is your budget preference?", ["Budget", "Mid-Range", "Fancy"])
    eating_preference = st.radio("How do you prefer to eat?", ["Dine-In", "Takeout", "Delivery"])

    # Navigation buttons
    if st.button("Back"):
        st.session_state.page = 1  # Go back to page 1
    if st.button("Submit"):
        next_page()  # Call the function to go to the next page