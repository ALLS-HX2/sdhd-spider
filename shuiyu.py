#!/usr/bin/env python3
import json
import os
from util import requestUtil

baseDir = './data/'

data = requestUtil.getJSON('https://www.diving-fish.com/api/chunithmprober/music_data', {'referer': 'https://www.diving-fish.com/maimaidx/prober/'})
if data != {}:
    data2 = []
    for el in data:
        if el['id'] < 8000:
            data2.append(el)
    os.makedirs(baseDir, exist_ok=True)
    with open(baseDir + 'songListSY.json', 'w', encoding='utf-8') as fp:
        json.dump(data2, fp, ensure_ascii=False, indent=2)
    print(f'数据源【水鱼查分器】OK，总曲目 {len(data2)}')
