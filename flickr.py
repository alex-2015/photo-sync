import flickrapi
  
def upload_callback(progress, done):
  if done:
    print 'Finished uploading'
  else:
    print 'At %s%%' % progress

def upload(fn):
  flickr.upload(filename=fn, title=fn, description=u'', is_public=0, is_family=0, is_friend=0, callback=upload_callback, format='rest')

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

try:
  upload('/Users/neilmcg/Documents/test/2013-12/IMG_2045.jpg')
except Exception, Argument:
  print 'Error uploading to Flickr', Argument