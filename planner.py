import streamlit as st
import streamlit.components.v1 as components
import requests
import google.generativeai as genai
import json
import urllib.parse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Gemini API Key
# It's better to ensure this is truly loaded from the environment
# and provide a clear message if it's not.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY environment variable not found. Please set it.")
    st.stop() # Stop the app if the key isn't available

genai.configure(api_key=GEMINI_API_KEY)

# Travelpayouts verification meta tag
st.markdown("""
<meta name="travelpayouts-site-verification" content="xyz12345" />
""", unsafe_allow_html=True)

# Travelpayouts affiliate JS script
st.markdown("""
<script data-noptimize="1" data-cfasync="false" data-wpfc-render="false">
  (function () {
      var script = document.createElement("script");
      script.async = 1;
      script.src = 'https://emrldtp.cc/NDM0MDk2.js?t=434096';
      document.head.appendChild(script);
  })();
</script>
""", unsafe_allow_html=True)

# User login or registration
st.sidebar.header("🔐 User Access")
login_email = st.sidebar.text_input("📧 Email")
login_password = st.sidebar.text_input("🔑 Password", type="password")
if st.sidebar.button("🔓 Login / Sign Up"):
    if login_email and login_password:
        st.sidebar.success(f"Welcome, {login_email.split('@')[0]}! 🎉")
    else:
        st.sidebar.error("Please enter both email and password.")

# Country → Cities
countries_cities = {
    "India 🇮🇳": ["Goa", "Manali", "Udaipur", "Jaipur", "Kerala"],
    "Thailand 🇹🇭": ["Bangkok", "Phuket", "Chiang Mai", "Krabi"],
    "Italy 🇮🇹": ["Rome", "Venice", "Florence", "Milan"],
    "USA 🇺🇸": ["New York", "Los Angeles", "Las Vegas", "San Francisco", "Miami"],
    "Japan 🇯🇵": ["Tokyo", "Kyoto", "Osaka", "Hokkaido"],
    "France 🇫🇷": ["Paris", "Nice", "Lyon", "Marseille"],
    "Australia 🇦🇺": ["Sydney", "Melbourne", "Brisbane", "Gold Coast"],
    "UAE 🇦🇪": ["Dubai", "Abu Dhabi", "Sharjah"],
    "UK 🇬🇧": ["London", "Edinburgh", "Manchester", "Birmingham"],
    "South Africa 🇿🇦": ["Cape Town", "Johannesburg", "Durban", "Pretoria"]
}

currency_symbols = {
    "INR (₹)": "₹",
    "USD ($)": "$",
    "EUR (€)": "€",
    "JPY (¥)": "¥",
    "AED (د.إ)": "د.إ",
    "GBP (£)": "£",
    "ZAR (R)": "R"
}

travel_styles = ["Budget 🛏️", "Standard ✈️", "Luxury 💎", "Backpacking 🎒", "Family 👨‍👩‍👧‍👦"]

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

def generate_booking_links(hotel, city):
    query = urllib.parse.quote_plus(f"{hotel} {city}")
    return {
        "Booking.com": f"https://www.booking.com/searchresults.html?ss={query}",
        "Agoda": f"https://www.agoda.com/search?city={query}",
        "Google Maps": f"https://www.google.com/maps?q={query}"
    }

def call_gemini(prompt):
    """
    Calls the Gemini API with a given prompt and returns the model's response.

    Args:
        prompt (str): The text prompt to send to the Gemini model.

    Returns:
        str: The generated text response from the Gemini API, or an error message.
    """
    try:
        # Correct model name: "gemini-1.5-flash" or "gemini-pro" are common choices.
        # "ggemini-2.5-flash" is not a valid public model name.
        model = genai.GenerativeModel("gemini-1.5-flash") # Or "gemini-pro"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error contacting Gemini API: {str(e)}"

def super_travel_agent(city, country, days, interests, currency_symbol, travel_style, flight_option, month):
    prompt = f"""
You are a professional travel planner AI.

Plan a {days}-day {travel_style} trip to {city}, {country} in {month}.

🧳 Preferences:
- Interests: {interests}
- Include flights: {flight_option}

💡 Provide:
1. Seasonal tips: is {month} good? Pros/cons.
2. Realistic total budget in {currency_symbol} ({'with flights' if flight_option == 'Yes' else 'excluding flights'})
3. Top 3 hotels with price + links: Booking, Agoda, Maps (use dummy prices for hotels if not specified by user. Provide a range e.g. 100-200 USD)
4. Top 3 flights with price (use dummy airline info, provide a range e.g. 300-500 USD) + links: Skyscanner, MMT
5. Day-wise itinerary with activities, food, hotel, tips.

Format:
- Use clear paragraphs for each section
- Separate hotels and flights as markdown bullet lists
- Then write itinerary:
  - **Day 1**: ...
  - **Day 2**: ... etc.

Use markdown formatting and spacing.
"""
    return call_gemini(prompt)

# Streamlit UI
st.set_page_config(page_title="AI Trip Planner", layout="centered")
st.title("🌐 AI Trip Planner: Flights + Hotels + Itinerary")
st.markdown("Smart planning with live price comparison and map links.")

selected_country = st.selectbox("🌍 Select Country", list(countries_cities.keys()))
available_cities = countries_cities[selected_country]

with st.form("trip_form"):
    selected_city = st.selectbox("🏙️ Select City", available_cities)
    travel_style = st.selectbox("✈️ Travel Style", travel_styles)
    currency_choice = st.selectbox("💱 Currency", list(currency_symbols.keys()))
    currency_symbol = currency_symbols[currency_choice]

    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("🕒 Number of Days", 1, 14, 5)
        month = st.selectbox("📅 Travel Month", months)
    with col2:
        interests = st.text_input("🎯 Your Interests", "beaches, adventure, seafood")
        flight_option = st.radio("✈️ Include Flights?", ["Yes", "No"], index=1)

    submit = st.form_submit_button("🧠 Generate Trip Plan")

if submit:
    st.subheader("🧠 AI-Powered Trip Plan")
    with st.spinner("Planning your itinerary and comparing prices..."):
        plan = super_travel_agent(
            selected_city, selected_country, days,
            interests, currency_symbol,
            travel_style, flight_option, month
        )
    st.markdown(plan, unsafe_allow_html=True)

    st.subheader("📍 Maps of Suggested Places")
    # Using the correct base URL for Google Maps
    st.markdown(f"[🗺️ View Hotels and Sights in {selected_city}](https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(selected_city + ' hotels and attractions')})")

    st.subheader("🏨 Book Hotels and Compare Flights")
    components.html(f"""
    <iframe src='https://tp.media/content?promo_id=4045&shmarker=123456&campaign_id=100&trs=264079&locale=en&powered_by=false&searchUrl=hotels&hotel_id=&city={urllib.parse.quote_plus(selected_city)}&country={urllib.parse.quote_plus(selected_country)}&lang=en&currency=usd' width='100%' height='250' frameborder='0'></iframe>
    <iframe src='https://tp.media/content?promo_id=4044&shmarker=123456&campaign_id=101&trs=264079&locale=en&powered_by=false&searchUrl=flights&city_from=&city_to={urllib.parse.quote_plus(selected_city)}&lang=en&currency=usd' width='100%' height='250' frameborder='0'></iframe>
    <div style='position:fixed;bottom:15px;right:15px;z-index:1000;'>
      <a href='https://www.skyscanner.com/' target='_blank'><img src='https://www.travelpayouts.com/img/banners/728x90_en_flight.png' width='240'/></a>
    </div>
    """, height=650)