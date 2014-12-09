Title: Async and blocking I/O in python
Date: 2014-12-09 16:00
Tags: python, asyncio, trollius, python2.7, python3,
Category: coding
Slug: async-and-blocking-io-in-python
Author: Kasper Jacobsen
Summary: -

Disclaimer: This is not an introduction to the asyncio or trollius module. The point is to show how blocking I/O in python can be turned into non-blocking I/O.

I recently had to write a wrapper around an API that had a specifically low hard coded return limit. The consumer of said API runs some map/reduce tasks on the data the API returns and it would be nice to process many pieces of items at a time instead of a few. To get around this problem you could make make sequential/successive calls to the API and merge the results, this however takes a long time. See the example below:

```python
from datetime import datetime

import requests

for url in ['http://google.com' for i in range(20)]:
    print requests.get(url).elapsed, datetime.now()
```


If you could do this asynchronously it would be awesome!
Enter asyncio, the python3 module for working asynchronously it introduces some new concepts like coroutines and futures (think promises if you're from JS-land). The problem with asyncio is that it is strictly python3 so if you need to be python2.7 compatible are you out of luck? No! Trollius is a backport of asyncio. I'll explain the revised example below:

```python
from datetime import datetime

import requests
import trollius


def _get(url):
    return requests.get(url), datetime.now()


def _do_calls(urls):
    loop = trollius.get_event_loop()
    futures = []
    for url in urls:
        futures.append(loop.run_in_executor(None, _get, url))
    return futures


@trollius.coroutine
def call():
    results = []
    futures = _do_calls(['http://google.com' for i in range(20)])
    for future in futures:
        result = yield trollius.From(future)
        print result[0].elapsed, result[1]
        results.append(result)
    raise trollius.Return(results)

loop = trollius.get_event_loop()
print loop.run_until_complete(call())
```

What is happening here is that we're creating an event loop to work in, and defining that it should run until the ``call`` method is complete.
The ``call`` method is getting a list of futures from ``_do_calls`` and resolving them one by one, trollius is then raising an exception to exit the generator
