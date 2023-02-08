# gb-dl-checker

Forked from https://gist.github.com/shlubbert/56d4865d1256a3d1a2eeed8c23df7bcb by shlubbert

Checks Giant Bomb downloads folders for the presence of all show episodes as well as checking for the highest quality available.

If videos are found they are re-named based to match our naming conventions. Missing episodes or episodes with lower quality will
be flagged in the output log.

Loading only the API dump will search and rename files across multiple shows. 

Specifying a Show CSV as well as the API dump will limit the analysis to just that show.

## USAGE
- Run gb-dl-checker.py (or exe)
- Choose your downloads folder (either show specific or high-level folder for multiple shows)
- (Required) Choose the location of the API dump CSV file
    - If you do not have this, export a CSV copy of the API dump https://docs.google.com/spreadsheets/d/1MPAHk9RS3yMExC7iX_eM_2W8ljyUXy-nBurjZ2fdU9s/edit)
- (Optional) If only checking a singular show, you can choose the location of the show CSV. This generally isn't necessary but just in case you need to limit the range!
    - If you do not have this, export a CSV of the Giant Bomb Archive sheet under the show-specific page)
- Hit 'Submit' and pray?

## TROUBLESHOOTING

- Both Chrome and Windows will flag the .exe for various reasons. It's safe. the source code is here to look at. You can install Python and run the .py file  through the command line if you're wary.

- If you run into permissions errors make sure you're running the app somewhere your account has permissions. That means stay out of system folders! Just use the 'ol desktop preferably

- If you get any errors about renaming or any incomprehensible errors at all it is probably related to the API dump. We've cleaned it up as much as possible but there still may be some weird filename conflicts here and there. Let us know and we'll try to update it.


![gb-dl-checker-v0.4](https://user-images.githubusercontent.com/18468361/217410976-8ebb3629-ddf1-495d-96ad-ee93ca470b41.png)
