# iSign

> A record of my ugly code

## Table of Contents

- [requirements](#requirements)
  * [PyCrypto](#pycrypto)
- [usage](#usage)
- [run immediately && tests](#run-immediately----tests)
- [config.sample](#configsample)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## requirements

`pip install -r requirements.txt`

### PyCrypto

 > https://github.com/Legrandin/pycryptodome

## usage

`C:\Python34\python.exe E:/iSign/iSign.py ./config.json`

## run immediately && tests

`python3 -m unittest tests/test_kittens.py`

----------------

## config.sample

``` js
{
    "task_name": {
        "schedule": {
            "interval": 2,  // pause interval * unit between runs (default 1)
            "unit": "hour",  // time units, e.g. 'minutes', 'hours', ...
            "at_time": ""  // optional time at which this job runs
        },
        "enable": false,
        "kitten": "tieba",  // in ./kittens dir
        "config": {
            ... // specific defined by each kitten
        }
    },
    ...
}
```
