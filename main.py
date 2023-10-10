import sys
import getopt
import wave
import pyaudio
import pygame
import numpy as np
from log import setup_logger
import matplotlib.pyplot as plt
from scipy.fft import fft
from gui import Visualizer

logger = setup_logger("main")


MAX_AMPLITUDE = 50000
FPS = 60


def main(argv):
    opts, _ = getopt.getopt(argv, "hi:", ["input="])
    for opt, arg in opts:
        if opt == "-h":
            print("main.py -i <wavefile>")
            sys.exit()
        elif opt in ("-i", "--input"):
            run_from_file(arg)
            return

    run_from_sysaudio()


def run_from_sysaudio():
    logger.info("Running visualizer for system audio")


def run_from_file(filepath):
    logger.info(f"Running visualzer for file: {filepath}")
    wavefile = wave.open(filepath, "rb")
    pa = pyaudio.PyAudio()

    # Sample width in bytes
    sample_width = wavefile.getsampwidth()
    dtype = get_dtype(sample_width)

    format = pa.get_format_from_width(sample_width)
    channels = wavefile.getnchannels()
    rate = wavefile.getframerate()

    # Calculate chunk size
    chunk = int((1 / FPS) * rate)

    logger.info(f"sample width: {sample_width}")
    logger.info(f"format      : {format}")
    logger.info(f"channels    : {channels}")
    logger.info(f"sample rate : {rate}")
    logger.info(f"chunk       : {chunk}")

    stream = pa.open(
        format=format,
        channels=channels,
        rate=rate,
        output=True,
    )

    # Window creation
    viz = Visualizer()

    logger.info("Creating window instance")
    # pygame.init()
    # running = True

    frame_counter = 0
    data = wavefile.readframes(chunk)

    logger.info("Starting main loop")
    while data:
        # Handle user inputs
        if viz.should_quit():
            viz.quit()
            break

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        #         running = False

        stream.write(data)
        data = wavefile.readframes(chunk)

        # TODO: create video frame from data
        logger.info(f"Handling frame {frame_counter}")
        handle_chunk(viz, data, dtype, rate)

        # plot_sig_data(data, dtype, rate)
        # display_plots(data, dtype, rate)
        frame_counter += 1

    # Cleanup
    print("Goodbye!")

    wavefile.close()
    stream.close()
    pa.terminate()



def get_dtype(sample_width: int):
    if sample_width == 1:
        return np.int8
    if sample_width == 2:
        return np.int16
    logger.error(f"Invalid sample width: {sample_width}")
    exit(1)


def get_freq_amp(sample_rate, samples):
    T = 1 / sample_rate
    num_samples = samples.size
    fft_sig_abs = abs(fft(samples))
    frequencies = np.linspace(0.0, 1.0 / (2.0 * T), num_samples // 2)
    amplitudes = 2 / num_samples * np.abs(fft_sig_abs[0 : num_samples // 2])
    return (frequencies, amplitudes)


def handle_chunk(viz, data, dtype, sample_rate):
    logger.info(f"Handling chunk (rate: {sample_rate}, dtype: {dtype})")

    sig = np.frombuffer(data, dtype)
    left, _right = sig[0::2], sig[1::2]
    freq_L, amp_L = get_freq_amp(sample_rate, left)

    logger.info(f"Frequencies: {freq_L.shape}")
    logger.info(f"Amplitudes : {amp_L.shape}")

    # FOR NOW IGNORE THE RIGHT CHANNEL
    # freq_R, amp_R = get_freq_amp(sample_rate, right)

    # Update screen
    viz.update(freq_L, amp_L)


def plot_sig_data(label, sig, sample_rate):
    T = 1 / sample_rate
    logger.info("Handling frame")
    # left, right = sig[0::2], sig[1::2]

    fig, (plot_a, plot_b, plot_c) = plt.subplots(3)
    plot_a.plot(sig)
    plot_a.set_xlabel("sample rate * time")
    plot_a.set_ylabel("energy")

    sig_frequencies, sig_amplitudes = get_freq_amp(sample_rate, sig)
    plot_b.semilogy(sig_frequencies, sig_amplitudes)

    plot_b.set_xlabel(label + " - Frequency")
    plot_b.set_ylabel(label + " - Amplitude")

    sig_frequencies, sig_amplitudes = get_freq_amp(sample_rate, sig)
    plot_b.semilogy(sig_frequencies, sig_amplitudes)

    plot_c.specgram(sig, NFFT=1024, Fs=T, noverlap=900)

    plot_c.set_xlabel("Time")
    plot_c.set_ylabel("Frequency")

    plt.suptitle(label + " Waveform")

    plt.show()


def display_plots(data, dtype, sample_rate):
    sig = np.frombuffer(data, dtype)
    left, right = sig[0::2], sig[1::2]
    plot_sig_data("Left", left, sample_rate)
    plot_sig_data("Right", right, sample_rate)


if __name__ == "__main__":
    main(sys.argv[1:])
