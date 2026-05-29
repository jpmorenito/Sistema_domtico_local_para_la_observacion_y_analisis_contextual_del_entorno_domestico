from PIL import Image
import numpy as np

img_bak = r"C:\Users\jacob\.gemini\antigravity\brain\cf77bcfa-95a5-4213-95d0-495806909af8\conexion_nodo_ambiente_1779985459934.png"

with Image.open(img_bak) as im:
    im = im.convert("RGB")
    arr = np.array(im)
    
    # 1. Yellow wire (LDR) near x = 680-710
    yellow_mask = (arr[180:590, 675:710, 0] > 180) & (arr[180:590, 675:710, 1] > 180) & (arr[180:590, 675:710, 2] < 100)
    y_yellow, x_yellow = np.where(yellow_mask)
    if len(y_yellow) > 0:
        print("Yellow wire y-range:", 180 + y_yellow.min(), 180 + y_yellow.max())
        
    # 2. Orange wire (Sound) near x = 675-710
    orange_mask = (arr[180:590, 675:710, 0] > 180) & (arr[180:590, 675:710, 1] > 80) & (arr[180:590, 675:710, 1] < 180) & (arr[180:590, 675:710, 2] < 80)
    y_orange, x_orange = np.where(orange_mask)
    if len(y_orange) > 0:
        print("Orange wire y-range:", 180 + y_orange.min(), 180 + y_orange.max())
        
    # 3. Green wire (Relay) near x = 675-710
    green_mask = (arr[180:590, 675:710, 1] > 150) & (arr[180:590, 675:710, 0] < 120) & (arr[180:590, 675:710, 2] < 120)
    y_green, x_green = np.where(green_mask)
    if len(y_green) > 0:
        print("Green wire y-range:", 180 + y_green.min(), 180 + y_green.max())
        
    # 4. Blue wire (DHT11) near x = 310-345
    blue_mask = (arr[180:590, 310:345, 2] > 150) & (arr[180:590, 310:345, 0] < 100) & (arr[180:590, 310:345, 1] > 80)
    y_blue, x_blue = np.where(blue_mask)
    if len(y_blue) > 0:
        print("Blue wire y-range:", 180 + y_blue.min(), 180 + y_blue.max())
        # Let's see if there are two blue wires
        y_unique = np.unique(180 + y_blue)
        print("Unique y-coords for blue wire:", y_unique)
