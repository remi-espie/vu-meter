''' This module introduces the Amplitude class which collects methods for
calculating, adding and displaying. '''

import math
import struct
from vu_constants import SHORT_NORMALIZE

class Amplitude:
    ''' an abstraction for Amplitudes (with an underlying float value)
    that packages a display function and many more '''

    def __init__(self, db_value=0):
        self.db_value = db_value
        self.boundary_char = '|'
        self.audio_char = '*'
        self.silence_char = ' '

    def __add__(self, other):
        return Amplitude(self.db_value + other.db_value)

    def __sub__(self, other):
        return Amplitude(self.db_value - other.db_value)

    def __gt__(self, other):
        return self.db_value > other.db_value

    def __lt__(self, other):
        return self.db_value < other.db_value

    def __eq__(self, other):
        return self.db_value == other.db_value

    def to_int(self, scale=1):
        ''' convert an amplitude to an integer given a scale such that one can
        choose the precision of the resulting integer '''
        return int(self.db_value * scale)

    def __int__(self):
        return self.to_int()

    def __str__(self):
        return self.db_value + " dB"

    @staticmethod
    def from_data(block):
        '''Generate an Amplitude object based on a block of audio input data'''
        count = len(block) / 2
        shorts = struct.unpack("%dh" % count, block)
        sum_squares = sum(s**2 * SHORT_NORMALIZE**2 for s in shorts)
        return Amplitude(math.sqrt(sum_squares / count))

    def display(self, mark, scale=50):
        '''Display an amplitude and another (marked) maximal Amplitude
        graphically '''
        vu_int = self.to_int(scale)
        mark_val = mark.to_int(scale)
        delta = abs(vu_int - mark_val)
        visual_str = f'{self.boundary_char}'
        visual_str += f'{self.audio_char * vu_int}'
        visual_str += f'{self.silence_char * (delta-1)}'
        visual_str += f'{self.boundary_char}'
        print(visual_str)
