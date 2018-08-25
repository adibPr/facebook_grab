#!/usr/bin/env python3

# sys module
import time
import csv
import logging
import os
import sys
import configparser

# third parties module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.remote.remote_connection import LOGGER
import pandas as pd

class FacebookGrab (object) : 


    def __init__ (self, **kwargs) : 
        self.keywords = ['jokowi', 'prabowo', '2019gantipresiden']

        # set profile 
        fp = webdriver.FirefoxProfile()
        fp.set_preference ('dom.webnotifications.enabled', False)
        self.driver = webdriver.Firefox (fp)

        # load account
        self.load_account (kwargs.get ('path_account', './account.ini'))

    def do_login (self) : 
        self.driver.get ('https://www.facebook.com/')

        # fill username
        self.driver.find_element_by_xpath ('//*[@id="email"]').send_keys (self.account['username'])
        # fill password 
        self.driver.find_element_by_xpath ('//*[@id="pass"]').send_keys (self.account['password'])
        # wait for 3 sec to click button
        time.sleep (3)
        # click login 
        self.driver.find_element_by_id ('loginbutton').click ()

    def load_account (self, path) : 
        config  = configparser.ConfigParser ()
        config.read (path)
        self.account = config['account']

    def process (self) : 
        # login
        self.do_login ()

        # change address to search query url 
        self.driver.get (self.get_search_address (self.keywords[0])) 

        self.get_posts ()

    def get_search_address (self, addr) : 
        # for public post
        PUBLIC_STORIES = 'https://www.facebook.com/search/str/{}/stories-keyword/stories-public'
        # for friends
        FRIEND_STORIES = 'https://www.facebook.com/search/str/{}/keywords_blended_posts?filters_rp_author=stories-feed-friends'
        return FRIEND_STORIES.format ('+'.join (addr.split (' ')))

    def get_posts (self) :
        elemets = self.driver.find_elements_by_class_name ('userContent')
        print (len (elemets))
        for e in elemets : 
            see_more = e.find_elements_by_class_name ("see_more_link_inner")
            if see_more : 
                see_more[0].click ()
            print (e.text)
        

def test_1 () : 
    FG = FacebookGrab ()
    FG.process ()

if __name__ == '__main__' : 
    test_1 ()
