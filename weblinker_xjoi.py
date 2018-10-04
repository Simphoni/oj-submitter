#!/usr/bin/python3

'''
This module contains submitting function on XJOI.

This module requires selenium
run `pip3 install selenium --user`.
If you haven't installed pip3, run `sudo apt install python3-pip`.
'''

import os
import time
import random
from selenium import webdriver


defaultOrder = [
    'a.cpp', 'A.cpp', '1.cpp', 'T1.cpp', 
    'b.cpp', 'B.cpp', '2.cpp', 'T2.cpp',
    'c.cpp', 'C.cpp', '3.cpp', 'T3.cpp',
    'd.cpp', 'D.cpp', '4.cpp', 'T4.cpp',
    'e.cpp', 'E.cpp', '5.cpp', 'T5.cpp',
    'f.cpp', 'F.cpp', '6.cpp', 'T6.cpp',
    'std.cpp', 'main.cpp',
    'bru.cpp', 'brute.cpp', 'bf.cpp'
]


def changeCap(c):
    if ord('a') <= ord(c) and ord(c) <= ord('z'):
        return chr(ord(c) + ord('A') - ord('a'))
    return chr(ord(c) + ord('a') - ord('A'))


def checkValidUrl(driver):
    p = driver.find_elements_by_tag_name('p')
    for i in p:
        if i.text == '404 Not Found' or i.text == 'Access Denied':
            return False
    return True


def submitFirefox(user_info, quiet):
    '''
    This function starts firefox driver, so make sure firefox is installed.
    Requires geckodriver to interact with firefox
    you can find it on https://github.com/mozilla/geckodriver/releases
    '''
    ojurl = 'http://210.33.19.103'
    try:
        option = webdriver.FirefoxOptions()
        option.set_headless(quiet)
        fx_driver = webdriver.Firefox(firefox_options=option)
        print('Firefox is on.')
        if not quiet:
            fx_driver.get('about:blank')
            fx_driver.maximize_window()
        fx_driver.get(ojurl)
        dropdown = fx_driver.find_elements_by_class_name('dropdown-toggle')
        dropdown[3].click()
        account = fx_driver.find_element_by_id('input-username')
        account.send_keys(user_info[0])
        password = fx_driver.find_element_by_id('input-password')
        password.send_keys(user_info[1])
        button = fx_driver.find_element_by_id("button-submit")
        button.click()
        print('Login success!')
        fx_driver.get(ojurl + '/contests')
        option = fx_driver.find_elements_by_tag_name('option')
        leng = len(option)
        for i in range(leng):
            print('[{}]: {}'.format(i + 1, option[i].text))
        try:
            level = input('Select a level from the above options (default 2) or state a contestID: ')
        except KeyboardInterrupt:
            puts('')
            return
        if level == '':
            level = '2'
        if not level.isdigit():
            print('Invalid input, exiting...')
            return
        if int(level) > leng:
            ID = int(level)
        else:
            fx_driver.get(ojurl + '/contests?type=' + level)
            contestList = fx_driver.find_elements_by_class_name('contest-table-text')
            leng = len('contestList')
            for i in range(0, leng, 5):
                print("[{}]: {} | {} | {} | {}".format(contestList[i].text,
                                                       contestList[i + 1].text,
                                                       contestList[i + 2].text,
                                                       contestList[i + 3].text,
                                                       contestList[i + 4].text))
            id = input('Select a contest from the above options (default {}): '.format(contestList[0].text))
            if id == '':
                ID = int(contestList[0].text)
            else:
                ID = int(id)
        baseurl = ojurl + '/contest/{}'.format(ID)
        fx_driver.get(baseurl)
        if not checkValidUrl(fx_driver):
            print('404 Not Found or Access Denied!')
            return
        cur = 0
        while True:
            cur += 1
            num = '{}'.format(cur)
            Num = 'T{}'.format(cur)
            alp = chr(ord('a') + cur - 1)
            Alp = chr(ord('A') + cur - 1)
            fx_driver.get(baseurl + '/problem/{}'.format(cur))
            if not checkValidUrl(fx_driver):
                break
            title = fx_driver.find_element_by_class_name('problem-view-title')
            print('{}: {}'.format(Num, title.text))
            code = ''
            if os.path.isdir(alp):
                for i in defaultOrder:
                    if os.path.isfile('./' + alp + '/' + i):
                        code = './' + alp + '/' + i
                        break
            elif os.path.isdir(Alp):
                for i in defaultOrder:
                    if os.path.isfile('./' + Alp + '/' + i):
                        code = './' + Alp + '/' + i
                        break
            elif os.path.isdir(num):
                for i in defaultOrder:
                    if os.path.isfile('./' + num + '/' + i):
                        code = './' + num + '/' + i
                        break
            elif os.path.isdir(Num):
                for i in defaultOrder:
                    if os.path.isfile('./' + Num + '/' + i):
                        code = './' + Num + '/' + i
                        break
            else:
                for i in range((cur - 1) * 4, len(defaultOrder)):
                    if os.path.isfile(defaultOrder[i]):
                        code = defaultOrder[i]
                        break
            try:
                if code == '':
                    path = input('Enter source path: ')
                else:
                    path = input('Enter source path (detected {}): '.format(code))
                if path == '':
                    if code == '':
                        raise KeyboardInterrupt
                else:
                    if not os.path.isfile(path):
                        raise KeyboardInterrupt
                    code = path
            except KeyboardInterrupt:
                print('Ignoring submission for {}.'.format(Num))
            else:
                fx_driver.get(baseurl + '/problem/{}/submit'.format(cur))
                file = open(code, 'r')
                attachment = 'This code is submitted by OJsubmitter developed by Simphoni'
                for i in range(0, 30):
                    idx = int(random.random() * len(attachment))
                    if (attachment[idx] == ' '):
                        continue
                    attachment = attachment[:idx] + changeCap(attachment[idx]) + attachment[idx + 1:]
                attachment = "//" + attachment + "."
                src = file.readlines()
                src.append('\n' + attachment)
                file.close()
                source = fx_driver.find_element_by_class_name('submit-textarea')
                source.send_keys(src)
                button = fx_driver.find_element_by_class_name('submit-submit')
                button.click()
                print('Submit successful!!')
    finally:
        try:
            fx_driver.close()
        except:
            pass
        print('Firefox Closed.')
        if os.path.exists(os.getcwd() + '/geckodriver.log'):
            os.system('rm geckodriver.log')
