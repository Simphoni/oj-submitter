#!/usr/bin/python3
'''
This module contains submitting function on codeforces.

This module requires selenium
run `pip3 install selenium --user`.
If you haven't installed pip3, run `sudo apt install python3-pip`.
'''

import os
from selenium import webdriver


def submitFirefox(round, id, code_path, user_info, quiet):
    '''
    This function starts firefox driver, so make sure firefox is installed.
    Requires geckodriver to interact with firefox
    you can find it on https://github.com/mozilla/geckodriver/releases
    '''
    ojurl = 'https://codeforces.com'
    try:
        option = webdriver.FirefoxOptions()
        option.set_headless(quiet)
        fx_driver = webdriver.Firefox(firefox_options=option)
        fx_driver.set_page_load_timeout(20)
        if not quiet:
            fx_driver.get('about:blank')
            fx_driver.maximize_window()
        try:
            fx_driver.get(ojurl + '/enter')
        except:
            fx_driver.execute_script('window.stop()')
        account = fx_driver.find_element_by_id('handleOrEmail')
        account.send_keys(user_info[0])
        password = fx_driver.find_element_by_id('password')
        password.send_keys(user_info[1])
        remember = fx_driver.find_element_by_id('remember')
        remember.click()
        button = fx_driver.find_element_by_class_name("submit")
        button.click()
        print('Login success! Submitting code...')
        try:
            fx_driver.get(ojurl + '/contest/' + round + '/submit/' + id)
        except TimeoutException:
            driver.execute_script('window.stop()')
        editor = fx_driver.find_element_by_name('sourceFile')
        editor.send_keys(code_path)
        button = fx_driver.find_element_by_class_name("submit")
        button.click()
        print('Finished.')
        raw_input('Press any key to exit.')
    finally:
        try:
            fx_driver.close()
        except:
            pass
        if os.path.exists(os.getcwd() + '/geckodriver.log'):
            os.system('rm geckodriver.log')
