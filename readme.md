Time-Frequency Fast-Fourier-Transformation
========================
* **Table of contents**
  * [Features](#Features)
  * [Interface Description](#Interface-Description)
  * [Demonstration of the program](#Demonstration-of-the-program)

Features
-------------------------

Fast-Fourier-Transformation-FFT performs the time-frequency FFT of the input signal and displays the result in the form of a 3D graph and spectrogram. The FFT is implemented by [the Cooley–Tukey FFT algorithm](#https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm) (time-thinning FFT). There is a choice of 4 types of windows presented: Rectangle, Triangle, Hanning, Hamming and the ability to set an arbitrary width of the DFT window. Signal input is carried out using the functions of the NumPy **arange** and **linspace** module.

Interface Description
-------------------------

The title of the window contains the name of the program, on the right side there are buttons for minimizing, expanding and closing the program. Information about the loaded signal and the selected window **[1]** is displayed on the control panel of the program, which has the following set of tools:

1. Loading the signal function **[2]** – import from the input field **[3]** of the description of the signal function;

2. Adjusting the screen width **[4]** using the slider (number of windows);

3. Selecting the type of window **[5]** (Rectangular, Triangular, Henning. Hamming);

4. Updating window parameters **[6]**, all changes are displayed on the time graph **[7]**;

5. FFT start button **[8]**;

6. Displaying FFT results **[9]**.

![interface](/photo/interface.png)

Demonstration of the program
-------------------------

**Input data:**

```mathematica
signal #1: t = {0:6}, A = 2.00, f = 5, SIN 
signal #2: t = {0:6}, A = 0.50, f = 55, COS
signal #3: t = {0:6}, A = 0.50, f = 240, COS
signal #4: t = {0:2}, A = 0.75, f = 100, COS
signal #5: t = {2:4}, A = 0.75, f = 145, COS
signal #6: t = {4:6}, A = 1.20, f = 30, COS
num = 500(step)*2(sampling rate)  
```

**Description of the signal using the NumPy module:**

```python
hstack((sin(2*pi*5*arange(500*2)/500) + 0.5*cos(2*pi*55*arange(500*2)/500) + 0.5*cos(2*pi*240*arange(500*2)/500) + 0.75*cos(2*pi*100*arange(500*2)/500), sin(2*pi*5*linspace(2, 4, num=500*2)) + 0.5*cos(2*pi*55*linspace(2, 4, num=500*2)) + 0.5*cos(2*pi*240*linspace(2, 4, num=500*2)) + 0.75*cos(2*pi*145*linspace(2, 4, num=500*2)), sin(2*pi*5*linspace(4, 6, num=500*2)) + 0.5*cos(2*pi*55*linspace(4, 6, num=500*2)) + 0.5*cos(2*pi*240*linspace(4, 6, num=500*2)) + 1.2*cos(2*pi*30*linspace(4, 6, num=500*2))))
```

_Setting up a window for signal processing_

---

> Select window = "Hamming Window"
>
> Number of windows = 1

![interface](/photo/property_window_1.png)

_Time Frequency Response of the Signal on the spectogram_

---

![interface](/photo/spectogram_window_1.png)

_Time Frequency Response of the Signal on the 3D-graph_

---

![interface](/photo/3d_graph_window_1.png)

_Setting up a window for signal processing_

---

> Select window = "Hamming Window"
>
> Number of windows = 16

![interface](/photo/property_window_2.png)

_Time Frequency Response of the Signal on the spectogram_

---

![interface](/photo/spectogram_window_2.png)

_Time Frequency Response of the Signal on the 3D-graph_

---

![interface](/photo/3d_graph_window_2.png)
