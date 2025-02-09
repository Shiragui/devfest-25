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