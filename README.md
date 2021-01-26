# Bordeaux Bike Travel Project

![Logo](https://raw.githubusercontent.com/pjdevs/bbt/master/bbt_full_transparent.png)
A safe routing application for bikes in Bordeaux using OpenStreet Map

## Functionalities

- Written in Python 3 with PyQt
- Save a geographical zone to a graph from OpenStreetMap data
- Search for adresses in France
- Pathfinding with this adresses
- Use custom version of the weighted A* algorithm for safety
- Adjust safety and speed settings

## Dependencies

You will need :

- requests
- folium
- overpy
- PyQt5
- PyQt5-sip (if not in PyQt5)
- PyQtWebEngine

But you can simply run
```
$ pip3 install -r requirements.txt
```

## Usage

#### 1 - Clone this repos

Run
```
$ git clone https://github.com/pjdevs/bbt
$ cd bbt
```
to enter the project directory

#### 2 - Save a graph

You must save a graph, using a bounding box of coordinates, in which you will use routing
Run this command for Bordeaux as an example
```
$ python3 src/graphbuilder.py 44.7973,-0.6580,44.8550,-0.5756
```

#### 3 - Enjoy BBT

Launch BBT !

```
$ python3 src/main.py
```
