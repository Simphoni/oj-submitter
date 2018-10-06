#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import requests

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


def accessible(page):
    a = '404 Not Found'
    b = 'Access Denied'
    n = len(page)
    for i in range(n - len(a) + 1):
        if page[i:i + len(a)] == a or page[i:i + len(b)] == b:
            return False
    return True


def blank(c):
    if c == ' ' or c == '\t' or c == '\n' or c == '\r':
        return True
    return False


def get_elements_from_text(page, str):
    n = len(page)
    list = []
    for i in range(n - len(str) + 1):
        if page[i:i + len(str)] == str:
            cur = 1
            ptr = i
            ele = ''
            copied = False
            while True:
                if blank(page[ptr]):
                    if copied:
                        ele += page[ptr]
                    ptr += 1
                    continue
                if page[ptr] == '<':
                    cur += 1
                elif page[ptr] == '>':
                    cur -= 1
                elif cur == 0:
                    ele += page[ptr]
                    copied = True
                if copied and cur != 0:
                    break
                ptr += 1
            while len(ele) and blank(ele[len(ele) - 1]):
                ele = ele[:len(ele) - 1]
            list.append(ele)
    return list


levels = ['普及组', '提高组', '省选', 'NOI', '集训队', 'IOI']
url = 'http://210.33.19.103'


def submitRequests(user):
    info = { 'user': user[0], 'pass': user[1] }
    userAgent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
    # login with a new session
    web = requests.session()
    res = web.post(url, data = info, headers = {
        'Referer': url + '/', 'User-Agent': userAgent
    })
    for i in range(len(levels)):
        print('[{}]: {}'.format(i + 1, levels[i]))
    try:
        level = input('Select a level from the above options (default 2): ')
    except KeyboardInterrupt:
        puts('')
        sys.exit()
    if not level.isdigit():
        level = '2'
    if int(level) > 6 or int(level) < 1:
        level = '2'
    res = web.get(url + '/contests?type=' + level)
    res.encoding = 'utf-8'
    info = get_elements_from_text(res.text, 'contest-table-text')
    for i in range(0, len(info), 5):
        if i + 5 > len(info):
            break
        print("[{}]: {} | {} | {} | {}".format(info[i], info[i + 1],
                                               info[i + 2], info[i + 3], info[i + 4]))
    try:
        if len(info) == 0:
            id = input('Select a contest: ')
        else:
            id = input('Select a contest (default {}): '.format(info[0]))
    except KeyboardInterrupt:
        print('')
        sys.exit()
    if id == '' and info[0]:
        id = info[0]
    contesturl = url + '/contest/' + id
    page = web.get(contesturl)
    page.encoding = 'utf-8'
    if not accessible(page.text):
        print('Access Denied or 404 Not Found.')
        sys.exit()
    cur = 0
    while True:
        cur += 1
        num = '{}'.format(cur)
        Num = 'T{}'.format(cur)
        alp = chr(ord('a') + cur - 1)
        Alp = chr(ord('A') + cur - 1)
        proburl = contesturl + '/problem/{}'.format(cur)
        page = web.get(proburl)
        page.encoding = 'utf-8'
        if not accessible(page.text):
            break
        title = get_elements_from_text(page.text, 'problem-view-title')
        print('{}: {}'.format(Num, title[0]))
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
            if path != '':
                code = path
        except KeyboardInterrupt:
            print('')
            print('Ignoring submission for {}.'.format(Num))
            continue
        if os.path.isfile(code):
            file = open(code, 'r')
            attachment = 'This code is submitted by OJsubmitter developed by Simphoni'
            for i in range(0, 30):
                idx = int(random.random() * len(attachment))
                if (attachment[idx] == ' '):
                    continue
                attachment = attachment[:idx] + changeCap(attachment[idx]) + attachment[idx + 1:]
            attachment = "//" + attachment + "."
            lines = file.readlines()
            src = ''
            for i in lines:
                src += i
            src = src + '\n' + attachment
            keys = { 'language': 'g++', 'source': src }
            header = {
                'Referer': proburl + '/submit',
                'User-Agent': userAgent,
            }
            web.post(proburl + '/submit'.format(cur), data = keys, headers = header)
            file.close()
            print('Submit successful!!')
        else:
            print('')
            print('Ignoring submission for {}.'.format(Num))
    print('Finished.')
