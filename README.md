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

For PyPy 3.9 (works faster):

If you're working with Windows, you'll want to install `lxml` from the corresponding wheel first.

Now, a `pp39` wheel for `lxml`... does not exist. Trying to do `pip install lxml` makes pip plop halfway. I built mine for w64, [here](https://github.com/Kaens/SiteMon/releases/download/v1.5/lxml-4.9.0-pp39-pypy39_pp73-win_amd64.whl) (SHA1 = 7f6ca65ad4d6a268777e5c3e594afccc968447d2 :: [malware-free](https://www.virustotal.com/gui/file-analysis/OTk5Zjk1OGQ4YmE5ODM0ZjAwMDk0ZTM5MmQzYzc5YmI6MTY1NTU4NzMyMg==)). Download the file, run cmd.exe in your Download folder, then finally install the prerequisites:

    pypy3 -m ensurepip
    pypy3 -m pip install --upgrade pip
    pypy3 -m pip install lxml-4.9.0-pp39-pypy39_pp73-win_amd64.whl
    pypy3 -m pip install keyboard requests_html

If it breaks, I hope there's an official binary for py39 by then...

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
