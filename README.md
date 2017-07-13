# iSign

## A record of my ugly code

----------------

## usage

`C:\Python34\python.exe E:/iSign/iSign.py ./config.json`

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
