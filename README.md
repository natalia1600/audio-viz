# Audio Waveform Visualizer

## Introduction

Audio Visualizer for system audio or an uploaded WAV file. It uses PyAudio for audio handling and Pygame for live visualization.


## Description
This program takes in chunks of raw signal data at a time from system audio or uploaded WAV file. For each chunk, it performs FFT (fourier transform) in order to obtain the frequency and amplitude needed to visualize the sound as the audio is playing. 
Using Pygame, rectangles are plotted at intervals across the graphical interface, with the amplitude representing the height of the rectangle at a frequency. For the next chunk of audio, the process is repeated, making the frame rate equal to chunks per second. The data used for visualization is the weighted average of the frequency/amplitude for the current chunk and that of the previous chunk. Color mapping corresponding to the amplitude level is applied to the rectangles, and the entire waveform is reflected along the X axis.


## Installation

Python3 required.

Install dependencies by running:
~~~
pip install -r requirements.txt
~~~


## Usage

* To use with WAV file:
~~~
python3 main.py -i <path_to_WAV_file>
~~~
WAV file will play along with the visualizer.


* To use with live system audio (in progress):
~~~
python3 main.py
~~~
