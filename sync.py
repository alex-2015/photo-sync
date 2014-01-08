#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys
import os
import shutil
import time
from datetime import datetime
import argparse
import re
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(filename):
  ret = {}
  try:
    image = Image.open(filename)
    info = image._getexif()
    for tag, value in info.items():
      decoded = TAGS.get(tag, tag)
      ret[decoded] = value
    return ret
  except IOError:
    print 'Error loading file EXIF data'
    return None
    
def get_photo_date(exif_data):
  date_string = exif_data['DateTimeOriginal']
  return datetime.strptime(date_string, "%Y:%m:%d %H:%M:%S")
  
def get_photo_dir(photo_date):
  month = str(photo_date.month)
  if (len(month) == 1):
    month = "0" + month;
  return str(photo_date.year) + "-" + month
  


argParser = argparse.ArgumentParser(description='Script to process photos from source and move them to dest.')
argParser.add_argument('source', help='source directory - absolute path')
argParser.add_argument('dest', help='destination directory - absolute path')
args = argParser.parse_args()


#sourceDir = '/Users/[username]/Dropbox/Camera Uploads/'
sourceDir = args.source

#make sure the path ends with '/'
match = re.search(r'^.*/$', sourceDir)
if not match:
  sourceDir += str("/")

if not os.path.isdir(sourceDir):
  print 'Can\'t find source directory: ' + sourceDir
  sys.exit(1)


#destDir = '/Users/[username]/Pictures/Photos/'
destDir = args.dest

#make sure the path ends with '/'
match = re.search(r'^.*/$', destDir)
if not match:
  destDir += str("/")

if not os.path.isdir(destDir):
  print 'Can\'t find destination directory: ' + destDir
  sys.exit(1)


error_files = []

for root, subFolders, files in os.walk(sourceDir):
  for photo_file in files:
    try:
      if photo_file.endswith((".png", ".jpg", ".jpeg", ".gif")):
        photoPath = os.path.join(root, photo_file)
        
        photo_data = get_exif_data(photoPath)
        
        if (photo_data is None):
          print 'No exif data found'
          error_files.append(photoPath)
        else:
          photo_date = get_photo_date(photo_data)
          photo_dir = get_photo_dir(photo_date)
          new_photo_dir = os.path.join(destDir, photo_dir)
          #if no directory exists for photo_date, create it
          if not os.path.exists(new_photo_dir) and not os.path.isdir(new_photo_dir):
            os.mkdir(new_photo_dir)

          shutil.copy2(photoPath, new_photo_dir)
          os.remove(photoPath)
    except Exception:
      print 'exception somewhere'
      error_files.append(photoPath)

for error_file in error_files:
  #TODO move these to an error folder
  print error_file

