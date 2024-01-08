#!/usr/bin/python311

import os
import time
import requests
from art import *
from bs4 import BeautifulSoup

# global variables for main use
_ua_ = ''
_problems_ = 5000 # set a number of solutions you want to download
_headers_ = {
    'User-Agent': _ua_
}

if __name__ == "__main__":
    
    # print init information
    tprint("codu", font="graffiti")
    input("Press enter to start running the scrapper @ codulluiandrei.ro")
    time.sleep(0.5)

    # get the user account login cookie to connect the scapper
    _ssid_ = input("Enter the login cookie of the account you want to download sources from: ")
    _cookies_ = {
        'SSID': _ssid_
    }

    # create or confirm directory for sources to be downloaded
    if not os.path.isdir("pbinfo"):
        os.mkdir("pbinfo")
        print("Directory for solutions was now created!")
    else:
        print("Directory for solutions already exists!")

    _counter_ = 0
    if _ssid_ != '':
        # for loop through all the problems
        for i in range(_problems_):

            # download the source code from pbinfo website
            _ev_addr_ = f"https://www.pbinfo.ro/?pagina=solutie-oficiala&id={i}"
            response = requests.get(_ev_addr_, headers=_headers_, cookies=_cookies_)

            if response.status_code == 200:

                # if solution can be found download it
                soup = BeautifulSoup(response.text, 'html.parser') # extract all html code from the page
                # select the target element from the page content
                target_element = soup.select_one("#zona-mijloc > div > div:nth-child(12) > div.col-lg-9.col-md-9 > pre")

                # if the target element is available download source code
                if target_element:
                    # save the source code inside variable
                    extracted_text = target_element.get_text()
                    # create directory for the new solution
                    if not os.path.isdir(f"pbinfo/pbinfo-{i}"):
                        os.mkdir(f"pbinfo/pbinfo-{i}")
                        # create and write code to file
                        _file_ = f"pbinfo/pbinfo-{i}/main.cpp"
                        with open(_file_, "w", encoding="utf-8") as file:
                            file.write(extracted_text)
                        print(f'Downloading source code of the solution for problem with id #{i}')

