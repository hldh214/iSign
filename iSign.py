import json
import schedule
import time
from collections import OrderedDict
from importlib import import_module
from pathlib import Path

with open(str(Path('./config.json').resolve())) as fp:
    config = json.load(fp, object_pairs_hook=OrderedDict)
    for key, value in config.items():
        if not value['enable']:
            continue

        kitten = import_module('kittens.{}'.format(value['kitten'])).Kitten(value['config'])
        kitten_schedule = value['schedule']

        schedule_unit = getattr(
            schedule.every(kitten_schedule['interval']), kitten_schedule['unit']
        )

        if kitten_schedule['at_time'] is None:
            schedule_unit.do(kitten.meow)
            continue

        schedule_unit.at(kitten_schedule['at_time']).do(kitten.meow)

while True:
    schedule.run_pending()
    time.sleep(10)
