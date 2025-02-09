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
    st.session_state.page += 1

# Function to go back
def prev_page():
    st.session_state.page -= 1

# Path to the anime logo
logo_path = "lets.png"  # Your logo filename

# st.markdown(
#     f"""
#     <h1 style='font-size: 120px; color: #FF4500; font-family: Arial, sans-serif; text-align: center; margin-top: 20px; margin-bottom: 10px; padding: 5px; background-color: rgba(255, 255, 255, 0.8);'>
#         <img src="{logo_path}" width="150" style='vertical-align: middle; margin-right: 10px;' />
#         Let's eat!
#     </h1>
#     """,
#     unsafe_allow_html=True
# )

st.markdown("""
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: left; font-size: 150px; font-weight: bold;margin-bottom: 1px;'>
        🍕 Let's              Eat! 🍽️
    </h1>
""", unsafe_allow_html=True)

# Path to the local image
image_path = "friends.png"  # Your image filename
# st.image(image_path, use_container_width=True)

# CSS for full-page background image
# st.markdown(
#     f"""
#     <style>
#         body {{
#             background-image: url('{image_path}');
#             background-size: cover;
#             background-position: center;
#             background-repeat: repeat-y;
#             height: 120vh;  /* Full height */
#             margin: 0;  /* Remove default margin */
#             color: white;  /* Optional: Change text color for better visibility */
#         }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Display the image caption (optional, can be removed if not needed)
st.image(image_path, use_container_width=True)
st.markdown("""
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: center;font-size: 24px;'>
        Welcome! Find restaurants based on your preferences.
    </h1>
""", unsafe_allow_html=True)
# Assuming you have a session state to track the current page
# Assuming you have a session state to track the current page
if 'page' not in st.session_state:
    st.session_state.page = 1  # Initialize the page if not already set

# Page 1: Individual or Group Search
if st.session_state.page == 1:
    st.subheader("Are you searching alone or with a group?")
    
    search_type = st.radio(
        "Choose one:",
        ["Individual", "Group"]
    )

    def next():
        if search_type == "Individual":
            st.session_state.page = 3  # Navigate to page 2
        else:
            st.session_state.page = 2  # Navigate to page 3

    st.button("Next", on_click=next)
        

# Page 2: Options Selection
elif st.session_state.page == 2:
    st.subheader("Group")
    room = st.multiselect(
        "Choose one:",
        ["Join a Room", "Host a Room"]
    )

    join_disabled = True

    if len(room) > 0 and room[0] == "Join a Room":
        st.subheader("Join a Room")
        room_code = st.text_input("Enter the 6-digit room code:")
        if len(room_code) != 6:
            st.warning("Please enter a valid 6-digit room code.")
        # next_page()
        joined_code = run_client("join", room_code)
        if joined_code:
            st.session_state["room_code"] = joined_code  # Store room info
            join_disabled = False
        else:
            st.warning("Invalid room code. Try again.")
    
    if len(room) > 0 and room[0] == "Host a Room":
        st.subheader("Host a Room")
        room_code = run_client("create")  # Get a new room code from server
        if room_code:
            st.write(f"Your new room code is: {room_code}")
            st.write("Share this code with your friends to join the room.")
            st.session_state["room_code"] = room_code  # Store for reference
            join_disabled = False

    def back():
        st.session_state.page = 1  # Go back to page 1

    def join():
        st.session_state.page = 3  # Navigate to page 3 after joining

    st.button("Back", on_click=back)
        
    # Enable the "Join" button only when the room code is valid
    st.button("Join", disabled=join_disabled, on_click=join)
        # Here you can handle the logic for joining the room if needed
        


# Page 3: Remaining Options for Group Search
elif st.session_state.page == 3:
    # st.markdown("<h1 style='font-size: 120px; color: #FF4500; font-family: Arial, sans-serif; text-align: center;'>Group Search Options</h1>", unsafe_allow_html=True)

    st.subheader("Where are you?")
    location = st.text_input("Enter your location:")

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

    st.subheader("Select your dietary restrictions:")
    religious_diet = st.multiselect(
        "Choose any that apply:",
        ["Halal", "Kosher", "Vegetarian", "Vegan", "Pescatarian", "Gluten-Free"]
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

    def back():
        st.session_state.page = 1  # Go back to page 1

    # Navigation buttons
    st.button("Back", on_click=back)
        
    st.button("Submit", on_clock=next_page)
