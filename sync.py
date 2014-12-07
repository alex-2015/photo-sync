import argparse
from datetime import datetime
import os
from PIL import Image
from PIL.ExifTags import TAGS
import re
import shutil
import sys
import time

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
    print 'Error loading file EXIF data: ', filename
    return None
    
def get_photo_date(exif_data, photoPath):
  if exif_data is not None and 'DateTime' in exif_data:
    date_string = exif_data['DateTime']
    return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
  
  return datetime.fromtimestamp(os.path.getmtime(photoPath))
  
def get_photo_dir(photo_date):
  month = str(photo_date.month)
  if (len(month) == 1):
    month = "0" + month;
  return str(photo_date.year) + "-" + month
  
def format_dir_name(dirname):
  #make sure the path ends with '/'
  match = re.search(r'^.*/$', dirname)
  if not match:
    dirname += str("/")

  if not os.path.isdir(dirname):
    print 'Can\'t find directory: ' + dirname
    sys.exit(1)
  
  return dirname


###################
# Parse arguments #
###################

argParser = argparse.ArgumentParser(description='Script to process photos from source and move them to dest.')
argParser.add_argument('source', help='source directory - absolute path')
argParser.add_argument('dest', help='destination directory - absolute path')
args = argParser.parse_args()

sourceDir = format_dir_name(args.source)
destDir = format_dir_name(args.dest)

###############
# Move photos #
###############

error_files = []

for root, subFolders, files in os.walk(sourceDir):
  for photo_file in files:
    try:
      if photo_file.endswith((".png", ".jpg", ".jpeg", ".gif", ".PNG")):
        photoPath = os.path.join(root, photo_file)
        try:
          photo_data = get_exif_data(photoPath)
        except:
          photo_data = None
        photo_date = get_photo_date(photo_data, photoPath)
        photo_dir = get_photo_dir(photo_date)
        new_photo_dir = os.path.join(destDir, photo_dir)
        
        #if no directory exists for photo_date, create it
        if not os.path.exists(new_photo_dir) and not os.path.isdir(new_photo_dir):
          os.mkdir(new_photo_dir)

        shutil.copy2(photoPath, new_photo_dir)
        os.remove(photoPath)
    except Exception, Argument:
      print 'exception: ', Argument
      error_files.append(photoPath)

#########################################################
# Move files that couldn't be processed to a new folder #
#########################################################

for error_file in error_files:
  err_photo_dir = os.path.join(sourceDir, 'errors')
  if not os.path.exists(err_photo_dir) and not os.path.isdir(err_photo_dir):
    os.mkdir(err_photo_dir)

  shutil.copy2(error_file, err_photo_dir)
  os.remove(error_file)

