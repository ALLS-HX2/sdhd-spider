#!/usr/bin/env python3
import json
from util import dbUtil

baseDir = './data/'

sqlRunner = dbUtil.MySQLUtil()

def escapeStr(s):
    return ''.join(s.split('"'))

with open(baseDir + 'songListSG.json', 'r', encoding='utf-8') as fp:
    dataSG = json.load(fp)
with open(baseDir + 'songListSY.json', 'r', encoding='utf-8') as fp:
    dataSY = json.load(fp)

sql = ['delete from chart', 'delete from songex', 'delete from song']

for el in dataSY:
    tmp1 = {'sid': el['id'], **el['basic_info']}
    tmp1['version'] = tmp1['from'].replace('中二节奏', 'CHUNITHM')
    tmp1['title'] = escapeStr(tmp1['title'])
    tmp1['artist'] = escapeStr(tmp1['artist'])
    sql.append('insert into song values ({sid}, "{title}", "{artist}", "{genre}", "{version}", {bpm})'.format(**tmp1))
    for i in range(len(el['cids'])):
        tmp2 = {'cid': el['cids'][i], 'sid': el['id'], 'diff': i, 'ds': el['ds'][i], **el['charts'][i]}
        tmp2['charter'] = escapeStr(tmp2['charter'])
        sql.append('insert into chart values ({cid}, {sid}, {diff}, {ds}, {combo}, "{charter}")'.format(**tmp2))

order = 1
for el in dataSG:
    tmp3 = {'sid': el['id'], 'order': order, **el}
    sql.append('insert into songex values ({sid}, {order}, "{image}")'.format(**tmp3))
    order += 1

sqlRunner.commit_data_many(sql)

songs = sqlRunner.select_all('select * from songview')
sql = []
nullCount = 10001
for el in songs:
    if el['gameorder'] is None:
        sql.append(f'insert into songex(sid, gameorder) values ({el["sid"]}, {nullCount})')
        nullCount += 1
sqlRunner.commit_data_many(sql)

charts = sqlRunner.select_all('select * from songchart')
for el in charts:
    el['ds'] = int(el['ds'] * 10)

with open(baseDir + 'entry.json', 'w', encoding='utf-8') as fp:
    json.dump({'songnum': len(songs), 'chartnum': len(charts)}, fp, ensure_ascii=False)
with open(baseDir + 'data.json', 'w', encoding='utf-8') as fp:
    json.dump({'data': charts}, fp, ensure_ascii=False)
