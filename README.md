# gb-dl-checker

Forked from https://gist.github.com/shlubbert/56d4865d1256a3d1a2eeed8c23df7bcb 

Checks Giant Bomb Preservation Project download folders for known filesizes of highest quality videos.

If videos are found they are re-named based on the API Dump/Show CSV. Missing episodes or episodes with lower quality will (hopefully)
be flagged in the output log.

Loading only the API dump will search and rename files across multiple shows. 

Specifying a Show CSV as well as the API dump will limit the analysis to just that show.

## USAGE
- Run gb-dl-checker.py (or exe)
- Choose your downloads folder (either show specific or high-level folder for multiple shows)
- Choose the location of the API dump CSV file (If you do not have this, export a CSV copy of the API dump https://docs.google.com/spreadsheets/d/1MPAHk9RS3yMExC7iX_eM_2W8ljyUXy-nBurjZ2fdU9s/edit)
- (Optional) If only checking a singular show, choose the location of the show CSV (export from Giant Bomb Archive sheet under the show-specific page)
- Hit 'Submit' and pray?
