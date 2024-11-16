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
def getItemData(itemType, itemName):
    response = req.get(f"{baseURL}/{itemType}?name={itemName}")
    return response.json()
#------------------------------------------------------------------------------#
st.title("Elden Ring Boss Finder")

#Input box for boss name
bossName = st.text_input("Enter Boss Name:")

searchButton = st.button("Search")
randomButton = st.button("Random")

bossData = None

#Handle Search button click
if searchButton and bossName:
    bossData = getBossData(bossName)
elif randomButton:  #Handle Random button click
    bossData = getRandomBoss()

#If the user searched but no data was found
if searchButton and bossData and not bossData.get("data"):
    st.write("No boss found. Please enter a valid boss name or click 'Random'.")

#Display boss information if data is retrieved
if bossData and "data" in bossData and bossData["data"]:
    bossInfo = bossData["data"][0]

    #Display boss information
    st.header(bossInfo["name"])
    st.image(bossInfo.get("image", ""))
    st.subheader("Description")
    st.write(bossInfo.get("description", "No description available"))
    st.subheader("Location")
    st.write(bossInfo.get("location", "Unknown"))
    st.subheader("Health Points")
    st.write(bossInfo.get("healthPoints", "Unknown"))
    st.subheader("Item Drops")
    st.write(bossInfo.get("drops", "Unknown"))

#Next task: Get dropped items and display their information
