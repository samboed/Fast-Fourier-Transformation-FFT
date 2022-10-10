from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
import matplotlib.pyplot as plt
import numpy
from load_data import ImportData
from fft_windows import WindowFunction
from time_freq_fft import TFFFT

RGB_CONST = 255
x_window = 1000
y_window = 600
Window.size = (x_window, y_window)
Window.clearcolor = (255 / RGB_CONST, 255 / RGB_CONST, 224 / RGB_CONST, 1)
Window.top = 110
Window.left = 180


class WindowBuild(FloatLayout):
    def __init__(self, **kwargs):
        super(WindowBuild, self).__init__(**kwargs)
        self.sampling_rate = None
        self.net_data_length = None
        self.increases_data_length = None
        self.time_range = None
        self.time_range_fft_data = None
        self.raw_data = None
        self.window_data = None
        self.window_type = None
        self.signal_data_window_TFfft = None
        self.index_window = None
        self.count_window = 1
        self.TFfft_data = None
        self.combined_func = None
        self.signal_data_up = None
        self.window_status = None


        # Design window
        self.label_parameters = Label(
            text=f"Sampling Rate: {self.sampling_rate}\nNet Data Length: {self.net_data_length}\n"
                 f"Increased Data Length: {self.increases_data_length}\n" +
                 f"Time Range Signal: {self.time_range} sec\nTime Range FFT Data: {self.time_range_fft_data} sec\n" +
                 f"Type Window: {self.window_type}",
            halign='left',
            color="white", font_size='15sp',
            pos_hint={"x": 0, "y": 0.8}, size_hint=(0.25, 0.1), )

        self.label_status = Label(text="Enter the function",
                                  color=(0 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1), font_size='20sp',
                                  pos_hint={"x": 0, "y": 0}, size_hint=(1.0, 0.1))

        self.input = TextInput(background_color=(1, 1, 1, 1),
                               pos_hint={"x": 0.25, "y": 0.1},
                               size_hint=(0.75, .1))

        btn_load_func = Button(text="Load Func Signal",
                               halign='center',
                               font_size="20sp",
                               on_press=self.btn_load_func,
                               background_color=(1, 1, 1, 1),
                               color="white",
                               size_hint=(0.25, .1),
                               pos_hint={"x": 0, "y": 0.1})

        btn_start = Button(text="START",
                                font_size="20sp",
                                on_press=self.start,
                                background_color=(1, 1, 1, 1),
                                color="white",
                                size_hint=(0.25, .1),
                                pos_hint={"x": 0, "y": 0.3})

        btn_update_window = Button(text="Update Window",
                                        font_size="20sp",
                                        on_press=self.update_window,
                                        background_color=(1, 1, 1, 1),
                                        color="white",
                                        size_hint=(0.25, .1),
                                        pos_hint={"x": 0, "y": 0.2})

        with self.label_status.canvas:
            Color(102/RGB_CONST, 102/RGB_CONST, 102/RGB_CONST, 1.0)
            Rectangle(pos=(0, 240), size=(250,5000))

        self.slider_window = Slider(min=0, max=0, value=0, step=1,
                                    pos_hint={"x": 0.01, "y": 0.6},
                                    size_hint=(0.23, 0.1))
        self.slider_window.bind(value=self.on_value)

        self.label_window = Label(text= f"Number of windows: {int(2**self.slider_window.value)}",
                                  color="white", font_size='15sp',
                                  pos_hint={"x": 0, "y": 0.65}, size_hint=(0.25, 0.1))
        self.spectogram = GridLayout(cols=1)
        popup = Popup(title="Spectrogram", size_hint=(0.9, 0.9), content=self.spectogram, disabled=True)
        btn_show_spectogram = Button(text="SG", font_size="20sp",
                                     size_hint=(0.05, 0.05),
                                     pos_hint={"x": 0.875, "y": 0.95})
        btn_show_spectogram.bind(on_release=popup.open)
        self.graph_3D = GridLayout(cols=1)
        popup = Popup(title="3D Spectrogram", size_hint=(0.9, 0.9), content=self.graph_3D, disabled=True)
        btn_show_graph_3D = Button(text="SG-3D", font_size="20sp",
                                   size_hint=(0.075, 0.05),
                                   pos_hint={"x": 0.925, "y": 0.95})
        btn_show_graph_3D.bind(on_release=popup.open)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequence')
        ax.set_zlabel('Amplitude')
        plt.title('Time Frequency Response of the Signal')
        plt_graph_3D = FigureCanvasKivyAgg(plt.gcf(), size_hint=(1.0, 1.0))
        self.graph_3D.add_widget(plt_graph_3D)
        plt.close()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title('Time Frequency Response of the Signal')
        plt_spectogram = FigureCanvasKivyAgg(plt.gcf(), size_hint=(1.0, 1.0))
        self.spectogram.add_widget(plt_spectogram)
        plt.close()
        self.figure_signal, ax = plt.subplots()
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Timing Diagram')
        plt.grid(True, color='lightgray')
        plt_signal = FigureCanvasKivyAgg(plt.gcf(), size_hint=(0.8, 0.8), pos_hint={"x": 0.25, "y": 0.20})
        self.add_widget(plt_signal)
        self.add_widget(self.label_status)
        self.add_widget(self.input)
        self.add_widget(btn_load_func)
        self.add_widget(btn_start)
        self.add_widget(btn_update_window)
        self.add_widget(btn_show_spectogram)
        self.add_widget(btn_show_graph_3D)
        self.add_widget(self.label_parameters)
        self.add_widget(self.slider_window)
        self.add_widget(self.label_window)

        name_select_rect_win = Label(text="Rectangle Window", pos_hint={"x": -0.38, "y": 0.10},
                                     color="white", font_size='15sp')
        self.add_widget(name_select_rect_win)
        self.active = CheckBox(active=False, pos_hint={'center_x': .04, 'center_y': .60}, group='group',
                               size_hint=(0.03, 0.03), on_active=self.select_rect)
        self.active.bind(active=self.select_rect)
        self.add_widget(self.active)

        name_select_triang_win = Label(text="Triangle Window", pos_hint={"x": -0.38, "y": 0.05},
                                       color="white", font_size='15sp')
        self.add_widget(name_select_triang_win)
        self.active = CheckBox(active=False, pos_hint={'center_x': .04, 'center_y': .55}, group='group',
                               size_hint=(0.03, 0.03), on_active=self.select_triang)
        self.active.bind(active=self.select_triang)
        self.add_widget(self.active)

        name_select_henning_win = Label(text="Henning Window", pos_hint={"x": -0.38, "y": 0},
                                        color="white", font_size='15sp')
        self.add_widget(name_select_henning_win)
        self.active = CheckBox(active=False, pos_hint={'center_x': .04, 'center_y': .50}, group='group',
                               size_hint=(0.03, 0.03), on_active=self.select_henning)
        self.active.bind(active=self.select_henning)
        self.add_widget(self.active)

        name_select_hamming_win = Label(text="Hamming Window", pos_hint={"x": -0.38, "y": -0.05},
                                        color="white", font_size='15sp')
        self.add_widget(name_select_hamming_win)
        self.active = CheckBox(active=False, pos_hint={'center_x': .04, 'center_y': .45}, group='group',
                               size_hint=(0.03, 0.03), on_active=self.select_hamming)
        self.active.bind(active=self.select_hamming)
        self.add_widget(self.active)

    def on_value(self, instance, brightness):
        self.count_window = 2**brightness
        self.label_window.text = f"Number of windows: {int(2**brightness)}"

    def select_rect(self, checkbox, value):
        try:
            if value:
                self.index_window = 0
            else:
                self.index_window = None
        except AttributeError:
            pass

    def select_triang(self, checkbox, value):
        try:
            if value:
                self.index_window = 1
            else:
                self.index_window = None
        except AttributeError:
            pass

    def select_henning(self, checkbox, value):
        try:
            if value:
                self.index_window = 2
            else:
                self.index_window = None
        except AttributeError:
            pass

    def select_hamming(self, checkbox, value):
        try:
            if value:
                self.index_window = 3
            else:
                self.index_window = None
        except AttributeError:
            pass

    def btn_load_func(self, instance):
        image_func = self.input.text
        if image_func == "":
            self.label_status.text = "ERROR INPUT: describe the function"
            self.label_status.color = 255/RGB_CONST, 0/RGB_CONST, 0/RGB_CONST, 1
        else:
            res_processing = ImportData(image_function=image_func).func_write()
            try:
                if res_processing[0] is False:
                    self.label_status.text = "ERROR INPUT: incorrect function description, see help"
                    self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1
                else:
                    self.raw_data = res_processing[0]
                    self.sampling_rate = res_processing[1]
                    self.label_status.text = res_processing[2]
                    self.net_data_length = numpy.shape(self.raw_data)[1]
                    if self.index_window is None:
                        self.index_window = 0
                    self.label_status.color = 0 / RGB_CONST, 255 / RGB_CONST, 0 / RGB_CONST, 1

                    raw_data_TFfft = TFFFT(self.raw_data, self.count_window)

                    self.increases_data_length = raw_data_TFfft.signal_length_up
                    self.signal_data_up = raw_data_TFfft.signal_data
                    self.window_status = WindowFunction(self.increases_data_length, self.count_window)
                    self.window_data = self.window_status.choice_window_func(self.index_window)[1]

                    self.combined_func = self.signal_data_up * self.window_data
                    self.signal_data_window_TFfft = TFFFT(self.combined_func, self.count_window)

                    self.update_label_parameters()
                    self.update_plot_signal()

                    self.slider_window.max = self.signal_data_window_TFfft.degree_fft - 4
            except TypeError:
                self.label_status.text = "ERROR INPUT: incorrect function description, see help"
                self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1

    def start(self, instance):
        if self.signal_data_window_TFfft is None:
            self.label_status.text = "ERROR ANALYSIS: imported data is missing"
            self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1
        elif self.window_data is None:
            self.label_status.text = "ERROR ANALYSIS: select a window"
            self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1
        else:

            self.signal_data_window_TFfft = TFFFT(self.combined_func, self.count_window)
            self.TFfft_data = self.signal_data_window_TFfft.run()
            self.length_TFfft_data = self.TFfft_data.shape
            self.label_status.text = "Complete"
            self.label_status.color = 0 / RGB_CONST, 255 / RGB_CONST, 0 / RGB_CONST, 1
            self.update_plot_tffft()

    def update_window(self, instance):
        try:
            if self.index_window is None:
                self.label_status.text = "ERROR UPDATE WINDOW: window type no selected"
                self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1
            elif self.combined_func is None:
                self.label_status.text = "ERROR UPDATE WINDOW: function data no load"
                self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1
            else:
                self.window_status = WindowFunction(self.increases_data_length, self.count_window)
                res_processing = self.window_status.choice_window_func(self.index_window)
                self.window_data = res_processing[1]
                self.window_type = res_processing[2]
                self.combined_func = self.signal_data_up * self.window_data
                self.update_label_parameters()
                self.update_plot_signal()
        except AttributeError:
            self.label_status.text = "ERROR UPDATE WINDOW: imported data is missing"
            self.label_status.color = 255 / RGB_CONST, 0 / RGB_CONST, 0 / RGB_CONST, 1

    def update_label_parameters(self):
        self.time_range = float(self.net_data_length / self.sampling_rate)
        self.time_range_fft_data = float(self.increases_data_length / self.sampling_rate)
        self.window_type = self.window_status.window_type
        self.label_parameters.text = f"Sampling Rate: {self.sampling_rate} Gz\nNet Data Length: {self.net_data_length}\n" \
                                     f"Increased Data Length: {self.increases_data_length}\n" + \
                                     "Time Range Signal: {:.3f} sec\nTime Range FFT Data: {:.3f} sec\n".format(
                                     self.time_range, self.time_range_fft_data) + \
                                     f"Type Window: {self.window_type}"

    def update_plot_signal(self):
        plt.clf()
        y_amp = self.signal_data_up.copy()[0, ::]
        x_time = numpy.array(range(0,len(y_amp))) / self.sampling_rate
        plt.plot(x_time, y_amp, color="steelblue")
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Timing Diagram')
        plt.grid(True, color='lightgray')
        if self.window_data is not None:
            window_data = self.window_data.copy()[0, ::]
            plt.plot(x_time, window_data, color="r")
            plt.plot(x_time, self.combined_func[0, ::], color="y")
        self.figure_signal.canvas.draw()

    def update_plot_tffft(self):
        x_time = numpy.array(range(0, self.increases_data_length)) / self.sampling_rate
        sampling_rate = self.sampling_rate
        increases_data_length = self.increases_data_length

        def frequency_axes(i):
            return i*sampling_rate/increases_data_length

        x = abs(x_time)
        z = (2 * abs(self.TFfft_data[:int(self.length_TFfft_data[0]/2), ::]) / self.increases_data_length)
        y = x.copy()
        y = numpy.fromfunction(frequency_axes, x.shape)[:int(self.length_TFfft_data[0]/2):] * self.count_window

        fig = plt.figure()
        ax = fig.add_subplot(111)
        pcolormesh = plt.pcolormesh(x[::4], y, z[::, ::4], shading='gouraud')
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        fig.colorbar(pcolormesh, shrink=1.0, aspect=8)
        ax.set_title('Time Frequency Response of the Signal')
        self.spectogram.clear_widgets()
        self.spectogram.add_widget(FigureCanvasKivyAgg(plt.gcf(), size_hint=(1.0, 1.0), pos_hint={"x": 0, "y": 0}))
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        surf = ax.plot_surface(y[None, :], x[::4, None], z.transpose()[::4, ::], cmap=plt.cm.cividis)
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Time')
        ax.set_zlabel('Amplitude')
        fig.colorbar(surf, shrink=0.5, aspect=6, pad=0.1)
        ax.set_title('Time Frequency Response of the Signal')
        self.graph_3D.clear_widgets()
        self.graph_3D.add_widget(FigureCanvasKivyAgg(plt.gcf(), size_hint=(1.0, 1.0), pos_hint={"x": 0, "y": 0}))
        plt.close()


class MyApp(App):

    def build(self):
        return WindowBuild()


if __name__ == '__main__':
    App_Window = MyApp()
    App_Window.title = "Time-Frequency FFT"
    App_Window.run()

