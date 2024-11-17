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
def getItemData():
    bossInfo = response['data'][0]
    drops = bossInfo.get('drops', [])
    endpoints = [
        "weapons",
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
                'description': 'Currency used in the Lands Between'
            })
        found = False
        for endpoint in endpoints:
            response = requests.get(f"https://eldenring.fanapis.com/api/{endpoint}?name={drop}")
            data = response.json()
            if data['count'] > 0:
                dropInfo = data['data'][0]
                dropInfo['type'] = endpoint[:-1]  # Remove the trailing 's' for singular form
                dropDetails.append(dropInfo)
                found = True
                break
        if not found:
            dropDetails.append({
                'name': drop,
                'description': 'No additional information available.',
                'type': 'unknown'
            })
    return {
        "boss_info": bossInfo,
        "drop_details": dropDetails
    }
    
    
    
    # itemType = None
    # if "weaponsData" not in st.session_state:
    #     st.session_state.weaponsData = req.get(f"{baseURL}/weapons?limit=400").json().get("data", [])
    # if "itemsData" not in st.session_state:
    #     st.session_state.itemsData = req.get(f"{baseURL}/items?limit=500").json().get("data", [])
    # if "ashesData" not in st.session_state:
    #     st.session_state.ashesData = req.get(f"{baseURL}/ashes?limit=100").json().get("data", [])
    # if "sorceriesData" not in st.session_state:
    #     st.session_state.sorceriesData = req.get(f"{baseURL}/sorceries?limit=100").json().get("data", [])
    # if "incantData" not in st.session_state:
    #     st.session_state.incantData = req.get(f"{baseURL}/incantations?limit=100").json().get("data", [])
    # response = req.get(f"{baseURL}/{itemType}?name={itemName}").json()
    # return response.json()
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
    st.subheader(viewedItem)
    #for item in bossInfo.get("drops"):
    #    st.write(item, "Unknown")

#Next task: Get dropped items and display their information
