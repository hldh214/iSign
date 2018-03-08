import grequests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


class Kitten:
    def __init__(self, config):
        self.config = config

    def gen_bkn(self, skey, var_i=5381):
        for each in skey:
            var_i += self.int_overflow(var_i << 5) + ord(each)

        return 2147483647 & var_i

    @staticmethod
    def int_overflow(val):
        maxint = 2147483647
        if not -maxint - 1 <= val <= maxint:
            val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
        return val

    def meow(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.binary_location = self.config['binary_location']

        opener = webdriver.Chrome(chrome_options=chrome_options)

        opener.get(
            'http://ui.ptlogin2.qq.com/cgi-bin/login?'
            'pt_hide_ad=1&style=9&appid=549000929&pt_no_auth=1&s_url=http://qzone.qq.com'
        )

        opener.find_element_by_xpath('//*[@id="u"]').send_keys(self.config['usn'])
        opener.find_element_by_xpath('//*[@id="p"]').send_keys(self.config['pwd'])

        opener.find_element_by_xpath('//*[@id="go"]').click()

        try:
            while opener.get_cookie('skey') is None:
                pass
        except WebDriverException:
            pass

        skey = opener.get_cookie('skey').get('value')
        opener.quit()

        headers = {
            'cookie': 'uin={0}; skey={1}'.format(self.config['usn'], skey)
        }

        return grequests.map((
            # clock_in
            grequests.get(
                'https://ti.qq.com/cgi-node/signin/pickup',
                headers=headers
            ),
            # qq_qun_gift
            grequests.post(
                'http://pay.qun.qq.com/cgi-bin/group_pay/good_feeds/draw_lucky_gift',
                data='bkn={}'.format(self.gen_bkn(skey)),
                headers=headers
            )
        ))
