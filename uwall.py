#!/usr/bin/env python
"""
Simple scirpt to change wallpaper form unsplash
"""
import urllib2
from gi.repository import Gio
import os
import sys
from os.path import expanduser

home = expanduser("~")
UNSPLASH_WALL_NAME = home + '/.config/uwall/unslpashWallPaper.jpeg'
UNSPLASH_URL = 'https://source.unsplash.com/random/1600x900'

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def gsettings_set(schema, path, key, value):
    """Set value of gsettings schema"""
    if path is None:
        gsettings = Gio.Settings.new(schema)
    else:
        gsettings = Gio.Settings.new_with_path(schema, path)
    if isinstance(value, list):
        return gsettings.set_strv(key, value)
    if isinstance(value, int):
        return gsettings.set_int(key, value)
    if isinstance(value, str):
        return gsettings.set_string(key, value)


def error_and_exit(message):
    """Error and exit whan the file is not found """
    sys.stderr.write(message + "\n")
    sys.exit(1)


def get_new_wallpaper():
    try:
        tmp_url_file = urllib2.urlopen(UNSPLASH_URL)
        tmp_file_data = tmp_url_file.read()
        ensure_dir(UNSPLASH_WALL_NAME)
        with open(UNSPLASH_WALL_NAME, "wb") as tmp_file:
            tmp_file.write(tmp_file_data)
        return True
    except Exception as e:
        error_and_exit('unable to get wallpaper from unsplash' + e.message)
        return False


def chanage_wallpaper():
    if get_new_wallpaper():
        gschema = 'org.gnome.desktop.background'
        key = 'picture-uri'
        if not os.path.isfile(UNSPLASH_WALL_NAME):
            error_and_exit('>>> Path "' + UNSPLASH_WALL_NAME +
                           '" isn\'t a file or file doesn\'t exit')
        full_path = os.path.abspath(UNSPLASH_WALL_NAME)
        uri = Gio.File.new_for_path(full_path).get_uri()
        gsettings_set(gschema, None, key, uri)


if __name__ == '__main__':
    chanage_wallpaper()
