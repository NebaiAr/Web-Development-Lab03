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
# Weapon and Sorcery data
weapon = None
sorcery = None

if searchButton:
    if weaponName:
        response = req.get(f"{baseURL}/weapons?name={weaponName}").json()
        if response.get("data"):
            weapon = response["data"][0]
        else:
            st.error("Weapon not found. Please try another name.")
    else:
        st.error("Please enter a weapon name or click the Randomize button.")
    
    if sorceryName:
        response = req.get(f"{baseURL}/sorceries?name={sorceryName}").json()
        if response.get("data"):
            sorcery = response["data"][0]
        else:
            st.error("Sorcery not found. Please try another name.")
    else:
        st.error("Please enter a sorcery name or click the Randomize button.")

elif randomButton:
    weapon = randomWeapon()
    sorcery = randomSorcery()


if weapon and sorcery:
    st.header("Selected Weapon and Sorcery")
    col1, col2 = st.columns(2)

    with col1:
        st.image(weapon.get("image"), caption=weapon.get("name", "Unknown Weapon"))
        st.write(f"**Description:** {weapon.get('description', 'No description available.')}")
        
    with col2:
        st.image(sorcery.get("image", ""), caption=sorcery.get("name", "Unknown Sorcery"))
        st.write(f"**Description:** {sorcery.get('description', 'No description available.')}")

    st.subheader("Battle Strategy")
    try:
        prompt = (
            f'''The attack key for weapons contains different types of damage and the amount
            of damage dealt by that weapon in particular. The defence key is similar, but rather
            than being a flat damage reduction, the amount describes the percent of that damage
            type that is blocked when the weapon is used to guard. The scalesWith key contains
            data for which stats the weapon damage scales with, and the letter under scaling
            describes how much the damage of the weapon scales. E scaling isn't great, D scaling
            is better, C scaling is roughly average, B scaling is good, A scaling is great, and
            S scaling is typically the best. The only weapons this works differently for are
            staffs and finger seals, which use the stat scaling to determine spell scaling
            (which affects the damage of sorceries and incantations). For instance, if a weapon
            scales D in strength and A in dex, it's more effective to level dexterity as it
            increases the damage more than leveling strength. The category describes what type
            of weapon it is, and the weight is how heavy it is. This is important primarily for
            playstyle purposes, as some players forfeit faster rolls and some agility for more
            defense. The description key (before attack) is a rough lore description of the
            weapon. Weapon data can be found as {st.session_state.weapon}. Sorceries work differently,
            using some different values than weapons. Under the sorceries endpoint of the API,
            cost describes how much FP (think mana) is required to use the sorcery. the
            description is, again, an in-lore description of the sorcery, providing some
            background information. The effects describes what the sorcery does (i.e. strikes
            from behind with projectile fired from distance' for the spell Ambush Shard).
            The requires key shows what stats are required to cast the sorcery in question and
            how much of that stat is required. For instance, the spell Ambush Shard requires 23
            intelligence, 0 faith, and 0 arcane to cast. Sorcery data is {st.session_state.sorcery}'''
        )
        response = model.generate_content(prompt)
        st.write(response) 
    except Exception as e:
        st.error(f"Failed to generate strategy: {e}")
    
    st.subheader("Now, do you have any more questions concerning this weapon combo?")
    followupQuestion = st.text_input("Enter your follow-up question:")
    followupButton = st.button("Ask AI")

    if followupButton and followupQuestion:
        try:
            followupResponse = model.generate_content(followupQuestion)
            st.write(followupResponse.result)
        except Exception as e:
            st.error(f"Failed to generate follow-up response: {e}")