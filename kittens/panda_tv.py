import re
from base64 import b64encode
from functools import partial

import grequests
import requests
from Crypto.Cipher import AES


class Kitten:
    def __init__(self, config):
        self.config = config
        self.opener = requests.session()

    @staticmethod
    def encrypt(text, key, iv='995d1b5ebbac3761'):
        cryptor = AES.new(key.encode(), mode=AES.MODE_CBC, IV=iv.encode())
        text = text.encode("utf-8")
        add = 16 - (len(text) % 16)
        text = text + (b'\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b64encode(ciphertext).decode()

    def meow(self):
        res = self.opener.get('https://u.panda.tv/ajax_aeskey').json()

        res = self.opener.get('https://u.panda.tv/ajax_login', params={
            'account': self.config['account'],
            'password': self.encrypt(self.config['password'], res['data']),
            'pdftsrc': '{{"os":"web","smid":"{0}"}}'.format(self.config['pdft']),
            '__plat': 'pc_web'
        }).json()

        if res['errno'] != 0:
            raise RuntimeError('Fail to login')

        res = self.opener.get('https://m.panda.tv/sign/index').text

        token = re.search(r'name="token"\s+value="(\w+)"', res)
        lottery_param = re.search(r'"key":\s*"(?P<app>[\w-]+)",\s*"date":\s*"(?P<validate>[\d-]+)"', res)

        if not (token and lottery_param):
            raise RuntimeError('Fail to get token')

        gen_requests = partial(grequests.request, session=self.opener)

        return grequests.map(
            [
                gen_requests('GET', 'https://m.panda.tv/api/sign/apply_sign', params={
                    'token': token.group(1)
                }),
                gen_requests('GET', 'https://roll.panda.tv/ajax_roll_draw', params={
                    'app': lottery_param.group('app'),
                    'validate': lottery_param.group('validate')
                }),
                gen_requests('POST', 'http://lvxing.pgc.panda.tv/api/badge/get', data={
                    'token': token.group(1)
                }),
            ] + [
                gen_requests('GET', 'https://pharah.gate.panda.tv/badge/get_badge', params={
                    'token': token.group(1),
                    'type': badge_type
                }) for badge_type in self.config['badge_types']
            ]
        )
