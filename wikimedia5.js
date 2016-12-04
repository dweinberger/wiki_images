// global
window.gImageArray = new Array();
window.cats = new Array();
window.pages = new Array();

//

// ----- Start with category search
function getSubCats(){
	// write out a file with the subcategories
	// get search term
	
	if ($("#subcatbtn").text() == "Get subcategories"){
		$("#subcatbtn").text("Working...");
	}
	else{
		alert("Refresh page to re-run");
		return;
	}
	
	var term = $("#term").val();
	
	var allcats = getAllCats(term,"");
	
		
	$("#response1").text("File written");
	$("#subcatbtn").text("Done. Refresh to re-run");
	
	$("#step2").slideDown();
	
	
}

// -------------- get all the subcategories
function getAllCats(term,cmcontinue){
		
		var query = "https://en.wikipedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtype=subcat&cmtitle=Category:" + term;
		if ( (cmcontinue!=="") && (cmcontinue !== undefined)){
			query += "&cmcontinue=" + cmcontinue;							//"&cmcontinue=subcat|3f372b49432937433d43335703422f4151374943413f2f414d273d043f372b49432937433d433357012b018f7a8f1d|17381965"
		}
	// 	var maxcatpages = 3;
// 		var catpagectr = 0;
		// get the subcats
		 $.ajax({
			url: query,
			dataType: "JSONP",
			async: false,
			success: function (json){
				var j = json;
				
				var catarray = json['query']['categorymembers'];
				var newcat;
				for (var i=0; i < catarray.length; i++){
					newcat = catarray[i]['title'];
				 	cats.push(newcat);
				 	
				 }
				 if (json['continue']){
				 	if (json['continue']['cmcontinue']){
				 		cmcontinue = json['continue']['cmcontinue'];
				 	}
				 	else {cmcontinue = "";
				 		$("#subcatbtn").text("Done.");
				 	}
				 }
				 else {cmcontinue = "";
				 	$("#subcatbtn").text("Done.");
				 	}
				if (cmcontinue != ""){
					getAllCats(term,cmcontinue);
				}
				if (cmcontinue == ""){
				
					$.ajax({
					type: "POST",
					async: false,
					data: {"term" : term, "names" : cats},
					url: "buildnamefile.php", 
					success: function(data) {
							$("#results").html($("#results").html() + "<br>wrote file");
						   },
						  error: function (e){
							if (e.statusText !== "OK"){
								alert("Failed to read recent files: " . e.statusText, "ERROR");
								//statusUpdate("Failed to read recent files: " . e.statusTex);
							}
							}
					
					});

				} // if cmcontinue == ""
			}
		});
	
	
	return cats;

}

// --------------- get all the pages in each of the categories
function getPages(){

		// get the original super-category
		var term = $("#term").val();
		var cat = term.replace(/ /g, '_');

	// read the existing file of subcats (do not add localhost/etc.)
	var fname = "wikipedia_subcats_of_" + cat + ".txt";
	var catstring = "";
	

	$.ajax({
		  url: fname,
		  //async: false,
		  success: function(txt){
		  	catstring = txt.split("\n");
		  	// send array of subcats out to get pages
		  	writeOutPages(catstring,fname)
		  		
		  	},
		  error: function(e){
		  	alert("Failed to read \n" + fname + "\n" + e.statusText);
			}
	});
	
}	

function writeOutPages(subcats){
	// for each of the subcats, gets the pages and writes to a file
	
	// get the original super-category
		var term = $("#term").val();
		var cat = term.replace(/ /g, '_');
	
		for (var j = 0 ; j < subcats.length; j++){
			// get pages for a category
			var query = "https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&format=json&cmtitle=Category:" + subcats[j];	
			// Get this subcat's pages
			 $.ajax({
				url: query,
				//async: false,
				dataType: "JSONP",
				data: {"subcat" : subcats[j]}, 
				success: function (json){
					// write out this subcat's pages
					var subcatj = subcats[j];
					var pagesj = json;
					$.ajax({
						type: "POST",
						async: false,
						data: {"subcategory" : subcatj, "json" : pagesj, "supercat" : cat},
						url: "buildpagefile.php", 
						success: function(data) {
								$("#response2").html("Wrote file for subcat: " + subcatj);
							   },
						 error: function (e){
								if (e.statusText !== "OK"){
									alert("Failed to read pages from subcat: " + subcat[j] + ": " + e.statusText, "ERROR");
								}
							}
							
					
					});
					}
					
			});
		}

}
	
	
function unused(){
	
	
	//localhost/greenCommons/wikimedia/ wikipedia_subcats_of_ENVIRONMENTAL_SCIENCE.txt
	
		var query = "https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&imlimit=100&titles=" + cat;
		if ( (1==2) && (cmcontinue!=="") && (cmcontinue !== undefined)){
			query += "&cmcontinue=" + cmcontinue;	
		}						
		 $.ajax({
			url: query,
			dataType: "JSONP",
			success: function (json){
				var j = json;
				
				var catarray = json['query']['categorymembers'];
				var newcat;
				for (var i=0; i < catarray.length; i++){
					newcat = catarray[i]['title'];
				 	cats.push(newcat);
				 	
				 }
				 if (json['continue']){
				 	if (json['continue']['cmcontinue']){
				 		cmcontinue = json['continue']['cmcontinue'];
				 	}
				 	else {cmcontinue = "";}
				 }
				 else {cmcontinue = "";}
				if (cmcontinue != ""){
					getPagesInCategory(cat,cmcontinue);
				}
			},
			error: function(e){
				alert(e.statusText);
			}
		});
	
	
	return cats;

}


// ---------------- build a file of names of the images
function getNames(nextpage){
	// generate list of image names
	
	// ----- Start with category search

	// get search term
	var term = $("#term").val();
	
	var allcats = getAllCats(term,"");

	// ------- now get all the pages in all the categories
	//			and save to a file
	for (var i=0; i < allcats.length; i++){

		
		getPagesInCategory(allcats[i], "");
		
	}
		
		
	// 
// 	if ((nextpage) && (nextpage != "START")){
// 		url = url + "&imcontinue=" + nextpage;
// 	}
// 	
// 	$("#results").html($("#results").html() + "<br>" + url);
// 	
	//https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Environmental_science
 
return

 
	 var masterArray = new Array();
 	var ctr = 0;
 $.ajax({
  	url: url,
  	dataType: "JSONP",
	success: function (json){
		ctr++;
		// the json sometimes has a magic number (a pageid) right below the "pages" fold
		// and that number only sometimes is expressed in the top level of 
		// the json, and then it's the first part of a string. But it isn't
		// always there. That number is the keyword below "pages" and is the
		// parent of "images", so we need it. But we don't know it.
		// So, convert the pages part of the json into an array and use [0] 
		// instead of the unreliable magic number.  
		var imageParent = Object.values( json['query']['pages'])[0];
		var images = imageParent['images']; // don't know why we need this
		var ct = images.length;
		// get the info for paging...a tag in imcontinue you use to
		// tell it where to begin next time.
		if ( (json['continue']) && (json['continue']['imcontinue'])){
			var nextpg = json['continue']['imcontinue'];
		}
		
		masterArray.length = 0;
		// Get the names
		for (var i=0; i < ct; i++){
			var rawtitle = images[i]["title"];
			var title = rawtitle.replace(/ /g, '_');
			masterArray.push(title);
		}
		//$("#results").html($("#results").html() + "<li>") + masterArray.length + "</li>";
		// write out list of files
		$.ajax({
			type: "POST",
			data: {"term" : term, "names" : masterArray},
            url: "buildnamefile.php", 
            success: function(data) {
                 	$("#results").html($("#results").html() + "<br>wrote file");
                   },
                  error: function (e){
                  	if (e.statusText !== "OK"){
                  		alert("Failed to read recent files: " . e.statusText, "ERROR");
                  		//statusUpdate("Failed to read recent files: " . e.statusTex);
                  	}
                  	}
		
		
		});
		// recurse if there's a nextpage
		// and arbitrarily stop at 7500 images
		if ((nextpg) && (ctr < 75)){
			getNames(nextpg);
		}
		
	}
    
  
  });
  
 
}

function getImageInfo(title){
	
	// iiurlwidth = width of thumbnail. Without this, no thumbnail is returned.
	// 				Also requires that url be set in iiprop.
	// To page through, get the imcontinue value and 
	// add it to the query thusly, for example:
	//	imcontinue=26700|Brain,_G_Reisch.png
	
		imageUrl = "https://en.wikipedia.org/w/api.php?action=query&titles=" + title + "&prop=imageinfo&iiprop=parsedcomment%7Ccomment%7Curl%7Cmime%7Csize%7Ccommonmetadata&format=json&iiurlwidth=150";
		
	$.get( imageUrl, function( j ) {
		
		// get img info
		var imgrec = new Array();
		var imginfoparent =  Object.values( j['query']['pages'])[0];
		var img = imginfoparent['imageinfo'][0];
		imgrec["description"] = img['parsedcomment'];
		imgrec['mime'] = img['mime'];
		//imgrec['size'] - img['size'];
		imgrec['thumbsize']= new Array({"thumbheight" :  img['thumbheight'], "thumbwidth" : img['thumbwidth']}) ;
		imgrec['thumburl']=img['thumburl'];
		imgrec['url'] = img['url'];
		imgrec['extent']= new Array({"width" :  img['width'], "height" : img['height'], "filesize" : img['size']}) ;
		gImageArray.push(imgrec);
		});


	
	return imginfo;
	
	
}