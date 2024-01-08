#!/usr/bin/python311

import os
import time
import requests
from art import *
from bs4 import BeautifulSoup

# global variables for main use
_ua_ = ''
_headers_ = {
    'User-Agent': _ua_
}

if __name__ == "__main__":
    
    # print init information
    tprint("codu", font="graffiti")
    input("Press enter to start running the scrapper @ codulluiandrei.ro")
    time.sleep(0.5)

    _ssid_ = input("Enter the login cookie of the account you want to download sources from: ")
    _cookies_ = {
        'SSID': _ssid_
    }

    if os.path.exists("pbinfo"):
        print("Directory for solutions is already created!")
    else:
        os.mkdir("pbinfo")
        print("Directory for solutions was now created!")
