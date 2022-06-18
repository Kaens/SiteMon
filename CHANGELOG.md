# SiteMon changelog

## v1.5 bugfixes in ini.example, SelTest

#### Minor:
  * Fixed the [python] example in the ini.example
  * Fixed the render option and the match amount status bar info in seltest.py
  * Tested on PyPy 3.9 too, setup instructions updated
  * Readme improved
  * A useless to-do retracted for SiteMon


## v1.5

##### Major:

  * Attribute (like "href") tracking added
  * Multiple consecutive matches can now be saved to continuity (yes, you can grab page links with this as `//a[contains(@href,'youtu']` or something like that)


## v1.4

#### Major:
  * CSS selector added
  * XpathTest → SelTest
  * SelTest can test all selector types

#### Important:
  * Better handling of zero hits and missing pages
  * Default UserAgent updated
  * Engine updated to CPython 3.10.5
  * SelTest will reload the page first if you Run after changing the URL


## v1.3

#### Important:
  * Error quits also respect --pause now
  * Fixed the -vv page writeout error
  * Exception prompts do better than say "occurred at (4)" and such
  * A regex continuity now holds the first match instead of a simple boolean tracking any change, so you can see what that change was
  * Clarified the explanation for both Types in the ini example
  * -u/--update → -f/--force


## v1.2

#### Major:
  * Base script-independent Tk GUI-based Xpath testing app added\
    (* required 3rd-party library: requests_html)
    
Base script's version stays at v1.1.


## v1.1

#### Major:
  * Removed the no-JS version since you can just not request JS in the JS version for it to behave the same way
  * CLI option added to wait for a keypress before closing\
    (* requires pip install keyboard)

#### Important:
  * Retries option added for the page downloader tweaking
  * Option added for the now-optional SSL verification

#### Minor:
  * Default UserAgent updated
  * Clarified default file locations a bit for Linux-style (but still untested)


## v1.0
  * Initial release, definitely compatible with Python 3.10.4.\
  (* required 3rd-party libraries: keyboard, requests_html)