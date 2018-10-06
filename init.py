#!/usr/bin/python3

import os

home = os.environ['HOME']
print('Installing selenium...')
os.system('pip3 install selenium --user')
print('Done.')
target = home + '/.local/bin'
if not os.path.isdir(target):
    os.system('mkdir ' + target)
os.system('ln -s ' + os.getcwd() + '/geckodriver ' + target + '/geckodriver')
os.system('ln -s ' + os.getcwd() + '/main.py ' + target + '/ojsubmitter')
print('Installation finished.')
