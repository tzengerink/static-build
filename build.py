#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    STATIC-BUILD
    ------------
    Easily concatinate and minify your JavaScript files and CSS stylesheets.

    First clone this repository as a submodule of your project. It is assumed
    this submodule is named `build`.

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
import json, subprocess, os


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


class Builder:
    """Assists in building static files.
    root -- Projects root directory.
    """
    def __init__(self, root):
        self.root = root

    def concat(self, paths, file_out):
        """Concatinate all files in list.
        paths    -- List of filepaths to concatinate.
        file_out -- Path to output file
        """
        File(file_out).clear()
        for file in paths:
            path = self.root+'/'+file
            File(file_out).write(File(self.root+'/'+file).read())

    def minify(self, file_in, file_out, file_type):
        """Minify file using the YUI Compressor.
        file_in  -- Path to input file.
        file_out -- Path to output file.
        type     -- Type of the file to minify (css/js)
        """
        subprocess.call(['java', '-jar',
            self.root+'/build/yuicompressor-2.4.7.jar', '-o', file_out,
            '--type', file_type, file_in])


def main():
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    builder = Builder(root)
    tmp = '/var/tmp/concat'
    for build in json.loads(File(root+'/build/builds.json').read()):
        for type in ['css', 'js']:
            builder.concat(build[type]['in'], tmp)
            builder.minify(tmp, build[type]['out'], type)


if __name__ == '__main__':
    main()
