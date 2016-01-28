# raspberry pi as a streamer/recorder

## Stuff used

* [bottle.py Python Web Framework](http://bottlepy.org/)
* [Vue.js library for building interactive web interfaces](http://vuejs.org/)
* [CSS with superpowers (SASS)](http://sass-lang.com/)
* [Compass CSS Authoring Framework](http://compass-style.org/)
* [alsacap](http://www.volkerschatz.com/noise/alsa.html)

## Sponsor

(please add sponsor info here)

## Dcos

Docs are currently availabe in [english](https://github.com/faebser/pi-stream/blob/master/docs/en/index.md) and [deutsch](https://github.com/faebser/pi-stream/blob/master/docs/de/index.md).

## Setup

*Note*: We will provide premade raspian disk images in the future.
Taken from here: https://stmllr.net/blog/live-streaming-mp3-audio-with-darkice-and-icecast2-on-raspberry-pi/

### Preconditions

* Raspberry Pi running Raspbian
* USB sound stick

### Compiling and installing DarkIce

The default darkice package comes without MP3 support. Since most of the Iceast-Hosting providers use MP3 we need to build Darkice with MP3 support from the sources.

Add a deb-src repository to your sources list at /etc/apt/sources.list:

    $ sudo sh -c "echo 'deb-src http://mirrordirector.raspbian.org/raspbian/ wheezy main contrib non-free rpi' >> /etc/apt/sources.list"
    $ sudo apt-get update
    (...some output...)

To fullfill the build dependencies, we have to install some additional packages:
    
    $ sudo apt-get --no-install-recommends install build-essential devscripts autotools-dev fakeroot dpkg-dev debhelper autotools-dev dh-make quilt ccache libsamplerate0-dev libpulse-dev libaudio-dev lame libjack-jackd2-dev libasound2-dev libtwolame-dev libfaad-dev libflac-dev libmp4v2-dev libshout3-dev libmp3lame-dev

Create a working directory:

    $ mkdir src && cd src/

Get the source package of darkice:

    $ apt-get source darkice
    (... some output ...)

Change the compile configuration to match Raspbian environment:

    $ cd darkice-1.0/
    $ vi debian/rules

    #!/usr/bin/make -f
    %:

         dh $@

    .PHONY: override_dh_auto_configure
    override_dh_auto_configure:
          ln -s /usr/share/misc/config.guess .
          ln -s /usr/share/misc/config.sub .
            dh_auto_configure -- --prefix=/usr --sysconfdir=/usr/share/doc/darkice/examples --with-vorbis-prefix=/usr/lib/arm-linux-gnueabihf/ --with-jack-prefix=/usr/lib/arm-linux-gnueabihf/ --with-alsa-prefix=/usr/lib/arm-linux-gnueabihf/ --with-faac-prefix=/usr/lib/arm-linux-gnueabihf/ --with-aacplus-prefix=/usr/lib/arm-linux-gnueabihf/ --with-samplerate-prefix=/usr/lib/arm-linux-gnueabihf/ --with-lame-prefix=/usr/lib/arm-linux-gnueabihf/ CFLAGS='-march=armv6 -mfpu=vfp -mfloat-abi=hard'

Please make sure that that you are using tabs for the indentation. The build will fail with spaces. Download the [rules](https://raw.githubusercontent.com/faebser/pi-stream/master/rules) if you encouter any problems.

Before we start to build the package, change the version of the package to reflect MP3 support. Debchange will ask you to add some comments to the changelog.

    $ debchange -v 1.0-999~mp3+1

    darkice (1.0-999~mp3+1) UNRELEASED; urgency=low

      * New build with mp3 support

     --  <pi@raspberrypi>  Sat, 11 Aug 2012 13:35:06 +0000

Now we are ready to build and install the new Darkice package:

    $ dpkg-buildpackage -rfakeroot -uc -b
    (... some output ...)
    $ sudo dpkg -i ../darkice_1.0-999~mp3+1_armhf.deb
    (... some output ...)
    Preparing to replace darkice 1.0-999 (using .../darkice_1.0-999~mp3+1_armhf.deb) ...
    Unpacking replacement darkice ...
    Setting up darkice (1.0-999~mp3+1) ...
    (... some output ...)

Tada, now Darkice with MP3 spport should be installed. To test please run:
    
    $ darkice

## Installing alsacap

* get the source from here: http://www.volkerschatz.com/noise/alsa.html (http://www.volkerschatz.com/noise/alsacap.tgz)
* ```mkdir alsacap ; cd alsacap```
* ```sudo make install```
* test with ```alsacap```

## Installing kernel I2C support

    sudo apt-get install python-smbus
    sudo apt-get install i2c-tools

## Running 

* ssh into your raspberry
* clone this repository
* make sure that bottle.py and pistream.py are executable
* ```sudo make run``` to start the server
* IP address will be on the LCD display or printed into stdout.