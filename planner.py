import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import urllib.parse

# Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "llama3"

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

def call_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_API,
            json={"model": MODEL, "prompt": prompt, "options": {"temperature": 0.6, "num_predict": 1024}},
            stream=True
        )
        result = ""
        for line in response.iter_lines():
            if line:
                try:
                    json_obj = json.loads(line.decode("utf-8"))
                    result += json_obj.get("response", "")
                except json.JSONDecodeError:
                    pass
        return result.strip() or "⚠️ No valid response from Ollama."
    except Exception as e:
        return f"❌ Error contacting Ollama: {str(e)}"

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
3. Top 3 hotels with price + links: Booking, Agoda, Maps
4. Top 3 flights with price (use dummy airline info) + links: Skyscanner, MMT
5. Day-wise itinerary with activities, food, hotel, tips.

Format:
- Use clear paragraphs for each section
- Separate hotels and flights as markdown bullet lists
- Then write itinerary:
  - **Day 1**: ...
  - **Day 2**: ... etc.

Use markdown formatting and spacing.
"""
    return call_ollama(prompt)

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
    st.markdown(f"[🗺️ View Hotels and Sights in {selected_city}](https://www.google.com/maps/search/{urllib.parse.quote_plus(selected_city + ' hotels and attractions')})")

    st.subheader("🏨 Book Hotels and Compare Flights")
    components.html(f"""
    <iframe src='https://tp.media/content?promo_id=4045&shmarker=123456&campaign_id=100&trs=264079&locale=en&powered_by=false&searchUrl=hotels&hotel_id=&city={urllib.parse.quote_plus(selected_city)}&country={urllib.parse.quote_plus(selected_country)}&lang=en&currency=usd' width='100%' height='250' frameborder='0'></iframe>
    <iframe src='https://tp.media/content?promo_id=4044&shmarker=123456&campaign_id=101&trs=264079&locale=en&powered_by=false&searchUrl=flights&city_from=&city_to={urllib.parse.quote_plus(selected_city)}&lang=en&currency=usd' width='100%' height='250' frameborder='0'></iframe>
    """, height=600)
