import streamlit as st
import requests as req
import random
import google.generativeai as genai
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCKpE5_kShn2_GcaL-oztw6Jn9_P9eITcs"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash") #this is the free model of google gemini

baseURL = "https://eldenring.fanapis.com/api"
def randomWeapon():
    response = req.get(f"{baseURL}/weapons?limit=100&page={random.randint(0, 3)}").json()
    return random.choice(response["data"])
    

def randomSorcery():
    response = req.get(f"{baseURL}/sorceries?limit=100").json()
    return random.choice(response["data"])
    

#---------------------------------------------------#

st.title("Elden Ring Battle Assistant")
st.write("Welcome to the Elden Ring AI Battle Assistant! Enter in a weapon and sorcery (or have them randomly selected for you) and recieve a detailed explanation on how you can pair them together in battle. Once the report is finished, you can ask follow-up questions about the combination")

with st.form("battle_form"):
    weaponName = st.text_input("Enter Weapon Name:")
    sorceryName = st.text_input("Enter Sorcery Name:")
    searchButton = st.form_submit_button("Search")
randomButton = st.button("Randomize Weapon and Sorcery")

# Weapon, Sorcery, and AI Context data
if "weapon" not in st.session_state:
    st.session_state.weapon = None
if "sorcery" not in st.session_state:
    st.session_state.sorcery = None
if "aiContext" not in st.session_state:
    st.session_state.aiContext = ""

if searchButton:
    if weaponName:
        response = req.get(f"{baseURL}/weapons?name={weaponName}").json()
        if response.get("data"):
            st.session_state.weapon = response["data"][0]
        else:
            st.error("Weapon not found. Please try another name.")
    else:
        st.error("Please enter a weapon name or click the Randomize button.")
    
    if sorceryName:
        response = req.get(f"{baseURL}/sorceries?name={sorceryName}").json()
        if response.get("data"):
            st.session_state.sorcery = response["data"][0]
        else:
            st.error("Sorcery not found. Please try another name.")
    else:
        st.error("Please enter a sorcery name or click the Randomize button.")

elif randomButton:
    st.session_state.weapon = randomWeapon()
    st.session_state.sorcery = randomSorcery()


if st.session_state.weapon and st.session_state.sorcery:
    st.header("Selected Weapon and Sorcery")
    col1, col2 = st.columns(2)

    with col1:
        st.image(st.session_state.weapon.get("image"), caption=st.session_state.weapon.get("name", "Unknown Weapon"))
        st.write(f"**Description:** {st.session_state.weapon.get('description', 'No description available.')}")
        
    with col2:
        st.image(st.session_state.sorcery.get("image", ""), caption=st.session_state.sorcery.get("name", "Unknown Sorcery"))
        st.write(f"**Description:** {st.session_state.sorcery.get('description', 'No description available.')}")

    st.subheader("Battle Strategy")
    if not st.session_state.aiContext:    
        try:
            prompt = (
                f"Explain how to effectively use the weapon '{weapon['name']}' and "
                f"the sorcery '{sorcery['name']}' in combination during battle in Elden Ring. "
                f"Provide a detailed strategy for maximizing their synergy."
            )
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.aiContext = response
        except Exception as e:
            st.error(f"Failed to generate strategy: {e}")
    
    st.subheader("Now, do you have any more questions concerning this weapon combo?")
    followupQuestion = st.text_input("Enter your follow-up question:")
    followupButton = st.button("Ask AI")

    if followupButton and followupQuestion:
        try:
            fullPrompt = f"{st.session_state.aiContext}\n\nFollow-up Question: {followupQuestion}"
            followupResponse = model.generate_content(fullPrompt)
            st.write(followupResponse.text)
            st.session_state.ai_context += f"\n\nFollow-up Question: {followupQuestion}\nAI Response: {followupResponse.text}"
        except Exception as e:
            st.error(f"Failed to generate follow-up response: {e}")