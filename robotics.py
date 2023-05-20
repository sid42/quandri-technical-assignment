from RPA.Browser.Selenium import Selenium
from datetime import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch import Elasticsearch
from botcmd import BotCmd
import time
import re
import os
import threading

WIKI_LINK = "https://en.wikipedia.org/wiki/{}"
DATE_REGEX = r'\b\d{1,2}\s+[A-Za-z]+\s+\d{4}\s+'
BIO_XPATH = "//*[@id=\"mw-content-text\"]/div[1]/p[normalize-space()]"
DOB_XPATH = "//table[contains(@class, 'infobox') and contains(@class, 'biography') and contains(@class, 'vcard')]//th[contains(text(), 'Born')]/following-sibling::td[1]"
DOD_XPATH = "//table[contains(@class, 'infobox') and contains(@class, 'biography') and contains(@class, 'vcard')]//th[contains(text(), 'Died')]/following-sibling::td[1]"

ALREADY_EXISTS_ERR = 400 
INDEX_NAME = 'quandri-scientists'
ES_HOST = format(os.getenv('ES_HOST', 'localhost'))

class Robot:
    def __init__(self, name):
        self.name = name
        self.br = Selenium()
        self.es = Elasticsearch([{'host': ES_HOST, 'port': 9200, 'scheme':'http'}])
        self.bot_cmd = BotCmd(self.cmd_search_func, self.get_scientists_info_from_wiki)
        self.es.indices.create(index=INDEX_NAME, ignore=[ALREADY_EXISTS_ERR])

    def say_hello(self):
        print("Hello, my name is", self.name, "\n")
    
    def say_goodbye(self):
        print("Goodbye, my name is", self.name, "\n")

    def get_scientists_info_from_wiki(self, scientists):
        self.br.open_available_browser()
        for scientist in scientists: 
            self.br.go_to(WIKI_LINK.format(scientist.replace(" ", "_")))
            bio = self.br.get_text(BIO_XPATH)
            dob_dirty = self.br.get_text(DOB_XPATH)
            dod_dirty = self.br.get_text(DOD_XPATH)

            dod_match = re.search(DATE_REGEX, dod_dirty)
            dob_match = re.search(DATE_REGEX, dob_dirty)
            dod, dob = None, None
            if dob_match: 
                dob = datetime.strptime(dob_match.group().strip(), '%d %B %Y')
            if dod_match: 
                dod = datetime.strptime(dod_match.group().strip(), '%d %B %Y')

            result = {
                "name" : scientist,
                "bio" : bio, 
                "birth" : dob, 
                "death" : dod, 
                "age" : relativedelta(dod, dob).years
            }

            self.es.index(index=INDEX_NAME, body=result)
        br.close_browser()

    def print_scientists_info(self):
        query = {
            "query": {
                "match_all": {}
            }
        }
        result = self.get_scientists_info_from_es(query)

        for scientist_data in result: 
            print("Here is some information about", scientist_data['name'])
            print("Bio: ", scientist_data["bio"])
            print("Date of Birth: ", scientist_data["birth"])
            print("Date of Death: ", scientist_data["death"])
            print("Age: ", scientist_data["age"], "\n\n")

    def cmd_search_func(self, text): 
        query = {
            "query": {
                "query_string": {
                    "query": text
                }
            }
        }
        return self.get_scientists_info_from_es(query)
        

    def get_scientists_info_from_es(self, query): 
        response = self.es.search(index=INDEX_NAME, body=query)
        documents = response['hits']['hits']
        return [document['_source'] for document in documents]


    def accept_search_commands(self): 
        self.bot_cmd.cmdloop()




            