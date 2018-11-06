#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import requests

url = 'http://codeforces.com'


def get_token(text):
    str = 'data-csrf'
    for i in range(len(text) - len(str) + 1):
        if text[i:i + len(str)] == str:
            ptr = i
            while text[ptr] != "'" and text[ptr] != '"':
                ptr += 1
            ptr += 1
            qtr = ptr
            while text[qtr] != "'" and text[qtr] != '"':
                qtr += 1
            return text[ptr:qtr]


def blank(c):
    if c == ' ' or c == '\t' or c == '\n' or c == '\r':
        return True
    return False


def parseVerdict(text):
    doing = False
    beg = 'status-verdict-cell'
    fea = 'data-submission-id'
    num = 'verdict-format-judged'
    result = {}
    for i in range(len(text) - len(beg) + 1):
        if text[i:i + len(beg)] == beg:
            doing = True
        if text[i:i + len(fea)] == fea and doing:
            break
        if not doing:
            continue
        if text[i] == '=':
            ptr = i - 1
            while not blank(text[ptr]):
                ptr -= 1
            fir = text[ptr + 1:i]
            ptr = i + 2
            while text[ptr] != '"' and text[ptr] != "'":
                ptr += 1
            sec = text[i + 2:ptr]
            result[fir] = sec
        if text[i:i + 5] == r'&nbsp' and result['class'] == 'time-consumed-cell':
            j = i - 1
            while text[j].isdigit():
                j -= 1
            result['execTime'] = text[j + 1:i] + 'ms'
        elif text[i:i + 5] == r'&nbsp' and result['class'] == 'memory-consumed-cell':
            j = i - 1
            while text[j].isdigit():
                j -= 1
            result['execMem'] = text[j + 1:i] + 'KB'
        elif i + len(num) <= len(text) and text[i:i + len(num)] == num:
            j = i
            while text[j] != '>':
                j += 1
            j += 1
            k = j
            while text[k].isdigit():
                k += 1
            result['testNumber'] = text[j:k]
    return result


def submitRequests(probcode, code_path, user):
    # login with a new session
    web = requests.session()
    main_page = web.get(url)
    csrf_token = get_token(main_page.text)
    headers = {
        'Referer': url + '/enter?back=%2F',
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
    }
    data = {
        'action': 'enter',
        'handleOrEmail': user[0],
        'password': user[1],
        'csrf_token': csrf_token
    }
    res = web.post(url + '/enter?back=/', data=data, headers=headers)
    src = ''
    srcFile = open(code_path, 'r')
    while True:
        li = srcFile.readline()
        if len(li) == 0:
            break
        src += li
    data = {
        'action': 'submitSolutionFormSubmitted',
        'csrf_token': csrf_token,
        'programTypeId': 50,
        'source': src,
        'submittedProblemCode': probcode,
        'tabSize': 8
    }
    res = web.post(url + '/problemset/submit', data=data, headers=headers)
    base = time.time()
    first = True
    while True:
        res = web.get(url + '/submissions/' + user[0])
        ver = parseVerdict(res.text)
        if first:
            print('submissionId: {}'.format(ver.get('submissionId')))
        curTime = round(time.time() - base, 3)
        if int(curTime * 1000) % 10 == 0:
            curTime += 0.001
        curTime = round(curTime, 3)
        print('[{}s]: '.format(curTime), end='')
        short = ver.get('submissionVerdict')
        if short == 'TESTING':
            print('\033[47;34mRunning on test {}\033[0m'.format(ver.get('testNumber')), end = '')
        elif short == 'COMPILATION_ERROR':
            print('\033[47;30mCompilation error\033[0m')
            sys.exit()
        elif short == 'OK':
            print('\033[47;32mAccepted\033[0m', end='')
        elif short == 'WRONG_ANSWER':
            print('\033[47;31mWrong Answer\033[0m on test {}'.format(ver.get('testNumber')), end='')
        elif short == 'TIME_LIMIT_EXCEEDED':
            print('\033[47;33mTime limit exceeded\033[0m on test {}'.format(ver.get('testNumber')), end='')
        elif short == 'RUNTIME_ERROR':
            print('\033[47;33mRuntime error\033[0m on test {}'.format(ver.get('testNumber')), end='')
        elif short == 'MEMORY_LIMIT_EXCEEDED':
            print('\033[47;33mMemory limit exceeded on test {}\033[0m'.format(ver.get('testNumber')), end='')
        else:
            print(short, end = '')
        print(' | ' + ver.get('execTime') + ' | ', end = '')
        print(ver.get('execMem'))
        first = False
        if short != 'TESTING':
            break
