import json
import time
import logging
import datetime
from collections import OrderedDict
from importlib import import_module
from sys import argv
from traceback import format_exc

from schedule import Scheduler
from requests.exceptions import BaseHTTPError

logger = logging.getLogger('schedule')


# ref: https://gist.github.com/mplewis/8483f1c24f2d6259aef6
class SafeScheduler(Scheduler):
    def _run_job(self, job):
        try:
            result = super()._run_job(job)
            if not result:
                raise RuntimeError('RuntimeError func.__name__: {0}'.format(job.__name__))
        except (RuntimeError, BaseHTTPError):
            logger.error(format_exc())
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()


with open(argv[1]) as fp:
    schedule = SafeScheduler()
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
    time.sleep(60)
