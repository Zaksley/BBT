import folium, webbrowser
import requests
import json


map = folium.Map( zoom_start=12)
print("Map created")


def UserEntry() :
    entry = input("Choisir votre adresse :")
    entry = entry.split()
    separator = '+'
    adress = separator.join(entry)
    print("Your adress : ",adress)
    return adress

adress = UserEntry()
jsonFocus = requests.get('https://nominatim.openstreetmap.org/search?q=' + adress +'&format=json&countrycodes=fr').json()
print("finding your adress")

for i in range(len(jsonFocus)) :
    
    latfocus = jsonFocus[i]['lat']
    lonfocus = jsonFocus[i]['lon']
    map.add_child(folium.Marker([latfocus,lonfocus], popup=i, tooltip=i))



print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open('./map.html')
