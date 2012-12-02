STATIC-BUILD
------------
Easily concatinate and minify your JavaScript files and CSS stylesheets.

First clone this repository as a submodule of your project. Inside the submodule
copy and rename `builds.json.default` and edit the file to meet your needs. You
should use the following as your template:

    [{
        "name" : "My Repo Name",
        "css" : {
            "in" : [],
            "out" : "css/style.min.css"
        },
        "js" : {
            "in" : [],
            "out" : "js/script.min.js"
        }
    }]

*Copyright (c) 2012, T. Zengerink - [See the lisence](https://raw.github.com/Mytho/static-build/master/LICENSE)*
