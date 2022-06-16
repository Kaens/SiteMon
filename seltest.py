#!/usr/bin/env python3

"""
SelTest is a Tk GUI app where you can quickly and easily test out
your element selector.

The Run button will download the page first if you haven't already,
but otherwise will simply update the selector query result.

You need to run the following prior to using the script:
  pip3 install requests_html

Conceived for personal use by Kaens Bard, 2022
Made and tested with CPython v3.10.5 win-x64.

Feedback: @kaens at Telegram
"""

from requests_html import HTMLSession
import tkinter as tk
from tkinter import ttk,messagebox
import warnings,sys,re
warnings.filterwarnings("ignore")
lasturl = ''
renderclicked=False

def load(url):
    global _req
    global page
    global lasturl
    warnings.filterwarnings("ignore")
    try:
        page = _req.get(url,verify=False)
    except Exception as e:
        warnings.filterwarnings("default")
        Info.set(f'Error loading page: {str(e)}')
        return(False)
    warnings.filterwarnings("default")
    Info.set("Page downloaded.")
    lasturl = url
    return(True)

def performtest(url,sel):
    global page
    global lasturl
    try:
        a = page
    except NameError:
        Info.set("No pages loaded, loading from URL field...")
        if load(url):
            Info.set("Page is loaded now, parsing...")
        else:
            return(False)

    # test passed, but what if we need to load anyway?
    if lasturl != url:
        Info.set("URL changed, reloading...")
        if load(url):
            Info.set("Page is loaded now, parsing...")
        else:
            return(False)

    Element = None
    Type = SelType.get()
    if Type == 'xpath':
        try:
            Element = page.html.xpath(sel)
        except Exception as e:
            Info.set(f"Xpath exception: {str(e)}")
            Element = None
    elif Type == 'css':
        try:
            Element = page.html.find(sel)
        except Exception as e:
            Info.set(f"CSS Selector exception: {str(e)}")
            Element = None
    elif Type == 're':
        try:
            Element = re.findall(sel,page.text)
        except Exception as e:
            Info.set(f"RegEx exception: {str(e)}")
            Element = None
    if Element:
        lsResult.delete("1.0",tk.END)
        if Type == 're':
            lsResult.insert(tk.END,Element[0])
        elif Type in ('xpath','css'):
            lsResult.insert(tk.END,Element[0].text)
        Info.set(f"Found {len(Element)} item(s), displaying the first one")
    else:
        lsResult.delete("1.0",tk.END)
        Info.set("Can't find it")

def btLoadCallback():
    global URL
    btLoad.state = tk.DISABLED
    btRenderJS.state = tk.DISABLED
    btRun.state = tk.DISABLED
    Info.set('Attempting to load the page...')
    load(URL.get())
    btLoad.state = tk.NORMAL
    btRenderJS.state = tk.NORMAL
    btRun.state = tk.NORMAL

def btRenderJSCallback():
    global _req, renderclicked
    btLoad.state = tk.DISABLED
    btRenderJS.state = tk.DISABLED
    btRun.state = tk.DISABLED
    if not renderclicked:
        if messagebox._show("Resource load warning",
          "The first time JS is used in this instance of Python, the script will download a copy of Chromium, which is around 140MB large in y2022. Continue?",
          "warning","okcancel") == 'ok':
            renderclicked = True
    if renderclicked:
        Info.set('Attempting to render the page...')
        try:
            _req.render()
        except Exception as e:
            Info.set(f"Render exception: {str(e)}")
            del e
    btLoad.state = tk.NORMAL
    btRenderJS.state = tk.NORMAL
    btRun.state = tk.NORMAL

# when btRun pressed
def btRunCallback():
    global URL, Sel
    btLoad.state = tk.DISABLED
    btRun.state = tk.DISABLED
    performtest(URL.get(),Sel.get())
    btLoad.state = tk.NORMAL
    btRun.state = tk.NORMAL


# GUI init

rt = tk.Tk()
rt.title('Selector Test for SiteMon')
rt.minsize(400,600)
rt.geometry('400x600')
rt.columnconfigure(0,weight=1)
rt.rowconfigure(0,weight=1)

ui = ttk.Frame(rt)
ui.grid(column=0,row=0,sticky='news')
ui.columnconfigure(0,weight=1)
ui.rowconfigure(4,weight=1)#result

URL = tk.StringVar()
urlf = ttk.LabelFrame(ui,text='URL:')
urlf.columnconfigure(0,weight=1)
urlf.grid(column=0,row=0,sticky='new')
tbURL = ttk.Entry(urlf,textvariable=URL,exportselection=0)
URL.set('https://python.org')
tbURL.grid(column=0,row=0,sticky='news')
tbURL.focus()

SelType = tk.StringVar()
stf = ttk.LabelFrame(ui,text='Selector type:')
stf.grid(column=0,row=1,sticky='new')
rbCSS = ttk.Radiobutton(stf,text='CSS',variable=SelType,value='css')
rbCSS.grid(column=0,row=0,sticky='new')
rbXpath = ttk.Radiobutton(stf,text='Xpath',variable=SelType,value='xpath')
rbXpath.grid(column=1,row=0,sticky='new')
rbRegex = ttk.Radiobutton(stf,text='RegEx',variable=SelType,value='re')
rbRegex.grid(column=2,row=0,sticky='new')
rbXpath.invoke()

Sel = tk.StringVar()
sf = ttk.LabelFrame(ui,text='Selector:')
sf.columnconfigure(0,weight=1)
sf.grid(column=0,row=2,sticky='new')
tbSel = ttk.Entry(sf,textvariable=Sel,exportselection=0)
Sel.set('/html/body')
tbSel.grid(column=0,row=0,sticky='news')

btf = ttk.Frame(ui)
btf.grid(column=0,row=3,sticky='new')
btLoad = ttk.Button(btf,text='Load URL',command=btLoadCallback)
btLoad.grid(column=0,row=0)
btRenderJS = ttk.Button(btf,text='Render JS',command=btRenderJSCallback)
btRenderJS.grid(column=1,row=0)

btRun = ttk.Button(btf,text='Run',command=btRunCallback)
btRun.grid(column=0,row=1)

resf = ttk.LabelFrame(ui,text='Result')
resf.grid(column=0,row=4,sticky='news')
resf.columnconfigure(0,weight=1)
resf.rowconfigure(0,weight=1)
if sys.platform in ('linux','linux2'):
    fnt=('DejaVu Sans',10)
elif sys.platform == 'win32':
    fnt=('Calibri',10)
elif sys.platform == 'darwin':
    fnt=('SF Pro',10)
else:
    fnt=()
lsResult = tk.Text(resf,bg='#000',fg='#ccc',selectbackground='#666',selectforeground='#fff',font=fnt)
lsResult.insert(tk.END,"Here the first element matching your selector will be shown."+
    "\nWhy not play around with selectors (with https://python.org as the playground) if you're new! Here are some suggestions:"+
    "\n CSS (https://waa.ai/csssel):\na\n#content\nul.sitemap>li:last-child li\n"+
    "\n Xpath (https://devhints.io/xpath):\n//*[@id=\"content\"]\n//div[4]\n//button[text()=\"Downloads\"]\n"+
    "\n Regex (https://waa.ai/pyregex):\nmeta.*>\n")
lsResult.grid(column=0,row=0,sticky='news')

Info = tk.StringVar()
lbInfo = ttk.Label(ui,textvariable=Info,compound='text',background='#aaa')
Info.set('Input your URL and selector. Run test.')
lbInfo.grid(column=0,row=4,sticky='sew')

_req = HTMLSession()
_req.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

finally:
    ui.mainloop()

_req.close()