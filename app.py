import streamlit as st

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
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: left; font-size: 80px; font-weight: bold;'>
        🍕 Let's Eat! 🍽️
    </h1>
""", unsafe_allow_html=True)

# Path to the local image
image_path = "friends.png"  # Your image filename

# CSS for full-page background image
st.markdown(
    f"""
    <style>
        body {{
            background-image: url('{image_path}');
            background-size: cover;
            background-position: center;
            background-repeat: repeat-y;
            height: 100vh;  /* Full height */
            margin: 0;  /* Remove default margin */
            color: white;  /* Optional: Change text color for better visibility */
        }}
    </style>
    """,
    unsafe_allow_html=True
)

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

    if st.button("Next"):
        if search_type == "Individual":
            st.session_state.page = 3  # Navigate to page 2
        else:
            st.session_state.page = 2  # Navigate to page 3

# Page 2: Options Selection
elif st.session_state.page == 2:
    st.subheader("Join a Room")
    room_code = st.text_input("Enter the 6-digit room code:")

    if len(room_code) != 6:
        st.warning("Please enter a valid 6-digit room code.")
        join_disabled = True
    else:
        join_disabled = False

    if st.button("Back"):
        st.session_state.page = 1  # Go back to page 1

    # Enable the "Join" button only when the room code is valid
    if st.button("Join", disabled=join_disabled):
        # Here you can handle the logic for joining the room if needed
        st.session_state.page = 3  # Navigate to page 3 after joining


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
