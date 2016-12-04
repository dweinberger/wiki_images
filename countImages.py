#!/usr/local/bin/python3

# Counts the images in a file of images from Wikipedia categories
# Useful to find the Wikipedia images so we can exclude them


import json
from pprint import pprint
import sys
#from collections import Counter



#get file of images 
args = str(sys.argv)
supercat =  str(sys.argv[1])
#pprint ("ARG1=" + args[1])
sourcefile = "images_in_subcategories_of_" + supercat + ".txt"

# create arrays
titleArray = {}

# read the article titles
f = open(sourcefile, 'r')
imagestxt = f.read()
images = json.loads(imagestxt)
allimages = images['images']

i=0
numberofimages = len(allimages)
pprint("number of images: " + str(numberofimages));
for thisimage in allimages[i: numberofimages - 2]:
	
	title = thisimage["title"]
	if title not in titleArray:
		titleArray[title] = 1
	print("TITLE: " + title)
	# look through the rest of the list
	for targimage in allimages[i + 1: numberofimages - 1]:
		targtitle = targimage["title"]
		if targtitle == title:
			titleArray[title] = titleArray[title] + 1
	

# write the file -- csv so I don't have to learn how to sort json	
outfilename = 'imagecount_for_' + supercat + '.csv'
f= open(outfilename, 'a')
for key, value in titleArray.items():
	key2 = key.replace("'", r"\'")
	key2 = key2.replace('"', r'\"')
	key2 = '"' + key2 + '"'
	f.write(key2)
	f.write("," )
	f.write( str(value) + "\n")
f.close()
		
	

