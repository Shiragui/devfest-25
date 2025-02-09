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
logo_path = "letseat.mp4"  # Your logo filename

# Display the anime logo in Streamlit
st.video(logo_path)

# CSS for custom title styling
st.markdown(
    """
    <style>
        .custom-title {
            font-size: 600px;  /* Set the font size */
            text-align: center;  /* Center the text */
            color: #FF4500;  /* Change color to gold */
            margin-top: 20px;  /* Add some top margin */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the title with custom styling
st.markdown("<h1 class='custom-title'>Let's eat!</h1>", unsafe_allow_html=True)


# #st.title("Let's eat!")
# st.write("Welcome! Find restaurants based on your preferences.")

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
st.image(image_path, caption="Welcome! Find restaurants based on your preferences.", use_container_width=True)


# Page 1: Individual or Group Search
if st.session_state.page == 1:
    st.subheader("Are you searching alone or with a group?")
    
    search_type = st.radio(
        "Choose one:",
        ["Individual", "Group"]
    )

    if search_type == "Group":
        st.write("In the future, this will allow groups to join a shared session!")

    st.button("Next", on_click=next_page)

# Page 2: Location Selection
elif st.session_state.page == 2:
    st.subheader("Where are you?")
    location = st.text_input("Enter your location:")
    

    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Page 3: Allergies
elif st.session_state.page == 3:
    st.subheader("Select your allergies:")
    allergies = st.multiselect(
        "Choose any that apply:",
        ["Peanuts", "Shellfish", "Dairy", "Gluten", "Soy", "Tree Nuts", "Eggs", "Other"]
    )

    if "Other" in allergies:
        custom_allergy = st.text_input("Specify other allergies:")

    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Page 4: Health-related dietary preferences
elif st.session_state.page == 4:
    st.subheader("Select your health-related dietary preference:")
    health_options = st.multiselect(
        "Choose any that apply:",
        ["Low-Sodium", "Low-Carb", "Diabetic-Friendly"]
    )

    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Page 5: Religious/Dietary Preferences
elif st.session_state.page == 5:
    st.subheader("Select your religious or dietary restrictions:")
    religious_diet = st.multiselect(
        "Choose any that apply:",
        ["Halal", "Kosher", "Vegetarian", "Vegan", "Pescatarian", "Hindu-Friendly (No Beef)", "Jain-Friendly"]
    )

    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Page 6: Cuisine Preferences
elif st.session_state.page == 6:
    st.subheader("Select your cuisine preferences:")
    cuisines = st.multiselect(
        "Which cuisines do you enjoy?",
        ["Italian", "Mexican", "Chinese", "Indian", "Japanese", "Thai", "Mediterranean", "Middle Eastern",
         "Korean", "American", "French", "African", "Latin American", "Greek"]
    )

    st.button("Back", on_click=prev_page)
    st.button("Next", on_click=next_page)

# Page 7: Budget and Eating Preference
elif st.session_state.page == 7:
    st.subheader("Select your budget and eating preference:")
    
    budget = st.radio("What is your budget preference?", ["Budget", "Mid-Range", "Fancy"])
    eating_preference = st.radio("How do you prefer to eat?", ["Dine-In", "Takeout", "Delivery"])

    st.button("Back", on_click=prev_page)
    st.button("Submit", on_click=next_page)