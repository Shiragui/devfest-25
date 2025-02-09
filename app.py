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

st.markdown("""
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: left; font-size: 100px; font-weight: bold;margin-bottom: 1px;'>
        🍽️ Dine-o- &nbsp&nbsp Mite! 🍕🌮🍣
    </h1>
""", unsafe_allow_html=True)

# Path to the local image
image_path = "friends.png"  # Your image filename


# Display the image caption (optional, can be removed if not needed)
st.image(image_path, use_container_width=True)
st.markdown("""
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: center;font-size: 24px;'>
        Where your cravings meet their perfect match.
    </h1>
""", unsafe_allow_html=True)

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

    st.subheader("Location, Location, Location?")
    location = st.text_input("📍Where are you now? No stalking, promise.")

    st.subheader("Allergies? 🩺")
    allergies = st.multiselect(
        "Pick your edible enemies:",
        ["🤢 Peanuts", "🍖 Shellfish", "🥛 Dairy", "🌾 Gluten", "🫘 Soy", "🌰 Tree Nuts", "🥚 Eggs", "❓ Other (Mystery allergies)"]
    )

    st.subheader("Health-Related Dietary Preference:")
    health_options = st.multiselect(
        "Choose your wellness vibe:",
        ["🧂 Low-Sodium (aka the flavor monk)", "🥗 Low-Carb (Team Zoodles)", "🍬 Diabetic-Friendly (Sugar, who?)"]
    )

    st.subheader("Dietary Restrictions:")
    religious_diet = st.multiselect(
        "What's your food philosophy?",
        ["🕌 Halal", "✡️  Kosher", "🌱 Vegetarian", "🥦 Vegan", "🐟 Pescatarian", "🚫 Gluten-Free"]
    )

    st.subheader("Cuisine Cravings:")
    cuisines = st.multiselect(
        "Spin the globe of gastronomy:",
        ["🍝 Italian", "🍔 Mexican", "🍣 Chinese", "🍕 Indian", "🍱 Japanese", "🍙 Thai", "🥗 Mediterranean", "🥘 Middle Eastern",
         "🍖 Korean", "🍔 American", "🍣 French", "🍚 African", "🍕 Latin American", "🍒 Greek"]
    )   

    st.subheader("Money Matters & Eating Style:")
    budget = st.radio("💸 What’s your vibe?", ["💰 Budget (Ballin’ on a budget)", "💵 Mid-Range (Treat yourself responsibly)", "💎 Fancy (Caviar dreams and truffle wishes)"])
    eating_preference = st.radio("🍽️ How would you like to feast?", ["🍴 Dine-In (For the ambiance)", "🥡 Takeout (Sweats mandatory)", "🚚 Delivery (Pajamas forever)"])

    def back():
        st.session_state.page = 1  # Go back to page 1

    # Navigation buttons
    st.button("🔙 Back", on_click=back)
        
    st.button("✅ Submit (aka “Feed Me Now!”)", on_click=next_page)