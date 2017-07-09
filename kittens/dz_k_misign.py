import requests
import re


class Kitten:
    def __init__(self, config):
        self.config = config

    def meow(self):
        hash_url = '{0}/plugin.php?id=k_misign:sign'.format(self.config['base_url'])
        re_hash = re.compile(r'formhash=(.+)">\u9000\u51fa</a>')
        headers = {'Cookie': self.config['cookie']}
        req = requests.get(hash_url, headers=headers)
        formhash = re_hash.findall(req.text)
        if not formhash:
            return False
        sign_url = '{0}/plugin.php?id=k_misign:sign&operation=qiandao&formhash={1}'.format(
            self.config['base_url'], formhash[0]
        )

        return requests.get(sign_url, headers=headers)
