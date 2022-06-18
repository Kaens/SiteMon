# SiteMon
SiteMon tracks changes in site contents as set up in the ini file, using CSS selectors, Xpath, or regular expressions.
JS is supported*. Passworded pages and browser cookies are not, yet. Definitely works on [CPython 3.10.5 w64](https://www.python.org/downloads/windows/) and [PyPy 3.9 w64](https://www.pypy.org/download.html).

As output, it sends to stdout the space-separated list of "pages" that changed, as well as adds them to a report file with timestamps.

(* The script renders JS using Chromium, so it will download Chromium to `~/.pyppeteer` (or `%LOCALAPPDATA%/pyppeteer/`) on first JS request.)

## Installation
For CPython:

    python3 -m ensurepip
    python3 -m pip install --upgrade pip
    python3 -m pip install keyboard requests_html

For PyPy 3.9 on Windows, things are currently much more complicated because [Christopher Gohlke's lxml builds](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml) are only up to 3.8, and requests_html requires those. So you have to install MSVS14+ and libxml2 first, which requires... a solid gitwalk, but if you're persistent then start from looking at the error messages:

    pypy3 -m ensurepip
    pypy3 -m pip install --upgrade pip
    pypy3 -m pip install keyboard requests_html

## Options
```
-h, --help            show this help message and exit
-c X, --config X      an ini file with the settings (default: ./sitemon.ini)
-C X, --continuity X  a JSON continuity file (default: ./sitemon.json)
-r X, --report X      the report file (default: ./sitemon.report.txt), "nul" for console-only
-f, --force           force re-check all pages
-t N, --retries N     do N retries downloading a page, -1 for infinite (default: 3)
-p, --pause           waits for a keypress before closing
-s, --sslcheck        perform SSL issue check (default: no checks)
-v, --verbose         verbose console output (multiple allowed)
-q, --quiet           no console output, overrides --verbose (multiple allowed)
```

Please read the sample config file for more instructions.
