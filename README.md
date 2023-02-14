# gb-dl-checker

Forked from https://gist.github.com/shlubbert/56d4865d1256a3d1a2eeed8c23df7bcb by shlubbert

Checks Giant Bomb downloads folders for the presence of all show episodes as well as checking for the highest quality available.

If videos are found they are re-named to match our naming conventions. Missing episodes or episodes with lower quality will
be flagged in the output log.

Loading only the API dump will search and rename files across multiple shows but will NOT be able to tell you if you have all of the episodes of a specific show.

Specifying a Show CSV AND the API dump will limit the analysis to just that show but will be able to report whether you have the full show or are missing episodes.

## USAGE
- Run gb-dl-checker.py (or exe)
> **Videos Folder:**
Choose your downloads folder (either show specific or high-level folder for multiple shows)


> **API CSV:**
Choose the location of the API dump CSV file
- If you do not have this, download it from the [releases page](https://github.com/muffinsAKA/gb-dl-checker/releases/tag/API-Dump-1.0) or export a CSV copy of the API dump here https://docs.google.com/spreadsheets/d/1MPAHk9RS3yMExC7iX_eM_2W8ljyUXy-nBurjZ2fdU9s/edit Open the spreadsheet and click on File > Download > Comma separated value (.csv)


> **Show CSV:** Tells the tool how many episodes are expected for the show and to alert if any are missing.
- If you do not have this, export a CSV of the Giant Bomb Archive sheet (found in #links-and-resources on Discord) under the show-specific page. Open the spreadsheet and navigate to your show's page. Click on File > Download > Comma separated value (.csv)

> **Upload CSV Output Directory:** Where the CSV(s) that will be used to batch upload to Archive.org will be saved/named.

> **Split uploads into how many CSVs?:**
This will let you split your videos across multiple CSVs for simultaneous uploads. We recommend this if you have good upload speed because Archive.org doesn't go very fast. A setting of ``1`` will not split them.

> **Which collection?:** This chooses which collection on Archive.org to upload to.  Admins can use `giant-bomb-archive` but not everyone will be admins. Regular uploaders will use a `opensource_movies` and will have their uploads moved into a collection later by Archive.org admins. If you don't know if you're an admin you probably aren't so stick with `opensource_movies`

- Hit 'Submit' and pray

After scanning and renaming has completed a log file will be output as `LogFile.txt` to the same directory as the exe

## Requirements (Python only)
PySimpleGUI

``pip install pysimplegui``

## TROUBLESHOOTING

- Both Chrome and Windows will flag the .exe for various reasons. It's safe. the source code is here to look at. You can install Python and run the .py file  through the command line if you're wary.

- If you run into permissions errors make sure you're running the app somewhere your account has permissions. That means stay out of system folders! Just use the 'ol desktop preferably

- If you get any errors about renaming or any incomprehensible errors at all it is probably related to the API dump. We've cleaned it up as much as possible but there still may be some weird filename conflicts here and there. Let us know and we'll try to update it.

## Screenshots
![gb-dl-checker-v1.5](https://user-images.githubusercontent.com/18468361/217961391-0954bd30-a61f-4e64-8ee1-370512c18d7c.png)
