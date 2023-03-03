# vu-meter
*Measure volumes unit with Python, and more !*

## Requirements
* [PyAudio](https://pypi.python.org/pypi/PyAudio)
* [NumPy](https://pypi.python.org/pypi/numpy)
* [Matplotlib](https://pypi.python.org/pypi/matplotlib)
* [SoundDevice](https://pypi.python.org/pypi/sounddevice)
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) (for Raspberry Pi)
* [RPi.GPIO emulator](https://github.com/nosix/raspberry-gpio-emulator) (for non-Raspberry Pi)
* [SciPy](https://pypi.python.org/pypi/scipy)

## Usage
### On your computer
Just run `vu_graph_maker.py`, clap your hands in front of the mic, and see every graph waving!

### On a Raspberry Pi
Run `vu_meter_rasp.py`, plug a LED in GPIO 32 and a USB mic, and see what it does!