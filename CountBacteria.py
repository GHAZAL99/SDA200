# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 11:27:50 2019

@author: Nabil Ghazal
"""
import os
import math
from PIL import Image, ImageDraw
height = 0  #height of the image
width = 0   #width of the image
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

def color_pixel(listcenters, coloredpath, file_name):
    while True:
        try:
            device = Image.open(file_name)
            break
            #device.load()
        except:
            print("Unable to load Image")
    d = ImageDraw.Draw(device)
    d.point(listcenters, fill= "RED")
    #device.show()
    device.save(coloredpath)
    #Insert save pathx
    return
def main():
    userinput = ""
    usertarget = ""
    fileList = []
    listBac = []
    filenum = 0
    while True:
        try:
            userinput = input("Directory:")
            usertarget = input("Target directory:")
            fileList = os.listdir(userinput)
            break
        except:
            print("Make sure to enter an Integer:")
    for name in fileList:
        bactpixel = []
        count = 0
        temp = "nab\z"
        x = str(userinput) + temp[3]   
        y = str(usertarget) + temp[3]
        pathfile = x + str(name)
        coloredpath = y + "colored" + str(filenum) + ".jpg"  
        pixelarray = load_image(pathfile)
        for row in pixelarray:
            for col in row:
                
                if int(col[0]) < 188 and int(col[0]) > 60 and int(col[1]) < 188 and int(col[1]) > 60 and int(col[2]) < 188 and int(col[2]) > 60:
               #if col < 200 :
                    count =  count +1
                    bactpixel.append((row.index(col),pixelarray.index(row)))
        color_pixel(bactpixel, coloredpath,pathfile)
        diameter = 15 #could be 14
        count = count / math.pi / (diameter / 2)**2
        listBac.append(count)
        filenum+=1
    for number in listBac:
        print(number)
    
main()