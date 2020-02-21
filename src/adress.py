import folium, webbrowser
import requests
import json


map = folium.Map( zoom_start=12)
print("Map created")


def UserEntry() :
    entry = input("Choisir votre adresse : ")
    entry = entry.split()
    separator = '+'
    adress = separator.join(entry)
    print("Your adress : ",adress)
    return adress

adress = UserEntry()
result = requests.get('https://nominatim.openstreetmap.org/search?q=' + adress +'&format=json&countrycodes=fr').json()
print("finding your adress")

print(result)
for i in range(len(result)) :
    
    lat = result[i]['lat']
    lon = result[i]['lon']
    map.add_child(folium.Marker([lat,lon], popup=i, tooltip=i))



print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open('./map.html')
