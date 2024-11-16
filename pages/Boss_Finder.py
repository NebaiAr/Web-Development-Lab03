import requests as req
import random
import streamlit as st

baseURL = "https://eldenring.fanapis.com/api"

#NEW
def getBossData(bossName=None):
    if bossName:
        response = req.get(f"{baseURL}/bosses?name={bossName}")
    else:
        response = req.get(f"{baseURL}/bosses?limit=100")
        bosses = response.json().get("data")
        bossName = random.choice(bosses)["name"]
        response = req.get(f"{baseURL}/bosses?name={bossName}")
    return response.json()

#NEW
def getRandomBoss():
    response = req.get(f"{baseURL}/bosses?limit=100")
    bosses = response.json().get("data")
    randomBossName = random.choice(bosses)["name"]
    response = req.get(f"{baseURL}/bosses?name={randomBossName}")
    return response.json()

#NEW
def getItemData(itemName):
    itemType = None
    weaponRes = req.get(f"{baseURL}/weapons?limit=400").json()
    itemRes = req.get(f"{baseURL}/items?limit=500").json()
    ashRes = req.get(f"{baseURL}/ashes?limit=100").json()
    if itemName in weaponRes['data']:
        itemType = 'weapons'
    elif itemName in itemRes['data']:
        itemType = 'items'
    elif itemName in ashRes['data']:
        itemType = 'items'
    response = req.get(f"{baseURL}/{itemType}?name={itemName}").json()
    return response.json()
#------------------------------------------------------------------------------#
st.title("Elden Ring Boss Finder")

#Input box for boss name
bossName = st.text_input("Enter Boss Name:")

searchButton = st.button("Search")
randomButton = st.button("Random")

if "bossData" not in st.session_state:
    st.session_state.bossData = None
if "bossInfo" not in st.session_state:
    st.session_state.bossInfo = None

#Handle Search button click
if searchButton and bossName:
    st.session_state.bossData = getBossData(bossName)
elif randomButton:  #Handle Random button click
    st.session_state.bossData = getRandomBoss()

#If the user searched but no data was found
if searchButton and st.session_state.bossData and not st.session_state.bossData.get("data"):
    st.write("No boss found. Please enter a valid boss name or click 'Random'.")

#Display boss information if data is retrieved
if st.session_state.bossData and "data" in st.session_state.bossData and st.session_state.bossData["data"]:
    st.session_state.bossInfo = st.session_state.bossData["data"][0]
    items = st.session_state.bossInfo.get("drops")

    #Display boss information
    st.header(st.session_state.bossInfo["name"])
    st.image(st.session_state.bossInfo.get("image", ""))
    st.subheader("Description")
    st.write(st.session_state.bossInfo.get("description", "No description available"))
    st.subheader("Location")
    st.write(st.session_state.bossInfo.get("location", "Unknown"))
    st.subheader("Health Points")
    st.write(st.session_state.bossInfo.get("healthPoints", "Unknown"))
    st.subheader("Item Drops")
    viewedItem = st.selectbox("Which drop would you like to view?", items)
    itemData = getItemData(viewedItem)
    st.subheader(itemData.get('name'))
    #for item in bossInfo.get("drops"):
    #    st.write(item, "Unknown")

#Next task: Get dropped items and display their information
