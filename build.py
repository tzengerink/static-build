#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    STATIC-BUILD
    ------------
    Easily concatinate and minify your JavaScript files and CSS stylesheets.

    First clone this repository as a submodule of your project. It is assumed
    this submodule is placed in your projects root directory.

    Inside the submodule copy and rename `builds.json.default` and edit the file
    to meet your needs. You should use the following as your template:

        [{
            "css" : {
                "in" : [],
                "out" : "css/style.min.css"
            },
            "js" : {
                "in" : [],
                "out" : "js/script.min.js"
            }
        }]

    Copyright (c) 2012, T. Zengerink
    Licensed under MIT Lisence
    See: https://raw.github.com/Mytho/static-build/master/LISENCE
"""
import argparse, json, subprocess, os


class Builder:
    """Assists in building static files.
    root_dir  -- Projects root directory.
    build_dir -- Path of build directory.
    tmp       -- Temporary file (Default='/var/tmp/static-build').
    """
    def __init__(self, root_dir, build_dir, tmp='/var/tmp/static-build'):
        self.root_dir = root_dir
        self.build_dir = build_dir
        self.tmp = tmp
        self.json = build_dir+'/builds.json'

    def build(self):
        """Build the files according to the JSON file."""
        for build in json.loads(File(self.json).read()):
            for type in ['css', 'js']:
                if type in build:
                    Log.write("Concatinating "+type+":")
                    self.concat(build[type]['in'])
                    Log.write("Minifying "+type+":")
                    self.minify(build[type]['out'], type)
        Log.write("Done")

    def concat(self, paths, file_out=None):
        """Concatinate all files in list.
        paths    -- List of filepaths to concatinate.
        file_out -- Path to output file (Default=None).
        """
        if file_out == None:
            file_out = self.tmp
        File(file_out).clear()
        for file in paths:
            Log.write(" "+file)
            path = self.root_dir+'/'+file
            File(file_out).write(File(self.root_dir+'/'+file).read())

    def minify(self, file_out, file_type, file_in=None):
        """Minify file using the YUI Compressor.
        file_out -- Path to output file.
        type     -- Type of the file to minify (css/js).
        file_in  -- Path to input file (Default=None).
        """
        if file_in == None:
            file_in = self.tmp
        Log.write(" "+file_out)
        subprocess.call(['java', '-jar',
                         self.build_dir+'/yuicompressor-2.4.7.jar',
                         '-o', self.root_dir+'/'+file_out, '--type',
                         file_type, file_in])


class File:
    """Assists in handling files.
    path -- Path of the file.
    """
    def __init__(self, path):
        self.path = path

    def clear(self):
        """Clear the contents of the file."""
        open(self.path, 'w').close()

    def read(self):
        """Read the contents of the file."""
        contents = ""
        handle = open(self.path)
        while 1:
            line = handle.readline()
            if not line:
                break
            contents += line
        handle.close()
        return contents

    def write(self, txt):
        """Append text to the end of the file.
        txt -- Text to append to the file.
        """
        handle = open(self.path, 'a')
        handle.write(txt)
        handle.close()


class Log:
    """Assists in logging output to the screen."""
    enabled = False
    @staticmethod
    def write(str):
        """Write string to the screen."""
        if Log.enabled:
            print(str)


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='be verbose')
    args = parser.parse_args()
    Log.enabled = args.verbose


def main():
    handle_args()
    Builder(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        os.path.dirname(os.path.realpath(__file__))).build()


if __name__ == '__main__':
    main()
