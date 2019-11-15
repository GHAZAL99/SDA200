## Protocol for counting bacteria in chambers:
*Pictures of the chambers were taken using a bright field microscope,using a 200x magnification.*
#### Cropping the images:
To get an accurate count of the bacteria, it is best to cop ou the parts of the image that do not contain the bacteria, especially the parts that have RGB values close to the bacterial ones. This cropping can be done using basic software such as the "Microsoft Paint".

#### Finding the right RGB range and the diameter:
1.For this part, I used ImageJ: <br />
Open the image, and hover with your mouse on the bacteria. You will see the RGB values of the pixels ou hover over under the ImageJ tool bar. PUUUUUUUUUT IMAGGGGGE
2. Compare the RGB values of the bacteria with different background pixels, that have different shades.
3. Write down for each color (red, green, blue) the largest range of values that would include the bacterial pixel RGB values, without including the background RGB values.
4. Determine the diameter of one bacterium using the measure tool, and take note of it.

#### Setting up the program:
1. Open the "CountBacteria.py" file.
2. Go to the main() function and find :
>**(line 79)** <br />if int(col[0]) < 188 and int(col[0]) > 60 and int(col[1]) < 188 and int(col[1]) > 60 and int(col[2]) < 188 and int(col[2]) > 60:

Replace the numbers presents in the __if statement__ with the numbers the numbers of the RGB range that you have determined in the previous section.
*Note: <br />
red = col[0] <br />
green = col[1] <br />
blue = col[2]*

3. Go to the line that has **"diameter" (line 84)**, and replace the value with the value that you have found in the previous section.

#### Running the program:
1. Put all the cropped images in a new file. (**Only images should be present in the file**).
2. Create another file where you would like to store the images that show you which pixels were detected.
3. Run the program: <br />
a. When prompted, insert the path of the first file created:
b. When prompted a second time, insert the path of the second file you created.
