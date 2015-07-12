Title: Weekend project: Spotify alarm clock #2
Date: 2015-07-12 20:00
Tags: tinkering, raspberry-pi, rpi, hack
Category: tinkering
Slug: weekend-project-spotify-alarm-clock-part-2
Author: Kasper Jacobsen
Summary: -

So in the first installment we got the hardware and the core software set up.

Time for our own stuff! I quickly smashed together a REST API that can create
and read alarms, and get a list of playlists from the Mopidy server.

It's all located [here on GitHub (raspberry-alarm)][1]. Let's cover the
installation part:

First you need to get a few dependencies:

    $ apt-get install git supervisor

The Pi Musicbox image already has pip and python installed so we don't need to
install that again.

Install, create and activate a `virtualenv` in root's home:

    $ pip install virtualenv
    $ virtualenv env
    $ . env/bin/activate

Now that we've got the `virtualenv` set up, it's time to clone the project with
git and install the projects dependencies:

    $ git clone https://github.com/Dinoshauer/raspberry-alarm.git
    $ cd raspberry-alarm
    $ pip install -r requirements.txt

We are almost there! The program called `supervisor` you installed before is a
process manager, it will help us make sure the REST API and the script is
running. It manages processes based on configuration files and I've written an
example below:

    [program:alarm-clock-api]

    user=root
    directory=/root/raspberry-alarm/
    command=/root/env/bin/python api.py

    autostart=true
    autorestart=true
    startsecs=3
    stopwaitsecs=3

    stopsignal=INT

    stdout_logfile=/root/logs/%(program_name)s.log
    redirect_stderr=true
    stdout_logfile_maxbytes=50MB
    stdout_logfile_backups=5

    [program:alarm-clock-service]

    user=root
    directory=/root/raspberry-alarm/
    command=/root/env/bin/python alarm-clock.py

    autostart=true
    autorestart=true
    startsecs=3
    stopwaitsecs=3

    stopsignal=INT

    stdout_logfile=/root/logs/%(program_name)s.log
    redirect_stderr=true
    stdout_logfile_maxbytes=50MB
    stdout_logfile_backups=5

We will want to place that in the directory `supervisor` looks for
configuration files in, which in this case is `/etc/supervisor/conf.d`, save it
as `alarm-clock.conf`.

Now, all you have to do is run:

    $ supervisorctl update

And you will see supervisor loading and starting the processes. You can now
create a new alarm with the following `curl` call:

    curl -XPOST http://[musicbox_ip]:5000/ -H "Content-Type:application/json" -d '
    {
      "playlist": "foo",
      "days": [
         {"day": "mon", "time": "06:00"},
         {"day": "sun", "time": "20:00"}
      ]
    }'

And on the given time the music should start playing!

That's it for the quick weekend-project! If you have any comments or if you
want to add features to the services we just created submit a pull request or
issue [to the repository][1].

Enjoy!

[1]: https://github.com/Dinoshauer/raspberry-alarm
