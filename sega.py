#!/usr/bin/env python3
import collections
import json
import os
import threading
from util import requestUtil

baseDir = './data/'
imgDir = baseDir + 'img/'
maxThread = 16

data = requestUtil.getJSON('https://chunithm.sega.jp/storage/json/music.json', {'referer': 'https://chunithm.sega.jp/music/new/'})
if data != {}:
    data2 = []
    for el in data:
        if el['we_star'] == '':
            data2.append(el)
    os.makedirs(baseDir, exist_ok=True)
    with open(baseDir + 'songListSG.json', 'w', encoding='utf-8') as fp:
        json.dump(data2, fp, ensure_ascii=False, indent=2)
    downloadQueue = collections.deque()
    for el in data2:
        filename = el['image']
        if not os.path.exists(imgDir + filename):
            downloadQueue.append(filename)
    print(f'数据源【SEGA】OK，总曲目 {len(data2)}，需下载 {len(downloadQueue)} 张封面')
    while 1:
        if len(threading.enumerate()) == 1 and len(downloadQueue) == 0:
            break
        elif len(threading.enumerate()) <= maxThread and len(downloadQueue):
            print(f'正在下载：{filename}，还剩 {len(downloadQueue) - 1} 张封面')
            filename = downloadQueue.popleft()
            threading.Thread(target=requestUtil.downloadFile, args=('https://new.chunithm-net.com/chuni-mobile/html/mobile/img/' + filename, imgDir + filename, {'referer': 'https://chunithm.sega.jp/'})).start()
