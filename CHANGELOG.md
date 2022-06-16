SiteMon changelog

v1.4

  + CSS selector added
  * Better handling of zero hits and missing pages
  * Default UserAgent updated
  * Engine updated to CPython 3.10.5
  * XpathTest → SelTest
  + SelTest can test all selector types
  * SelTest will reload the page first if you Run after changing the URL

v1.3

  * Error quits also respect --pause now
  * Fixed the -vv page writeout error
  * Exception prompts do better than say "occurred at (4)" and such
  * A regex continuity now holds the first match instead of a simple boolean tracking any change, so you can see what that change was
  * Clarified the explanation for both Types in the ini example
  * -u/--update → -f/--force

v1.2

  + Base script-independent Tk GUI-based Xpath testing app added
    (* required 3rd-party library: requests_html)
  Base script's version stays at v1.1.

v1.1
  - Removed the no-JS version since you can just not request JS in 
  the JS version for it to behave the same way
  + CLI option added to wait for a keypress before closing
    (* requires pip install keyboard)
  + Retries option added for the page downloader tweaking
  + Option added for the now-optional SSL verification
  * Default UserAgent updated
  * Clarified default file locations a bit for Linux-style (but still untested)

v1.0

  Initial release, definitely compatible with Python 3.10.4.
  (* required 3rd-party libraries: keyboard, requests_html)