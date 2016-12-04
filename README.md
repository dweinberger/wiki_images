# Wikipedia Image Scraper

Give it an official Wikipedia (WP) category and it will find all the images on the articles within that category and within categories nested one level below it. So, if the category is Recipes, and if Recipes has two subcategories, Raw and Cooked, it will find the images on the pages listed under those two categories. It delves no deeper, however, and thus does not find pages that are classified as Vegetables  under the Cooked or Raw categories.

The way it does this is ridiculous.

## Part 1

First, you use the Web page WikipediaSubcats.html to generate a text file that contains all the subcategories of the main category you give it. It writes these out as "wikipedia_subcats_of_SUPERCAT.txt" where SUPERCAT = the top level category.  This category name should have underscores instead of spaces, as in "Environmental_science".

Presumably you'll run this from localhost because its point is to generate a saved file. It uses wikimedia5.js, which calls buildanamefile.php. To get past the cross-platform issue, it expects you to install  and activate a particular Chrome extension: [https://chrome.google.com/webstore/category/extensions?hl=en-US](https://chrome.google.com/webstore/category/extensions?hl=en-US).

You'll also need a copy of jquery, all in that same flat folder.

Yes, this is a convoluted way of generating a text file. I should rewrite it as a Python script, which would make it my second Python script. In a new version, the category browsing function would recurse to discover all the generations of children under the starting category.


## Part 2

Then you switch to Python. Why? Because I couldn't get MAMP's PHP to pass the security gate of the WP API. Python does it like a charm. Unfortunately, I've never written anything in Python before, so try not to laugh.

Why in separate scripts? Because I've never written anything in Python before, and this seemed like a better way to contain the damage. Ok?

So, launch your terminal and change the directory to where the "wikipedia_subcats_of_SUPERCAT.txt" file is (except with the real name of the supercategory). Then run:

``` python  getArticlesFromCategories.py Supercat```

where Supercat  is the top level category, as in:

``` python  getArticlesFromCategories.py Environmental_science```

This will create a  JSON file that consists of the articles in WP under each of the categories listed in wikipedia_subcats_of_SUPERCAT.txt. For each article it records the article title, the subcategory it's under, and, just to be safe, the supercat of the whole damn thing. This file's name will be, in our example: "titles_in_subcategories_of_Environmental_science.txt"

## Part 3

Now you run Python again. This time it's getImagesFromArticles.py, with the main category as an argument, as in:

```getImagesFromArticles.py Environmental_science```

 It will read the list of article titles, scrape each for its images, and create a JSON file of them. It excludes at least some of the more obvious generic Wikipedia images, such as the logo and navigational images. (You can expand that list by adding to the exclusionList in the Python script.

 This will generate a JSON file with a title like "images_in_subcategories_of_Environmental_science.txt"

 It's just that simple!

 ## License, etc.

 This is released under an MIT open source license. Do whatever the hell you want with it, although I strongly advise you to do nothing with it because it is a godawful, ridiculous, poorly constructed piece of code mainly constructed of pieces copy and pasted from Stackoverflow and other sources.

 David Weinberger
 Dec. 3, 2016
 david@weinberger.org
