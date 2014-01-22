import argparse
from datetime import datetime
import flickrapi
import json
import os
from PIL import Image
from PIL.ExifTags import TAGS
import re
import shutil
import sys

def load_config():
  f = open('./config_file', 'r')
  config = json.load(f)
  return config
  
def save_config(config):
  f = open('./config_file', 'w')
  json.dump(config, f)
  
def sync_config(latest_folder_synced, latest_photo_synced_today):
  config['latest_folder_synced'] = latest_folder_synced.isoformat()
  config['latest_photo_synced'] = latest_photo_synced_today.isoformat()
  save_config(config)

def get_source_dir(source_arg):
  #make sure the path ends with '/'
  match = re.search(r'^.*/$', source_arg)
  if not match:
    source_arg += str("/")

  if not os.path.isdir(source_arg):
    print 'Can\'t find source directory: ' + source_arg
    sys.exit(1)
  
  return source_arg

def get_exif_data(filename):
  ret = {}
  try:
    image = Image.open(filename)
    info = image._getexif()
    for tag, value in info.items():
      decoded = TAGS.get(tag, tag)
      ret[decoded] = value
    return ret
  except Exception, Argument:
    print 'Couldn\'t load EXIF data for file: ', Argument
    return None
    
def get_photo_date(photoPath):
  try:
    exif_data = get_exif_data(photoPath)
  except:
    exif_data = None
    
  if exif_data is not None and 'DateTime' in exif_data:
    date_string = exif_data['DateTime']
    return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
  
  return datetime.fromtimestamp(os.path.getmtime(photoPath))

def connect_to_flickr():
  api_key = '1ddcc9a22038f6fd14c18d53f5420653'
  api_secret = '8c5a7838b8057254'
  flickr = flickrapi.FlickrAPI(api_key, api_secret)
  (token, frob) = flickr.get_token_part_one(perms='write')
  if not token: raw_input("Press ENTER after you authorized this program")
  flickr.get_token_part_two((token, frob))
  return flickr

def upload_callback(progress, done):
  if done:
    print 'Finished uploading'
  else:
    print 'At %s%%' % progress

def upload(fn, flickr):
  file_title = os.path.basename(fn)
  flickr.upload(filename=fn, title=file_title, description=u'', is_public=0, is_family=0, is_friend=0, callback=upload_callback, format='rest')


###################
# Parse arguments #
###################

argParser = argparse.ArgumentParser(description='Script to upload photos to Flickr.')
argParser.add_argument('source', help='source directory - absolute path')
args = argParser.parse_args()

sourceDir = get_source_dir(args.source)

#####################
# Connect to Flickr #
#####################

try:
  flickr = connect_to_flickr()
except Exception:
  print 'Exception connecting to Flickr'

########################
# Get latest sync data #
########################

config = load_config()
if 'latest_folder_synced' in config:
  latest_folder_synced = config['latest_folder_synced']
  latest_folder_synced = datetime.strptime(latest_folder_synced, "%Y-%m-%dT%H:%M:%S")
else:
  latest_folder_synced = datetime.min
if 'latest_photo_synced' in config:
  latest_photo_synced = config['latest_photo_synced']
  latest_photo_synced = datetime.strptime(latest_photo_synced, "%Y-%m-%dT%H:%M:%S")
else:
  latest_photo_synced = datetime.min
latest_photo_synced_today = latest_photo_synced

#################
# Upload photos #
#################

error_files = []
try:
  for root, subFolders, files in os.walk(sourceDir):
    print '\n'
    foldername = os.path.basename(root)
    print 'Processing directory: ' + foldername
    try:
      current_folder_date = datetime.strptime(foldername, "%Y-%m")
    except Exception, Argument:
      print 'Skipping directory:', Argument
      continue
    
    if current_folder_date >= latest_folder_synced:
      latest_folder_synced = current_folder_date
    else:
      print 'Directory already processed.'
      continue
    
    for photo_file in files:
      try:
        if photo_file.endswith((".png", ".jpg", ".jpeg", ".gif", ".PNG")):
          photoPath = os.path.join(root, photo_file)
          
          photo_date = get_photo_date(photoPath)
          if photo_date > latest_photo_synced:
            upload(photoPath, flickr)
            print 'Uploading ' + photoPath + "..."
            if (photo_date > latest_photo_synced_today):
              latest_photo_synced_today = photo_date
      except Exception, Argument:
        print 'exception: ', Argument
        error_files.append(photoPath)
except Exception, Argument:
  print 'Error uploading to Flickr', Argument

########################################
# Move files that couldn't be uploaded #
########################################

for error_file in error_files:
  err_photo_dir = os.path.join(sourceDir, 'flickrErrors')
  if not os.path.exists(err_photo_dir) and not os.path.isdir(err_photo_dir):
    os.mkdir(err_photo_dir)

  shutil.copy2(error_file, err_photo_dir)

#########################
# Save latest sync data #
#########################

sync_config(latest_folder_synced, latest_photo_synced_today)
