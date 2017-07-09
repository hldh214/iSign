from kittens import *
from collections import OrderedDict
import json

with open('./config.json') as fp:
    config = json.load(fp, object_pairs_hook=OrderedDict)
    for key, value in config.items():
        kitten = eval(value['kitten']).Kitten(value['config'])
        print(kitten.meow().text)
