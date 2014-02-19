#!/usr/local/bin/python

import os
import sys
import glob
import time
import datetime
import csv
import EXIF
import Image
from operator import itemgetter
sys.path.append('/home/isop/www/photo/')
sys.path.append('/home/isop/lib/Imaging-1.1.7/PIL/')

thumbnail_size = 200

try:
    # using join to get target-directory with a trailing slash.
    directory = os.path.join(sys.argv[1],"")
    if not os.path.isdir(directory):
        print "target directory is not exists or not directory.\n"
        raise Exception()
except:
    print "Initpics make thumbnails and gather properties of pictures in target directory."
    print "usage : python initpics.py <target directory>"
    sys.exit()
print "target directory is %s" % directory

# make thumbnails directory
thumbdir = os.path.join(directory,"thumbnails")
if not os.path.isdir(thumbdir):
    try:
        os.mkdir(thumbdir)
    except:
        print "Can't make thumbnails direcotry."
        sys.exit()
print "thumbnail directory is %s" % thumbdir


print "Making thumbnails and gathering properties of pictures."
csvdata = []

# read file name
for i, infile in enumerate(glob.glob(directory+'*.jpg')):

    # getmtime
    unixfiledate = os.path.getmtime(infile)
    filedate = time.strftime('%Y:%m:%d %X',time.localtime(unixfiledate))

    # convert thumbnail
    if not os.path.isfile(directory+"thumbnails/_thumb_"+os.path.basename(infile)):
        print i+1,": making a thumbnail."
        # read image
        image = Image.open(infile)
        image.thumbnail((thumbnail_size,thumbnail_size), Image.ANTIALIAS)

        # save filtered image
        image.save(directory+"thumbnails/_thumb_"+os.path.basename(infile))
    else:
        print i+1,": a thumbnail exists."
        image = Image.open(directory+"thumbnails/_thumb_"+os.path.basename(infile))


    width, height = image.size


    # file open
    fp = open(infile)
    exif = EXIF.process_file(fp)


    # get EXIF datetime
    try:
        datetime = exif['EXIF DateTimeOriginal']
    except KeyError:
        datetime = filedate

    unixdatetime = time.mktime(time.strptime(str(datetime),'%Y:%m:%d %X'))

    # get EXIF Image Orientation
    try:
        orientation = exif['Image Orientation']
    except KeyError:
        orientation = "Orientation Undefined"

    if width>height:
        tateyoko = "yoko"
    else:
        tateyoko = "tate"
    csvdata.append((os.path.basename(infile),unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,tateyoko))

csvdata = sorted(csvdata, key=itemgetter(1))
writer = csv.writer(open(directory+"sort_datetime.csv","wb"))
for row in csvdata: writer.writerow(row)

csvdata = sorted(csvdata, key=itemgetter(1),reverse=True)
writer = csv.writer(open(directory+"sort_datetime_reverse.csv","wb"))
for row in csvdata: writer.writerow(row)

csvdata = sorted(csvdata, key=itemgetter(3))
writer = csv.writer(open(directory+"sort_filedate.csv","wb"))
for row in csvdata: writer.writerow(row)

csvdata = sorted(csvdata, key=itemgetter(3),reverse=True)
writer = csv.writer(open(directory+"sort_filedate_reverse.csv","wb"))
for row in csvdata: writer.writerow(row)
