import sys
import requests

url = 'http://210.33.19.103'


def accessible(page):
    a = '404 Not Found'
    b = 'Access Denied'
    n = len(page)
    for i in range(n - len(a) + 1):
        if page[i:i + len(a)] == a or page[i:i + len(b)] == b:
            return False
    return True


def parseProblem(page):
    fea = r'/problem/'
    plen = len(page)
    flen = len(fea)
    ret = []
    for i in range(0, plen - flen + 1):
        if page[i:i + flen] == fea:
            str = page[i + flen:i + flen + 4]
            if str.isdigit() is True:
                ret.append(str)
    return ret


def rateIt(menu, submenu, user):
    if not menu.isdigit():
        print('Menu name should be an INTEGER!')
        sys.exit()
    if not submenu.isdigit():
        print('Submenu name should be an INTEGER!')
        sys.exit()
    wei = input('Enter rate value (-1, 0, 1): ')
    if wei != '1' and wei != '0' and wei != '-1':
        print('Rate value shoud be in [-1, 1]!')
        sys.exit()
    menu = int(menu) - 1
    submenu = int(submenu) - 1
    info = {'user': user[0], 'pass': user[1]}
    userAgent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
    # login with a new session
    web = requests.session()
    web.post(url, data=info, headers={
        'Referer': url + '/', 'User-Agent': userAgent
    })
    chk = web.get(url + '/user/change_profile')
    if not accessible(chk.text):
        print('Login failed, invalid username/password!')
        sys.exit()
    problemset = '{}/problemlist/{}/{}'.format(url, menu, submenu)
    page = web.get(problemset)
    idx = parseProblem(page.text)
    data = {}
    for i in idx:
        data['rating-' + i] = wei
    web.post(problemset, data=data, headers={
        'Referer': url + '/', 'User-Agent': userAgent
    })
