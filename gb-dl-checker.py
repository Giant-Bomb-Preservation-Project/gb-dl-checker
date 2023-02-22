# GB File Checker with UI

import PySimpleGUI as sg
from glob import glob
import csv, sys, os, math, re, random, string
import subprocess

# Change UI theme
sg.theme("DarkPurple3")

### UI Layout ###

# Console window settings
consoleframe = [
[sg.Multiline
(key='logfile',
size=(125,120),
font=('Courier New', 10),
background_color='#4e172e', 
text_color='#E16363',
reroute_stdout=True, 
reroute_stderr=True,
autoscroll=True),
]
]

# Interface layout
split_choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
controlframe = [
[sg.Text("Videos Folder: "), sg.Input(key="-GBINPUT-", change_submits=True), sg.FolderBrowse(key="-GBDIR-")],
[sg.Text("API CSV: "), sg.Input(key="-APIINPUT-", change_submits=True), sg.FileBrowse(key="-APICSV-")],
[sg.Text("Show CSV: "), sg.Input(key="-SHOWINPUT-", change_submits=True), sg.FileBrowse(key="-SHOWCSV-")],
]

csv_frame = [
[sg.Text("Upload CSV Output Directory: "), sg.Input(key="-CSVinputbox-", change_submits=True), sg.FileSaveAs(button_text='Browse', file_types=[("CSV Files", "*.csv", )], key="-UPLOADCSV-")],
[sg.Text("Split uploads into how many CSVs?: "), sg.Combo(split_choices, default_value = 1, key='-SPLITS-')],
]

collection_frame = [
[sg.Text("Which collection?"), sg.Radio("giant-bomb-archive", "Radio1", key='-GBID-'), sg.Radio ("opensource_movies", "Radio1", key='-OSID-'), sg.Radio("custom", "Radio1", key='-CUST-')],
[sg.Text("Custom id: "), sg.Input(size=(25,5), key='-CID-')],
[sg.Button("Submit", size=(10,1)), sg.Button("Upload", size=(10,1))],
]

# Layout call of above elements
layout = [
[sg.Column(controlframe, element_justification='center')],
[sg.HSeparator(color='#E16363')],
[sg.Column(csv_frame, element_justification='center')],
[sg.HSeparator(color='#E16363')],
[sg.Column(collection_frame, element_justification='center')],
[sg.HSeparator(color='#E16363')],
[sg.Column(consoleframe, element_justification='center')]]

# Draw window and designate app icon
window = sg.Window("GB DL Checker", layout, element_justification='center', finalize=True, size=(700,600), icon='gbsp.ico')

while True:
    event, values = window.read()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Submit":
        
        ### MAIN SCRIPT EXECUTION ###

        # Define the path variables from shlubbert's og script with the inputs from the chosen locations 
        
        # If input box has content in it, take that, otherwise take the input from the directory/filebrowser
        if values["-GBINPUT-"] != '':
          video_folder = values["-GBINPUT-"]
        elif values["-GBDIR-"] == True:
          video_folder = values["-GBDIR-"]

        # Repeated
        if values["-APIINPUT-"] != '':
          apidump_csv = values["-APIINPUT-"]
        elif values["-APICSV-"] == True:
          apidump_csv = values["-APICSV-"]
        
        # Repeated
        if values["-SHOWINPUT-"] != '':
          show_csv = values["-SHOWINPUT-"]
        elif values["-SHOWCSV-"] == True:
          show_csv = values["-SHOWCSV-"]
        else:
          show_csv = ''

        # Where the output CSV will be saved (old files will be overwritten).
        # Can then be passed to the IA CLI with `ia upload --spreadsheet=upload.csv`
        if values["-UPLOADCSV-"] != '':
          output_csv = values["-UPLOADCSV-"]
        elif values["-CSVinputbox-"] == True:
          output_csv = values["-CSVinputbox-"]
        else:
          output_csv = (os.getcwd() + '\\upload.csv')
        
        # Split the output into multiple CSV files to allow running multiple instances
        # of the IA CLI simultaneously for faster uploads (theoretically... if it doesn't ratelimit)
        output_parts = int(values["-SPLITS-"])

        # Optional: Identifier of the archive.org collection, if there is one
        # (otherwise uploads will have to be moved by an IA admin afterwards)
        if values["-GBID-"] == True:
          collection_id = 'giant-bomb-archive'
        elif values["-OSID-"] == True:
          collection_id = 'opensource_movies'
        elif values["-CUST-"] == True:
          collection_id = values["-CID-"]
        else:
          collection_id = ''



        # Define variables for api dump table, show table, and video files path
        apidump = list(csv.DictReader(open(apidump_csv, 'r', encoding='utf-8')))
        show = list(csv.DictReader(open(show_csv, 'r', encoding='utf-8'))) if show_csv else None
        video_files = glob(os.path.join(video_folder, '**/*.mp4'), recursive=True)
        output = []

        # Print findings for above variables
        print(len(video_files), 'videos in folder', video_folder)
        print(len(apidump), 'entries in API dump', apidump_csv)
        if show: print(len(show), 'entries in show', show_csv)
        print('')

        for path in video_files:
          filepath = os.path.dirname(path)
          filename = os.path.basename(path)
          filesize = os.path.getsize(path)

          # Try to match the local file with an entry in the GB API based on its file size
          apidata = None
          for row in apidump:
            if row['best_size_bytes'] and filesize == float(row['best_size_bytes'].replace(',','')):
              apidata = row
              
              if not show:
                  
                  # Take original filename and rename to the name on the API sheet
                  filename_normalized = apidata['Filename']
                  new_path = os.path.join(filepath, filename_normalized + '.mp4')
                  os.rename(path, new_path)
                  
                  # Print file renaming to Console
                  print("     ")
                  print("-------------------------")
                  print('FOUND: ' + filename)
                  print('RENAMED TO: ' + filename_normalized + '.mp4')
                  print('-------------------------') 
              break

          if apidata:
          
          # If a show has been specified, check if this video is part of it
            skip = False
            if show:
                skip = True
                for showrow in show:
                    if showrow['guid'] == apidata['guid']:
                      showrow['_found_'] = True
                      
                      # Rename files (only runs if Show CSV present)
                      filename_normalized = apidata['Filename']
                      new_path = os.path.join(filepath, filename_normalized + '.mp4')
                      os.rename(path, new_path)
                      
                      # Print file renaming to Console
                      print('     ')
                      print('-------------------------')
                      print('FOUND: ' + filename)
                      print('RENAMED TO: ' + filename_normalized + '.mp4')
                      print('-------------------------')  
                      skip = False
                      break

            if skip:
                print('-', end='')
                sys.stdout.flush()
      
            else:
          
                # Check for duplicates
                for outrow in output:
                    if outrow['external-identifier'] == 'gb-guid:' + apidata['guid']:
                      print(f'\nVideo ID {apidata["guid"]} appears more than once:')
                      print(' ', outrow['file'])
                      print(' ', path)

                # Assemble all the metadata for the Internet Archive
                output.append({
                  'identifier': 'gb-' + apidata['guid'] + '-ID' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                  'file': new_path,
                  'title': apidata['name'],
                  'description': apidata['deck'],
                  'subject[0]': 'Giant Bomb',
                  'subject[1]': apidata['video_show'],
                  'hosts': apidata['hosts'],
                  'creator': 'Giant Bomb',
                  'date': apidata['publish_date'].split(' ')[0],
                  'collection': collection_id,
                  'mediatype': 'movies',
                  'external-identifier': 'gb-guid:' + apidata['guid'],
                })

                print(' ', end='')
                sys.stdout.flush()

          else:
            print('\n***[ MISSING ] *** ')
            print(filename, '(Maybe not the highest quality?)')

        print('\n')

        # Check if whole show was found
        if show:
          foundcount = 0
          notfound = []

          for row in show:
            if '_found_' in row: foundcount += 1
            else: notfound.append(row)

          if foundcount == len(show):
            print('All show entries were found locally!')
          else:
            print(len(show)-foundcount, 'entries from', show_csv, 'were missing locally:')
            for row in notfound:
              print(' ', row['guid'], row['name'])

          print('')


        # WRITE OUTPUT CSV
        print(len(output), 'files ready to upload')

        for i in range(output_parts):
          outpath = f'{os.path.splitext(output_csv)[0]}{i+1}.csv' if output_parts > 1 else output_csv
          start = math.ceil(len(output) / output_parts * i)
          end = math.ceil(len(output) / output_parts * (i+1))

          with open(outpath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=output[0].keys())
            writer.writeheader()
            writer.writerows(output[start:end])
            print('  Saved output to', outpath)

        # Closing logo
        bomber1 = ("               \|/                          ")
        bomber2 = ("             `--+--'                        ")
        bomber3 = ("               /|\                          ")
        bomber4 = ("              ' | '                         ")
        bomber5 = ("            ,--'#`--.                       ")
        bomber6 = ("            |#######|                       ")
        bomber7 = ("         _.-'#######`-._                    ")
        bomber8 = ("      ,-'###############`-.                 ")
        bomber9 = ("     '#####################`,               ")
        bomber10 = ("   /####### @ @###### @ @###\           ")              
        bomber11 = ("  |######(@    @####@    @####|             ")
        bomber12 = (" |#######(@ (X) @###@ (X) @####|            ")
        bomber13 = (" |#########@   @#####@   @#####|            ")
        bomber14 = (" |#############################|            ")
        bomber15 = (" |########) [][][][][][] )#####|            ")
        bomber16 = ("  |######### (    \     )#####|             ")
        bomber17 = ("   \############(   \   )###/              ")
        bomber18 = ("    `.###########(   | )###,'               ")
        bomber19 = ("       `._#######(__/###_,'                 ")
        bomber20 = ("          `--..####..--'")
        print(bomber1)
        print(bomber2)
        print(bomber3)
        print(bomber4)
        print(bomber5)
        print(bomber6)
        print(bomber7)
        print(bomber8)
        print(bomber9)
        print(bomber10)
        print(bomber11)
        print(bomber12)
        print(bomber13)
        print(bomber14)
        print(bomber15)
        print(bomber16)
        print(bomber17)
        print(bomber18)
        print(bomber19)
        print(bomber20)

        print('Brought to you by Kane & Lynch 3')

        # Save sg.Multiline console window to text file
        with open("LogFile.txt", "w", encoding='UTF-8') as f:
          f.write(window['logfile'].get())
    
    # Upload to Internet Archive (must be logged in)
    elif event == "Upload":
      
      # Creates upload launcher naming based on Upload CSV input
      outpath_manager = f'{os.path.splitext(output_csv)[0]}_upload_manager.bat'
      
      # Deletes existing launcher
      if os.path.exists(outpath_manager):
        os.remove(outpath_manager)
      
      # Write separate Powershell scripts for each CSV created earlier
      # e.g. MarioMaker1.csv, Mariomaker2.csv would mean MarioMaker1.bat, Mariomaker2.bat
      for i in range(output_parts):
        outpath_bat = f'{os.path.splitext(output_csv)[0]}{i+1}.bat' if output_parts > 1 else f'{os.path.splitext(output_csv)[0]}.bat'       
        outpath_csv = f'{os.path.splitext(output_csv)[0]}{i+1}.csv' if output_parts > 1 else output_csv
        with open(outpath_bat, "w", encoding='UTF-8') as f:
            f.write('ia upload --spreadsheet=' + '\"' + outpath_csv + '\"' + ' --retries 100')
            f.close
        
        # Write upload launcher bat file that executes each individual instance of Powershell
        with open(outpath_manager, "a", encoding='UTF-8') as f:
          f.write(f"start \"{outpath_bat}\" \n")
      subprocess.Popen([outpath_manager], shell=True)