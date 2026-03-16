# PythonHelpers
A couple scripts written in python that have helped with some basic tasks in my day to day work.

# bgremover
Used for taking any picture format and converting it both into a png file aswell as removing the background. Script is configurable to change the background's color, uses rgb codes and with the allows for a gradient to be removed rather than just a single color. This can also be configured to allow zero tolerance by change the signs to an '=='.

# CSVCleaner
Kind of hard coded right now but can be configured but allows a user to input multiple similar .csv files and merge it into a singular csv document. This was used when converting a webpage from wordpress that output multiple CSV files that all served the same purpose and contained different data. In future I will also configure this to output database files so that it is more usable for other purposes.

# WebFixer
Used in tandem with CSVCleaner. Using a service like simplystatic to download a static html version of your wordpress website, this attempts to fix a webpage that cannot find styling pages and files to work as a standard html/javascript website rather than relying on PHP. If the folder structure is sensical than this script works great otherwise manual configuration of the site may still be necessary.

# Upscaler
Uses pillow scaling to attempt to increase the resolution of a target image. This is a modification of the BGRemover script with the BGRemover content removed. This isn't better than most AI scalers but it serves its purpose especially for higher res images.

# cleaner
This allows a user to input a text file and simply extract the names of a variable aswell as the data that is tied to them. In my case I used this for EU4 modding by extracting what data type each variable is from the wikipage and removing the headers above each one. You can find input and output examples in their respective folders.

# Eu4CCGen
Generates an html document that lists 10,000 unused RGB codes from a BMP file. It only lists 10,000 to limit file size and time to open. Provides and HTML document with a built in checklist that allows you to easily track which color codes you have used as you utilize the tool aswell as providing an example color splotch.

# HMapGen
Generates an updated heightmap file from a provided file and attempts to translate your provinces.bmp file to a heightmap to remove a layer of busy work that comes with map modding. Currently this only works with matching file resolutions however either this script will be updated or another will be made in order to account for maps that have updated resolutions.

# EU4PHRecolor
Recolors a provide province map to use unused rgb codes based off a provided provinces.bmp file. This allows the user to quickly translate images generated on websites like fantasy map generator to something more eu4 safe for modding.

# EU4ChievmentsUp - (**W.I.P**)
Allows an eu4 player to generate a list of Eu4 achievments based off their profile and organizes it in a way so that a player can filter by country and conduct a run from a starting country with a list of endgoals and tips to accomplish said achievments. This script currently requires to user to download the EU4 wiki page (Go [Here]([https://eu4.paradoxwikis.com/Achievements]) -> Right-Click -> save-as) this also requires to user to have their steam api key handy as this parses steam servers to find achievments you have already completed. All of the required fields are at the top of the script in all caps and can be copy pasted. This script is entirely hosted locally but if you are worried feel free to copy paste the code into your own textfile to see what its doing. Currently the script is broken with its regex and is going to require tweaking.
