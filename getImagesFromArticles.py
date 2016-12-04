#!/usr/local/bin/python3

# Takes a json file of info about pages under some set of categories
# and uses the page title to retrieve info about the images on the page


import urllib.request
from urllib.request import urlopen
import urllib.parse
import json
from pprint import pprint
import sys
import codecs
import datetime
import requests


# get json file that lists all the articles in the subcategories
#get file of subcats under supercategory
args = str(sys.argv)
supercat =  str(sys.argv[1])
#pprint ("ARG1=" + args[1])
sourcefile = "titles_in_subcategories_of_" + supercat + ".txt"
#pprint ("sourcefile=" + sourcefile + "\n")
# read the article titles
f = open(sourcefile, 'r')
articlestxt = f.read()
articles = json.loads(articlestxt)

# images we don't care about
exclusionList= ["File:Commons-logo.svg","File:Folder Hexagonal Icon.svg","File:Portal-puzzle.svg","File:Folder_Hexagonal_Icon.svg","File:Wiktionary-logo.svg","File:Merge-arrow.svg","File:Mergefrom.svg","File:Lock-green.svg","File:Ambox important.svg","File:Wiki letter w.svg","File:Edit-clear.svg","File:Text document with red question mark.svg","File:People icon.svg","File:Book Hexagonal Icon.svg","File:Wiki letter w cropped.svg","File:Wikiquote-logo.svg","File:The Earth seen from Apollo 17 with transparent background.png","File:Wiktionary-logo-v2.svg","File:Emblem-money.svg",
"File:Flag of South Africa.svg","File:Flag of Austria.svg","File:Wikisource-logo.svg", "File:Emojiu1f30f.svg","File:Nuvola apps package favorite.svg","File:Countries by GDP (PPP) Per Capita in 2015.svg","File:Water cycle.png", "File:Office-book.svg","File:Merge-arrows.svg","File:Papapishu-Lab-icon-6.svg","File:Symbol template class.svg","File:Flag of the Czech Republic.svg","File:Scientist.svg","File:Flag of Denmark.svg","File:Flag of Australia.svg","File:Flag of Europe.svg","File:Flag of France.svg","File:Handshake (Workshop Cologne '06).jpeg","File:Atmosphere composition diagram-en.svg","File:Flag of Spain.svg","File:P vip.svg","File:Flag of Brazil.svg","File:Image of Triangle Shirtwaist Factory fire on March 25 - 1911.jpg","File:Flag of the Netherlands.svg","File:2000 Year Temperature Comparison.png","File:Flag of Romania.svg","File:Flag of Belgium (civil).svg","File:Flag of Russia.svg","File:Diatoms through the microscope.jpg","File:Wikiversity-logo.svg","File:Science-symbol-2.svg","File:Flag of the United Kingdom.svg","File:Flag of Canada.svg","File:Staphylococcus aureus VISA 2.jpg","File:Flag of Italy.svg","File:Pepsi in India.jpg","File:A coloured voting box.svg","File:Phil Radford.jpg","File:Wikinews-logo.svg","File:Complex-adaptive-system.jpg","File:Padlock-silver.svg","File:Flag of Japan.svg","File:Flag of Germany.svg","File:AirPollutionSource.jpg","File:Wikispecies-logo.svg","File:Esculaap4.svg","File:Nuvola apps kfig.svg","File:Wind-turbine-icon.svg","File:Paw (Animal Rights symbol).svg","File:Leaf.svg","File:ShipTracks MODIS 2005may11.jpg",
"File:Ambox globe content.svg","File:Symbol support vote.svg","File:Symbol book class2.svg", "File:Unbalanced scales.svg","File:Flag of the United States.svg","File:Ambox wikify.svg"
]

# Create json for images
imageArray = []
finaljson = {"supercat" : supercat, "date": str(datetime.datetime.now())}

#go through articles grabbing images and looking each one up
ctr = 0
pages = articles["pages"]
# #pprint(pages)
for article in pages:
	##pprint(article)
	tit = article["title"].replace(" ","_")
	#print("newart: " + tit)
	# get images on an article page
	query="https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&titles=" + tit + "&imlimit=100"
	#pprint("After query")
	try:
		ctr = ctr + 1;
		# query the api for the list of images for this article
	
		resp = requests.get(query)
		results = resp.json()
		#reader = codecs.getreader("utf-8") # turn it from bytes to string
		#iresults = json.load(reader(iresponse))
		# get the stupid magic key aaarrrggghhh

		# Now get the pageid that WP uses for as a key
		# for the list of images. That number is unknown to us.
		# Aaaarrrggghhh
		qlist = results["query"]["pages"]
		keylist = qlist.keys()
		for keys in keylist:
			pageID = str(keys)
		# get the list of images, if any
		if 'images' in results["query"]["pages"][pageID]:
			images = results["query"]["pages"][pageID]["images"]
			##pprint(images)
			# go through the images getting the info about each
			##pprint("good query: " + query)
			for image in images:
				# get the data for the image
				if "title" in image:
					ititle = image["title"]
					imgtitle = ititle.replace(" ","_")
					#imgtitle = imgtitle.encode('utf-8') 
					pprint("imgtitle=" + imgtitle)
					iquery = "https://en.wikipedia.org/w/api.php?action=query&titles=" + imgtitle + "&prop=imageinfo&iiprop=parsedcomment%7Ccomment%7Curl%7Cmime%7Cmediatype%7Csize%7Ccommonmetadata%7Cuser&format=json&iiurlwidth=150"
				
					
					
					# -- thanks for the help wrangling unicode, Win Treese!
					r = requests.get(iquery)
					iresults = r.json()
					
					# get the stupid magic key aaarrrggghhh
					iqlist = iresults["query"]["pages"]
					ikeylist = iqlist.keys()
					for ikeys in ikeylist:
						ipageID = str(ikeys)
						#pprint("ipageid=" + ipageID)
					info = iresults["query"]["pages"][ipageID]["imageinfo"][0]
					##pprint(info)
					imagetit = iresults["query"]["pages"][ipageID]["title"]
					#pprint("TIT: " + imagetit)
					if  imagetit not in exclusionList:
						#pprint("URL: " + info["url"])
						# create json entry for one image
						oneimage = {}
						oneimage["subcat"]=article["subcat"]
						oneimage["parent"]=article["supercat"]
						oneimage["title"]=imagetit
					
						if "user" in info:
							oneimage["user"]=info["user"]
						
						extent = [] # build extent sublist
						if "size" in info:
							extent.append( {"size" : info["size"], "units" : "bytes"})
						if "width" in info:
							extent.append( {"width" : info["width"], "units" : "pixels"})
						if "height" in info:
							extent.append( {"height" : info["height"], "units" : "pixels"})
						oneimage["extent"] = extent
					
						thumb = {} # build thumbnail sublist
						if "thumburl" in info:
							thumb["thumburl"] = info["thumburl"]
						if "thumbwidth" in info:
							thumb["thumbwidth"] = info["thumbwidth"]
						if "thumbheight" in info:
							thumb["thumbheight"] =  info["thumbheight"]
						oneimage["thumbnail"] = thumb
					
						if "url" in info:
							oneimage["url"]= info["url"]
						if "descriptionurl" in info:
							oneimage["descriptionUrl"]=info["descriptionurl"]
						oneimage["identifiers"]=[{"pageID" : ipageID}]
						if "mime" in info:
							oneimage["mime"]=info["mime"]
						if "mediatype" in info:
							oneimage["mediatype"]=info["mediatype"]
						if "comment" in info:
							comment= info["comment"]
							if len(comment) > 2:
								p1 = comment.find("Description:")
								if p1 > -1:
									p2 = comment.find("\n", p1+1)
									desc = comment[p1 + 12 : p2 -1]
									oneimage["description"] = desc
						#add this to the master json
						imageArray.append(oneimage)
			
		finaljson["images"] = imageArray;					
		outfilename = "images_in_subcategories_of_" + supercat + ".txt"
		with open(outfilename, 'w') as outfile:
			json.dump(finaljson, outfile)
						

		
	except urllib.error.URLError as e:
			#pprint(e)
			pprint( 'ERROR: ' +  e.reason + " query: " + query)

# ---- NOTES: some sample api urls
#
# 	#this works to get the images on the page:
# 	https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&imlimit=5&titles=Creative_Energy_Homes&imlimit=100
# 	
# 	# this gets info about each images
# 	http://en.wikipedia.org/w/api.php?action=query&titles=File:Portal-puzzle.svg&prop=imageinfo&iiprop=url&format=json
# 	
# 	#this works too
# 	https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&titles=Creative_Energy_Homes&imlimit=100
