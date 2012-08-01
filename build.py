#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    STATIC-BUILD
    ------------
    Easily concatinate and minify your JavaScript files and CSS stylesheets.

    Simply edit `builds.json` to meet your needs. You should use the following
    as your template:

        [{
            "dir" : "static",
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
import json, subprocess


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
        handle.write(contents)
        handle.close()


def concatenate(paths, filepath, root=False):
    """Concatinate all files in list.
    paths    -- List of filepaths to concatinate.
    filepath -- Filepath of the resulting file.
    root     -- Root directory.
    """
    File(filepath).clear()
    for file in paths:
        path = root+'/'+file if root else file
        File(filepath).write(File(path).read())


def minify(path_in, path_out, type):
    """Minify all files in the given list.
    path_in  -- Path to input file.
    path_out -- Path to output file.
    type     -- Type of the file to minify (css/js)
    """
    subprocess.call(['java', '-jar', 'yuicompressor-2.4.7.jar', '-o',
        path_out, '--type', type, path_in])


def main():
    for build in json.loads(File('builds.json').read()):
        tmp = '/var/tmp/concat'
        for type in ['css', 'js']:
            concatenate(build[type]['in'], tmp, build['dir'])
            minify(tmp, build['dir']+'/'+build[type]['out'], type)


if __name__ == '__main__':
    main()
