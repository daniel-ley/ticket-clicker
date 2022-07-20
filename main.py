#!/usr/bin/python3

from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from time import sleep
import re
import webbrowser as wb

URL = ""
SEARCH_TERM = ""

SEARCH_PATTERN = [SEARCH_TERM.title(), SEARCH_TERM.upper(), SEARCH_TERM.lower()]

check_frequency_minutes = 5

failsafe = 0
hours_to_run = 12
number_of_iterations = (hours_to_run * 60) / check_frequency_minutes

user_agents = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}


def check_page(url, headers, search_pattern):
    print(f"Page Checked at:  {datetime.now().strftime('%H:%M:%S')}")

    with get(url, headers=headers) as response:
        # if (response.status_code != 200 and
                response.text.rstrip()[-8:].lower() != "</html>" or
                len(response.text) == 0):
            print("... and a PROBLEM was encountered")
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            matches = soup.find_all(string=re.compile(search_pattern))
            if len(matches) > 0:
                return str(matches[0]).strip()


running = True
while running:
    for i in range(0, len(SEARCH_PATTERN)):
        print(i)
        page_check = check_page(URL, user_agents, SEARCH_PATTERN[i])
        if page_check:
            print(page_check)
            wb.open(URL)
            running = False
        else:
            failsafe += 1
            if failsafe >= number_of_iterations:
                running = False

    print(f"Checked sleeping for {str(check_frequency_minutes)} minutes")
    sleep(check_frequency_minutes * 60)
