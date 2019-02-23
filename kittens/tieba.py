import grequests
import requests
import re
from hashlib import md5
from collections import OrderedDict


class Kitten(object):
    def __init__(self, config):
        self.bduss = config['bduss']
        self.headers = {
            'Cookie': 'BDUSS={0};STOKEN={1};'.format(config['bduss'], config['stoken'])
        }

    def get_liked_tieba(self):
        pn = 0
        re_pn = re.compile(r'ForumManager')
        re_result = re.compile(r'<a href="/f\?kw=(.*?)" title="(.*?)"')
        resp = []
        while 1:
            pn += 1
            mylike_url = 'http://tieba.baidu.com/f/like/mylike?&pn={0}'.format(pn)
            res = requests.get(mylike_url, headers=self.headers).text
            if not re_pn.findall(res):
                break
            else:
                res = re_result.findall(res)
                for each in res:
                    resp.append(each)

        return resp

    def meow(self):
        tieba_arr = self.get_liked_tieba()

        if not tieba_arr:
            raise RuntimeError('Fail to get tieba_arr')

        rs = []
        for each in tieba_arr:
            name = each[1]
            sign_url = 'http://c.tieba.baidu.com/c/c/forum/sign'
            tbs_url = 'http://tieba.baidu.com/dc/common/tbs'
            tbs = requests.get(tbs_url, headers=self.headers).json()['tbs']
            data = OrderedDict([
                ('BDUSS', self.bduss),
                ('kw', name),
                ('tbs', tbs),
            ])

            sign_str = ''.join(['{0}={1}'.format(key, value) for key, value in data.items()])

            sign_str = md5((sign_str + 'tiebaclient!!!').encode('utf-8')).hexdigest().upper()
            data['sign'] = sign_str

            rs.append(grequests.post(sign_url, data=data, headers=self.headers))

        return grequests.map(rs)
