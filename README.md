# SiteMon
SiteMon tracks changes in specific DOM elements on the sites as set up in the ini file, using Xpath or regex.
JS is supported. Passworded pages and browser cookies are not, yet. Definitely works on Python 3.10.4.

As output, it sends to stdout the space-separated list of "pages" that changed, as well as adds them to a report file with timestamps.

The script renders JS using Chromium, so it will download Chromium to ~/.pyppeteer (or %LOCALAPPDATA%/pyppeteer/) on first JS request.

You need to run the following prior to using the script:
  - pip3 install keyboard
  - pip3 install requests_html

## Options
```
  -h, --help            show this help message and exit
  -c X, --config X      an ini file with the settings (default: ./sitemon.ini)
  -C X, --continuity X  a JSON continuity file (default: ./sitemon.json)
  -r X, --report X      the report file (default: ./sitemon.report.txt), "nul" for console-only
  -u, --update          check all pages regardless of the Frequency setting
  -t N, --retries N     do N retries downloading a page, -1 for infinite (default: 3)
  -p, --pause           waits for a keypress before closing
  -s, --sslcheck        perform SSL issue check (default: no checks)
  -v, --verbose         verbose console output (multiple allowed)
  -q, --quiet           no console output, overrides --verbose (multiple allowed)
```

Please read the sample config file for more instructions.
