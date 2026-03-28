import streamlit as st
import pickle
import pandas as pd

df = pickle.load(open('restaurant_data.pkl', 'rb'))

food_to_cuisine = {
    "pizza": "italian",
    "pasta": "italian",
    "biryani": "north indian",
    "dosa": "south indian",
    "idli": "south indian",
    "noodles": "chinese",
    "burger": "fast food"
}

def recommend(food, location, max_cost):
    
    cuisine = food_to_cuisine.get(food.lower(), food.lower())
    
    result = df[df['cuisines'].str.contains(cuisine)]
    
    if location:
        result = result[result['location'].str.lower() == location.lower()]
    
    if max_cost:
        result = result[result['approx_cost(for two people)'] <= max_cost]
    
    result['score'] = (result['rate'] * 2) + (result['votes'] / 1000)
    
    result = result.sort_values(by='score', ascending=False)
    
    return result.head(10)

st.set_page_config(page_title="Swiggy Style Recommender", layout="wide")

st.title("🍽️ Swiggy Style Restaurant Recommender")

col1, col2, col3 = st.columns(3)

with col1:
    food = st.text_input("🍕 What do you want to eat?")

with col2:
    location = st.text_input("📍 Location")

with col3:
    max_cost = st.number_input("💰 Budget", min_value=0)

if st.button("🔍 Find Restaurants"):
    
    results = recommend(food, location, max_cost)
    
    if results.empty:
        st.warning("No restaurants found 😔")
    else:
        for _, row in results.iterrows():
            st.markdown(f"""
            ### 🍴 {row['name']}
            📍 {row['location']}  
            ⭐ Rating: {row['rate']} | 👍 Votes: {row['votes']}  
            🍽️ {row['cuisines']}
            💰 Cost for two: ₹{row['approx_cost(for two people)']}
            """)