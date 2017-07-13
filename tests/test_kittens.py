import unittest
import json
from collections import OrderedDict
from importlib import import_module


class MyTestCase(unittest.TestCase):
    def test_kittens(self):
        with open('./config.json') as fp:
            config = json.load(fp, object_pairs_hook=OrderedDict)
            for key, value in config.items():
                if not value['enable']:
                    continue

                kitten = import_module('kittens.{}'.format(value['kitten'])).Kitten(value['config'])
                res = kitten.meow()

                if isinstance(res, list):
                    [self.assertEqual(each.status_code, 200) for each in res]
                else:
                    self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
