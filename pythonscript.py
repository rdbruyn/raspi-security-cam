import os
import sqlite3
import numpy as np
import io
import picamera
import time
import timeit
from PIL import Image
from datetime import datetime

def compare(a, b, threshold):
    return (np.abs(a.astype(np.int16) - b.astype(np.int16)) > threshold).any(axis = 2)

image_dir = '/home/pi/Desktop/Security_Cam_Project'
output_dir = '/var/www/html/Video_Footage/'

os.chdir(output_dir)

#Camera stuff
width = 1280
height = 720
camera = picamera.PiCamera(framerate=25, resolution=(width, height))
camera.annotate_text_size = 12
camera.led = False
time.sleep(5)

#File and stream stuff
videostream = io.BytesIO()
sqlite_file = '/home/pi/Desktop/Security_Cam_Project/footage.sqlite'
if os.path.isfile(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('SELECT id FROM recordings ORDER BY id DESC')
    r = c.fetchone()
    if r is not None:
        #update recording count, and get the oldest file
        c.execute('SELECT id FROM recordings ORDER BY id')
        r = c.fetchone()
        oldestfileid = r[0]
    
else:
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('CREATE TABLE recordings (id INTEGER, Year INTEGER, Month INTEGER, Day INTEGER, Hour INTEGER, Filename TEXT)')
    conn.commit()
    recordingcount = 0

sensitivity = 20
stillmodifier = 0.03
activemodifier = 0.01
pingpongmodifier = 0.7
totalPixels = width * height
movementThreshold = totalPixels * stillmodifier
x = y = deltaCount = deltaPercent = 0
bwhichImage, bpaused, bmotionConfirmed = True, False, False

#Capture one pic to begin with
camera.capture(image_dir + '/Image1', 'jpeg', True)
image_1 = Image.open(image_dir + '/Image1')
image_1_arr = np.array(image_1)

## Code starts. Run infinite loop

while True:
    tic = timeit.default_timer()
##Take photos, alternating between image 1 and image 2
    if bwhichImage:
        camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
        camera.capture(image_dir + '/Image2', 'jpeg', True)
        image_2 = Image.open(image_dir + '/Image2')
        image_2_arr = np.array(image_2)
    else:
        camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
        camera.capture(image_dir + '/Image1', 'jpeg', True)
        image_1 = Image.open(image_dir + '/Image1')
        image_1_arr = np.array(image_1)

    x = y = deltaCount = 0
##Pixel by pixel comparison of images
    subarr = compare(image_1_arr, image_2_arr, sensitivity)
    subarr = subarr.astype(np.int).sum()
    deltaCount = subarr
    #print np.abs(image_1_arr - image_2_arr)
    print deltaCount, movementThreshold
    toc = timeit.default_timer()
    
    print str(toc - tic)
    ##If there is no movement, swap bwhichImage and start loop again
    if deltaCount >= movementThreshold:
        bmotionConfirmed = True
        camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
        print 'Motion confirmed'
    else:
        bmotionConfirmed = False
        print 'No Motion'
        bwhichImage = not bwhichImage
        if camera.recording:
            movementThreshold = totalPixels * activemodifier
            if not bpaused:
                bpaused = True
                for x in range(0, 3):
                    camera.wait_recording(0.5)
                    camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
                continue
            else:
                bpaused = False
                camera.stop_recording()
                camera.stop_preview()
                output.write(videostream.getvalue())
                output.close()
                videostream = io.BytesIO()
                os.system("MP4Box -fps 25 -add '" + timestr + ".h264' '" + otimestr + ".mp4'")
                os.remove(output_dir + timestr + '.h264')
                movementThreshold = totalPixels * pingpongmodifier
                if bwhichImage:
                    camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
                    camera.capture(image_dir + '/Image1', 'jpeg', True)
                    image_2 = Image.open(image_dir + '/Image2')
                    image_2_arr = np.array(image_2)
                else:
                    camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
                    camera.capture(image_dir + '/Image2', 'jpeg', True)
                    image_1 = Image.open(image_dir + '/Image1')
                    image_1_arr = np.array(image_1)
        else:
            movementThreshold = totalPixels * stillmodifier
        continue
##Check if there is still space left on the drive. If not, delete oldest files
    current_dir = os.getcwd()
    diskStats = os.statvfs(current_dir)
    diskSpace = diskStats.f_bavail * diskStats.f_frsize
    while ( diskSpace < 1 * 10**9 ):
        print diskSpace
        filelist = sorted(os.listdir(output_dir), key = os.path.getctime)
        os.remove(output_dir + filelist[0])
        #Find oldest file id
        c.execute('SELECT id FROM recordings ORDER BY id')
        r = c.fetchone()
        oldestfileid = r[0]
        c.execute("DELETE FROM recordings WHERE id={idn}".format(idn=oldestfileid))
        conn.commit()
        diskStats = os.statvfs(current_dir)
        diskSpace = diskStats.f_bavail * diskStats.f_frsize
##Record timestamped video
    if not camera.recording:
        camera.annotate_text = time.strftime('%Y/%m/%d - %H:%M:%S')
        camera.start_recording(videostream, format='h264', quality=20)
        camera.start_preview()
    ##Find the current time and date
        timestr = time.strftime("%Y%m%d-%H %M %S")
        otimestr = time.strftime("%Y%m%d-%H:%M:%S")
        dt = datetime.strptime(otimestr, '%Y%m%d-%H:%M:%S')
        print otimestr
        c.execute('SELECT id FROM recordings ORDER BY id DESC')
        r = c.fetchone()
        if r is not None:
            newestfileid = r[0]
        else:
            newestfileid = 0

        c.execute("INSERT INTO recordings (id, Year, Month, Day, Hour, Filename) VALUES (?, ?, ?, ?, ?, ?)", \
            (newestfileid + 1, dt.year, dt.month, dt.day, dt.hour, otimestr))
        conn.commit()
        
        output = io.open(output_dir + timestr + '.h264', 'wb')
        movementThreshold = totalPixels * activemodifier
    bwhichImage = not bwhichImage

camera.close()
