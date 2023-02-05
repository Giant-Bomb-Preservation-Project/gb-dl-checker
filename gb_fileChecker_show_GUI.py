# GB File Checker with UI

import PySimpleGUI as sg
from glob import glob
import csv, sys, os, math, re

# Redefine default print method to sg.Print (pySimpleGUI)
print = sg.Print
sg.SetOptions(debug_win_size=(100,50))

# Change theme
sg.theme("DarkPurple3")

# UI Layout
layout = [
[sg.Text("Videos Folder: "), sg.Input(), sg.FolderBrowse(key="-GBDIR-")],
[sg.Text("API CSV: "), sg.Input(), sg.FileBrowse(key="-APICSV-")],
[sg.Text("Show CSV: "), sg.Input(), sg.FileBrowse(key="-SHOWCSV-")],
[sg.Button("Submit")]

]

# Draw window
window = sg.Window("GB DL Checker", layout, size=(500,150))

while True:
    event, values = window.read()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "Submit":
        # Define the path variables from shlubbert's og script with the inputs from the chosen locations 
        video_folder = values["-GBDIR-"]
        apidump_csv = values["-APICSV-"]
        show_csv = values["-SHOWCSV-"]
        
        apidump = list(csv.DictReader(open(apidump_csv, 'r', encoding='utf-8')))
        show = list(csv.DictReader(open(show_csv, 'r', encoding='utf-8'))) if show_csv else None
        video_files = glob(os.path.join(video_folder, '**/*.mp4'), recursive=True)
        output = []

        print(len(video_files), 'videos in folder', video_folder)
        print(len(apidump), 'entries in API dump', apidump_csv)
        if show: print(len(show), 'entries in show', show_csv)
        print('')

        for path in video_files:
          filename = os.path.basename(path)
          filesize = os.path.getsize(path)

          # Try to match the local file with an entry in the GB API based on its file size
          apidata = None
          for row in apidump:
            if row['best_size_bytes'] and filesize == float(row['best_size_bytes'].replace(',','')):
              apidata = row
              new_file_path_dump = os.path.join(video_folder, row['Filename']+'.mp4')
              os.rename (path, new_file_path_dump)

          if apidata:
        # If a show has been specified, check if this video is part of it
            skip = False
            if show:
                skip = True
                for showrow in show:
                    if showrow['guid'] == apidata['guid']:
                      showrow['_found_'] = True
                      skip = False
                      new_file_path_show = os.path.join(video_folder, showrow['Filename']+'.mp4')
                      os.rename (path, new_file_path_show)

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

            print('+', end='')
            sys.stdout.flush()

        else:
            print('\nNo match for', path, '(Maybe not the highest quality?)')

    print('\n')

    #
    # CHECK IF WHOLE SHOW WAS FOUND
    #

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
    sg.Print(bomber1)
    sg.Print(bomber2)
    sg.Print(bomber3)
    sg.Print(bomber4)
    sg.Print(bomber5)
    sg.Print(bomber6)
    sg.Print(bomber7)
    sg.Print(bomber8)
    sg.Print(bomber9)
    sg.Print(bomber10)
    sg.Print(bomber11)
    sg.Print(bomber12)
    sg.Print(bomber13)
    sg.Print(bomber14)
    sg.Print(bomber15)
    sg.Print(bomber16)
    sg.Print(bomber17)
    sg.Print(bomber18)
    sg.Print(bomber19)
    sg.Print(bomber20)

    
    sg.Print('Brought to you by Kane & Lynch 3', do_not_reroute_stdout=False)