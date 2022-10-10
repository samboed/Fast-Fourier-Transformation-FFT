import numpy
from math import *
from cmath import exp as exp_complex


class FFT:
    def __init__(self, raw_data):
        self.length_raw_data = numpy.shape(raw_data)[1]
        self.degree_fft = ceil(log(self.length_raw_data, 2))
        self.length_up_raw_data = 2**self.degree_fft
        if self.degree_fft != self.length_raw_data:
            raw_data = numpy.hstack([raw_data, numpy.zeros((1,  self.length_up_raw_data - self.length_raw_data))])
        self.list_dft_data = raw_data.astype("complex128")
        self.turning_coefficients = None
        self.fft_data = None

    def __splitting(self, raw_data):
        for ind_split in range(0, self.degree_fft-1):
            N = int(self.length_up_raw_data / 2 ** (ind_split + 1))
            raw_data_even = numpy.atleast_2d(raw_data[0, ::2].copy()).reshape(2**ind_split, N)
            raw_data_odd = numpy.atleast_2d(raw_data[0, 1::2].copy()).reshape(2**ind_split, N)
            raw_data = numpy.hstack([raw_data_even, raw_data_odd]).reshape(1, self.length_up_raw_data)
        return raw_data

    def __search_coefficients_fft(self, step_thinning):
        N = 2**(step_thinning+1)
        n = 2**step_thinning
        for m in range(0, n):
            self.turning_coefficients[0, m::n] = self.turning_coefficients[0, m::n] * exp_complex(-1j*2*pi*m/N)

    def __dft(self, split_part_data, step_thinning):
        M = 2**(self.degree_fft-step_thinning)
        split_part_data = numpy.atleast_2d(split_part_data).reshape(M, int(self.length_up_raw_data / M)).copy()
        x = split_part_data[::2, :].copy()
        y = split_part_data[1::2, :].copy()
        turning_coefficients = self.turning_coefficients.reshape(int(M / 2), int(self.length_up_raw_data / M)).copy()
        split_part_data[::2, :] = x.copy() + y.copy() * turning_coefficients.copy()
        split_part_data[1::2, :] = x.copy() - y.copy() * turning_coefficients.copy()
        return split_part_data.reshape(1, self.length_up_raw_data)

    def __unification(self):
        flat_fft_data_split = self.__splitting(self.list_dft_data).astype("complex128")
        for step_thinning in range(0, self.degree_fft):
            self.turning_coefficients = numpy.ones((1, int(self.length_up_raw_data / 2))).astype("complex128")
            self.__search_coefficients_fft(step_thinning)
            flat_fft_data_split = self.__dft(flat_fft_data_split, step_thinning)
        self.fft_data = flat_fft_data_split.copy()

    def run(self):
        self.__unification()
        return self.fft_data
