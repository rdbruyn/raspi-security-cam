# Raspberry Pi Security Camera

## Description

This project assumes that you have a Raspberry Pi with an attached PiCamera
module. It allows your Pi to record video footage from the PiCamera whenever it
detects motion. It does this by continually running an internal video feed
inside a Python script, and snapping frames from the feed for comparison. If
two frames have differing pixels above a certain threshold, then movement must
be taking place, and the video feed starts being written to a file. Recording
stops once the difference between frames in the video feed falls below the
threshold again.

The script also deletes old footage when the Pi's storage becomes full,
allowing you to keep the most relevant footage on hand. The videos are also
converted to a format that is easily viewable by web browsers. The code in the
`Example Code` folder is a collection of PHP scripts that can be served by an
Apache or Nginx server running on the Pi itself, for example, so that the video
footage can be viewed over a local network.

## Notes

* This is my very first Python 2 and PHP coding ever, so try not to mind some of the
  messy code in the scripts.
* The script uses an SQLite3 database. You don't have to create the database
  files yourself, but make sure that it is installed on your Pi.
* The PHP scripts in the `Example Code` folder can be included in the `www`
  folder of your webserver of choice, and should give you a crude but
functional interface for viewing the video footage over a local network
* If you want the script to start up whenever the Pi is turned on, instead of
  having to use SSH or some other manual method of starting the security
camera, add a `crontab` job to run the `launcher.sh` script with `bash` on
startup.
* No video compression is applied to the recorded footage. As a result,
  the video files may be quite large, despite the conservative resolution.

## TODO

* Refactor code and convert to Python 3.
* Add CSS to the web pages.
