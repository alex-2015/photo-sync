import argparse
import flickrapi
import os
import re

def load_config():
  f = open('config_file', 'w')
  config = json.load(f)
  return config
  
def save_config(config):
  f = open('config_file', 'w')
  json.dump(config, f)


def get_source_dir(source_arg):
  #make sure the path ends with '/'
  match = re.search(r'^.*/$', source_arg)
  if not match:
    source_arg += str("/")

  if not os.path.isdir(source_arg):
    print 'Can\'t find source directory: ' + source_arg
    sys.exit(1)
  
  return source_arg
  

def upload_callback(progress, done):
  if done:
    print 'Finished uploading'
  else:
    print 'At %s%%' % progress

def upload(fn):
  file_title = os.path.basename(fn)
  flickr.upload(filename=fn, title=file_title, description=u'', is_public=0, is_family=0, is_friend=0, callback=upload_callback, format='rest')


###################
# Parse arguments #
###################

argParser = argparse.ArgumentParser(description='Script to upload photos to Flickr.')
argParser.add_argument('source', help='source directory - absolute path')
args = argParser.parse_args()

sourceDir = get_source_dir(args.source)

config = load_config

#####################
# Connect to Flickr #
#####################

try:
  api_key = '1ddcc9a22038f6fd14c18d53f5420653'
  api_secret = '8c5a7838b8057254'
  flickr = flickrapi.FlickrAPI(api_key, api_secret)
  (token, frob) = flickr.get_token_part_one(perms='write')
  if not token: raw_input("Press ENTER after you authorized this program")
  flickr.get_token_part_two((token, frob))
  print 'Connected to Flickr'
except Exception:
  print 'Exception connecting to Flickr'

#################
# Upload photos #
#################

error_files = []

try:
  for root, subFolders, files in os.walk(sourceDir):
    for photo_file in files:
      try:
        if photo_file.endswith((".png", ".jpg", ".jpeg", ".gif", ".PNG")):
          photoPath = os.path.join(root, photo_file)
          upload(photoPath)
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


save_config(config)