PyAlsaCap
=========

PyAlsaCap is a tool inspired from `alsacap` written by [Volker Schatz](http://www.volkerschatz.com/profile.html).

`alsacap` is a C command line tool allowing user to query soundcards (formats, capabilities), [`pyalsacap.py`](pyalsacap.py) is a Python 3 alsacap clone that mimic alsacap.
PyAlsaCap can also be used as a Python module, because it does not only print sound card information but alsa generates a Python3 data structure with this informations.

PyAlsaCap query directly libasound2 alsa C-library using Python `ctypes` module.

State
-----

PyAlsaCap is not complete, all the alsacap args are not handled.

Usage
-----

You can use PyAlsaCap from shell:

```text
luser@computer ~ $ ./pyalsacap.py -R
*** Scanning for recording devices ***
Card 0, ID `Intel', name `HDA Intel'
  Device 0, ID `AD198x Analog', name `AD198x Analog', 2 subdevices (2 available)
    2 channels, sampling rate 8000..192000 Hz
    Sample formats: S16_LE
      Subdevice 0, name `subdevice #0'
      Subdevice 1, name `subdevice #0'
Card 29, ID `ThinkPadEC', name `ThinkPad Console Audio Control'
```

You can compare with alsacap output:

```text
luser@computer ~ $ ./alsacap -R
*** Scanning for recording devices ***
Card 0, ID `Intel', name `HDA Intel'
  Device 0, ID `AD198x Analog', name `AD198x Analog', 2 subdevices (2 available)
    2 channels, sampling rate 8000..192000 Hz
    Sample formats: S16_LE, S32_LE
      Subdevice 0, name `subdevice #0'
      Subdevice 1, name `subdevice #1'
Card 29, ID `ThinkPadEC', name `ThinkPad Console Audio Control'
```

You can use PyAlsaCap from Python:

```python
In [1]: from pyalsacap import *
In [2]: insp = Inspector()
In [3]: cards = insp.GetCards()
In [4]: cards
Out[4]:
{
    0: {
        'id': 'Intel',
        'name': 'HDA Intel',
        'devices': {
            0: {
                'channels': [2, 2],
                'formats': ['S16_LE'],
                'id': 'AD198x Analog',
                'name': 'AD198x Analog',
                'rate': [8000, 192000],
                'subdevices_available': 1,
                'subdevices': {
                    0: {
                        'name': 'subdevice #0'
                    }
                }
            },
            1: {
                'channels': [2, 2],
                'formats': ['S16_LE'],
                'id': 'AD198x Digital',
                'name': 'AD198x Digital',
                'rate': [44100, 192000],
                'subdevices_available': 1,
                'subdevices': {
                    0: {
                        'name': 'subdevice #0'
                    }
                }
            }
        }
    },
    29: {
        'id': 'ThinkPadEC',
        'name': 'ThinkPad Console Audio Control',
        'devices': {
        }
    }
}
```

Author
------

PyAlsaCap is written by Thomas Debesse <pyalsacap@illwieckz.net>.

Original `alsacap` is written by Volker Schatz (alsacap on the volkerschatz.com domain).

License
-------

PyAlsaCap is distributed under the free non-copyleft [ISC license](COPYING.md).

Useful links:
-------------

* [Volker Schatz's alsacap source code](http://www.volkerschatz.com/noise/alsacap.c);
* [PyAlsaCap : Python, pointeurs, et cartes sons…](http://linuxfr.org/users/illwieckz/journaux/pyalsacap-python-pointeurs-et-cartes-sons), a french blog entry that present the first public version of pyAlsaCap with some explanation (can be used as a french tutorial for programming in Python with ctypes);
* [Python official website](https://www.python.org/);
* [Python ctypes module documentation](http://docs.python.org/dev/library/ctypes.html);
* [Advanced Linux Sound Architecture (ALSA) project homepage](http://www.alsa-project.org).
