import sys
import time
import json
import requests

url = 'http://codeforc.es/api/user.status?handle={}&from={}&count={}'
# url = 'http://codeforces.com/api/user.status?handle={}&from={}&count={}'
friends = [
    'ACRush',
    'Altria-PenDragon',
    'AwD',
    'bmerry',
    'ccz181078',
    'Chloe_fan',
    'CommonAnts',
    'C_SUNSHINE',
    'cuizhuyefei',
    'cxt',
    'dddddddx.R',
    'Dozebear',
    'dreamoon',
    'fateice',
    'FizzyDavid',
    'fjzzq2002',
    'frank_c1',
    'function348',
    'I_am_Faded',
    'izban',
    'j_______________________',
    'jiaqiyang',
    'jiry_2',
    'JOHNKRAM',
    'kczno1',
    'laofudasuan',
    'matthew99',
    'mythologicalsama',
    'nqiiii',
    'OhWeOnFire',
    'OO0OOO00O0OOO0O00OOO0OO',
    'orbitingflea',
    'Panole233',
    'Petr',
    'Radewoosh',
    'rng_58',
    'R.xddddddd',
    'samjia2000',
    'scott_wu',
    'sd0061',
    '_SHENZHEBEI_',
    'Stilwell',
    'Swistakk',
    'Syloviaely',
    'Tangjz',
    'teja349',
    'Tommyr7',
    'tourist',
    'tqyaaaaang',
    'wangyisong1996',
    'whzzt',
    'wxh010910',
    'xumingkuan',
    'xyz111',
    'yanQval',
    'yasugongshang',
    'yfzcsc',
    'yjq_naiive',
    'yutaka1999',
    'YuukaKazami',
    'ywwyww',
    'zhangzy',
    'zhouyuyang'
]


def readStatus():
    web = requests.session()
    try:
        userID = input('Enter userId (default zhouyuyang): ')
    except KeyboardInterrupt:
        sys.exit()
    except:
        userID = 'zhouyuyang'
    if userID == '':
        userID = 'zhouyuyang'
    try:
        left = int(input('Enter left bound (default 1): '))
    except KeyboardInterrupt:
        sys.exit()
    except:
        left = 1
    try:
        right = int(input('Enter right bound (default 30): '))
    except KeyboardInterrupt:
        sys.exit()
    except:
        right = 30
    if left < 1:
        left = 1
    if left > right:
        right = left
    res = web.get(url.format(userID, left, right - left + 1))
    res = json.loads(res.text)
    if res.get('result') == None:
        print('No such user!!!')
        sys.exit()
    res = res['result']
    visited = {}
    print('Submission history from {}:'.format(userID))
    for i in res:
        problem = i['problem']
        try:
            con = '{}{}'.format(problem['contestId'], problem['index'])
        except:
            continue
        if visited.get(con) != None:
            continue
        visited[con] = True
        na = problem['name']
        while len(na) < 50:
            na += ' '
        Id = problem['contestId']
        while len(con) < 7:
            con = ' ' + con
        print('[{}]: {} | '.format(con, na), end='')
        if problem.get('points'):
            str = '{}'.format(problem['points'])
        else:
            str = 'Null'
        while len(str) < 6:
            str += ' '
        print(str, end=' | ')
        leg = len(problem['tags'])
        for j in range(leg):
            print(problem['tags'][j], end='')
            if j + 1 < leg:
                print(', ', end='')
        print()
