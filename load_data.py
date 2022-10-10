import numpy
from numpy import sin, cos, pi, zeros, ones, hstack, linspace, array, arange


class ImportData:
    def __init__(self, file_path=None, image_function=None):
        self.file_path = file_path
        self.image_function = image_function
        self.sampling_rate = None
        self.frequency = []
        self.signal_function = None
        self.normalization_status = True
        self.data = None

    def func_write(self):
        try:
            self.sampling_rate = int(self.image_function.replace(' ', '').split("/")[1].split(')')[0])
            self.data = numpy.atleast_2d(eval(self.image_function))
            if self.normalization_status is True:
                self.normalization()
            return self.data, self.sampling_rate, "Successful function reading"
        except Exception as e:
            print(f"ERROR in read function: {e}")

    def normalization(self):
        self.data = self.data[:, :]/self.data.max()
