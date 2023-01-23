#!/usr/bin/python3
import pyaudio
import matplotlib.pyplot as plt
import numpy
import time
from amplitude import Amplitude
from vu_constants import RATE, INPUT_FRAMES_PER_BLOCK


def main():
    audio = pyaudio.PyAudio()
    hl, = plt.plot([], [])
    ax = plt.gca()
    ax.set_autoscale_on(True)

    try:
        stream = audio.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=INPUT_FRAMES_PER_BLOCK
                            )

        maximal = Amplitude()

        hl.set_xdata(numpy.append(hl.get_xdata(), 0))
        hl.set_ydata(numpy.append(hl.get_xdata(), 0))
        plt.draw()
        while True:
            data = stream.read(INPUT_FRAMES_PER_BLOCK)
            amp = Amplitude.from_data(data)
            if amp > maximal:
                maximal = amp
            hl.set_xdata(numpy.append(hl.get_xdata(), amp.db_value))
            hl.set_ydata(numpy.append(hl.get_xdata(), 0.1))

            plt.draw()
            amp.display(scale=100, mark=maximal)
            time.sleep(0.1)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


if __name__ == "__main__":
    main()
