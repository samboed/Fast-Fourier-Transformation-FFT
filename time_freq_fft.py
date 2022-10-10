import numpy
from math import *
from fft import FFT


class TFFFT:
    def __init__(self, signal_data, count_window):
        self.signal_length = numpy.shape(signal_data)[1]
        self.degree_fft = ceil(log(self.signal_length, 2))
        self.signal_length_up = 2 ** self.degree_fft
        if self.degree_fft != self.signal_length:
            self.signal_data = numpy.hstack([signal_data,
                                             numpy.zeros((1, self.signal_length_up-self.signal_length))]).astype("complex128")
        self.count_window = int(count_window)
        self.done_data = numpy.ones((int(self.signal_length/self.count_window),
                                     self.signal_length)).astype("complex128")

    def run(self):
        start = 0
        length_window = int(self.signal_length_up/self.count_window)
        end = start + length_window
        list_zeros = [0] * length_window
        for window_fft in range(self.count_window):
            self.done_data[::, start:end:] = FFT(self.signal_data[::,
                                                 start:start+length_window:]).run()[list_zeros].transpose()
            start = (window_fft+1)*length_window
            end = start + length_window
        return self.done_data
