Title: Weekend project: Spotify alarm clock #1
Date: 2015-07-12 18:00
Tags: tinkering, raspberry-pi, rpi, hack
Category: tinkering
Slug: weekend-project-spotify-alarm-clock-part-1
Author: Kasper Jacobsen
Summary: -

## Motivation

I like waking up to music in the morning. I use [Spotify][1] a lot.

## The problem?

The apps for iOS that function as a spotify alarm clock all require that they
are left open over night, or iOS will block the app from starting spotify I
guess. *This sucks.* **Hard.**

## Solution!

I have a Raspberry Pi, I have a Spotify account. I know the [mopidy][2] project
exists. I also know that the [Pi Musicbox][3] project exists!

All I need is a speaker of some sort and I'm pretty much ready to throw myself
into the deep end.

I thought I'd just get a cheap mini-speaker (one of those portable ones) to
start with, and I ended up with one of these [JBL Go][4]'s. It's not my place
to review the speaker itself as I am in no way an audiophile and it's out of
the scope of this post.

Seeing as the JBL Go has bluetooth I figured I'd give it a shot setting using
bluetooth, so I got a [USB Bluetooth dongle][5] as well. Apparently using
bluetooth with anything else than a mouse/keyboard is a pain in the ass, so I
spent a few hours on the initial Arch install of the Raspberry Pi trying to get
that to work. Now, in retrospect I could've maybe gotten the older BlueZ4 and
gotten away with using Arch. But since debian is lovely and not at all up to
date on the packages in the repos it was way easier to go with a debian distro
for this quick hack.

## Getting started

So after my failed late-night attempt with Arch, I decided to start fresh and
go directly with the [Pi Musicbox][3] distro. After the initial setup and
testing that everything was working correctly without the bluetooth speaker, I
started setting that up.

You'll need the bluetooth packages ofcourse.

    $ apt-get install bluetooth bluez bluez-utils bluez-alsa

And make sure that your interface is up (also, don't forget to turn on the
speaker):

    $ hcitool hci0 up
    $ hcitool scan

Once you got your speakers `MAC` address, you'll want to pair it to your Pi:

    $ bluez-simple-agent hci0 0C:A6:94:F9:C0:F4

This is where I first ran into trouble. The `bluez-simple-agent` script seems
to be flawed somehow, so I had to edit the script myself. Open the file at
`/usr/bin/bluez-simple-agent` and change:

    capability = "KeyboardDisplay"

to:

    capability = "DisplayYesNo"

That did the trick, and I could successfully pair to my speaker. So, now you
can connect to the speaker with:

    $ bluez-test-audio connect 0C:A6:94:F9:C0:F4


Now, you just have to trust the unit:

    $ bluez-test-device trusted 0C:A6:94:F9:C0:F4 yes

(You can run `bluez-test-device trusted 0C:A6:94:F9:C0:F4` to see if it's
trusted, 0 = No 1 = Yes)

Now you have to edit the alsa-sound config file. I couldn't get it to work with
editing `~/.asoundrc`, so I just went for `/etc/asound.conf`. Add this section,
to the file:

    pcm.bluetooth {
        type bluetooth
        device 0C:A6:94:F9:C0:F4
        profile "auto"
    }

Then I added the following to the specific sections of
`/etc/bluetooth/audio.conf`:

    [General]
    Enable=Source,Sink,Socket

    ...

    Disable=Media

And restart the bluetooth service:

    $ service bluetooth restart

Now you can play music over bluetooth via your Raspberry Pi, but it doesn't
work with Mopidy just yet. The Mopidy forums were very helpful
[(check out this question, we're going to be doing the same thing).][6]

You actually only need to set a few config parameters in
`/etc/mopidy/mopidy.conf`:

    [audio]

    ...

    output = alsasink device=bluetooth

    [alsamixer]
    card = 0
    control = PCM

Now, as for the `[alsamixer]` section you can run `amixer scontrols`, to see
what you should put there, I figure the values above are fairly standard for a
Raspberry Pi.

You will also have to do something about `/opt/musicbox/setsound.sh` as that
script "resets" the alsa config in `/etc/asound.conf` that we edited earlier.

Since that script is run at startup it'd be very neat to make the Pi connect,
to the speaker during startup so we wouldn't have to log in and connect to the
speaker manually in case the Pi reboots. First we'll back up the original
script:

    $ mv /opt/musicbox/setsound.sh{,.bak}

Then we can add our own in `/opt/musicbox/setsound.sh` with these contents:

    #!/bin/bash

    bluez-test-audio connect 0C:A6:94:F9:C0:F4

Now the Pi is going to try and connect to the speaker during startup! That's
great!

## Quick recap

What we have now:

* Fully functional Pi Musicbox setup that is connected to the bluetooth speaker

What we still don't have:

* Alarm clock functionality

Check out the next part, soon to come for the actual alarm clock functions!

[1]: https://spotify.com/
[2]: https://mopidy.com/
[3]: http://www.pimusicbox.com/
[4]: http://eu.jbl.com/jbl_product_detail_eu/jbl-go-black.html
[5]: http://www.belkin.com/us/p/P-F8T065/
[6]: https://discuss.mopidy.com/t/howto-connect-musicbox-to-bluetooth/697/6
