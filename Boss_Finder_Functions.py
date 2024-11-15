import requests as req
import random
import streamlit as st

url = "https://eldenring.fanapis.com/api"

def getBossData(bossName=None):
    if bossName:
        response = req.get(f"{baseURL}/bosses?name={bossName}")
    else:
        response = req.get(f"{baseURL}/bosses")
        bosses = response.json().get("data", [])
        bossName = random.choice(bosses)["name"]
        response = req.get(f"{baseURL}/bosses?name={bossName}")
    return response.json()

def getRandomBoss():
    response = req.get(f"{baseURL}/bosses")
    bosses = response.json().get("data", [])
    randomBossName = random.choice(bosses)["name"]
    response = req.get(f"{baseURL}/bosses?name={randomBossName}")
    return response.json()

def getItemData(itemType, itemName):
    response = req.get(f"{baseURL}/{itemType}?name={itemName}")
    return response.json()
