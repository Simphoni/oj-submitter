#!/usr/bin/python3
'''
This module contains submitting function on codeforces.

This module requires selenium
run `pip3 install selenium --user`.
If you haven't installed pip3, run `sudo apt install python3-pip`.
'''

from selenium import webdriver


def submitFirefox(round, id, code_path, user_info):
    '''
    This function starts firefox driver, so make sure firefox is installed.
    Requires geckodriver to interact with firefox
    you can find it on https://github.com/mozilla/geckodriver/releases
    '''
    ojurl = 'https://codeforc.es'
    fx_driver = webdriver.Firefox()
    fx_driver.get('about:blank')
    fx_driver.maximize_window()
    fx_driver.get(ojurl + '/enter')
    account = fx_driver.find_element_by_id('handleOrEmail')
    account.send_keys(user_info[0])
    password = fx_driver.find_element_by_id('password')
    password.send_keys(user_info[1])
    remember = fx_driver.find_element_by_id('remember')
    remember.click()
    button = fx_driver.find_element_by_class_name("submit")
    button.click()
    print('Login success! Submitting code...')
    fx_driver.get(ojurl + '/contest/' + round + '/submit/' + id)
    editor = fx_driver.find_element_by_name('sourceFile')
    editor.send_keys(code_path)
    button = fx_driver.find_element_by_class_name("submit")
    button.click()
    print('Finished.')
