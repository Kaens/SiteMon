#!/usr/bin/env python3

"""
XpathTest is a Tk GUI app where you can quickly and easily test out
your element selector.

The Run button will download the page first if you haven't already,
but otherwise will simply update the Xpath query result.

You need to run the following prior to using the script:
  pip3 install requests_html

Conceived for personal use by Kaens Bard, 2022
Made and tested with CPython v3.10.4 win-x64.

Feedback: @kaens at Telegram
"""

from requests_html import HTMLSession
import tkinter as tk
from tkinter import ttk
import warnings,sys
warnings.filterwarnings("ignore")

def load(url):
    global _req
    global page
    warnings.filterwarnings("ignore")
    try:
        page = _req.get(url,verify=False)
    except Exception as e:
        warnings.filterwarnings("default")
        Info.set(f'Error loading page: {str(e)}')
        return(False)
    warnings.filterwarnings("default")
    Info.set("Page downloaded.")
    return(True)

def performtest(url,xpath):
    global page
    try:
        a = page
    except NameError:
        Info.set("No pages loaded, loading from URL field...")
        if load(url):
            Info.set("Page is loaded now, parsing...")
        else:
            return(False)
    RawElement = page.html.xpath(xpath)
    if RawElement:
        lsResult.delete("1.0",tk.END)
        lsResult.insert(tk.END,RawElement[0].text)#.split('\n'))
        Info.set(f"Found {len(RawElement)} item(s), displaying the first one")
    else:
        lsResult.delete("1.0",tk.END)
        Info.set("Can't find it")

def btLoadCallback():
    global URL
    btLoad.state = tk.DISABLED
    btRun.state = tk.DISABLED
    Info.set('Attempting to load the page...')
    load(URL.get())
    btLoad.state = tk.NORMAL
    btRun.state = tk.NORMAL

# when btRun pressed
def btRunCallback():
    global URL, Xpath
    btLoad.state = tk.DISABLED
    btRun.state = tk.DISABLED
    performtest(URL.get(),Xpath.get())
    btLoad.state = tk.NORMAL
    btRun.state = tk.NORMAL

# GUI init

rt = tk.Tk()
rt.title('Xpath Test for SiteMon')
rt.minsize(400,640)
rt.geometry('400x640')
rt.columnconfigure(0,weight=1)
rt.rowconfigure(0,weight=1)

ui = ttk.Frame(rt)
ui.grid(column=0,row=0,sticky='news')
ui.columnconfigure(0,weight=1)
ui.rowconfigure(0,weight=0)
ui.rowconfigure(1,weight=0)
ui.rowconfigure(2,weight=0)
ui.rowconfigure(3,weight=10)
ui.rowconfigure(0,weight=0)

URL = tk.StringVar()
urlf = ttk.LabelFrame(ui,text='URL:')
urlf.columnconfigure(0,weight=1)
urlf.grid(column=0,row=0,sticky='new')
tbURL = ttk.Entry(urlf,textvariable=URL,exportselection=0)
URL.set('https://python.org')
tbURL.grid(column=0,row=0,sticky='news')
tbURL.focus()

Xpath = tk.StringVar()
xpf = ttk.LabelFrame(ui,text='Xpath:')
xpf.columnconfigure(0,weight=1)
xpf.grid(column=0,row=1,sticky='new')
tbXpath = ttk.Entry(xpf,textvariable=Xpath,exportselection=0)
Xpath.set('/html/body')
tbXpath.grid(column=0,row=0,sticky='news')

btf = ttk.Frame(ui)
btf.grid(column=0,row=2,sticky='new')
btLoad = ttk.Button(btf,text='Load URL',command=btLoadCallback)
btLoad.grid(column=0,row=0)
btRun = ttk.Button(btf,text='Run',command=btRunCallback)
btRun.grid(column=0,row=1)

resf = ttk.LabelFrame(ui,text='Result')
resf.grid(column=0,row=3,sticky='news')
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
lsResult = tk.Text(resf,bg='#000',fg='#ccc',selectbackground='#777',selectforeground='#fff')
lsResult.grid(column=0,row=0,sticky='news')

Info = tk.StringVar()
lbInfo = ttk.Label(ui,textvariable=Info,compound='text',background='#aaa')
Info.set('Input your URL and Xpath. Load page. Run test.')
lbInfo.grid(column=0,row=4,sticky='sew')

#for c in ui.winfo_children():
#    c.grid_configure(padx=5,pady=5)

_req = HTMLSession()
_req.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53"

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

finally:
    ui.mainloop()

_req.close()