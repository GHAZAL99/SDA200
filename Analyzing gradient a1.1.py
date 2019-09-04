# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:58:54 2019

@author: Nabil Ghazal
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from PIL import Image, ImageDraw
import numpy as np
height = 0  #height of the image
width = 0   #width of the image
file_name = input("Write file name with extension: (ex: .jpg)")
#Reurns a list containing the RGBs of each pixel: List[Rows[pixels(RGB)]]
def image_pixelizing(image1):
    """Image-->pixel"""
    global height, width
    pixels_in_image = list(image1.getdata())
    width, height = image1.size
    number_pixels = height * width
    start = 0
    end = width
    list_rows = []
    while end <= number_pixels:
        list_rows.append( pixels_in_image[start:end])
        start = end
        end = end + width
    return list_rows

def load_image(file_name):

    while True:
        try:
            device = Image.open(file_name)
            break
            #device.load()
        except:
            print("Unable to load Image")
    pixels = image_pixelizing(device)
    return pixels


# =============================================================================
# x1,y1 are the coordinates of the center of the 1st chamber
# x2,y2 are the coordinates of the center of the 21st chamber
# srow1x, srow1y are the coordinates for the last chamber of the 1st row
# srow2x, srow2y are the coordinates for the last chamber of the 2nd row
# scol1x, scol1y are the coordinates of the 9th chamber of the first (left-most) column
# scol2x, scol2y are the coordinates of the 10th chamber of the last (right-most) column
# =============================================================================
    
def select_centers(x1, y1, x2, y2, srow1x, srow1y, scol1x, scol1y, srow2x, srow2y, scol2x, scol2y):
    #try to use 6 points, and find the linear equations of each to find the rest of the points
    #needs fixing
    column = 0
    row = 0
    list_centers = []
    ordonnee1 = 0
    ordonnee2 = 0
    distancex1 = (srow1x -x1)/19
    distancex2 = (x2 - srow2x)/19
    distancey1 = (srow1y -y1)/19
    distancey2 = (srow2y-y2)/19
    jumpx1 = (scol1x - x1)/4
    jumpx2 = (scol2x - x2)/4
    jumpy1 = (scol1y - y1)/4
    jumpy2 = (scol2y - y2)/4
    abcisse1 = 0
    abcisse2 = 0
    while row < 5:
        evencenter = []
        oddcenter = []
        addabc1 = abcisse1
        addabc2 = abcisse2
        addord1 = ordonnee1
        addord2 = ordonnee2
        while column < 20:
            abc1 = (x1 + addabc1)
            abc2 =(x2 + addabc2)
            ord1 =(y1 + addord1)
            ord2 =(y2 + addord2)
            location1 = (int(abc1), int(ord1))
            location2 = (int(abc2), int(ord2))
            evencenter.append(location1)
            oddcenter.append(location2)
            addabc1 =  addabc1 + distancex1
            addabc2 =  addabc2 - distancex2
            addord1 =  addord1 + distancey1
            addord2 =  addord2 + distancey2
            column += 1
        for loc in evencenter:
            list_centers.append(loc)
        for loc in oddcenter:
            list_centers.append(loc)
        abcisse1 = abcisse1 + jumpx1
        abcisse2 = abcisse2 + jumpx2
        ordonnee1 = ordonnee1 + jumpy1
        ordonnee2 = ordonnee2 + jumpy2
        column = 0
        row += 1
    return list_centers

##creates a list of all coordinates that lie within the circle
##radius of zero = checks only the center
## use a smaller circle and average the RGB, or larger circle and use select_BOC with it
    
def select_circle(centerx, centery, radius):
    global height, width
    lrow = centery - radius
    hrow = centery + radius
    lcolumn = centerx - radius
    rcolumn = centerx + radius
    cursorx = lcolumn
    cursory = lrow
    if lcolumn < 0:
        lcolumn = 0
    if rcolumn > width:
        rcolumn = width
    if lrow < 0:
        lrow = 0
    if hrow > height:
        hrow = height
    circle_list = []
    #list of tupils (x,y) that have the coordinates of the pixels within the circle
    while cursorx <= rcolumn:
        while cursory <= hrow:
            pixel = (cursorx, cursory)
            if (radius**2) >= ((centerx - cursorx)**2 + (centery - cursory)**2):
                circle_list.append(pixel)
            cursory += 1
        cursory = 0
        cursorx += 1
    return circle_list

#average of the intensity in a circle
def aver_ch_intensity_bg(centerx, centery, radius, pixelarray):
    circle = select_circle(centerx, centery, radius)
    listRGB = pixelarray
    intensityList = []
    for pixel in circle:
        colorRGB = listRGB[pixel[1]][pixel[0]]
        intensity = colorRGB[0] + colorRGB[1] + colorRGB[2]
        intensityList.append(intensity)
    size = len(intensityList)
    maximal = max(intensityList)
    sumIntens = 0
    for intens in intensityList:
        sumIntens += intens
    if size == 0:
        size = 1
    averageIntens = sumIntens / size
    return averageIntens, maximal #averageIntens

#Determines intensity of each pixel within a chamber (removes intensities that are too high if the standard deviation is high)
def aver_ch_intensity(centerx, centery, radius, pixelarray, bgintensity):
    circle = select_circle(centerx, centery, radius)
    listRGB = pixelarray
    intensityList = []
    for pixel in circle:
        colorRGB = listRGB[pixel[1]][pixel[0]]
        intensity = colorRGB[0] + colorRGB[1] + colorRGB[2]
        intensityList.append(intensity)
    std = np.std(intensityList)
    if std >= 4 :
        intenscopy = intensityList[:]
        for intens in intenscopy:
            if (bgintensity - intens) <= 60:
                intensityList.remove(intens)
    size = len(intensityList)
    if size < 39: #if size is smaller than half
        return 0
    sumIntens = 0
    for intens in intensityList:
        sumIntens += intens
    if size == 0:
        size = 1
    averageIntens = sumIntens / size
    return averageIntens


#Use the following test function to check the RGB values of specific chambers
def aver_ch_intensity3(centerx, centery, radius, pixelarray):
    circle = select_circle(centerx, centery, radius)
    listRGB = pixelarray
    intensityList = []
    for pixel in circle:
        colorRGB = listRGB[pixel[1]][pixel[0]]
            ###YOU SHOULD ADD A THRESHOLD HERE
        print(colorRGB)
        intensity = colorRGB[0] + colorRGB[1] + colorRGB[2]
        intensityList.append(intensity)
    size = len(intensityList)
    sumIntens = 0
    for intens in intensityList:
        sumIntens += intens
    if size == 0:
        size = 1
    averageIntens = sumIntens / size
    return averageIntens


def draw_centers(listcenters, image, bgloc):
    while True:
        try:
            device = Image.open(file_name)
            break
            #device.load()
        except:
            print("Unable to load Image")
    d = ImageDraw.Draw(device)
    chambern = 0
    d.point(listcenters, fill= "BLACK")
    for center in listcenters:
        d.text(((center[0] - 25), (center[1] - 25)), str(chambern),fill = 50)
        d.ellipse(((center[0] - 5), (center[1] - 5), (center[0] + 5), (center[1] + 5)), fill = 128)
        d.ellipse(((center[0]-bgloc - 2), (center[1]+bgloc - 2), (center[0]-bgloc + 2), (center[1]+bgloc + 2)), fill = 128)
        chambern += 1
    device.show()
    return



def main():
    global height, width
    print("Make sure your device in the image is horizontal")
    pixelarray = load_image(file_name)
    
# =============================================================================
# x1,y1 are the coordinates of the center of the 1st chamber
# x2,y2 are the coordinates of the center of the 21st chamber
# srow1x, srow1y are the coordinates for the last chamber of the 1st row
# srow2x, srow2y are the coordinates for the last chamber of the 2nd row
# scol1x, scol1y are the coordinates of the 9th chamber of the first (left-most) column
# scol2x, scol2y are the coordinates of the 10th chamber of the last (right-most) column
# =============================================================================
    print("Enter the following values separated by a comma (,), in the following order (TIP: save them on a separate file):")
    print("1-centerx1: Type the x-axis value of the center of 1st chamber of the device:")
    print("2-centery1: Type the y-axis value of the center of the 1st chamber of the device:")
    print("3-centerx2: Type the x-axis value of the center of the 21st chamber of the device:(1st chamber of the second row from the right)")
    print("4-centery2: Type the y-axis value of the center of the 21st chamber of the device:(1st chamber of the 2nd row from the right)")
    print("5-srow1x: Type the x-axis value of the center of the 20th chamber of the device:(Last chamber of the 1st row)")
    print("6-srow1y: Type the y-axis value of the center of the 20th chamber of the device:(Last chamber of the 1st row)")
    print("7-scol1x: Type the x-axis value of the center of the 9th chamber of the 1st column (from the left):")
    print("8-scol1y: Type the y-axis value of the center of the 9th chamber of the 1st column (from the left):")
    print("9-srow2x: Type the x-axis value of the center of the 1st chamber of the 2nd row (from the right):")
    print("10-srow2y: Type the y-axis value of the center of the 1st chamber of the 2nd row (from the right):")
    print("11-scol2x: Type the x-axis value of the center of the 10th chamber of the last column (from the left):")
    print("12-scol2y: Type the y-axis value of the center of the 10th chamber of the last column (from the left):")
    print("Template: Centers: centerx1, centery1, centerx2, centery2, srow1x, srow1y, scol1x, scol1y, srow2x, sorw2y, scol2x, scol2y")
    while True:
        try:
            userinput = input("Centers:")
            centers = userinput.split(",")
            listCenters = select_centers(int(centers[0]), int(centers[1]), int(centers[2]), int(centers[3]), int(centers[4]), int(centers[5]), int(centers[6]), int(centers[7]), int(centers[8]), int(centers[9]), int(centers[10]), int(centers[11]))
            break
        except:
            print("Make sure to enter an Integer:")

# =============================================================================
   ## listCenters = select_centers(centerx1, centery1, centerx2, centery2, srow1x, srow1y, scol1x, scol1y, srow2x, sorw2y, scol2x, scol2y)
    #listCenters = select_centers(94, 355, 1266, 400, 1262, 355, 90, 742, 96, 400, 1267, 787) #Snap-164
    #listCenters = select_centers(80,414,1274,468,1269,422,80,806,86,464,1270,854) #Snap-166
    #listCenters = select_centers(58,340,1258,386,1256,338, 54, 736,61,386, 1257,774)#Snap 163
    #listCenters = select_centers(89, 402, 1282, 444, 1279, 400, 96, 788, 94, 448, 1287, 829) #Snap - 165
    #listCenters = select_centers(318,518,1286,566,1282,530,316,830,322,556,1282,870) #Snap - 171
    #listCenters = select_centers(300,429, 1264, 464, 1261, 428,299, 737, 301, 465, 1262, 778) #Snap - 172
    #listCenters = select_centers(234,398,1197,436, 1194, 398,232,706,238,432,1196,742) #Snap - 173
    #listCenters = select_centers(250,400,1204,458,1200,424,250,712,252,436,1210,766) #Snap - 174
    #listCenters = select_centers(269,385,1236,440,1233,404,265,695,273,422,1236,748) #Snap - 175
    #listCenters = select_centers(248,400,1216,456,1214,418,246,710,252,438,1214,766) #Snap - 176
    #listCenters = select_centers(221,378,1189,424,1186,390,218,685,226,414,1190,733) #Snap - 177
    #listCenters = select_centers(225,400,1193,448,1188,410,225,706,229,434,1192,760) #Snap - 178
    #listCenters = select_centers(243,362,1216,418,1214,380,236,670,246,400,1210,722) #Snap - 189
    #listCenters = select_centers(243,362,1216,418,1214,380,236,670,246,400,1210,722) #Snap - 189
    #bgloc: choose the distance of the bg area from the center of the droplet
    while True:
        try:
            print("Background samples are used to normalize the intensity with the background")
            print("Insert the distance between the background sample and the center of the chamber. Type 0 or 12 for default (12 pixels).")
            bgloc = int(input("Background sample distance from center of the chamber:"))
            break
        except:
            print("Make sure to enter an Integer:")
    while True:
        try:
            bgradius = int(input("Background sample radius in pixels (2 pixels is recommended):"))
            break
        except:
            print("Make sure to enter an Integer:")
    while True:
        try:
            chamberradius = int(input("Chamber sample radius in pixels (5 pixels is recommended):"))
            break
        except:
            print("Make sure to enter an Integer:")
    if bgloc == 0:    
        bgloc = 12
    chambern = 0
    listavbg = []
    #This part is not very efficient but NECESSARY:
    for center in listCenters:
        bgintensity, maximal = aver_ch_intensity_bg((center[0] - bgloc ), (center[1] + bgloc), bgradius, pixelarray)
        listavbg.append(maximal)
    bgmean = np.mean(listavbg) #average maximal background intensity
    for center in listCenters:
        bgintensity, maximal = aver_ch_intensity_bg((center[0] - bgloc ), (center[1] + bgloc), bgradius, pixelarray)
        coefficient = 2 - float(maximal/bgmean) #variation of the bg of the droplet from the mean
        intensity1 = aver_ch_intensity(center[0], center[1], chamberradius, pixelarray, maximal)
        intensity = float(intensity1) * coefficient
        if intensity != 0:
            print(str(chambern) +" "+ str(center) + " " + str( intensity) + " " + str(intensity1)+ " " + str(maximal) + " " + str(coefficient))#Intensity
        chambern += 1

# #     intensity3 = aver_ch_intensity3(listCenters[70][0], listCenters[70][1], 10, pixelarray)
    draw_centers(listCenters, file_name, bgloc)


main()
