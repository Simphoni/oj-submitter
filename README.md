For Chinese readers, see also [Release Notes](https://simphoni.coding.me/2018/10/05/OJsubmitter/)
# OJ-submitter
This tool is used for submitting code from a terminal to OnlineJudges.  
It can only be used under **Linux** operating system.  

# Intro
We currently only support Codeforces, BZOJ and XJOI.  
+ Use `./main.py -a` to add a user(you must store (at least) one user before submitting)  
+ Use `./main.py -oj={OJname} -p={problemID} -c={code_path}` to submit  
+ Use `./main.py -q` to enable quiet mode(will not open GUI Firefox)  
+ Use `./main.py -r` to rate a whole problemlist in XJOI  
+ Use `./main.py -h` to view the history submissions of a certain user in Codeforces  
  
We now support XJOI Contests!!  
Switch to your code directory and OJsubmitter will automatically detect your source code.  
Enjoy :)  
  
# Tips
For your safety, the parameters of our credential-storer is not given, you need to choose some **big primes** for it.  
**OJsubmitter not working? Make sure python3-requests is installed.**  

# TODO
- [x] Secure credential storage  
- [x] Rewrite Codeforces quiet mode  
- [x] XJOI rater  
- [x] Codeforces status reader  
- [ ] Language selection  
