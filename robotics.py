from RPA.Browser.Selenium import Selenium
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import re

DATE_REGEX = r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\s+'
BIO_XPATH = "//*[@id=\"mw-content-text\"]/div[1]/p[normalize-space()]"
DOB_XPATH = "//table[contains(@class, 'infobox') and contains(@class, 'biography') and contains(@class, 'vcard')]//th[contains(text(), 'Born')]/following-sibling::td[1]"
DOD_XPATH = "//table[contains(@class, 'infobox') and contains(@class, 'biography') and contains(@class, 'vcard')]//th[contains(text(), 'Died')]/following-sibling::td[1]"

class Robot:
    def __init__(self, name):
        self.name = name
        self.browser = Selenium()
        self.browser.open_available_browser()

    def say_hello(self):
        print("Hello, my name is", self.name, "\n")
    
    def say_goodbye(self):
        print("Goodbye, my name is", self.name, "\n")

    def open_and_parse(self, webpage):
        self.browser.execute_javascript("window.open()")
        self.browser.go_to(webpage)
        bio = self.browser.get_text(BIO_XPATH)
        dob_dirty = self.browser.get_text(DOB_XPATH)
        dod_dirty = self.browser.get_text(DOD_XPATH)

        dod_match = re.search(DATE_REGEX, dod_dirty)
        dob_match = re.search(DATE_REGEX, dob_dirty)
        dod, dob = None, None
        if dob_match: 
            dob = datetime.strptime(dob_match.group().strip(), '%d %B %Y')
        if dod_match: 
            dod = datetime.strptime(dod_match.group().strip(), '%d %B %Y')

        return {
            "bio" : bio, 
            "birth" : dob, 
            "death" : dod, 
            "age" : relativedelta(dod, dob).years
        }