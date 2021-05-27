from graphics import *
import math
import re
import json


# Base terrains
GRASSLAND = 0
GRASSLAND_HILLS = 1
PLAINS = 2
PLAINS_HILLS = 3
DESERT = 4
DESERT_HILLS = 5
TUNDRA = 6
TUNDRA_HILLS = 7
SNOW = 8
SNOW_HILLS = 9
COAST = 10
LAKE = 11
OCEAN = 12
MOUNTAINS = 13

# Terrain features
WOODS = 14
RAINFOREST = 15
MARSH = 16
ADJ_RIVER = 17
FLOODPLAINS = 18
OASIS = 19
CLIFFS = 20
REEF = 21
ICE = 22
VOLCANO = 23
VOLCANIC_SOIL = 24
GEOTHERMAL_FISSURE = 25


def main():
    height = 900
    width = 1400
    win = GraphWin("Civ 6 cheats", width, height)
    win.setBackground(color_rgb(0, 0, 0))
    
    map = drawMap(win);
    xOffset = 0
    yOffset = 0

    # Draw UI
    rectangle = Rectangle(Point(0,0), Point(width,100))
    rectangle.setFill("black")
    rectangle.draw(win)
    line = Line(Point(0,100), Point(width,100))
    line.setOutline("grey")
    line.draw(win)
    textBox = Rectangle(Point(20,30), Point(width-20, 70))
    textBox.setOutline("grey")
    textBox.draw(win)
    textView = Text(Point(width/2,50), "")
    textView.setOutline("grey")
    textView.draw(win)

    baseTerrainDic = {
        "g": GRASSLAND,
        "gh": GRASSLAND_HILLS,
        "p": PLAINS,
        "ph": PLAINS_HILLS,
        "d": DESERT,
        "dh": DESERT_HILLS,
        "t": TUNDRA,
        "th": TUNDRA_HILLS,
        "s": SNOW,
        "sh": SNOW_HILLS,
        "c": COAST,
        "l": LAKE,
        "o": OCEAN,
        "m": MOUNTAINS
    }

    terrainFeaturesDic = {
        "w": WOODS,
        "r": RAINFOREST,
        "ma": MARSH,
        "ar": ADJ_RIVER,
        "f": FLOODPLAINS,
        "oa": OASIS,
        "cl": CLIFFS,
        "re": REEF,
        "i": ICE,
        "v": VOLCANO,
        "vs": VOLCANIC_SOIL,
        "gf": GEOTHERMAL_FISSURE,
    }

    lastClickedTile = None
    while True:
        mouseClick = win.checkMouse()
        if mouseClick != None:
            tileClicked = tileClick(mouseClick, map, xOffset, yOffset)
            if (tileClicked != None):
                tileClicked.poly.setFill("green")
                if lastClickedTile != None:
                    lastClickedTile.poly.setFill("black")
                lastClickedTile = tileClicked
                textView.setText(tileClicked.text)

        keyPress = win.checkKey()
        moveAmt = 20
        directions = {
            "Left": [-moveAmt, 0],
            "Right": [moveAmt, 0], 
            "Up": [0, -moveAmt], 
            "Down": [0, moveAmt]
        }
        if keyPress != "":
            print(keyPress)
            if keyPress in directions:
                for i in map:
                    for j in i:
                        offset = directions[keyPress]
                        j.poly.move(offset[0], offset[1])
                xOffset += offset[0]
                yOffset += offset[1]
            elif keyPress == "F1":
                saveMap(map)
            else:
                if lastClickedTile != None:
                    addText(lastClickedTile, textView, keyPress)
                


class Tile:
    def __init__(self):
        self.mapX = None
        self.mapY = None
        self.coord = None
        self.poly = None
        self.text = ""
        self.baseTerrain = None
        self.terrainFeatures = []
    
    def setCoord(self, point):
        self.coord = point
        self.poly = makeHexagonPoly(point)

    def __str__(self):
        return "(%d,%d)" %(self.mapX,self.mapY)



def makeHexagonPoly(centre):
    scale = 10
    x = centre.getX()
    y = centre.getY()
    aPolygon = Polygon(Point(x-3.5*scale,y-1.7*scale), Point(x,y-4*scale), Point(x+3.5*scale,y-1.7*scale), 
        Point(x+3.5*scale,y+1.7*scale), Point(x,y+4*scale), Point(x-3.5*scale,y+1.7*scale))
    return aPolygon


def drawMap(win):
    mapXLength = 10
    mapYLength = 10
    map = [[Tile]*mapYLength for i in range(mapXLength)]

    for i in range(0, mapXLength):
        for j in range(0, mapYLength):
            map[i][j] = Tile()
            map[i][j].mapX = i
            map[i][j].mapY = j

            if j%2 == 0:
                map[i][j].setCoord(Point(i*76+100, j*62+100))
            else:
                map[i][j].setCoord(Point(i*76+138, j*62+100))
            map[i][j].poly.setOutline("green")
            map[i][j].poly.setWidth(2)
            map[i][j].poly.draw(win)
    
    return map


def tileClick(mouse, map, xOffset, yOffset):
    a = mouse.getX()-xOffset
    b = mouse.getY()-yOffset
    aproxMapX1 = math.floor((a-100)/76)
    aproxMapX2 = math.ceil((a-100)/76)
    mapY = round((b-100)/62)
    
    t1 = None
    t2 = None
    mapLength = len(map)
    if (mapY >= 0 and mapY < mapLength):    
        if aproxMapX1 >= 0 and aproxMapX1 < mapLength:
            if aproxMapX2 >= 0 and aproxMapX2 < mapLength:
                t1 = map[aproxMapX1][mapY]
                t2 = map[aproxMapX2][mapY]
                dt1 = (t1.coord.getX() - a)**2 + (t1.coord.getY() - b)**2
                dt2 = (t2.coord.getX() - a)**2 + (t2.coord.getY() - b)**2
                if dt1 < dt2:
                    return t1
                else:
                    return t2
            else:
                t1 = map[aproxMapX1][mapY]
                return t1
        elif aproxMapX2 >= 0 and aproxMapX2 < mapLength:
            t2 = map[aproxMapX2][mapY]
            return t2
    

def addText(tile, textView, keyPress):

    if keyPress == "comma":
        keyPress = ","
    elif keyPress == "space":
        keyPress = " "
    elif keyPress == "BackSpace":
        keyPress = ""
        textView.setText(textView.getText()[:-1])
        if len(tile.text) > 0:
            tile.text = tile.text[:-1]
    if len(keyPress) == 1:
        textView.setText(textView.getText()+keyPress)
        tile.text = tile.text + keyPress

    parseText(tile)


def parseText(tile):
    modifiers = re.split(",", tile.text)
    for modifier in modifiers:
        if (modifier == "g"):
            tile.baseTerrain = GRASSLAND
        elif (modifier == "gh"):
            tile.baseTerrain = GRASSLAND_HILLS
        elif (modifier == "p"):
            tile.baseTerrain = PLAINS
        elif (modifier == "ph"):
            tile.baseTerrain = PLAINS_HILLS
        elif (modifier == "d"):
            tile.baseTerrain = DESERT
        elif (modifier == "dh"):
            tile.baseTerrain = DESERT_HILLS
        elif (modifier == "t"):
            tile.baseTerrain = TUNDRA
        elif (modifier == "th"):
            tile.baseTerrain = TUNDRA_HILLS
        elif (modifier == "s"):
            tile.baseTerrain = SNOW
        elif (modifier == "sh"):
            tile.baseTerrain = SNOW_HILLS
        elif (modifier == "c"):
            tile.baseTerrain = COAST
        elif (modifier == "l"):
            tile.baseTerrain = LAKE
        elif (modifier == "o"):
            tile.baseTerrain = OCEAN
        elif (modifier == "m"):
            tile.baseTerrain = MOUNTAINS
        elif (modifier == "w"):
            tile.terrainFeatures.append(WOODS)
        elif (modifier == "r"):
            tile.terrainFeatures.append(RAINFOREST)
        elif (modifier == "m"):
            tile.terrainFeatures.append(MARSH)
        elif (modifier == "ar"):
            tile.terrainFeatures.append(ADJ_RIVER)
        elif (modifier == "f"):
            tile.terrainFeatures.append(FLOODPLAINS)
        elif (modifier == "oa"):
            tile.terrainFeatures.append(OASIS)
        elif (modifier == "cl"):
            tile.terrainFeatures.append(CLIFFS)
        elif (modifier == "re"):
            tile.terrainFeatures.append(REEF)
        elif (modifier == "i"):
            tile.terrainFeatures.append(ICE)
        elif (modifier == "v"):
            tile.terrainFeatures.append(VOLCANO)
        elif (modifier == "vs"):
            tile.terrainFeatures.append(VOLCANIC_SOIL)
        elif (modifier == "gf"):
            tile.terrainFeatures.append(GEOTHERMAL_FISSURE)

    print("%d" % tile.baseTerrain)
        

def saveMap(map):
    mapDict = {}
    i = 0
    for column in map:
        for tile in column:
            mapDict[i] = {
                'mapX': tile.mapX,
                'mapY': tile.mapY,
                'text': tile.text,
                'baseTerrain': tile.baseTerrain,
                'terrainFeatures': tile.terrainFeatures
            }
            i += 1

    with open('map-data.json', 'w') as f:
        json.dump(mapDict, f)
    print("Map saved")



    


main()