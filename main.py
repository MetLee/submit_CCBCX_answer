import base64
import hmac
import json
import requests as r
import time

from hashlib import sha1


token = 'token'
sk = 'sk'
pid = 55

answers = ['answer1', 'answer2']


def hash_hmac(code, key, sha1):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
    return base64.b64encode(hmac_code).decode()


def fetch_post_with_sign(url, data):
    ts = int(time.time() * 1000)
    data_body = json.dumps(data, separators=(',', ':'))
    us = 'token={token}&ts={ts}&bodyString={data_body}'.format(
        token=token, ts=ts, data_body=data_body)
    sign = hash_hmac(us, sk, sha1)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'Content-Type': 'application/json',
        'User-Token': token,
        'X-Auth-Token': 'Ccxc-Auth {ts} {sign}'.format(ts=ts, sign=sign)
    }
    return r.post(url, data_body, headers=headers)


def main():
    for answer in answers:
        data = {'pid': pid, 'answer': answer}
        rst = fetch_post_with_sign(
            'https://api.ccxc.online/api/v1/check-answer', data)
        print(answer, rst.text)
        time.sleep(5 * 60 + 5)
    input()


if __name__ == '__main__':
    main()
