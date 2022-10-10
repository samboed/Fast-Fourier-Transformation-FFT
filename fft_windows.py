import numpy
from math import *


class WindowFunction:
    def __init__(self, length_data, count_window):
        self.length_data = length_data
        self.window_type = None
        self.window_func = None
        self.count_window = count_window

    def choice_window_interval(self, count_window):
        self.count_window = count_window

    def choice_window_func(self, choice):
        try:
            size_window_array = int(self.length_data / self.count_window)
            N_half = int(size_window_array / 2)
            window_array = numpy.zeros((1, size_window_array))
            match choice:
                case 0:
                    # Прямоугольное окно
                    self.window_type = "Rectangle"
                    window_array[0, :size_window_array] = numpy.full((1, size_window_array), 1)
                    self.window_func = numpy.resize(window_array, (1, self.length_data))
                    return True, self.window_func, self.window_type
                case 1:
                    # Треугольное окно
                    self.window_type = "Triangular"

                    def triangular_func_left(i, j):
                        return j/N_half

                    def triangular_func_right(i, j):
                        return 1 - j/N_half

                    window_array[0, :N_half] = numpy.fromfunction(triangular_func_left, (1, N_half))
                    window_array[0, N_half:size_window_array] = numpy.fromfunction(triangular_func_right, (1, N_half))
                    self.window_func = numpy.resize(window_array, (1, self.length_data))
                    return True, self.window_func, self.window_type
                case 2:
                    # Окно Хеннинга
                    self.window_type = "Henning"

                    def henning_func(i, j):
                        return 0.5 - 0.5*numpy.cos(2*pi*j/(size_window_array-1))

                    window_array[0, :size_window_array] = numpy.fromfunction(henning_func, (1, size_window_array))
                    self.window_func = numpy.resize(window_array, (1, self.length_data))
                    return True, self.window_func, self.window_type
                case 3:
                    # Окно Хэмминга
                    self.window_type = "Hamming"

                    def hamming_func(i, j):
                        return 0.54 - 0.46 * numpy.cos(2 * pi * j / (size_window_array - 1))

                    window_array[0, :size_window_array] = numpy.fromfunction(hamming_func, (1, size_window_array))
                    self.window_func = numpy.resize(window_array, (1, self.length_data))
                    return True, self.window_func, self.window_type
        except Exception as e:
            return False, e
