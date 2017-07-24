import grequests
import qqlib


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
        qq = qqlib.QQ(self.config['usn'], self.config['pwd'])
        qq.login()

        skey = qq.session.cookies.get('skey')
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
