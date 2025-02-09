import streamlit as st
from server import start_server, get_names, concat_restaraunts, get_restaraunts, voting_complete, preferences_complete, picked_preferences, vote, get_winning_vote
from client import run_client
import threading
import datetime
from datetime import datetime, timezone
from using_groq import get_recommendations
from streamlit_autorefresh import st_autorefresh
from pymongo import MongoClient

client = MongoClient("mongodb+srv://annanya:lettuceDecide@cluster0.lrcdj.mongodb.net/?ssl=true&tlsAllowInvalidCertificates=true")
db = client["food_finder"]
preferences_collection = db["user_preferences"]

st.set_page_config(page_title="Lettuce Decide!", layout="wide")

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

if "preferences" not in st.session_state:
    st.session_state.preferences = {}

if 'curr_room' not in st.session_state:
    st.session_state['curr_room'] = ""


@st.fragment
def display_names():
    if st.session_state['curr_room']:
        names = get_names(st.session_state['curr_room'])
        num_people = len(names)

        if names:
            for i, col in enumerate(st.columns(num_people)):
                with col:
                    st.write(names[i])

    st_autorefresh(interval=3000, key="refresh_names")


# Function to move to the next page
def next_page():
    st.session_state.page += 1

# Function to go back
def prev_page():
    st.session_state.page -= 1

# Path to the anime logo
logo_path = "lets.png"  # Your logo filename
# st.markdown("""
#     <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: left; font-size: 100px; font-weight: bold;margin-bottom: 1px;'>
#         🍽️ Dine-o- &nbsp&nbsp Mite! 🍕🌮🍣
#     </h1>
# """, unsafe_allow_html=True)
st.markdown("""
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align: left; font-size: 110px; font-weight: bold;margin-bottom: 1px;'>
        &nbsp🍽️ Lettuce Decide! 🍕🌮
    </h1>
""", unsafe_allow_html=True)
st.markdown("""
    <h1 style='color: #FF4500; font-family: "Comic Sans MS", cursive, sans-serif; text-align:; font-size: 24px;'>
            &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Where your cravings meet their perfect match.
    </h1>
""", unsafe_allow_html=True)

# Path to the local image
image_path = "friends.png"  # Your image filename
# Display the image caption (optional, can be removed if not needed)
st.image(image_path, use_container_width=False)


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

    room_code = ""

    if len(room) > 0 and room[0] == "Join a Room":
        st.subheader("Join a Room")
        room_code = st.text_input("Enter the 6-digit room code:")
        name = st.text_input("Enter your name")
        if len(room_code) != 6:
            st.warning("Please enter a valid 6-digit room code.")
        else:
            room_code = run_client("join", name, room_code)
            if not name:
                st.warning("Please enter your name")
            elif room_code:
                st.session_state["room_code"] = room_code  # Store room info
                join_disabled = False
                st.session_state['curr_room'] = room_code
            else:
                st.warning("Invalid room code. Try again.")
    
    if len(room) > 0 and room[0] == "Host a Room":
        st.subheader("Host a Room")
        name = st.text_input("Enter your name")
        if not name:
            st.warning("Please enter your name.")
        else:  
            room_code = run_client("create", name)  # Get a new room code from server
            st.session_state['curr_room'] = room_code
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
    display_names()

    st.subheader("Location, Location, Location?")
    location = st.text_input("📍Where are you now? No stalking, promise.", st.session_state.preferences.get("location", ""))
    st.session_state.preferences["location"] = location

    st.subheader("Allergies? 🩺")
    allergies = st.multiselect(
        "Pick your edible enemies:",
        ["🤢 Peanuts", "🍖 Shellfish", "🥛 Dairy", "🌾 Gluten", "🫘 Soy", "🌰 Tree Nuts", "🥚 Eggs", "❓ Other (Mystery allergies)"],
        default=st.session_state.preferences.get("allergies", [])
    )
    st.session_state.preferences["allergies"] = allergies

    st.subheader("Health-Related Dietary Preference:")
    health_options = st.multiselect(
        "Choose your wellness vibe:",
        ["🧂 Low-Sodium (aka the flavor monk)", "🥗 Low-Carb (Team Zoodles)", "🍬 Diabetic-Friendly (Sugar, who?)"], 
        default=st.session_state.preferences.get("health_options", [])
    )
    st.session_state.preferences["health_options"] = health_options

    st.subheader("Dietary Restrictions:")
    religious_diet = st.multiselect(
        "What's your food philosophy?",
        ["🕌 Halal", "✡️  Kosher", "🌱 Vegetarian", "🥦 Vegan", "🐟 Pescatarian", "🚫 Gluten-Free"],
        default=st.session_state.preferences.get("religious_diet", [])
    )
    st.session_state.preferences["religious_diet"] = religious_diet

    st.subheader("Cuisine Cravings:")
    cuisines = st.multiselect(
        "Spin the globe of gastronomy:",
        ["🍝 Italian", "🍔 Mexican", "🍣 Chinese", "🍕 Indian", "🍱 Japanese", "🍙 Thai", "🥗 Mediterranean", "🥘 Middle Eastern",
         "🍖 Korean", "🍔 American", "🍣 French", "🍚 African", "🍕 Latin American", "🍒 Greek"],
        default=st.session_state.preferences.get("cuisines", [])
    )
    st.session_state.preferences["cuisines"] = cuisines

    st.subheader("Money Matters & Eating Style:")
    budget_options = st.radio("💸 What’s your vibe?", ["💰 Budget (Ballin’ on a budget)", "💵 Mid-Range (Treat yourself responsibly)", "💎 Fancy (Caviar dreams and truffle wishes)"])
    budget_labels = ["Budget", "Mid-Range", "Fancy"] 

    selected_budget = st.session_state.preferences.get("budget", "Budget")
    selected_budget_index = budget_labels.index(selected_budget) if selected_budget in budget_labels else 0

    eating_options = ["🍴 Dine-In (For the ambiance)", "🥡 Takeout (Sweats mandatory)", "🚚 Delivery (Pajamas forever)"]
    eating_labels = ["Dine-In", "Takeout", "Delivery"]

    selected_eating = st.session_state.preferences.get("eating_preference", "Dine-In")
    selected_eating_index = eating_labels.index(selected_eating) if selected_eating in eating_labels else 0

    eating_preference = st.radio("🍽️ How would you like to feast?", eating_options, index=selected_eating_index)


    def back():
        st.session_state.page = 1  # Go back to page 1

    # Navigation buttons
    st.button("🔙 Back", on_click=back)
        
    st.button("✅ Submit (aka “Feed Me Now!”)", on_click=next_page)

def save_preferences():
    preferences_data = st.session_state.preferences.copy()
    preferences_data["timestamp"] = datetime.now(timezone.utc)

    if "preferences_saved" not in st.session_state:
        preferences_collection.insert_one(preferences_data)
        st.session_state["preferences_saved"] = True
        st.success("Your preferences have been saved!")

    if "restaurant_choices" not in st.session_state:
        restaurant_names, recommendations = get_recommendations(preferences_data)
        st.session_state["restaurant_choices"] = restaurant_names
        if st.session_state["curr_room"]:
            concat_restaraunts(restaurant_names, st.session_state["curr_room"])
            picked_preferences(st.session_state["curr_room"])
        st.session_state["recommendations_text"] = recommendations
    
    st.write("### Recommended Restaurants:")
    st.write(st.session_state["recommendations_text"])

    if st.session_state["curr_room"]:
        # Wait for everyone to submit their preferences
        while not preferences_complete(st.session_state["curr_room"]):
            continue
        # Once preferences are complete, get the restaurant choices
        st.session_state["restaurant_choices"] = get_restaraunts(st.session_state["curr_room"])

    if "restaurant_choices" in st.session_state and st.session_state["restaurant_choices"]:
        chosen_restaurant = st.selectbox(
            "🍽️ Choose a restaurant to visit:",
            st.session_state["restaurant_choices"]
        )

        # Handle the final selection
        if st.button("Confirm Selection"):
            if st.session_state["curr_room"]:
                vote(chosen_restaurant, st.session_state["curr_room"])
                while not voting_complete(st.session_state["curr_room"]):
                    continue
                st.success(get_winning_vote(st.session_state["curr_room"]))
            else:
                st.session_state["final_restaurant"] = chosen_restaurant
                st.success(f"✅ You have chosen: {chosen_restaurant}!")


if st.session_state.page == 4:
    save_preferences()
