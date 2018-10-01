#!/usr/bin/python3
'''
This module contains submitting function on BZOJ.

This module requires selenium
run `pip3 install selenium --user`.
If you haven't installed pip3, run `sudo apt install python3-pip`.
'''

import time
from selenium import webdriver


def submitFirefox(id, code_path, user_info, quiet):
    '''
    This function starts firefox driver, so make sure firefox is installed.
    Requires geckodriver to interact with firefox
    you can find it on https://github.com/mozilla/geckodriver/releases
    '''
    ojurl = 'https://www.lydsy.com/JudgeOnline'
    option = webdriver.FirefoxOptions()
    option.set_headless(quiet)
    fx_driver = webdriver.Firefox(firefox_options=option)
    fx_driver.get('about:blank')
    fx_driver.maximize_window()
    fx_driver.get(ojurl + '/loginpage.php')
    account = fx_driver.find_element_by_name('user_id')
    account.send_keys(user_info[0])
    password = fx_driver.find_element_by_name('password')
    password.send_keys(user_info[1])
    button = fx_driver.find_element_by_name("submit")
    button.click()
    print('Login success! Submitting code...')
    fx_driver.get(ojurl + '//submitpage.php?id=' + id)
    editor = fx_driver.find_element_by_name('source')
    file = open(code_path, 'r')
    source = ''
    while True:
        str = file.readline()
        if len(str) == 0:
            break
        source += str
    editor.send_keys(source)
    button = fx_driver.find_elements_by_tag_name('input')
    button[1].click()
    print('Done.')
    print('Fetching realtime status (press Ctrl-C to terminate)')
    base = time.time()
    while True:
        fx_driver.refresh()
        id = fx_driver.find_elements_by_tag_name('font')
        try:
            verdict = id[2].text
        except:
            continue
        print('[{}s]: {}'.format(time.time() - base, verdict))
        if verdict != 'Pending' and verdict != 'Running_&_Judging' and verdict != 'Compiling':
            break
        time.sleep(0.2)
