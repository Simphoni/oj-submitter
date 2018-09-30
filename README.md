# OJ-submitter
This tool is used for submitting code from a terminal to OnlineJudges.  
It can only be used under Linux operating system.  
It needs to use Firefox browser, so make sure it is installed.  
Selenium is required, run `pip3 install selenium`
Before running `./main.py`, move `geckodriver` into `~/.local/bin/`  

# Intro
We currently only support Codeforces and BZOJ.  
Use `./main.py -a` to add a user(you must store (at least) one user before submitting)  
Use `./main.py -oj={OJname} -p={problemID} -c={code_path}` to submit  
Just follow the instructions, everything will be alright!  

# TODO
