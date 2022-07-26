from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from time import sleep
import re
import webbrowser as wb

URL = "http://www.google.com"
SEARCH_TERM = "google"

SEARCH_PATTERNS = [SEARCH_TERM.title(), SEARCH_TERM.upper(),
        SEARCH_TERM.lower()]

USER_AGENTS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/39.0.2171.95 Safari/537.36'}

#Control Params
CHECK_FREQUENCY_MINUTES = 5
HOURS_TO_RUN = 12
NUMBER_OF_ITERATIONS = (HOURS_TO_RUN * 60) / CHECK_FREQUENCY_MINUTES


class page_monitor_agent:
    def __init__(self, page, iterations, search, freq):
        self.page = page
        self.iterations = iterations
        self.search = search
        self.freq = freq
        self.monitor(self.page, self.iterations, self.search, self.freq)


    def check_page(self, url, headers, search_pattern):
        print(f"Page Checked at:  {datetime.now().strftime('%H:%M:%S')}")

        with get(url, headers=headers) as response:
            if (response.status_code != 200 and
                    response.text.rstrip()[-8:].lower() != "</html>" or
                    len(response.text) == 0):
                print("... and a PROBLEM was encountered")
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                matches = soup.find_all(string=re.compile(search_pattern))
                if len(matches) > 0:
                    return str(matches[0]).strip()


    def monitor(self, url, number_of_iterations, search_patterns, check_frequency_minutes):
        running = True
        failsafe = 0
        while running:
            for i, search_pattern in enumerate(search_patterns):
                print(f'{i}. Checking for "{search_pattern}" on page: {url}')
                page_check = self.check_page(url, USER_AGENTS, search_pattern)
                if page_check:
                    print(page_check)
                    wb.open(URL)
                    running = False
                    break
                else:
                    failsafe += 1
                    if failsafe >= number_of_iterations:
                        running = False

            print(f"Check Again in {str(check_frequency_minutes)} minutes")
            sleep(check_frequency_minutes * 60)


if __name__ == "__main__":
    monitor_agent = page_monitor_agent(URL, NUMBER_OF_ITERATIONS, 
                                        SEARCH_PATTERNS, 
                                        CHECK_FREQUENCY_MINUTES)

