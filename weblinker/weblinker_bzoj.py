#!/usr/bin/python3
'''
This module contains submitting function on BZOJ.
'''

import os
import time
from selenium import webdriver


def submitFirefox(id, code_path, user_info, quiet):
    '''
    This function submits code to BZOJ.
    It still uses firefox headless when quiet mode is on.
    '''
    ojurl = 'https://www.lydsy.com/JudgeOnline'
    try:
        option = webdriver.FirefoxOptions()
        option.set_headless(quiet)
        fx_driver = webdriver.Firefox(firefox_options=option)
        if not quiet:
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
        editor.send_keys(file.readlines())
        file.close()
        button = fx_driver.find_elements_by_tag_name('input')
        button[1].click()
        print('Done.')
        if not quiet:
            return
        print('Fetching realtime status... (To interrupt, press Ctrl-c)')
        base = time.time()
        while True:
            fx_driver.refresh()
            id = fx_driver.find_elements_by_tag_name('font')
            try:
                verdict = id[2].text
            except:
                continue
            cur = round(time.time() - base, 3)
            if int(cur * 1000) % 10 == 0:
                cur += 0.001
            cur = round(cur, 3)
            print('[{}s]: {}'.format(cur, verdict))
            if verdict != 'Pending' and verdict != 'Running_&_Judging' and verdict != 'Compiling':
                break
            time.sleep(0.2)
    finally:
        try:
            fx_driver.close()
        except:
            pass
        if os.path.exists(os.getcwd() + '/geckodriver.log'):
            os.system('rm geckodriver.log')
