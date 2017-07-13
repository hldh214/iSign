import json
import schedule
import time
from collections import OrderedDict
from importlib import import_module

with open('./config.json') as fp:
    config = json.load(fp, object_pairs_hook=OrderedDict)
    for key, value in config.items():
        if not value['enable']:
            continue

        kitten = import_module('kittens.{}'.format(value['kitten'])).Kitten(value['config'])
        kitten_schedule = value['schedule']

        getattr(
            schedule.every(kitten_schedule['interval']), kitten_schedule['unit']
        ).at(kitten_schedule['at_time']).do(kitten.meow)

while True:
    schedule.run_pending()
    time.sleep(10)
