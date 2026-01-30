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
