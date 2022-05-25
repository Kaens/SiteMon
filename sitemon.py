#!/usr/bin/env python3

"""
SiteMon tracks changes in specific DOM elements on the sites
as set up in the ini file, rendering the JS in them first.

As output, it outputs to stdout the space-separated list of "pages"
that changed, as well as adds them to a report file with timestamps.

Please run the script with "--help" and read the sample config file
for more instructions.

You can specify -v and -q several times (or like -vv -qq).

The script renders JS using Chromium, so it will download Chromium
to ~/.pyppeteer (or %LOCALAPPDATA%/pyppeteer/) on first JS request.

You need to run the following prior to using the script:
  pip3 install keyboard
  pip3 install requests_html

Conceived for personal use by Kaens Bard, 2022
Made and tested with CPython v3.10.4 win-x64.

Feedback: @kaens at Telegram


TODO:
  - make regex make a bit more sense, like save the first hit or something
  - defer the pre-parsing to BeautifulSoup because who knows how broken the tracked pages are
"""

SiteMonVersion = "1.1"

import argparse, re, os, json, struct, sys, keyboard, warnings
from datetime import datetime, timedelta
from configparser import ConfigParser
from requests_html import HTMLSession
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def main():
    ConfFN = './sitemon.ini'
    ContFN = './sitemon.json'
    ReportFN = './sitemon.report.txt'
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"
    Referer = ''
    H = {} # continuity, short for 'history'
    UpdatedPages = []

    optp = argparse.ArgumentParser(prefix_chars='/-',description="Tracks changes in the specific site elements for you.\nJS works. Passworded pages and cookie logins do not.",epilog=f'SiteMon v{SiteMonVersion}')
    optp.add_argument('-c','--config', dest='ConfFile',action='store',metavar='X',help=f"an ini file with the settings (default: {ConfFN})")
    optp.add_argument('-C','--continuity', dest='ContFile',action='store',metavar='X',help=f"a JSON continuity file (default: {ContFN})")
    optp.add_argument('-r','--report', dest='ReportFile',action='store',metavar='X',help=f'the report file (default: {ReportFN}), \"nul\" for console-only')
    optp.add_argument('-u','--update', dest='U',action='store_true',help="check all pages regardless of the Frequency setting")
    optp.add_argument('-t','--retries',dest='Retries',type=int,metavar='N',help="how many retries to do downloading the pages, -1 for infinite (default: 3)")
    optp.add_argument('-p','--pause',dest='Pause',action='store_true',help="waits for a keypress before closing")
    optp.add_argument('-s','--sslcheck',dest='VerifySSL',action='store_true',help="perform SSL issue check (default: no checks)")
    optp.add_argument('-v','--verbose', dest='V',action='count',default=0,help="verbose console output (multiple allowed)")
    optp.add_argument('-q','--quiet', dest='Q',action='count',default=0,help="no console output, overrides --verbose (multiple allowed)")
    #process arguments, optionally show help and quit:
    o = optp.parse_args()
    if o.V>1 and o.Q==0:
        print(o)
    #set up the config filename
    if o.ConfFile:
        ConfFN = o.ConfFile

    if not os.path.exists(ConfFN):
        if o.Q==0:
            print('Copy the sitemon.ini.example to sitemon.ini, and make adjustments using the sample settings')
        return(1)

    # ---- load the ini file (but the commmand line takes priority) ---
    try:
        if o.Q==0:
            print('Reading configuration...')
        conf = ConfigParser()
        conf.read(ConfFN)
        if not o.ContFile:
            ContFN = conf.get('Main','ContinuityFile',fallback=ContFN)
        if not o.Retries:
            Retries = conf.get('Main','Retries',fallback=3)
        if not o.ReportFile:
            ReportFN = conf.get('Main','ReportFile',fallback=ReportFN)
        UserAgent = conf.get('Main','UserAgent',fallback=UserAgent)
        Pages = conf.get('Main','Pages',fallback='').replace(' ','').split(',')
    except Exception as e:
        if o.Q==0:
            print("Exception occurred: "+str(e))
        return(1)

    # --- override the ini file values (separate because it's outside of "try")
    if o.ContFile:
        ContFN = o.ContFile
    if o.ReportFile:
        ReportFN = o.ReportFile
    if o.Retries:
        if o.Retries < 0:
            Retries = None
        else:
            Retries = o.Retries
    if Retries == -1:
        Retries = None

    if o.V>0 and o.Q==0:
        print(f'Pages to check: {Pages}')

    if o.Q==0:
        print('Loading continuity...')
    try:
        H = json.load(open(ContFN,encoding='utf-8-sig'))
    except FileNotFoundError:
        if o.Q==0:
            print("The continuity file was not found and will be created.")
    except Exception as e:
        if o.Q==0:
            print("Exception occurred: "+str(e))
        return(2)

    # ---- init a browser session----

    warnings.filterwarnings("ignore") # urllib3's Retry is obsolete and drops a warning
    retry_strategy = Retry(
        total=Retries, read=Retries, connect=Retries, # simplifying it all
        redirect=10,
        backoff_factor=0.2,
        status_forcelist=[413, 429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    httpadapter = HTTPAdapter(max_retries=retry_strategy)
    session = HTMLSession(mock_browser=False)
    session.mount("https://", httpadapter)
    session.mount("http://", httpadapter)
    warnings.filterwarnings("default")


    # ---- Main loop begins ---- #

    for Page in Pages:

        if o.V>0 and o.Q==0:
            print(f'Processing entry "{Page}"...')

        Updated = False

        try:
            URL = conf.get(Page,'URL')
        except:
            if o.V>0 and o.Q==0:
                print(f"{Page}'s URL parameter invalid, skipping...")
            continue

        try:
            JS = conf.getboolean(Page,'JS')
        except:
            JS = False
        if not o.VerifySSL:
            try:
                VerifySSL = conf.getboolean(Page,'VerifySSL')
            except:
                VerifySSL = False
        else:
            VerifySSL = True
        if VerifySSL:
            warnings.filterwarnings("default")
        else:
            warnings.filterwarnings("ignore")
        try:
            Referer = conf.get(Page,'Referer')
        except:
            Referer = ''

        Type = conf.get(Page,'Type').lower()
        if Type not in ('xpath','regex'):
            if o.V>0 and o.Q==0:
                print(f"{Page}'s type parameter invalid, skipping...")
                continue

        Search = conf.get(Page,'Search')

        if not o.U: # the following only applies if we're not force updating
            Frequency = conf.get(Page,'Frequency')
            try:
                Frequency = int(Frequency)
            except:
                if o.V>0 and o.Q==0:
                    print(f"{Page}'s Frequency parameter invalid, using 1 minute")
                Frequency = 1
            if Frequency <= 0:
                DTcmp = datetime.fromisoformat('9999-12-31')
            else:
                DTcmp = datetime.now() - timedelta(minutes=Frequency)

            if Page in H:
                try:
                    DT = datetime.fromisoformat(H[Page]["last_checked"])
                except:
                    DT = datetime.now()
            else:
                #a new page that must be added and not skipped
                DT = datetime.fromisoformat('1970-01-01')

            if DTcmp < DT:
                if o.V>0 and o.Q==0:
                    print(f"It's not yet the time to check {Page}, skipping...")
                continue

        # ---- if it's time to check again: ----
        try:
            if o.V>0 and o.Q==0:
                print(f'Reading up the "{Page}" page...')

            session.headers['User-Agent'] = UserAgent
            if Referer != '':
                session.headers['Referer'] = Referer
            r = session.get(URL,verify=VerifySSL)
            if JS:
                r.html.render() # executes the js
            if o.V>1 and o.Q==0:
                print(f'Saving the page to {Page}.html...')
                open(f'{Page}.html','w',encoding='utf-8').write(res.text)
        except Exception as e:
            if o.Q==0:
                print(f"Exception occurred at (4): {str(e)}. Moving on...")
            del e
            continue

        # ---- if url load succeeded: ----
        try:
            if o.V>0 and o.Q==0:
                print(f'Picking the requested element...')
            if o.V>1 and o.Q==0:
                print(f'The search is {Search}')
            if Type == "xpath":
                RawElement = r.html.xpath(Search)
                if RawElement:
                    Element = RawElement[0].text
            elif Type == "regex":
                rf = re.findall(Search,r.text)
                if rf:
                    Element = len(rf)
                else:
                    Element = 0
            if o.V>1 and o.Q==0:
                print(f'The element is {Element}')
        except Exception as e:
            if o.Q==0:
                print(f"Exception occurred at (5): {str(e)}. Moving on...")
            del e
            continue

        # ---- if xml element pick succeeded: ----
        if Page in H:
            if H[Page]["element"] != Element:
                Updated = True
                if o.V>0 and o.Q==0:
                    print(f'Element updated since {H[Page]["element"]}')
            else:
                if o.V>0 and o.Q==0:
                    print(f'Element has not changed')
        else:
            if o.Q==0:
                print(f'Storing "{Page}" in the continuity...')
        H[Page] = {
            "last_checked": datetime.now().isoformat(),
            "element": Element
        }
        if Updated:
            UpdatedPages.append([Page,H[Page]["last_checked"]])

    # ---- Main loop ends ----

    if o.V>1 and o.Q==0:
        print(H)
    if o.Q==0:
        print(f'Saving continuity as {ContFN}...')
    try:
        json.dump(H,open(ContFN,'w',encoding='utf-8-sig'),indent=2)
    except Exception as e:
        if o.Q==0:
            print("Exception occurred at (3): "+str(e))
        return(3)

    if o.Q==0:
        if len(UpdatedPages)==0:
            print(f'No updates.')
        else:
            if ReportFN.lower() != 'nul':
                print(f'Saving the list of updated pages to {ReportFN}...')
    try:
        open(ReportFN,'a',encoding="utf-8").write('\n'.join(f"{a[0]} {a[1]}" for a in UpdatedPages))
    except Exception as e:
        if o.Q==0:
            print("Exception occurred at (6): "+str(e))
        return(6)

    #print the updates to stdout
    if o.Q<2:
        sys.stdout.write(' '.join(a[0] for a in UpdatedPages))

    if o.V>0 and o.Q==0:
        print('All done.')

    if o.Pause:
        a = keyboard.read_key()


if __name__=="__main__":
    main()
