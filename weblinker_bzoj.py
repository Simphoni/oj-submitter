#!/usr/bin/python3
'''
This module contains submitting function on BZOJ.

This module requires selenium
run `pip3 install selenium --user`.
If you haven't installed pip3, run `sudo apt install python3-pip`.
'''

from selenium import webdriver


def submitFirefox(id, code_path, user_info):
    '''
    This function starts firefox driver, so make sure firefox is installed.
    Requires geckodriver to interact with firefox
    you can find it on https://github.com/mozilla/geckodriver/releases
    '''
    ojurl = 'https://www.lydsy.com/JudgeOnline'
    fx_driver = webdriver.Firefox()
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
    print('Finished.')
