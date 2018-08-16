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
        self.keyword = ['jokowi', 'prabowo', '2019gantipresiden']
        self.driver = webdriver.Firefox ()
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


def test_1 () : 
    FG = FacebookGrab ()
    FG.do_login ()

if __name__ == '__main__' : 
    test_1 ()
