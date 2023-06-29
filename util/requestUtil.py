#!/usr/bin/env python3
import os
import requests

commonHeader = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'cache-control': 'no-cache',
    'pragma': 'no-cache'
}

maxRetryCount = 5
timeout = 60

def getJSON(url, headers = {}, maxRetryCount = maxRetryCount, timeout=timeout):
    nowAttempt = 1
    while 1:
        try:
            resp = requests.get(url, headers=commonHeader | headers, timeout=timeout)
            resp.encoding = resp.apparent_encoding
            return resp.json()
        except requests.Timeout:
            print(f'获取 {url} 超时，重传次数 {nowAttempt}/{maxRetryCount}')
            nowAttempt += 1
            if nowAttempt > maxRetryCount:
                return {}

def downloadFile(url, toFile, headers = {}, maxRetryCount = maxRetryCount, timeout=timeout):
    nowAttempt = 1
    while 1:
        try:
            resp = requests.get(url, headers=commonHeader | headers, timeout=timeout)
            break
        except requests.Timeout:
            print(f'获取 {url} 超时，重传次数 {nowAttempt}/{maxRetryCount}')
            nowAttempt += 1
            if nowAttempt > maxRetryCount:
                return
    os.makedirs(os.path.dirname(toFile), exist_ok=True)
    with open(toFile, 'wb') as fp:
        for chunk in resp.iter_content(chunk_size=128):
            fp.write(chunk)
