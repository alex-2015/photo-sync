#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys
import os
import shutil
import time
from datetime import datetime
import argparse
import re

argParser = argparse.ArgumentParser(description='Script to process photos from source and move them to dest.')
argParser.add_argument('source', help='source directory - absolute path')
argParser.add_argument('dest', help='destination directory - absolute path')
args = argParser.parse_args()

#sourceDir = '/Users/[username]/Dropbox/Camera Uploads/'
sourceDir = args.source
match = re.search(r'^.*/$', sourceDir)
if not match:
    sourceDir += str("/")

#destDir = '/Users/[username]/Pictures/Photos/'
destDir = args.dest
match = re.search(r'^.*/$', destDir)
if not match:
    destDir += str("/")

if not os.path.isdir(sourceDir):
  print 'Can\'t find source directory: ' + sourceDir
  sys.exit(1)
if not os.path.isdir(destDir):
  print 'Can\'t find destination directory: ' + destDir
  sys.exit(1)

error_files = []

for root, subFolders, files in os.walk(sourceDir):
  for photo_file in files:
    try:
      if photo_file.endswith(".jpg") or photo_file.endswith(".jpeg") or photo_file.endswith(".png") or photo_file.endswith(".gif"):
        photoPath = os.path.join(root, photo_file)
        photo_date = datetime.fromtimestamp(os.path.getmtime(photoPath))

        #if no directory exists for photo_date, create it
        new_photo_dir = os.path.join(destDir, photo_date.strftime("%Y-%m"))
        if not os.path.exists(new_photo_dir) and not os.path.isdir(new_photo_dir):
          os.mkdir(new_photo_dir)

        shutil.copy2(photoPath, new_photo_dir)
        os.remove(photoPath)
    except Exception:
      error_files.append(photoPath)

for error_file in error_files:
  print error_file

