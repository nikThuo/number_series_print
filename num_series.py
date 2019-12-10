import random
import sys

import docx
import win32print
import win32ui
import os

def generateCode():
    codes = []

    while len(codes) < 100:
        code = ('%06x' % random.randrange(16**6)).upper()
        if code in codes:
            continue
        else:
            codes += [code]

    return code

def printCode():
    c = generateCode()
    printer_name = win32print.GetDefaultPrinter()
    print(printer_name)
    hPrinter = win32print.OpenPrinter(printer_name)
    # print(hPrinter)

    if sys.version_info >= (3,):
        raw_data = bytes(c, "utf-8")
        # print('$$$$$$', c)
    else:
        raw_data = c
        # print('$$$$$$', c)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, (c, None, "RAW"))
        # print('$$$$$$', c)
        try:
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, raw_data)
            win32print.EndPagePrinter(hPrinter)
        finally:
            win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)


    # print(os.path.abspath(str(c)))
    # # os.startfile(os.path.abspath(str(c)))
    # os.system('start c')

printCode()
