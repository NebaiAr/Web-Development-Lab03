import requests as req
import random
import streamlit as st

baseURL = "https://eldenring.fanapis.com/api"

def getBossData(bossName=None):
    if bossName:
        response = req.get(f"{baseURL}/bosses?name={bossName}")
    else:
        response = req.get(f"{baseURL}/bosses?limit=100")
        bosses = response.json().get("data")
        bossName = random.choice(bosses)["name"]
        response = req.get(f"{baseURL}/bosses?name={bossName}")
    return response.json()

def getRandomBoss():
    response = req.get(f"{baseURL}/bosses?limit=100")
    bosses = response.json().get("data")
    randomBossName = random.choice(bosses)["name"]
    response = req.get(f"{baseURL}/bosses?name={randomBossName}")
    return response.json()

def getItemData(response):
    bossInfo = response['data'][0]
    drops = bossInfo.get('drops', [])
    endpoints = [
        "weapons",
        "ashes",
        "ammos",
        "items",
        "spirits",
        "armors",
        "shields",
        "talismans",
        "incantations",
        "sorceries"
    ]
    dropDetails = []
    for drop in drops:
        if "Runes" in drop:
            dropDetails.append({
                'name': drop,
                'description': 'Currency used in the Lands Between',
                'type': 'currency',
                'image': 'https://eldenring.fanapis.com/images/items/17f69df1f09l0i2012e482ufurh3wy.png'
            })
            continue
        found = False
        for endpoint in endpoints:
            response = req.get(f"https://eldenring.fanapis.com/api/{endpoint}?name={drop}")
            data = response.json()
            if data['count'] > 0:
                dropInfo = data['data'][0]
                dropInfo['type'] = endpoint[:]  # Remove the trailing 's' for singular form
                dropDetails.append(dropInfo)
                found = True
                break
        if not found:
            dropDetails.append({
                'name': drop,
                'description': 'No additional information available.',
                'type': 'unknown',
                'image': None
            })
    return {
        "boss_info": bossInfo,
        "drop_details": dropDetails
    }
    
    
#------------------------------------------------------------------------------#
st.title("Elden Ring Boss Finder")

#Input box for boss name + submit/random button created
with st.form(key="boss_search_form"):
    bossName = st.text_input("Enter Boss Name:") #NEW
    searchButton = st.form_submit_button("Search") #NEW
randomButton = st.button("Random")

if "bossData" not in st.session_state:
    st.session_state.bossData = None
if "bossInfo" not in st.session_state:
    st.session_state.bossInfo = None
if "dropDetails" not in st.session_state:
    st.session_state.dropDetails = None
#Handle Search button click
if searchButton and bossName:
    st.session_state.bossData = getBossData(bossName)
elif randomButton:  #Handle Random button click
    st.session_state.bossData = getRandomBoss()


#If the user searched but no data was found
if searchButton and st.session_state.bossData and not st.session_state.bossData.get('data'):
    st.write("No boss found. Please enter a valid boss name or click 'Random'.")

#Display boss information if data is retrieved
if st.session_state.bossData and "data" in st.session_state.bossData and st.session_state.bossData["data"]:
    st.session_state.bossInfo = st.session_state.bossData["data"][0]
    st.session_state.dropDetails = getItemData(st.session_state.bossData)["drop_details"]

    #Display boss information
    st.header(st.session_state.bossInfo["name"])
    if st.session_state.bossInfo.get('image') == None:
        st.write("No image available. Sorry :(")
    else:
        st.image(st.session_state.bossInfo.get("image"))
    st.subheader("Description")
    st.write(st.session_state.bossInfo.get("description", "No description available"))
    st.subheader("Location")
    st.write(st.session_state.bossInfo.get("location", "Unknown"))
    st.subheader("Health Points")
    st.write(st.session_state.bossInfo.get("healthPoints", "Unknown"))
    st.subheader("Item Drops")
    dropNames = [drop['name'] for drop in st.session_state.dropDetails]
    selectedDrop = st.selectbox("Select a drop to view details:", dropNames) #NEW
    for drop in st.session_state.dropDetails:
        if drop['name'] == selectedDrop:
            st.write(f"**Name:** {drop['name']}")
            st.write(f"**Type:** {drop['type'].capitalize()}")
            st.write(f"**Description:** {drop.get('description', 'No description available.')}")
            if type(drop['image']) == str:
                st.image(drop['image'])
            elif drop['image'] == None:
                st.write(f"**Image**: No image available")
            break
    #for item in bossInfo.get("drops"):
    #    st.write(item, "Unknown")

#Next task: Get dropped items and display their information
