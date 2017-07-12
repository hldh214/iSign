from kittens import *
from collections import OrderedDict
import json

with open('./config.json') as fp:
    config = json.load(fp, object_pairs_hook=OrderedDict)
    for key, value in config.items():
        if not value['enable']:
            continue
        kitten = eval(value['kitten']).Kitten(value['config'])
        res = kitten.meow()

        if isinstance(res, list):
            print([each.text for each in res])
        else:
            print(res.text)
