from base64 import b64encode
from functools import partial

import grequests
import requests
from Crypto.Cipher import AES


class Kitten:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def encrypt(text, key, iv='995d1b5ebbac3761'):
        cryptor = AES.new(key.encode(), mode=AES.MODE_CBC, IV=iv.encode())
        text = text.encode("utf-8")
        add = 16 - (len(text) % 16)
        text = text + (b'\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b64encode(ciphertext).decode()

    def meow(self):
        opener = requests.session()
        res = opener.get('https://u.panda.tv/ajax_aeskey', headers={
            'Cookie': 'SESSCYPHP={0};'.format(self.config['SESSCYPHP'])
        }).json()
        res = opener.get('https://u.panda.tv/ajax_login', params={
            'account': self.config['account'],
            'password': self.encrypt(self.config['password'], res['data']),
            '__plat': 'pc_web',
        }, headers={
            'Cookie': 'SESSCYPHP={0}; pdft={1};'.format(self.config['SESSCYPHP'], self.config['pdft'])
        })
        token = res.cookies.get('I')[-32:]
        if not token:
            raise RuntimeError('Fail to get token')

        res = opener.get('https://api.m.panda.tv/ajax_get_token_and_login').json()
        if res['errno'] != 0:
            raise RuntimeError('Fail to get api_m_panda')
        api_m_panda_time = res['data']['time']
        api_m_panda_token = res['data']['token']

        gen_requests = partial(grequests.request, session=opener)

        res = grequests.map(
            [
                # client_sign
                gen_requests('GET', 'https://m.panda.tv/sign/index'),
                # http://www.panda.tv/sp/fornew2017.html
                gen_requests('GET', 'http://roll.panda.tv/ajax_sign', params={
                    'app': 'fornew',
                    'token': token
                }),
                # school_sigh
                gen_requests('POST', 'http://api.m.panda.tv/tavern/fortune/user/signin?pt_time={0}&pt_sign={1}'.format(
                    api_m_panda_time, api_m_panda_token
                ), data={
                    'groupid': 101500
                })
            ] + [
                # get_badge
                gen_requests('GET', 'https://pharah.gate.panda.tv/badge/get_badge', params={
                    'token': token,
                    'type': badge_type
                }) for badge_type in self.config['badge_types']
            ]
        )

        return res
