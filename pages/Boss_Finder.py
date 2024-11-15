import streamlit as st
import Boss_Finder_Functions

st.title("Elden Ring Boss Finder")

# Input box for boss name
bossName = st.text_input("Enter Boss Name:")

search_button = st.button("Search")
random_button = st.button("Random")

bossData = None

# Handle Search button click
if searchButton and bossName:
    bossData = getBossData(bossName)
elif randomButton:  # Handle Random button click
    bossData = getRandomBoss()

# Display boss information if data is retrieved
if bossData and "data" in bossData and bossData["data"]:
    bossInfo = bossData["data"][0]

    # Display boss information
    st.header(bossInfo["name"])
    st.image(bossInfo.get("image", ""))
    st.subheader("Description")
    st.write(bossInfo.get("description", "No description available"))
    st.subheader("Location")
    st.write(bossInfo.get("location", "Unknown"))
    st.subheader("Health Points")
    st.write(bossInfo.get("health", "Unknown"))

    # Display dropped items
    st.subheader("Dropped Items")
    for drop in bossInfo.get("drops", []):
        itemType = drop.get("type", "").lower()
        itemName = drop.get("name", "")
        
        with st.expander(f"{itemName} ({itemType.title()})"):
            itemData = getItemData(itemType, itemName)
            if "data" in itemData and itemData["data"]:
                itemInfo = itemData["data"][0]
                st.write("Description:", itemInfo.get("description", "No description available"))
                st.write("Attack Power:", itemInfo.get("attack_power", "N/A"))
                st.write("Location:", itemInfo.get("location", "Unknown"))
                st.write("Other Info:", itemInfo.get("additional_info", "None"))
else:
    st.write("No boss found. Please enter a boss name or click 'Random'.")
