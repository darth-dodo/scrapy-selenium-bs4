#urban dictionary homepage downloader


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from collections import OrderedDict
import pymongo
import argparse

class UrbanDictScraper():
    def __init__(self):

        self.client = pymongo.MongoClient('localhost',27017)
        self.db = self.client['urbana']
        self.collection = self.db['default']

        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.header = { 'User-Agent' : self.user_agent }
        self.PAUSE = 3


    def contentGen(self, Url = "http://www.urbandictionary.com", pages = 10):

        # Load webdriver
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", self.user_agent)
        browser = webdriver.Firefox(profile)
        # browser.set_window_size(480, 320)
        browser.set_window_position(800, 0)

        print "Loading Urban Dict..."
        # load Urban Dict and wait for PAUSE
        browser.get(Url)
        browser.implicitly_wait(self.PAUSE)

        elem = browser.find_element_by_tag_name("body")

        no_of_pagedowns = int(pages)
        while no_of_pagedowns:
	   elem.send_keys(Keys.PAGE_DOWN)
	   time.sleep(2)
	   no_of_pagedowns -= 1
	   print 'pages left ~ ', no_of_pagedowns

        browser.close()

        words_raw = browser.find_elements_by_class_name("word")
        meanings_raw = browser.find_elements_by_class_name("meaning")
        examples_raw = browser.find_elements_by_class_name("example")

        words = [words_raw[i].text.encode('utf-8') for i,enum in enumerate(words_raw)]
        meanings = [meanings_raw[i].text.encode('utf-8') for i, enum in enumerate(meanings_raw)]
        examples = [examples_raw[i].text.encode('utf-8') for i, enum in enumerate(examples_raw)]


        urban_list = list(zip(words, meanings, examples))



        return urban_list

    def mongoColl(self,urban_data, collName = 'urbana'):

        print self.collection
        self.collection = self.db[collName]
        print self.collection

        for i,items in enumerate(urban_data):
            print urban_data[i]
            self.collection.update({"word":urban_data[i][0]},
                                       {"word" : urban_data[i][0]
                                        ,"meaning" : urban_data[i][1]
                                        ,"example" : urban_data[i][2]
                                        },upsert = True)

        # words_meanings = dict(zip(words, meanings))

        # print (json.dumps(words_meanings, indent=4))

        def validURL(self,url):
            if "urbandictionary.com" in url:
                return True



if __name__ == '__main__':

    ready = False

    parser = argparse.ArgumentParser(description="Urban dictionary scraper")

    parser.add_argument('-u','--URL',help=' Optional Urban dictionary URL... Default is homepage. (www.urbandictionary.com)',required=False)

    parser.add_argument('-p','--pages', type=int,
                        help='Number of pagedowns scraped. Default is 10',
                        required=False)

    parser.add_argument('-o','--output',help='output format preferred. Valid entries "json","csv" ',
                        required=False)

    parser.add_argument('-c','--collName', help='MongoDB collection name for Database UrbanDict. Default is urbanD',required=False)

    args = parser.parse_args()

    s_urban = UrbanDictScraper()

    if (args.URL):
        input_url = args.URL
        print 'valid url'

        #basic validation
        if(s_urban.validURL(input_url)):
            ready = True
        else:
            print r"Please enter a valid url from site ~\nhttp://www.urbandictionary.com"

        #downloading data
    if(args.pages and ready == True):
        pages = int(args.pages)
        print 'Downloading data from ',input_url,'for ',pages,' pagedowns'
        s_output = s_urban.contentGen(input_url, pages)

    elif (ready == True):
        print 'Default page downs is 10.. Data from 10 page downs..'
        s_output = s_urban.contentGen(input_url)

    else:
        print 'Downloading data from urbandictionary homepage'
        s_output = s_urban.contentGen()


            #projecting the data:
    if (args.collName):
        print 'Data present in ', args.collName,'collection of MongoDB'
        s_urban.mongoColl(s_output,args.collName)
    else:
        print 'Data in default "Urbana" collection'
        s_urban.mongoColl(s_output)


