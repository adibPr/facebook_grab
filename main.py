#!/usr/bin/env python3

# sys module
import time
import csv
import logging
import os
import sys
import configparser
import csv
from urllib import parse

# third parties module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.remote.remote_connection import LOGGER
import pandas as pd

class FacebookGrab (object) : 


    def __init__ (self, **kwargs) : 
        # set profile 
        fp = webdriver.FirefoxProfile()
        fp.set_preference ('dom.webnotifications.enabled', False)
        self.driver = webdriver.Firefox (fp)

        # load basic arguments
        self.kwargs = kwargs
        self.kwargs['min_char'] = kwargs.get ('min_char', 1000)
        self.kwargs['max_post'] = kwargs.get ('max_post', 200)
        self.kwargs['save_file'] = kwargs.get ('save_file', 'out.csv')
        self.counter = 0 # counter how many post meet this criteria

        self.buff = open (self.kwargs['save_file'], 'w')
        self.writer = csv.writer (self.buff)

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

    def process (self, keyword) : 
        # login
        self.do_login ()

        # change address to search query url 
        self.driver.get (self.get_search_address (keyword))

        self.get_posts ()

    def get_search_address (self, addr) : 
        date_option = r'{"name":"creation_time","args":"{\"start_year\":\"2018\",\"start_month\":\"2018-01\",\"end_year\":\"2018\",\"end_month\":\"2018-12\"}"}'
        WITH_DATE = '?filters_rp_creation_time=' + parse.quote (date_option)

        # for public post
        PUBLIC_STORIES = 'https://www.facebook.com/search/str/{}/stories-keyword/stories-public'
        # for friends
        FRIEND_STORIES = 'https://www.facebook.com/search/str/{}/keywords_blended_posts?filters_rp_author=stories-feed-friends'
        return PUBLIC_STORIES.format ('+'.join (addr.split (' '))) + WITH_DATE

    def get_posts (self) :
        # scrolling taken from : 
        # https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python

        last_index = 0
        last_indexes = [None, None, None, None, None]
        while True : 
            content_wrappers = self.driver.find_elements_by_class_name ('userContentWrapper')
            print ("content {}-{}".format (last_index, len (content_wrappers)))

            for cw in content_wrappers[last_index:] : 
                props = self.process_post (cw)
                print (len (props['text']))
                if len (props['text']) >= self.kwargs['min_char'] : 

                    # write
                    self.writer.writerow ([props[_] for _ in ('date', 'username', 'text')])
                    print ("Write it")

                    # increase counter
                    self.counter += 1
            
            # scroll page a little bit
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep (3)
            last_index = len (content_wrappers)

            if self.counter >= self.kwargs['max_post'] : 
                self.buff.close ()
                break

            # exit loop when no more post found
            last_indexes.insert (0, last_index)
            last_indexes = last_indexes[:5]
            if all ([_ == last_indexes[0] for _ in last_indexes]) : 
                break

    def process_post (self, cw) : 
        post = {}
        # first scroll into view
        self.driver.execute_script ("arguments[0].scrollIntoView ();", cw)

        # get some basic username and time of post
        post['username'] = cw.find_element_by_class_name ('fwn.fcg').text
        post['date'] = cw.find_element_by_class_name ('timestampContent').text

        # get actual content
        content = cw.find_element_by_class_name ('userContent')
        # check if it has "see more" link
        see_more = content.find_elements_by_class_name ("see_more_link_inner")
        if see_more : 
            # if yes, then click it
            see_more[0].click ()
        user_content = cw.find_element_by_class_name ('userContent')
        post['text'] = user_content.text

        # TODO : check if it has link to post (like continue to read)
        """
        cont_read = user_content.find_elements_by_class_name ('text_exposed_link')
        if cont_read : 
            print (content)
            print (cont_read[0].text)
            # if yes, open a new tab, and then open it in there
            url = cont_read[0].get_attribute ("href")
            print (url)
        """

        return post

def test_1 () : 
    FG = FacebookGrab ()
    FG.process ('jokowi')

if __name__ == '__main__' : 
    test_1 ()
