import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
from collections import OrderedDict

browser = webdriver.Firefox()
browser.get("http://www.urbandictionary.com")
time.sleep(10)
elem = browser.find_element_by_tag_name("body")
no_of_pagedowns = 10

while no_of_pagedowns:
	elem.send_keys(Keys.PAGE_DOWN)
	time.sleep(2)
	no_of_pagedowns -= 1
	print 'pages left ~ ', no_of_pagedowns

words_raw = browser.find_elements_by_class_name("word")
meanings_raw = browser.find_elements_by_class_name("meaning")

words = [words_raw[i].text.encode('utf-8') for i,enum in enumerate(words_raw)]
meanings = [meanings_raw[i].text.encode('utf-8') for i, enum in enumerate(meanings_raw)]

words_meanings = OrderedDict(zip(words, meanings))

print (json.dumps(words_meanings, indent=4))

