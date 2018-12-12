# PiGallery
Simple Set of tools to get artworks datasets

Current museums: MOMA, TATE & MET

## Use guide

**getlistpainters.py** [WIP] / Edit:
  'url=' to the Wikipedia url of the wanted category
  'output_name=' to the desire filename
  
**reverse.py** [WIP] method to reformat painters.csv to tate format

**[museum]_download.py** both 3 downloaders work the same:
'--csv [CSVPATH]' path to museum database CSV
'--out [DIRNAME]' path to output files directory
'--artist [CSVPATH] -a [CSVPATH]' path to the artist list file
'--type [TYPE]' artworks types (optional) [currently not working]
'--list [LISTFILE]' list file of the downloaded artworks (optional)

## Future goals

- [ ] Update tools to be more automatic
- [ ] Common 'download.py' inteface to call all downloaders
- [ ] Counter anti-bots automatic
- [ ] More museums  
