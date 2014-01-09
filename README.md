#Photo Sync
##Photo organiser script for OS X

This script lets you take photos from one location on your hard drive and organise them in another location.

For example, I use the script to take auto-uploaded photos from the Dropbox Camera Uploads directory and move them to my Pictures directory.

###Organisation

In the new location, the script organises photos by month. If required, it will create a directory for the month in which the photo was taken, and it will move the photo file into that directory.

###Dependencies
This is a Python script, and I built it using 2.7.5. I can't guarantee that it will run using an older version, and I haven't tested it with Python 3 either.

The only module I had to install was [Pillow, the modern version of PIL](http://pillow.readthedocs.org/en/latest/index.html) (the Python imaging library). I installed it using pip:
    pip install Pillow

###Use
You can set the script up using launchd, as I have done, or you can run it manually.

####Using launchd
Create a file in the ~/Library/LaunchAgents directory. For more information, I found [Nathan Grigg's tutorial](http://nathangrigg.net/2012/07/schedule-jobs-using-launchd/) useful.

####Running Manually
    python sync.py /absolute/path/to/source /absolute/path/to/dest

###Contact
I'm [@neilmcguiggan on Twitter](http://twitter.com/neilmcguiggan). You can also email me at neil [at] mcguiggan [dot] org. I welcome any feature suggestions or pull requests you may have.