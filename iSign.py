import json
import time
import logging
import datetime
import threading
from collections import OrderedDict
from importlib import import_module
from sys import argv, stdout
from traceback import format_exc

from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)

from schedule import Scheduler
from requests.exceptions import RequestException

logging.basicConfig(stream=stdout, level=logging.ERROR, format='%(asctime)s - %(message)s')
logger = logging.getLogger('schedule')


# ref: https://gist.github.com/mplewis/8483f1c24f2d6259aef6
class SafeScheduler(Scheduler):
    def _run_job(self, job):
        try:
            super()._run_job(job)
        except (RuntimeError, RequestException, ValueError):
            logger.error(format_exc())
            job.last_run = datetime.datetime.now()
            job._schedule_next_run()


# ref: https://schedule.readthedocs.io/en/stable/faq.html#how-to-execute-jobs-in-parallel
def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


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

        if kitten_schedule['at_time'] is not None:
            schedule_unit = schedule_unit.at(kitten_schedule['at_time'])

        if ('multi_thread' in value) and value['multi_thread']:
            schedule_unit.do(run_threaded, kitten.meow)
        else:
            schedule_unit.do(kitten.meow)

while True:
    schedule.run_pending()
    time.sleep(60)
