#!/usr/bin/python3
import os
import sys
import random
import pickle
import getpass

oj = ''
code_path = ''
problem_id = ''
command = sys.argv
n = len(command)
home = os.environ['HOME']
confdir = home + '/.ojsubmitter'
store = False
quiet = False
OJlist = ['CF', 'BZOJ', 'XJOI']
passwd_path = ''
useConfig = False

map = {
    'cf': 'CF',
    'CF': 'CF',
    'Cf': 'CF',
    'codeforces': 'CF',
    'Codeforces': 'CF',
    'bz': 'BZOJ',
    'BZ': 'BZOJ',
    'bzoj': 'BZOJ',
    'Bzoj': 'BZOJ',
    'lydsy': 'BZOJ',
    'xj': 'XJOI',
    'xjoi': 'XJOI',
    'XJOI': 'XJOI',
    'Xjoi': 'XJOI'
}


def readUserInfo():
    if os.path.exists(passwd_path) is False:
        print("No user info stored, use 'ojsubmitter -a' to add one.")
        sys.exit()
    try:
        file = open(passwd_path, "rb")
        account = pickle.load(file)
        file.close()
    except:
        print("No user info stored, use 'ojsubmitter -a' to add one.")
        sys.exit()
    if len(account) == 0:
        print("No user info stored, use 'ojsubmitter -a' to add one.")
        sys.exit()
    cnt = 0
    for i in account:
        print(r"[{}] {}".format(cnt, i))
        cnt += 1
    try:
        num = input("Select an account from local credentials (default 0): ")
        if num == '':
            num = '0'
        if not num.isdigit():
            print('Invalid input, exiting...')
            sys.exit()
        num = int(num)
        if num >= len(account):
            print('Range violation, exiting...')
            sys.exit()
    except KeyboardInterrupt:
        print()
        sys.exit()
    cnt = 0
    for i in account:
        if cnt == num:
            return [i, account[i]]
        cnt += 1


def changeCap(c):
    if ord('a') <= ord(c) and ord(c) <= ord('z'):
        return chr(ord(c) + ord('A') - ord('a'))
    return chr(ord(c) + ord('a') - ord('A'))


def getOJ():
    global oj
    for i in range(0, len(OJlist)):
        print("[{}] {}".format(i, OJlist[i]))
    print('Select an OJ from supported list (defaut 0):', end=' ')
    try:
        num = input()
        if num == '':
            num = '0'
        if not num.isdigit():
            print('Invalid input, exiting...')
            sys.exit()
        num = int(num)
        if num >= len(OJlist):
            print('Range violation, exiting...')
            sys.exit()
    except KeyboardInterrupt:
        print('')
        sys.exit()
    oj = OJlist[num]
    passwd_path = confdir + '/.' + oj + '-credentials'

def storeUserInfo():
    if oj == '':
        getOJ()
    passwd_path = confdir + '/.' + oj + '-credentials'
    if os.path.exists(confdir) is False:
        os.system('mkdir ' + confdir)
    account = {}
    if os.path.exists(passwd_path) is False:
        os.system('touch ' + passwd_path)
    try:
        file = open(passwd_path, 'rb')
        account = pickle.load(file)
        file.close()
    except:
        account = {}
    fir = input('account: ')
    sec = getpass.getpass('password: ')
    if fir in account:
        print("This account has previously been stored, update password? [Y/n/d]", end='')
        a = input()
        if a == '' or a == 'y' or a == 'Y' or a == 'yes':
            account[fir] = sec
        elif a == 'd' or a == 'delete' or a == 'D':
            print('Deleting account...')
            account.pop(fir)
        else:
            print('Giving up...')
            sys.exit()
    else:
        account[fir] = sec
    file = open(passwd_path, 'wb')
    pickle.dump(account, file)
    file.close()
    print('User info successfully updated!!')


# parse command
for i in range(1, n):
    if command[i][0] == '-':
        if len(command[i]) == 1:
            print("Ignored argument '{}'.".format(command[i]))
        elif command[i][1] == '-':
            if command[i][2:6] == 'prob':
                d = 5
                while command[i][d] != '=':
                    d = d + 1
                problem_id = command[i][d + 1:]
            elif command[i][2:6] == 'code':
                d = 5
                while command[i][d] != '=':
                    d = d + 1
                code_path = command[i][d + 1:]
            elif command[i][2:4] == 'oj':
                d = 4
                while command[i][d] != '=':
                    d = d + 1
                oj = map[command[i][d + 1:]]
            elif command[i][2:6] == 'quiet':
                quiet = True
            elif command[i][2:6] == 'last':
                useConfig = True
            else:
                print("Ignored argument '{}'.".format(command[i]))
        else:
            if command[i][1] == 'p':
                d = 2
                while command[i][d] != '=':
                    d = d + 1
                problem_id = command[i][d + 1:]
            elif command[i][1] == 'c':
                d = 2
                while command[i][d] != '=':
                    d = d + 1
                code_path = command[i][d + 1:]
            elif command[i][1] == 'a':
                store = True
            elif command[i][1] == 'o':
                d = 2
                while command[i][d] != '=':
                    d = d + 1
                try:
                    oj = map[command[i][d + 1:]]
                except:
                    print("Ignored argument '{}'.".format(command[i]))
                    oj = ''
            elif command[i][1] == 'q':
                quiet = True
            else:
                print("Ignored argument '{}'.".format(command[i]))
    else:
        print("Ignored argument '{}'.".format(command[i]))

# add an account
if store is True:
    storeUserInfo()
    sys.exit()
# fetch oj name from input
if oj == '':
    getOJ()
passwd_path = confdir + '/.' + oj + '-credentials'
# fetch user info from input
user = readUserInfo()
# fetch code path from input and check if the file exists
if oj != 'XJOI':
    if code_path == '':
        code_path = input('Enter the code path. (e.g. ~/Documents/a.cpp or a.cpp): ')
    if code_path[0] == '~':
        code_path = home + code_path[1:]
    if code_path[0] != '/':
        code_path = os.getcwd() + '/' + code_path
    if os.path.exists(code_path) is False:
        print("Solution file {} doesn't exist, exiting.".format(code_path))
        sys.exit()
    # copy code to ~/.ojsubmitter/cache*
    new_path = home + '/.ojsubmitter/cache'
    dot = len(code_path) - 1
    while dot > 0 and code_path[dot] != '.':
        dot -= 1
    if code_path[dot] == '.':
        new_path += code_path[dot:]
    os.system('cp ' + code_path + ' ' + new_path)
    # add random chars
    if code_path[dot:] == '.cpp':
        attachment = 'This code is submitted by OJsubmitter developed by Simphoni'
        for i in range(0, 30):
            idx = int(random.random() * len(attachment))
            if (attachment[idx] == ' '):
                continue
            attachment = attachment[:idx] + changeCap(attachment[idx]) + attachment[idx + 1:]
            attachment = "'//" + attachment + ".'"
        os.system('echo ' + attachment + ' >> ' + new_path)

if oj == 'CF':
    # info-collecting module for Codeforces
    # check missing elements
    if problem_id == '':
        print('Enter problem id. (e.g. 1053D):', end=' ')
        problem_id = input()
    l = len(problem_id)
    # parse & check if round & problem info is valid
    if problem_id[:l - 1].isdigit() is False:
        print('Invalid round info, exiting.')
        sys.exit()
    if problem_id[l - 1:].isalpha() is False:
        print('Invalid problem info, exiting.')
        sys.exit()
    import weblinker_cf
    print('Submiting \033[0;31;46m{}\033[0m to Codeforces \033[0;31;46m{}\033[0m...'.format(code_path, problem_id))
    weblinker_cf.submitFirefox(problem_id[:l - 1], problem_id[l - 1:], new_path, user, quiet)
elif oj == 'BZOJ':
    # info-collecting module for BZOJ
    # check missing elements
    if problem_id == '':
        print('Enter problem id. (e.g. 1001):', end=' ')
        problem_id = input()
    l = len(problem_id)
    # parse & check if problem info is valid
    if problem_id.isdigit() is False:
        print('Invalid problem info, exiting.')
        sys.exit()
    import weblinker_bzoj
    print('Submiting \033[0;31;46m{}\033[0m to BZOJ \033[0;31;46m{}\033[0m...'.format(code_path, problem_id))
    weblinker_bzoj.submitFirefox(problem_id, new_path, user, quiet)
elif oj == 'XJOI':
    # provide interactive config environment
    import weblinker_xjoi
    weblinker_xjoi.submitFirefox(user, quiet)
else:
    print("OnlineJudge {} currently not supported. If you think it meanful to add it into OJsubmitter, please contact xjzjohn@outlook.com.".format(oj))
