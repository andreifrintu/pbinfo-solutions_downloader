#!/usr/bin/python311

import os
import time
import shutil
import requests
import datetime
from art import *
from bs4 import BeautifulSoup

# global variables for main use
_ua_ = ''
_problems_ = 5000 # set a number of solutions you want to download
_counter_ = 0
_headers_ = {
    'User-Agent': _ua_
}

if __name__ == "__main__":

    try:

        def log(message):
            _log_file_ = "script.log"
            _timestamp_ = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            try:
                with open(_log_file_, "a") as log_file:
                    log_file.write(_timestamp_ + " " + message + "\n")
            except Exception as e:
                print(f"Error writing to the log file: {e}")

        # print init information
        tprint("codu", font="graffiti")
        input("Press enter to start running the scrapper @ codulluiandrei.ro")
        time.sleep(0.5)

        log("Application was started [SUCCESS]\n")

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
            shutil.rmtree("pbinfo") # dev only
            os.mkdir("pbinfo")
            print("Directory for solutions already exists!")

        def save_solution(i):
            global _counter_

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
                    log(f"Downloaded source code of the solution for problem with id #{i} [SUCCESS]")
                    _counter_ = _counter_ + 1

        def dl_until(number):
            if 1 <= number <= _problems_:
                # will download from 1 to 5000
                print(f"Downloading {number} sources that are available!")
                # go from source 0 to source 5000 and check availability
                for i in range(_problems_):
                    # download the source code from pbinfo website
                    save_solution(i)
                        
                    if _counter_ == number:
                        print("The number of solutions you specified was downloaded! Exiting the program.")
                        log("Finished downloading - Application was closed [SUCCESS]\n")
                        exit()
                    
            else:
                raise ValueError("Input must be between 1 and 5000")

        def dl_range(number1, number2):
            if 1 <= number1 <= _problems_ and 1 <= number2 <= _problems_:
                # will download from {number1} to {number2}
                print(f"Downloading sources from range [{number1}, {number2}]")
                # go from source {number1} to source {number2}
                for i in range(number1, number2):
                    # download the source code from pbinfo website
                    save_solution(i)
                print("Solutions from the range you specified were downloaded! Exiting the program.")
                log("Finished downloading - Application was closed [SUCCESS]\n")
                exit()
            else:
                raise ValueError("Both numbers must be between 1 and 5000")

        while True:

            # check if the user input one, two, or more / less numbers
            # until it gets a right case (1 or 2 numbers)
            _problems_input_ = input("Enter the number / range of sources you want to download (space-separated): ").split()

            # only one number input
            if len(_problems_input_) == 1:
                try:
                    dl_until(int(_problems_input_[0]))
                    break
                except ValueError as e:
                    print(f"ERROR: {e}. Please enter a valid number!")

            # two numbers input
            elif len(_problems_input_) == 2:
                try:
                    number1, number2 = sorted(map(int, _problems_input_))
                    dl_range(number1, number2)
                    break
                except ValueError as e:
                    print(f"ERROR: {e}. Please enter valid numbers")

            # worst case, zero or more numbers
            else:
                print("ERROR: Invalid input. Please enter either one or two numbers.")

    except KeyboardInterrupt:
        print("\nCTRL + C pressed! Exiting the program.")
        log("CTRL + C - Application was closed [SUCCESS]\n")

