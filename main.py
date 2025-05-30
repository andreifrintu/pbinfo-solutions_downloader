#!/usr/bin/python311

import os
import time
import shutil
import requests
import datetime
from art import *
from bs4 import BeautifulSoup

# global variables for main use
_ua_ = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'
_problems_ = 5000 # set a number of solutions you want to download
_ids_ = []
_unique_ = False
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
        _optimization_ = True if input("Do you want only needed solutions [for codulluiandrei.ro]? (Y/n): ").lower() == 'y' else False
        time.sleep(0.5)
        _unique_ = True if input("Do you want unique solutions [from codulluiandrei.ro]? (Y/n): ").lower() == 'y' else False

        print("Optimization variable was set to " + str(_optimization_))
        print("Unique variable was set to " + str(_unique_))
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
                target_element = soup.select_one("pre.code_cpp")

                if _optimization_:
                    _unique_sol_ = False
                else:
                    # if unique problem selection is set
                    if _unique_:
                        # edit variable value depending on website availability
                        _unique_sol_ = False if requests.get(f"https://codulluiandrei.ro/rezolvari/pbinfo/{i}").status_code == 404 else True
                    else:
                        _unique_sol_ = False

                # if the target element is available download source code
                if target_element and not _unique_sol_:
                    # save the source code inside variable
                    extracted_text = target_element.get_text()

                    extracted_text = extracted_text.replace('"\n"', '"\\n"')
                    cleaned_text = "\n".join(line for line in extracted_text.splitlines() if line.strip())
                    extracted_text = cleaned_text

                    # create directory for the new solution
                    if not os.path.isdir(f"pbinfo/pbinfo-{i}"):
                        os.mkdir(f"pbinfo/pbinfo-{i}")
                        # create and write code to file
                        _file_ = f"pbinfo/pbinfo-{i}/main.cpp"
                        with open(_file_, "w", encoding="utf-8") as file:
                            file.write(extracted_text)
                        _ids_.append(i)
                        print(f"Downloaded source code of the solution for problem with id #{i} [SUCCESS]")
                        log(f"Downloaded source code of the solution for problem with id #{i} [SUCCESS]")
                        _counter_ = _counter_ + 1
            else:
                # if the solution is not available, print error message
                print(f"Solution for problem with id #{i} was not found! [ERROR]")
                log(f"Solution for problem with id #{i} was not found! [ERROR]")

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
                        log(', '.join(map(str, _ids_)) + "\n")
                        log("Finished downloading - Application was closed [SUCCESS]\n\n")
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
                log(', '.join(map(str, _ids_)) + "\n")
                log("Finished downloading - Application was closed [SUCCESS]\n\n")
                exit()
            else:
                raise ValueError("Both numbers must be between 1 and 5000")

        def dl_list(numbers):
            for i in numbers:
                save_solution(i)
            print("All the available needed solutions were downloaded! Exiting the program.")
            log(', '.join(map(str, _ids_)) + "\n")
            log("Finished downloading - Application was closed [SUCCESS]\n\n")
            exit()

        if _optimization_:
            # download all the solutions found at this web url
            # list of all needed solutions from 0 to 5000
            dl_list([int(i) for i in requests.get('https://ajax.codulluiandrei.ro/ajax/needed.php').text.split(',')])

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
        log("CTRL + C - Application was closed [SUCCESS]\n\n")

