#######################################################################
# Python script to convert DayOne exported JSON file with photos in 
# separate markdown files and photo files in subfolders
#######################################################################
import json
import os
from shutil import copyfile

# define input filename / output target folders
dayone_export_json = 'Journal.json' # name of the DayOne JSON export file
dayone_folder_photos = 'photos/'    # name of the subfolder where the exported photos are stored
target_folder = 'Diary '            # name of the target folder for markdown files - the year will be added
target_folder_photos = '/NBImages'  # name of the subfolder within the target folder for photos

# read JSON file and convert it to python dict object
with open(dayone_export_json, encoding="utf8") as f:
  dayone_entries = json.load(f)

# go through all the entries and write target marktdown files
for entry in dayone_entries['entries']:
  
  # date formating for file name and headline
  str_entry_creationDate = entry['creationDate']
  str_entry_creationDate = str_entry_creationDate.replace('T', ' ')
  slice_object = slice(-1) 
  str_entry_creationDate = str_entry_creationDate[slice_object]
  slice_object = slice(-3) 
  str_entry_creationDate_heading = str_entry_creationDate.replace(':', '.')
  str_entry_folder = target_folder + str_entry_creationDate_heading[:4]
  str_entry_folder_images = str_entry_folder + target_folder_photos
  str_entry_creationDate_heading = str_entry_creationDate_heading[slice_object]

  # DayOne entry text
  str_entry_text = entry['text']

  # check if DayOne entry has a headline
  headline_exists = str_entry_text.find('\n\n')
  # check if DayOne entry has a photo
  photo_exists = str_entry_text.find('![]')
  if photo_exists == 0:
    str_entry_text = str_entry_text[55:]
  headline_exists = str_entry_text.find('\n\n')
  # print (str_entry_creationDate, ' - Ü', headline_exists)

  # if there is a headline, do special formating
  if headline_exists > 0:
    if headline_exists < 80:
      str_headline = str_entry_text[:headline_exists]
      str_entry_text = str_entry_text[headline_exists+2:]
      # remove special characters from headline in order to save file
      str_headline = str_headline.replace(':', '-')
      str_headline = str_headline.replace(',', ' -')
      str_headline = str_headline.replace('¿', '')
      str_headline = str_headline.replace('?', '')
      str_headline = str_headline.replace('->', '-')
      str_headline = str_headline.replace('/', '-')      
      str_headline = str_headline.replace('\n', ' - ')  
      str_headline = str_headline.replace('*', '-')       
      str_headline = str_headline.replace('"', '')       
      str_entry_creationDate_heading = str_entry_creationDate_heading + ' ' + str_headline
      
  str_entry_creationDate_filename = str_entry_folder + "/" + str_entry_creationDate_heading + '.md'

  print ('Converting DayOne entry: ', str_entry_creationDate_heading)

  # create folder if not exits
  if not os.path.exists(str_entry_folder):
     os.makedirs(str_entry_folder)

  # create subfolder for photos if not exits
  if not os.path.exists(str_entry_folder_images):
     os.makedirs(str_entry_folder_images)

  # if the entry has a photos: get it, rename it and copy it to target folder
  if entry.get('photos'):
      entry_photo = entry['photos']
      entry_photo_md5 = entry_photo[0]['md5']
      entry_photo_filename = dayone_folder_photos + entry_photo_md5 + ".jpeg"
      entry_photo_full_destination_filename = str_entry_folder_images + "/" + str_entry_creationDate_heading + ".jpg"
      entry_photo_destination_filename = target_folder_photos + str_entry_creationDate_heading + ".jpg"
      copyfile(entry_photo_filename, entry_photo_full_destination_filename)

  # create target markdown file in structure with DayOne entry elements
  with open(str_entry_creationDate_filename,'w',encoding = 'utf-8') as file:
    file.write("# ")
    file.write(str_entry_creationDate_heading)
    file.write("\n\n")
    file.write(str_entry_text)
    file.write("\n\n")
    if entry.get('photos'):
        file.write("![](")
        file.write(entry_photo_destination_filename)
        file.write(")\n\n")        
    file.write("***\n\nTags: ")
    if entry['starred']:
      file.write("#stern ")
    if entry.get('tags'):
      list_tags = entry['tags']
      str_tags = " #".join(list_tags)
      str_tags = str_tags.lower()
      str_tags = '#' + str_tags + ' '
      str_tags = str_tags.replace('# #', '#')
      str_tags = str_tags.replace('round table', 'roundtable')
      file.write(str_tags)
    file.write("\nDatumZeit: ")
    file.write(str_entry_creationDate)
    file.write(" ")   
    file.write(entry['timeZone'])
    file.write(" \n")   
    if entry.get('location'):
      entry_location = entry['location']
      file.write("Ort: \n")      
      if entry_location.get('placeName'):
        file.write(entry_location['placeName'])  
        file.write(" \n")  
      if entry_location.get('localityName'):
        file.write(entry_location['localityName'])  
        file.write(" \n")  
      if entry_location.get('administrativeArea'):      
        file.write(entry_location['administrativeArea'])  
        file.write(" \n")
      if entry_location.get('country'):      
        file.write(entry_location['country'])  
        file.write(" \n")
      if entry_location.get('latitude'):
        file.write("[Karte](https://maps.apple.com/?q=")
        file.write(str(entry_location['latitude'])) 
        file.write(",") 
        file.write(str(entry_location['longitude'])) 
        file.write("&ll=") 
        file.write(str(entry_location['latitude'])) 
        file.write(",") 
        file.write(str(entry_location['longitude'])) 
        file.write(")\n") 
      if entry_location.get('foursquareID'):  
        file.write("[Foursquare](https://de.foursquare.com/v/")    
        file.write(str(entry_location['foursquareID']))
        file.write(")\n")     
      file.write("LatitudeBreite: ")
      if entry_location.get('latitude'):      
        file.write(str(entry_location['latitude']))  
      file.write(" \nLongitudeLänge: ")   
      if entry_location.get('longitude'):      
        file.write(str(entry_location['longitude']))        
      file.write(" \n")
    if entry.get('weather'):
      entry_weather = entry['weather']
      file.write("\nWetter: \n")      
      if entry_weather.get('temperatureCelsius'):
        file.write('Temperatur: ')
        file.write(str(entry_weather['temperatureCelsius'])) 
        file.write(' °C \n')
      if entry_weather.get('conditionsDescription'):
        file.write(entry_weather['conditionsDescription'])
        file.write(' \n')
    if entry.get('userActivity'):
      entry_useractivity = entry['userActivity']
      if entry_useractivity.get('stepCount'):
        file.write('\nSchritte: ')
        file.write(str(entry_useractivity['stepCount']))    
        file.write(' \n')   
    if entry['creationDevice']:      
      file.write("\nErstelltMit: \n")
      file.write(entry['creationDevice'])  
      file.write(" \n")
      file.write(entry['creationDeviceModel'])  
      file.write(" \n")
      file.write(entry['creationOSVersion'])  
      file.write(" \n")
    file.write("converted from DayOne JSON Export\n")
  file.close()

print ('Done!')
# end