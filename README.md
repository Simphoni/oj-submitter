For Chinese readers, see also [Release Notes](https://simphoni.coding.me/2018/10/05/OJsubmitter/)
# OJ-submitter
This tool is used for submitting code from a terminal to OnlineJudges.  
It can only be used under Linux operating system.  
It needs to use Firefox browser, so make sure it is installed.  
Selenium is required, run `pip3 install selenium`  
Before running `./main.py`, move `geckodriver` into `~/.local/bin/`  

# Intro
We currently only support Codeforces, BZOJ and XJOI.  
Use `./main.py -a` to add a user(you must store (at least) one user before submitting)  
Use `./main.py -oj={OJname} -p={problemID} -c={code_path}` to submit  
Use `./main.py -q` to enable quiet mode(will not open GUI Firefox)
We now support fetching realtime status from BZOJ (make sure you turned on quiet mode)  
We now support XJOI Contests!! Switch to your code directory and OJsubmitter will automatically detect your source code.  
Just follow the instructions, everything will be alright!  
Enjoy!!  

# Release 0.3
Quiet mode rewritten for XJOI.  
This time, instead of starting Firefox headless, we use the requests lib directly to access the web. It's now much quicker than release 0.2.
Enjoy!!

# TODO
Language selection  
Remember last submission
