import streamlit as st

st.title("Food Finder")
st.write("Welcome! Find restaurants based on your preferences.")

# Input example
location = st.text_input("Enter your location:")
if location:
    st.write(f"Searching for restaurants near {location}...")
