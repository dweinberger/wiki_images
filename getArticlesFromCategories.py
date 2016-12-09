#!/usr/local/bin/python3

import urllib.request
from urllib.request import urlopen
import json
from pprint import pprint
import sys
import codecs
import datetime


#get file of subcats under supercategory
args = str(sys.argv)
supercat =  str(sys.argv[1])
print ("ARG1=" + args[1])
filename = "wikipedia_subcats_of_" + supercat + ".txt"
print ("filename=" + filename + "\n")

f = open(filename, 'r')
subcatstxt = f.read()
#turn subcats into a list
subcatstxt = subcatstxt.replace(" ","_")
subcats = subcatstxt.splitlines()

# Create json for pagetitles
pageTitles = []
finaljson = {"supercat" : supercat, "date": str(datetime.datetime.now())}


# For each subcat, get all the pages
for cat in subcats:
	print( "=======" + str(ctr) + ": " + cat)
	#titlesfile.write("-------- " + cat + " -------------");
	ctr = ctr + 1
	ddone = False
	cont = ""
	# get all pages for one cat
	while not ddone:
		query = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&format=json&cmtitle=" + cat
		# if there's a continuation page from last time, start there
		if not (cont==""):
			query = query + "&cmcontinue=" + cont
		
		# request the pages for this subcat
		#request = urllib.request.Request(query)
	
		try:
			# query the api for the list of pages for this subcat
			with urllib.request.urlopen(query) as response:
				reader = codecs.getreader("utf-8") # turn it from bytes to string
				data = json.load(reader(response))
				# get array of pages
				pages = data["query"]["categorymembers"]
				#pprint(pages)
		
			# go through the array of pages and build json
			alltitles = ""
			for page in pages:
				# get a page
				pagename = page['title']
				print( "TITLE: " + pagename)
				onepage = {}
				onepage['title'] = pagename
				onepage['subcat'] = cat
				onepage['supercat'] = supercat
				# add this to main json
				pageTitles.append(onepage)
				# pgs = iter(pageTitles)
# 				next(pgs)['page'] = onepage
			# is there a "continue" item for this api return?
			cont = "no continue"
			if 'continue' in data:
				if "cmcontinue" in data["continue"]:
					print ("continue: " +  data["continue"]["cmcontinue"])
					cont = data["continue"]["cmcontinue"]
				else:
					cont = ""
					ddone = True
			else:
				cont = ""
				ddone = True
			
			
		except urllib.error.URLError as e:
			print( 'ERROR: ' +  e.reason)
			
	# add page array to the json
	finaljson["pages"]=pageTitles
	

outfilename = "titles_in_subcategories_of_" + supercat + ".txt"
with open(outfilename, 'w') as outfile:
    json.dump(finaljson, outfile)
