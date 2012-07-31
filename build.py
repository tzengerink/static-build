#!/usr/bin/env python
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


def clear_contents(filepath):
    """Clear the contents of a file.
    filepath -- Path to the file.
    """
    handle = open(filepath, 'w')
    handle.close()


def concatenate(paths, filepath, root=False):
    """Concatinate all files in list.
    paths    -- List of filepaths to concatinate.
    filepath -- Filepath of the resulting file.
    root     -- Root directory.
    """
    clear_contents(filepath)
    for file in paths:
        path = root+'/'+file if root else file
        put_contents(get_contents(path), filepath)


def get_contents(filepath):
    """Get the contents of a file as a string.
    filepath -- Path to the file to get
    """
    contents = ""
    handle = open(filepath)
    while 1:
        line = handle.readline()
        if not line:
            break
        contents += line
    handle.close()
    return contents


def minify(path_in, path_out, type):
    """Minify all files in the given list.
    path_in  -- Path to input file.
    path_out -- Path to output file.
    type     -- Type of the file to minify (css/js)
    """
    subprocess.call(['java', '-jar', 'tools/yuicompressor-2.4.7.jar', '-o',
        path_out, '--type', type, path_in])


def put_contents(contents, filepath):
    """Append file with given text.
    txt      -- Text to append to file.
    filepath -- Path of the file.
    """
    handle = open(filepath, 'a')
    handle.write(contents)
    handle.close()


def main():
    for build in json.loads(get_contents("builds.json")):
        tmp = '/var/tmp/concat'
        for type in ['css', 'js']:
            concatenate(build[type]['in'], tmp, build['dir'])
            minify(tmp, build['dir']+'/'+build[type]['out'], type)


if __name__ == '__main__':
    main()
